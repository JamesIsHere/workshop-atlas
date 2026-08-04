"""Fill + render pipeline (U2.2): fact store -> filled official
AcroForm PDFs (P2 gate ruling 1).

Value resolution order per question source (see forms/README.md):
fact (role contact), registry (role contact display_name), preparer
(preparer user), firm (firm_settings), else form_answers. The
form_field_overrides layer is the PDF-values view: overlays the
computed fill, never syncs back, cleared by sync_database_values.
"""

import logging

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject

from app import facts, forms

logging.getLogger("pypdf").setLevel(logging.ERROR)

READ_ONLY_FLAG = 1  # PDF field flag bit /Ff 1

INTERPRETER_FACTS = {
    "q.interpreter.family_name": "bio.family_name",
    "q.interpreter.given_name": "bio.given_name",
    "q.interpreter.street": "addr.street",
    "q.interpreter.city": "addr.city",
    "q.interpreter.state": "addr.state",
    "q.interpreter.zip": "addr.zip",
    "q.interpreter.phone": "contact.phone",
    "q.interpreter.email": "contact.email",
}
INTERPRETER_ORG_KEY = "q.interpreter.organization"


# --- answers (petition-specific store) ---

def set_answer(conn, smart_form_id, question_key, value, now, idx=0):
    conn.execute(
        "INSERT INTO form_answers (smart_form_id, question_key, idx, value,"
        " updated_at) VALUES (?,?,?,?,?)"
        " ON CONFLICT(smart_form_id, question_key, idx) DO UPDATE SET"
        " value=excluded.value, updated_at=excluded.updated_at",
        (smart_form_id, question_key, idx, value, now))


def get_answer(conn, smart_form_id, question_key, idx=0):
    row = conn.execute(
        "SELECT value FROM form_answers WHERE smart_form_id=? AND"
        " question_key=? AND idx=?",
        (smart_form_id, question_key, idx)).fetchone()
    return row["value"] if row else None


# --- preparer resolution (preparer-population, fx-0038) ---

def preparer_of(conn, smart_form_id):
    """Form-specific preparer overrides the account-level default."""
    row = conn.execute("SELECT preparer_id FROM smart_forms WHERE id=?",
                       (smart_form_id,)).fetchone()
    if row and row["preparer_id"]:
        return row["preparer_id"]
    setting = conn.execute(
        "SELECT value FROM firm_settings WHERE key='preparer.default_user_id'"
    ).fetchone()
    return int(setting["value"]) if setting else None


def _preparer_field(conn, user_id, field):
    if user_id is None:
        return None
    if field == "email":
        row = conn.execute("SELECT email FROM users WHERE id=?",
                           (user_id,)).fetchone()
        return row["email"] if row else None
    row = conn.execute(
        "SELECT value FROM user_settings WHERE user_id=? AND key=?",
        (user_id, f"preparer.{field}")).fetchone()
    if row:
        return row["value"]
    # name-atom fallback: split users.name (first token given, last family)
    if field in ("family_name", "given_name"):
        row = conn.execute("SELECT name FROM users WHERE id=?",
                           (user_id,)).fetchone()
        if row and row["name"]:
            parts = row["name"].split()
            return parts[-1] if field == "family_name" else parts[0]
    return None


def _firm_setting(conn, key):
    row = conn.execute("SELECT value FROM firm_settings WHERE key=?",
                       (key,)).fetchone()
    return row["value"] if row else None


# --- value resolution ---

def resolve_question(conn, smart_form_id, question):
    """Return the resolved value list (index = repeat idx)."""
    source = question.get("source")
    slots = max(1, len(question.get("pdf_fields") or [1]))
    if source is None:
        rows = conn.execute(
            "SELECT idx, value FROM form_answers WHERE smart_form_id=? AND"
            " question_key=? ORDER BY idx",
            (smart_form_id, question["key"])).fetchall()
        vals = [None] * slots
        for r in rows:
            if r["idx"] < slots:
                vals[r["idx"]] = r["value"]
        return vals
    if "fact" in source:
        spec = source["fact"]
        cid = forms.role_contact(conn, smart_form_id,
                                 spec.get("role", "client"))
        if cid is None:
            return [None] * slots
        if question.get("repeating"):
            return [facts.get_fact(conn, spec["subject"], cid, spec["key"], i)
                    for i in range(slots)]
        return [facts.get_fact(conn, spec["subject"], cid, spec["key"])]
    if "registry" in source:
        spec = source["registry"]
        cid = forms.role_contact(conn, smart_form_id, spec["role"])
        if cid is None:
            return [None] * slots
        row = conn.execute(f"SELECT {spec['field']} FROM contacts WHERE id=?",
                           (cid,)).fetchone()
        return [row[spec["field"]] if row else None]
    if "preparer" in source:
        return [_preparer_field(conn, preparer_of(conn, smart_form_id),
                                source["preparer"])]
    if "firm" in source:
        return [_firm_setting(conn, source["firm"])]
    raise ValueError(f"unknown source on {question['key']}: {source}")


def db_values(conn, smart_form_form_id):
    """pdf field -> value as computed from the database (the
    Database-values view)."""
    sff = conn.execute("SELECT * FROM smart_form_forms WHERE id=?",
                       (smart_form_form_id,)).fetchone()
    if sff is None:
        raise ValueError(f"unknown smart_form_form {smart_form_form_id}")
    schema = forms.schema_of(conn, sff["form_edition_id"])
    out = {}
    for q in schema["questions"]:
        vals = resolve_question(conn, sff["smart_form_id"], q)
        for i, field in enumerate(q.get("pdf_fields", [])):
            v = vals[i] if i < len(vals) else None
            if v is not None:
                out[field] = v
    return out


def pdf_values(conn, smart_form_form_id):
    """Database values overlaid with manual PDF-view edits (the
    PDF-values view). Edits never sync back (fx-0020)."""
    out = db_values(conn, smart_form_form_id)
    for r in conn.execute(
            "SELECT field, value FROM form_field_overrides"
            " WHERE smart_form_form_id=?", (smart_form_form_id,)):
        out[r["field"]] = r["value"]
    return out


def set_pdf_override(conn, smart_form_form_id, field, value):
    conn.execute(
        "INSERT INTO form_field_overrides (smart_form_form_id, field, value)"
        " VALUES (?,?,?) ON CONFLICT(smart_form_form_id, field)"
        " DO UPDATE SET value=excluded.value",
        (smart_form_form_id, field, value))


def sync_database_values(conn, smart_form_form_id):
    """Refresh from the database, overwriting manual PDF edits."""
    conn.execute("DELETE FROM form_field_overrides WHERE smart_form_form_id=?",
                 (smart_form_form_id,))


# --- rendering ---

def _print_settings(conn):
    editable = _firm_setting(conn, "print.editable_pdf")
    na = _firm_setting(conn, "print.na_autofill")
    return (editable is None or editable == "1", na == "1")


def _checkbox_on(field):
    for state in field.get("/_States_", []):
        if state != "/Off":
            return state
    return "/Yes"


def render_form(conn, smart_form_form_id, out_path):
    """Fill the official PDF for one included form and write it to
    out_path. Returns the page count."""
    sff = conn.execute("SELECT * FROM smart_form_forms WHERE id=?",
                       (smart_form_form_id,)).fetchone()
    schema = forms.schema_of(conn, sff["form_edition_id"])
    editable, na_autofill = _print_settings(conn)
    values = pdf_values(conn, smart_form_form_id)

    reader = PdfReader(forms.PDFS_DIR / schema["pdf"])
    fields = reader.get_fields() or {}
    writer = PdfWriter(clone_from=reader)

    fill = {}
    for name, value in values.items():
        f = fields.get(name)
        if f is None:
            continue
        if f.get("/FT") == "/Btn":
            truthy = str(value).lower() in ("true", "1", "yes", "y")
            fill[name] = _checkbox_on(f) if truthy else "/Off"
        else:
            fill[name] = str(value)
    if na_autofill:
        for name, f in fields.items():
            if f.get("/FT") == "/Tx" and name not in fill:
                fill[name] = "N/A"

    for page in writer.pages:
        writer.update_page_form_field_values(page, fill,
                                             auto_regenerate=False)
    if not editable:
        for page in writer.pages:
            for annot in page.get("/Annots") or []:
                obj = annot.get_object()
                flags = int(obj.get("/Ff", 0))
                obj[NameObject("/Ff")] = NumberObject(flags | READ_ONLY_FLAG)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return len(writer.pages)


def print_all(conn, smart_form_id, out_path, workdir):
    """Print All: one combined PDF containing every included form
    (fx-0025/0035). Returns (page_count, per_form_pages)."""
    writer = PdfWriter()
    per_form = []
    for sff in forms.forms_of(conn, smart_form_id):
        part = workdir / f"part-{sff['id']}.pdf"
        render_form(conn, sff["id"], part)
        reader = PdfReader(part)
        per_form.append((sff["form_code"], len(reader.pages)))
        for page in reader.pages:
            writer.add_page(page)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return sum(n for _, n in per_form), per_form


# --- import controls (fx-0036, fx-0023, fx-0018) ---

def import_stored_value(conn, smart_form_id, question_key, contact_id,
                        fact_key, now, idx=0, fact_idx=0):
    """Import control: a stored contact fact populates a form field
    without retyping."""
    value = facts.get_fact(conn, "contact", contact_id, fact_key, fact_idx)
    if value is None:
        raise ValueError(f"contact {contact_id} has no {fact_key}")
    set_answer(conn, smart_form_id, question_key, value, now, idx)
    return value


def import_interpreter(conn, smart_form_id, interpreter_contact_id, now):
    """Interpreter import: stored fields populate; organization
    auto-populates once remembered (emp.employer_name)."""
    filled = {}
    for qkey, fkey in INTERPRETER_FACTS.items():
        v = facts.get_fact(conn, "contact", interpreter_contact_id, fkey)
        if v is not None:
            set_answer(conn, smart_form_id, qkey, v, now)
            filled[qkey] = v
    org = facts.get_fact(conn, "contact", interpreter_contact_id,
                         "emp.employer_name")
    if org is not None:
        set_answer(conn, smart_form_id, INTERPRETER_ORG_KEY, org, now)
        filled[INTERPRETER_ORG_KEY] = org
    return filled


def set_interpreter_org(conn, smart_form_id, interpreter_contact_id, org,
                        now):
    """Manual first-time entry; remembered on the interpreter contact
    so subsequent imports auto-populate (fx-0023)."""
    set_answer(conn, smart_form_id, INTERPRETER_ORG_KEY, org, now)
    facts.set_fact(conn, "contact", interpreter_contact_id,
                   "emp.employer_name", org, now)


def import_i129_answers(conn, target_smart_form_id, source_smart_form_id,
                        now):
    """Import Answers for I-129: Application-tab answers only, prior
    answers in that tab overwritten; contact tabs untouched."""
    def app_keys(sfid):
        for sff in forms.forms_of(conn, sfid):
            if sff["form_code"] == "i-129":
                schema = forms.schema_of(conn, sff["form_edition_id"])
                return {q["key"] for q in schema["questions"]
                        if q.get("tab") == "Application"}
        raise ValueError(f"smart form {sfid} does not include an I-129")

    keys = app_keys(target_smart_form_id) & app_keys(source_smart_form_id)
    copied = []
    for r in conn.execute(
            "SELECT question_key, idx, value FROM form_answers"
            " WHERE smart_form_id=?", (source_smart_form_id,)):
        if r["question_key"] in keys:
            set_answer(conn, target_smart_form_id, r["question_key"],
                       r["value"], now, r["idx"])
            copied.append(r["question_key"])
    return sorted(copied)
