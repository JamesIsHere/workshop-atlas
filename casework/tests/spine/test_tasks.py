"""Spine tests: case-tracking task entries (U3.3)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import tasks  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM, CLEO = 1, 2, 3
DANA = 1  # contact; matter 1 primary


def test_case_tracking_tasks(conn):
    """tasks: typed on the index or a contact/matter tab -> created
    with the creator as default assignee and the contact/matter
    attached where applicable; assignable to any staff member."""
    conn.actor.set("user", BRAM)
    # Tasks index: no attachment
    t1 = tasks.create_task(conn, "Order certified translations", NOW, BRAM)
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (t1,)).fetchone()
    assert (row["contact_id"], row["matter_id"]) == (None, None)
    assert tasks.assignees(conn, t1) == [BRAM]  # creator by default
    # matter tab: auto-attached to matter AND its primary contact
    t2 = tasks.create_task(conn, "Draft cover letter", NOW, BRAM,
                           matter_id=1)
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (t2,)).fetchone()
    assert (row["contact_id"], row["matter_id"]) == (DANA, 1)
    # reassignable to any staff member
    tasks.assign_task(conn, t2, [CLEO])
    assert tasks.assignees(conn, t2) == [CLEO]
    # tab listings
    assert t2 in [t["id"] for t in tasks.list_tasks(conn, matter_id=1)]
    assert t1 in [t["id"] for t in tasks.list_tasks(conn)]
    # completion clears it from the open view
    tasks.complete_task(conn, t1, NOW)
    assert t1 not in [t["id"] for t in tasks.list_tasks(conn)]
    assert t1 in [t["id"] for t in
                  tasks.list_tasks(conn, include_completed=True)]


def test_case_tracking_task_lists(conn):
    """task-lists: Import Task List -> the list's tasks are created
    with default durations and assignees applied."""
    conn.actor.set("user", ADA)
    tl = tasks.create_task_list(conn, "H-1B filing checklist")
    tasks.add_list_item(conn, tl, "Collect passport bio page", 1,
                        duration_days=3, default_assignee_id=CLEO)
    tasks.add_list_item(conn, tl, "Draft LCA", 2, duration_days=7,
                        default_assignee_id=BRAM)
    tasks.add_list_item(conn, tl, "File petition", 3)
    created = tasks.import_task_list(conn, tl, NOW, ADA, matter_id=1)
    rows = [conn.execute("SELECT * FROM tasks WHERE id=?", (t,)).fetchone()
            for t in created]
    assert [r["title"] for r in rows] == \
        ["Collect passport bio page", "Draft LCA", "File petition"]
    # default durations: due = import day + duration_days
    assert [r["due_date"] for r in rows] == \
        ["2026-08-04", "2026-08-08", None]
    # default assignees applied; no default -> importer holds it
    assert [tasks.assignees(conn, t) for t in created] == \
        [[CLEO], [BRAM], [ADA]]
    # imported onto the matter -> attached to it and its primary contact
    assert all((r["matter_id"], r["contact_id"]) == (1, DANA)
               for r in rows)


def test_case_tracking_task_reference_date_due_dates(conn):
    """task-reference-date-due-dates: a list task set to From
    Reference Date (date, direction, day count) -> imported copies
    carry a due date computed from the contact's reference date."""
    conn.actor.set("user", ADA)
    tl = tasks.create_task_list(conn, "Status expiry drill")
    # Dana's imm.status_expiry is seeded 2027-06-30
    tasks.add_list_item(conn, tl, "File extension", 1,
                        ref_fact_key="imm.status_expiry",
                        ref_direction="before", ref_days=90)
    tasks.add_list_item(conn, tl, "Post-expiry audit", 2,
                        ref_fact_key="imm.status_expiry",
                        ref_direction="after", ref_days=10)
    created = tasks.import_task_list(conn, tl, NOW, ADA, contact_id=DANA)
    due = [conn.execute("SELECT due_date FROM tasks WHERE id=?",
                        (t,)).fetchone()["due_date"] for t in created]
    assert due == ["2027-04-01", "2027-07-10"]
    # reference dates are contact-level date/expiry facts only
    try:
        tasks.add_list_item(conn, tl, "Bad rule", 3,
                            ref_fact_key="bio.given_name",
                            ref_direction="before", ref_days=5)
        assert False, "non-date reference fact must be refused"
    except ValueError:
        pass
    # contact without the fact: task lands with no due date, no crash
    created2 = tasks.import_task_list(conn, tl, NOW, ADA, contact_id=6)
    due2 = conn.execute("SELECT due_date FROM tasks WHERE id=?",
                        (created2[0],)).fetchone()["due_date"]
    assert due2 is None
