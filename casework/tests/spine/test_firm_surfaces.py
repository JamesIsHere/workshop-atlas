"""Spine tests: U4.4 cross-cutting surfaces -- CSV export,
universal search, notification settings."""

import csv
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import exports, forms, notify, receipts, search  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
LATER = "2026-08-03T09:00:00Z"
EVEN_LATER = "2026-08-06T09:00:00Z"
ADA, BRAM, CLEO = 1, 2, 3
DANA = 1


def _rows(text):
    return list(csv.reader(io.StringIO(text)))


def test_contacts_and_matters_csv_export(conn):
    """csv-export: Export on the Contacts or Matters dashboard -> a
    CSV of all records."""
    conn.actor.set("user", ADA)
    crows = _rows(exports.export_contacts_csv(conn))
    n_contacts = conn.execute(
        "SELECT count(*) FROM contacts WHERE deleted_at IS NULL"
    ).fetchone()[0]
    assert len(crows) == n_contacts + 1  # header + every record
    assert crows[0][:3] == ["id", "kind", "display_name"]
    dana = next(r for r in crows[1:] if r[0] == "1")
    assert dana[2] == "Dana Synthetic"
    assert "dana@example.test" in dana
    mrows = _rows(exports.export_matters_csv(conn))
    n_matters = conn.execute(
        "SELECT count(*) FROM matters WHERE deleted_at IS NULL"
    ).fetchone()[0]
    assert len(mrows) == n_matters + 1
    m1 = next(r for r in mrows[1:] if r[0] == "1")
    assert m1[2] == "Dana Synthetic"  # primary contact resolved


def test_firm_settings_universal_search(conn):
    """universal-search: partial contact/matter/form names match and
    selecting a result opens its page; receipt numbers (full or
    partial) surface the matter AND its primary contact; Recents
    lists the most recently accessed records."""
    conn.actor.set("user", ADA)
    # contact by partial name
    hits = search.search(conn, "dan")
    assert {"type": "contact", "id": DANA,
            "label": "Dana Synthetic"} in hits
    # matter by partial name (matter 1's own title)
    m1_name = conn.execute(
        "SELECT name FROM matters WHERE id=1").fetchone()["name"]
    assert ("matter", 1) in {(h["type"], h["id"])
                             for h in search.search(conn, m1_name[:6])}
    # form by partial title
    sfid = forms.create_smart_form(conn, "Dana searchable intake", NOW,
                                   ADA, contact_id=DANA)
    assert ("smart_form", sfid) in {
        (h["type"], h["id"])
        for h in search.search(conn, "searchable int")}
    # receipt number, partial: matter + primary contact both surface
    conn.execute("INSERT INTO uscis_responses (receipt_number, status,"
                 " as_of) VALUES ('SYN0000000042','Case Was Received',"
                 " '2026-07-30T12:00:00Z')")
    receipts.add_receipt(conn, 1, "SYN0000000042", NOW)
    rhits = search.search(conn, "0000042")
    assert {(h["type"], h["id"]) for h in rhits} == {("matter", 1),
                                                     ("contact", DANA)}
    assert all(h["receipt_number"] == "SYN0000000042" for h in rhits)
    # selecting opens the page and feeds Recents (newest first, dedup)
    opened = search.open_record(conn, ADA, "contact", DANA, NOW)
    assert opened["display_name"] == "Dana Synthetic"
    search.open_record(conn, ADA, "matter", 1, LATER)
    search.open_record(conn, ADA, "contact", DANA, EVEN_LATER)
    assert search.recents(conn, ADA) == [{"type": "contact", "id": DANA},
                                         {"type": "matter", "id": 1}]


def test_firm_settings_notification_settings(conn):
    """notification-settings: admin routes email notifications to
    admin, assignee, or all staff -> subsequent notifications go to
    the selected parties (receipt-status sender retrofit)."""
    conn.actor.set("user", ADA)
    conn.execute("INSERT INTO uscis_responses (receipt_number, status,"
                 " as_of) VALUES ('SYN0000000077','Case Was Received',"
                 " '2026-07-30T12:00:00Z')")
    rid = receipts.add_receipt(conn, 1, "SYN0000000077", NOW)
    # route to ALL staff; a scheduled change mails everyone
    notify.set_routing(conn, "all")
    conn.execute("INSERT INTO uscis_responses (receipt_number, status,"
                 " as_of) VALUES ('SYN0000000077','RFE Sent',"
                 " '2026-08-02T12:00:00Z')")
    receipts.scheduled_checks(conn, LATER)
    got = [r["recipient"] for r in conn.execute(
        "SELECT recipient FROM email_outbox WHERE template="
        "'receipt_status' AND created_at=? ORDER BY id", (LATER,))]
    assert got == ["ada.admin@example.test", "bram.attorney@example.test",
                   "cleo.paralegal@example.test"]
    # route to ADMIN; the next change mails Ada alone
    notify.set_routing(conn, "admin")
    conn.execute("INSERT INTO uscis_responses (receipt_number, status,"
                 " as_of) VALUES ('SYN0000000077','Case Approved',"
                 " '2026-08-05T12:00:00Z')")
    receipts.scheduled_checks(conn, EVEN_LATER)
    got = [r["recipient"] for r in conn.execute(
        "SELECT recipient FROM email_outbox WHERE template="
        "'receipt_status' AND created_at=? ORDER BY id", (EVEN_LATER,))]
    assert got == ["ada.admin@example.test"]
    # in-app notifications ride the same routing
    who = [n["user_id"] for n in conn.execute(
        "SELECT user_id FROM notifications WHERE kind='receipt_status'"
        " AND created_at=?", (EVEN_LATER,))]
    assert who == [ADA]
    # unknown routing values refuse
    try:
        notify.set_routing(conn, "everyone")
        raise AssertionError("bad routing value accepted")
    except ValueError:
        pass
