"""Spine tests: login.* and firm-settings.two-factor-authentication.

Each test receives a fresh seeded connection (run_spine.py). Criteria
cited from ../docketwise-spec/corpus/ by entry id. Seeded staff all
use password 'synthetic-password' (seeds/gen_seed.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import auth  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
PW = "synthetic-password"
ADA = "ada.admin@example.test"


def _full_login_email_2fa(conn, email, password, now):
    """Password login -> (mandatory) email-2FA path -> authenticated."""
    status, token = auth.login(conn, email, password, now)
    if status == "enrollment_required":
        auth.enroll_twofa(conn, _uid(conn, email), "email", token, now)
    elif status != "twofa_required":
        return status, None
    code = conn.execute(
        "SELECT c.code FROM twofa_challenges c JOIN sessions s"
        " ON s.id = c.session_id WHERE s.token=? AND c.used_at IS NULL"
        " ORDER BY c.id DESC LIMIT 1", (token,)).fetchone()["code"]
    assert auth.verify_twofa(conn, token, code, now)
    return "ok", token


def _uid(conn, email):
    return conn.execute("SELECT id FROM users WHERE email=?",
                        (email,)).fetchone()["id"]


def test_login_email_password_login(conn):
    """login.email-password-login: email + password -> authenticated
    into the firm's account; logout clears the session."""
    conn.actor.set("system", None)
    # wrong password rejected, no session created
    status, token = auth.login(conn, ADA, "wrong-password", NOW)
    assert status == "bad_credentials" and token is None
    assert conn.execute("SELECT count(*) FROM sessions").fetchone()[0] == 0
    # right password authenticates (through mandatory 2FA)
    status, token = _full_login_email_2fa(conn, ADA, PW, NOW)
    assert status == "ok"
    assert auth.session_user(conn, token, NOW) == _uid(conn, ADA)
    # logout clears the session (corpus detail, fx-0229)
    auth.logout(conn, token)
    assert auth.session_user(conn, token, NOW) is None
    # deactivated users cannot log in
    conn.execute("UPDATE users SET deactivated_at=? WHERE email=?", (NOW, ADA))
    status, _ = auth.login(conn, ADA, PW, NOW)
    assert status == "deactivated"


def test_login_password_reset(conn):
    """login.password-reset: submitting the account email sends a
    reset email; completing it sets a new password."""
    conn.actor.set("system", None)
    token = auth.request_password_reset(conn, ADA, NOW)
    assert token is not None
    # a reset email landed in the outbox (never a socket), token inside
    mail = conn.execute(
        "SELECT * FROM email_outbox WHERE template='password_reset'"
        " AND recipient=?", (ADA,)).fetchone()
    assert mail is not None and token in mail["body"]
    # completing sets the new password; old stops working, new works
    assert auth.complete_password_reset(conn, token, "new-synthetic-pw", NOW)
    assert auth.login(conn, ADA, PW, NOW)[0] == "bad_credentials"
    status, _ = auth.login(conn, ADA, "new-synthetic-pw", NOW)
    assert status in ("enrollment_required", "twofa_required")
    # token is single-use
    assert not auth.complete_password_reset(conn, token, "again", NOW)
    # unknown email quietly does nothing (no account enumeration)
    assert auth.request_password_reset(conn, "nobody@example.test", NOW) is None


def test_firm_settings_two_factor_authentication(conn):
    """firm-settings.two-factor-authentication (adapted): OTP from the
    chosen method (app or email) required to complete login; admin
    reset forces re-enrollment at next login."""
    conn.actor.set("system", None)
    bram = "bram.attorney@example.test"
    cleo = "cleo.paralegal@example.test"

    # EMAIL METHOD: enroll, then a fresh login demands the mailed code
    status, token = auth.login(conn, bram, PW, NOW)
    assert status == "enrollment_required"
    auth.enroll_twofa(conn, _uid(conn, bram), "email", token, NOW)
    status2, token2 = auth.login(conn, bram, PW, NOW)
    assert status2 == "twofa_required"
    assert auth.session_user(conn, token2, NOW) is None  # not in yet
    code = conn.execute(
        "SELECT c.code FROM twofa_challenges c JOIN sessions s"
        " ON s.id=c.session_id WHERE s.token=? AND c.used_at IS NULL"
        " ORDER BY c.id DESC LIMIT 1", (token2,)).fetchone()["code"]
    wrong = "000000" if code != "000000" else "111111"
    assert not auth.verify_twofa(conn, token2, wrong, NOW)
    assert auth.verify_twofa(conn, token2, code, NOW)
    assert auth.session_user(conn, token2, NOW) == _uid(conn, bram)

    # APP METHOD: TOTP from the enrolled secret completes login
    status, token = auth.login(conn, cleo, PW, NOW)
    assert status == "enrollment_required"
    secret = auth.enroll_twofa(conn, _uid(conn, cleo), "app", token, NOW)
    status3, token3 = auth.login(conn, cleo, PW, NOW)
    assert status3 == "twofa_required"
    assert not auth.verify_twofa(conn, token3, "000000", NOW)
    assert auth.verify_twofa(conn, token3, auth.totp_code(secret, NOW), NOW)
    assert auth.session_user(conn, token3, NOW) == _uid(conn, cleo)

    # ADMIN RESET: clears 2FA -> next login forces re-enrollment
    conn.actor.set("user", _uid(conn, ADA))
    auth.reset_twofa(conn, _uid(conn, bram))
    status4, _ = auth.login(conn, bram, PW, NOW)
    assert status4 == "enrollment_required"
    # and the reset itself is on the audit trail, attributed to Ada
    row = conn.execute(
        "SELECT actor_type, actor_id FROM audit_log WHERE"
        " entity_type='users' AND entity_id=? AND action='update'"
        " ORDER BY id DESC LIMIT 1", (_uid(conn, bram),)).fetchone()
    assert (row["actor_type"], row["actor_id"]) == ("user", _uid(conn, ADA))
