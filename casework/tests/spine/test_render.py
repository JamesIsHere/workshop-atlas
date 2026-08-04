"""Spine tests: fill + render pipeline and import controls (U2.2)."""

import logging
import sys
import tempfile
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import facts, forms, render  # noqa: E402

logging.getLogger("pypdf").setLevel(logging.ERROR)

NOW = "2026-08-01T09:00:00Z"
ADA = 1

G28_CLIENT_FAMILY = "form1[0].#subform[1].Pt3Line5a_FamilyName[0]"
G28_BAR_NUMBER = "form1[0].#subform[0].Pt2Line1b_BarNumber[0]"
G28_ATTY_EMAIL = "form1[0].#subform[0].Line6_EMail[0]"
G28_ATTY_FAMILY = "form1[0].#subform[0].Pt1Line2a_FamilyName[0]"
G28_FIRM_NAME = "form1[0].#subform[0].Pt2Line1d_NameofFirmOrOrganization[0]"
I129_US_STREET = "form1[0].#subform[2].Line8a_StreetNumberName[0]"


def _read_fields(path):
    from pypdf import PdfReader
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return PdfReader(path).get_fields() or {}


def _g28_sff(conn, sfid):
    return next(r for r in forms.forms_of(conn, sfid)
                if r["form_code"] == "g-28")


def test_smart_forms_pdf_values_view(conn):
    """pdf-values-view: PDF-view edits appear on the form but not in
    the database values, until a database sync overwrites them."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Dana G-28", NOW, ADA,
                                   contact_id=1, form_codes=["g-28"])
    sff = _g28_sff(conn, sfid)
    db = render.db_values(conn, sff["id"])
    assert db[G28_CLIENT_FAMILY] == "Synthetic"  # from the fact store
    render.set_pdf_override(conn, sff["id"], G28_CLIENT_FAMILY, "Edited-By-Hand")
    assert render.pdf_values(conn, sff["id"])[G28_CLIENT_FAMILY] == "Edited-By-Hand"
    assert render.db_values(conn, sff["id"])[G28_CLIENT_FAMILY] == "Synthetic"
    # sync database values overwrites the manual edit
    render.sync_database_values(conn, sff["id"])
    assert render.pdf_values(conn, sff["id"])[G28_CLIENT_FAMILY] == "Synthetic"


def test_smart_forms_form_download_print(conn):
    """form-download-print: Print All produces a single PDF holding
    every form in the packet."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Emil N-400", NOW, ADA,
                                   contact_id=2, form_codes=["n-400", "g-28"])
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        total, per_form = render.print_all(conn, sfid, td / "all.pdf", td)
        from pypdf import PdfReader
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            combined = len(PdfReader(td / "all.pdf").pages)
    assert [c for c, _ in per_form] == ["n-400", "g-28"]
    assert combined == total == sum(n for _, n in per_form)
    assert total > 4  # more than either form alone: both are in there


def test_smart_forms_editable_pdf_toggle(conn):
    """editable-pdf-toggle: unchecking Print Editable PDF flattens
    the download; the default stays editable."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Dana G-28", NOW, ADA,
                                   contact_id=1, form_codes=["g-28"])
    sff = _g28_sff(conn, sfid)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        render.render_form(conn, sff["id"], td / "editable.pdf")
        f = _read_fields(td / "editable.pdf")
        assert int(f[G28_CLIENT_FAMILY].get("/Ff") or 0) & 1 == 0
        conn.execute("INSERT INTO firm_settings (key, value)"
                     " VALUES ('print.editable_pdf','0')")
        render.render_form(conn, sff["id"], td / "flat.pdf")
        f = _read_fields(td / "flat.pdf")
        assert int(f[G28_CLIENT_FAMILY].get("/Ff") or 0) & 1 == 1
        assert f[G28_CLIENT_FAMILY].get("/V") == "Synthetic"  # still filled


def test_smart_forms_na_autofill(conn):
    """na-autofill: the print setting fills every empty text field
    with N/A; filled fields keep their values."""
    conn.actor.set("user", ADA)
    conn.execute("INSERT INTO firm_settings (key, value)"
                 " VALUES ('print.na_autofill','1')")
    sfid = forms.create_smart_form(conn, "Dana G-28", NOW, ADA,
                                   contact_id=1, form_codes=["g-28"])
    sff = _g28_sff(conn, sfid)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "na.pdf"
        render.render_form(conn, sff["id"], out)
        f = _read_fields(out)
    assert f[G28_CLIENT_FAMILY].get("/V") == "Synthetic"
    # an unmapped text field reads N/A (receipt number never set)
    assert f["form1[0].#subform[1].Pt3Line4_ReceiptNumber[0]"].get("/V") == "N/A"
    empties = [k for k, v in f.items()
               if v.get("/FT") == "/Tx" and not v.get("/V")]
    assert not empties, f"empty text fields left: {empties[:3]}"


def test_smart_forms_preparer_population(conn):
    """preparer-population: the account-level preparer fills preparer
    fields on all forms; a form-specific preparer overrides it."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Dana G-28", NOW, ADA,
                                   contact_id=1, form_codes=["g-28"])
    sff = _g28_sff(conn, sfid)
    db = render.db_values(conn, sff["id"])
    # account default is Bram (seeded preparer.default_user_id=2)
    assert db[G28_BAR_NUMBER] == "VA-SYNTH-123"
    assert db[G28_ATTY_EMAIL] == "bram.attorney@example.test"
    assert db[G28_ATTY_FAMILY] == "Synthetic"
    assert db[G28_FIRM_NAME] == "Synthetic Law LLP"  # firm settings ride along
    # form-specific preparer overrides the default (fx-0038)
    sfid2 = forms.create_smart_form(conn, "Dana G-28 (Cleo)", NOW, ADA,
                                    contact_id=1, form_codes=["g-28"],
                                    preparer_id=3)
    sff2 = _g28_sff(conn, sfid2)
    assert render.db_values(conn, sff2["id"])[G28_ATTY_EMAIL] == \
        "cleo.paralegal@example.test"


def test_smart_forms_data_import_into_forms(conn):
    """data-import-into-forms: a stored value populates a form field
    without retyping (petitioner's address as beneficiary's intended
    U.S. address, fx-0036)."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "H-1B for Emil", NOW, ADA,
                                   contact_id=2, form_codes=["i-129", "g-28"])
    forms.assign_role(conn, sfid, "petitioner", 1)
    forms.assign_role(conn, sfid, "beneficiary", 2)
    got = render.import_stored_value(conn, sfid, "q.i129.beneficiary_us_street",
                                     1, "addr.street", NOW)
    assert got == "100 Synthetic Way"  # Dana's stored address, not retyped
    sff = next(r for r in forms.forms_of(conn, sfid)
               if r["form_code"] == "i-129")
    assert render.db_values(conn, sff["id"])[I129_US_STREET] == \
        "100 Synthetic Way"


def test_smart_forms_interpreter_import(conn):
    """interpreter-import: stored interpreter fields populate; the
    organization is remembered and auto-populates next import."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Dana intake", NOW, ADA,
                                   contact_id=1, form_codes=["g-28"])
    filled = render.import_interpreter(conn, sfid, 6, NOW)  # Ivo interprets
    assert filled["q.interpreter.family_name"] == "Synthetic"
    assert filled["q.interpreter.email"] == "ivo@example.test"
    assert "q.interpreter.organization" not in filled  # entered manually once
    render.set_interpreter_org(conn, sfid, 6, "Synthetic Language Services", NOW)
    # subsequent import of the same interpreter auto-populates the org
    sfid2 = forms.create_smart_form(conn, "Emil intake", NOW, ADA,
                                    contact_id=2, form_codes=["g-28"])
    filled2 = render.import_interpreter(conn, sfid2, 6, NOW)
    assert filled2["q.interpreter.organization"] == "Synthetic Language Services"


def test_smart_forms_i129_answer_import(conn):
    """i129-answer-import: Application-tab answers copy from an
    existing I-129 and overwrite the target tab; contact-specific
    information does not travel."""
    conn.actor.set("user", ADA)
    src = forms.create_smart_form(conn, "H-1B 2025", NOW, ADA,
                                  contact_id=2, form_codes=["i-129"])
    forms.assign_role(conn, src, "beneficiary", 2)
    render.set_answer(conn, src, "q.i129.classification_symbol", "H-1B", NOW)
    render.set_answer(conn, src, "q.i129.wages", "100000", NOW)
    dst = forms.create_smart_form(conn, "H-1B 2026", NOW, ADA,
                                  contact_id=4, form_codes=["i-129"])
    forms.assign_role(conn, dst, "beneficiary", 4)
    render.set_answer(conn, dst, "q.i129.classification_symbol", "L-1", NOW)
    copied = render.import_i129_answers(conn, dst, src, NOW)
    assert "q.i129.classification_symbol" in copied
    assert render.get_answer(conn, dst, "q.i129.classification_symbol") == "H-1B"
    assert render.get_answer(conn, dst, "q.i129.wages") == "100000"
    # contact-specific info did not travel: beneficiary is still Gil
    assert forms.role_contact(conn, dst, "beneficiary") == 4