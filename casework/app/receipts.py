"""USCIS receipt tracking (U3.5): replay adapter + Case Tracking view.

uscis_responses is the captured dataset -- FULLY SYNTHETIC by P3
gate ruling 1 (receipt numbers must be fake; live USCIS querying is
post-v1). The adapter reads the latest response per receipt; status
lands on matter_receipts with an append-only history. Manual checks
refresh silently; scheduled checks (scheduler.tick, frequency =
firm setting) notify the matter's assignees on change.
"""

import json
from datetime import datetime, timedelta, timezone

FREQ_KEY = "receipts.check_frequency_hours"
FREQ_DEFAULT_HOURS = 24


def _parse(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)


def adapter_status(conn, receipt_number):
    """Latest captured response for a receipt, or None."""
    return conn.execute(
        "SELECT status, as_of FROM uscis_responses WHERE receipt_number=?"
        " ORDER BY as_of DESC, id DESC LIMIT 1", (receipt_number,)
    ).fetchone()


def add_receipt(conn, matter_id, receipt_number, now, description=None):
    """Adding a receipt performs the initial adapter lookup so the
    status displays immediately (adapted uscis-receipt-tracking)."""
    rid = conn.execute(
        "INSERT INTO matter_receipts (matter_id, receipt_number,"
        " description) VALUES (?,?,?)",
        (matter_id, receipt_number, description)).lastrowid
    check_receipt(conn, rid, now)
    return rid


def check_receipt(conn, receipt_id, now, kind="manual"):
    """Query the adapter; refresh stored status if changed. Returns
    True when the status moved. Scheduled changes notify."""
    r = conn.execute("SELECT * FROM matter_receipts WHERE id=?",
                     (receipt_id,)).fetchone()
    latest = adapter_status(conn, r["receipt_number"])
    conn.execute("UPDATE matter_receipts SET last_checked_at=? WHERE id=?",
                 (now, receipt_id))
    if latest is None or latest["status"] == r["current_status"]:
        return False
    conn.execute(
        "UPDATE matter_receipts SET current_status=?, status_as_of=?"
        " WHERE id=?", (latest["status"], latest["as_of"], receipt_id))
    conn.execute(
        "INSERT INTO receipt_status_history (matter_receipt_id, status,"
        " recorded_at, check_kind) VALUES (?,?,?,?)",
        (receipt_id, latest["status"], now, kind))
    if kind == "scheduled":
        _notify(conn, r, latest["status"], now)
    return True


def scheduled_checks(conn, now):
    """Tick handler: check every live receipt whose last check is
    older than the configured frequency."""
    row = conn.execute("SELECT value FROM firm_settings WHERE key=?",
                       (FREQ_KEY,)).fetchone()
    hours = int(row["value"]) if row is not None else FREQ_DEFAULT_HOURS
    threshold = _parse(now) - timedelta(hours=hours)
    for r in conn.execute(
            "SELECT id, last_checked_at FROM matter_receipts WHERE"
            " deleted_at IS NULL ORDER BY id").fetchall():
        if r["last_checked_at"] is not None \
                and _parse(r["last_checked_at"]) > threshold:
            continue
        check_receipt(conn, r["id"], now, kind="scheduled")


def _notify(conn, receipt_row, new_status, now):
    from app import notify  # lazy: keeps module deps one-way
    m = conn.execute("SELECT * FROM matters WHERE id=?",
                     (receipt_row["matter_id"],)).fetchone()
    # U4.4 retrofit: recipients follow the firm-wide notification
    # routing setting ('assignee' default = pre-P4 behavior)
    targets = notify.recipients(conn, matter_id=m["id"])
    payload = json.dumps({"matter_id": m["id"],
                          "receipt_number": receipt_row["receipt_number"],
                          "old": receipt_row["current_status"],
                          "new": new_status})
    for uid in targets:
        conn.execute(
            "INSERT INTO notifications (user_id, kind, payload, created_at)"
            " VALUES (?,?,?,?)", (uid, "receipt_status", payload, now))
        email = conn.execute("SELECT email FROM users WHERE id=?",
                             (uid,)).fetchone()["email"]
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, f"Case status update on {m['name']}",
             f"Receipt {receipt_row['receipt_number']} on {m['name']}"
             f" moved to: {new_status}.",
             "receipt_status", "matters", m["id"], now))


def case_tracking_view(conn, matter_id=None, contact_id=None):
    """The Case Tracking tab: priority-date status + receipts, on a
    matter or on a contact (aggregating its primary matters)."""
    from app import bulletin  # lazy: keeps module deps one-way
    if (matter_id is None) == (contact_id is None):
        raise ValueError("exactly one of matter_id/contact_id")
    if matter_id is not None:
        return {"priority_date": bulletin.matter_status(conn, matter_id),
                "receipts": _receipts_of(conn, [matter_id])}
    mids = [r["id"] for r in conn.execute(
        "SELECT id FROM matters WHERE primary_contact_id=? AND"
        " deleted_at IS NULL ORDER BY id", (contact_id,))]
    return {"matters": [{"matter_id": mid,
                         "priority_date": bulletin.matter_status(conn, mid)}
                        for mid in mids],
            "receipts": _receipts_of(conn, mids)}


def _receipts_of(conn, matter_ids):
    out = []
    for mid in matter_ids:
        out.extend(conn.execute(
            "SELECT * FROM matter_receipts WHERE matter_id=? AND"
            " deleted_at IS NULL ORDER BY id", (mid,)).fetchall())
    return out
