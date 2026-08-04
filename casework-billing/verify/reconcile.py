"""Three-way reconciliation engine (P5 U5.2; goal.md F7).

Per bank account, at a period end:

    bank closing balance
  + deposits in transit          (occurred, not yet cleared, IN)
  - outstanding disbursements    (occurred, not yet cleared, OUT)
  = book balance                 (journal postings through period_end)
  = sub-ledger sum               (trust accounts only: client claims)

Every reconciling item is enumerated with a cause -- no plug. The
statement side comes from bank_statement.py (events only); the book
side reads the journal. Matching: statement lines match book postings
by entry linkage (external_event_id) where settlements carry it, else
by (bank account, business date, direction-side, amount) -- exact in
the deterministic synthetic world. Unmatched lines or postings are
discrepancies and fail the reconciliation.
"""

import bank_statement


def _book_postings(conn, bank_account_id, period_end):
    """Bank-account postings through period_end, with direction from
    the account's debit-normal convention (banks are assets)."""
    rows = conn.execute(
        """SELECT p.id, p.entry_id, p.side, p.amount_cents, e.posted_at,
                  e.kind, e.external_event_id, e.reverses_entry_id
           FROM journal_postings p JOIN journal_entries e ON e.id=p.entry_id
           WHERE p.account_id=? AND e.posted_at <= ?
           ORDER BY p.entry_id, p.id""",
        (bank_account_id, period_end)).fetchall()
    return [{"posting_id": r[0], "entry_id": r[1],
             "direction": "in" if r[2] == "debit" else "out",
             "amount_cents": r[3], "date": r[4], "kind": r[5],
             "event_id": r[6], "reverses": r[7]} for r in rows]


def _sub_ledger_sum(conn, bank_account_id):
    total = 0
    stack = [bank_account_id]
    while stack:
        parent = stack.pop()
        for r in conn.execute(
                "SELECT id FROM ledger_accounts WHERE parent_id=?",
                (parent,)).fetchall():
            stack.append(r[0])
            d, c = conn.execute(
                "SELECT COALESCE(SUM(CASE WHEN side='debit' THEN"
                " amount_cents ELSE 0 END),0),"
                " COALESCE(SUM(CASE WHEN side='credit' THEN amount_cents"
                " ELSE 0 END),0) FROM journal_postings WHERE account_id=?",
                (r[0],)).fetchone()
            total += c - d  # liability sub-accounts are credit-normal
    return total


def three_way(conn, bank_account_id, period_end):
    stmt = bank_statement.statement(conn, bank_account_id, period_end)
    book = _book_postings(conn, bank_account_id, period_end)
    book_balance = sum(p["amount_cents"] if p["direction"] == "in"
                       else -p["amount_cents"] for p in book)

    # matching: linkage first (a batch event may cover SEVERAL
    # postings -- one processor deposit, n settled payments; program
    # ruling 2026-08-04, billing-ui worklog s2 finding 2 -- so the
    # linked GROUP matches iff its signed sum equals the line), then
    # exact (date, direction, amount)
    unmatched_postings = list(book)
    matched, unmatched_lines = [], []

    def _signed(amount, direction):
        return amount if direction == "in" else -amount

    for line in stmt["lines"]:
        group = [p for p in unmatched_postings
                 if p["event_id"] == line["event_id"]]
        if group and sum(_signed(p["amount_cents"], p["direction"])
                         for p in group) == _signed(
                             line["amount_cents"], line["direction"]):
            for p in group:
                unmatched_postings.remove(p)
                matched.append((line, p))
            continue
        hit = next((p for p in unmatched_postings
                    if p["date"] == line["occurred_on"]
                    and p["direction"] == line["direction"]
                    and p["amount_cents"] == line["amount_cents"]),
                   None)
        if hit is None:
            unmatched_lines.append(line)
        else:
            unmatched_postings.remove(hit)
            matched.append((line, hit))
    # postings left unmatched must be exactly the not-yet-cleared
    # events. Linkage groups first, same n:1 rule as cleared lines --
    # one uncleared batch event may cover several postings.
    items = []
    still_unmatched = []
    for pend in list(stmt["pending"]):
        group = [p for p in unmatched_postings
                 if p["event_id"] == pend["event_id"]]
        if group and sum(_signed(p["amount_cents"], p["direction"])
                         for p in group) == _signed(
                             pend["amount_cents"], pend["direction"]):
            stmt["pending"].remove(pend)
            for p in group:
                unmatched_postings.remove(p)
                cause = ("deposit in transit" if p["direction"] == "in"
                         else "outstanding disbursement")
                items.append({"cause": cause,
                              "amount_cents": p["amount_cents"],
                              "date": p["date"], "entry_id": p["entry_id"]})
    for p in unmatched_postings:
        pend = next((q for q in stmt["pending"]
                     if q["occurred_on"] == p["date"]
                     and q["direction"] == p["direction"]
                     and q["amount_cents"] == p["amount_cents"]),
                    None)
        if pend is None:
            still_unmatched.append(p)
        else:
            stmt["pending"].remove(pend)
            cause = ("deposit in transit" if p["direction"] == "in"
                     else "outstanding disbursement")
            items.append({"cause": cause, "amount_cents": p["amount_cents"],
                          "date": p["date"], "entry_id": p["entry_id"]})

    dit = sum(i["amount_cents"] for i in items
              if i["cause"] == "deposit in transit")
    outstanding = sum(i["amount_cents"] for i in items
                      if i["cause"] == "outstanding disbursement")
    identity = stmt["closing_balance_cents"] + dit - outstanding \
        == book_balance
    kind = conn.execute("SELECT kind FROM ledger_accounts WHERE id=?",
                        (bank_account_id,)).fetchone()[0]
    sub_sum = _sub_ledger_sum(conn, bank_account_id) \
        if kind == "trust_bank" else None
    sub_ok = (sub_sum == book_balance) if sub_sum is not None else True
    return {"bank_account_id": bank_account_id, "period_end": period_end,
            "bank_balance_cents": stmt["closing_balance_cents"],
            "deposits_in_transit_cents": dit,
            "outstanding_disbursements_cents": outstanding,
            "book_balance_cents": book_balance,
            "sub_ledger_sum_cents": sub_sum,
            "items": items, "matched": len(matched),
            "unmatched_statement_lines": unmatched_lines,
            "unmatched_book_postings": still_unmatched,
            "identity_holds": identity and sub_ok
            and not unmatched_lines and not still_unmatched}


def report_lines(recon):
    out = ["account %d period %s: bank %d + DIT %d - outstanding %d ="
           " book %d%s -> %s"
           % (recon["bank_account_id"], recon["period_end"],
              recon["bank_balance_cents"],
              recon["deposits_in_transit_cents"],
              recon["outstanding_disbursements_cents"],
              recon["book_balance_cents"],
              ("" if recon["sub_ledger_sum_cents"] is None
               else " = subledger %d" % recon["sub_ledger_sum_cents"]),
              "HOLDS" if recon["identity_holds"] else "BROKEN")]
    for i in recon["items"]:
        out.append("  item: %s %d (%s, entry %d)"
                   % (i["cause"], i["amount_cents"], i["date"],
                      i["entry_id"]))
    for l in recon["unmatched_statement_lines"]:
        out.append("  UNMATCHED LINE: %r" % (l,))
    for p in recon["unmatched_book_postings"]:
        out.append("  UNMATCHED POSTING: %r" % (p,))
    return out
