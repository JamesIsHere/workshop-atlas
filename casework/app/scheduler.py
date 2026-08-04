"""Scheduler (U3.1): the shared tick. No daemon, no wall clock.

tick(conn, now) dispatches every piece of due time-driven work:
event reminders here, receipt auto-checks join in U3.5. Tests (and,
post-v1, an OS scheduler entry) drive time by calling tick with an
explicit now -- determinism is the point, do not reach for real
clocks. Work dispatched by the tick attributes to the system actor;
the caller's actor is restored on exit.
"""

from datetime import datetime, timedelta, timezone

from app import events


def _parse(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)


def _fmt(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _minus_months(dt, months):
    """Calendar-month subtraction, day clamped to the target month."""
    total = dt.year * 12 + (dt.month - 1) - months
    year, month = divmod(total, 12)
    month += 1
    for day in range(dt.day, 27, -1):
        try:
            return dt.replace(year=year, month=month, day=day)
        except ValueError:
            continue
    return dt.replace(year=year, month=month, day=min(dt.day, 28))


def fire_time(starts_at, offset_value, offset_unit):
    start = _parse(starts_at)
    if offset_unit == "months":
        return _minus_months(start, offset_value)
    delta = timedelta(**{offset_unit: offset_value})
    return start - delta


def tick(conn, now):
    """Dispatch all due work as the system actor."""
    from app import billing, receipts  # lazy: avoids an import cycle
    prev = (conn.actor.actor_type, conn.actor.actor_id)
    conn.actor.set("system", None)
    try:
        _fire_event_reminders(conn, now)
        receipts.scheduled_checks(conn, now)
        billing.scheduled_work(conn, now)
    finally:
        conn.actor.set(*prev)


def _fire_event_reminders(conn, now):
    due = conn.execute(
        "SELECT r.id, r.event_id, r.offset_value, r.offset_unit,"
        " e.title, e.starts_at FROM event_reminders r"
        " JOIN events e ON e.id = r.event_id"
        " WHERE r.fired_at IS NULL AND e.deleted_at IS NULL").fetchall()
    now_dt = _parse(now)
    for r in due:
        if fire_time(r["starts_at"], r["offset_value"],
                     r["offset_unit"]) > now_dt:
            continue
        for email, name in events.attendee_emails(conn, r["event_id"]):
            conn.execute(
                "INSERT INTO email_outbox (recipient, subject, body,"
                " template, entity_type, entity_id, created_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (email, f"Reminder: {r['title']}",
                 f"Dear {name}, this is a reminder for {r['title']}"
                 f" starting {r['starts_at']}.",
                 "event_reminder", "events", r["event_id"], now))
        conn.execute("UPDATE event_reminders SET fired_at=? WHERE id=?",
                     (now, r["id"]))
