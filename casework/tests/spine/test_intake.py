"""Spine tests: intake core (U2.3)."""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import forms, intake, render  # noqa: E402

logging.getLogger("pypdf").setLevel(logging.ERROR)

NOW = "2026-08-01T09:00:00Z"
ADA = 1

G28_CLIENT_FAMILY = "form1[0].#subform[1].Pt3Line5a_FamilyName[0]"
N400_FAMILY = "form1[0].#subform[0].P2_Line1_FamilyName[0]"


def _sf_two_forms(conn):
    return forms.create_smart_form(conn, "Emil N-400 package", NOW, ADA,
                                   contact_id=2,
                                   form_codes=["n-400", "g-28"])


def test_smart_forms_single_intake_autofill(conn):
    """single-intake-autofill: one combined questionnaire; a response
    entered once populates the mapped fields on every selected form
    without re-entry."""
    conn.actor.set("user", ADA)
    sfid = _sf_two_forms(conn)
    items = intake.combined_intake(conn, sfid)
    # the family-name question asks ONCE and feeds both forms
    fam = [i for i in items if i["key"] in
           ("q.n400.family_name", "q.g28.client_family_name")]
    assert len(fam) == 1
    assert set(fam[0]["forms"]) == {"n-400", "g-28"}
    # answer once -> both forms' mapped PDF fields carry the value
    intake.answer_intake(conn, sfid, fam[0]["key"], "Synthetic-Nova", NOW)
    by_code = {r["form_code"]: r for r in forms.forms_of(conn, sfid)}
    assert render.db_values(conn, by_code["n-400"]["id"])[N400_FAMILY] == \
        "Synthetic-Nova"
    assert render.db_values(conn, by_code["g-28"]["id"])[G28_CLIENT_FAMILY] == \
        "Synthetic-Nova"
    # petition-specific answers stay per form
    intake.answer_intake(conn, sfid, "q.n400.date_became_lpr",
                         "2019-01-15", NOW)
    assert render.get_answer(conn, sfid, "q.n400.date_became_lpr") == \
        "2019-01-15"


def test_smart_forms_question_flagging(conn):
    """question-flagging: a flagged question is marked for the client
    and a flagged-only view exists."""
    conn.actor.set("user", ADA)
    sfid = _sf_two_forms(conn)
    intake.flag_question(conn, sfid, "q.n400.a_number")
    client_view = intake.combined_intake(conn, sfid, viewer="invitee")
    marked = {i["key"]: i["flagged"] for i in client_view}
    assert marked["q.n400.a_number"] is True  # client sees the flag
    flagged = intake.combined_intake(conn, sfid, viewer="invitee",
                                     flagged_only=True)
    assert [i["key"] for i in flagged] == ["q.n400.a_number"]
    # unflag clears the filter
    intake.flag_question(conn, sfid, "q.n400.a_number", flagged=False)
    assert intake.combined_intake(conn, sfid, flagged_only=True) == []


def test_smart_forms_question_hiding(conn):
    """question-hiding: a hidden question disappears from the
    invitee's questionnaire; the firm still sees it (eye control)."""
    conn.actor.set("user", ADA)
    sfid = _sf_two_forms(conn)
    intake.hide_question(conn, sfid, "q.n400.uscis_elis_account")
    invitee_keys = {i["key"] for i in
                    intake.combined_intake(conn, sfid, viewer="invitee")}
    assert "q.n400.uscis_elis_account" not in invitee_keys
    firm = {i["key"]: i for i in intake.combined_intake(conn, sfid)}
    assert firm["q.n400.uscis_elis_account"]["hidden"] is True


def test_smart_forms_question_comments(conn):
    """question-comments: comment + @ mention -> the tagged party
    gets an email with a link to the comment and can respond in
    place; tagging an uninvited client prompts granting access."""
    conn.actor.set("user", ADA)
    sfid = _sf_two_forms(conn)
    res = intake.add_comment(conn, sfid, "q.n400.a_number", "user", ADA,
                             "Emil, is this your current A-number?", NOW,
                             mentions=[("contact", 2)])
    assert res["needs_access"] == [2]  # uninvited -> grant prompt
    mail = conn.execute(
        "SELECT * FROM email_outbox WHERE template='question_mention'"
    ).fetchall()
    assert len(mail) == 1
    assert mail[0]["recipient"] == "emil@example.test"
    assert res["link"] in mail[0]["body"]  # link to the comment
    # the contact responds in place -- through their own link (the
    # HTTP leg owed from the U2.3 build, paid at U2.5)
    import tempfile
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _http
    from app import invitations
    inv_id = invitations.invite(conn, sfid, 2, "link", NOW)
    token = conn.execute("SELECT token FROM intake_invitations WHERE id=?",
                         (inv_id,)).fetchone()["token"]
    with tempfile.TemporaryDirectory() as td:
        with _http.client_surface(conn, td) as base:
            status, _body = _http.post_form(
                f"{base}/intake/{token}/comment",
                {"question": "q.n400.a_number",
                 "body": "Yes, that is correct."})
    assert status == 200
    thread = intake.comments_of(conn, sfid, "q.n400.a_number")
    assert [(c["author_type"], c["body"][:3]) for c in thread] == \
        [("user", "Emi"), ("contact", "Yes")]


def test_smart_forms_intake_search(conn):
    """intake-search: keyword search locates questions across all
    tabs for firm and client; hidden questions stay hidden from the
    client's search."""
    conn.actor.set("user", ADA)
    sfid = _sf_two_forms(conn)
    hits = intake.search_questions(conn, sfid, "family")
    assert any(i["key"] == "q.n400.family_name" for i in hits)
    tabs = {i["tab"] for i in intake.search_questions(conn, sfid, "name")}
    assert len(tabs) > 1  # matches located across tabs, no tab-by-tab walk
    intake.hide_question(conn, sfid, "q.n400.family_name")
    client_hits = intake.search_questions(conn, sfid, "family",
                                          viewer="invitee")
    assert not any(i["key"] == "q.n400.family_name" for i in client_hits)


def test_smart_forms_smart_forms_lite(conn):
    """smart-forms-lite: the lite questionnaire carries only
    contact-specific questions; petition fields are edited directly
    on the PDF via the PDF values view."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Emil N-400 lite", NOW, ADA,
                                   contact_id=2, kind="lite",
                                   form_codes=["n-400"])
    keys = {i["key"] for i in intake.combined_intake(conn, sfid)}
    assert "q.n400.family_name" in keys          # contact-specific stays
    assert "q.n400.date_became_lpr" not in keys  # petition question gone
    # petition field is completed on the PDF directly
    sff = forms.forms_of(conn, sfid)[0]
    render.set_pdf_override(
        conn, sff["id"],
        "form1[0].#subform[1].P2_Line9_DateBecamePermanentResident[0]",
        "2019-01-15")
    assert render.pdf_values(conn, sff["id"])[
        "form1[0].#subform[1].P2_Line9_DateBecamePermanentResident[0]"] == \
        "2019-01-15"