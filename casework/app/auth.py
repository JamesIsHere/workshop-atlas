"""Auth core (U1.1): passwords, sessions, 2FA, password reset.

Stdlib only. All timestamps ISO-8601 UTC strings; every function that
needs the clock takes `now` (ISO string) so tests are deterministic.
2FA enrollment is MANDATORY (corpus: first login requires MFA
enrollment): a password-authenticated user with twofa_method NULL is
in state 'enrollment_required' -- which is also how an admin's 2FA
reset forces re-enrollment without any schema flag.

Permission enforcement is U1.2's job; nothing here checks levels.
"""

import hashlib
import hmac
import secrets
import struct
from datetime import datetime, timedelta, timezone

SCRYPT_N, SCRYPT_R, SCRYPT_P = 16384, 8, 1
SCRYPT_MAXMEM = 64 * 1024 * 1024
SESSION_DAYS = 14
RESET_HOURS = 24
TOTP_STEP = 30
TOTP_DIGITS = 6


def _parse(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _fmt(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def hash_password(password, salt):
    """PHC-style string; salt is bytes. Deterministic for fixed salt."""
    dk = hashlib.scrypt(password.encode("utf-8"), salt=salt,
                        n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P,
                        maxmem=SCRYPT_MAXMEM, dklen=64)
    return (f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}"
            f"${salt.hex()}${dk.hex()}")


def verify_password(password, stored):
    try:
        algo, n, r, p, salt_hex, hash_hex = stored.split("$")
    except ValueError:
        return False
    if algo != "scrypt":
        return False
    dk = hashlib.scrypt(password.encode("utf-8"), salt=bytes.fromhex(salt_hex),
                        n=int(n), r=int(r), p=int(p),
                        maxmem=SCRYPT_MAXMEM, dklen=64)
    return hmac.compare_digest(dk.hex(), hash_hex)


def set_password(conn, user_id, password):
    salt = secrets.token_bytes(16)
    conn.execute("UPDATE users SET password_hash=? WHERE id=?",
                 (hash_password(password, salt), user_id))


# --- login / sessions ---

def login(conn, email, password, now):
    """Password-authenticate; returns (status, token-or-None).

    status: bad_credentials | deactivated | enrollment_required |
    twofa_required | ok. A session row exists for the last three;
    twofa_passed=1 only for ok.
    """
    row = conn.execute(
        "SELECT * FROM users WHERE email=? AND deleted_at IS NULL",
        (email,)).fetchone()
    if row is None or not verify_password(password, row["password_hash"]):
        return ("bad_credentials", None)
    if row["deactivated_at"] is not None:
        return ("deactivated", None)
    token = secrets.token_hex(32)
    expires = _fmt(_parse(now) + timedelta(days=SESSION_DAYS))
    if row["twofa_method"] is None:
        status, passed = "enrollment_required", 0
    else:
        status, passed = "twofa_required", 0
    conn.execute(
        "INSERT INTO sessions (token, user_id, created_at, expires_at,"
        " twofa_passed) VALUES (?,?,?,?,?)",
        (token, row["id"], now, expires, passed))
    if status == "twofa_required" and row["twofa_method"] == "email":
        _issue_email_challenge(conn, token, row, now)
    return (status, token)


def session_user(conn, token, now):
    """Fully-authenticated user id for token, else None."""
    row = conn.execute(
        "SELECT s.user_id, s.expires_at, s.twofa_passed FROM sessions s"
        " WHERE s.token=?", (token,)).fetchone()
    if row is None or not row["twofa_passed"]:
        return None
    if _parse(now) >= _parse(row["expires_at"]):
        return None
    return row["user_id"]


def logout(conn, token):
    # FKs are RESTRICT: clear the session's ephemeral challenges first
    conn.execute("DELETE FROM twofa_challenges WHERE session_id IN"
                 " (SELECT id FROM sessions WHERE token=?)", (token,))
    conn.execute("DELETE FROM sessions WHERE token=?", (token,))


# --- 2FA ---

def _totp(secret_hex, at, step_offset=0):
    counter = int(_parse(at).timestamp()) // TOTP_STEP + step_offset
    digest = hmac.new(bytes.fromhex(secret_hex),
                      struct.pack(">Q", counter), hashlib.sha1).digest()
    off = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[off:off + 4])[0] & 0x7FFFFFFF)
    return str(code % (10 ** TOTP_DIGITS)).zfill(TOTP_DIGITS)


def totp_code(secret_hex, at):
    """Current TOTP code -- what the authenticator app would show."""
    return _totp(secret_hex, at)


def enroll_twofa(conn, user_id, method, token, now):
    """Set 2FA method for the session's user. Returns the app secret
    for method 'app' (to load into an authenticator), else None. The
    session stays unverified until verify_twofa succeeds."""
    if method not in ("app", "email"):
        raise ValueError(f"unknown 2fa method: {method}")
    secret = secrets.token_hex(20) if method == "app" else None
    conn.execute("UPDATE users SET twofa_method=?, totp_secret=? WHERE id=?",
                 (method, secret, user_id))
    if method == "email":
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        _issue_email_challenge(conn, token, row, now)
    return secret


def _issue_email_challenge(conn, token, user_row, now):
    sid = conn.execute("SELECT id FROM sessions WHERE token=?",
                       (token,)).fetchone()["id"]
    code = str(secrets.randbelow(10 ** TOTP_DIGITS)).zfill(TOTP_DIGITS)
    conn.execute(
        "INSERT INTO twofa_challenges (session_id, code, created_at)"
        " VALUES (?,?,?)", (sid, code, now))
    conn.execute(
        "INSERT INTO email_outbox (recipient, subject, body, template,"
        " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (user_row["email"], "Your login code",
         f"Your verification code is {code}", "twofa_code",
         "users", user_row["id"], now))


def verify_twofa(conn, token, code, now):
    """Complete a twofa_required session. True on success."""
    sess = conn.execute(
        "SELECT s.id, s.user_id, u.twofa_method, u.totp_secret"
        " FROM sessions s JOIN users u ON u.id = s.user_id"
        " WHERE s.token=?", (token,)).fetchone()
    if sess is None or sess["twofa_method"] is None:
        return False
    ok = False
    if sess["twofa_method"] == "app":
        # accept adjacent steps for clock skew
        ok = any(hmac.compare_digest(_totp(sess["totp_secret"], now, d), code)
                 for d in (-1, 0, 1))
    else:
        chal = conn.execute(
            "SELECT id, code FROM twofa_challenges WHERE session_id=?"
            " AND used_at IS NULL ORDER BY id DESC LIMIT 1",
            (sess["id"],)).fetchone()
        if chal is not None and hmac.compare_digest(chal["code"], code):
            conn.execute("UPDATE twofa_challenges SET used_at=? WHERE id=?",
                         (now, chal["id"]))
            ok = True
    if ok:
        conn.execute("UPDATE sessions SET twofa_passed=1 WHERE id=?",
                     (sess["id"],))
    return ok


def reset_twofa(conn, target_user_id):
    """Admin action: clear 2FA so the next login forces re-enrollment.
    Caller is responsible for actor attribution (conn.actor)."""
    conn.execute("UPDATE users SET twofa_method=NULL, totp_secret=NULL"
                 " WHERE id=?", (target_user_id,))


# --- password reset ---

def request_password_reset(conn, email, now):
    """Always quietly succeeds (no account enumeration); mails a reset
    token via the outbox when the address matches a live user."""
    row = conn.execute(
        "SELECT * FROM users WHERE email=? AND deleted_at IS NULL",
        (email,)).fetchone()
    if row is None:
        return None
    token = secrets.token_hex(32)
    conn.execute(
        "INSERT INTO password_resets (user_id, token, created_at)"
        " VALUES (?,?,?)", (row["id"], token, now))
    conn.execute(
        "INSERT INTO email_outbox (recipient, subject, body, template,"
        " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (row["email"], "Password reset",
         f"Use this token to set a new password: {token}",
         "password_reset", "users", row["id"], now))
    return token


def complete_password_reset(conn, token, new_password, now):
    """Single-use, expiring token -> set the new password. True on success."""
    row = conn.execute(
        "SELECT * FROM password_resets WHERE token=?", (token,)).fetchone()
    if row is None or row["used_at"] is not None:
        return False
    if _parse(now) - _parse(row["created_at"]) > timedelta(hours=RESET_HOURS):
        return False
    set_password(conn, row["user_id"], new_password)
    conn.execute("UPDATE password_resets SET used_at=? WHERE id=?",
                 (now, row["id"]))
    return True
