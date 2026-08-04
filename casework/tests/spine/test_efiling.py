"""Spine tests: submission-ready packages (U2.7, e-filing family
adapted -- government submission out, artifacts in)."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import efiling, forms, intake, render  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA = 1

N400_FAMILY = "form1[0].#subform[0].P2_Line1_FamilyName[0]"


def _n400_package(conn):
    return forms.create_smart_form(conn, "Emil N-400 e-file", NOW, ADA,
                                   contact_id=2,
                                   form_codes=["n-400", "g-28"])


def _complete_n400(conn, sfid):
    """Answer everything the validator requires."""
    intake.answer_intake(conn, sfid, "q.n400.middle_name", "N/A", NOW)
    intake.answer_intake(conn, sfid, "q.n400.date_became_lpr",
                         "2019-01-15", NOW)
    intake.answer_intake(conn, sfid, "q.n400.uscis_elis_account",
                         "SYNTH-ELIS-1", NOW)
    intake.answer_intake(conn, sfid, "q.g28.client_phone",
                         "+1-555-0102", NOW)
    intake.answer_intake(conn, sfid, "q.g28.client_street",
                         "300 Synthetic Ave", NOW)
    intake.answer_intake(conn, sfid, "q.g28.client_city", "Faketown", NOW)
    intake.answer_intake(conn, sfid, "q.g28.client_state", "VA", NOW)
    intake.answer_intake(conn, sfid, "q.g28.client_zip", "00003", NOW)
    intake.answer_intake(conn, sfid, "q.g28.appearance_form_number",
                         "N-400", NOW)
    intake.answer_intake(conn, sfid, "q.g28.receipt_number", "N/A", NOW)


def test_smart_forms_efiling_validation(conn):
    """efiling-validation (adapted): an incomplete questionnaire
    yields a per-question error list with links; package export is
    blocked until re-validation passes."""
    conn.actor.set("user", ADA)
    sfid = _n400_package(conn)
    efiling.toggle_paper(conn, sfid, "efile_package")
    errors = efiling.validate(conn, sfid)
    assert errors, "incomplete questionnaire must produce errors"
    missing = {e["question"] for e in errors}
    assert "q.n400.middle_name" in missing  # Emil has no middle name yet
    for e in errors:
        assert e["link"].endswith(e["question"])  # Go-to-question link
        assert e["reason"]                        # with an explanation
    # export is BLOCKED while errors remain
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        try:
            efiling.export_package(conn, sfid, td / "pkg", td)
            raise AssertionError("export succeeded with a failing"
                                 " validation")
        except efiling.EfilingBlocked as e:
            assert len(e.errors) == len(errors)
        # fix everything, re-validate, and the block lifts
        _complete_n400(conn, sfid)
        assert efiling.validate(conn, sfid) == []
        manifest = efiling.export_package(conn, sfid, td / "pkg", td)
    assert manifest["forms"] == ["n-400"]


def test_smart_forms_uscis_efiling_sync(conn):
    """uscis-efiling-sync (adapted): validated questionnaire -> a
    submission-ready package (form artifact + structured field
    payload) with the G-28 attached; my.uscis.gov sync is out."""
    conn.actor.set("user", ADA)
    sfid = _n400_package(conn)
    efiling.toggle_paper(conn, sfid, "efile_package")
    _complete_n400(conn, sfid)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        manifest = efiling.export_package(conn, sfid, td / "pkg", td)
        pkg = td / "pkg"
        assert (pkg / "n-400.pdf").exists()      # the form artifact
        assert (pkg / "g-28.pdf").exists()       # attached G-28 (fx-0017)
        payload = json.loads((pkg / "n-400.json").read_text())
    assert manifest["attached_g28"] is True
    assert payload["edition"] == "01/20/25"
    assert payload["fields"][N400_FAMILY] == "Synthetic"  # from the facts


def test_smart_forms_efiling_paper_toggle(conn):
    """efiling-paper-toggle (adapted): the N-400 switches between
    e-file-package and paper without recreating the intake."""
    conn.actor.set("user", ADA)
    sfid = _n400_package(conn)
    intake.answer_intake(conn, sfid, "q.n400.date_became_lpr",
                         "2019-01-15", NOW)
    sff_id = efiling.toggle_paper(conn, sfid, "efile_package")
    mode = conn.execute("SELECT mode FROM smart_form_forms WHERE id=?",
                        (sff_id,)).fetchone()["mode"]
    assert mode == "efile_package"
    # back to paper: same smart form, same intake, answers intact
    efiling.toggle_paper(conn, sfid, "paper")
    mode = conn.execute("SELECT mode FROM smart_form_forms WHERE id=?",
                        (sff_id,)).fetchone()["mode"]
    assert mode == "paper"
    assert render.get_answer(conn, sfid, "q.n400.date_became_lpr") == \
        "2019-01-15"  # nothing was recreated
    # the toggle is an N-400 capability (fx-0017)
    other = forms.create_smart_form(conn, "Dana I-130", NOW, ADA,
                                    contact_id=1, form_codes=["i-130"])
    try:
        efiling.toggle_paper(conn, other, "efile_package")
        raise AssertionError("toggle accepted without an N-400")
    except ValueError:
        pass


def test_smart_forms_h1b_electronic_registration(conn):
    """h1b-electronic-registration (adapted): one registration Smart
    Form for the employer and up to 20 selected beneficiaries; bulk
    limit enforced; e-filing itself is out."""
    conn.actor.set("user", ADA)
    sfid = efiling.create_h1b_registration(conn, 7, [1, 2, 4],
                                           "H-1B cap registrations", NOW,
                                           ADA)
    kind = conn.execute("SELECT kind FROM smart_forms WHERE id=?",
                        (sfid,)).fetchone()["kind"]
    assert kind == "h1b_registration"
    payload = efiling.registration_payload(conn, sfid)
    assert payload["employer"] == "Synthetic Staffing LLC"
    assert [b["given_name"] for b in payload["beneficiaries"]] == \
        ["Dana", "Emil", "Gil"]
    # the 20-beneficiary bulk limit is enforced (fx-0013)
    try:
        efiling.create_h1b_registration(conn, 7, list(range(1, 23)),
                                        "too many", NOW, ADA)
        raise AssertionError("21+ beneficiaries accepted")
    except ValueError:
        pass