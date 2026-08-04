"""Spine tests: packet assembly (U2.6)."""

import sys
import tempfile
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import custom, forms, intake, packets, render  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA = 1


def _page_count(path):
    from pypdf import PdfReader
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return len(PdfReader(path).pages)


def _page_text(path, page=0):
    from pypdf import PdfReader
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return PdfReader(path).pages[page].extract_text() or ""


def test_smart_forms_packet_assembly(conn):
    """packet-assembly: forms and files combine into one packet in
    the chosen (reordered) order."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Dana package", NOW, ADA,
                                   contact_id=1, matter_id=1,
                                   form_codes=["g-28"])
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # an evidentiary file joins the packet (1-page synthetic PDF)
        fid = custom.save_client_upload(
            conn, sfid, "evidence.pdf",
            _one_page_pdf("SYNTHETIC EVIDENCE"), NOW, td)
        packets.sync_form_parts(conn, sfid)
        packets.add_file_part(conn, sfid, fid)
        parts = packets.parts_of(conn, sfid)
        assert [p["part_type"] for p in parts] == ["form", "file"]
        # drag the file above the form and assemble
        packets.set_order(conn, sfid, [parts[1]["id"], parts[0]["id"]])
        result = packets.assemble_packet(conn, sfid, td / "packet.pdf", td)
        assert result["parts"] == ["evidence.pdf", "G-28"]  # chosen order
        assert result["pages"] == 1 + 4  # file page then the G-28
        assert _page_text(td / "packet.pdf", 0).find("SYNTHETIC EVIDENCE") >= 0


def test_smart_forms_packet_toc(conn):
    """packet-toc: Include Table of Contents adds a first page
    listing every form and document with its page number; inline
    renames show in the TOC."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "Dana package", NOW, ADA,
                                   contact_id=1, matter_id=1,
                                   form_codes=["g-28", "n-400"])
    conn.execute("UPDATE smart_forms SET include_toc=1 WHERE id=?", (sfid,))
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        packets.sync_form_parts(conn, sfid)
        parts = packets.parts_of(conn, sfid)
        packets.rename_part(conn, parts[0]["id"], "Notice of Appearance")
        result = packets.assemble_packet(conn, sfid, td / "packet.pdf", td)
        # TOC page numbers: TOC is page 1, G-28 starts at 2, N-400 at 6
        assert result["toc"] == [("Notice of Appearance", 2), ("N-400", 6)]
        assert result["pages"] == 1 + 4 + 14
        toc_text = _page_text(td / "packet.pdf", 0)
    assert "Table of Contents" in toc_text
    assert "Notice of Appearance" in toc_text and "page 2" in toc_text
    assert "N-400" in toc_text and "page 6" in toc_text


def test_smart_forms_eta9089_conditional_assembly(conn):
    """eta9089-conditional-assembly: trigger answers add the
    corresponding appendices and final determination to the
    prepared form."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "PERM for Emil", NOW, ADA,
                                   contact_id=2, form_codes=["eta-9089"])
    intake.answer_intake(conn, sfid,
                         "q.eta9089.worker_has_additional_experience",
                         "true", NOW)
    intake.answer_intake(conn, sfid, "q.eta9089.college_teacher",
                         "true", NOW)
    # multiple_worksites and final determination NOT triggered
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        result = packets.assemble_packet(conn, sfid, td / "eta.pdf", td)
        # main 7 + Appendix A 5 + Appendix D 1; no AppB (1), no FD (2)
        assert result["pages"] == 7 + 5 + 1
        # now trigger the final determination too and reassemble
        intake.answer_intake(conn, sfid,
                             "q.eta9089.request_final_determination",
                             "true", NOW)
        result2 = packets.assemble_packet(conn, sfid, td / "eta2.pdf", td)
        assert result2["pages"] == 7 + 5 + 1 + 2


def test_smart_forms_packet_addenda(conn):
    """packet-addenda: additional information in place of Appendix C
    lands on generated addendum pages, navigable as a distinct
    packet part."""
    conn.actor.set("user", ADA)
    sfid = forms.create_smart_form(conn, "PERM for Emil", NOW, ADA,
                                   contact_id=2, form_codes=["eta-9089"])
    intake.answer_intake(conn, sfid, "q.eta9089.additional_info",
                         "Extra recruitment details in place of"
                         " Appendix C.", NOW)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        result = packets.assemble_packet(conn, sfid, td / "eta.pdf", td)
        parts = packets.parts_of(conn, sfid)
        assert [p["part_type"] for p in parts] == ["form", "addendum"]
        assert result["parts"][-1] == "Addendum (ETA-9089)"
        assert result["pages"] == 7 + 1  # main form + addendum page
        addendum_text = _page_text(td / "eta.pdf", 7)
    assert "Extra recruitment details" in addendum_text


def _one_page_pdf(text):
    import io
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, text)
    return bytes(pdf.output())