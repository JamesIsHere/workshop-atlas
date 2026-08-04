"""Spine tests: expiry auto-calendaring + VMAX report (U3.2)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import expiry, facts, reports, scheduler  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM = 1, 2
DANA = 1  # contact; matter 1 primary, assignee Bram


def test_contacts_and_matters_expiry_date_reminders(conn):
    """expiry-date-reminders: entering an expiry date with a reminder
    setting configured -> event + notification reminder created
    automatically; recipients rule + client attendee honored."""
    conn.actor.set("user", ADA)
    expiry.configure_reminder(conn, "imm.ead_expiry", 60,
                              "assignees", include_client=1)
    expiry.configure_reminder(conn, "imm.ead_expiry", 30, "assignees")
    expiry.set_expiry_date(conn, DANA, "imm.ead_expiry", "2026-12-01", NOW)
    evs = conn.execute(
        "SELECT * FROM events WHERE source='expiry_auto' AND contact_id=?"
        " AND deleted_at IS NULL ORDER BY id", (DANA,)).fetchall()
    assert len(evs) == 2  # one per configured reminder setting
    assert all(e["starts_at"] == "2026-12-01T00:00:00Z" for e in evs)
    assert "EAD expiry" in evs[0]["title"]
    offsets = [conn.execute(
        "SELECT offset_value, offset_unit FROM event_reminders WHERE"
        " event_id=?", (e["id"],)).fetchone() for e in evs]
    assert sorted((o["offset_value"], o["offset_unit"]) for o in offsets) \
        == [(30, "days"), (60, "days")]
    # recipients=assignees -> Bram (matter 1 assignee); client included
    att = conn.execute(
        "SELECT user_id, contact_id FROM event_attendees WHERE event_id=?",
        (evs[0]["id"],)).fetchall()
    pairs = [(a["user_id"], a["contact_id"]) for a in att]
    assert (BRAM, None) in pairs and (None, DANA) in pairs
    # the reminder rides the standard tick: 60 days out -> outbox email
    scheduler.tick(conn, "2026-10-02T09:00:00Z")
    mails = conn.execute(
        "SELECT recipient FROM email_outbox WHERE template='event_reminder'"
        " AND entity_id=?", (evs[0]["id"],)).fetchall()
    assert "bram.attorney@example.test" in [m["recipient"] for m in mails]
    # re-entering the date supersedes the old auto events, never stacks
    expiry.set_expiry_date(conn, DANA, "imm.ead_expiry", "2027-03-01", NOW)
    live = conn.execute(
        "SELECT starts_at FROM events WHERE source='expiry_auto'"
        " AND contact_id=? AND deleted_at IS NULL", (DANA,)).fetchall()
    assert len(live) == 2
    assert all(e["starts_at"] == "2027-03-01T00:00:00Z" for e in live)
    # custom expiry dates extend the type list (contact-level)
    key = facts.define_custom_attribute(conn, "visa_stamp_expiry", "contact",
                                        "expiry", "Visa stamp expiry")
    expiry.configure_reminder(conn, key, 14, "all")
    expiry.set_expiry_date(conn, DANA, key, "2026-11-15", NOW)
    ev = conn.execute(
        "SELECT * FROM events WHERE source='expiry_auto' AND contact_id=?"
        " AND deleted_at IS NULL AND starts_at='2026-11-15T00:00:00Z'",
        (DANA,)).fetchone()
    assert ev is not None and "Visa stamp expiry" in ev["title"]
    # a non-expiry fact key is refused
    try:
        expiry.configure_reminder(conn, "bio.date_of_birth", 30, "all")
        assert False, "non-expiry key must be refused"
    except ValueError:
        pass


def test_reports_vmax_tracking(conn):
    """vmax-tracking: set a contact's VMAX date, run the VMAX report ->
    contacts ordered by time remaining in status; corpus columns;
    date-range filter."""
    conn.actor.set("user", ADA)
    # seeded: Dana (contact 1) vmax 2027-06-30; add two more
    facts.set_fact(conn, "contact", 2, "imm.vmax_date", "2026-10-15", NOW)
    facts.set_fact(conn, "contact", 3, "imm.vmax_date", "2028-01-01", NOW)
    rows = reports.vmax_report(conn, NOW)
    names = [r["contact"] for r in rows]
    # least time remaining first
    assert names == ["Emil Synthetic", "Dana Synthetic", "Fara Synthetic"]
    assert [set(r) >= {"contact", "email", "principal_applicant",
                       "vmax_time_remaining_days", "vmax_date"}
            for r in rows] == [True, True, True]
    emil = rows[0]
    assert emil["vmax_date"] == "2026-10-15"
    assert emil["vmax_time_remaining_days"] == 75  # 2026-08-01 -> 10-15
    assert emil["email"] == "emil@example.test"
    # date-range filter: only expirations inside the window
    windowed = reports.vmax_report(conn, NOW, start="2026-09-01",
                                   end="2027-12-31")
    assert [r["contact"] for r in windowed] == \
        ["Emil Synthetic", "Dana Synthetic"]
