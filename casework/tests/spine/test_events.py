"""Spine tests: events module (U3.1)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import events, scheduler  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM = 1, 2
DANA = 1  # contact


def test_events_module_exists(conn):
    """module-exists: create an event -> it appears on the firm
    calendar and can be reopened and edited."""
    conn.actor.set("user", ADA)
    eid = events.create_event(
        conn, "USCIS interview -- Dana", "2026-09-10T14:00:00Z", NOW, ADA,
        description="Field office", ends_at="2026-09-10T15:00:00Z",
        contact_id=DANA, matter_id=1)
    cal = events.list_events(conn, "2026-09-01T00:00:00Z",
                             "2026-10-01T00:00:00Z")
    assert eid in [e["id"] for e in cal]
    # reopen and edit
    events.update_event(conn, eid, title="USCIS interview -- Dana (moved)",
                        starts_at="2026-09-11T14:00:00Z")
    e = conn.execute("SELECT * FROM events WHERE id=?", (eid,)).fetchone()
    assert e["title"].endswith("(moved)")
    assert e["starts_at"] == "2026-09-11T14:00:00Z"
    # a soft-deleted event leaves the calendar
    conn.execute("UPDATE events SET deleted_at=?, deleted_by=? WHERE id=?",
                 (NOW, ADA, eid))
    cal = events.list_events(conn, "2026-09-01T00:00:00Z",
                             "2026-10-01T00:00:00Z")
    assert eid not in [e["id"] for e in cal]


def test_events_event_attendees(conn):
    """event-attendees: search a firm member or contact by name or
    email and select them -> that person is an attendee."""
    conn.actor.set("user", ADA)
    eid = events.create_event(conn, "Strategy call",
                              "2026-08-15T10:00:00Z", NOW, ADA)
    # firm member found by name fragment
    hits = events.search_people(conn, "bram")
    assert ("user", BRAM) in [(h["kind"], h["id"]) for h in hits]
    # contact found by email address
    hits = events.search_people(conn, "dana@example.test")
    assert ("contact", DANA) in [(h["kind"], h["id"]) for h in hits]
    events.add_attendee(conn, eid, user_id=BRAM)
    events.add_attendee(conn, eid, contact_id=DANA)
    rows = conn.execute("SELECT user_id, contact_id FROM event_attendees"
                        " WHERE event_id=?", (eid,)).fetchall()
    assert (BRAM, None) in [(r["user_id"], r["contact_id"]) for r in rows]
    assert (None, DANA) in [(r["user_id"], r["contact_id"]) for r in rows]


def test_events_event_reminders(conn):
    """event-reminders (adapted): value + unit of time -> attendees
    receive an EMAIL reminder that far before the start; multiple
    reminders per event; SMS refused."""
    conn.actor.set("user", ADA)
    eid = events.create_event(conn, "Filing deadline",
                              "2026-08-20T09:00:00Z", NOW, ADA)
    events.add_attendee(conn, eid, user_id=BRAM)
    events.add_attendee(conn, eid, contact_id=DANA)
    events.add_reminder(conn, eid, 2, "days")
    events.add_reminder(conn, eid, 1, "hours")
    # SMS is refused by adaptation, not silently accepted
    try:
        events.add_reminder(conn, eid, 30, "minutes", channel="sms")
        assert False, "sms reminder must be refused"
    except ValueError:
        pass
    # before the first fire time: nothing goes out
    scheduler.tick(conn, "2026-08-17T09:00:00Z")
    assert conn.execute("SELECT count(*) FROM email_outbox WHERE"
                        " template='event_reminder'").fetchone()[0] == 0
    # 2 days before start: first reminder -> both attendees, email only
    scheduler.tick(conn, "2026-08-18T09:00:00Z")
    mails = conn.execute(
        "SELECT recipient, subject FROM email_outbox WHERE"
        " template='event_reminder' AND entity_id=?", (eid,)).fetchall()
    recips = sorted(m["recipient"] for m in mails)
    assert recips == ["bram.attorney@example.test", "dana@example.test"]
    assert all("Filing deadline" in m["subject"] for m in mails)
    # re-tick: no duplicate sends
    scheduler.tick(conn, "2026-08-18T10:00:00Z")
    assert conn.execute("SELECT count(*) FROM email_outbox WHERE"
                        " template='event_reminder'").fetchone()[0] == 2
    # 1 hour before start: the second reminder fires independently
    scheduler.tick(conn, "2026-08-20T08:00:00Z")
    assert conn.execute("SELECT count(*) FROM email_outbox WHERE"
                        " template='event_reminder'").fetchone()[0] == 4


def test_events_default_reminder_settings(conn):
    """default-reminder-settings: admin sets firm default
    notifications -> new events carry those reminders by default."""
    conn.actor.set("user", ADA)
    events.set_default_reminders(conn, [{"value": 1, "unit": "days"},
                                        {"value": 30, "unit": "minutes"}])
    raw = conn.execute("SELECT value FROM firm_settings WHERE key=?",
                       ("events.default_reminders",)).fetchone()["value"]
    assert json.loads(raw) == [{"value": 1, "unit": "days"},
                               {"value": 30, "unit": "minutes"}]
    eid = events.create_event(conn, "Consult", "2026-08-25T11:00:00Z",
                              NOW, ADA)
    rows = conn.execute(
        "SELECT offset_value, offset_unit FROM event_reminders WHERE"
        " event_id=? ORDER BY id", (eid,)).fetchall()
    assert [(r["offset_value"], r["offset_unit"]) for r in rows] == \
        [(1, "days"), (30, "minutes")]
    # defaults are defaults, not law: opting out creates none
    eid2 = events.create_event(conn, "Quick sync", "2026-08-26T11:00:00Z",
                               NOW, ADA, use_defaults=False)
    assert conn.execute("SELECT count(*) FROM event_reminders WHERE"
                        " event_id=?", (eid2,)).fetchone()[0] == 0
