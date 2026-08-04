"""Spine tests: USCIS receipt tracking via the synthetic replay
dataset (U3.5). Receipt numbers are deliberately fake (SYN prefix);
uscis_responses IS the captured dataset (fully synthetic by P3 gate
ruling 1 -- real receipt numbers cannot exist here)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import bulletin, receipts, scheduler  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM = 1, 2
RCPT = "SYN0000000001"


def _respond(conn, number, status, as_of):
    conn.execute("INSERT INTO uscis_responses (receipt_number, status,"
                 " as_of) VALUES (?,?,?)", (number, status, as_of))


def test_case_tracking_uscis_receipt_tracking(conn):
    """uscis-receipt-tracking (adapted): add a receipt number -> its
    current status, sourced from the replay adapter, is displayed on
    the matter and its primary contact."""
    conn.actor.set("user", ADA)
    _respond(conn, RCPT, "Case Was Received", "2026-07-30T12:00:00Z")
    rid = receipts.add_receipt(conn, 1, RCPT, NOW,
                               description="I-130 petition")
    row = conn.execute("SELECT * FROM matter_receipts WHERE id=?",
                       (rid,)).fetchone()
    assert row["current_status"] == "Case Was Received"
    assert row["status_as_of"] == "2026-07-30T12:00:00Z"
    # displayed on the matter's Case Tracking view...
    view = receipts.case_tracking_view(conn, matter_id=1)
    assert [r["receipt_number"] for r in view["receipts"]] == [RCPT]
    assert view["receipts"][0]["current_status"] == "Case Was Received"
    # ...and on its primary contact's (Dana, contact 1)
    cview = receipts.case_tracking_view(conn, contact_id=1)
    assert [r["receipt_number"] for r in cview["receipts"]] == [RCPT]


def test_case_tracking_receipt_status_manual_check(conn):
    """receipt-status-manual-check (adapted): Update beside a receipt
    -> the adapter is queried and the stored status refreshed if
    changed."""
    conn.actor.set("user", ADA)
    _respond(conn, RCPT, "Case Was Received", "2026-07-30T12:00:00Z")
    rid = receipts.add_receipt(conn, 1, RCPT, NOW)
    # dataset moves on
    _respond(conn, RCPT, "Request for Additional Evidence Was Sent",
             "2026-08-02T12:00:00Z")
    changed = receipts.check_receipt(conn, rid, "2026-08-03T09:00:00Z")
    assert changed is True
    row = conn.execute("SELECT * FROM matter_receipts WHERE id=?",
                       (rid,)).fetchone()
    assert row["current_status"] == \
        "Request for Additional Evidence Was Sent"
    assert row["last_checked_at"] == "2026-08-03T09:00:00Z"
    hist = conn.execute(
        "SELECT status, check_kind FROM receipt_status_history WHERE"
        " matter_receipt_id=? ORDER BY id", (rid,)).fetchall()
    assert [(h["status"], h["check_kind"]) for h in hist] == \
        [("Case Was Received", "manual"),
         ("Request for Additional Evidence Was Sent", "manual")]
    # manual refresh is silent -- notifications belong to scheduled
    assert conn.execute("SELECT count(*) FROM notifications").fetchone()[0] == 0
    # unchanged dataset: check updates last_checked_at only
    assert receipts.check_receipt(conn, rid, "2026-08-04T09:00:00Z") is False
    assert conn.execute("SELECT count(*) FROM receipt_status_history"
                        " WHERE matter_receipt_id=?", (rid,)).fetchone()[0] == 2


def test_case_tracking_receipt_status_auto_checks(conn):
    """receipt-status-auto-checks (adapted): the stored status updates
    without user action on the configured schedule; frequency is a
    firm setting, not a subscription tier."""
    conn.actor.set("user", ADA)
    conn.execute("INSERT INTO firm_settings (key, value) VALUES"
                 " ('receipts.check_frequency_hours', '6')")
    _respond(conn, RCPT, "Case Was Received", "2026-07-30T12:00:00Z")
    rid = receipts.add_receipt(conn, 1, RCPT, NOW)  # checked at NOW
    _respond(conn, RCPT, "Case Was Approved", "2026-08-01T10:00:00Z")
    # 2h later: inside the 6h window -> the tick must NOT re-check
    scheduler.tick(conn, "2026-08-01T11:00:00Z")
    row = conn.execute("SELECT * FROM matter_receipts WHERE id=?",
                       (rid,)).fetchone()
    assert row["current_status"] == "Case Was Received"
    # 7h later: due -> status updates without user action
    scheduler.tick(conn, "2026-08-01T16:00:00Z")
    row = conn.execute("SELECT * FROM matter_receipts WHERE id=?",
                       (rid,)).fetchone()
    assert row["current_status"] == "Case Was Approved"
    assert row["last_checked_at"] == "2026-08-01T16:00:00Z"
    hist = conn.execute(
        "SELECT check_kind FROM receipt_status_history WHERE"
        " matter_receipt_id=? ORDER BY id DESC LIMIT 1", (rid,)).fetchone()
    assert hist["check_kind"] == "scheduled"


def test_case_tracking_receipt_status_notifications(conn):
    """receipt-status-notifications (adapted): a scheduled check that
    detects a change -> matter assignees get an email and an in-app
    notification."""
    conn.actor.set("user", ADA)
    _respond(conn, RCPT, "Case Was Received", "2026-07-30T12:00:00Z")
    rid = receipts.add_receipt(conn, 1, RCPT, NOW)  # matter 1 -> Bram
    _respond(conn, RCPT, "Case Was Approved", "2026-08-02T10:00:00Z")
    scheduler.tick(conn, "2026-08-03T09:00:00Z")  # default 24h: due
    mail = conn.execute(
        "SELECT * FROM email_outbox WHERE template='receipt_status'"
        ).fetchall()
    assert [m["recipient"] for m in mail] == ["bram.attorney@example.test"]
    assert RCPT in mail[0]["body"] and "Case Was Approved" in mail[0]["body"]
    n = conn.execute("SELECT * FROM notifications WHERE"
                     " kind='receipt_status'").fetchall()
    assert [r["user_id"] for r in n] == [BRAM]
    payload = json.loads(n[0]["payload"])
    assert payload["receipt_number"] == RCPT
    assert payload["new"] == "Case Was Approved"


def test_case_tracking_module_exists(conn):
    """module-exists: the Case Tracking view on a matter or its
    primary contact displays the tracked statuses -- priority date
    and USCIS receipts together."""
    conn.actor.set("user", ADA)
    bulletin.load_month(conn, "2026-06", NOW)
    _respond(conn, RCPT, "Case Was Received", "2026-07-30T12:00:00Z")
    receipts.add_receipt(conn, 1, RCPT, NOW)
    view = receipts.case_tracking_view(conn, matter_id=1)
    # both tracked-status families, one tab
    assert view["priority_date"]["final_action"]["status"] == "current"
    assert view["priority_date"]["final_action"]["cutoff"] == "01JAN24"
    assert view["receipts"][0]["current_status"] == "Case Was Received"
    # the primary contact's page shows the same chain
    cview = receipts.case_tracking_view(conn, contact_id=1)
    assert cview["matters"][0]["priority_date"]["filing"]["cutoff"] == "C"
    assert cview["receipts"][0]["receipt_number"] == RCPT
