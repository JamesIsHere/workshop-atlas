"""Visa Bulletin replay adapter + priority-date tracking (U3.4).

Replays the captured dataset (data/visa_bulletin/raw/, immutable,
see its README) into the visa_bulletin table one month at a time --
the load IS the monthly bulletin publication, so change detection
and the monthly digest ride it (not the tick). Cells stay verbatim
('C', 'U', DDMONYY); status is computed on read, never stored.
Live monthly fetch is post-v1 (external service, Approval required).
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "visa_bulletin" / "raw"

# verbatim bulletin row labels -> category codes (matters carry codes)
_CATEGORY_PREFIXES = [
    ("5th Unreserved", "EB-5"),
    ("5th Set Aside: Rural", "EB-5R"),
    ("5th Set Aside: (Rural", "EB-5R"),
    ("5th Set Aside: High Unemployment", "EB-5H"),
    ("5th Set Aside: (High Unemployment", "EB-5H"),
    ("5th Set Aside: Infrastructure", "EB-5I"),
    ("5th Set Aside: (Infrastructure", "EB-5I"),
    ("Certain Religious Workers", "EB-4R"),
    ("Other Workers", "EB-OW"),
    ("1st", "EB-1"), ("2nd", "EB-2"), ("3rd", "EB-3"), ("4th", "EB-4"),
    ("F1", "F1"), ("F2A", "F2A"), ("F2B", "F2B"), ("F3", "F3"),
    ("F4", "F4"),
]

# column position -> chargeability (headers vary in whitespace only)
_COUNTRIES = ["ALL", "China", "India", "Mexico", "Philippines"]

_CHARTS = {"family_final_action": "final_action",
           "family_filing": "filing",
           "employment_final_action": "final_action",
           "employment_filing": "filing"}

_MONTHS = {m: i + 1 for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
     "SEP", "OCT", "NOV", "DEC"])}


def _category(label):
    for prefix, code in _CATEGORY_PREFIXES:
        if label.startswith(prefix):
            return code
    raise ValueError(f"unrecognized bulletin category row: {label}")


def cutoff_to_iso(cell):
    """'01FEB18' -> '2018-02-01'; C/U have no date."""
    if cell in ("C", "U"):
        return None
    day, mon, yy = cell[:2], cell[2:5], int(cell[5:7])
    year = 1900 + yy if yy >= 90 else 2000 + yy
    return f"{year:04d}-{_MONTHS[mon]:02d}-{int(day):02d}"


def load_month(conn, month, now):
    """Insert one captured month (in order), then diff tracked
    matters against the previous month: in-app notifications +
    the monthly digest email for every status change."""
    prev = conn.execute(
        "SELECT max(bulletin_month) AS m FROM visa_bulletin").fetchone()["m"]
    if prev is not None and month <= prev:
        raise ValueError(f"bulletin months load in order: {month} <= {prev}")
    before = _tracked_statuses(conn) if prev is not None else {}
    payload = json.loads(
        (DATA_DIR / f"visa-bulletin-{month}.json").read_text(
            encoding="utf-8"))
    if payload["bulletin_month"] != month:
        raise ValueError("capture file month mismatch")
    for chart_key, chart in _CHARTS.items():
        rows = payload["charts"][chart_key]
        if len(rows[0]) != len(_COUNTRIES) + 1:
            raise ValueError(f"unexpected column count in {chart_key}")
        for row in rows[1:]:
            for i, country in enumerate(_COUNTRIES, start=1):
                conn.execute(
                    "INSERT INTO visa_bulletin (bulletin_month, chart,"
                    " preference_category, chargeability, cutoff_date)"
                    " VALUES (?,?,?,?,?)",
                    (month, chart, _category(row[0]), country, row[i]))
    changes = []
    if before:
        after = _tracked_statuses(conn)
        for (matter_id, chart), old in sorted(before.items()):
            new = after.get((matter_id, chart))
            if new is not None and new != old:
                changes.append({"matter_id": matter_id, "chart": chart,
                                "old": old, "new": new,
                                "bulletin_month": month})
        _notify(conn, changes, month, now)
    return changes


def _tracked_statuses(conn):
    out = {}
    for m in conn.execute(
            "SELECT id FROM matters WHERE deleted_at IS NULL"
            " AND priority_date IS NOT NULL"
            " AND preference_category IS NOT NULL ORDER BY id"):
        s = matter_status(conn, m["id"])
        if s is None:
            continue
        for chart in ("filing", "final_action"):
            out[(m["id"], chart)] = s[chart]["status"]
    return out


def _cell(conn, month, chart, category, country):
    row = conn.execute(
        "SELECT cutoff_date FROM visa_bulletin WHERE bulletin_month=?"
        " AND chart=? AND preference_category=? AND chargeability=?",
        (month, chart, category, country)).fetchone()
    return None if row is None else row["cutoff_date"]


def _chargeability(country):
    if country is None:
        return "ALL"
    for c in _COUNTRIES[1:]:
        if c.lower() == country.strip().lower():
            return c
    return "ALL"


def matter_status(conn, matter_id, month=None):
    """{'filing': {...}, 'final_action': {...}} against the given
    (default: latest loaded) bulletin month; None when unloadable."""
    if month is None:
        month = conn.execute("SELECT max(bulletin_month) AS m FROM"
                             " visa_bulletin").fetchone()["m"]
        if month is None:
            return None
    m = conn.execute("SELECT * FROM matters WHERE id=?",
                     (matter_id,)).fetchone()
    if m is None or m["priority_date"] is None \
            or m["preference_category"] is None:
        return None
    country = _chargeability(m["chargeability_country"])
    out = {"bulletin_month": month}
    for chart in ("filing", "final_action"):
        cell = _cell(conn, month, chart, m["preference_category"], country)
        if cell is None:
            out[chart] = {"status": "unknown_category", "cutoff": None}
        elif cell == "C":
            out[chart] = {"status": "current", "cutoff": "C"}
        elif cell == "U":
            out[chart] = {"status": "unavailable", "cutoff": "U"}
        else:
            cur = m["priority_date"] < cutoff_to_iso(cell)
            out[chart] = {"status": "current" if cur else "not_current",
                          "cutoff": cell}
    return out


def _notify(conn, changes, month, now):
    if not changes:
        return
    admins = [r["id"] for r in conn.execute(
        "SELECT id FROM users WHERE deleted_at IS NULL AND is_admin=1"
        " ORDER BY id")]
    lines = []
    for c in changes:
        m = conn.execute("SELECT name, assignee_id FROM matters WHERE"
                         " id=?", (c["matter_id"],)).fetchone()
        targets = [m["assignee_id"]] if m["assignee_id"] is not None \
            else admins
        for uid in targets:
            conn.execute(
                "INSERT INTO notifications (user_id, kind, payload,"
                " created_at) VALUES (?,?,?,?)",
                (uid, "priority_date_status", json.dumps(c), now))
        lines.append(f"Matter {m['name']}: {c['chart']}"
                     f" {c['old']} -> {c['new']}")
    body = (f"Visa Bulletin {month} priority date changes:\n"
            + "\n".join(lines))
    for uid in admins:
        email = conn.execute("SELECT email FROM users WHERE id=?",
                             (uid,)).fetchone()["email"]
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, f"Visa Bulletin digest -- {month}", body,
             "visa_bulletin_digest", None, None, now))
