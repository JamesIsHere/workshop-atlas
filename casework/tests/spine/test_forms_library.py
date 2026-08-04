"""Spine tests: smart-forms library/editions/collections (U2.1)."""

import json
import logging
import sys
import warnings
from pathlib import Path

logging.getLogger("pypdf").setLevel(logging.ERROR)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import forms  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA = 1
STARTER = {"eta-9089", "g-28", "i-129", "i-130", "n-400"}


def test_smart_forms_forms_library(conn):
    """forms-library (content): user selects a case type -> system
    offers the required forms from the maintained library. Tested
    against the 5-form starter set (content ruling); every schema
    pdf_field must exist in its real PDF's AcroForm."""
    conn.actor.set("user", ADA)
    lib = {r["code"]: r for r in forms.library(conn)}
    assert set(lib) == STARTER
    # case type -> required forms (seeded matter types)
    req = {mt: [r["form_code"] for r in forms.required_forms(conn, mt)]
           for mt in (1, 2, 3, 4)}
    assert req[1] == ["i-130", "g-28"]
    assert req[2] == ["n-400", "g-28"]
    assert req[3] == ["i-129", "g-28"]
    assert req[4] == ["eta-9089", "g-28"]
    # every G-28 attaches: G-28 required for every seeded case type
    assert all("g-28" in codes for codes in req.values())
    # schemas ground out in the real PDFs on disk
    from pypdf import PdfReader
    for code, row in lib.items():
        schema = forms.schema_of(conn, row["edition_id"])
        pdf_path = forms.PDFS_DIR / schema["pdf"]
        assert pdf_path.exists(), f"{code}: missing {schema['pdf']}"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fields = set((PdfReader(pdf_path).get_fields() or {}).keys())
        for q in schema["questions"]:
            for f in q["pdf_fields"]:
                assert f in fields, f"{code}: {q['key']} maps missing field {f}"
        for att in schema.get("attachments", []):
            assert (forms.PDFS_DIR / att["pdf"]).exists()


def test_smart_forms_form_updates_versioning(conn):
    """form-updates-versioning (adapted): new edition loaded into the
    library -> previously prepared forms migrate automatically."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Emil N-400", NOW, ADA,
                                   contact_id=2, form_codes=["n-400", "g-28"])
    before = {r["form_code"]: r["edition"] for r in forms.forms_of(conn, sfid)}
    assert before["n-400"] == "01/20/25"
    schema = forms.schema_of(conn, forms.current_edition(conn, "n-400")["id"])
    schema["edition"] = "09/09/26"
    new_eid = forms.register_edition(conn, schema, NOW)
    after = {r["form_code"]: r["edition"] for r in forms.forms_of(conn, sfid)}
    assert after["n-400"] == "09/09/26"  # migrated, no user action
    assert after["g-28"] == before["g-28"]  # other forms untouched
    assert forms.current_edition(conn, "n-400")["id"] == new_eid


def test_smart_forms_form_version_toggle(conn):
    """form-version-toggle (adapted): revert to the previous edition
    and back when one exists in the library; USCIS forms with
    previous versions revert together (fx-0027)."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Emil N-400", NOW, ADA,
                                   contact_id=2, form_codes=["n-400", "g-28"])
    schema = forms.schema_of(conn, forms.current_edition(conn, "n-400")["id"])
    schema["edition"] = "09/09/26"
    forms.register_edition(conn, schema, NOW)
    now = {r["form_code"]: r["edition"] for r in forms.forms_of(conn, sfid)}
    assert now["n-400"] == "09/09/26"
    forms.switch_version(conn, sfid, "previous")
    prev = {r["form_code"]: r["edition"] for r in forms.forms_of(conn, sfid)}
    assert prev["n-400"] == "01/20/25"  # reverted
    assert prev["g-28"] == "09/17/18"   # single-edition form untouched
    forms.switch_version(conn, sfid, "latest")
    back = {r["form_code"]: r["edition"] for r in forms.forms_of(conn, sfid)}
    assert back["n-400"] == "09/09/26"  # re-advanced


def test_smart_forms_smart_form_collections(conn):
    """smart-form-collections: a named collection of forms appears in
    the creation list and adds all its forms at once."""
    conn.actor.set("user", ADA)
    cid = forms.create_collection(conn, "Family Package", ["i-130", "g-28"])
    listed = {c["name"]: c for c in forms.list_collections(conn)}
    assert "Family Package" in listed
    assert listed["Family Package"]["forms"] == ["i-130", "g-28"]
    sfid = forms.create_smart_form(conn, "Dana Family Package", NOW, ADA,
                                   contact_id=1, collection_id=cid)
    got = [(r["form_code"], r["position"]) for r in forms.forms_of(conn, sfid)]
    assert got == [("i-130", 1), ("g-28", 2)]
