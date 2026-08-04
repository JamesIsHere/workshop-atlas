"""Expiry auto-calendaring (U3.2): dates in, deadlines out.

Per expiry-type reminder config (lead time + recipients + optional
client attendee); entering an expiry date through set_expiry_date
writes the fact store ONCE and auto-creates the calendar event and
its reminder (fx-0147). Events carry source='expiry_auto' +
source_fact_id so re-entering a date supersedes its own events and
never touches manual ones. Dispatch is scheduler.tick's job.
"""

from datetime import datetime, timedelta, timezone

from app import events, facts


def configure_reminder(conn, fact_key, lead_days, recipients,
                       include_client=0):
    """One row per reminder; several rows per type = several
    reminders (fx-0147 multiple-reminders detail)."""
    d = facts.definition(conn, fact_key)
    if d is None:
        raise ValueError(f"undefined fact key: {fact_key}")
    if d["value_type"] != "expiry" or d["subject_type"] != "contact":
        raise ValueError(f"{fact_key} is not a contact expiry date")
    return conn.execute(
        "INSERT INTO expiry_reminder_settings (fact_key, lead_days,"
        " recipients, include_client) VALUES (?,?,?,?)",
        (fact_key, lead_days, recipients, include_client)).lastrowid


def _recipient_users(conn, rule, contact_id):
    if rule == "admin":
        q = ("SELECT id FROM users WHERE deleted_at IS NULL"
             " AND is_admin=1 ORDER BY id")
        return [r["id"] for r in conn.execute(q)]
    if rule == "all":
        return [r["id"] for r in conn.execute(
            "SELECT id FROM users WHERE deleted_at IS NULL ORDER BY id")]
    # assignees of the associated contact: staff assigned to its live
    # matters (contacts carry no assignee of their own)
    return [r["assignee_id"] for r in conn.execute(
        "SELECT DISTINCT assignee_id FROM matters WHERE"
        " primary_contact_id=? AND deleted_at IS NULL"
        " AND assignee_id IS NOT NULL ORDER BY assignee_id",
        (contact_id,))]


def set_expiry_date(conn, contact_id, fact_key, date, now):
    """Write the fact, then rebuild this fact's auto events: one per
    configured reminder setting, reminder at lead_days before."""
    facts.set_fact(conn, "contact", contact_id, fact_key, date, now)
    fact_id = conn.execute(
        "SELECT id FROM facts WHERE subject_type='contact' AND"
        " subject_id=? AND key=? AND idx=0", (contact_id, fact_key)
    ).fetchone()["id"]
    # supersede: prior auto events for this fact leave the calendar
    conn.execute(
        "UPDATE events SET deleted_at=?, deleted_by=NULL WHERE"
        " source='expiry_auto' AND source_fact_id=? AND deleted_at IS NULL",
        (now, fact_id))
    label = facts.definition(conn, fact_key)["label"]
    contact = conn.execute("SELECT display_name FROM contacts WHERE id=?",
                           (contact_id,)).fetchone()
    settings = conn.execute(
        "SELECT * FROM expiry_reminder_settings WHERE fact_key=?"
        " ORDER BY id", (fact_key,)).fetchall()
    created = []
    for s in settings:
        eid = conn.execute(
            "INSERT INTO events (title, starts_at, contact_id, source,"
            " source_fact_id, created_at, created_by)"
            " VALUES (?,?,?,?,?,?,?)",
            (f"{label} -- {contact['display_name']}", f"{date}T00:00:00Z",
             contact_id, "expiry_auto", fact_id, now, None)).lastrowid
        events.add_reminder(conn, eid, s["lead_days"], "days")
        for uid in _recipient_users(conn, s["recipients"], contact_id):
            events.add_attendee(conn, eid, user_id=uid)
        if s["include_client"]:
            events.add_attendee(conn, eid, contact_id=contact_id)
        created.append(eid)
    return created
