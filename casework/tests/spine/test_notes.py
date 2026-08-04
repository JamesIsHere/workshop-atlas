"""Spine tests: notes module (U1.5)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import notes  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
LATER = "2026-08-01T10:00:00Z"
ADA, BRAM, CLEO = 1, 2, 3


def test_notes_module_exists(conn):
    """module-exists: Notes Dashboard and contact/matter Notes tabs
    list the notes for their scope."""
    conn.actor.set("user", ADA)
    n1 = notes.create_note(conn, "Dashboard note", NOW, ADA)
    n2 = notes.create_note(conn, "About Dana", NOW, ADA, contact_id=1)
    n3 = notes.create_note(conn, "On the I-130", NOW, ADA, matter_id=1)
    all_ids = notes.list_notes(conn)
    assert {n1, n2, n3} <= set(all_ids)
    assert set(notes.list_notes(conn, contact_id=1)) == {n2, n3}
    assert notes.list_notes(conn, matter_id=1) == [n3]


def test_notes_note_creation(conn):
    """note-creation: content in a chosen scope; matter-tab notes
    associate the matter AND its primary contact; notify-all lands a
    notification for every other active member."""
    conn.actor.set("user", CLEO)
    nid = notes.create_note(conn, "Called USCIS", NOW, CLEO,
                            title="Call log", matter_id=2, notify_all=1)
    n = conn.execute("SELECT * FROM notes WHERE id=?", (nid,)).fetchone()
    assert n["matter_id"] == 2
    assert n["contact_id"] == 2  # matter 2's primary contact (Emil)
    assert notes.assignees(conn, nid) == [CLEO]  # creator by default
    who = [r["user_id"] for r in conn.execute(
        "SELECT user_id FROM notifications WHERE kind='note_notify_all'"
        " ORDER BY user_id")]
    assert who == [ADA, BRAM]


def test_notes_note_assignment(conn):
    """note-assignment: add and remove firm-member assignees."""
    conn.actor.set("user", ADA)
    nid = notes.create_note(conn, "Reassign me", NOW, ADA)
    notes.assign(conn, nid, BRAM)
    assert notes.assignees(conn, nid) == [ADA, BRAM]
    notes.unassign(conn, nid, ADA)
    assert notes.assignees(conn, nid) == [BRAM]


def test_notes_note_client_association(conn):
    """note-client-association: Set a Client re-associates the note;
    choosing a matter brings its primary contact."""
    conn.actor.set("user", ADA)
    nid = notes.create_note(conn, "Unfiled thought", NOW, ADA)
    n = conn.execute("SELECT contact_id, matter_id FROM notes WHERE id=?",
                     (nid,)).fetchone()
    assert (n["contact_id"], n["matter_id"]) == (None, None)
    notes.set_client(conn, nid, matter_id=3)
    n = conn.execute("SELECT contact_id, matter_id FROM notes WHERE id=?",
                     (nid,)).fetchone()
    assert (n["contact_id"], n["matter_id"]) == (3, 3)  # Fara's I-130
    notes.set_client(conn, nid, contact_id=5)
    n = conn.execute("SELECT contact_id, matter_id FROM notes WHERE id=?",
                     (nid,)).fetchone()
    assert (n["contact_id"], n["matter_id"]) == (5, None)


def test_notes_note_categories(conn):
    """note-categories: premade categories ship; a custom category is
    creatable, assignable, and filterable."""
    conn.actor.set("user", ADA)
    premade = [r["name"] for r in conn.execute(
        "SELECT name FROM note_categories WHERE builtin=1 ORDER BY id")]
    assert premade == ["Government Action", "Memo", "Meeting", "Phone Call"]
    cid = notes.create_category(conn, "RFE Strategy")
    n1 = notes.create_note(conn, "RFE angle", NOW, ADA, category_id=cid)
    notes.create_note(conn, "Memo note", NOW, ADA, category_id=2)
    assert notes.list_notes(conn, category_id=cid) == [n1]


def test_notes_pinned_notes(conn):
    """pinned-notes: a pinned note tops the list in every scope."""
    conn.actor.set("user", ADA)
    n1 = notes.create_note(conn, "Old note", NOW, ADA, contact_id=1)
    n2 = notes.create_note(conn, "New note", LATER, ADA, contact_id=1)
    assert notes.list_notes(conn, contact_id=1) == [n2, n1]  # newest first
    notes.pin(conn, n1)
    assert notes.list_notes(conn, contact_id=1) == [n1, n2]  # pinned tops
    notes.pin(conn, n1, pinned=False)
    assert notes.list_notes(conn, contact_id=1) == [n2, n1]


def test_notes_notes_export(conn):
    """notes-export: the Notes tab's Export produces a PDF of that
    contact's/matter's notes."""
    conn.actor.set("user", ADA)
    notes.create_note(conn, "Passport received", NOW, ADA,
                      title="Intake progress", matter_id=1, category_id=3)
    notes.create_note(conn, "Unrelated note", NOW, ADA, contact_id=5)
    pdf = notes.export_notes_pdf(conn, matter_id=1)
    assert pdf.startswith(b"%PDF-")
    assert pdf.rstrip().endswith(b"%%EOF")
    # uncompressed streams: the scoped note is in, the other is out
    assert b"Passport received" in pdf and b"Intake progress" in pdf
    assert b"[Meeting]" in pdf
    assert b"Unrelated note" not in pdf
