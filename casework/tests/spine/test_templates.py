"""Spine tests: template-automation (U4.3)."""

import io
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import facts, templates  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA = 1
DANA = 1

CT_XML = ('<?xml version="1.0"?><Types xmlns="http://schemas.'
          'openxmlformats.org/package/2006/content-types"/>')


def _docx(body_text):
    """Minimal .docx container: content types + word/document.xml."""
    doc = (f'<?xml version="1.0"?><w:document><w:body><w:p><w:r>'
           f'<w:t>{body_text}</w:t></w:r></w:p></w:body></w:document>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", CT_XML)
        z.writestr("word/document.xml", doc)
    return buf.getvalue()


def _document_xml(docx_bytes):
    return zipfile.ZipFile(io.BytesIO(docx_bytes)).read(
        "word/document.xml").decode("utf-8")


def test_template_automation_module_exists(conn):
    """module-exists: a merge-tagged .docx uploads as an automated
    template; exporting against a client substitutes the client's
    information for the tags."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        tid = templates.upload_template(
            conn, "Welcome letter",
            _docx("Dear #full_name#, welcome to our firm."), NOW, td)
        out = templates.export_template(conn, tid, DANA, NOW)
        text = _document_xml(out)
        assert "Dear Dana Synthetic, welcome to our firm." in text
        assert "#full_name#" not in text


def test_template_automation_template_upload(conn):
    """template-upload: named and uploaded on the Automated Templates
    page -> stored and selectable for a new export; non-docx bytes
    refuse."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        tid = templates.upload_template(conn, "Engagement letter",
                                        _docx("#full_name#"), NOW, td)
        listed = templates.list_templates(conn)
        assert (tid, "Engagement letter") in [(t["id"], t["name"])
                                              for t in listed]
        try:
            templates.upload_template(conn, "Bad", b"plain text", NOW, td)
            raise AssertionError("non-zip accepted as a template")
        except ValueError:
            pass


def test_template_automation_template_export(conn):
    """template-export: Create New > Template with Client (required),
    Matter (optional), Template (required) -> a populated document."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        tid = templates.upload_template(
            conn, "Case cover",
            _docx("Re: #matter_title# for #matter_applicant#"), NOW, td)
        # matter 1 is Dana's I-130
        out = templates.export_template(conn, tid, DANA, NOW, matter_id=1)
        text = _document_xml(out)
        assert "#matter_title#" not in text
        m = conn.execute("SELECT name FROM matters WHERE id=1").fetchone()
        assert m["name"] in text
        assert "Dana Synthetic" in text
        # client is required
        try:
            templates.export_template(conn, tid, 9999, NOW)
            raise AssertionError("export without a real client")
        except ValueError:
            pass


def test_template_automation_merge_tags(conn):
    """merge-tags: documented tags (#full_name#, contact fields, date
    tags) are replaced by the client's field values; custom
    attributes extend the vocabulary (owed custom-attributes
    TEMPLATE leg rides the same mechanism)."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        key = facts.define_custom_attribute(
            conn, "passport-number", "contact", "text", "Passport Number")
        facts.set_fact(conn, "contact", DANA, key, "P-SYNTH-777", NOW)
        tid = templates.upload_template(
            conn, "Tag probe",
            _docx("#full_name# / #email# / #today# / #date_long# /"
                  " passport #passport_number#"), NOW, td)
        text = _document_xml(templates.export_template(conn, tid, DANA,
                                                       NOW))
        assert "Dana Synthetic" in text
        assert "dana@example.test" in text
        assert "2026-08-01" in text
        assert "August 1, 2026" in text
        assert "passport P-SYNTH-777" in text
        assert "#" not in text  # no raw tags survive an export
