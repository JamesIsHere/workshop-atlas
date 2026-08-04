#!/usr/bin/env python
"""U1.1 engine unit tests -- standalone script, exit 0 on pass.
Run: python tests/unit_ledger.py (from casework-billing/)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASEWORK = ROOT.parent / "casework"
sys.path.insert(0, str(CASEWORK))
sys.path.insert(0, str(ROOT / "verify"))

from app import db as appdb, ledger  # noqa: E402
import run_fiduciary as fid  # noqa: E402

SEED = CASEWORK / "seeds" / "seed.sql"
D = "2026-08-02"
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


def t_drift_guard():
    assert ledger.RECIPE_ACCOUNT_KINDS == fid.RECIPE_KINDS, \
        "engine and verifier recipe tables have drifted"


def t_recipes_and_balances():
    conn = fresh()
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    op = ledger.create_bank_account(conn, "operating_bank", "SYNTH Op", 1)
    ledger.record_trust_deposit(conn, iolta, 500000, D, 1, contact_id=1)
    ledger.earn_out(conn, iolta, op, 300000, D, 1, contact_id=1)
    ledger.disburse(conn, iolta, 120000, D, 1, contact_id=1,
                    counterparty="SYNTH-USCIS")
    assert ledger.account_balance(conn, iolta) == 80000
    sub = ledger.ensure_client_trust(conn, iolta, 1)
    assert ledger.account_balance(conn, sub) == 80000
    assert ledger.account_balance(conn, op) == 300000
    ok, _ = fid.check_f1(conn)
    assert ok, "F1 on engine-posted ledger"


def t_blocks_fire_atomically():
    conn = fresh()
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    ledger.record_trust_deposit(conn, iolta, 100000, D, 1, contact_id=1)
    n_entries = conn.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0]
    n_events = conn.execute("SELECT COUNT(*) FROM external_events").fetchone()[0]
    try:
        ledger.disburse(conn, iolta, 999999, D, 1, contact_id=1)
        raise AssertionError("overdraft disbursement was allowed")
    except ledger.LedgerError:
        pass
    try:
        op = ledger.create_bank_account(conn, "operating_bank", "SYNTH Op", 1)
        ledger.earn_out(conn, iolta, op, 999999, D, 1, contact_id=1)
        raise AssertionError("over-available earn_out was allowed")
    except ledger.LedgerError:
        pass
    assert conn.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0] \
        == n_entries + 0 or True
    # nothing was written by the blocked attempts (entry count grew only
    # by the successful ops above the failures: none)
    assert conn.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0] \
        == n_entries, "blocked entry leaked postings"
    assert conn.execute("SELECT COUNT(*) FROM external_events").fetchone()[0] \
        == n_events, "blocked entry leaked external events"


def t_matter_vs_client_pots():
    conn = fresh()
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    cbase = ledger.trust_account_tab(conn, contact_id=1)["available_cents"]
    ledger.record_trust_deposit(conn, iolta, 100000, D, 1, contact_id=1)
    ledger.record_trust_deposit(conn, iolta, 50000, D, 1, matter_id=1)
    try:
        ledger.disburse(conn, iolta, 120000, D, 1, matter_id=1)
        raise AssertionError("matter pot spent client-level funds")
    except ledger.LedgerError:
        pass
    ledger.disburse(conn, iolta, 50000, D, 1, matter_id=1)
    assert ledger.trust_account_tab(conn, matter_id=1)["available_cents"] == 0
    assert ledger.trust_account_tab(conn, contact_id=1)["available_cents"] \
        == cbase + 100000


def t_conformance():
    conn = fresh()
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    fee = ledger.ensure_income_account(conn)
    try:
        ledger._post(conn, "trust_deposit",
                     [(iolta, "debit", 100), (fee, "credit", 100)],
                     1, D)
        raise AssertionError("fee_income accepted in trust_deposit recipe")
    except ledger.LedgerError:
        pass
    try:
        ledger._post(conn, "trust_deposit", [(iolta, "debit", 100)], 1, D)
        raise AssertionError("unbalanced entry accepted")
    except ledger.LedgerError:
        pass


def t_reversal():
    conn = fresh()
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    cbase = ledger.trust_account_tab(conn, contact_id=1)["available_cents"]
    dep = ledger.record_trust_deposit(conn, iolta, 100000, D, 1, contact_id=1)
    e = ledger.disburse(conn, iolta, 40000, D, 1, contact_id=1)
    rev = ledger.reverse_entry(conn, e, 1, D)
    row = conn.execute("SELECT reverses_entry_id, kind FROM journal_entries"
                       " WHERE id=?", (rev,)).fetchone()
    assert row["reverses_entry_id"] == e and row["kind"] == "reversal"
    assert ledger.trust_account_tab(conn, contact_id=1)["available_cents"] \
        == cbase + 100000, "reversal restored the position"
    # reversing THIS test's deposit after its funds are spent must block
    ledger.disburse(conn, iolta, 90000, D, 1, contact_id=1)
    try:
        ledger.reverse_entry(conn, dep, 1, D)
        raise AssertionError("deposit reversal overdrew spent funds")
    except ledger.LedgerError:
        pass


def t_audit_and_fiduciary():
    conn = fresh()
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    op = ledger.create_bank_account(conn, "operating_bank", "SYNTH Op", 1)
    ledger.record_trust_deposit(conn, iolta, 500000, D, 1, contact_id=1,
                                memo="Retainer")
    ledger.earn_out(conn, iolta, op, 200000, D, 1, contact_id=1)
    ledger.record_bill_direct_payment(conn, op, 50000, D, 1)
    n = conn.execute("SELECT COUNT(*) FROM audit_log WHERE entity_type IN"
                     " ('journal_entries','journal_postings',"
                     "'external_events','ledger_accounts')").fetchone()[0]
    assert n > 0, "ledger mutations are audited"
    lines = []
    for chk in (fid.check_f1, fid.check_f2, fid.check_f3, fid.check_f4,
                fid.check_f5, fid.check_f6, fid.check_f8):
        ok, line = chk(conn)
        lines.append(line)
        assert ok, line
    return lines


if __name__ == "__main__":
    for f in (t_drift_guard, t_recipes_and_balances,
              t_blocks_fire_atomically, t_matter_vs_client_pots,
              t_conformance, t_reversal, t_audit_and_fiduciary):
        check(f.__name__, f)
    print("unit_ledger: %d/7 pass" % (7 - len(FAILS)))
    sys.exit(1 if FAILS else 0)
