"""Packet assembly (U2.6): forms + evidentiary files + addenda in a
chosen order, with an optional generated table of contents
(fx-0020/0045). Addenda are a distinct, navigable packet part; the
attested generator is the ETA-9089 additional-information answer in
place of Appendix C (fx-0042)."""

import io
import logging

from fpdf import FPDF
from pypdf import PdfReader, PdfWriter

from app import forms, render

logging.getLogger("pypdf").setLevel(logging.ERROR)
logging.getLogger("fpdf").setLevel(logging.ERROR)


# --- parts ---

def sync_form_parts(conn, smart_form_id):
    """Every included form appears on the Assemble tab as a part."""
    for sff in forms.forms_of(conn, smart_form_id):
        row = conn.execute(
            "SELECT id FROM packet_parts WHERE smart_form_id=? AND"
            " smart_form_form_id=?", (smart_form_id, sff["id"])).fetchone()
        if row is None:
            pos = conn.execute(
                "SELECT coalesce(max(position)+1, 1) FROM packet_parts"
                " WHERE smart_form_id=?", (smart_form_id,)).fetchone()[0]
            conn.execute(
                "INSERT INTO packet_parts (smart_form_id, part_type,"
                " smart_form_form_id, position, display_name)"
                " VALUES (?,'form',?,?,?)",
                (smart_form_id, sff["id"], pos,
                 sff["display_name"] or sff["form_code"].upper()))


def add_file_part(conn, smart_form_id, file_id, display_name=None):
    """Attach an evidentiary file to the packet (searched by contact
    or file name on the real Assemble tab; custody came in U2.4)."""
    f = conn.execute("SELECT * FROM files WHERE id=?", (file_id,)).fetchone()
    if f is None:
        raise ValueError(f"unknown file {file_id}")
    pos = conn.execute(
        "SELECT coalesce(max(position)+1, 1) FROM packet_parts"
        " WHERE smart_form_id=?", (smart_form_id,)).fetchone()[0]
    return conn.execute(
        "INSERT INTO packet_parts (smart_form_id, part_type, file_id,"
        " position, display_name) VALUES (?,'file',?,?,?)",
        (smart_form_id, file_id, pos, display_name or f["name"])).lastrowid


def ensure_addendum_parts(conn, smart_form_id):
    """A form whose schema declares an addendum_question with a
    non-empty answer contributes a distinct addendum part."""
    for sff in forms.forms_of(conn, smart_form_id):
        schema = forms.schema_of(conn, sff["form_edition_id"])
        qkey = schema.get("addendum_question")
        if not qkey:
            continue
        text = render.get_answer(conn, smart_form_id, qkey)
        exists = conn.execute(
            "SELECT id FROM packet_parts WHERE smart_form_id=? AND"
            " part_type='addendum' AND smart_form_form_id=?",
            (smart_form_id, sff["id"])).fetchone()
        if text and not exists:
            pos = conn.execute(
                "SELECT coalesce(max(position)+1, 1) FROM packet_parts"
                " WHERE smart_form_id=?", (smart_form_id,)).fetchone()[0]
            conn.execute(
                "INSERT INTO packet_parts (smart_form_id, part_type,"
                " smart_form_form_id, position, display_name)"
                " VALUES (?,'addendum',?,?,?)",
                (smart_form_id, sff["id"], pos,
                 f"Addendum ({sff['form_code'].upper()})"))


def parts_of(conn, smart_form_id):
    return conn.execute(
        "SELECT * FROM packet_parts WHERE smart_form_id=?"
        " ORDER BY position", (smart_form_id,)).fetchall()


def set_order(conn, smart_form_id, part_ids):
    """Persist the drag-and-drop order."""
    known = {r["id"] for r in parts_of(conn, smart_form_id)}
    if set(part_ids) != known:
        raise ValueError("order must include every part exactly once")
    for pos, pid in enumerate(part_ids, 1):
        conn.execute("UPDATE packet_parts SET position=? WHERE id=?",
                     (pos, pid))


def rename_part(conn, part_id, display_name):
    """Inline rename; the name shows in the table of contents."""
    conn.execute("UPDATE packet_parts SET display_name=? WHERE id=?",
                 (display_name, part_id))


# --- assembly ---

def _text_pdf(title, body_text):
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)
    for line in body_text.splitlines() or [""]:
        pdf.multi_cell(0, 8, line, new_x="LMARGIN", new_y="NEXT")
    return PdfReader(io.BytesIO(bytes(pdf.output())))


def _render_form_part(conn, smart_form_id, sff_id, workdir):
    """Filled form plus its triggered conditional attachments
    (eta9089-conditional-assembly, fx-0042)."""
    sff = conn.execute("SELECT * FROM smart_form_forms WHERE id=?",
                       (sff_id,)).fetchone()
    schema = forms.schema_of(conn, sff["form_edition_id"])
    out = workdir / f"packet-form-{sff_id}.pdf"
    render.render_form(conn, sff_id, out)
    readers = [PdfReader(out)]
    for att in schema.get("attachments", []):
        answer = render.get_answer(conn, smart_form_id,
                                   att["when"]["question"])
        if answer == att["when"]["equals"]:
            readers.append(PdfReader(forms.PDFS_DIR / att["pdf"]))
    return readers


def assemble_packet(conn, smart_form_id, out_path, workdir):
    """Build the packet: parts in their chosen order, optional TOC
    first page listing every part with its page number. Returns
    {'pages', 'toc', 'parts'}."""
    sync_form_parts(conn, smart_form_id)
    ensure_addendum_parts(conn, smart_form_id)
    include_toc = conn.execute(
        "SELECT include_toc FROM smart_forms WHERE id=?",
        (smart_form_id,)).fetchone()["include_toc"]

    rendered = []  # (display_name, [readers])
    for part in parts_of(conn, smart_form_id):
        if part["part_type"] == "form":
            readers = _render_form_part(conn, smart_form_id,
                                        part["smart_form_form_id"], workdir)
        elif part["part_type"] == "file":
            f = conn.execute("SELECT * FROM files WHERE id=?",
                             (part["file_id"],)).fetchone()
            content = open(f["stored_path"], "rb").read()
            if not content.startswith(b"%PDF"):
                raise ValueError(f"file part {f['name']} is not a PDF")
            readers = [PdfReader(io.BytesIO(content))]
        else:  # addendum
            sff = conn.execute(
                "SELECT * FROM smart_form_forms WHERE id=?",
                (part["smart_form_form_id"],)).fetchone()
            schema = forms.schema_of(conn, sff["form_edition_id"])
            text = render.get_answer(conn, smart_form_id,
                                     schema["addendum_question"]) or ""
            readers = [_text_pdf(part["display_name"] or "Addendum",
                                 text)]
        rendered.append((part["display_name"], readers))

    toc = []
    toc_pages = 1 if include_toc else 0
    page = toc_pages + 1
    for name, readers in rendered:
        toc.append((name, page))
        page += sum(len(r.pages) for r in readers)

    writer = PdfWriter()
    if include_toc:
        toc_text = "\n".join(f"{name} .......... page {p}"
                             for name, p in toc)
        toc_reader = _text_pdf("Table of Contents", toc_text)
        for pg in toc_reader.pages:
            writer.add_page(pg)
    for _name, readers in rendered:
        for r in readers:
            for pg in r.pages:
                writer.add_page(pg)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return {"pages": len(writer.pages), "toc": toc,
            "parts": [name for name, _ in rendered]}
