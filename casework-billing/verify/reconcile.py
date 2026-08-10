"""Three-way reconciliation engine (P5 U5.2; goal.md F7).

REAL-BANK MATCHING (James's ruling 2026-08-07 s8, superseding the
2026-08-04 mirror-event design; the amendment's authorization still
governs the files): the bank record holds exactly what the bank saw,
corrections and refunds live in the books only. The engine MATCHES
statement lines to book postings and EXPLAINS every difference as a
reconciling item with a cause -- no plug. Per bank account, at a
period end:

    bank closing balance
  + deposits in transit          (occurred, not yet cleared, IN)
  - outstanding disbursements    (occurred, not yet cleared, OUT)
  +/- corrections awaiting bank  (books corrected; bank unchanged)
  = book balance                 (journal postings through period_end)
  = sub-ledger sum               (trust accounts only: client claims)

Matching stages, per account and period:
  A. entry linkage (external_event_id): a settlement-batch line
     matches its linked postings iff the group's signed sum equals
     the line (n:1; program ruling 2026-08-04).
  B. exact (business date, direction, amount); when several postings
     qualify, prefer the one payment-linked to the line, then
     originals over correction entries.
  C. pending events (occurred, not yet cleared) against remaining
     postings, same linkage-then-exact rules -> timing items
     ("deposit in transit" / "outstanding disbursement").
  D. correction families: remaining postings grouped by payment (a
     reversal joins its reversed entry's payment; a repost carries
     its own) or, without one, by reversal/replacement lineage. Each
     family's net book effect is explained as one item -- cause
     "correction awaiting bank" (repost present) or "refund awaiting
     bank" (payment reversal without repost). A family netting to
     zero (e.g. a date-only edit) matches clean, no item.

Anything still unmatched -- statement lines the books cannot
explain, book postings no cause covers -- breaks the identity.
Every item carries cause, direction, amount, date, and entry.

The statement side comes from bank_statement.py (events only); the
book side reads the journal.
"""

import bank_statement


def _signed(amount, direction):
    return amount if direction == "in" else -amount


def _book_postings(conn, bank_account_id, period_end):
    """Bank-account postings through period_end, with direction from
    the account's debit-normal convention (banks are assets)."""
    rows = conn.execute(
        """SELECT p.id, p.entry_id, p.side, p.amount_cents, e.posted_at,
                  e.kind, e.external_event_id, e.reverses_entry_id,
                  e.replaces_entry_id, e.payment_id
           FROM journal_postings p JOIN journal_entries e ON e.id=p.entry_id
           WHERE p.account_id=? AND e.posted_at <= ?
           ORDER BY p.entry_id, p.id""",
        (bank_account_id, period_end)).fetchall()
    return [{"posting_id": r[0], "entry_id": r[1],
             "direction": "in" if r[2] == "debit" else "out",
             "amount_cents": r[3], "date": r[4], "kind": r[5],
             "event_id": r[6], "reverses": r[7], "replaces": r[8],
             "payment_id": r[9]} for r in rows]


def _sub_ledger_sum(conn, bank_account_id, period_end):
    """Client claims AS OF period_end -- all three legs of the
    identity must be stated at the same date. (Fixed 2026-08-09 with
    the period-close build: the unfiltered sum was latent-correct
    only because suites reconciled at period ends covering all
    activity; a retrospective recompute -- closing July from August,
    F9's drift check -- needs the claims leg dated like the others.)"""
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
                " ELSE 0 END),0) FROM journal_postings p"
                " JOIN journal_entries e ON e.id=p.entry_id"
                " WHERE p.account_id=? AND e.posted_at <= ?",
                (r[0], period_end)).fetchone()
            total += c - d  # liability sub-accounts are credit-normal
    return total


def _is_correction(p):
    return p["reverses"] is not None or p["replaces"] is not None


def _family_keys(book):
    """posting_id -> (payment_id or None, lineage-root entry id). A
    reversal/repost belongs to the entry it reverses/replaces; chains
    (edit after edit) collapse to the terminal original, and a
    correction entry without its own payment_id inherits the root's."""
    parent, payment_of = {}, {}
    for p in book:
        e = p["entry_id"]
        payment_of[e] = p["payment_id"]
        target = p["reverses"] if p["reverses"] is not None \
            else p["replaces"]
        if target is not None:
            parent[e] = target

    def root(e):
        seen = set()
        while e in parent and e not in seen:
            seen.add(e)
            e = parent[e]
        return e

    fam = {}
    for p in book:
        r = root(p["entry_id"])
        pay = p["payment_id"] if p["payment_id"] is not None \
            else payment_of.get(r)
        fam[p["posting_id"]] = (pay, r)
    return fam


def _timing_item(p):
    cause = ("deposit in transit" if p["direction"] == "in"
             else "outstanding disbursement")
    return {"cause": cause, "direction": p["direction"],
            "amount_cents": p["amount_cents"], "date": p["date"],
            "entry_id": p["entry_id"]}


def three_way(conn, bank_account_id, period_end):
    stmt = bank_statement.statement(conn, bank_account_id, period_end)
    book = _book_postings(conn, bank_account_id, period_end)
    book_balance = sum(_signed(p["amount_cents"], p["direction"])
                       for p in book)
    fam = _family_keys(book)

    unmatched = list(book)
    matched, unmatched_lines, items = [], [], []

    def _linkage_group(event_id, target_signed):
        group = [p for p in unmatched if p["event_id"] == event_id]
        if group and sum(_signed(p["amount_cents"], p["direction"])
                         for p in group) == target_signed:
            return group
        return None

    # A: entry linkage, then B: exact with preference, over cleared lines
    for line in stmt["lines"]:
        group = _linkage_group(line["event_id"],
                               _signed(line["amount_cents"],
                                       line["direction"]))
        if group:
            for p in group:
                unmatched.remove(p)
                matched.append((line, p))
            continue
        cands = [p for p in unmatched
                 if p["date"] == line["occurred_on"]
                 and p["direction"] == line["direction"]
                 and p["amount_cents"] == line["amount_cents"]]
        cands.sort(key=lambda p: (
            0 if (line["payment_id"] is not None
                  and fam[p["posting_id"]][0] == line["payment_id"]) else 1,
            1 if _is_correction(p) else 0,
            p["posting_id"]))
        if cands:
            hit = cands[0]
            unmatched.remove(hit)
            matched.append((line, hit))
        else:
            unmatched_lines.append(line)

    # C: pending events -> timing items. Linkage groups first (one
    # uncleared batch event may cover several postings), then exact.
    for pend in list(stmt["pending"]):
        group = _linkage_group(pend["event_id"],
                               _signed(pend["amount_cents"],
                                       pend["direction"]))
        if group:
            stmt["pending"].remove(pend)
            for p in group:
                unmatched.remove(p)
                items.append(_timing_item(p))
    for p in list(unmatched):
        pend = next((q for q in stmt["pending"]
                     if q["occurred_on"] == p["date"]
                     and q["direction"] == p["direction"]
                     and q["amount_cents"] == p["amount_cents"]),
                    None)
        if pend is not None:
            stmt["pending"].remove(pend)
            unmatched.remove(p)
            items.append(_timing_item(p))

    # D: correction families over whatever the bank cannot show.
    families = {}
    still_unmatched = []
    for p in unmatched:
        pay, lineage_root = fam[p["posting_id"]]
        if pay is not None:
            families.setdefault(("pay", pay), []).append(p)
        elif _is_correction(p):
            families.setdefault(("root", lineage_root), []).append(p)
        else:
            still_unmatched.append(p)
    for key, group in sorted(families.items(),
                             key=lambda kv: kv[1][0]["posting_id"]):
        has_repost = any(p["replaces"] is not None for p in group)
        has_reversal = any(p["reverses"] is not None for p in group)
        if not (has_repost or has_reversal):
            # payment-linked postings with no correction structure and
            # no bank line -- nothing explains them
            still_unmatched.extend(group)
            continue
        net = sum(_signed(p["amount_cents"], p["direction"])
                  for p in group)
        anchor = max((p for p in group if _is_correction(p)),
                     key=lambda p: p["entry_id"])
        for p in group:
            matched.append((None, p))
        if net == 0:
            continue  # books correction nets to zero: clean, no item
        cause = ("correction awaiting bank" if has_repost
                 else "refund awaiting bank" if key[0] == "pay"
                 else "correction awaiting bank")
        items.append({"cause": cause,
                      "direction": "in" if net > 0 else "out",
                      "amount_cents": abs(net), "date": anchor["date"],
                      "entry_id": anchor["entry_id"]})

    dit = sum(i["amount_cents"] for i in items
              if i["cause"] == "deposit in transit")
    outstanding = sum(i["amount_cents"] for i in items
                      if i["cause"] == "outstanding disbursement")
    corrections_net = sum(_signed(i["amount_cents"], i["direction"])
                          for i in items
                          if i["cause"] not in ("deposit in transit",
                                                "outstanding disbursement"))
    identity = stmt["closing_balance_cents"] + dit - outstanding \
        + corrections_net == book_balance
    kind = conn.execute("SELECT kind FROM ledger_accounts WHERE id=?",
                        (bank_account_id,)).fetchone()[0]
    sub_sum = _sub_ledger_sum(conn, bank_account_id, period_end) \
        if kind == "trust_bank" else None
    sub_ok = (sub_sum == book_balance) if sub_sum is not None else True
    return {"bank_account_id": bank_account_id, "period_end": period_end,
            "bank_balance_cents": stmt["closing_balance_cents"],
            "deposits_in_transit_cents": dit,
            "outstanding_disbursements_cents": outstanding,
            "corrections_net_cents": corrections_net,
            "book_balance_cents": book_balance,
            "sub_ledger_sum_cents": sub_sum,
            "items": items, "matched": len(matched),
            "unmatched_statement_lines": unmatched_lines,
            "unmatched_book_postings": still_unmatched,
            "identity_holds": identity and sub_ok
            and not unmatched_lines and not still_unmatched}


def report_lines(recon):
    out = ["account %d period %s: bank %d + DIT %d - outstanding %d"
           " %+d corrections = book %d%s -> %s"
           % (recon["bank_account_id"], recon["period_end"],
              recon["bank_balance_cents"],
              recon["deposits_in_transit_cents"],
              recon["outstanding_disbursements_cents"],
              recon["corrections_net_cents"],
              recon["book_balance_cents"],
              ("" if recon["sub_ledger_sum_cents"] is None
               else " = subledger %d" % recon["sub_ledger_sum_cents"]),
              "HOLDS" if recon["identity_holds"] else "BROKEN")]
    for i in recon["items"]:
        out.append("  item: %s %s %d (%s, entry %d)"
                   % (i["cause"], i["direction"], i["amount_cents"],
                      i["date"], i["entry_id"]))
    for l in recon["unmatched_statement_lines"]:
        out.append("  UNMATCHED LINE: %r" % (l,))
    for p in recon["unmatched_book_postings"]:
        out.append("  UNMATCHED POSTING: %r" % (p,))
    return out
