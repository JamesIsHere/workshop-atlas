"""Spine tests: files-and-documents storage core (U4.1).

Owed custody extensions land here (state.md): client uploads and
produced artifacts (shared docs, notes exports) surface on the same
Files index as firm uploads.
"""

import sys
import tempfile
import zipfile
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import custom, files, forms, notes  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM, CLEO = 1, 2, 3
DANA, EMIL, FARA = 1, 2, 3


def test_files_and_documents_module_exists(conn):
    """module-exists: the Files Dashboard lists the firm's files and
    folders for viewing and management -- firm uploads, client
    uploads, and produced artifacts together (owed custody legs)."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid = files.upload_file(conn, "evidence.pdf", b"%PDF-firm", NOW,
                                td, contact_id=DANA, user_id=ADA)
        folder = files.create_folder(conn, "Dana evidence", NOW,
                                     contact_id=DANA, user_id=ADA)
        # owed leg 1: a client upload (U2.4 path) shares the index
        sfid = forms.create_smart_form(conn, "Dana intake", NOW, ADA,
                                       contact_id=DANA)
        conn.actor.set("contact", DANA)
        cfid = custom.save_client_upload(conn, sfid, "passport.jpg",
                                         b"jpegbytes", NOW, Path(td))
        conn.actor.set("user", ADA)
        # owed leg 2: a produced artifact (notes export) takes custody
        notes.create_note(conn, "Filed I-130", NOW, ADA, contact_id=DANA)
        pdf = notes.export_notes_pdf(conn, contact_id=DANA)
        pfid = files.save_produced(conn, "dana-notes.pdf", pdf, NOW, td,
                                   contact_id=DANA)
        listed = files.list_files(conn)
        assert {fid, cfid, pfid} <= {r["id"] for r in listed}
        sources = {r["id"]: r["source"] for r in listed}
        assert sources[fid] == "firm"
        assert sources[cfid] == "client"
        assert sources[pfid] == "produced"
        assert folder in {r["id"] for r in
                          conn.execute("SELECT id FROM folders WHERE"
                                       " deleted_at IS NULL")}


def test_files_and_documents_file_upload(conn):
    """file-upload: pick a file, click Upload -> stored and listed
    under the chosen contact, matter, or folder; rename at upload;
    uploading from inside a folder files it there."""
    conn.actor.set("user", CLEO)
    with tempfile.TemporaryDirectory() as td:
        f1 = files.upload_file(conn, "renamed-brief.pdf", b"%PDF-brief",
                               NOW, td, matter_id=1, user_id=CLEO)
        row = files.get_file(conn, f1)
        assert row["matter_id"] == 1
        assert row["name"] == "renamed-brief.pdf"
        assert Path(row["stored_path"]).read_bytes() == b"%PDF-brief"
        folder = files.create_folder(conn, "Court filings", NOW,
                                     contact_id=EMIL, user_id=CLEO)
        f2 = files.upload_file(conn, "motion.pdf", b"%PDF-motion", NOW,
                               td, folder_id=folder, user_id=CLEO)
        row2 = files.get_file(conn, f2)
        assert row2["folder_id"] == folder
        assert row2["contact_id"] == EMIL  # inherited from the folder
        assert [r["id"] for r in files.list_files(conn, folder_id=folder)] \
            == [f2]


def test_files_and_documents_folders(conn):
    """folders: name + optional contact/matter at creation; matter
    assignment requires the matter's primary contact (fx-0195)."""
    conn.actor.set("user", ADA)
    fold = files.create_folder(conn, "Dana docs", NOW, contact_id=DANA,
                               user_id=ADA)
    row = conn.execute("SELECT * FROM folders WHERE id=?",
                       (fold,)).fetchone()
    assert (row["contact_id"], row["matter_id"]) == (DANA, None)
    # matter 1's primary contact is Dana: matter-only assignment
    # brings the primary contact; a mismatched contact is refused
    fold2 = files.create_folder(conn, "I-130 packet", NOW, matter_id=1,
                                user_id=ADA)
    row2 = conn.execute("SELECT * FROM folders WHERE id=?",
                        (fold2,)).fetchone()
    assert (row2["contact_id"], row2["matter_id"]) == (DANA, 1)
    try:
        files.create_folder(conn, "Bad", NOW, contact_id=EMIL,
                            matter_id=1, user_id=ADA)
        raise AssertionError("mismatched contact accepted")
    except ValueError:
        pass


def test_files_and_documents_subfolders(conn):
    """subfolders: any folder can hold subfolders."""
    conn.actor.set("user", ADA)
    parent = files.create_folder(conn, "Evidence", NOW, contact_id=DANA,
                                 user_id=ADA)
    child = files.create_folder(conn, "Photos", NOW, parent_id=parent,
                                user_id=ADA)
    subs = files.subfolders(conn, parent)
    assert [s["id"] for s in subs] == [child]
    assert subs[0]["name"] == "Photos"


def test_files_and_documents_file_assignment(conn):
    """file-assignment: More Actions > Update re-assigns an existing
    file or folder to a contact, matter, and/or folder."""
    conn.actor.set("user", BRAM)
    with tempfile.TemporaryDirectory() as td:
        fid = files.upload_file(conn, "loose.txt", b"unfiled", NOW, td,
                                user_id=BRAM)
        target = files.create_folder(conn, "Fara file room", NOW,
                                     contact_id=FARA, user_id=BRAM)
        files.assign(conn, "file", fid, contact_id=FARA, matter_id=3,
                     folder_id=target)
        row = files.get_file(conn, fid)
        assert (row["contact_id"], row["matter_id"], row["folder_id"]) \
            == (FARA, 3, target)
        # folders re-assign too
        files.assign(conn, "folder", target, contact_id=FARA, matter_id=3)
        frow = conn.execute("SELECT * FROM folders WHERE id=?",
                            (target,)).fetchone()
        assert (frow["contact_id"], frow["matter_id"]) == (FARA, 3)


def test_files_and_documents_file_renaming(conn):
    """file-renaming: the pencil icon renames files and folders in
    place."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid = files.upload_file(conn, "scan0001.pdf", b"%PDF-scan", NOW,
                                td, user_id=ADA)
        files.rename(conn, "file", fid, "birth-certificate.pdf")
        assert files.get_file(conn, fid)["name"] == "birth-certificate.pdf"
        fold = files.create_folder(conn, "New folder", NOW, user_id=ADA)
        files.rename(conn, "folder", fold, "Naturalization")
        assert conn.execute("SELECT name FROM folders WHERE id=?",
                            (fold,)).fetchone()["name"] == "Naturalization"


def test_files_and_documents_file_download(conn):
    """file-download: the download icon returns the file's bytes."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid = files.upload_file(conn, "notice.pdf", b"%PDF-notice", NOW,
                                td, contact_id=DANA, user_id=ADA)
        name, content = files.download(conn, fid)
        assert name == "notice.pdf"
        assert content == b"%PDF-notice"


def test_files_and_documents_bulk_file_download(conn):
    """bulk-file-download: checked files and folders leave together
    (one zip; folder contents ride under the folder name)."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        f1 = files.upload_file(conn, "a.txt", b"alpha", NOW, td,
                               user_id=ADA)
        f2 = files.upload_file(conn, "b.txt", b"bravo", NOW, td,
                               user_id=ADA)
        fold = files.create_folder(conn, "Bundle", NOW, user_id=ADA)
        files.upload_file(conn, "inside.txt", b"charlie", NOW, td,
                          folder_id=fold, user_id=ADA)
        blob = files.bulk_download(conn, file_ids=[f1, f2],
                                   folder_ids=[fold])
        z = zipfile.ZipFile(io.BytesIO(blob))
        assert sorted(z.namelist()) == ["Bundle/inside.txt", "a.txt",
                                        "b.txt"]
        assert z.read("Bundle/inside.txt") == b"charlie"


def test_files_and_documents_file_preview(conn):
    """file-preview (adapted): supported types display without a
    download -- pdf, png, jpeg/jpg, txt, csv in v1; Office formats
    refuse (post-v1 conversion dependency)."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        pdf = files.upload_file(conn, "form.pdf", b"%PDF-1.4 preview",
                                NOW, td, user_id=ADA)
        ctype, content = files.preview(conn, pdf)
        assert ctype == "application/pdf"
        assert content == b"%PDF-1.4 preview"
        csvf = files.upload_file(conn, "list.csv", b"a,b\n1,2", NOW, td,
                                 user_id=ADA)
        assert files.preview(conn, csvf)[0] == "text/csv"
        docx = files.upload_file(conn, "memo.docx", b"PKdocx", NOW, td,
                                 user_id=ADA)
        try:
            files.preview(conn, docx)
            raise AssertionError("docx preview should refuse in v1")
        except ValueError:
            pass


def test_files_and_documents_file_printing(conn):
    """file-printing: the printer icon serves the content for a new
    tab, no download step."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid = files.upload_file(conn, "cover-letter.pdf",
                                b"%PDF-cover", NOW, td, user_id=ADA)
        ctype, content = files.print_view(conn, fid)
        assert ctype == "application/pdf"
        assert content == b"%PDF-cover"
