"""Spine tests: contacts-and-matters matter-side entries (U1.4)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import matters  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
SOON = "2026-08-10T09:00:00Z"    # inside a 14-day Intake duration
LATE = "2026-09-01T09:00:00Z"    # past it
ADA, BRAM = 1, 2


def test_contacts_and_matters_matter_creation(conn):
    """matter-creation: contact + name required; optional description,
    type/status, preference category, priority date, assignee."""
    conn.actor.set("user", ADA)
    mid = matters.create_matter(
        conn, "Hana Synthetic I-129", 5, NOW, ADA,
        description="Synthetic petition", matter_type_id=1,
        matter_status_id=1, priority_date="2023-05-01",
        preference_category="EB-2", chargeability_country="Testlandia",
        assignee_id=BRAM, auto_assign_tasks=1)
    m = conn.execute("SELECT * FROM matters WHERE id=?", (mid,)).fetchone()
    assert m["primary_contact_id"] == 5 and m["assignee_id"] == BRAM
    assert m["preference_category"] == "EB-2"
    # born with a status -> the history starts at creation
    h = conn.execute("SELECT from_status_id, to_status_id FROM"
                     " matter_status_history WHERE matter_id=?",
                     (mid,)).fetchone()
    assert (h["from_status_id"], h["to_status_id"]) == (None, 1)


def test_contacts_and_matters_matter_types_statuses(conn):
    """matter-types-statuses: type + ordered statuses -> progress bar
    position and type/status/late filterability."""
    conn.actor.set("user", ADA)
    # seeded: matter 1 is I-130 (type 1) at Intake (status 1, 14 days)
    assert matters.progress(conn, 1, SOON) == (1, 4, False)
    assert matters.progress(conn, 1, LATE) == (1, 4, True)
    # advancing moves the bar and resets the duration clock
    matters.set_status(conn, 1, 2, SOON, changed_by=ADA)
    pos, total, late = matters.progress(conn, 1, SOON)
    assert (pos, total, late) == (2, 4, False)
    # filters: by type, by status, by lateness
    assert 1 in matters.list_matters(conn, SOON, matter_type_id=1)
    assert 1 in matters.list_matters(conn, SOON, matter_status_id=2)
    assert 1 not in matters.list_matters(conn, SOON, late=True)
    late_ids = matters.list_matters(conn, "2026-10-01T00:00:00Z", late=True)
    assert 1 in late_ids  # 30-day Preparing duration blown by October
    # the transition is on the history (who/when/from/to)
    h = conn.execute(
        "SELECT * FROM matter_status_history WHERE matter_id=1"
        " ORDER BY id DESC LIMIT 1").fetchone()
    assert (h["from_status_id"], h["to_status_id"], h["changed_by"]) \
        == (1, 2, ADA)


def test_contacts_and_matters_matter_status_automations(conn):
    """matter-status-automations (adapted): entering a status with
    automations adds the task list and emails the primary contact via
    the outbox, without manual action."""
    conn.actor.set("user", ADA)
    # build a task list and a status carrying both automations
    tl = conn.execute("INSERT INTO task_lists (name) VALUES"
                      " ('Intake checklist')").lastrowid
    for pos, (title, days) in enumerate(
            [("Collect passport", 3), ("Conflict check", None)], 1):
        conn.execute(
            "INSERT INTO task_list_items (task_list_id, title, position,"
            " duration_days, default_assignee_id) VALUES (?,?,?,?,?)",
            (tl, title, pos, days, 3))
    st = matters.add_status(conn, 1, "Automated Intake", 9,
                            duration_days=7, auto_task_list_id=tl,
                            auto_email_template="status_update")
    # matter 1: primary contact Dana, assignee Bram, auto_assign off
    matters.set_status(conn, 1, st, NOW, changed_by=ADA)
    tasks = conn.execute(
        "SELECT t.title, t.due_date, a.user_id FROM tasks t LEFT JOIN"
        " task_assignees a ON a.task_id = t.id WHERE t.matter_id=1"
        " ORDER BY t.id").fetchall()
    assert [t["title"] for t in tasks] == \
        ["Collect passport", "Conflict check"]
    assert tasks[0]["due_date"] == "2026-08-04"  # NOW + 3 days
    assert tasks[0]["user_id"] == 3  # item default assignee (Cleo)
    mail = conn.execute(
        "SELECT * FROM email_outbox WHERE template='status_update'"
        " AND entity_type='matters' AND entity_id=1").fetchone()
    assert mail is not None
    assert mail["recipient"] == "dana@example.test"
    assert "Automated Intake" in mail["body"]
    assert mail["sent_at"] is None  # outbox, never a socket


def test_contacts_and_matters_matter_linked_contacts(conn):
    """matter-linked-contacts: an additional contact appears in the
    matter's Related Contacts with its relationship title."""
    conn.actor.set("user", ADA)
    matters.link_contact(conn, 1, 7, relationship="Employer")
    matters.link_contact(conn, 1, 2, relationship="Beneficiary spouse")
    linked = matters.linked_contacts(conn, 1)
    assert (7, "Synthetic Staffing LLC", "Employer") in linked
    assert (2, "Emil Synthetic", "Beneficiary spouse") in linked


def test_contacts_and_matters_matter_archiving(conn):
    """matter-archiving: bulk archive -> matters leave the active view
    and appear under the Archived view; un-archive reverses."""
    conn.actor.set("user", ADA)
    matters.archive_matters(conn, [3, 4], NOW)
    active = matters.list_matters(conn, NOW, view="active")
    archived = matters.list_matters(conn, NOW, view="archived")
    assert 3 not in active and 4 not in active
    assert archived == [3, 4]
    matters.unarchive_matters(conn, [3])
    assert 3 in matters.list_matters(conn, NOW, view="active")
    assert matters.list_matters(conn, NOW, view="archived") == [4]
