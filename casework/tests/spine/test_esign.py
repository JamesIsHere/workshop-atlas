"""Spine tests: files-and-documents e-signature family (U4.2).

Capture model per P4 gate ruling 1: draw = stroke data (rendered as
vector strokes), type = name text; date fields auto-populate; the
completed artifact is stamped, hashed, and auto-filed.
"""

import io
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pypdf import PdfReader  # noqa: E402

from app import esign, files, forms  # noqa: E402
from tests.spine import _http  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM, CLEO = 1, 2, 3
DANA, EMIL = 1, 2

DRAW = json.dumps({"mode": "draw",
                   "strokes": [[[0, 0], [40, 12], [80, 0], [120, 8]]]})
TYPE_DANA = json.dumps({"mode": "type", "text": "Dana Synthetic"})


def _pdf_bytes():
    return (forms.PDFS_DIR / "g-28.pdf").read_bytes()


def _prepared(conn, td, contact_id=DANA, matter_id=None, user_id=ADA):
    """Upload a PDF and prepare it with one contact signer + fields."""
    fid = files.upload_file(conn, "retainer.pdf", _pdf_bytes(), NOW, td,
                            contact_id=contact_id, matter_id=matter_id,
                            user_id=user_id)
    esid = esign.prepare(conn, fid, NOW, user_id)
    signer = esign.add_signer(conn, esid, contact_id=contact_id)
    sig = esign.add_field(conn, esid, signer, "signature", 1, 100, 120)
    date = esign.add_field(conn, esid, signer, "date", 1, 300, 120)
    return fid, esid, signer, sig, date


def test_files_and_documents_esignature(conn):
    """esignature (anchor): prepare a stored PDF, request signatures,
    signers sign electronically, the completed file is collected
    inside the system -- no third-party tool."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid, esid, signer, sig, date = _prepared(conn, td)
        esign.request_signatures(conn, esid, NOW)
        esign.sign(conn, esid, signer,
                   {sig: TYPE_DANA}, NOW, td)
        es = conn.execute("SELECT * FROM esign_files WHERE id=?",
                          (esid,)).fetchone()
        assert es["status"] == "completed"
        signed = files.get_file(conn, es["signed_file_id"])
        assert signed["source"] == "produced"
        assert signed["name"] == "retainer-signed.pdf"
        content = Path(signed["stored_path"]).read_bytes()
        assert content.startswith(b"%PDF")
        assert len(PdfReader(io.BytesIO(content)).pages) \
            == len(PdfReader(io.BytesIO(_pdf_bytes())).pages)


def test_files_and_documents_esignature_preparation(conn):
    """esignature-preparation: signers added in setup, fields placed
    and assigned, draft saved; editable until requested; only PDFs
    can be prepared."""
    conn.actor.set("user", BRAM)
    with tempfile.TemporaryDirectory() as td:
        txt = files.upload_file(conn, "notes.txt", b"not a pdf", NOW, td,
                                user_id=BRAM)
        try:
            esign.prepare(conn, txt, NOW, BRAM)
            raise AssertionError("non-PDF prepared")
        except ValueError:
            pass
        fid = files.upload_file(conn, "agreement.pdf", _pdf_bytes(), NOW,
                                td, contact_id=DANA, user_id=BRAM)
        esid = esign.prepare(conn, fid, NOW, BRAM)
        s1 = esign.add_signer(conn, esid, contact_id=DANA)
        s2 = esign.add_signer(conn, esid, user_id=BRAM)
        f1 = esign.add_field(conn, esid, s1, "signature", 1, 90, 100)
        esign.add_field(conn, esid, s2, "initials", 1, 90, 60)
        placed = esign.fields_of(conn, esid)
        assert [(f["signer_id"], f["field_type"]) for f in placed] \
            == [(s1, "signature"), (s2, "initials")]
        # trashcan icon: a draft field is removable
        esign.remove_field(conn, f1)
        assert [f["field_type"] for f in esign.fields_of(conn, esid)] \
            == ["initials"]
        assert conn.execute("SELECT status FROM esign_files WHERE id=?",
                            (esid,)).fetchone()["status"] == "draft"


def test_files_and_documents_esignature_requests(conn):
    """esignature-requests (adapted): Send to Unsigned emails each
    unsigned signer; the file locks after the first send; re-sending
    reaches the still-unsigned only."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid, esid, signer, sig, date = _prepared(conn, td)
        s2 = esign.add_signer(conn, esid, user_id=BRAM)
        i2 = esign.add_field(conn, esid, s2, "initials", 1, 90, 60)
        sent = esign.request_signatures(conn, esid, NOW)
        assert sorted(sent) == [signer, s2]
        recipients = [r["recipient"] for r in conn.execute(
            "SELECT recipient FROM email_outbox WHERE"
            " template='esign_request' ORDER BY id")]
        assert recipients == ["dana@example.test",
                              "bram.attorney@example.test"]
        # locked after send
        try:
            esign.add_field(conn, esid, signer, "text", 1, 10, 10)
            raise AssertionError("field added after request")
        except ValueError:
            pass
        # Bram signs; re-send reaches Dana alone
        conn.actor.set("user", BRAM)
        esign.sign(conn, esid, s2, {i2: json.dumps(
            {"mode": "type", "text": "BS"})}, NOW, td)
        conn.actor.set("user", ADA)
        assert esign.request_signatures(conn, esid, NOW) == [signer]


def test_files_and_documents_esignature_signing(conn):
    """esignature-signing: a requested contact signer opens the
    secure link and completes fields (drawn signature, auto date)
    over plain HTTP; firm members sign in-app."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid, esid, signer, sig, date = _prepared(conn, td)
        s2 = esign.add_signer(conn, esid, user_id=CLEO)
        i2 = esign.add_field(conn, esid, s2, "initials", 1, 90, 60)
        esign.request_signatures(conn, esid, NOW)
        token = conn.execute(
            "SELECT access_token FROM esign_signers WHERE id=?",
            (signer,)).fetchone()["access_token"]
        with _http.client_surface(conn, td) as base:
            status, page = _http.get(f"{base}/esign/{token}")
            assert status == 200
            assert "signature (page 1)" in page
            status, _page = _http.post_form(
                f"{base}/esign/{token}/sign", {f"field_{sig}": DRAW})
            assert status == 200
        row = conn.execute("SELECT * FROM esign_fields WHERE id=?",
                           (sig,)).fetchone()
        assert json.loads(row["value"])["mode"] == "draw"
        # empty date auto-populated from the signing date: the same
        # clock stamps signed_at, so derive the expectation from it
        # (a literal here expires the day after it is written)
        signed_at = conn.execute(
            "SELECT signed_at FROM esign_signers WHERE id=?",
            (signer,)).fetchone()["signed_at"]
        assert conn.execute("SELECT value FROM esign_fields WHERE id=?",
                            (date,)).fetchone()["value"] == signed_at[:10]
        # firm member signs via the Sign button (in-app, no link)
        conn.actor.set("user", CLEO)
        esign.sign(conn, esid, s2, {i2: json.dumps(
            {"mode": "type", "text": "CP"})}, NOW, td)
        assert conn.execute(
            "SELECT signed_at FROM esign_signers WHERE id=?",
            (s2,)).fetchone()["signed_at"] is not None


def test_files_and_documents_esignature_completion(conn):
    """esignature-completion: each signer gets a copy of their
    portion; once all sign, every signer receives the completed
    file."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid, esid, signer, sig, date = _prepared(conn, td)
        s2 = esign.add_signer(conn, esid, user_id=BRAM)
        i2 = esign.add_field(conn, esid, s2, "initials", 1, 90, 60)
        esign.request_signatures(conn, esid, NOW)
        esign.sign(conn, esid, signer, {sig: TYPE_DANA}, NOW, td)
        partial = [r["recipient"] for r in conn.execute(
            "SELECT recipient FROM email_outbox WHERE template='esign_copy'"
            " ORDER BY id")]
        assert partial == ["dana@example.test"]  # own portion
        conn.actor.set("user", BRAM)
        esign.sign(conn, esid, s2, {i2: json.dumps(
            {"mode": "type", "text": "BS"})}, NOW, td)
        copies = [r["recipient"] for r in conn.execute(
            "SELECT recipient FROM email_outbox WHERE template='esign_copy'"
            " ORDER BY id")]
        # Dana's portion, Bram's portion, then completed copies to both
        assert copies == ["dana@example.test", "bram.attorney@example.test",
                          "dana@example.test", "bram.attorney@example.test"]


def test_files_and_documents_esignature_status(conn):
    """esignature-status: the Files index carries each file's
    e-Signature Status, pending signers surface on mouseover, and the
    index filters by status."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid, esid, signer, sig, date = _prepared(conn, td)
        plain = files.upload_file(conn, "plain.pdf", _pdf_bytes(), NOW,
                                  td, user_id=ADA)
        statuses = {r["id"]: r["esign_status"]
                    for r in files.list_files(conn)}
        assert statuses[fid] == "draft"
        assert statuses[plain] is None
        esign.request_signatures(conn, esid, NOW)
        assert esign.pending_signers(conn, esid) == ["Dana Synthetic"]
        requested = files.list_files(conn, esign_status="requested")
        assert [r["id"] for r in requested] == [fid]
        esign.sign(conn, esid, signer, {sig: TYPE_DANA}, NOW, td)
        assert esign.pending_signers(conn, esid) == []
        assert files.list_files(conn, esign_status="completed")[0]["id"] \
            == fid


def test_files_and_documents_esignature_signed_notifications(conn):
    """esignature-signed-notifications: when the document is signed
    the firm receives an email and an in-app notification."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid, esid, signer, sig, date = _prepared(conn, td)
        esign.request_signatures(conn, esid, NOW)
        esign.sign(conn, esid, signer, {sig: TYPE_DANA}, NOW, td)
        # no matter on the file -> preparer (Ada) is the firm target
        notif = conn.execute(
            "SELECT * FROM notifications WHERE kind='esign_signed'"
        ).fetchall()
        assert [n["user_id"] for n in notif] == [ADA]
        assert json.loads(notif[0]["payload"])["name"] == "retainer.pdf"
        mails = [r["recipient"] for r in conn.execute(
            "SELECT recipient FROM email_outbox WHERE"
            " template='esign_signed'")]
        assert mails == ["ada.admin@example.test"]


def test_files_and_documents_esignature_auto_filing(conn):
    """esignature-auto-filing: the signed document files itself under
    the associated contact/matter -- no manual upload."""
    conn.actor.set("user", ADA)
    with tempfile.TemporaryDirectory() as td:
        fid, esid, signer, sig, date = _prepared(conn, td, contact_id=DANA,
                                                 matter_id=1)
        esign.request_signatures(conn, esid, NOW)
        esign.sign(conn, esid, signer, {sig: TYPE_DANA}, NOW, td)
        es = conn.execute("SELECT * FROM esign_files WHERE id=?",
                          (esid,)).fetchone()
        signed = files.get_file(conn, es["signed_file_id"])
        assert (signed["contact_id"], signed["matter_id"]) == (DANA, 1)
        assert signed["sha256"]  # tamper-evidence anchor in custody
        listed = files.list_files(conn, matter_id=1)
        assert es["signed_file_id"] in {r["id"] for r in listed}
