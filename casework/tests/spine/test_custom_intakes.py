"""Spine tests: custom intakes, document requests, templates (U2.4)."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import custom, facts, forms, intake, render  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA = 1


def _basic_container(conn):
    """Container with premade + custom + document-request questions."""
    ci = custom.create_custom_intake(conn, "AoS Basic Intake", NOW)
    tab = custom.add_tab(conn, ci, "Background", 1)
    premade = custom.add_question(conn, ci, tab, "Given name", "premade", 1,
                                  save_to_fact_key="bio.given_name")
    free = custom.add_question(conn, ci, tab, "How did you hear about us?",
                               "text", 2)
    docreq = custom.add_question(conn, ci, tab,
                                 "Upload your passport photo page",
                                 "document_request", 3)
    return ci, premade, free, docreq


def test_smart_forms_custom_intakes(conn):
    """custom-intakes: firm builds a custom questionnaire and shares
    it; the client completes it and pre-made question answers save to
    their contact record."""
    conn.actor.set("user", ADA)
    ci, premade, free, _ = _basic_container(conn)
    sfid = custom.instantiate(conn, ci, "Hana AoS intake", NOW, ADA,
                              contact_id=5, matter_id=None)
    items = {i["key"]: i for i in intake.combined_intake(conn, sfid)}
    assert f"cq.{premade}" in items and f"cq.{free}" in items
    assert items[f"cq.{premade}"]["tab"] == "Background"
    # client answers: the premade answer lands on the CONTACT RECORD
    intake.answer_intake(conn, sfid, f"cq.{premade}", "Hana-Updated", NOW)
    assert facts.get_fact(conn, "contact", 5, "bio.given_name") == \
        "Hana-Updated"
    # the free-text answer stays with the intake
    intake.answer_intake(conn, sfid, f"cq.{free}", "A friend", NOW)
    assert render.get_answer(conn, sfid, f"cq.{free}") == "A friend"


def test_smart_forms_custom_questions(conn):
    """custom-questions (+ the OWED custom-attributes intake leg):
    a custom question on a custom tab is answerable by the invitee
    and its answer can save to a custom attribute; custom tabs work
    on any smart form intake."""
    conn.actor.set("user", ADA)
    key = facts.define_custom_attribute(conn, "referral-source", "contact",
                                        "text", "Referral source")
    ci = custom.create_custom_intake(conn, "Extras", NOW)
    tab = custom.add_tab(conn, ci, "Extra Questions", 1)
    saved = custom.add_question(conn, ci, tab, "Who referred you?", "text",
                                1, save_to_fact_key=key)
    # all custom types are addable
    for pos, qt in enumerate(("number", "date", "boolean", "list",
                              "expiry", "document_request"), 2):
        custom.add_question(conn, ci, tab, f"Probe {qt}", qt, pos,
                            list_options='["a","b"]' if qt == "list" else None)
    # attach to a STANDARD smart form -- custom tabs on any intake
    sfid = forms.create_smart_form(conn, "Dana G-28", NOW, ADA,
                                   contact_id=1, form_codes=["g-28"])
    custom.attach_container(conn, sfid, ci)
    invitee = {i["key"]: i for i in
               intake.combined_intake(conn, sfid, viewer="invitee")}
    assert f"cq.{saved}" in invitee  # invitee sees and can answer it
    intake.answer_intake(conn, sfid, f"cq.{saved}", "Emil Synthetic", NOW)
    # the answer saved to the custom attribute on the contact
    assert facts.get_fact(conn, "contact", 1, key) == "Emil Synthetic"
    # duplicate tab names are refused (fx-0020)
    try:
        custom.add_tab(conn, ci, "Extra Questions", 9)
        raise AssertionError("duplicate tab name accepted")
    except Exception:
        pass


def test_smart_forms_document_requests(conn):
    """document-requests: client uploads against a document request
    save under the intake's contact and matter; multiple files per
    request."""
    conn.actor.set("user", ADA)
    ci, _premade, _free, docreq = _basic_container(conn)
    sfid = custom.instantiate(conn, ci, "Dana AoS intake", NOW, ADA,
                              contact_id=1, matter_id=1)
    with tempfile.TemporaryDirectory() as td:
        f1 = custom.save_client_upload(conn, sfid, "passport.pdf",
                                       b"%PDF-synthetic-passport", NOW,
                                       Path(td), question_id=docreq)
        f2 = custom.save_client_upload(conn, sfid, "passport-back.pdf",
                                       b"%PDF-synthetic-back", NOW,
                                       Path(td), question_id=docreq)
        rows = custom.request_uploads(conn, sfid, docreq)
    assert [r["id"] for r in rows] == [f1, f2]  # multiple per request
    for r in rows:
        assert (r["contact_id"], r["matter_id"]) == (1, 1)  # custody rule
        assert r["source"] == "client"


def test_smart_forms_client_file_upload(conn):
    """client-file-upload: Upload File during the questionnaire
    attaches the file and the firm can see it."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Emil N-400", NOW, ADA,
                                   contact_id=2, matter_id=2,
                                   form_codes=["n-400"])
    with tempfile.TemporaryDirectory() as td:
        fid = custom.save_client_upload(conn, sfid, "evidence.pdf",
                                        b"%PDF-synthetic-evidence", NOW,
                                        Path(td))
        row = conn.execute("SELECT * FROM files WHERE id=?",
                           (fid,)).fetchone()
        assert Path(row["stored_path"]).exists()  # firm can retrieve it
    assert (row["contact_id"], row["matter_id"]) == (2, 2)
    assert row["uploaded_by_contact_id"] == 2


def test_smart_forms_templated_intakes(conn):
    """templated-intakes: a saved template captures forms, custom
    questions, and question settings; a new Smart Form from it
    carries all three. Comments do not travel (fx-0041)."""
    conn.actor.set("user", ADA)
    ci, premade, free, _ = _basic_container(conn)
    sfid = forms.create_smart_form(conn, "Emil package", NOW, ADA,
                                   contact_id=2,
                                   form_codes=["n-400", "g-28"])
    custom.attach_container(conn, sfid, ci)
    intake.hide_question(conn, sfid, "q.n400.uscis_elis_account")
    intake.flag_question(conn, sfid, f"cq.{free}")
    intake.add_comment(conn, sfid, f"cq.{free}", "user", ADA,
                       "internal note", NOW)
    tid = custom.save_template(conn, sfid, "N-400 Standard Package", NOW)
    new = custom.create_from_template(conn, tid, "Gil package", NOW, ADA,
                                      contact_id=4)
    # forms travelled
    assert [r["form_code"] for r in forms.forms_of(conn, new)] == \
        ["n-400", "g-28"]
    # custom questions travelled (fresh ids, same prompts); the
    # premade given-name question DEDUPES into N-400's given-name
    # item (same contact, same fact key) -- the combined-intake rule
    items = intake.combined_intake(conn, new)
    prompts = {i["label"] for i in items}
    assert {"How did you hear about us?",
            "Upload your passport photo page"} <= prompts
    given = [i for i in items
             if i["key"] in ("q.n400.given_name",)]
    assert given and "custom" in given[0]["forms"]  # premade merged in
    # settings travelled: the same form question is hidden, the
    # cloned custom question is flagged
    by_key = {i["key"]: i for i in items}
    assert by_key["q.n400.uscis_elis_account"]["hidden"] is True
    flagged = [i for i in items if i["flagged"]]
    assert len(flagged) == 1
    assert flagged[0]["label"] == "How did you hear about us?"
    # comments did NOT travel
    assert intake.comments_of(conn, new, flagged[0]["key"]) == []