"""Spine tests: activity feeds and trash can (U1.6)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import contacts, feed, notes, trash  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM = 1, 2


def test_contacts_and_matters_activity_feeds(conn):
    """activity-feeds (adapted): the Firm Feed lists creations and
    updates of in-scope resource types, searchable; per-contact and
    per-matter feeds scope correctly."""
    conn.actor.set("user", ADA)
    cid = contacts.create_contact(conn, "person", NOW, ADA,
                                  given_name="Odo", family_name="Synthetic")
    conn.actor.set("user", BRAM)
    nid = notes.create_note(conn, "Feed probe note", NOW, BRAM,
                            matter_id=1)
    conn.execute("UPDATE matters SET description='updated' WHERE id=1")

    rows = feed.firm_feed(conn)
    kinds = {(r["entity_type"], r["semantic_action"]) for r in rows}
    assert ("contacts", "insert") in kinds
    assert ("notes", "insert") in kinds
    assert ("matters", "update") in kinds
    # filter by resource type and by firm member
    assert all(r["entity_type"] == "notes"
               for r in feed.firm_feed(conn, entity_type="notes"))
    by_bram = feed.firm_feed(conn, actor_id=BRAM)
    assert by_bram and all(r["actor_id"] == BRAM for r in by_bram)
    # search by resource content
    hits = feed.firm_feed(conn, q="Feed probe note")
    assert [r["entity_id"] for r in hits] == [nid]
    # per-contact and per-matter feeds
    assert any(r["entity_type"] == "contacts" and r["entity_id"] == cid
               for r in feed.contact_feed(conn, cid))
    mrows = feed.matter_feed(conn, 1)
    assert any(r["entity_type"] == "notes" and r["entity_id"] == nid
               for r in mrows)
    assert any(r["entity_type"] == "matters" and
               r["semantic_action"] == "update" for r in mrows)


def test_firm_settings_trash_can(conn):
    """trash-can: deleted records appear in the Trash view; Restore
    returns them to their dashboard."""
    conn.actor.set("user", ADA)
    nid = notes.create_note(conn, "Doomed note", NOW, ADA, contact_id=1)
    trash.soft_delete(conn, "notes", nid, deleted_by=ADA, now=NOW)
    trash.soft_delete(conn, "contacts", 6, deleted_by=ADA, now=NOW)
    # gone from the dashboards
    assert nid not in notes.list_notes(conn, contact_id=1)
    assert 6 not in [c for c, _ in contacts.list_contacts(conn, "primary")]
    # present in the Trash views
    assert [t[0] for t in trash.list_trash(conn, "notes")] == [nid]
    assert [t[0] for t in trash.list_trash(conn, "contacts")] == [6]
    # restore returns the records to their dashboards
    trash.restore(conn, "notes", nid)
    trash.restore(conn, "contacts", 6)
    assert nid in notes.list_notes(conn, contact_id=1)
    assert 6 in [c for c, _ in contacts.list_contacts(conn, "primary")]
    assert trash.list_trash(conn, "notes") == []
    # the audit surface labels the round-trip correctly
    labels = [r["semantic_action"] for r in feed.firm_feed(
        conn, entity_type="notes") if r["entity_id"] == nid]
    assert labels[0] == "restore" and "soft_delete" in labels
    # non-tombstoned tables are refused
    try:
        trash.soft_delete(conn, "facts", 1, ADA, NOW)
        assert False, "facts must not be trashable"
    except ValueError:
        pass
