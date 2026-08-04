"""Spine tests: priority-date tracking over the captured Visa
Bulletin dataset (U3.4). Cutoff values asserted here are verbatim
from data/visa_bulletin/raw/ (see its README for provenance)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import bulletin, matters  # noqa: E402

NOW = "2026-08-01T09:00:00Z"
ADA, BRAM = 1, 2


def test_case_tracking_priority_date_tracking(conn):
    """priority-date-tracking (adapted): priority date + preference
    category on a matter -> status for filing and status for final
    action computed against the loaded bulletin dataset."""
    conn.actor.set("user", ADA)
    bulletin.load_month(conn, "2026-06", NOW)
    # matter 1 (seeded): F2A / Mexico / PD 2022-03-15
    s = bulletin.matter_status(conn, 1)
    # June 2026 F2A Mexico final action 01JAN24: PD 2022 is earlier
    assert s["final_action"]["status"] == "current"
    assert s["final_action"]["cutoff"] == "01JAN24"
    # F2A filing chart is C across the board
    assert s["filing"]["status"] == "current"
    assert s["filing"]["cutoff"] == "C"
    # matter 3 (seeded): F1 / India / PD 2020-11-02
    s = bulletin.matter_status(conn, 3)
    # June F1 India final action 01SEP17, filing 01OCT18: not current
    assert s["final_action"]["status"] == "not_current"
    assert s["final_action"]["cutoff"] == "01SEP17"
    assert s["filing"]["status"] == "not_current"
    # unlisted countries charge to ALL; U renders as unavailable
    mid = matters.create_matter(
        conn, "Ivo Synthetic EB-2", 6, NOW, ADA, matter_type_id=3,
        priority_date="2013-08-01", preference_category="EB-2",
        chargeability_country="India", assignee_id=BRAM)
    s = bulletin.matter_status(conn, mid)
    assert s["final_action"]["status"] == "current"  # 01SEP13 in June
    bulletin.load_month(conn, "2026-07", NOW)
    s = bulletin.matter_status(conn, mid)
    assert s["final_action"]["status"] == "unavailable"  # July: U
    assert s["final_action"]["cutoff"] == "U"


def test_case_tracking_priority_date_notifications(conn):
    """priority-date-notifications (adapted): a loaded bulletin
    update that changes a tracked matter's status -> in-app
    notification + the change appears in the monthly email digest."""
    conn.actor.set("user", ADA)
    # EB-1 India, PD between July's and June's cutoffs: the captured
    # Jun->Jul retrogression (15DEC22 -> 15OCT22) flips it backward
    retro = matters.create_matter(
        conn, "Hana Synthetic EB-1", 5, NOW, ADA, matter_type_id=3,
        priority_date="2022-11-01", preference_category="EB-1",
        chargeability_country="India", assignee_id=BRAM)
    # F2A worldwide, PD after Jul cutoff but before Aug's big jump
    # (01JAN25 -> 22JUL26): flips forward on the August load
    fwd = matters.create_matter(
        conn, "Ivo Synthetic F2A", 6, NOW, ADA, matter_type_id=1,
        priority_date="2025-06-01", preference_category="F2A",
        chargeability_country="Testlandia")
    bulletin.load_month(conn, "2026-06", NOW)
    assert bulletin.matter_status(conn, retro)["final_action"]["status"] \
        == "current"
    # first load never notifies -- there is no prior status to diff
    assert conn.execute("SELECT count(*) FROM notifications").fetchone()[0] == 0
    changes = bulletin.load_month(conn, "2026-07", NOW)
    assert bulletin.matter_status(conn, retro)["final_action"]["status"] \
        == "not_current"
    assert any(c["matter_id"] == retro and c["chart"] == "final_action"
               and c["new"] == "not_current" for c in changes)
    # in-app notification reaches the matter assignee
    n = conn.execute(
        "SELECT * FROM notifications WHERE kind='priority_date_status'"
        " AND user_id=?", (BRAM,)).fetchall()
    payloads = [json.loads(r["payload"]) for r in n]
    assert any(p["matter_id"] == retro for p in payloads)
    # the change appears in the monthly email digest (to admins)
    mail = conn.execute(
        "SELECT * FROM email_outbox WHERE template='visa_bulletin_digest'"
        " ORDER BY id DESC").fetchall()
    assert any("Hana Synthetic EB-1" in m["body"] and
               m["recipient"] == "ada.admin@example.test" for m in mail)
    # assignee-less matter falls back to admin in-app notification
    changes = bulletin.load_month(conn, "2026-08", NOW)
    assert any(c["matter_id"] == fwd and c["new"] == "current"
               for c in changes)
    n = conn.execute(
        "SELECT payload FROM notifications WHERE user_id=?", (ADA,)).fetchall()
    assert any(json.loads(r["payload"])["matter_id"] == fwd for r in n)
    # flat cells notify nothing: matter 1 (F2A Mexico) was current in
    # June and July alike -- no notification rows name it
    all_payloads = [json.loads(r["payload"]) for r in conn.execute(
        "SELECT payload FROM notifications").fetchall()]
    assert not any(p["matter_id"] == 1 for p in all_payloads)
