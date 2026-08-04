"""Notes (U1.5): creation surfaces, assignment, client association,
categories, pinning, PDF export.

Creation scoping mirrors the spec: dashboard notes start
unassociated; contact-tab notes associate the contact; matter-tab
notes associate the matter AND its primary contact.
"""


def create_note(conn, body, now, created_by, title=None, contact_id=None,
                matter_id=None, category_id=None, notify_all=0):
    if matter_id is not None and contact_id is None:
        contact_id = conn.execute(
            "SELECT primary_contact_id FROM matters WHERE id=?",
            (matter_id,)).fetchone()["primary_contact_id"]
    nid = conn.execute(
        "INSERT INTO notes (title, body, contact_id, matter_id,"
        " category_id, notify_all, created_at, created_by)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (title, body, contact_id, matter_id, category_id, notify_all,
         now, created_by)).lastrowid
    # creator is the default assignee
    conn.execute("INSERT INTO note_assignees (note_id, user_id)"
                 " VALUES (?,?)", (nid, created_by))
    if notify_all:
        for (uid,) in conn.execute(
                "SELECT id FROM users WHERE deleted_at IS NULL AND"
                " deactivated_at IS NULL AND id != ?", (created_by,)):
            conn.execute(
                "INSERT INTO notifications (user_id, kind, payload,"
                " created_at) VALUES (?,?,?,?)",
                (uid, "note_notify_all", str(nid), now))
    return nid


def assign(conn, note_id, user_id):
    conn.execute("INSERT INTO note_assignees (note_id, user_id)"
                 " VALUES (?,?)", (note_id, user_id))


def unassign(conn, note_id, user_id):
    conn.execute("DELETE FROM note_assignees WHERE note_id=? AND"
                 " user_id=?", (note_id, user_id))


def assignees(conn, note_id):
    return [r["user_id"] for r in conn.execute(
        "SELECT user_id FROM note_assignees WHERE note_id=? ORDER BY"
        " user_id", (note_id,))]


def set_client(conn, note_id, contact_id=None, matter_id=None):
    """Update the note's association; picking a matter also brings its
    primary contact."""
    if matter_id is not None and contact_id is None:
        contact_id = conn.execute(
            "SELECT primary_contact_id FROM matters WHERE id=?",
            (matter_id,)).fetchone()["primary_contact_id"]
    conn.execute("UPDATE notes SET contact_id=?, matter_id=? WHERE id=?",
                 (contact_id, matter_id, note_id))


def create_category(conn, name):
    return conn.execute("INSERT INTO note_categories (name, builtin)"
                        " VALUES (?, 0)", (name,)).lastrowid


def pin(conn, note_id, pinned=True):
    conn.execute("UPDATE notes SET pinned=? WHERE id=?",
                 (1 if pinned else 0, note_id))


def list_notes(conn, contact_id=None, matter_id=None, category_id=None):
    """Dashboard (no scope) or a contact/matter Notes tab; pinned
    notes first, then newest."""
    q = "SELECT id FROM notes WHERE deleted_at IS NULL"
    params = []
    if contact_id is not None:
        q += " AND contact_id=?"
        params.append(contact_id)
    if matter_id is not None:
        q += " AND matter_id=?"
        params.append(matter_id)
    if category_id is not None:
        q += " AND category_id=?"
        params.append(category_id)
    q += " ORDER BY pinned DESC, created_at DESC, id DESC"
    return [r["id"] for r in conn.execute(q, params)]


# --- PDF export (minimal stdlib writer; uncompressed streams) ---

def _pdf_escape(text):
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _pdf(lines):
    """One-page PDF carrying the given text lines."""
    content = ["BT /F1 11 Tf 50 780 Td 14 TL"]
    for line in lines:
        content.append(f"({_pdf_escape(line)}) Tj T*")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", "replace")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]"
        b" /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
        + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    return bytes(out)


def export_notes_pdf(conn, contact_id=None, matter_id=None):
    """The Notes tab's Export button: a PDF of that scope's notes."""
    ids = list_notes(conn, contact_id=contact_id, matter_id=matter_id)
    lines = ["Notes export"]
    for nid in ids:
        n = conn.execute("SELECT * FROM notes WHERE id=?", (nid,)).fetchone()
        cat = ""
        if n["category_id"]:
            cat = " [" + conn.execute(
                "SELECT name FROM note_categories WHERE id=?",
                (n["category_id"],)).fetchone()["name"] + "]"
        lines.append(f"{n['created_at']}{cat} {n['title'] or ''}")
        lines.extend(n["body"].splitlines())
        lines.append("")
    return _pdf(lines)
