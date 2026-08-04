"""Template automation (U4.3): merge-tagged .docx -> populated
document (fx-0217..0220).

Authoring happens outside the product; the product-side capability
is accepting the .docx, storing it as a named automated template,
and exporting it against a client (required) and matter (optional)
with tags replaced. Tag substitution edits the XML inside the .docx
zip -- stdlib only, no new dependencies (P4 design note).

Vocabulary: a documented subset of the corpus tag families (contact
biographics, address, matter fields, dates -- fx-0219) plus firm-
defined custom attributes, whose labels extend the vocabulary
(#<label-slug>#, fx-0144 join on contacts-and-matters.
custom-attributes).
"""

import io
import re
import zipfile
from datetime import datetime
from pathlib import Path

from app import facts, files

# tag -> (kind, spec); contact facts resolve against the export's
# client, matter facts against its matter
CONTACT_FACT_TAGS = {
    "first_name": "bio.given_name",
    "last_name": "bio.family_name",
    "email": "contact.email",
    "phone": "contact.phone",
    "a_number": "imm.a_number",
    "street": "addr.street",
    "city": "addr.city",
    "state": "addr.state",
    "zip": "addr.zip",
}

TAG_RE = re.compile(r"#([a-z0-9_]+)#")


def upload_template(conn, name, docx_bytes, now, storage_dir):
    """Account Settings > Automated Templates: name + upload
    (fx-0218). The bytes must be a zip (.docx container)."""
    if not zipfile.is_zipfile(io.BytesIO(docx_bytes)):
        raise ValueError("automated templates must be .docx files")
    _sha, stored = files.store_content(storage_dir, docx_bytes)
    return conn.execute(
        "INSERT INTO doc_templates (name, stored_path, created_at)"
        " VALUES (?,?,?)", (name, stored, now)).lastrowid


def list_templates(conn):
    """The templates selectable when creating a new export."""
    return conn.execute(
        "SELECT * FROM doc_templates WHERE deleted_at IS NULL"
        " ORDER BY name, id").fetchall()


def _custom_tags(conn):
    """Firm-defined custom attributes extend the vocabulary: the
    label, slugged, becomes the tag."""
    out = {}
    for d in conn.execute(
            "SELECT * FROM fact_definitions WHERE is_custom=1"):
        slug = re.sub(r"[^a-z0-9]+", "_", d["label"].lower()).strip("_")
        out[slug] = (d["subject_type"], d["key"])
    return out


def _date_long(iso_date):
    d = datetime.strptime(iso_date, "%Y-%m-%d")
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def tag_values(conn, contact_id, now, matter_id=None):
    """Resolve the whole vocabulary for one export. Unknown values
    resolve to '' -- a produced document never carries raw tags."""
    contact = conn.execute("SELECT * FROM contacts WHERE id=?",
                           (contact_id,)).fetchone()
    if contact is None:
        raise ValueError(f"no contact {contact_id}")
    vals = {"full_name": contact["display_name"],
            "today": now[:10], "date_long": _date_long(now[:10])}
    for tag, key in CONTACT_FACT_TAGS.items():
        vals[tag] = facts.get_fact(conn, "contact", contact_id, key)
    if matter_id is not None:
        m = conn.execute("SELECT * FROM matters WHERE id=?",
                         (matter_id,)).fetchone()
        if m is None:
            raise ValueError(f"no matter {matter_id}")
        vals["matter_title"] = m["name"]
        vals["matter_description"] = m["description"]
        vals["matter_applicant"] = conn.execute(
            "SELECT display_name FROM contacts WHERE id=?",
            (m["primary_contact_id"],)).fetchone()["display_name"]
    for slug, (subject, key) in _custom_tags(conn).items():
        subject_id = contact_id if subject == "contact" else matter_id
        if subject_id is not None:
            vals[slug] = facts.get_fact(conn, subject, subject_id, key)
    return {k: (v if v is not None else "") for k, v in vals.items()}


def _substitute(xml_text, vals):
    return TAG_RE.sub(lambda m: vals.get(m.group(1), ""), xml_text)


def export_template(conn, template_id, contact_id, now, matter_id=None):
    """Create New > Template: client required, matter optional
    (fx-0218). Returns the produced .docx bytes with every tag
    replaced by the client's (and matter's) information."""
    t = conn.execute(
        "SELECT * FROM doc_templates WHERE id=? AND deleted_at IS NULL",
        (template_id,)).fetchone()
    if t is None:
        raise ValueError(f"no template {template_id}")
    vals = tag_values(conn, contact_id, now, matter_id=matter_id)
    src = zipfile.ZipFile(io.BytesIO(Path(t["stored_path"]).read_bytes()))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for item in src.infolist():
            content = src.read(item.filename)
            if item.filename.endswith(".xml"):
                content = _substitute(
                    content.decode("utf-8"), vals).encode("utf-8")
            stamped = zipfile.ZipInfo(item.filename, (1980, 1, 1, 0, 0, 0))
            out.writestr(stamped, content)
    return buf.getvalue()
