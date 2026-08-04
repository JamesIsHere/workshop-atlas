"""User management, permissions, groups, privacy (U1.2).

Levels are hierarchical: none < view < create < edit < delete. A
missing per-type row means full access (small-firm default). The
'delete' verb additionally requires the global can_delete flag;
export/archive/reassign are global-flag verbs with no per-type level.
Admins short-circuit every check. Callers own actor attribution.
"""

LEVELS = {"none": 0, "view": 1, "create": 2, "edit": 3, "delete": 4}
GLOBAL_VERBS = ("export", "archive", "reassign")


# --- user administration (Settings > User Access) ---

def create_user(conn, email, name, now, role_label=None):
    cur = conn.execute(
        "INSERT INTO users (email, name, password_hash, role_label,"
        " created_at) VALUES (?,?,?,?,?)",
        (email, name, "UNSET", role_label, now))
    return cur.lastrowid


def update_user(conn, user_id, **fields):
    allowed = {"email", "name", "role_label", "timezone",
               "is_admin", "is_owner"}
    bad = set(fields) - allowed
    if bad:
        raise ValueError(f"not editable here: {sorted(bad)}")
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE users SET {sets} WHERE id=?",
                 (*fields.values(), user_id))


def deactivate_user(conn, user_id, now):
    conn.execute("UPDATE users SET deactivated_at=? WHERE id=?",
                 (now, user_id))


def reactivate_user(conn, user_id):
    conn.execute("UPDATE users SET deactivated_at=NULL WHERE id=?",
                 (user_id,))


def delete_user(conn, user_id, deleted_by, now):
    """Tombstone (trash-restorable). Hard removal is the purge layer's
    job, which does not exist in v1."""
    conn.execute("UPDATE users SET deleted_at=?, deleted_by=? WHERE id=?",
                 (now, deleted_by, user_id))


# --- permissions ---

def set_permission(conn, user_id, record_type, level):
    if level not in LEVELS:
        raise ValueError(f"unknown level: {level}")
    conn.execute(
        "INSERT INTO user_permissions (user_id, record_type, level)"
        " VALUES (?,?,?) ON CONFLICT (user_id, record_type)"
        " DO UPDATE SET level=excluded.level",
        (user_id, record_type, level))


def set_global_permissions(conn, user_id, **flags):
    allowed = {"can_delete", "can_export", "can_archive", "can_reassign",
               "firm_settings_access"}
    bad = set(flags) - allowed
    if bad:
        raise ValueError(f"unknown global flags: {sorted(bad)}")
    row = conn.execute("SELECT user_id FROM user_global_permissions"
                       " WHERE user_id=?", (user_id,)).fetchone()
    if row is None:
        conn.execute("INSERT INTO user_global_permissions (user_id)"
                     " VALUES (?)", (user_id,))
    sets = ", ".join(f"{k}=?" for k in flags)
    conn.execute(f"UPDATE user_global_permissions SET {sets}"
                 " WHERE user_id=?", (*flags.values(), user_id))


def _is_admin(conn, user_id):
    row = conn.execute("SELECT is_admin, is_owner FROM users WHERE id=?",
                       (user_id,)).fetchone()
    return bool(row and (row["is_admin"] or row["is_owner"]))


def _global_flag(conn, user_id, flag):
    row = conn.execute(
        f"SELECT {flag} FROM user_global_permissions WHERE user_id=?",
        (user_id,)).fetchone()
    # absent row = allowed: same small-firm default as per-type levels
    return True if row is None else bool(row[flag])


def can(conn, user_id, record_type, verb):
    """Verb in view|create|edit|delete or a global verb."""
    if _is_admin(conn, user_id):
        return True
    if verb in GLOBAL_VERBS:
        return _global_flag(conn, user_id, f"can_{verb}")
    if verb not in LEVELS or verb == "none":
        raise ValueError(f"unknown verb: {verb}")
    row = conn.execute(
        "SELECT level FROM user_permissions WHERE user_id=? AND"
        " record_type=?", (user_id, record_type)).fetchone()
    level = LEVELS[row["level"]] if row else LEVELS["delete"]
    if level < LEVELS[verb]:
        return False
    if verb == "delete":
        return _global_flag(conn, user_id, "can_delete")
    return True


# --- groups and record privacy ---

def create_group(conn, name, accounting_notes_permission=0):
    cur = conn.execute(
        "INSERT INTO user_groups (name, accounting_notes_permission)"
        " VALUES (?,?)", (name, accounting_notes_permission))
    return cur.lastrowid


def add_group_member(conn, group_id, user_id):
    conn.execute("INSERT INTO user_group_members (group_id, user_id)"
                 " VALUES (?,?)", (group_id, user_id))


def set_privacy(conn, entity_type, entity_id, group_id):
    """Mark a contact/matter Private to a designated group (additive:
    several groups may be designated)."""
    conn.execute(
        "INSERT INTO record_privacy (entity_type, entity_id, group_id)"
        " VALUES (?,?,?)", (entity_type, entity_id, group_id))


def clear_privacy(conn, entity_type, entity_id):
    conn.execute("DELETE FROM record_privacy WHERE entity_type=? AND"
                 " entity_id=?", (entity_type, entity_id))


def _in_designated_group(conn, user_id, entity_type, entity_id):
    rows = conn.execute(
        "SELECT group_id FROM record_privacy WHERE entity_type=? AND"
        " entity_id=?", (entity_type, entity_id)).fetchall()
    if not rows:
        return None  # public: no designation at all
    member = conn.execute(
        "SELECT 1 FROM user_group_members m JOIN record_privacy p"
        " ON p.group_id = m.group_id WHERE m.user_id=? AND"
        " p.entity_type=? AND p.entity_id=? LIMIT 1",
        (user_id, entity_type, entity_id)).fetchone()
    return member is not None


def matter_assignee_label(conn, matter_id):
    """Assignee display string for a matter: 'Name (Role)' -- the
    user-roles criterion's surface (role shown next to the name)."""
    row = conn.execute(
        "SELECT u.name, u.role_label FROM matters m JOIN users u"
        " ON u.id = m.assignee_id WHERE m.id=?", (matter_id,)).fetchone()
    if row is None:
        return None
    return f"{row['name']} ({row['role_label']})" if row["role_label"] \
        else row["name"]


def visible(conn, user_id, entity_type, entity_id):
    """Privacy check for contacts and matters. A contact's privacy
    cascades to its matters and takes precedence (fx-0095)."""
    if _is_admin(conn, user_id):
        return True
    if entity_type == "matter":
        contact = conn.execute(
            "SELECT primary_contact_id FROM matters WHERE id=?",
            (entity_id,)).fetchone()
        if contact is not None:
            via_contact = _in_designated_group(
                conn, user_id, "contact", contact["primary_contact_id"])
            if via_contact is not None:
                return via_contact
    own = _in_designated_group(conn, user_id, entity_type, entity_id)
    return True if own is None else own
