"""Spine tests: contacts-and-matters contact-side entries (U1.3)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import contacts, facts  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
LATER = "2026-08-01T10:00:00Z"
ADA = 1


def test_contacts_and_matters_contact_creation(conn):
    """contact-creation: person or company created with a name ->
    exists and is open for field-by-field editing."""
    conn.actor.set("user", ADA)
    cid = contacts.create_contact(conn, "person", NOW, ADA,
                                  given_name="Nia", family_name="Synthetic",
                                  email="nia@example.test")
    row = conn.execute("SELECT * FROM contacts WHERE id=?", (cid,)).fetchone()
    assert row["kind"] == "person"
    assert row["display_name"] == "Nia Synthetic"  # composed from atoms
    f = facts.facts_of(conn, "contact", cid)
    assert f[("bio.given_name", 0)] == "Nia"
    assert f[("contact.email", 0)] == "nia@example.test"
    # further fields are edited per-field on the overview page
    facts.set_fact(conn, "contact", cid, "bio.date_of_birth",
                   "1992-02-02", LATER)
    assert facts.get_fact(conn, "contact", cid, "bio.date_of_birth") \
        == "1992-02-02"
    # company creation
    co = contacts.create_contact(conn, "company", NOW, ADA,
                                 company_name="Synthetic Widgets Inc")
    row = conn.execute("SELECT kind, display_name FROM contacts WHERE id=?",
                       (co,)).fetchone()
    assert (row["kind"], row["display_name"]) == \
        ("company", "Synthetic Widgets Inc")


def test_contacts_and_matters_custom_attributes(conn):
    """custom-attributes (adapted): admin defines a custom field ->
    fillable on overview pages AND available in custom intakes
    (P2 leg, landed with U2.4) AND in automated templates (P4 leg,
    landed with U4.3)."""
    conn.actor.set("user", ADA)
    key = facts.define_custom_attribute(
        conn, "bar-number", "contact", "text", "Bar number")
    assert key == "custom.bar-number"
    d = facts.definition(conn, key)
    assert d["is_custom"] == 1 and d["value_type"] == "text"
    facts.set_fact(conn, "contact", 1, key, "VA-99999", NOW)
    assert facts.get_fact(conn, "contact", 1, key) == "VA-99999"
    # P4 template consumption: the label extends the tag vocabulary
    from app import templates
    assert templates.tag_values(conn, 1, NOW)["bar_number"] == "VA-99999"
    # P2 intake consumption: a custom question saving to the custom
    # attribute lands the invitee's answer on the contact
    from app import custom, intake
    ci = custom.create_custom_intake(conn, "Attr probe", NOW)
    tab = custom.add_tab(conn, ci, "Probe", 1)
    qid = custom.add_question(conn, ci, tab, "Bar number?", "text", 1,
                              save_to_fact_key=key)
    sfid = custom.instantiate(conn, ci, "Probe intake", NOW, ADA,
                              contact_id=3)
    intake.answer_intake(conn, sfid, f"cq.{qid}", "VA-12345", NOW)
    assert facts.get_fact(conn, "contact", 3, key) == "VA-12345"
    # all six value types are definable, incl. expiry and list
    for vt in ("number", "date", "boolean", "list", "expiry"):
        k = facts.define_custom_attribute(
            conn, f"probe-{vt}", "matter", vt, f"Probe {vt}",
            list_options='["a","b"]' if vt == "list" else None)
        assert facts.definition(conn, k)["value_type"] == vt
    # subject-type mismatch is refused at the write path
    try:
        facts.set_fact(conn, "matter", 1, key, "x", NOW)
        assert False, "matter write against a contact key must fail"
    except ValueError:
        pass


def test_contacts_and_matters_related_contacts(conn):
    """related-contacts: a relation appears on both contacts."""
    conn.actor.set("user", ADA)
    contacts.relate(conn, 1, 2, "spouse")
    contacts.relate(conn, 7, 2, "employer")
    assert (2, "spouse") in contacts.relations_of(conn, 1)
    assert (1, "spouse") in contacts.relations_of(conn, 2)  # mirrored
    assert (7, "employer") in contacts.relations_of(conn, 2)
    # stored once: exactly one row for the pair
    n = conn.execute(
        "SELECT count(*) FROM contact_relations WHERE"
        " (contact_id=1 AND related_contact_id=2) OR"
        " (contact_id=2 AND related_contact_id=1)").fetchone()[0]
    assert n == 1


def test_contacts_and_matters_contact_search(conn):
    """contact-search: name, email, phone, A-Number, and unique
    identifier all find their contact."""
    conn.actor.set("user", ADA)
    hits = {q: [c for c, _ in contacts.search_contacts(conn, q)]
            for q in ("Dana", "emil@example.test", "+1-555-0103",
                      "A-SYNTH-0004", "SYNTH-C5")}
    assert hits["Dana"] == [1]
    assert hits["emil@example.test"] == [2]
    assert hits["+1-555-0103"] == [3]
    assert hits["A-SYNTH-0004"] == [4]
    assert hits["SYNTH-C5"] == [5]
    # tombstoned contacts stay out of results
    conn.execute("UPDATE contacts SET deleted_at=?, deleted_by=? WHERE id=1",
                 (NOW, ADA))
    assert [c for c, _ in contacts.search_contacts(conn, "Dana")] == []


def test_contacts_and_matters_contact_archiving(conn):
    """contact-archiving: bulk archive -> contacts leave the primary
    view and appear under Archived Contacts; un-archive reverses."""
    conn.actor.set("user", ADA)
    contacts.archive_contacts(conn, [5, 6], NOW)
    primary = [c for c, _ in contacts.list_contacts(conn, "primary")]
    archived = [c for c, _ in contacts.list_contacts(conn, "archived")]
    assert 5 not in primary and 6 not in primary
    assert archived == [5, 6]
    contacts.unarchive_contacts(conn, [5])
    assert 5 in [c for c, _ in contacts.list_contacts(conn, "primary")]
    assert [c for c, _ in contacts.list_contacts(conn, "archived")] == [6]


def test_contacts_and_matters_contact_merging(conn):
    """contact-merging: duplicates merge to a single contact carrying
    the most recently updated data; references repoint; losers are
    trash-recoverable."""
    conn.actor.set("user", ADA)
    # a duplicate Dana with a NEWER email and an extra fact
    dup = contacts.create_contact(conn, "person", LATER, ADA,
                                  given_name="Dana", family_name="Synthetic",
                                  email="dana.new@example.test")
    facts.set_fact(conn, "contact", dup, "imm.ead_expiry",
                   "2027-01-31", LATER)
    conn.execute("UPDATE matters SET primary_contact_id=? WHERE id=2", (dup,))
    contacts.relate(conn, dup, 2, "sibling")

    survivor = contacts.merge_contacts(conn, [1, dup], NOW, merged_by=ADA)
    assert survivor == 1
    # single live Dana remains
    live = [c for c, _ in contacts.search_contacts(conn, "Dana")]
    assert live == [1]
    # newest data won; older survivor values kept where not superseded
    assert facts.get_fact(conn, "contact", 1, "contact.email") \
        == "dana.new@example.test"
    assert facts.get_fact(conn, "contact", 1, "imm.ead_expiry") \
        == "2027-01-31"
    assert facts.get_fact(conn, "contact", 1, "bio.date_of_birth") \
        == "1990-04-12"
    # references repointed
    assert conn.execute("SELECT primary_contact_id FROM matters WHERE id=2"
                        ).fetchone()[0] == 1
    assert (2, "sibling") in contacts.relations_of(conn, 1)
    # loser is tombstoned (trash-recoverable), not destroyed
    row = conn.execute("SELECT deleted_at, deleted_by FROM contacts"
                       " WHERE id=?", (dup,)).fetchone()
    assert row["deleted_at"] == NOW and row["deleted_by"] == ADA
    # loser carries no facts
    assert facts.facts_of(conn, "contact", dup) == {}
