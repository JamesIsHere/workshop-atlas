"""Contacts (U1.3): create, relations, search, archive, merge.

Name model (schema-design.md): atoms are facts, display_name is the
one acknowledged derived label, composed here on write. Registry
columns are mechanics only; identifiers live in the fact store.
"""

from app import facts

# the four searchable identifier fact keys (gate ruling 7)
IDENTIFIER_KEYS = ("contact.email", "contact.phone", "imm.a_number",
                   "meta.unique_identifier")

# every contact-bearing FK column in the schema, for merge repointing;
# (table, column) -- record_privacy/question_comments handled apart.
CONTACT_FK_COLS = [
    ("matters", "primary_contact_id"),
    ("matter_contacts", "contact_id"),
    ("folders", "contact_id"),
    ("files", "contact_id"),
    ("files", "uploaded_by_contact_id"),
    ("esign_signers", "contact_id"),
    ("smart_forms", "contact_id"),
    ("intake_invitations", "contact_id"),
    ("notes", "contact_id"),
    ("tasks", "contact_id"),
    ("events", "contact_id"),
    ("event_attendees", "contact_id"),
]


def compose_display_name(given, family, middle=None):
    parts = [p for p in (given, middle, family) if p]
    return " ".join(parts)


def create_contact(conn, kind, now, created_by, given_name=None,
                   family_name=None, middle_name=None, company_name=None,
                   email=None, phone=None):
    """Create a person or company; atoms land in facts, display_name
    is composed. Returns the new contact id."""
    if kind == "person":
        display = compose_display_name(given_name, family_name, middle_name)
    elif kind == "company":
        display = company_name
    else:
        raise ValueError(f"unknown contact kind: {kind}")
    if not display:
        raise ValueError("a name is required")
    cur = conn.execute(
        "INSERT INTO contacts (kind, display_name, created_at, created_by)"
        " VALUES (?,?,?,?)", (kind, display, now, created_by))
    cid = cur.lastrowid
    atom_pairs = (("bio.given_name", given_name),
                  ("bio.family_name", family_name),
                  ("bio.middle_name", middle_name),
                  ("contact.email", email), ("contact.phone", phone))
    for key, value in atom_pairs:
        if value is not None:
            facts.set_fact(conn, "contact", cid, key, value, now)
    facts.set_fact(conn, "contact", cid, "meta.synthetic", "true", now)
    return cid


def refresh_display_name(conn, contact_id, now):
    """Recompose the derived label from current name atoms (persons)."""
    row = conn.execute("SELECT kind FROM contacts WHERE id=?",
                       (contact_id,)).fetchone()
    if row is None or row["kind"] != "person":
        return
    f = facts.facts_of(conn, "contact", contact_id)
    display = compose_display_name(f.get(("bio.given_name", 0)),
                                   f.get(("bio.family_name", 0)),
                                   f.get(("bio.middle_name", 0)))
    if display:
        conn.execute("UPDATE contacts SET display_name=? WHERE id=?",
                     (display, contact_id))


# --- relations (stored once, mirrored by read) ---

def relate(conn, contact_id, related_contact_id, relation_type):
    if contact_id == related_contact_id:
        raise ValueError("a contact cannot relate to itself")
    conn.execute(
        "INSERT INTO contact_relations (contact_id, related_contact_id,"
        " relation_type) VALUES (?,?,?)",
        (contact_id, related_contact_id, relation_type))


def relations_of(conn, contact_id):
    """[(other_contact_id, relation_type)] seen from either side."""
    rows = conn.execute(
        "SELECT related_contact_id AS other, relation_type FROM"
        " contact_relations WHERE contact_id=?"
        " UNION ALL"
        " SELECT contact_id AS other, relation_type FROM contact_relations"
        " WHERE related_contact_id=?", (contact_id, contact_id)).fetchall()
    return [(r["other"], r["relation_type"]) for r in rows]


# --- search ---

def search_contacts(conn, query):
    """Match on display_name or any identifier fact (email, phone,
    A-Number, unique identifier). Live contacts only."""
    like = f"%{query}%"
    rows = conn.execute(
        "SELECT DISTINCT c.id, c.display_name FROM contacts c"
        " LEFT JOIN facts f ON f.subject_type='contact' AND"
        "   f.subject_id=c.id AND f.key IN (?,?,?,?)"
        " WHERE c.deleted_at IS NULL AND"
        "   (c.display_name LIKE ? OR f.value LIKE ?)"
        " ORDER BY c.id", (*IDENTIFIER_KEYS, like, like)).fetchall()
    return [(r["id"], r["display_name"]) for r in rows]


# --- archiving (working-set filter, distinct from trash) ---

def archive_contacts(conn, contact_ids, now):
    for cid in contact_ids:
        conn.execute("UPDATE contacts SET archived_at=? WHERE id=?",
                     (now, cid))


def unarchive_contacts(conn, contact_ids):
    for cid in contact_ids:
        conn.execute("UPDATE contacts SET archived_at=NULL WHERE id=?",
                     (cid,))


def list_contacts(conn, view="primary"):
    """view: primary (unarchived, live) | archived (live)."""
    cond = "archived_at IS NULL" if view == "primary" \
        else "archived_at IS NOT NULL"
    rows = conn.execute(
        f"SELECT id, display_name FROM contacts WHERE deleted_at IS NULL"
        f" AND {cond} ORDER BY id").fetchall()
    return [(r["id"], r["display_name"]) for r in rows]


# --- merge ---

def merge_contacts(conn, contact_ids, now, merged_by):
    """Merge duplicates: lowest id survives; per-(key, idx) the most
    recently updated fact value wins; every contact FK repoints to the
    survivor; losers are tombstoned (trash-recoverable). Returns the
    survivor id."""
    ids = sorted(set(contact_ids))
    if len(ids) < 2:
        raise ValueError("merge needs at least two contacts")
    survivor, losers = ids[0], ids[1:]
    qmarks = ",".join("?" for _ in ids)

    # newest value per (key, idx) across all duplicates; on equal
    # updated_at the survivor's own value wins (sorted last, so its
    # overwrite is final)
    rows = conn.execute(
        f"SELECT key, idx, value, updated_at, subject_id FROM facts"
        f" WHERE subject_type='contact' AND subject_id IN ({qmarks})"
        f" ORDER BY updated_at,"
        f" CASE WHEN subject_id=? THEN 1 ELSE 0 END",
        (*ids, survivor)).fetchall()
    winners = {}
    for r in rows:
        winners[(r["key"], r["idx"])] = r["value"]

    # repoint FK columns (loser links duplicating survivor links die)
    lq = ",".join("?" for _ in losers)
    conn.execute(
        f"DELETE FROM matter_contacts WHERE contact_id IN ({lq}) AND"
        f" matter_id IN (SELECT matter_id FROM matter_contacts WHERE"
        f" contact_id=?)", (*losers, survivor))
    for table, col in CONTACT_FK_COLS:
        conn.execute(f"UPDATE {table} SET {col}=? WHERE {col} IN ({lq})",
                     (survivor, *losers))
    conn.execute(
        f"DELETE FROM record_privacy WHERE entity_type='contact' AND"
        f" entity_id IN ({lq}) AND group_id IN (SELECT group_id FROM"
        f" record_privacy WHERE entity_type='contact' AND entity_id=?)",
        (*losers, survivor))
    conn.execute(
        f"UPDATE record_privacy SET entity_id=? WHERE entity_type='contact'"
        f" AND entity_id IN ({lq})", (survivor, *losers))
    # relations: drop would-be self-relations, dedupe, then repoint
    conn.execute(
        f"DELETE FROM contact_relations WHERE contact_id IN ({qmarks})"
        f" AND related_contact_id IN ({qmarks})", (*ids, *ids))
    conn.execute(
        f"UPDATE contact_relations SET contact_id=? WHERE"
        f" contact_id IN ({lq})", (survivor, *losers))
    conn.execute(
        f"UPDATE contact_relations SET related_contact_id=? WHERE"
        f" related_contact_id IN ({lq})", (survivor, *losers))

    # facts: losers' rows die, winners land on the survivor
    conn.execute(
        f"DELETE FROM facts WHERE subject_type='contact' AND"
        f" subject_id IN ({lq})", losers)
    for (key, idx), value in winners.items():
        facts.set_fact(conn, "contact", survivor, key, value, now, idx)

    for loser in losers:
        conn.execute("UPDATE contacts SET deleted_at=?, deleted_by=?"
                     " WHERE id=?", (now, merged_by, loser))
    refresh_display_name(conn, survivor, now)
    return survivor
