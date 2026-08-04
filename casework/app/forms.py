"""Forms library and editions (U2.1). Schema-driven engine over the
official AcroForm PDFs in forms/pdfs (P2 gate ruling 1).

The db (form_definitions / form_editions.schema_json) is the runtime
authority; forms/schemas/*.json is its source, loaded by the seed and
by load_library(). Fill/render lives in app/render.py (U2.2); this
module owns the library: definitions, editions with auto-migration
and revert, collections, smart-form creation, role assignment.
"""

import json
from pathlib import Path

FORMS_DIR = Path(__file__).resolve().parent.parent / "forms"
SCHEMAS_DIR = FORMS_DIR / "schemas"
PDFS_DIR = FORMS_DIR / "pdfs"


# --- library ---

def load_library(conn, now):
    """Idempotent: upsert every forms/schemas/*.json as the current
    edition of its form. New (code, edition) pairs migrate prepared
    forms exactly like new_edition()."""
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        register_edition(conn, schema, now)


def register_edition(conn, schema, now):
    """Insert the edition if unseen and make it current; prepared
    forms on older editions migrate automatically (form-updates-
    versioning). Returns the form_editions id."""
    code = schema["code"]
    conn.execute(
        "INSERT INTO form_definitions (code, title, agency, efilable)"
        " VALUES (?,?,?,?) ON CONFLICT(code) DO UPDATE SET"
        " title=excluded.title, agency=excluded.agency,"
        " efilable=excluded.efilable",
        (code, schema["title"], schema["agency"], schema.get("efilable", 0)))
    row = conn.execute(
        "SELECT id, is_current FROM form_editions WHERE form_code=? AND edition=?",
        (code, schema["edition"])).fetchone()
    if row:
        eid = row["id"]
        if not row["is_current"]:
            _make_current(conn, code, eid)
        return eid
    cur = conn.execute(
        "INSERT INTO form_editions (form_code, edition, schema_json, is_current)"
        " VALUES (?,?,?,0)", (code, schema["edition"], json.dumps(schema)))
    eid = cur.lastrowid
    _make_current(conn, code, eid)
    return eid


def _make_current(conn, code, edition_id):
    """Point is_current at edition_id and migrate every prepared form
    from this code's other editions onto it."""
    conn.execute("UPDATE form_editions SET is_current=0"
                 " WHERE form_code=? AND is_current=1 AND id<>?",
                 (code, edition_id))
    conn.execute("UPDATE form_editions SET is_current=1 WHERE id=?",
                 (edition_id,))
    conn.execute(
        "UPDATE smart_form_forms SET form_edition_id=?"
        " WHERE form_edition_id IN (SELECT id FROM form_editions"
        "   WHERE form_code=? AND id<>?)",
        (edition_id, code, edition_id))


def current_edition(conn, code):
    row = conn.execute(
        "SELECT * FROM form_editions WHERE form_code=? AND is_current=1",
        (code,)).fetchone()
    if row is None:
        raise ValueError(f"no current edition for form {code}")
    return row


def editions_of(conn, code):
    """Editions in registration (id) order."""
    return conn.execute(
        "SELECT * FROM form_editions WHERE form_code=? ORDER BY id",
        (code,)).fetchall()


def schema_of(conn, form_edition_id):
    row = conn.execute("SELECT schema_json FROM form_editions WHERE id=?",
                       (form_edition_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown form_edition {form_edition_id}")
    return json.loads(row["schema_json"])


def library(conn):
    """All forms with their current edition."""
    return conn.execute(
        "SELECT fd.code, fd.title, fd.agency, fd.efilable,"
        " fe.id AS edition_id, fe.edition"
        " FROM form_definitions fd"
        " JOIN form_editions fe ON fe.form_code=fd.code AND fe.is_current=1"
        " ORDER BY fd.code").fetchall()


def required_forms(conn, matter_type_id):
    """forms-library criterion: case type -> the required forms."""
    return conn.execute(
        "SELECT mtf.form_code, fd.title FROM matter_type_forms mtf"
        " JOIN form_definitions fd ON fd.code=mtf.form_code"
        " WHERE mtf.matter_type_id=? ORDER BY mtf.position",
        (matter_type_id,)).fetchall()


def set_required_forms(conn, matter_type_id, form_codes):
    conn.execute("DELETE FROM matter_type_forms WHERE matter_type_id=?",
                 (matter_type_id,))
    for pos, code in enumerate(form_codes, 1):
        conn.execute(
            "INSERT INTO matter_type_forms (matter_type_id, form_code, position)"
            " VALUES (?,?,?)", (matter_type_id, code, pos))


# --- collections ---

def create_collection(conn, name, form_codes):
    cur = conn.execute("INSERT INTO form_collections (name) VALUES (?)",
                       (name,))
    cid = cur.lastrowid
    for code in form_codes:
        conn.execute(
            "INSERT INTO form_collection_forms (collection_id, form_code)"
            " VALUES (?,?)", (cid, code))
    return cid


def list_collections(conn):
    """Collections with their form codes, for the new-Smart-Form list."""
    out = []
    for row in conn.execute(
            "SELECT id, name FROM form_collections"
            " WHERE deleted_at IS NULL ORDER BY name"):
        codes = [r["form_code"] for r in conn.execute(
            "SELECT form_code FROM form_collection_forms"
            " WHERE collection_id=? ORDER BY id", (row["id"],))]
        out.append({"id": row["id"], "name": row["name"], "forms": codes})
    return out


# --- smart forms ---

def create_smart_form(conn, title, now, created_by, contact_id=None,
                      matter_id=None, kind="standard", form_codes=(),
                      collection_id=None, preparer_id=None):
    """Create the container and attach forms (individually and/or a
    whole collection at once) at their current editions."""
    codes = list(form_codes)
    if collection_id is not None:
        codes += [r["form_code"] for r in conn.execute(
            "SELECT form_code FROM form_collection_forms"
            " WHERE collection_id=? ORDER BY id", (collection_id,))]
    cur = conn.execute(
        "INSERT INTO smart_forms (title, contact_id, matter_id, preparer_id,"
        " kind, created_at, created_by) VALUES (?,?,?,?,?,?,?)",
        (title, contact_id, matter_id, preparer_id, kind, now, created_by))
    sfid = cur.lastrowid
    primary_roles = set()
    for pos, code in enumerate(codes, 1):
        edition = current_edition(conn, code)
        conn.execute(
            "INSERT INTO smart_form_forms (smart_form_id, form_edition_id,"
            " position, mode) VALUES (?,?,?, 'paper')",
            (sfid, edition["id"], pos))
        pr = json.loads(edition["schema_json"]).get("primary_role")
        if pr:
            primary_roles.add(pr)
    if contact_id is not None:
        # the smart form's contact IS each included form's primary
        # individual unless a role is assigned otherwise -- this is
        # what lets the combined intake dedupe across forms (U2.3)
        for role in {"client"} | primary_roles:
            assign_role(conn, sfid, role, contact_id)
    return sfid


def forms_of(conn, smart_form_id):
    return conn.execute(
        "SELECT sff.*, fe.form_code, fe.edition FROM smart_form_forms sff"
        " JOIN form_editions fe ON fe.id=sff.form_edition_id"
        " WHERE sff.smart_form_id=? ORDER BY sff.position",
        (smart_form_id,)).fetchall()


def assign_role(conn, smart_form_id, role, contact_id):
    conn.execute(
        "INSERT INTO smart_form_contacts (smart_form_id, role, contact_id)"
        " VALUES (?,?,?) ON CONFLICT(smart_form_id, role)"
        " DO UPDATE SET contact_id=excluded.contact_id",
        (smart_form_id, role, contact_id))


def role_contact(conn, smart_form_id, role):
    row = conn.execute(
        "SELECT contact_id FROM smart_form_contacts"
        " WHERE smart_form_id=? AND role=?", (smart_form_id, role)).fetchone()
    if row:
        return row["contact_id"]
    if role == "client":
        row = conn.execute("SELECT contact_id FROM smart_forms WHERE id=?",
                           (smart_form_id,)).fetchone()
        return row["contact_id"] if row else None
    return None


# --- version toggle (form-version-toggle) ---

def switch_version(conn, smart_form_id, direction):
    """USCIS forms with more than one library edition revert together
    (fx-0027); direction is 'previous' or 'latest'. Returns the list
    of (form_code, edition) now in effect."""
    if direction not in ("previous", "latest"):
        raise ValueError("direction must be 'previous' or 'latest'")
    out = []
    for row in forms_of(conn, smart_form_id):
        eds = editions_of(conn, row["form_code"])
        agency = conn.execute(
            "SELECT agency FROM form_definitions WHERE code=?",
            (row["form_code"],)).fetchone()["agency"]
        if agency != "USCIS" or len(eds) < 2:
            out.append((row["form_code"], row["edition"]))
            continue
        ids = [e["id"] for e in eds]
        target = ids[-2] if direction == "previous" else ids[-1]
        conn.execute("UPDATE smart_form_forms SET form_edition_id=?"
                     " WHERE id=?", (target, row["id"]))
        edition = conn.execute("SELECT edition FROM form_editions WHERE id=?",
                               (target,)).fetchone()["edition"]
        out.append((row["form_code"], edition))
    return out
