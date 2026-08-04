"""Activity feeds (U1.6): firm, per-contact, and per-matter views
over the activity_feed VIEW. Consumers use semantic_action only
(gate ruling 8) -- never raw action filters.
"""


def firm_feed(conn, entity_type=None, actor_id=None, q=None, limit=50):
    """The Firm Feed: newest first, filterable by resource type and
    firm member, searchable over resource content."""
    sql = ("SELECT id, at, actor_type, actor_id, semantic_action,"
           " entity_type, entity_id, changes FROM activity_feed WHERE 1=1")
    params = []
    if entity_type is not None:
        sql += " AND entity_type=?"
        params.append(entity_type)
    if actor_id is not None:
        sql += " AND actor_type='user' AND actor_id=?"
        params.append(actor_id)
    if q is not None:
        sql += " AND changes LIKE ?"
        params.append(f"%{q}%")
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    return conn.execute(sql, params).fetchall()


def contact_feed(conn, contact_id, limit=50):
    """A contact's feed: its own row plus every in-scope resource
    carrying the contact (contact_id in the changes json)."""
    return conn.execute(
        "SELECT id, at, actor_type, actor_id, semantic_action,"
        " entity_type, entity_id, changes FROM activity_feed WHERE"
        " (entity_type='contacts' AND entity_id=?)"
        " OR json_extract(changes, '$.contact_id')=?"
        " OR json_extract(changes, '$.new.contact_id')=?"
        " OR json_extract(changes, '$.primary_contact_id')=?"
        " OR json_extract(changes, '$.new.primary_contact_id')=?"
        " ORDER BY id DESC LIMIT ?",
        (contact_id,) * 5 + (limit,)).fetchall()


def matter_feed(conn, matter_id, limit=50):
    return conn.execute(
        "SELECT id, at, actor_type, actor_id, semantic_action,"
        " entity_type, entity_id, changes FROM activity_feed WHERE"
        " (entity_type='matters' AND entity_id=?)"
        " OR json_extract(changes, '$.matter_id')=?"
        " OR json_extract(changes, '$.new.matter_id')=?"
        " ORDER BY id DESC LIMIT ?",
        (matter_id,) * 3 + (limit,)).fetchall()
