"""Trash can (U1.6): list and restore tombstoned records.

The set of trashable tables derives from the generator's own
soft_delete declarations -- the same sweep-and-schema-agree pattern
as verify/checks.py (gate ruling 9).
"""

from app.schema.gen_schema import TABLES

TOMBSTONED = tuple(name for name, _cols, soft, _aud in TABLES if soft)


def _check(record_type):
    if record_type not in TOMBSTONED:
        raise ValueError(f"not a trashable record type: {record_type}")


def soft_delete(conn, record_type, record_id, deleted_by, now):
    _check(record_type)
    conn.execute(f"UPDATE {record_type} SET deleted_at=?, deleted_by=?"
                 " WHERE id=?", (now, deleted_by, record_id))


def list_trash(conn, record_type):
    """[(id, deleted_at, deleted_by)] for a dashboard's Trash view."""
    _check(record_type)
    rows = conn.execute(
        f"SELECT id, deleted_at, deleted_by FROM {record_type}"
        " WHERE deleted_at IS NOT NULL ORDER BY deleted_at, id").fetchall()
    return [(r["id"], r["deleted_at"], r["deleted_by"]) for r in rows]


def restore(conn, record_type, record_id):
    """Clear the tombstone; the audit trigger records it and the feed
    labels it 'restore' (semantic_action)."""
    _check(record_type)
    conn.execute(f"UPDATE {record_type} SET deleted_at=NULL,"
                 " deleted_by=NULL WHERE id=?", (record_id,))
