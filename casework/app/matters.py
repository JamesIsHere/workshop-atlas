"""Matters (U1.4): creation, workflows, status automations, linked
contacts, archiving. set_status is the one transition path -- it
writes history and fires automations; nothing else moves a matter.
"""

from datetime import datetime, timedelta, timezone

from app import facts, tasks


def _parse(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


# --- workflow admin (Settings > Matter Workflows) ---

def create_matter_type(conn, name):
    return conn.execute("INSERT INTO matter_types (name) VALUES (?)",
                        (name,)).lastrowid


def add_status(conn, matter_type_id, name, position, duration_days=None,
               auto_task_list_id=None, auto_email_template=None):
    return conn.execute(
        "INSERT INTO matter_statuses (matter_type_id, name, position,"
        " duration_days, auto_task_list_id, auto_email_template)"
        " VALUES (?,?,?,?,?,?)",
        (matter_type_id, name, position, duration_days,
         auto_task_list_id, auto_email_template)).lastrowid


# --- matters ---

def create_matter(conn, name, primary_contact_id, now, created_by,
                  description=None, matter_type_id=None,
                  matter_status_id=None, priority_date=None,
                  preference_category=None, chargeability_country=None,
                  assignee_id=None, auto_assign_tasks=0):
    cur = conn.execute(
        "INSERT INTO matters (name, description, primary_contact_id,"
        " matter_type_id, matter_status_id, status_entered_at,"
        " priority_date, preference_category, chargeability_country,"
        " assignee_id, auto_assign_tasks, created_at, created_by)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (name, description, primary_contact_id, matter_type_id,
         matter_status_id, now if matter_status_id else None,
         priority_date, preference_category, chargeability_country,
         assignee_id, auto_assign_tasks, now, created_by))
    mid = cur.lastrowid
    if matter_status_id is not None:
        conn.execute(
            "INSERT INTO matter_status_history (matter_id, from_status_id,"
            " to_status_id, changed_at, changed_by) VALUES (?,?,?,?,?)",
            (mid, None, matter_status_id, now, created_by))
        _fire_automations(conn, mid, matter_status_id, now)
    return mid


def set_status(conn, matter_id, status_id, now, changed_by):
    """The one status-transition path: history + automations."""
    old = conn.execute("SELECT matter_status_id FROM matters WHERE id=?",
                       (matter_id,)).fetchone()["matter_status_id"]
    conn.execute("UPDATE matters SET matter_status_id=?,"
                 " status_entered_at=? WHERE id=?",
                 (status_id, now, matter_id))
    conn.execute(
        "INSERT INTO matter_status_history (matter_id, from_status_id,"
        " to_status_id, changed_at, changed_by) VALUES (?,?,?,?,?)",
        (matter_id, old, status_id, now, changed_by))
    _fire_automations(conn, matter_id, status_id, now)


def _fire_automations(conn, matter_id, status_id, now):
    status = conn.execute("SELECT * FROM matter_statuses WHERE id=?",
                          (status_id,)).fetchone()
    matter = conn.execute("SELECT * FROM matters WHERE id=?",
                          (matter_id,)).fetchone()
    if status["auto_task_list_id"] is not None:
        # one task-creation engine (U3.3): the automation is an import
        # with the matter assignee as override when auto_assign is on
        tasks.import_task_list(
            conn, status["auto_task_list_id"], now, None,
            matter_id=matter_id,
            assignee_override=matter["assignee_id"]
            if matter["auto_assign_tasks"] else None)
    if status["auto_email_template"] is not None:
        email = facts.get_fact(conn, "contact",
                               matter["primary_contact_id"], "contact.email")
        if email is not None:
            contact = conn.execute(
                "SELECT display_name FROM contacts WHERE id=?",
                (matter["primary_contact_id"],)).fetchone()
            conn.execute(
                "INSERT INTO email_outbox (recipient, subject, body,"
                " template, entity_type, entity_id, created_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (email, f"Update on {matter['name']}",
                 f"Dear {contact['display_name']}, your matter"
                 f" {matter['name']} has entered status {status['name']}.",
                 status["auto_email_template"], "matters", matter_id, now))


# --- workflow display / filtering ---

def progress(conn, matter_id, today):
    """(position, total, late) for the matter's workflow bar."""
    m = conn.execute("SELECT * FROM matters WHERE id=?",
                     (matter_id,)).fetchone()
    if m["matter_status_id"] is None:
        return None
    statuses = conn.execute(
        "SELECT id, position, duration_days FROM matter_statuses WHERE"
        " matter_type_id=? AND deleted_at IS NULL ORDER BY position",
        (m["matter_type_id"],)).fetchall()
    current = next(s for s in statuses if s["id"] == m["matter_status_id"])
    late = False
    if current["duration_days"] is not None and m["status_entered_at"]:
        deadline = _parse(m["status_entered_at"]) + \
            timedelta(days=current["duration_days"])
        late = _parse(today) > deadline
    return (current["position"], len(statuses), late)


def list_matters(conn, today, view="active", matter_type_id=None,
                 matter_status_id=None, late=None):
    cond = "archived_at IS NULL" if view == "active" \
        else "archived_at IS NOT NULL"
    q = (f"SELECT id FROM matters WHERE deleted_at IS NULL AND {cond}")
    params = []
    if matter_type_id is not None:
        q += " AND matter_type_id=?"
        params.append(matter_type_id)
    if matter_status_id is not None:
        q += " AND matter_status_id=?"
        params.append(matter_status_id)
    ids = [r["id"] for r in conn.execute(q + " ORDER BY id", params)]
    if late is not None:
        ids = [i for i in ids
               if (p := progress(conn, i, today)) and p[2] == late]
    return ids


# --- linked contacts ---

def link_contact(conn, matter_id, contact_id, relationship=None):
    conn.execute(
        "INSERT INTO matter_contacts (matter_id, contact_id, relationship)"
        " VALUES (?,?,?)", (matter_id, contact_id, relationship))


def linked_contacts(conn, matter_id):
    rows = conn.execute(
        "SELECT mc.contact_id, c.display_name, mc.relationship"
        " FROM matter_contacts mc JOIN contacts c ON c.id = mc.contact_id"
        " WHERE mc.matter_id=? ORDER BY mc.id", (matter_id,)).fetchall()
    return [(r["contact_id"], r["display_name"], r["relationship"])
            for r in rows]


# --- archiving ---

def archive_matters(conn, matter_ids, now):
    for mid in matter_ids:
        conn.execute("UPDATE matters SET archived_at=? WHERE id=?",
                     (now, mid))


def unarchive_matters(conn, matter_ids):
    for mid in matter_ids:
        conn.execute("UPDATE matters SET archived_at=NULL WHERE id=?",
                     (mid,))
