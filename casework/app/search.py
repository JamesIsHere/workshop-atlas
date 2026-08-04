"""Universal search (firm-settings.universal-search, fx-0090 +
fx-0212 case-tracking join): one bar over Contacts, Matters, and
Forms by partial name, plus USCIS receipt numbers (full or partial
-- matches surface the carrying matter AND its primary contact).
Selecting a result opens its page; opens feed the Recents button
(most recently accessed contacts and matters, record_access log).
"""


def search(conn, query):
    """Matching records for a partial term, grouped in display
    order: contacts, matters, forms, then receipt-number hits."""
    like = f"%{query.lower()}%"
    out = []
    for r in conn.execute(
            "SELECT id, display_name FROM contacts WHERE deleted_at IS NULL"
            " AND lower(display_name) LIKE ? ORDER BY id", (like,)):
        out.append({"type": "contact", "id": r["id"],
                    "label": r["display_name"]})
    for r in conn.execute(
            "SELECT id, name FROM matters WHERE deleted_at IS NULL"
            " AND lower(name) LIKE ? ORDER BY id", (like,)):
        out.append({"type": "matter", "id": r["id"], "label": r["name"]})
    for r in conn.execute(
            "SELECT id, title FROM smart_forms WHERE deleted_at IS NULL"
            " AND lower(title) LIKE ? ORDER BY id", (like,)):
        out.append({"type": "smart_form", "id": r["id"],
                    "label": r["title"]})
    seen = {(o["type"], o["id"]) for o in out}
    for r in conn.execute(
            "SELECT mr.receipt_number, m.id AS matter_id,"
            " m.name AS matter_name, c.id AS contact_id,"
            " c.display_name FROM matter_receipts mr"
            " JOIN matters m ON m.id=mr.matter_id"
            " JOIN contacts c ON c.id=m.primary_contact_id"
            " WHERE mr.deleted_at IS NULL AND m.deleted_at IS NULL"
            " AND lower(mr.receipt_number) LIKE ? ORDER BY mr.id", (like,)):
        for hit in (
                {"type": "matter", "id": r["matter_id"],
                 "label": r["matter_name"],
                 "receipt_number": r["receipt_number"]},
                {"type": "contact", "id": r["contact_id"],
                 "label": r["display_name"],
                 "receipt_number": r["receipt_number"]}):
            if (hit["type"], hit["id"]) not in seen:
                seen.add((hit["type"], hit["id"]))
                out.append(hit)
    return out


def open_record(conn, user_id, entity_type, entity_id, now):
    """Selecting a result opens its page; contact/matter opens land
    in the access log that feeds Recents."""
    table = {"contact": "contacts", "matter": "matters",
             "smart_form": "smart_forms"}.get(entity_type)
    if table is None:
        raise ValueError(f"unknown entity type {entity_type}")
    row = conn.execute(
        f"SELECT * FROM {table} WHERE id=? AND deleted_at IS NULL",
        (entity_id,)).fetchone()
    if row is None:
        raise ValueError(f"no {entity_type} {entity_id}")
    if entity_type in ("contact", "matter"):
        conn.execute(
            "INSERT INTO record_access (user_id, entity_type, entity_id,"
            " at) VALUES (?,?,?,?)", (user_id, entity_type, entity_id, now))
    return row


def recents(conn, user_id, limit=10):
    """The Recents button: most recently accessed contacts and
    matters, newest first, deduplicated."""
    rows = conn.execute(
        "SELECT entity_type, entity_id, max(id) AS last_id"
        " FROM record_access WHERE user_id=?"
        " GROUP BY entity_type, entity_id"
        " ORDER BY last_id DESC LIMIT ?", (user_id, limit)).fetchall()
    return [{"type": r["entity_type"], "id": r["entity_id"]} for r in rows]
