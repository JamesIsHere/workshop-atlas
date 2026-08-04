"""Intake core (U2.3): the combined questionnaire over a smart
form's included forms.

One combined intake, deduped by resolved identity: fact-sourced
questions collapse when they resolve to the same (subject, contact,
fact key), so one answer populates every mapped field across every
selected form (single-intake-autofill; invariant 1). Petition-
specific questions keep their per-form keys. The intake is the
WRITE path: answers land in the fact store or form_answers, never
in private copies.
"""

import json

from app import facts, forms, render


def _questions(conn, smart_form_id):
    """All questions across included forms plus the attached custom
    container (custom tabs work on any smart form intake, fx-0020),
    in form/position order."""
    out = []
    for sff in forms.forms_of(conn, smart_form_id):
        schema = forms.schema_of(conn, sff["form_edition_id"])
        for q in schema["questions"]:
            out.append((sff["form_code"], q))
    sf = conn.execute("SELECT custom_intake_id FROM smart_forms WHERE id=?",
                      (smart_form_id,)).fetchone()
    if sf and sf["custom_intake_id"]:
        from app import custom
        for cq in custom.container_questions(conn, sf["custom_intake_id"]):
            q = {"key": f"cq.{cq['id']}", "label": cq["prompt"],
                 "qtype": cq["qtype"], "tab": cq["tab"] or "Custom",
                 "pdf_fields": []}
            if cq["save_to_fact_key"]:
                q["source"] = {"fact": {"subject": "contact",
                                        "role": "client",
                                        "key": cq["save_to_fact_key"]}}
            out.append(("custom", q))
    return out


def _identity(conn, smart_form_id, q):
    """Dedupe identity: fact questions collapse on resolved subject;
    everything else stays per-question-key."""
    source = q.get("source") or {}
    if "fact" in source:
        spec = source["fact"]
        cid = forms.role_contact(conn, smart_form_id,
                                 spec.get("role", "client"))
        return ("fact", spec["subject"], cid, spec["key"])
    if "registry" in source:
        spec = source["registry"]
        cid = forms.role_contact(conn, smart_form_id, spec["role"])
        return ("registry", cid, spec["field"])
    return ("question", q["key"])


def _settings(conn, smart_form_id):
    return {r["question_key"]: r for r in conn.execute(
        "SELECT * FROM question_settings WHERE smart_form_id=?",
        (smart_form_id,))}


def combined_intake(conn, smart_form_id, viewer="firm",
                    flagged_only=False):
    """The single combined questionnaire. viewer='invitee' drops
    hidden questions (question-hiding); flagged_only filters to
    flagged ones (question-flagging). Lite smart forms carry only
    contact-specific questions (smart-forms-lite)."""
    kind = conn.execute("SELECT kind FROM smart_forms WHERE id=?",
                        (smart_form_id,)).fetchone()["kind"]
    settings = _settings(conn, smart_form_id)
    seen = {}
    items = []
    for code, q in _questions(conn, smart_form_id):
        source = q.get("source") or {}
        if kind == "lite" and not ("fact" in source or "registry" in source):
            continue  # petition fields ride the PDF-values view
        ident = _identity(conn, smart_form_id, q)
        if ident in seen:
            seen[ident]["forms"].append(code)
            continue
        s = settings.get(q["key"])
        item = {"key": q["key"], "label": q["label"], "tab": q["tab"],
                "qtype": q["qtype"], "forms": [code],
                "hidden": bool(s and s["hidden"]),
                "flagged": bool(s and s["flagged"])}
        seen[ident] = item
        items.append(item)
    if viewer == "invitee":
        items = [i for i in items if not i["hidden"]]
    if flagged_only:
        items = [i for i in items if i["flagged"]]
    return items


def _find_question(conn, smart_form_id, question_key):
    for _code, q in _questions(conn, smart_form_id):
        if q["key"] == question_key:
            return q
    raise ValueError(f"no question {question_key} on smart form"
                     f" {smart_form_id}")


def answer_intake(conn, smart_form_id, question_key, value, now, idx=0):
    """THE intake write path (invariant 1): fact-sourced answers
    enter the fact store once and flow to every consumer; registry
    answers update the derived label's source; petition answers land
    in form_answers. Answering any member of a deduped group updates
    them all, because they share the store."""
    q = _find_question(conn, smart_form_id, question_key)
    source = q.get("source") or {}
    if "fact" in source:
        spec = source["fact"]
        cid = forms.role_contact(conn, smart_form_id,
                                 spec.get("role", "client"))
        if cid is None:
            raise ValueError(f"no contact for role {spec.get('role')}")
        facts.set_fact(conn, spec["subject"], cid, spec["key"], value,
                       now, idx)
        return ("fact", cid, spec["key"])
    if "registry" in source:
        spec = source["registry"]
        cid = forms.role_contact(conn, smart_form_id, spec["role"])
        if cid is None:
            raise ValueError(f"no contact for role {spec['role']}")
        conn.execute(f"UPDATE contacts SET {spec['field']}=? WHERE id=?",
                     (value, cid))
        return ("registry", cid, spec["field"])
    if "preparer" in source or "firm" in source:
        raise ValueError(f"{question_key} is firm-side data, not an"
                         " intake answer")
    render.set_answer(conn, smart_form_id, question_key, value, now, idx)
    return ("answer", smart_form_id, question_key)


# --- question settings (fx-0031, fx-0020/0041) ---

def _upsert_setting(conn, smart_form_id, question_key, column, value):
    conn.execute(
        f"INSERT INTO question_settings (smart_form_id, question_key,"
        f" {column}) VALUES (?,?,?)"
        f" ON CONFLICT(smart_form_id, question_key) DO UPDATE SET"
        f" {column}=excluded.{column}",
        (smart_form_id, question_key, value))


def flag_question(conn, smart_form_id, question_key, flagged=True):
    _upsert_setting(conn, smart_form_id, question_key, "flagged",
                    int(flagged))


def hide_question(conn, smart_form_id, question_key, hidden=True):
    _upsert_setting(conn, smart_form_id, question_key, "hidden",
                    int(hidden))


# --- comments and mentions (fx-0028/0031) ---

def add_comment(conn, smart_form_id, question_key, author_type, author_id,
                body, now, mentions=()):
    """Comment on a question; @mentions get an email notification
    with a link to the comment. Mentioning a contact with no live
    invitation returns it in needs_access -- the grant prompt; the
    grant itself is the invitation loop (U2.5)."""
    _find_question(conn, smart_form_id, question_key)
    cur = conn.execute(
        "INSERT INTO question_comments (smart_form_id, question_key,"
        " author_type, author_id, body, created_at) VALUES (?,?,?,?,?,?)",
        (smart_form_id, question_key, author_type, author_id, body, now))
    comment_id = cur.lastrowid
    needs_access = []
    link = f"/intake/{smart_form_id}/question/{question_key}#c{comment_id}"
    for kind, target_id in mentions:
        if kind == "user":
            row = conn.execute("SELECT email, name FROM users WHERE id=?",
                               (target_id,)).fetchone()
            email = row["email"] if row else None
        elif kind == "contact":
            email = facts.get_fact(conn, "contact", target_id,
                                   "contact.email")
            live = conn.execute(
                "SELECT count(*) FROM intake_invitations WHERE"
                " smart_form_id=? AND contact_id=? AND status IN"
                " ('sent','accepted','returned')",
                (smart_form_id, target_id)).fetchone()[0]
            if not live:
                needs_access.append(target_id)
        else:
            raise ValueError(f"unknown mention kind {kind}")
        if email:
            conn.execute(
                "INSERT INTO email_outbox (recipient, subject, body,"
                " template, entity_type, entity_id, created_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (email, "You were mentioned on an intake question",
                 f"{body}\n\nRespond here: {link}", "question_mention",
                 "smart_forms", smart_form_id, now))
    return {"comment_id": comment_id, "link": link,
            "needs_access": needs_access}


def comments_of(conn, smart_form_id, question_key):
    return conn.execute(
        "SELECT * FROM question_comments WHERE smart_form_id=? AND"
        " question_key=? ORDER BY id", (smart_form_id, question_key)
    ).fetchall()


# --- search (fx-0030) ---

def search_questions(conn, smart_form_id, keyword, viewer="firm"):
    """Keyword search over the combined intake, across all tabs, for
    firm users and clients alike; the client variant cannot surface
    hidden questions."""
    kw = keyword.lower()
    return [i for i in combined_intake(conn, smart_form_id, viewer=viewer)
            if kw in i["label"].lower()]
