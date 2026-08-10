#!/usr/bin/env python
"""run_fiduciary.py -- verifier 2: fiduciary invariant suite F1-F8.

Usage:
  python run_fiduciary.py <path-to-db>   run suite, write fiduciary-report.txt
  python run_fiduciary.py --selftest     instantiate design/ledger-schema-draft.sql
                                         in-memory, verify every check runs, is
                                         vacuously green on an empty ledger, and
                                         goes RED on deliberately broken scenarios
                                         (oracle calibration).

Report output carries no timestamps: goal.md requires two consecutive
byte-identical reports at close.

Skeleton status (P0): F1-F5, F8 fully implemented against the draft
schema. F6 implements the segregation half (fee entries never touch
trust) plus batch arithmetic; full settlement-linkage assertion deepens
in P3 when linkage fields carry data. F7 is a stub until the statement
generator exists (P5); it reports NO-STATEMENT as a distinct status,
never PASS, so a missing recon can never read as green.
"""
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRAFT_DDL = HERE.parent / "design" / "ledger-schema-draft.sql"
REPORT = HERE / "fiduciary-report.txt"

TRUST_KINDS = ("client_trust", "matter_trust")
BANK_TRUST = "trust_bank"

# Allowed account-kind sets per entry kind (recipe conformance, F5).
RECIPE_KINDS = {
    "trust_deposit":       {"trust_bank", "client_trust", "matter_trust"},
    "bill_direct_payment": {"operating_bank", "fee_income"},
    "earn_out":            {"trust_bank", "client_trust", "matter_trust",
                            "operating_bank", "fee_income"},
    "disbursement":        {"trust_bank", "client_trust", "matter_trust"},
    "sim_settlement":      {"trust_bank", "client_trust", "matter_trust",
                            "operating_bank", "fee_income"},
    "processor_fee":       {"processor_fee_expense", "operating_bank"},
    "chargeback":          {"chargeback_expense", "operating_bank"},
    # reversal inherits the reversed entry's kinds; checked structurally.
}


def natural_balance(kind, debits, credits):
    """Balance in the account's natural sign (assets/expenses debit-normal)."""
    if kind in ("operating_bank", "trust_bank", "processor_fee_expense",
                "chargeback_expense"):
        return debits - credits
    return credits - debits


def all_postings(con):
    return con.execute(
        """SELECT p.entry_id, p.account_id, p.side, p.amount_cents,
                  a.kind, a.parent_id, e.kind AS entry_kind,
                  e.reverses_entry_id
           FROM journal_postings p
           JOIN ledger_accounts a ON a.id = p.account_id
           JOIN journal_entries e ON e.id = p.entry_id
           ORDER BY p.entry_id, p.id"""
    ).fetchall()


def check_f1(con):
    rows = con.execute(
        """SELECT e.id,
                  SUM(CASE WHEN p.side='debit' THEN p.amount_cents
                           ELSE -p.amount_cents END) AS imbalance
           FROM journal_entries e JOIN journal_postings p ON p.entry_id=e.id
           GROUP BY e.id HAVING imbalance != 0"""
    ).fetchall()
    n = con.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0]
    return (len(rows) == 0,
            "F1 BALANCE: %d entries checked, %d unbalanced" % (n, len(rows)))


def _tree_children(con):
    """Map trust_bank id -> list of descendant liability account ids."""
    accounts = con.execute(
        "SELECT id, kind, parent_id FROM ledger_accounts").fetchall()
    by_parent = {}
    kinds = {}
    for aid, kind, parent in accounts:
        kinds[aid] = kind
        by_parent.setdefault(parent, []).append(aid)
    banks = [aid for aid, k in kinds.items() if k == BANK_TRUST]
    tree = {}
    for b in banks:
        desc = []
        stack = list(by_parent.get(b, []))
        while stack:
            a = stack.pop()
            desc.append(a)
            stack.extend(by_parent.get(a, []))
        tree[b] = [a for a in desc if kinds[a] in TRUST_KINDS]
    return tree, kinds


def _balances(con):
    bal = {}
    for r in con.execute(
        """SELECT p.account_id, a.kind,
                  SUM(CASE WHEN p.side='debit' THEN p.amount_cents ELSE 0 END),
                  SUM(CASE WHEN p.side='credit' THEN p.amount_cents ELSE 0 END)
           FROM journal_postings p JOIN ledger_accounts a ON a.id=p.account_id
           GROUP BY p.account_id"""):
        bal[r[0]] = natural_balance(r[1], r[2] or 0, r[3] or 0)
    return bal


def check_f2(con):
    tree, kinds = _tree_children(con)
    bal = _balances(con)
    bad = []
    for bank, subs in tree.items():
        bank_bal = bal.get(bank, 0)
        sub_sum = sum(bal.get(a, 0) for a in subs)
        if bank_bal != sub_sum:
            bad.append((bank, bank_bal, sub_sum))
    return (len(bad) == 0,
            "F2 CONTROL: %d trust banks checked, %d identity violations%s"
            % (len(tree), len(bad),
               "" if not bad else " " + repr(bad)))


def _running(con):
    """Replay postings in posting order; yield (entry, account, kind,
    running-balance-after) for trust-relevant accounts."""
    run = {}
    out = []
    for (entry, acct, side, cents, kind, _parent, ekind, _rev) in all_postings(con):
        if kind not in TRUST_KINDS and kind != BANK_TRUST:
            continue
        delta = natural_balance(kind, cents, 0) if side == "debit" \
            else natural_balance(kind, 0, cents)
        run[acct] = run.get(acct, 0) + delta
        out.append((entry, acct, kind, ekind, side, cents, run[acct]))
    return out


def check_f3(con):
    bad = [(e, a, b) for (e, a, k, ek, s, c, b) in _running(con) if b < 0]
    n = len(_running(con))
    return (len(bad) == 0,
            "F3 NO-OVERDRAFT: %d trust postings replayed, %d negative points"
            % (n, len(bad)))


def check_f4(con):
    bad = []
    for (entry, acct, kind, ekind, side, cents, after) in _running(con):
        outflow = (kind in TRUST_KINDS and side == "debit") or \
                  (kind == BANK_TRUST and side == "credit")
        if outflow and after < 0:
            bad.append(entry)
    return (len(set(bad)) == 0,
            "F4 AVAILABILITY: %d over-available outflow entries"
            % len(set(bad)))


def check_f5(con):
    entries = {}
    ekinds = {}
    revs = {}
    for (entry, acct, side, cents, kind, _p, ekind, rev) in all_postings(con):
        entries.setdefault(entry, set()).add(kind)
        ekinds[entry] = ekind
        revs[entry] = rev
    bad = []
    for entry, kinds in entries.items():
        ek = ekinds[entry]
        if ek == "reversal":
            if revs[entry] is None:
                bad.append((entry, "reversal without reverses_entry_id"))
                continue
            allowed = entries.get(revs[entry], set())
        else:
            allowed = RECIPE_KINDS.get(ek)
        if allowed is None:
            bad.append((entry, "unknown recipe %s" % ek))
        elif not kinds <= allowed:
            bad.append((entry, "kinds %s outside recipe %s"
                        % (sorted(kinds), ek)))
        if BANK_TRUST in kinds and not (kinds & set(TRUST_KINDS)):
            bad.append((entry, "trust_bank moved without sub-ledger leg"))
    return (len(bad) == 0,
            "F5 SEGREGATION: %d entries checked, %d violations%s"
            % (len(entries), len(bad), "" if not bad else " " + repr(bad)))


def check_f6(con):
    bad = []
    for (entry, acct, side, cents, kind, _p, ekind, _r) in all_postings(con):
        if ekind == "processor_fee" and kind in TRUST_KINDS + (BANK_TRUST,):
            bad.append(entry)
    arith = con.execute(
        """SELECT id FROM settlement_batches
           WHERE gross_cents - fee_cents != net_cents"""
    ).fetchall()
    # trust batches must settle GROSS -- fees never netted from trust
    net_trust = con.execute(
        """SELECT b.id FROM settlement_batches b
           JOIN ledger_accounts a ON a.id = b.bank_account_id
           WHERE a.kind='trust_bank' AND b.mode != 'gross'""").fetchall()
    # linkage (deepened P3): every processor_batch event's amount equals
    # the postings booked against it on that bank account
    unlinked = []
    for ev_id, ev_bank, ev_cents, ev_dir in con.execute(
            """SELECT id, bank_account_id, amount_cents, direction
               FROM external_events WHERE event_type='processor_batch'"""):
        side = "debit" if ev_dir == "in" else "credit"
        booked = con.execute(
            """SELECT COALESCE(SUM(p.amount_cents),0)
               FROM journal_entries e
               JOIN journal_postings p ON p.entry_id = e.id
               WHERE e.external_event_id=? AND p.account_id=?
                 AND p.side=?""",
            (ev_id, ev_bank, side)).fetchone()[0]
        if booked != ev_cents:
            unlinked.append((ev_id, ev_cents, booked))
    ok = not bad and not arith and not net_trust and not unlinked
    return (ok,
            "F6 GROSS-VS-NET: %d fee-into-trust entries, %d batch "
            "arithmetic errors, %d net-mode trust batches, %d "
            "event-linkage mismatches"
            % (len(set(bad)), len(arith), len(net_trust), len(unlinked)))


def check_f7(con):
    """LIVE as of P5 (U5.2); STRENGTHENED 2026-08-07 to the real-bank
    model (James's ruling, s8 close; F7 amendment's only allowed
    direction). Per bank account with external events, run the
    three-way reconciliation at TWO period ends: mid-lag (the max
    event date, so clearing lags leave genuine reconciling items) and
    all-cleared (max date + 10 days). Asserts:
      (a) the identity holds at both periods, nothing unmatched;
      (b) every item's cause is from the closed vocabulary and
          carries a direction;
      (c) at the all-cleared period, TIMING items have resolved --
          only correction/refund items (books-only by design) may
          persist;
      (d) bank-record purity: the events linked to a payment are
          exactly its birth shape (direct 1, trust_transfer 2,
          sim 0) -- a correction that fabricated or destroyed a bank
          event is a RED, whatever the reconciliation says.
    No events at all reports NO-EVENTS (a fresh empty ledger has no
    reconciliation to prove)."""
    import reconcile
    banks = [r[0] for r in con.execute(
        "SELECT DISTINCT bank_account_id FROM external_events"
        " ORDER BY bank_account_id").fetchall()]
    if not banks:
        return (None, "F7 THREE-WAY-RECON: NO-EVENTS (nothing to"
                      " reconcile; not a pass)")
    max_day = con.execute(
        "SELECT MAX(occurred_on) FROM external_events").fetchone()[0]
    later = reconcile.bank_statement._plus_days(max_day, 10)
    known = {"deposit in transit", "outstanding disbursement",
             "correction awaiting bank", "refund awaiting bank"}
    timing = {"deposit in transit", "outstanding disbursement"}
    broken, total_items = [], 0
    bad_cause = late_timing = 0
    for b in banks:
        for period in (max_day, later):
            r = reconcile.three_way(con, b, period)
            total_items += len(r["items"])
            if not r["identity_holds"]:
                broken.append((b, period))
            for i in r["items"]:
                if i["cause"] not in known \
                        or i.get("direction") not in ("in", "out"):
                    bad_cause += 1
                if period == later and i["cause"] in timing:
                    late_timing += 1
    birth_shape = {"direct": 1, "trust_transfer": 2,
                   "sim_card": 0, "sim_echeck": 0}
    impure = []
    for pid, method, n_events in con.execute(
            """SELECT p.id, p.method, COUNT(e.id)
               FROM invoice_payments p
               LEFT JOIN external_events e ON e.payment_id = p.id
               GROUP BY p.id, p.method ORDER BY p.id"""):
        if n_events != birth_shape.get(method, -1):
            impure.append((pid, method, n_events))
    ok = (not broken and bad_cause == 0 and late_timing == 0
          and not impure)
    return (ok,
            "F7 THREE-WAY-RECON: %d accounts x 2 periods, %d reconciling"
            " items enumerated, %d identity breaks; strengthened:"
            " %d unknown-cause items, %d timing items surviving"
            " all-cleared, %d payments with fabricated/missing bank"
            " events%s"
            % (len(banks), total_items, len(broken), bad_cause,
               late_timing, len(impure),
               "" if not impure else " " + repr(impure)))


def check_f8(con):
    # (a) active probe: journal must refuse UPDATE and DELETE.
    probes_ok = True
    eid = con.execute("SELECT id FROM journal_entries LIMIT 1").fetchone()
    if eid:
        for sql in ("UPDATE journal_entries SET memo='x' WHERE id=?",
                    "DELETE FROM journal_entries WHERE id=?"):
            try:
                con.execute("SAVEPOINT f8")
                con.execute(sql, (eid[0],))
                probes_ok = False
            except sqlite3.DatabaseError:
                pass
            finally:
                con.execute("ROLLBACK TO f8")
                con.execute("RELEASE f8")
    # (b) audit sweep: no update/delete audit rows for journal tables,
    # except postings updates whose changes touch only clearing fields.
    try:
        rows = con.execute(
            """SELECT id, entity_type, action, changes FROM audit_log
               WHERE entity_type IN ('journal_entries','journal_postings')
                 AND action IN ('update','delete')"""
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []  # selftest db has no audit_log
    bad = []
    for rid, etype, action, changes in rows:
        if etype == "journal_postings" and action == "update" and changes \
           and "cleared_at" in changes:
            continue
        bad.append(rid)
    return (probes_ok and not bad,
            "F8 IMMUTABILITY: probe %s, %d forbidden audit rows"
            % ("held" if probes_ok else "FAILED", len(bad)))


def check_f9(con):
    """F9 CLOSED-PERIOD IMMUTABILITY (billing-ui period-close.md PC1;
    program amendment 2026-08-09 -- a STRENGTHENING, F1-F8 untouched):
    every closed period's ledger-side snapshot must recompute
    byte-equal today. The app-layer lock guards the recipe surface;
    this check catches ANY writer -- a money fact snuck into a closed
    month by any path shifts the recompute and goes RED. Compares the
    tie fields and reconciling items only (never display names); the
    billing-document fields are deliberately outside the lock (sheet
    element 9)."""
    try:
        rows = con.execute("SELECT period, snapshot FROM period_closes"
                           " WHERE status='closed' ORDER BY period"
                           ).fetchall()
    except sqlite3.OperationalError:
        rows = []  # pre-close schema: nothing closed, vacuously green
    import json

    import reconcile
    TIE_FIELDS = ("bank_balance_cents", "deposits_in_transit_cents",
                  "outstanding_disbursements_cents",
                  "corrections_net_cents", "book_balance_cents",
                  "sub_ledger_sum_cents", "identity_holds")
    drifted = []
    for period, snap_text in rows:
        snap = json.loads(snap_text)
        for a in snap["accounts"]:
            r = reconcile.three_way(con, a["bank_account_id"],
                                    snap["period_end"])
            live = {k: r[k] for k in TIE_FIELDS}
            live["identity_holds"] = bool(live["identity_holds"])
            frozen = {k: a[k] for k in TIE_FIELDS}
            live_items = sorted(
                ({"cause": i["cause"], "direction": i["direction"],
                  "amount_cents": i["amount_cents"], "date": i["date"],
                  "entry_id": i["entry_id"]} for i in r["items"]),
                key=lambda i: (i["date"], i["entry_id"], i["cause"]))
            if live != frozen or live_items != a["items"]:
                drifted.append("%s a%d" % (period, a["bank_account_id"]))
    return (not drifted,
            "F9 CLOSED PERIODS: %d closed, %d drifted%s"
            % (len(rows), len(drifted),
               "" if not drifted else " " + repr(drifted)))


CHECKS = [check_f1, check_f2, check_f3, check_f4, check_f5, check_f6,
          check_f7, check_f8, check_f9]


def run_suite(con):
    lines, greens, reds, stubs = [], 0, 0, 0
    for chk in CHECKS:
        ok, line = chk(con)
        if ok is None:
            stubs += 1
            lines.append(line + "  [STUB]")
        elif ok:
            greens += 1
            lines.append(line + "  [PASS]")
        else:
            reds += 1
            lines.append(line + "  [RED]")
    verdict = "GREEN" if reds == 0 and stubs == 0 else \
              ("RED" if reds else "INCOMPLETE (stubs outstanding)")
    lines.append("fiduciary: %d pass, %d red, %d stub; verdict: %s"
                 % (greens, reds, stubs, verdict))
    return reds == 0 and stubs == 0, lines


def selftest():
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys=OFF")  # draft DDL stands alone
    con.executescript(DRAFT_DDL.read_text())
    failures = []

    # 1. Empty ledger: every non-stub check must PASS.
    ok, lines = run_suite(con)
    for ln in lines:
        if "[RED]" in ln:
            failures.append("empty-ledger red: " + ln)

    # 2. Calibration: each scenario must turn its check RED.
    con.executescript("""
      INSERT INTO ledger_accounts (id,kind,name) VALUES
        (1,'trust_bank','IOLTA'), (4,'operating_bank','Operating'),
        (5,'fee_income','Fees');
      INSERT INTO ledger_accounts (id,kind,name,parent_id,contact_id)
        VALUES (2,'client_trust','Client A',1,101);
    """)
    # F1: unbalanced entry.
    con.executescript("""
      INSERT INTO journal_entries (id,kind) VALUES (1,'trust_deposit');
      INSERT INTO journal_postings (entry_id,account_id,side,amount_cents)
        VALUES (1,1,'debit',10000);
    """)
    if check_f1(con)[0]:
        failures.append("F1 failed to flag unbalanced entry")
    # F2: bank says 100.00, sub-ledger says 0.
    if check_f2(con)[0]:
        failures.append("F2 failed to flag control mismatch")
    # F5: trust_bank moved without sub-ledger leg.
    if check_f5(con)[0]:
        failures.append("F5 failed to flag missing sub-ledger leg")
    # F3: overdraft -- client sub-account debited with no funds.
    con.executescript("""
      INSERT INTO journal_entries (id,kind) VALUES (2,'disbursement');
      INSERT INTO journal_postings (entry_id,account_id,side,amount_cents)
        VALUES (2,2,'debit',5000),(2,1,'credit',5000);
    """)
    if check_f3(con)[0]:
        failures.append("F3 failed to flag overdraft")
    if check_f4(con)[0]:
        failures.append("F4 failed to flag over-available outflow")
    # F6: batch arithmetic.
    con.execute("""INSERT INTO settlement_batches
      (settle_date,bank_account_id,mode,gross_cents,fee_cents,net_cents)
      VALUES ('2026-01-01',1,'gross',10000,300,9800)""")
    if check_f6(con)[0]:
        failures.append("F6 failed to flag batch arithmetic error")
    # F8: immutability triggers must hold under direct attack.
    if not check_f8(con)[0]:
        failures.append("F8 probe: journal accepted UPDATE/DELETE")
    # Clearing exception: un-cleared -> cleared must be ALLOWED once.
    try:
        con.execute("UPDATE journal_postings SET cleared_at='2026-01-02'"
                    " WHERE entry_id=1")
    except sqlite3.DatabaseError:
        failures.append("clearing annotation was wrongly blocked")
    try:
        con.execute("UPDATE journal_postings SET cleared_at='2026-02-01'"
                    " WHERE entry_id=1")
        failures.append("re-clearing a cleared posting was wrongly allowed")
    except sqlite3.DatabaseError:
        pass

    # F9: a closed period whose frozen snapshot disagrees with the
    # live recompute must go RED (the drift IS the violation).
    con.executescript("""
      CREATE TABLE period_closes (
        id INTEGER PRIMARY KEY, period TEXT NOT NULL,
        status TEXT NOT NULL, prepared_by INTEGER, prepared_at TEXT,
        approved_by INTEGER, approved_at TEXT, snapshot TEXT NOT NULL);
    """)
    import json as _json
    _bogus = _json.dumps({"period": "2026-01", "period_end": "2026-01-31",
                          "accounts": [{"bank_account_id": 1,
                                        "bank_balance_cents": 999999,
                                        "deposits_in_transit_cents": 0,
                                        "outstanding_disbursements_cents": 0,
                                        "corrections_net_cents": 0,
                                        "book_balance_cents": 999999,
                                        "sub_ledger_sum_cents": 999999,
                                        "identity_holds": True,
                                        "items": []}]})
    con.execute("INSERT INTO period_closes (period, status, snapshot)"
                " VALUES ('2026-01','closed',?)", (_bogus,))
    if check_f9(con)[0]:
        failures.append("F9 failed to flag a drifted closed period")

    print("selftest: draft DDL instantiated; empty ledger %d/7 non-stub "
          "checks pass; calibration scenarios: %s"
          % (7, "all behaved" if not failures else "FAILURES"))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


def seeded_db():
    """Fresh in-memory db from casework schema + seed (the state
    verifier 1 runs against), PLUS the F7-lock overlay (program
    ruling 2026-08-04, billing-ui worklog s2): an amount edit, a
    full refund, and two online payments settling in ONE processor
    batch, driven through the real billing machinery. The overlay
    lives HERE, not in seed.sql, so the parity suite's seeded world
    stays exactly as sealed; this suite alone carries the stronger
    scenario."""
    casework = HERE.parent.parent / "casework"
    sys.path.insert(0, str(casework))
    from app import billing, processor
    from app import db as appdb
    con = appdb.create_db(":memory:")
    con.actor.set("system", None)
    con.executescript((casework / "seeds" / "seed.sql")
                      .read_text(encoding="utf-8"))
    d1, d2, d3 = "2026-08-04", "2026-08-05", "2026-08-06"
    iolta = con.execute("SELECT id FROM ledger_accounts WHERE"
                        " kind='trust_bank'").fetchone()[0]
    op = con.execute("SELECT id FROM ledger_accounts WHERE"
                     " kind='operating_bank'").fetchone()[0]
    b1 = billing.create_invoice(con, "bill", 1, 1, d1)
    billing.add_charge(con, b1, "service", "SYNTH corrected consult",
                       60000, 1)
    p1 = billing.record_payment(con, b1, "direct", 40000, d1, 1,
                                destination_account_id=op)
    billing.edit_payment(con, p1, 1, d2, amount_cents=55000)
    b2 = billing.create_invoice(con, "bill", 3, 1, d1)
    billing.add_charge(con, b2, "service", "SYNTH refunded consult",
                       30000, 1)
    p2 = billing.record_payment(con, b2, "direct", 30000, d1, 1,
                                destination_account_id=op)
    billing.refund_payment(con, p2, 1, d2, note="SYNTH refund")
    for i, (cid, cents) in enumerate(((1, 250000), (3, 400000))):
        tr = billing.create_invoice(con, "trust_request", cid, 1, d2,
                                    trust_level="client",
                                    trust_account_id=iolta)
        billing.add_charge(con, tr, "service",
                           "SYNTH retainer request", cents, 1)
        billing.pay_online(con, tr, "SYNTHETIC-VISA-LOCK-%d" % i,
                           "card", d2)
    processor.settle(con, d3, posted_by=1)
    return con


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    con = seeded_db() if sys.argv[1] == "--seeded" \
        else sqlite3.connect(sys.argv[1])
    ok, lines = run_suite(con)
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("report: %s" % REPORT)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
