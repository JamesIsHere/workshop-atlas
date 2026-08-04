"""Spine tests: firm-settings user administration / permissions /
groups, time zone, personal-settings.user-roles (U1.2)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import auth, users  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
PW = "synthetic-password"
ADA, BRAM, CLEO = 1, 2, 3  # seeded staff ids (seeds/gen_seed.py)
BRAM_EMAIL = "bram.attorney@example.test"


def test_firm_settings_managing_users(conn):
    """managing-users: deactivation blocks login while the user's data
    and logs remain; reactivation restores login; add/edit/delete."""
    conn.actor.set("user", ADA)
    # deactivate Bram -> login refused
    users.deactivate_user(conn, BRAM, NOW)
    assert auth.login(conn, BRAM_EMAIL, PW, NOW)[0] == "deactivated"
    # ... while his record and audit logs remain accessible
    row = conn.execute("SELECT * FROM users WHERE id=?", (BRAM,)).fetchone()
    assert row["deleted_at"] is None and row["name"] == "Bram Synthetic"
    logs = conn.execute(
        "SELECT count(*) FROM audit_log WHERE entity_type='users' AND"
        " entity_id=?", (BRAM,)).fetchone()[0]
    assert logs >= 2  # seed insert + the deactivation update
    # reactivate -> login proceeds again (to the 2FA stage)
    users.reactivate_user(conn, BRAM)
    assert auth.login(conn, BRAM_EMAIL, PW, NOW)[0] in (
        "enrollment_required", "twofa_required")
    # add a member (email + name), edit their name and email
    uid = users.create_user(conn, "nu.new@example.test", "Nu Synthetic", NOW)
    users.update_user(conn, uid, email="nu@example.test", name="Nu S.")
    row = conn.execute("SELECT email, name FROM users WHERE id=?",
                       (uid,)).fetchone()
    assert (row["email"], row["name"]) == ("nu@example.test", "Nu S.")
    # delete = tombstone; the login path no longer sees the user
    users.delete_user(conn, uid, deleted_by=ADA, now=NOW)
    row = conn.execute("SELECT deleted_at FROM users WHERE id=?",
                       (uid,)).fetchone()
    assert row["deleted_at"] == NOW


def test_firm_settings_user_permissions(conn):
    """user-permissions: per-record-type levels plus global flags
    govern each verb; admins bypass."""
    conn.actor.set("user", ADA)
    # level 'view' on contacts: view yes, create no
    users.set_permission(conn, CLEO, "contacts", "view")
    assert users.can(conn, CLEO, "contacts", "view")
    assert not users.can(conn, CLEO, "contacts", "create")
    # raise to 'edit': edit yes, delete still no (level short)
    users.set_permission(conn, CLEO, "contacts", "edit")
    assert users.can(conn, CLEO, "contacts", "edit")
    assert not users.can(conn, CLEO, "contacts", "delete")
    # level 'delete' + global can_delete on -> delete allowed
    users.set_permission(conn, CLEO, "contacts", "delete")
    users.set_global_permissions(conn, CLEO, can_delete=1)
    assert users.can(conn, CLEO, "contacts", "delete")
    # global can_delete off blocks delete despite the per-type level
    users.set_global_permissions(conn, CLEO, can_delete=0)
    assert not users.can(conn, CLEO, "contacts", "delete")
    # global verb: export governed by can_export
    users.set_global_permissions(conn, CLEO, can_export=0)
    assert not users.can(conn, CLEO, "contacts", "export")
    # untouched record type keeps the full-access default
    assert users.can(conn, CLEO, "notes", "edit")
    # 'none' blocks even viewing
    users.set_permission(conn, CLEO, "matters", "none")
    assert not users.can(conn, CLEO, "matters", "view")
    # admin bypasses everything
    users.set_permission(conn, ADA, "contacts", "none")
    assert users.can(conn, ADA, "contacts", "delete")


def test_firm_settings_user_permission_groups(conn):
    """user-permission-groups: a Private contact/matter is viewable
    only by designated-group members and admins; contact privacy
    cascades to its matters and takes precedence."""
    conn.actor.set("user", ADA)
    g_cleo = users.create_group(conn, "Removal Team")
    users.add_group_member(conn, g_cleo, CLEO)
    g_bram = users.create_group(conn, "Business Team")
    users.add_group_member(conn, g_bram, BRAM)
    # public by default: everyone sees contact 1
    assert users.visible(conn, BRAM, "contact", 1)
    # private to Cleo's group: Cleo and admin see it, Bram does not
    users.set_privacy(conn, "contact", 1, g_cleo)
    assert users.visible(conn, CLEO, "contact", 1)
    assert users.visible(conn, ADA, "contact", 1)
    assert not users.visible(conn, BRAM, "contact", 1)
    # cascade: matter 1 (primary contact 1) inherits the restriction
    assert users.visible(conn, CLEO, "matter", 1)
    assert not users.visible(conn, BRAM, "matter", 1)
    # ... and contact privacy takes precedence over matter-level
    users.set_privacy(conn, "matter", 1, g_bram)
    assert not users.visible(conn, BRAM, "matter", 1)
    # matter-level privacy alone governs once the contact is public
    users.clear_privacy(conn, "contact", 1)
    assert users.visible(conn, BRAM, "matter", 1)
    assert not users.visible(conn, CLEO, "matter", 1)


def test_firm_settings_time_zone_setting(conn):
    """time-zone-setting: user saves an events time zone -> persisted
    on their account."""
    conn.actor.set("user", CLEO)
    users.update_user(conn, CLEO, timezone="America/Chicago")
    row = conn.execute("SELECT timezone FROM users WHERE id=?",
                       (CLEO,)).fetchone()
    assert row["timezone"] == "America/Chicago"


def test_personal_settings_user_roles(conn):
    """user-roles: a saved User Role label shows next to the user's
    name where they are assigned to a matter."""
    conn.actor.set("user", CLEO)
    users.update_user(conn, CLEO, role_label="Senior Paralegal")
    # matter 3 is seeded with assignee Cleo
    assert users.matter_assignee_label(conn, 3) == \
        "Cleo Synthetic (Senior Paralegal)"
    # admins set another user's role via Edit User
    conn.actor.set("user", ADA)
    users.update_user(conn, BRAM, role_label="Of Counsel")
    row = conn.execute("SELECT role_label FROM users WHERE id=?",
                       (BRAM,)).fetchone()
    assert row["role_label"] == "Of Counsel"
