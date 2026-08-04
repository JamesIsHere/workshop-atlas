"""The fact-store write path (invariant 1, U1.3).

Every consumer reads facts through keys; every writer comes through
set_fact, which refuses undefined keys and subject-type mismatches --
the write-path guard for what the deferred fact-integrity sweep will
later assert wholesale.
"""

VALUE_TYPES = ("text", "number", "date", "boolean", "list", "expiry")


def define_custom_attribute(conn, slug, subject_type, value_type, label,
                            list_options=None, repeating=0):
    """Firm-defined custom field: key custom.<slug>, is_custom=1."""
    if value_type not in VALUE_TYPES:
        raise ValueError(f"unknown value type: {value_type}")
    key = f"custom.{slug}"
    conn.execute(
        "INSERT INTO fact_definitions (key, subject_type, value_type,"
        " label, is_custom, repeating, list_options) VALUES (?,?,?,?,1,?,?)",
        (key, subject_type, value_type, label, repeating, list_options))
    return key


def definition(conn, key):
    return conn.execute("SELECT * FROM fact_definitions WHERE key=?",
                        (key,)).fetchone()


def set_fact(conn, subject_type, subject_id, key, value, now, idx=0):
    d = definition(conn, key)
    if d is None:
        raise ValueError(f"undefined fact key: {key}")
    if d["subject_type"] != subject_type:
        raise ValueError(f"{key} is a {d['subject_type']} fact,"
                         f" not {subject_type}")
    if idx and not d["repeating"]:
        raise ValueError(f"{key} is not a repeating fact")
    conn.execute(
        "INSERT INTO facts (subject_type, subject_id, key, idx, value,"
        " updated_at) VALUES (?,?,?,?,?,?)"
        " ON CONFLICT (subject_type, subject_id, key, idx)"
        " DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
        (subject_type, subject_id, key, idx, value, now))


def get_fact(conn, subject_type, subject_id, key, idx=0):
    row = conn.execute(
        "SELECT value FROM facts WHERE subject_type=? AND subject_id=?"
        " AND key=? AND idx=?", (subject_type, subject_id, key, idx)).fetchone()
    return None if row is None else row["value"]


def facts_of(conn, subject_type, subject_id):
    """{(key, idx): value} for one subject."""
    rows = conn.execute(
        "SELECT key, idx, value FROM facts WHERE subject_type=? AND"
        " subject_id=?", (subject_type, subject_id)).fetchall()
    return {(r["key"], r["idx"]): r["value"] for r in rows}


def delete_fact(conn, subject_type, subject_id, key, idx=0):
    """Sanctioned hard delete (gate ruling 9); audited by trigger."""
    conn.execute(
        "DELETE FROM facts WHERE subject_type=? AND subject_id=? AND"
        " key=? AND idx=?", (subject_type, subject_id, key, idx))
