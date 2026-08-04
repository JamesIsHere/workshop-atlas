"""Spine tests: client surface + invitations over real HTTP (U2.5,
P2 gate ruling 2)."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import custom, facts, forms, invitations, sharing  # noqa: E402
import _http  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA = 1


def _package(conn, contact_id=2):
    return forms.create_smart_form(conn, "Client package", NOW, ADA,
                                   contact_id=contact_id,
                                   form_codes=["n-400", "g-28"])


def test_smart_forms_intake_invitations(conn):
    """intake-invitations (adapted): email and shareable link both
    grant the contact secure access to complete the questionnaire;
    SMS and portal are deferred."""
    conn.actor.set("user", ADA)
    sfid = _package(conn)
    invitations.invite(conn, sfid, 2, "email", NOW)
    mail = conn.execute("SELECT * FROM email_outbox WHERE"
                        " template='intake_invitation'").fetchall()
    assert len(mail) == 1 and mail[0]["recipient"] == "emil@example.test"
    assert "/intake/" in mail[0]["body"]  # the secure link travels by email
    link_inv = invitations.invite(conn, sfid, 2, "link", NOW)
    token = conn.execute("SELECT token FROM intake_invitations WHERE id=?",
                         (link_inv,)).fetchone()["token"]
    with tempfile.TemporaryDirectory() as td:
        with _http.client_surface(conn, td) as base:
            status, page = _http.get(f"{base}/intake/{token}")
    assert status == 200 and "questionnaire" in page.lower()
    # SMS stays deferred with prejudice
    try:
        invitations.invite(conn, sfid, 2, "sms", NOW)
        raise AssertionError("sms channel accepted")
    except ValueError:
        pass


def test_smart_forms_invitation_permissions(conn):
    """invitation-permissions: an unchecked tab is invisible to the
    invitee and not writable through their link."""
    conn.actor.set("user", ADA)
    sfid = _package(conn)
    inv_id = invitations.invite(conn, sfid, 2, "link", NOW,
                                restricted_tabs=["Eligibility"])
    token = conn.execute("SELECT token FROM intake_invitations WHERE id=?",
                         (inv_id,)).fetchone()["token"]
    with tempfile.TemporaryDirectory() as td:
        with _http.client_surface(conn, td) as base:
            _status, page = _http.get(f"{base}/intake/{token}")
            assert "lawful permanent resident" not in page  # tab dropped
            assert "Current legal family name" in page      # others remain
            code = _http.expect_error(
                _http.post_form, f"{base}/intake/{token}/answer",
                {"question": "q.n400.date_became_lpr", "value": "2019-01-15"})
    assert code == 403  # restricted questions are not writable either


def test_smart_forms_invitation_tracking(conn):
    """invitation-tracking: Sent -> Accepted (opened) -> Returned for
    Review (submitted), each with a date; resend and revoke work;
    revoked links go dead."""
    conn.actor.set("user", ADA)
    sfid = _package(conn)
    inv_id = invitations.invite(conn, sfid, 2, "email", NOW)
    row = invitations.track(conn, sfid)[0]
    assert (row["status"], row["address"]) == ("sent", "emil@example.test")
    token = conn.execute("SELECT token FROM intake_invitations WHERE id=?",
                         (inv_id,)).fetchone()["token"]
    with tempfile.TemporaryDirectory() as td:
        with _http.client_surface(conn, td) as base:
            _http.get(f"{base}/intake/{token}")  # client opens the intake
            assert invitations.track(conn, sfid)[0]["status"] == "accepted"
            _http.post_form(f"{base}/intake/{token}/submit", {})
            row = invitations.track(conn, sfid)[0]
            assert row["status"] == "returned"     # Returned for Review
            assert row["status_at"] != NOW         # with its own date
            # resend re-issues the email and re-marks Sent
            invitations.resend(conn, inv_id, NOW)
            assert invitations.track(conn, sfid)[0]["status"] == "sent"
            assert conn.execute(
                "SELECT count(*) FROM email_outbox WHERE template LIKE"
                " 'intake_invitation%'").fetchone()[0] == 2
            # revoke kills the link
            invitations.revoke(conn, inv_id, NOW)
            code = _http.expect_error(_http.get, f"{base}/intake/{token}")
    assert code == 404


def test_smart_forms_invitation_settings(conn):
    """invitation-settings (adapted): the firm's default email
    invitation message rides every invitation without retyping."""
    conn.actor.set("user", ADA)
    conn.execute("INSERT INTO firm_settings (key, value) VALUES"
                 " ('invitation.default_email_message',"
                 "  'Welcome to Synthetic Law LLP -- please complete this.')")
    sfid = _package(conn)
    invitations.invite(conn, sfid, 2, "email", NOW)  # no message given
    mail = conn.execute("SELECT body FROM email_outbox WHERE"
                        " template='intake_invitation'").fetchone()
    assert "Welcome to Synthetic Law LLP" in mail["body"]
    # an explicit message still wins
    invitations.invite(conn, sfid, 2, "email", NOW,
                       message="Custom note for Emil.")
    bodies = [r["body"] for r in conn.execute(
        "SELECT body FROM email_outbox WHERE template='intake_invitation'"
        " ORDER BY id")]
    assert "Custom note for Emil." in bodies[1]


def test_smart_forms_multilingual_intake(conn):
    """multilingual-intake (adapted): language chosen at invitation
    renders the questionnaire in that language; the client can
    re-translate; custom questions are not translated (fx-0029)."""
    conn.actor.set("user", ADA)
    sfid = _package(conn)
    ci = custom.create_custom_intake(conn, "Extras", NOW)
    tab = custom.add_tab(conn, ci, "Extras", 1)
    custom.add_question(conn, ci, tab, "How did you hear about us?",
                        "text", 1)
    custom.attach_container(conn, sfid, ci)
    inv_id = invitations.invite(conn, sfid, 2, "link", NOW, language="es")
    token = conn.execute("SELECT token FROM intake_invitations WHERE id=?",
                         (inv_id,)).fetchone()["token"]
    with tempfile.TemporaryDirectory() as td:
        with _http.client_surface(conn, td) as base:
            _status, page = _http.get(f"{base}/intake/{token}")
            assert "Apellido legal actual" in page   # invitation language
            assert "How did you hear about us?" in page  # custom untouched
            # client re-translates back to English
            _status, page_en = _http.get(f"{base}/intake/{token}?lang=en")
    assert "Current legal family name" in page_en


def test_smart_forms_mobile_intake(conn):
    """mobile-intake: the questionnaire completes on any browser --
    plain HTML forms, no JavaScript required (ruling 2 proxy)."""
    conn.actor.set("user", ADA)
    sfid = _package(conn)
    inv_id = invitations.invite(conn, sfid, 2, "link", NOW)
    token = conn.execute("SELECT token FROM intake_invitations WHERE id=?",
                         (inv_id,)).fetchone()["token"]
    with tempfile.TemporaryDirectory() as td:
        with _http.client_surface(conn, td) as base:
            _status, page = _http.get(f"{base}/intake/{token}")
            assert "<script" not in page          # nothing needs JS
            assert "viewport" in page             # small screens welcome
            status, _body = _http.post_form(
                f"{base}/intake/{token}/answer",
                {"question": "q.n400.family_name",
                 "value": "Synthetic-Movil"})
    assert status == 200
    # the plain form POST landed in the fact store
    assert facts.get_fact(conn, "contact", 2, "bio.family_name") == \
        "Synthetic-Movil"


def test_smart_forms_document_sharing(conn):
    """document-sharing: selected completed documents go to the
    contact; unchecked parts are excluded."""
    conn.actor.set("user", ADA)
    sfid = _package(conn)
    with tempfile.TemporaryDirectory() as td:
        produced = sharing.share_documents(conn, sfid, 2, NOW, Path(td),
                                           exclude=("g-28",))
        rows = conn.execute(
            "SELECT * FROM files WHERE produced_from_smart_form_id=?",
            (sfid,)).fetchall()
        assert len(rows) == len(produced) == 1
        assert rows[0]["name"] == "n-400-completed.pdf"  # g-28 excluded
        assert rows[0]["source"] == "produced"
        assert Path(rows[0]["stored_path"]).exists()
    mail = conn.execute("SELECT * FROM email_outbox WHERE"
                        " template='document_share'").fetchone()
    assert mail["recipient"] == "emil@example.test"
    assert "n-400-completed.pdf" in mail["body"]
    assert "g-28" not in mail["body"]