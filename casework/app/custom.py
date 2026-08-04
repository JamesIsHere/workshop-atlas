"""Custom intakes, custom questions, document requests, client
uploads, and intake templates (U2.4).

A custom_intakes row is a reusable question container (tabs +
questions). A kind='custom_intake' smart form is the container
alone; attaching a container to any smart form gives that intake
custom tabs (fx-0020/0029). Premade questions save to standard fact
keys -- the contact record; custom questions may save to custom
attributes (custom.* keys). Upload custody is minimal here (files
row + sha-named content); file management proper is P4.
"""

import json

from app import facts, forms, render

QTYPES = ("text", "textarea", "number", "date", "boolean", "list",
          "expiry", "document_request", "premade")


# --- containers ---

def create_custom_intake(conn, name, now):
    return conn.execute(
        "INSERT INTO custom_intakes (name, created_at) VALUES (?,?)",
        (name, now)).lastrowid


def add_tab(conn, custom_intake_id, name, position):
    """Custom tabs require unique names within their intake."""
    return conn.execute(
        "INSERT INTO custom_intake_tabs (custom_intake_id, name, position)"
        " VALUES (?,?,?)", (custom_intake_id, name, position)).lastrowid


def add_question(conn, custom_intake_id, tab_id, prompt, qtype, position,
                 save_to_fact_key=None, list_options=None):
    """qtype 'premade' MUST save to a standard fact key (that is what
    premade means: the answer lands on the contact record); custom
    qtypes may save to a custom attribute."""
    if qtype not in QTYPES:
        raise ValueError(f"unknown question type {qtype}")
    if qtype == "premade" and not save_to_fact_key:
        raise ValueError("premade questions save to a fact key")
    if save_to_fact_key:
        row = conn.execute("SELECT key FROM fact_definitions WHERE key=?",
                           (save_to_fact_key,)).fetchone()
        if row is None:
            raise ValueError(f"unknown fact key {save_to_fact_key}")
    qid = conn.execute(
        "INSERT INTO custom_questions (prompt, qtype, save_to_fact_key,"
        " list_options) VALUES (?,?,?,?)",
        (prompt, qtype, save_to_fact_key, list_options)).lastrowid
    conn.execute(
        "INSERT INTO custom_intake_questions (custom_intake_id, tab_id,"
        " question_id, position) VALUES (?,?,?,?)",
        (custom_intake_id, tab_id, qid, position))
    return qid


def container_questions(conn, custom_intake_id):
    """Questions with their tab names, in tab/position order."""
    return conn.execute(
        "SELECT cq.id, cq.prompt, cq.qtype, cq.save_to_fact_key,"
        " cq.list_options, t.name AS tab, ciq.position"
        " FROM custom_intake_questions ciq"
        " JOIN custom_questions cq ON cq.id=ciq.question_id"
        " LEFT JOIN custom_intake_tabs t ON t.id=ciq.tab_id"
        " WHERE ciq.custom_intake_id=?"
        " ORDER BY t.position, ciq.position", (custom_intake_id,)).fetchall()


def attach_container(conn, smart_form_id, custom_intake_id):
    """Custom questions can be added to any smart form intake."""
    conn.execute("UPDATE smart_forms SET custom_intake_id=? WHERE id=?",
                 (custom_intake_id, smart_form_id))


def instantiate(conn, custom_intake_id, title, now, created_by,
                contact_id, matter_id=None):
    """A custom intake shared with a client is created as a Smart
    Form (fx-0026/0029)."""
    sfid = forms.create_smart_form(conn, title, now, created_by,
                                   contact_id=contact_id,
                                   matter_id=matter_id,
                                   kind="custom_intake")
    attach_container(conn, sfid, custom_intake_id)
    return sfid


# --- upload custody (minimal; management is P4) ---

def _store_content(storage_dir, filename, content):
    from app import files as files_mod  # lazy: files.py is the custody home
    return files_mod.store_content(storage_dir, content)


def save_client_upload(conn, smart_form_id, filename, content, now,
                       storage_dir, question_id=None):
    """Client upload during a questionnaire. Files save under the
    intake's contact and matter; a document-request upload is also
    linked to its question (next idx slot -> multiple files per
    request)."""
    sf = conn.execute("SELECT contact_id, matter_id FROM smart_forms"
                      " WHERE id=?", (smart_form_id,)).fetchone()
    sha, stored = _store_content(storage_dir, filename, content)
    fid = conn.execute(
        "INSERT INTO files (name, contact_id, matter_id, sha256,"
        " size_bytes, stored_path, source, uploaded_at,"
        " uploaded_by_contact_id) VALUES (?,?,?,?,?,?,'client',?,?)",
        (filename, sf["contact_id"], sf["matter_id"], sha, len(content),
         stored, now, sf["contact_id"])).lastrowid
    if question_id is not None:
        row = conn.execute(
            "SELECT qtype FROM custom_questions WHERE id=?",
            (question_id,)).fetchone()
        if row is None or row["qtype"] != "document_request":
            raise ValueError(f"question {question_id} is not a document"
                             " request")
        nxt = conn.execute(
            "SELECT coalesce(max(idx)+1, 0) FROM form_answers WHERE"
            " smart_form_id=? AND question_key=?",
            (smart_form_id, f"cq.{question_id}")).fetchone()[0]
        render.set_answer(conn, smart_form_id, f"cq.{question_id}",
                          str(fid), now, idx=nxt)
    return fid


def request_uploads(conn, smart_form_id, question_id):
    """Files collected against a document request, in upload order."""
    return conn.execute(
        "SELECT f.* FROM form_answers fa JOIN files f"
        " ON f.id=CAST(fa.value AS INTEGER)"
        " WHERE fa.smart_form_id=? AND fa.question_key=? ORDER BY fa.idx",
        (smart_form_id, f"cq.{question_id}")).fetchall()


# --- templates (templated-intakes, fx-0041) ---

def save_template(conn, smart_form_id, name, now):
    """Capture forms, custom tabs/questions, and question settings.
    Comments are NOT saved to templates (fx-0041)."""
    sf = conn.execute("SELECT * FROM smart_forms WHERE id=?",
                      (smart_form_id,)).fetchone()
    config = {
        "kind": sf["kind"],
        "forms": [r["form_code"] for r in forms.forms_of(conn, smart_form_id)],
        "questions": [
            {"tab": q["tab"], "prompt": q["prompt"], "qtype": q["qtype"],
             "save_to_fact_key": q["save_to_fact_key"],
             "list_options": q["list_options"], "position": q["position"]}
            for q in (container_questions(conn, sf["custom_intake_id"])
                      if sf["custom_intake_id"] else [])],
        "settings": [],
    }
    # custom-question settings travel by list index (ids change on
    # clone); form-question settings travel by their stable q.* key
    cq_index = {f"cq.{q['id']}": i for i, q in enumerate(
        container_questions(conn, sf["custom_intake_id"])
        if sf["custom_intake_id"] else [])}
    for r in conn.execute(
            "SELECT question_key, hidden, flagged FROM question_settings"
            " WHERE smart_form_id=? ORDER BY question_key",
            (smart_form_id,)):
        entry = {"hidden": r["hidden"], "flagged": r["flagged"]}
        if r["question_key"] in cq_index:
            entry["cq_index"] = cq_index[r["question_key"]]
        else:
            entry["question_key"] = r["question_key"]
        config["settings"].append(entry)
    return conn.execute(
        "INSERT INTO intake_templates (name, config_json, created_at)"
        " VALUES (?,?,?)", (name, json.dumps(config), now)).lastrowid


def create_from_template(conn, template_id, title, now, created_by,
                         contact_id, matter_id=None):
    """Reusing a template follows the normal new-Smart-Form flow; the
    new intake carries the template's forms, custom questions, and
    question settings."""
    row = conn.execute("SELECT * FROM intake_templates WHERE id=?",
                       (template_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown template {template_id}")
    config = json.loads(row["config_json"])
    sfid = forms.create_smart_form(conn, title, now, created_by,
                                   contact_id=contact_id,
                                   matter_id=matter_id,
                                   kind=config.get("kind", "standard"),
                                   form_codes=config["forms"])
    new_cq_ids = []
    if config["questions"]:
        container = create_custom_intake(conn, f"{row['name']} (from"
                                         " template)", now)
        tabs = {}
        for q in config["questions"]:
            tab_name = q["tab"] or "Custom"
            if tab_name not in tabs:
                tabs[tab_name] = add_tab(conn, container, tab_name,
                                         len(tabs) + 1)
            qid = conn.execute(
                "INSERT INTO custom_questions (prompt, qtype,"
                " save_to_fact_key, list_options) VALUES (?,?,?,?)",
                (q["prompt"], q["qtype"], q["save_to_fact_key"],
                 q["list_options"])).lastrowid
            conn.execute(
                "INSERT INTO custom_intake_questions (custom_intake_id,"
                " tab_id, question_id, position) VALUES (?,?,?,?)",
                (container, tabs[tab_name], qid, q["position"]))
            new_cq_ids.append(qid)
        attach_container(conn, sfid, container)
    for s in config["settings"]:
        if "cq_index" in s:
            key = f"cq.{new_cq_ids[s['cq_index']]}"
        else:
            key = s["question_key"]
        conn.execute(
            "INSERT INTO question_settings (smart_form_id, question_key,"
            " hidden, flagged) VALUES (?,?,?,?)",
            (sfid, key, s["hidden"], s["flagged"]))
    return sfid
