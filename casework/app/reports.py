"""Reports (U3.2): VMAX tracking.

The VMAX date (last date a client can remain in status absent
further extensions) lives in the fact store as imm.vmax_date; the
report orders clients by time remaining (fx-0162, fx-0168).
principal_applicant is the contact itself in v1 -- dependent
chains are post-v1 content work (report columns are the corpus's:
contact, email, principal applicant, time remaining, VMAX date).
"""

from datetime import datetime, timezone


def _day(ts):
    return datetime.strptime(ts[:10], "%Y-%m-%d").replace(
        tzinfo=timezone.utc)


def vmax_report(conn, today, start=None, end=None):
    rows = conn.execute(
        "SELECT c.id, c.display_name, f.value AS vmax_date,"
        " fe.value AS email"
        " FROM facts f JOIN contacts c ON c.id = f.subject_id"
        " LEFT JOIN facts fe ON fe.subject_type='contact'"
        "  AND fe.subject_id=c.id AND fe.key='contact.email' AND fe.idx=0"
        " WHERE f.subject_type='contact' AND f.key='imm.vmax_date'"
        "  AND f.idx=0 AND c.deleted_at IS NULL").fetchall()
    out = []
    for r in rows:
        if start is not None and r["vmax_date"] < start:
            continue
        if end is not None and r["vmax_date"] > end:
            continue
        remaining = (_day(r["vmax_date"]) - _day(today)).days
        out.append({"contact": r["display_name"], "email": r["email"],
                    "principal_applicant": r["display_name"],
                    "vmax_time_remaining_days": remaining,
                    "vmax_date": r["vmax_date"]})
    out.sort(key=lambda x: (x["vmax_time_remaining_days"], x["contact"]))
    return out
