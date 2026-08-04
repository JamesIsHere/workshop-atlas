"""e-Signature subsystem (U4.2): native signing on stored PDFs.

Capture model per P4 gate ruling 1 (image-class, corpus fx-0194
"drawn or typed"): draw = stroke data posted over the client HTTP
surface, rendered into the PDF as vector strokes; type = a name
rendered as text in a signature style; date fields auto-populate.
No cryptographic signatures. The completed artifact is stamped with
every field value and taken into custody as a produced file under
the source file's contact/matter (auto-filing); its sha256 rides
the audited files insert, signer + timestamp ride esign_events.

Lifecycle: draft (signers/fields editable) -> requested (locked,
signers sign) -> completed (stamped copy filed, everyone notified).
Email only; the SMS channel is deferred (adapted wording).
"""

import io
import json
import secrets
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from app import facts, files

FIELD_TYPES = ("signature", "initials", "text", "date")


def _esign(conn, esign_file_id):
    row = conn.execute(
        "SELECT * FROM esign_files WHERE id=? AND deleted_at IS NULL",
        (esign_file_id,)).fetchone()
    if row is None:
        raise ValueError(f"no e-signature file {esign_file_id}")
    return row


def _require_draft(conn, esign_file_id):
    row = _esign(conn, esign_file_id)
    if row["status"] != "draft":
        raise ValueError("e-signature file is no longer editable"
                         " (signatures already requested)")
    return row


def _event(conn, esign_file_id, event, now, signer_id=None):
    conn.execute(
        "INSERT INTO esign_events (esign_file_id, signer_id, event, at)"
        " VALUES (?,?,?,?)", (esign_file_id, signer_id, event, now))


# --- preparation (fx-0194: setup modal + prepare page) ---

def prepare(conn, file_id, now, user_id):
    """The feather icon: open a stored PDF for e-signing. Only PDFs
    can be prepared (fx-0194)."""
    f = files.get_file(conn, file_id)
    if not f["name"].lower().endswith(".pdf"):
        raise ValueError("only PDF documents can be prepared for"
                         " e-signing")
    esid = conn.execute(
        "INSERT INTO esign_files (file_id, created_at, created_by)"
        " VALUES (?,?,?)", (file_id, now, user_id)).lastrowid
    _event(conn, esid, "prepared", now)
    return esid


def add_signer(conn, esign_file_id, contact_id=None, user_id=None):
    """Signing parties: contacts sign by secure link, firm members on
    the same account sign via the Sign button (fx-0194)."""
    _require_draft(conn, esign_file_id)
    if (contact_id is None) == (user_id is None):
        raise ValueError("exactly one of contact_id/user_id")
    token = secrets.token_hex(16) if contact_id is not None else None
    return conn.execute(
        "INSERT INTO esign_signers (esign_file_id, contact_id, user_id,"
        " access_token) VALUES (?,?,?,?)",
        (esign_file_id, contact_id, user_id, token)).lastrowid


def add_field(conn, esign_file_id, signer_id, field_type, page, x, y):
    """Prepare e-Signature File page: place a field at a document
    location and assign it to a signer."""
    _require_draft(conn, esign_file_id)
    if field_type not in FIELD_TYPES:
        raise ValueError(f"unknown field type {field_type}")
    return conn.execute(
        "INSERT INTO esign_fields (esign_file_id, signer_id, field_type,"
        " page, x, y) VALUES (?,?,?,?,?,?)",
        (esign_file_id, signer_id, field_type, page, x, y)).lastrowid


def remove_field(conn, field_id):
    """The trashcan icon on a placed field (draft only)."""
    row = conn.execute("SELECT esign_file_id FROM esign_fields WHERE id=?",
                       (field_id,)).fetchone()
    if row is None:
        raise ValueError(f"no field {field_id}")
    _require_draft(conn, row["esign_file_id"])
    conn.execute("DELETE FROM esign_fields WHERE id=?", (field_id,))


# --- requests (Send to Unsigned; email only, SMS deferred) ---

def signers_of(conn, esign_file_id):
    return conn.execute(
        "SELECT * FROM esign_signers WHERE esign_file_id=? ORDER BY id",
        (esign_file_id,)).fetchall()


def pending_signers(conn, esign_file_id):
    """Mouseover on a pending status: who still needs to sign."""
    out = []
    for s in signers_of(conn, esign_file_id):
        if s["signed_at"] is not None:
            continue
        out.append(_signer_name(conn, s))
    return out


def _signer_name(conn, signer):
    if signer["contact_id"] is not None:
        return conn.execute("SELECT display_name FROM contacts WHERE id=?",
                            (signer["contact_id"],)).fetchone()["display_name"]
    return conn.execute("SELECT name FROM users WHERE id=?",
                        (signer["user_id"],)).fetchone()["name"]


def _signer_email(conn, signer):
    if signer["contact_id"] is not None:
        return facts.get_fact(conn, "contact", signer["contact_id"],
                              "contact.email")
    return conn.execute("SELECT email FROM users WHERE id=?",
                        (signer["user_id"],)).fetchone()["email"]


def request_signatures(conn, esign_file_id, now):
    """Send to Unsigned: each unsigned signer receives an e-signature
    request by email (adapted: SMS deferred). Re-invoking re-sends to
    the still-unsigned only. After the first send the file is locked."""
    es = _esign(conn, esign_file_id)
    if es["status"] == "completed":
        raise ValueError("e-signature file is already completed")
    f = files.get_file(conn, es["file_id"])
    sent = []
    for s in signers_of(conn, esign_file_id):
        if s["signed_at"] is not None:
            continue
        email = _signer_email(conn, s)
        if email is None:
            raise ValueError(f"signer {s['id']} has no email")
        link = (f"/esign/{s['access_token']}" if s["access_token"]
                else "(sign in-app via the Sign button)")
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, f"Signature requested: {f['name']}",
             f"Please sign {f['name']}: {link}", "esign_request",
             "esign_files", esign_file_id, now))
        _event(conn, esign_file_id, "request_sent", now, s["id"])
        sent.append(s["id"])
    if es["status"] == "draft":
        conn.execute("UPDATE esign_files SET status='requested' WHERE id=?",
                     (esign_file_id,))
    return sent


# --- signing (ruling 1: draw strokes / typed name; date auto) ---

def signer_by_token(conn, token):
    return conn.execute(
        "SELECT * FROM esign_signers WHERE access_token=?",
        (token,)).fetchone()


def fields_of(conn, esign_file_id, signer_id=None):
    q = "SELECT * FROM esign_fields WHERE esign_file_id=?"
    params = [esign_file_id]
    if signer_id is not None:
        q += " AND signer_id=?"
        params.append(signer_id)
    return conn.execute(q + " ORDER BY page, id", params).fetchall()


def _validate_value(field_type, value):
    if field_type in ("signature", "initials"):
        v = json.loads(value)
        if v.get("mode") == "draw":
            if not v.get("strokes"):
                raise ValueError("drawn signature carries no strokes")
        elif v.get("mode") == "type":
            if not v.get("text"):
                raise ValueError("typed signature carries no text")
        else:
            raise ValueError("signature mode must be draw or type")


def sign(conn, esign_file_id, signer_id, values, now, storage_dir):
    """Complete a signer's required fields. values = {field_id:
    value}; signature/initials values are JSON (mode draw|type);
    empty date fields auto-populate from the signing date (fx-0194).
    The signer's copy goes out; the last signature completes the
    file."""
    es = _esign(conn, esign_file_id)
    if es["status"] != "requested":
        raise ValueError("signatures have not been requested")
    signer = conn.execute("SELECT * FROM esign_signers WHERE id=?",
                          (signer_id,)).fetchone()
    if signer is None or signer["esign_file_id"] != esign_file_id:
        raise ValueError(f"no signer {signer_id} on file {esign_file_id}")
    if signer["signed_at"] is not None:
        raise ValueError("signer has already signed")
    for field in fields_of(conn, esign_file_id, signer_id):
        value = values.get(field["id"])
        if value is None and field["field_type"] == "date":
            value = now[:10]
        if value is None:
            raise ValueError(f"field {field['id']} ({field['field_type']})"
                             " is required")
        _validate_value(field["field_type"], value)
        conn.execute("UPDATE esign_fields SET value=? WHERE id=?",
                     (value, field["id"]))
    conn.execute("UPDATE esign_signers SET signed_at=? WHERE id=?",
                 (now, signer_id))
    _event(conn, esign_file_id, "signed", now, signer_id)
    f = files.get_file(conn, es["file_id"])
    _mail_copy(conn, signer, f["name"], "your completed portion",
               esign_file_id, now)
    if all(s["signed_at"] is not None
           for s in signers_of(conn, esign_file_id)):
        _complete(conn, esign_file_id, now, storage_dir)


def _mail_copy(conn, signer, file_name, what, esign_file_id, now):
    email = _signer_email(conn, signer)
    if email is None:
        return
    conn.execute(
        "INSERT INTO email_outbox (recipient, subject, body, template,"
        " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (email, f"Copy of {file_name}",
         f"Attached: {file_name} with {what}.", "esign_copy",
         "esign_files", esign_file_id, now))


# --- completion: stamp, custody, notify (fx-0194/0199) ---

def _overlay_pdf(page_w, page_h, ops):
    """Minimal one-page PDF whose content stream is ops (vector
    strokes + text); merged onto the source page by pypdf."""
    stream = ops.encode("latin-1", "replace")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_w:.2f}"
         f" {page_h:.2f}] /Contents 4 0 R /Resources << /Font"
         " << /F1 5 0 R >> >> >>").encode(),
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
        + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>",
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


def _pdf_escape(text):
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _field_ops(field):
    """Content-stream operators stamping one field at its location."""
    x, y = field["x"], field["y"]
    if field["field_type"] in ("signature", "initials"):
        v = json.loads(field["value"])
        if v["mode"] == "draw":
            ops = ["1.2 w"]
            for stroke in v["strokes"]:
                if len(stroke) < 2:
                    continue
                ops.append(f"{x + stroke[0][0]:.2f} {y + stroke[0][1]:.2f} m")
                for px, py in stroke[1:]:
                    ops.append(f"{x + px:.2f} {y + py:.2f} l")
                ops.append("S")
            return "\n".join(ops)
        text = v["text"]
    else:
        text = field["value"]
    return (f"BT /F1 12 Tf {x:.2f} {y:.2f} Td"
            f" ({_pdf_escape(str(text))}) Tj ET")


def _stamp(source_bytes, fields):
    """Merge every field value onto its page; returns stamped PDF."""
    reader = PdfReader(io.BytesIO(source_bytes))
    writer = PdfWriter(clone_from=reader)
    by_page = {}
    for f in fields:
        by_page.setdefault(f["page"], []).append(f)
    for pageno, page_fields in by_page.items():
        if pageno < 1 or pageno > len(writer.pages):
            raise ValueError(f"field placed on missing page {pageno}")
        page = writer.pages[pageno - 1]
        box = page.mediabox
        ops = "\n".join(_field_ops(f) for f in page_fields)
        overlay = PdfReader(io.BytesIO(
            _overlay_pdf(float(box.width), float(box.height), ops)))
        page.merge_page(overlay.pages[0])
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def _complete(conn, esign_file_id, now, storage_dir):
    """All portions in: stamp the artifact, take produced custody
    under the source file's contact/matter (auto-filing, fx-0199),
    send every signer the completed copy, notify the firm."""
    es = _esign(conn, esign_file_id)
    f = files.get_file(conn, es["file_id"])
    stamped = _stamp(Path(f["stored_path"]).read_bytes(),
                     fields_of(conn, esign_file_id))
    stem = f["name"][:-4] if f["name"].lower().endswith(".pdf") else f["name"]
    signed_id = files.save_produced(
        conn, f"{stem}-signed.pdf", stamped, now, storage_dir,
        contact_id=f["contact_id"], matter_id=f["matter_id"],
        folder_id=f["folder_id"])
    conn.execute(
        "UPDATE esign_files SET status='completed', signed_file_id=?"
        " WHERE id=?", (signed_id, esign_file_id))
    _event(conn, esign_file_id, "completed", now)
    for s in signers_of(conn, esign_file_id):
        _mail_copy(conn, s, f["name"], "all signatures completed",
                   esign_file_id, now)
    _notify_firm(conn, es, f, now)
    return signed_id


def _notify_firm(conn, es_row, file_row, now):
    """Signed notification (fx-0199): email + in-app to the firm.
    Recipients follow the firm notification-settings routing when the
    file rides a matter; otherwise the preparer (or admins)."""
    from app import notify  # lazy: notify retrofits senders in U4.4
    targets = notify.recipients(conn, matter_id=file_row["matter_id"],
                                fallback_user_id=es_row["created_by"])
    payload = json.dumps({"esign_file_id": es_row["id"],
                          "file_id": file_row["id"],
                          "name": file_row["name"]})
    for uid in targets:
        conn.execute(
            "INSERT INTO notifications (user_id, kind, payload, created_at)"
            " VALUES (?,?,?,?)", (uid, "esign_signed", payload, now))
        email = conn.execute("SELECT email FROM users WHERE id=?",
                             (uid,)).fetchone()["email"]
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, f"Signed: {file_row['name']}",
             f"{file_row['name']} was signed by all parties and filed"
             " automatically.", "esign_signed", "esign_files",
             es_row["id"], now))
