"""Firm-wide email notification routing (firm-settings.
notification-settings, fx-0104).

One firm-wide setting decides who receives email notifications:
the firm's admin(s), the assignee of the particular matter, or all
staff members. Default is 'assignee' (matter assignee, falling back
to admins) -- the pre-P4 sender behavior, now centralized. The P3
expiry per-type recipient config is MORE specific and keeps
precedence where set (design note, P4 gate).
"""

SETTING_KEY = "notifications.recipients"
DEFAULT = "assignee"


def routing(conn):
    row = conn.execute("SELECT value FROM firm_settings WHERE key=?",
                       (SETTING_KEY,)).fetchone()
    return row["value"] if row is not None else DEFAULT


def set_routing(conn, rule):
    """Admin surface: route to 'admin', 'assignee', or 'all'."""
    if rule not in ("admin", "assignee", "all"):
        raise ValueError(f"unknown notification routing {rule}")
    conn.execute(
        "INSERT INTO firm_settings (key, value) VALUES (?,?)"
        " ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (SETTING_KEY, rule))


def _admins(conn):
    return [r["id"] for r in conn.execute(
        "SELECT id FROM users WHERE deleted_at IS NULL AND is_admin=1"
        " AND deactivated_at IS NULL ORDER BY id")]


def recipients(conn, matter_id=None, fallback_user_id=None):
    """Resolve the firm routing to user ids for one notification.
    'assignee' without a matter (or an unassigned matter) falls back
    to fallback_user_id, then admins."""
    rule = routing(conn)
    if rule == "all":
        return [r["id"] for r in conn.execute(
            "SELECT id FROM users WHERE deleted_at IS NULL"
            " AND deactivated_at IS NULL ORDER BY id")]
    if rule == "admin":
        return _admins(conn)
    if matter_id is not None:
        row = conn.execute("SELECT assignee_id FROM matters WHERE id=?",
                           (matter_id,)).fetchone()
        if row is not None and row["assignee_id"] is not None:
            return [row["assignee_id"]]
    if fallback_user_id is not None:
        return [fallback_user_id]
    return _admins(conn)
