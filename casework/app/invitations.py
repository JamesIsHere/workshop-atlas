"""Intake invitations (U2.5): email + shareable link, tracking,
revocation, firm defaults. SMS and portal channels are deferred by
ruling (email-only adapted wordings)."""

import json
import secrets

from app import facts


def _default_message(conn):
    row = conn.execute("SELECT value FROM firm_settings WHERE"
                       " key='invitation.default_email_message'").fetchone()
    return row["value"] if row else None


def invite(conn, smart_form_id, contact_id, channel, now, language="en",
           message=None, restricted_tabs=None):
    """Send an invitation. Email invitations carry the custom message
    or the firm's default without retyping (invitation-settings);
    link invitations mint the same secure token."""
    if channel not in ("email", "link"):
        raise ValueError("v1 channels are email and link (SMS/portal"
                         " deferred)")
    token = secrets.token_hex(16)
    if message is None:
        message = _default_message(conn)
    inv_id = conn.execute(
        "INSERT INTO intake_invitations (smart_form_id, contact_id,"
        " channel, token, language, status, status_at, restricted_tabs,"
        " message) VALUES (?,?,?,?,?,'sent',?,?,?)",
        (smart_form_id, contact_id, channel, token, language, now,
         json.dumps(restricted_tabs) if restricted_tabs else None,
         message)).lastrowid
    if channel == "email":
        email = facts.get_fact(conn, "contact", contact_id, "contact.email")
        if email is None:
            raise ValueError(f"contact {contact_id} has no email fact")
        body = (message or "Please complete your questionnaire.") + \
            f"\n\nYour secure link: {link_of(token)}"
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, "Please complete your intake questionnaire", body,
             "intake_invitation", "smart_forms", smart_form_id, now))
    return inv_id


def link_of(token):
    return f"/intake/{token}"


def by_token(conn, token):
    return conn.execute("SELECT * FROM intake_invitations WHERE token=?",
                        (token,)).fetchone()


def _set_status(conn, invitation_id, status, now):
    conn.execute("UPDATE intake_invitations SET status=?, status_at=?"
                 " WHERE id=?", (status, now, invitation_id))


def accept(conn, token, now):
    inv = by_token(conn, token)
    if inv and inv["status"] == "sent":
        _set_status(conn, inv["id"], "accepted", now)


def return_for_review(conn, token, now):
    """Client submits the intake -> Returned for Review with date."""
    inv = by_token(conn, token)
    if inv is None or inv["status"] == "revoked":
        raise ValueError("invitation not live")
    _set_status(conn, inv["id"], "returned", now)


def revoke(conn, invitation_id, now):
    """Revoked -> the intake is no longer accessible via this link."""
    _set_status(conn, invitation_id, "revoked", now)


def resend(conn, invitation_id, now):
    """Resend re-issues the email (same token) and re-marks Sent --
    used after flagging questions for review (fx-0031/0039)."""
    inv = conn.execute("SELECT * FROM intake_invitations WHERE id=?",
                       (invitation_id,)).fetchone()
    if inv is None:
        raise ValueError(f"unknown invitation {invitation_id}")
    if inv["channel"] == "email":
        email = facts.get_fact(conn, "contact", inv["contact_id"],
                               "contact.email")
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, "Reminder: please complete your intake questionnaire",
             (inv["message"] or "Please review the flagged questions.") +
             f"\n\nYour secure link: {link_of(inv['token'])}",
             "intake_invitation_resend", "smart_forms",
             inv["smart_form_id"], now))
    _set_status(conn, invitation_id, "sent", now)


def track(conn, smart_form_id):
    """Invitation tracking: contact, address used, status with its
    date (invitation-tracking)."""
    out = []
    for inv in conn.execute(
            "SELECT * FROM intake_invitations WHERE smart_form_id=?"
            " ORDER BY id", (smart_form_id,)):
        if inv["channel"] == "email":
            address = facts.get_fact(conn, "contact", inv["contact_id"],
                                     "contact.email")
        else:
            address = "shareable link"
        out.append({"invitation_id": inv["id"],
                    "contact_id": inv["contact_id"],
                    "address": address, "channel": inv["channel"],
                    "status": inv["status"], "status_at": inv["status_at"],
                    "link": link_of(inv["token"])})
    return out


def restricted_tabs_of(inv):
    return set(json.loads(inv["restricted_tabs"])) if inv["restricted_tabs"] \
        else set()
