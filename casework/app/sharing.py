"""Document sharing (U2.5): completed forms, the whole packet, or
selected parts go to a contact; unchecked parts are excluded
(fx-0020/0045). Rendered artifacts become files rows
(source='produced') and the contact gets an email listing them."""

import hashlib

from app import facts, forms, render


def share_documents(conn, smart_form_id, contact_id, now, workdir,
                    exclude=()):
    """Render every included form except the excluded codes, take
    custody as produced files, and email the contact. Returns the
    produced file ids."""
    email = facts.get_fact(conn, "contact", contact_id, "contact.email")
    if email is None:
        raise ValueError(f"contact {contact_id} has no email fact")
    sf = conn.execute("SELECT contact_id, matter_id FROM smart_forms"
                      " WHERE id=?", (smart_form_id,)).fetchone()
    produced = []
    names = []
    for sff in forms.forms_of(conn, smart_form_id):
        if sff["form_code"] in exclude:
            continue
        out = workdir / f"share-{smart_form_id}-{sff['form_code']}.pdf"
        render.render_form(conn, sff["id"], out)
        content = out.read_bytes()
        name = f"{sff['form_code']}-completed.pdf"
        fid = conn.execute(
            "INSERT INTO files (name, contact_id, matter_id, sha256,"
            " size_bytes, stored_path, source,"
            " produced_from_smart_form_id, uploaded_at,"
            " uploaded_by_user_id) VALUES (?,?,?,?,?,?,'produced',?,?,?)",
            (name, sf["contact_id"], sf["matter_id"],
             hashlib.sha256(content).hexdigest(), len(content), str(out),
             smart_form_id, now, None)).lastrowid
        produced.append(fid)
        names.append(name)
    conn.execute(
        "INSERT INTO email_outbox (recipient, subject, body, template,"
        " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (email, "Documents shared with you",
         "The following completed documents were shared with you:\n- " +
         "\n- ".join(names), "document_share", "smart_forms",
         smart_form_id, now))
    return produced
