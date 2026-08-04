"""Tasks (U3.3): work items, reusable lists, reference-date due dates.

create_task carries the type-and-Enter contract: creator is the
default assignee, a matter attaches its primary contact too
(fx-0213). import_task_list is the Import Task List button AND the
engine behind matter-status automations (matters._fire_automations
delegates here) -- one implementation for both entry paths.
"""

from datetime import datetime, timedelta, timezone

from app import facts


def _parse(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)


def _day(date_str):
    return datetime.strptime(date_str[:10], "%Y-%m-%d").replace(
        tzinfo=timezone.utc)


# --- tasks ---

def create_task(conn, title, now, created_by, contact_id=None,
                matter_id=None, due_date=None, assignee_id=None):
    if matter_id is not None and contact_id is None:
        m = conn.execute("SELECT primary_contact_id FROM matters WHERE"
                         " id=?", (matter_id,)).fetchone()
        contact_id = m["primary_contact_id"] if m else None
    tid = conn.execute(
        "INSERT INTO tasks (title, contact_id, matter_id, due_date,"
        " created_at, created_by) VALUES (?,?,?,?,?,?)",
        (title, contact_id, matter_id, due_date, now,
         created_by)).lastrowid
    holder = assignee_id if assignee_id is not None else created_by
    if holder is not None:
        conn.execute("INSERT INTO task_assignees (task_id, user_id)"
                     " VALUES (?,?)", (tid, holder))
    return tid


def assign_task(conn, task_id, user_ids):
    """Replace the assignee set; any staff member is assignable."""
    conn.execute("DELETE FROM task_assignees WHERE task_id=?", (task_id,))
    for uid in user_ids:
        conn.execute("INSERT INTO task_assignees (task_id, user_id)"
                     " VALUES (?,?)", (task_id, uid))


def assignees(conn, task_id):
    return [r["user_id"] for r in conn.execute(
        "SELECT user_id FROM task_assignees WHERE task_id=?"
        " ORDER BY user_id", (task_id,))]


def complete_task(conn, task_id, now):
    conn.execute("UPDATE tasks SET completed_at=? WHERE id=?",
                 (now, task_id))


def list_tasks(conn, contact_id=None, matter_id=None,
               include_completed=False):
    q = "SELECT * FROM tasks WHERE deleted_at IS NULL"
    params = []
    if not include_completed:
        q += " AND completed_at IS NULL"
    if contact_id is not None:
        q += " AND contact_id=?"
        params.append(contact_id)
    if matter_id is not None:
        q += " AND matter_id=?"
        params.append(matter_id)
    return conn.execute(q + " ORDER BY id", params).fetchall()


# --- task lists (Settings > Task Lists) ---

def create_task_list(conn, name):
    return conn.execute("INSERT INTO task_lists (name) VALUES (?)",
                        (name,)).lastrowid


def add_list_item(conn, task_list_id, title, position, duration_days=None,
                  default_assignee_id=None, ref_fact_key=None,
                  ref_direction=None, ref_days=None):
    if ref_fact_key is not None:
        d = facts.definition(conn, ref_fact_key)
        if d is None or d["subject_type"] != "contact" \
                or d["value_type"] not in ("date", "expiry"):
            raise ValueError(f"{ref_fact_key} is not a contact-level"
                             " date reference")
        if ref_direction not in ("before", "after") or ref_days is None:
            raise ValueError("reference rule needs direction + day count")
    return conn.execute(
        "INSERT INTO task_list_items (task_list_id, title, position,"
        " duration_days, ref_fact_key, ref_direction, ref_days,"
        " default_assignee_id) VALUES (?,?,?,?,?,?,?,?)",
        (task_list_id, title, position, duration_days, ref_fact_key,
         ref_direction, ref_days, default_assignee_id)).lastrowid


def _item_due(conn, item, now, contact_id):
    if item["ref_fact_key"] is not None and contact_id is not None:
        ref = facts.get_fact(conn, "contact", contact_id,
                             item["ref_fact_key"])
        if ref is None:
            return None  # missing reference date -> no due date, no crash
        sign = -1 if item["ref_direction"] == "before" else 1
        return (_day(ref) + sign * timedelta(days=item["ref_days"])
                ).strftime("%Y-%m-%d")
    if item["duration_days"] is not None:
        return (_parse(now) + timedelta(days=item["duration_days"])
                ).strftime("%Y-%m-%d")
    return None


def import_task_list(conn, task_list_id, now, imported_by,
                     contact_id=None, matter_id=None,
                     assignee_override=None):
    """The list's tasks, created in position order. Assignee per
    task: the override (automation's matter assignee), else the
    item default, else the importer."""
    if matter_id is not None and contact_id is None:
        m = conn.execute("SELECT primary_contact_id FROM matters WHERE"
                         " id=?", (matter_id,)).fetchone()
        contact_id = m["primary_contact_id"] if m else None
    items = conn.execute(
        "SELECT * FROM task_list_items WHERE task_list_id=?"
        " ORDER BY position", (task_list_id,)).fetchall()
    created = []
    for item in items:
        holder = assignee_override if assignee_override is not None \
            else (item["default_assignee_id"]
                  if item["default_assignee_id"] is not None
                  else imported_by)
        created.append(create_task(
            conn, item["title"], now, imported_by, contact_id=contact_id,
            matter_id=matter_id, due_date=_item_due(conn, item, now,
                                                    contact_id),
            assignee_id=holder))
    return created
