"""Period-close engine (billing-ui period-close.md, RATIFIED
2026-08-09; program amendment same date).

The close is HARD (PC1): once a month is closed, ledger._post and
ledger.create_external_event refuse any money fact dated into it via
assert_open() below; late-arriving facts post current-dated into the
open month. The act is TWO-STEP (PC2): prepare() freezes a
canonical-JSON snapshot signed by the preparer; approve() recomputes
live and compares -- any drift voids the prepare ("stale"), a clean
match locks the month. Same person may sign both; the record shows
it. Close requires the tie (PC3): every bank account's three-way
identity must HOLD, and every reconciling item must be individually
acknowledged (ack keys) to prepare.

The tie comes from the fiduciary suite's own engine
(casework-billing/verify/reconcile.py), imported lazily the same way
app_ui/billing_ui.py imports it: the close gates on the oracle's
numbers, never a reimplementation. Lazy so the spine suite (which
never closes a month) keeps zero cross-child imports.

Months close in strict chronological order; a month is closable only
once it has ended. No reopen exists BY DESIGN (sheet element 10): a
reopen affordance would make the hard close soft in disguise.

Money is integer cents; the cash-concentration share is integer
basis points. No floats.
"""

import json
from datetime import date as _date


class PeriodError(ValueError):
    pass


# --- month arithmetic (ISO strings throughout) ------------------------

def _month_of(iso):
    return iso[:7]


def _next_month(period):
    y, m = int(period[:4]), int(period[5:7])
    return f"{y + (m == 12)}-{(m % 12) + 1:02d}"


def _month_end(period):
    first_of_next = _date.fromisoformat(_next_month(period) + "-01")
    return _date.fromordinal(first_of_next.toordinal() - 1).isoformat()


def _month_name(period):
    # '2026-07' -> 'July 2026': error text faces the driver, and the
    # driver's surface never speaks ISO
    return _date.fromisoformat(period + "-01").strftime("%B %Y")


# --- the lock (PC1) ---------------------------------------------------

def last_closed(conn):
    """Latest closed period 'YYYY-MM' or None. Strict-order closing
    makes this the whole closed set: every month <= it is closed."""
    return conn.execute("SELECT MAX(period) FROM period_closes"
                        " WHERE status='closed'").fetchone()[0]


def assert_open(conn, iso_date):
    lc = last_closed(conn)
    if lc is not None and _month_of(iso_date) <= lc:
        raise PeriodError(
            f"{_month_name(_month_of(iso_date))} is closed (hard close"
            f" through {_month_name(lc)}): post the fact current-dated"
            f" in the open month")


# --- what is closable -------------------------------------------------

def closable_month(conn, today):
    """(period, period_end) for the one closable month, or None.
    Strict order: the month after the last close; before any close,
    the earliest month carrying a money fact. Only ended months
    close (flagged judgment call, build record): period_end < today."""
    lc = last_closed(conn)
    if lc is not None:
        period = _next_month(lc)
    else:
        row = conn.execute(
            "SELECT MIN(m) FROM ("
            " SELECT MIN(substr(posted_at,1,7)) AS m FROM journal_entries"
            " UNION ALL"
            " SELECT MIN(substr(occurred_on,1,7)) FROM external_events"
            " UNION ALL"
            " SELECT MIN(substr(issued_date,1,7)) FROM invoices"
            "  WHERE issued_date IS NOT NULL AND deleted_at IS NULL"
            " UNION ALL"
            " SELECT MIN(substr(payment_date,1,7)) FROM invoice_payments"
            "  WHERE deleted_at IS NULL)").fetchone()
        period = row[0]
        if period is None:
            return None
    period_end = _month_end(period)
    if period_end >= today:
        return None
    return period, period_end


# --- the snapshot -----------------------------------------------------

def canonical(snapshot):
    return json.dumps(snapshot, sort_keys=True, separators=(",", ":"))


def item_key(bank_account_id, item):
    return "a%d|%s|%s|%d|%s|%d" % (
        bank_account_id, item["cause"], item["direction"],
        item["amount_cents"], item["date"], item["entry_id"])


def _oracle():
    import sys
    from pathlib import Path
    v = Path(__file__).resolve().parents[2] / "casework-billing" / "verify"
    if str(v) not in sys.path:
        sys.path.insert(0, str(v))
    import reconcile
    return reconcile


def compute(conn, period, period_end):
    """The full close view for one month, recomputed from scratch --
    ties per bank account (oracle engine), carried items, the five
    story figures, and the two firm-wide rankings (sheet elements
    3-6). Deterministic given the db; canonical() of the result is
    the PC2 comparison unit."""
    from app import billing, ledger
    reconcile = _oracle()

    accounts, ties_hold = [], True
    for b in ledger.list_bank_accounts(conn):
        r = reconcile.three_way(conn, b["id"], period_end)
        ties_hold = ties_hold and r["identity_holds"]
        accounts.append({
            "bank_account_id": b["id"], "name": b["name"],
            "kind": b["kind"],
            "bank_balance_cents": r["bank_balance_cents"],
            "deposits_in_transit_cents": r["deposits_in_transit_cents"],
            "outstanding_disbursements_cents":
                r["outstanding_disbursements_cents"],
            "corrections_net_cents": r["corrections_net_cents"],
            "book_balance_cents": r["book_balance_cents"],
            "sub_ledger_sum_cents": r["sub_ledger_sum_cents"],
            "identity_holds": bool(r["identity_holds"]),
            "items": sorted(
                ({"cause": i["cause"], "direction": i["direction"],
                  "amount_cents": i["amount_cents"], "date": i["date"],
                  "entry_id": i["entry_id"]} for i in r["items"]),
                key=lambda i: (i["date"], i["entry_id"], i["cause"])),
        })

    like = period + "%"
    billed = conn.execute(
        "SELECT COALESCE(SUM(c.amount_cents),0) -"
        " COALESCE((SELECT SUM(discount_cents) FROM invoices"
        "   WHERE issued_date LIKE ? AND deleted_at IS NULL),0)"
        " FROM invoice_charges c JOIN invoices i ON i.id=c.invoice_id"
        " WHERE i.issued_date LIKE ? AND i.deleted_at IS NULL"
        " AND c.deleted_at IS NULL", (like, like)).fetchone()[0]
    collected = conn.execute(
        "SELECT COALESCE(SUM(amount_cents),0) FROM invoice_payments"
        " WHERE payment_date LIKE ? AND deleted_at IS NULL",
        (like,)).fetchone()[0]
    flows = conn.execute(
        "SELECT p.side, COALESCE(SUM(p.amount_cents),0)"
        " FROM journal_postings p"
        " JOIN journal_entries e ON e.id=p.entry_id"
        " JOIN ledger_accounts a ON a.id=p.account_id"
        " WHERE a.kind='trust_bank' AND e.posted_at LIKE ?"
        " GROUP BY p.side", (like,)).fetchall()
    flow = {r[0]: r[1] for r in flows}
    earned = conn.execute(
        "SELECT COALESCE(SUM(p.amount_cents),0) FROM journal_postings p"
        " JOIN journal_entries e ON e.id=p.entry_id"
        " JOIN ledger_accounts a ON a.id=p.account_id"
        " WHERE a.kind='fee_income' AND p.side='credit'"
        " AND e.kind='earn_out' AND e.posted_at LIKE ?",
        (like,)).fetchone()[0]
    story = {"billed_cents": billed, "collected_cents": collected,
             "into_trust_cents": flow.get("debit", 0),
             "out_of_trust_cents": flow.get("credit", 0),
             "earned_from_trust_cents": earned}

    # WAY BEHIND: outstanding balance per client via the billing
    # module's own arithmetic (single source), aged at period_end.
    behind = {}
    for inv in conn.execute(
            "SELECT id, contact_id, issued_date FROM invoices"
            " WHERE issued_date IS NOT NULL AND issued_date <= ?"
            " AND deleted_at IS NULL ORDER BY id", (period_end,)):
        bal = billing.invoice_balance(conn, inv["id"])
        if bal <= 0:
            continue
        c = behind.setdefault(inv["contact_id"],
                              {"outstanding_cents": 0,
                               "oldest_issued": inv["issued_date"]})
        c["outstanding_cents"] += bal
        c["oldest_issued"] = min(c["oldest_issued"], inv["issued_date"])
    pe_ord = _date.fromisoformat(period_end).toordinal()
    way_behind = sorted(
        ({"contact_id": cid, "name": _name(conn, cid),
          "outstanding_cents": v["outstanding_cents"],
          "oldest_issued": v["oldest_issued"],
          "age_days": pe_ord -
              _date.fromisoformat(v["oldest_issued"]).toordinal()}
         for cid, v in behind.items()),
        key=lambda r: (-r["outstanding_cents"], r["contact_id"]))

    # KEEPS US IN CASH: collections by client, trailing three months
    # (the close month and the two before), share in basis points.
    start = period
    for _ in range(2):
        y, m = int(start[:4]), int(start[5:7])
        start = f"{y - (m == 1)}-{(m - 2) % 12 + 1:02d}"
    rows = conn.execute(
        "SELECT i.contact_id, COALESCE(SUM(p.amount_cents),0) AS c"
        " FROM invoice_payments p JOIN invoices i ON i.id=p.invoice_id"
        " WHERE p.deleted_at IS NULL AND substr(p.payment_date,1,7) >= ?"
        " AND p.payment_date <= ? GROUP BY i.contact_id",
        (start, period_end)).fetchall()
    total = sum(r["c"] for r in rows)
    keeps = sorted(
        ({"contact_id": r["contact_id"], "name": _name(conn, r["contact_id"]),
          "collected_cents": r["c"],
          "share_bp": (r["c"] * 10000) // total if total else 0}
         for r in rows if r["c"] > 0),
        key=lambda x: (-x["collected_cents"], x["contact_id"]))

    return {"period": period, "period_end": period_end,
            "accounts": accounts, "ties_hold": bool(ties_hold),
            "story": story, "way_behind": way_behind,
            "keeps_in_cash": keeps}


def _name(conn, contact_id):
    row = conn.execute("SELECT display_name FROM contacts WHERE id=?",
                       (contact_id,)).fetchone()
    return row["display_name"] if row else f"contact {contact_id}"


def required_acks(snapshot):
    return {item_key(a["bank_account_id"], i)
            for a in snapshot["accounts"] for i in a["items"]}


# --- the act (PC2 + PC3) ----------------------------------------------

def get_row(conn, period, statuses=("prepared", "closed")):
    q = ",".join("?" * len(statuses))
    return conn.execute(
        f"SELECT * FROM period_closes WHERE period=? AND status IN ({q})"
        " ORDER BY id DESC LIMIT 1", (period, *statuses)).fetchone()


def list_closed(conn):
    return conn.execute("SELECT * FROM period_closes WHERE"
                        " status='closed' ORDER BY period").fetchall()


def prepare(conn, user_id, on_date, acks):
    """PC3 gate + snapshot freeze. acks is the set of item_key()
    strings the preparer acknowledged; it must equal the recomputed
    item set exactly -- an item that appeared since the review was
    rendered fails loud, never closes silently."""
    closable = closable_month(conn, on_date)
    if closable is None:
        raise PeriodError("no month is closable")
    period, period_end = closable
    snap = compute(conn, period, period_end)
    if not snap["ties_hold"]:
        broken = [a["name"] for a in snap["accounts"]
                  if not a["identity_holds"]]
        raise PeriodError("cannot close %s: reconciliation broken for %s"
                          % (_month_name(period), ", ".join(broken)))
    required = required_acks(snap)
    if set(acks) != required:
        raise PeriodError(
            "carried items and acknowledgments differ (%d acknowledged,"
            " %d required) -- re-review the close page"
            % (len(set(acks)), len(required)))
    prior = get_row(conn, period, statuses=("prepared",))
    if prior is not None:
        conn.execute("UPDATE period_closes SET status='void' WHERE id=?",
                     (prior["id"],))
    conn.execute(
        "INSERT INTO period_closes (period, status, prepared_by,"
        " prepared_at, snapshot) VALUES (?,?,?,?,?)",
        (period, "prepared", user_id, on_date, canonical(snap)))
    return snap


def approve(conn, user_id, on_date):
    """PC2 second signature. Recomputes live and compares canonical
    JSON against the frozen snapshot: drift voids the prepare (a
    posting landed mid-review; nobody approves numbers nobody saw);
    a clean match locks the month."""
    closable = closable_month(conn, on_date)
    if closable is None:
        raise PeriodError("no month is closable")
    period, period_end = closable
    row = get_row(conn, period, statuses=("prepared",))
    if row is None:
        raise PeriodError(f"{_month_name(period)} has no prepared close"
                          f" to approve")
    fresh = canonical(compute(conn, period, period_end))
    if fresh != row["snapshot"]:
        conn.execute("UPDATE period_closes SET status='void' WHERE id=?",
                     (row["id"],))
        raise PeriodError(
            f"stale prepare for {_month_name(period)}: the numbers moved"
            " since it was prepared -- the prepare is void, re-prepare"
            " from the close page")
    conn.execute(
        "UPDATE period_closes SET status='closed', approved_by=?,"
        " approved_at=? WHERE id=?", (user_id, on_date, row["id"]))
    return get_row(conn, period, statuses=("closed",))
