#!/usr/bin/env python
"""Period-close engine unit tests (period-close.md, ratified
2026-08-09; program amendment same date) -- standalone script, exit 0
on pass. Run: python tests/unit_period_close.py (from
casework-billing/). Convention: unit_ledger.py (NOT test_* -- the
parity runner's discovery is corpus-map-bound; the close is not a
corpus entry)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASEWORK = ROOT.parent / "casework"
sys.path.insert(0, str(CASEWORK))
sys.path.insert(0, str(ROOT / "verify"))

from app import db as appdb, ledger, period  # noqa: E402

SEED = CASEWORK / "seeds" / "seed.sql"
TODAY = "2026-08-09"
FAILS = []


def fresh():
    conn = appdb.create_db(":memory:")
    conn.actor.set("system", None)
    conn.executescript(SEED.read_text(encoding="utf-8"))
    conn.actor.set("user", 1)
    return conn


def check(name, fn):
    try:
        fn()
        print("  PASS %s" % name)
    except Exception as ex:
        FAILS.append(name)
        print("  FAIL %s -- %s: %s" % (name, type(ex).__name__, ex))


def _july_world(conn):
    """July facts: one cleared deposit, one month-end check still
    outstanding at 07-31 (T+3 clearing) -> exactly one carried item."""
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    ledger.record_trust_deposit(conn, iolta, 500000, "2026-07-10", 1,
                                contact_id=1)
    ledger.disburse(conn, iolta, 120000, "2026-07-29", 1, contact_id=1,
                    counterparty="SYNTH court")
    return iolta


def _prepare(conn, on_date=TODAY):
    p, pe = period.closable_month(conn, on_date)
    snap = period.compute(conn, p, pe)
    return period.prepare(conn, 1, on_date,
                          period.required_acks(snap))


def t_closable_ordering_and_month_over():
    conn = fresh()
    assert period.closable_month(conn, TODAY) is None, \
        "empty world must have nothing closable"
    _july_world(conn)
    assert period.closable_month(conn, TODAY) == ("2026-07", "2026-07-31")
    assert period.closable_month(conn, "2026-07-20") is None, \
        "a month still running must not be closable"


def t_prepare_requires_exact_acks():
    conn = fresh()
    _july_world(conn)
    try:
        period.prepare(conn, 1, TODAY, set())
        raise AssertionError("prepare accepted missing acknowledgments")
    except period.PeriodError:
        pass


def t_happy_path_and_strict_order():
    conn = fresh()
    _july_world(conn)
    _prepare(conn)
    row = period.get_row(conn, "2026-07")
    assert row["status"] == "prepared" and row["prepared_by"] == 1
    rec = period.approve(conn, 1, TODAY)
    assert rec["status"] == "closed" and rec["approved_by"] == 1
    assert period.last_closed(conn) == "2026-07"
    # strict order: August is next, closable only from September on
    assert period.closable_month(conn, TODAY) is None
    assert period.closable_month(conn, "2026-09-02") == \
        ("2026-08", "2026-08-31")


def t_stale_prepare_voids():
    conn = fresh()
    iolta = _july_world(conn)
    _prepare(conn)
    # a July fact lands mid-review (July is not closed yet -- legal)
    ledger.record_trust_deposit(conn, iolta, 10000, "2026-07-15", 1,
                                contact_id=1)
    try:
        period.approve(conn, 1, TODAY)
        raise AssertionError("approve accepted drifted numbers")
    except period.PeriodError:
        pass
    assert period.get_row(conn, "2026-07") is None, \
        "stale prepare must be void"
    _prepare(conn)
    assert period.approve(conn, 1, TODAY)["status"] == "closed"


def t_hard_lock_and_current_dated_correction():
    conn = fresh()
    iolta = _july_world(conn)
    _prepare(conn)
    period.approve(conn, 1, TODAY)
    # backdated recipe posting must refuse
    try:
        ledger.record_trust_deposit(conn, iolta, 5000, "2026-07-20", 1,
                                    contact_id=1)
        raise AssertionError("closed month accepted a posting")
    except period.PeriodError:
        pass
    # backdated bank fact must refuse
    try:
        ledger.create_external_event(conn, "deposit", iolta,
                                     "2026-07-20", 5000, "in")
        raise AssertionError("closed month accepted a bank event")
    except period.PeriodError:
        pass
    # correcting a closed-month entry works CURRENT-DATED
    eid = conn.execute("SELECT id FROM journal_entries WHERE"
                       " kind='trust_deposit' ORDER BY id LIMIT 1"
                       ).fetchone()[0]
    try:
        ledger.reverse_entry(conn, eid, 1, "2026-07-11")
        raise AssertionError("closed month accepted a backdated reversal")
    except period.PeriodError:
        pass
    # August 2026 is open until closed; current-dated reversal lands.
    # (Reversing the 5,000.00 deposit fails F4 only if spent; here
    # 1,200.00 was disbursed, so reverse a fresh smaller deposit.)
    e2 = ledger.record_trust_deposit(conn, iolta, 7000, "2026-08-05", 1,
                                     contact_id=1)
    ledger.reverse_entry(conn, e2, 1, "2026-08-06")


def t_no_reopen_surface():
    assert not hasattr(period, "reopen"), \
        "reopen exists -- element 10 says it must not"


TESTS = [t_closable_ordering_and_month_over,
         t_prepare_requires_exact_acks,
         t_happy_path_and_strict_order,
         t_stale_prepare_voids,
         t_hard_lock_and_current_dated_correction,
         t_no_reopen_surface]

if __name__ == "__main__":
    print("unit_period_close: %d tests" % len(TESTS))
    for t in TESTS:
        check(t.__name__, t)
    print("%d/%d pass" % (len(TESTS) - len(FAILS), len(TESTS)))
    sys.exit(1 if FAILS else 0)
