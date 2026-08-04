"""Time tracking (casework-billing P4 U4.1; fx-0064, fx-0073).

Entries carry duration, date, description, contact and/or matter.
Durations parse the attested formats (2h, 36m, 2.8h, 5.5m). The
timer is a running entry (timer_started_at set); stop accrues the
elapsed span into duration_seconds and a stopped timer can resume.

Rates (goal.md decision default 4 -- OUR design, the corpus attests
no mechanism): per-user default hourly rate in user_settings
(billing.hourly_rate_cents), per-entry override column; the charge
amount at import time is duration x rate rounded half-up to the
cent. Money integer cents throughout.
"""

from datetime import datetime, timezone


class TimeError(ValueError):
    pass


def parse_duration(text):
    """'2h', '36m', '2.8h', '5.5m' -> seconds (fx-0064 formats)."""
    t = text.strip().lower()
    if not t or t[-1] not in "hm":
        raise TimeError(f"unrecognized duration: {text!r}")
    try:
        value = float(t[:-1])
    except ValueError:
        raise TimeError(f"unrecognized duration: {text!r}")
    seconds = value * (3600 if t[-1] == "h" else 60)
    return int(round(seconds))


def _parse_ts(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)


def create_entry(conn, user_id, entry_date, duration=None,
                 duration_seconds=None, description=None, contact_id=None,
                 matter_id=None, rate_cents_per_hour=None):
    if contact_id is None and matter_id is None:
        raise TimeError("a time entry needs a contact or matter (fx-0064)")
    if duration is not None:
        duration_seconds = parse_duration(duration)
    cur = conn.execute(
        "INSERT INTO time_entries (user_id, contact_id, matter_id,"
        " entry_date, description, duration_seconds, rate_cents_per_hour)"
        " VALUES (?,?,?,?,?,?,?)",
        (user_id, contact_id, matter_id, entry_date, description,
         duration_seconds or 0, rate_cents_per_hour))
    return cur.lastrowid


def start_timer(conn, user_id, now, description=None, contact_id=None,
                matter_id=None):
    """The dashboard timer widget (fx-0064): a running entry."""
    entry = create_entry(conn, user_id, now[:10], duration_seconds=0,
                         description=description, contact_id=contact_id,
                         matter_id=matter_id)
    conn.execute("UPDATE time_entries SET timer_started_at=? WHERE id=?",
                 (now, entry))
    return entry


def stop_timer(conn, entry_id, now):
    row = conn.execute("SELECT * FROM time_entries WHERE id=? AND"
                       " deleted_at IS NULL", (entry_id,)).fetchone()
    if row is None or row["timer_started_at"] is None:
        raise TimeError("no running timer on that entry")
    elapsed = int((_parse_ts(now)
                   - _parse_ts(row["timer_started_at"])).total_seconds())
    conn.execute("UPDATE time_entries SET duration_seconds="
                 " duration_seconds + ?, timer_started_at=NULL WHERE id=?",
                 (max(elapsed, 0), entry_id))


def resume_timer(conn, entry_id, now):
    """A stopped timer can be resumed (fx-0073)."""
    row = conn.execute("SELECT timer_started_at FROM time_entries WHERE"
                       " id=? AND deleted_at IS NULL",
                       (entry_id,)).fetchone()
    if row is None:
        raise TimeError(f"no such entry: {entry_id}")
    if row["timer_started_at"] is not None:
        raise TimeError("timer already running")
    conn.execute("UPDATE time_entries SET timer_started_at=? WHERE id=?",
                 (now, entry_id))


def update_entry(conn, entry_id, duration=None, description=None,
                 entry_date=None, rate_cents_per_hour=None):
    sets, vals = [], []
    if duration is not None:
        sets.append("duration_seconds=?")
        vals.append(parse_duration(duration))
    for col, v in (("description", description), ("entry_date", entry_date),
                   ("rate_cents_per_hour", rate_cents_per_hour)):
        if v is not None:
            sets.append(f"{col}=?")
            vals.append(v)
    if sets:
        conn.execute(f"UPDATE time_entries SET {', '.join(sets)}"
                     " WHERE id=? AND deleted_at IS NULL",
                     (*vals, entry_id))


def entries(conn, contact_id=None, matter_id=None, user_id=None,
            date_from=None, date_to=None, unbilled_only=False):
    """Contact overview, matter overview, or the firm-wide index, with
    filters (fx-0073). Billed = an invoice charge links the entry."""
    conds, vals = ["t.deleted_at IS NULL"], []
    if contact_id is not None:
        conds.append("t.contact_id=?")
        vals.append(contact_id)
    if matter_id is not None:
        conds.append("t.matter_id=?")
        vals.append(matter_id)
    if user_id is not None:
        conds.append("t.user_id=?")
        vals.append(user_id)
    if date_from is not None:
        conds.append("t.entry_date >= ?")
        vals.append(date_from)
    if date_to is not None:
        conds.append("t.entry_date <= ?")
        vals.append(date_to)
    if unbilled_only:
        conds.append("NOT EXISTS (SELECT 1 FROM invoice_charges c WHERE"
                     " c.time_entry_id = t.id AND c.deleted_at IS NULL)")
    return conn.execute(
        f"SELECT t.* FROM time_entries t WHERE {' AND '.join(conds)}"
        " ORDER BY t.entry_date, t.id", vals).fetchall()


def user_default_rate(conn, user_id):
    row = conn.execute(
        "SELECT value FROM user_settings WHERE user_id=? AND"
        " key='billing.hourly_rate_cents'", (user_id,)).fetchone()
    return int(row["value"]) if row else None


def set_user_default_rate(conn, user_id, rate_cents_per_hour):
    conn.execute(
        "INSERT INTO user_settings (user_id, key, value) VALUES"
        " (?,'billing.hourly_rate_cents',?) ON CONFLICT(user_id, key)"
        " DO UPDATE SET value=excluded.value",
        (user_id, str(rate_cents_per_hour)))


def charge_amount(conn, entry):
    """duration x rate, rounded half-up to the cent (decision default
    4). Integer math only."""
    rate = entry["rate_cents_per_hour"]
    if rate is None:
        rate = user_default_rate(conn, entry["user_id"])
    if rate is None:
        raise TimeError("no rate: set a per-entry override or the user's"
                        " default hourly rate")
    return (entry["duration_seconds"] * rate + 1800) // 3600
