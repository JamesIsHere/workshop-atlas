"""Events (U3.1): firm calendar, attendees, email reminders.

Capability parity with events.*: creation/editing, attendee search
across firm members and contacts, reminder offsets (value + unit,
multiple per event). Channel is EMAIL ONLY -- the adapted criterion
defers SMS with prejudice; add_reminder refuses anything else.
Reminder dispatch lives in scheduler.tick, not here.
"""

import json

from app import facts

OFFSET_UNITS = ("minutes", "hours", "days", "weeks", "months")

DEFAULTS_KEY = "events.default_reminders"


def create_event(conn, title, starts_at, now, created_by, description=None,
                 ends_at=None, contact_id=None, matter_id=None,
                 use_defaults=True):
    eid = conn.execute(
        "INSERT INTO events (title, description, starts_at, ends_at,"
        " contact_id, matter_id, created_at, created_by)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (title, description, starts_at, ends_at, contact_id, matter_id,
         now, created_by)).lastrowid
    if use_defaults:
        for d in default_reminders(conn):
            add_reminder(conn, eid, d["value"], d["unit"])
    return eid


def update_event(conn, event_id, **fields):
    allowed = ("title", "description", "starts_at", "ends_at",
               "contact_id", "matter_id")
    unknown = set(fields) - set(allowed)
    if unknown:
        raise ValueError(f"not editable: {', '.join(sorted(unknown))}")
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE events SET {sets} WHERE id=?",
                 (*fields.values(), event_id))


def list_events(conn, start=None, end=None):
    """Calendar window: non-deleted events ordered by start."""
    q = "SELECT * FROM events WHERE deleted_at IS NULL"
    params = []
    if start is not None:
        q += " AND starts_at >= ?"
        params.append(start)
    if end is not None:
        q += " AND starts_at < ?"
        params.append(end)
    return conn.execute(q + " ORDER BY starts_at, id", params).fetchall()


# --- attendees ---

def search_people(conn, query):
    """Firm members and contacts matched by name or email; the
    Attendees box search (fx-0240)."""
    like = f"%{query}%"
    hits = []
    for r in conn.execute(
            "SELECT id, name, email FROM users WHERE deleted_at IS NULL"
            " AND (name LIKE ? OR email LIKE ?) ORDER BY id", (like, like)):
        hits.append({"kind": "user", "id": r["id"], "name": r["name"],
                     "email": r["email"]})
    for r in conn.execute(
            "SELECT c.id, c.display_name, f.value AS email FROM contacts c"
            " LEFT JOIN facts f ON f.subject_type='contact'"
            "  AND f.subject_id=c.id AND f.key='contact.email' AND f.idx=0"
            " WHERE c.deleted_at IS NULL"
            "  AND (c.display_name LIKE ? OR f.value LIKE ?)"
            " ORDER BY c.id", (like, like)):
        hits.append({"kind": "contact", "id": r["id"],
                     "name": r["display_name"], "email": r["email"]})
    return hits


def add_attendee(conn, event_id, user_id=None, contact_id=None):
    if (user_id is None) == (contact_id is None):
        raise ValueError("exactly one of user_id/contact_id")
    conn.execute(
        "INSERT INTO event_attendees (event_id, user_id, contact_id)"
        " VALUES (?,?,?)", (event_id, user_id, contact_id))


def attendee_emails(conn, event_id):
    """(email, display) per attendee that has an address."""
    out = []
    rows = conn.execute("SELECT user_id, contact_id FROM event_attendees"
                        " WHERE event_id=?", (event_id,)).fetchall()
    for r in rows:
        if r["user_id"] is not None:
            u = conn.execute("SELECT name, email FROM users WHERE id=?",
                             (r["user_id"],)).fetchone()
            if u is not None:
                out.append((u["email"], u["name"]))
        else:
            email = facts.get_fact(conn, "contact", r["contact_id"],
                                   "contact.email")
            if email is not None:
                c = conn.execute("SELECT display_name FROM contacts"
                                 " WHERE id=?", (r["contact_id"],)).fetchone()
                out.append((email, c["display_name"]))
    return out


# --- reminders ---

def add_reminder(conn, event_id, value, unit, channel="email"):
    if channel != "email":
        raise ValueError("email reminders only: SMS is deferred with"
                         " prejudice (adapted criterion)")
    if unit not in OFFSET_UNITS:
        raise ValueError(f"unknown offset unit: {unit}")
    return conn.execute(
        "INSERT INTO event_reminders (event_id, offset_value, offset_unit,"
        " channel) VALUES (?,?,?,'email')", (event_id, value, unit)).lastrowid


def default_reminders(conn):
    row = conn.execute("SELECT value FROM firm_settings WHERE key=?",
                       (DEFAULTS_KEY,)).fetchone()
    return json.loads(row["value"]) if row is not None else []


def set_default_reminders(conn, reminders):
    for d in reminders:
        if d["unit"] not in OFFSET_UNITS:
            raise ValueError(f"unknown offset unit: {d['unit']}")
    payload = json.dumps(reminders)
    conn.execute(
        "INSERT INTO firm_settings (key, value) VALUES (?,?)"
        " ON CONFLICT (key) DO UPDATE SET value=excluded.value",
        (DEFAULTS_KEY, payload))
