"""Trust-shaped ledger engine (casework-billing child, P1 U1.1).

Paper design: ../casework-billing/design/ledger-design.md (P0 gate
ratified 2026-08-03). Client funds are LIABILITIES: client_trust /
matter_trust sub-accounts sit under a trust_bank control account, so
the fiduciary identity (bank balance == sum of client claims) is
double-entry arithmetic, not application discipline.

The RECIPE functions are the ONLY posting surface -- there is no
free-form posting entry point. Every recipe:
- posts one balanced journal entry (debits == credits, asserted),
- blocks overdraft/over-available BEFORE write (F3/F4; the fiduciary
  verifier re-proves the same facts after the fact),
- conforms to its allowed account-kind set (F5; RECIPE_ACCOUNT_KINDS
  is the authority, cross-checked against the verifier's copy by a
  drift-guard test in ../casework-billing/tests/),
- co-writes the external event the bank will witness (F7 substrate).

posted_at carries the caller-supplied business date (deterministic
seeds and tests); wall-clock truth lives in the audit trail. The
journal is append-only at the schema layer; corrections go through
reverse_entry(), never UPDATE.
"""

RECIPE_ACCOUNT_KINDS = {
    "trust_deposit":       {"trust_bank", "client_trust", "matter_trust"},
    "bill_direct_payment": {"operating_bank", "fee_income"},
    "earn_out":            {"trust_bank", "client_trust", "matter_trust",
                            "operating_bank", "fee_income"},
    "disbursement":        {"trust_bank", "client_trust", "matter_trust"},
    "sim_settlement":      {"trust_bank", "client_trust", "matter_trust",
                            "operating_bank", "fee_income"},
    "processor_fee":       {"processor_fee_expense", "operating_bank"},
    "chargeback":          {"chargeback_expense", "operating_bank"},
}

DEBIT_NORMAL = ("operating_bank", "trust_bank", "processor_fee_expense",
                "chargeback_expense")
SUB_KINDS = ("client_trust", "matter_trust")
BANK_KINDS = ("operating_bank", "trust_bank")


class LedgerError(ValueError):
    pass


# --- accounts ---------------------------------------------------------

def create_bank_account(conn, kind, name, created_by):
    if kind not in BANK_KINDS:
        raise LedgerError(f"not a bank account kind: {kind}")
    cur = conn.execute(
        "INSERT INTO ledger_accounts (kind, name, created_by) VALUES (?,?,?)",
        (kind, name, created_by))
    return cur.lastrowid


def list_bank_accounts(conn):
    rows = conn.execute(
        "SELECT id, kind, name FROM ledger_accounts WHERE kind IN (?,?)"
        " AND deleted_at IS NULL ORDER BY id", BANK_KINDS).fetchall()
    return [{"id": r["id"], "kind": r["kind"], "name": r["name"],
             "balance_cents": account_balance(conn, r["id"])} for r in rows]


def _account_kind(conn, account_id):
    row = conn.execute("SELECT kind FROM ledger_accounts WHERE id=?",
                       (account_id,)).fetchone()
    if row is None:
        raise LedgerError(f"no such account: {account_id}")
    return row["kind"]


def account_balance(conn, account_id):
    """Balance in the account's natural sign, own postings only."""
    kind = _account_kind(conn, account_id)
    row = conn.execute(
        "SELECT SUM(CASE WHEN side='debit' THEN amount_cents ELSE 0 END),"
        " SUM(CASE WHEN side='credit' THEN amount_cents ELSE 0 END)"
        " FROM journal_postings WHERE account_id=?", (account_id,)).fetchone()
    d, c = row[0] or 0, row[1] or 0
    return (d - c) if kind in DEBIT_NORMAL else (c - d)


def ensure_client_trust(conn, trust_bank_id, contact_id):
    """Get-or-create the client-level sub-account under a trust bank.
    Name is a mechanical key, never a copied display name (views join
    contacts for labels -- single fact store)."""
    if _account_kind(conn, trust_bank_id) != "trust_bank":
        raise LedgerError("client sub-accounts live under a trust_bank")
    row = conn.execute(
        "SELECT id FROM ledger_accounts WHERE kind='client_trust'"
        " AND parent_id=? AND contact_id=? AND deleted_at IS NULL",
        (trust_bank_id, contact_id)).fetchone()
    if row:
        return row["id"]
    cur = conn.execute(
        "INSERT INTO ledger_accounts (kind, name, parent_id, contact_id)"
        " VALUES ('client_trust', ?, ?, ?)",
        (f"client_trust:{contact_id}", trust_bank_id, contact_id))
    return cur.lastrowid


def ensure_matter_trust(conn, trust_bank_id, matter_id):
    """Matter-level sub-account, child of the matter's client sub-account
    (ledger-design.md section 1 tree)."""
    m = conn.execute("SELECT primary_contact_id FROM matters WHERE id=?",
                     (matter_id,)).fetchone()
    if m is None:
        raise LedgerError(f"no such matter: {matter_id}")
    client_acct = ensure_client_trust(conn, trust_bank_id,
                                      m["primary_contact_id"])
    row = conn.execute(
        "SELECT id FROM ledger_accounts WHERE kind='matter_trust'"
        " AND parent_id=? AND matter_id=? AND deleted_at IS NULL",
        (client_acct, matter_id)).fetchone()
    if row:
        return row["id"]
    cur = conn.execute(
        "INSERT INTO ledger_accounts (kind, name, parent_id, matter_id)"
        " VALUES ('matter_trust', ?, ?, ?)",
        (f"matter_trust:{matter_id}", client_acct, matter_id))
    return cur.lastrowid


def ensure_income_account(conn):
    row = conn.execute("SELECT id FROM ledger_accounts WHERE"
                       " kind='fee_income' AND deleted_at IS NULL").fetchone()
    if row:
        return row["id"]
    return conn.execute("INSERT INTO ledger_accounts (kind, name)"
                        " VALUES ('fee_income','Fee Income')").lastrowid


def _resolve_sub(conn, trust_bank_id, contact_id, matter_id):
    """The corpus holds funds at client level OR matter level (fx-0061,
    fx-0065); the two pots are distinct."""
    if matter_id is not None:
        return ensure_matter_trust(conn, trust_bank_id, matter_id)
    if contact_id is not None:
        return ensure_client_trust(conn, trust_bank_id, contact_id)
    raise LedgerError("trust recipes need a contact_id or matter_id")


# --- posting core (module-internal) -----------------------------------

def _post(conn, kind, legs, posted_by, posted_at, memo=None,
          invoice_id=None, payment_id=None, external_events=(),
          reverses_entry_id=None, replaces_entry_id=None,
          allowed_kinds=None, external_event_id=None):
    debits = sum(c for _a, s, c in legs if s == "debit")
    credits = sum(c for _a, s, c in legs if s == "credit")
    if debits != credits:
        raise LedgerError(f"unbalanced {kind}: {debits} != {credits}")
    kinds = {_account_kind(conn, a) for a, _s, _c in legs}
    allowed = allowed_kinds if allowed_kinds is not None \
        else RECIPE_ACCOUNT_KINDS.get(kind)
    if allowed is None or not kinds <= allowed:
        raise LedgerError(f"recipe conformance: {sorted(kinds)} not allowed"
                          f" for {kind}")
    # F3/F4 blocks BEFORE write: no sub-account or trust bank may go
    # negative from this entry's outflows.
    for acct, side, cents in legs:
        akind = _account_kind(conn, acct)
        outflow = (akind in SUB_KINDS and side == "debit") or \
                  (akind == "trust_bank" and side == "credit")
        if outflow and account_balance(conn, acct) < cents:
            raise LedgerError(
                f"insufficient funds: account {acct} has "
                f"{account_balance(conn, acct)}, entry needs {cents}")
    conn.execute("SAVEPOINT ledger_post")
    try:
        cur = conn.execute(
            "INSERT INTO journal_entries (kind, memo, invoice_id,"
            " payment_id, external_event_id, reverses_entry_id,"
            " replaces_entry_id, posted_at, posted_by)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (kind, memo, invoice_id, payment_id, external_event_id,
             reverses_entry_id, replaces_entry_id, posted_at, posted_by))
        entry_id = cur.lastrowid
        for acct, side, cents in legs:
            conn.execute(
                "INSERT INTO journal_postings (entry_id, account_id, side,"
                " amount_cents) VALUES (?,?,?,?)", (entry_id, acct, side, cents))
        for ev in external_events:
            conn.execute(
                "INSERT INTO external_events (event_type, bank_account_id,"
                " occurred_on, amount_cents, direction, counterparty, memo,"
                " invoice_id, payment_id) VALUES (?,?,?,?,?,?,?,?,?)",
                (ev["event_type"], ev["bank_account_id"], ev["occurred_on"],
                 ev["amount_cents"], ev["direction"], ev.get("counterparty"),
                 ev.get("memo"), invoice_id, payment_id))
    except Exception:
        conn.execute("ROLLBACK TO ledger_post")
        conn.execute("RELEASE ledger_post")
        raise
    conn.execute("RELEASE ledger_post")
    return entry_id


# --- recipes ----------------------------------------------------------

def record_trust_deposit(conn, trust_bank_id, amount_cents, date, posted_by,
                         contact_id=None, matter_id=None, memo=None,
                         invoice_id=None, payment_id=None,
                         replaces_entry_id=None):
    sub = _resolve_sub(conn, trust_bank_id, contact_id, matter_id)
    return _post(conn, "trust_deposit",
                 [(trust_bank_id, "debit", amount_cents),
                  (sub, "credit", amount_cents)],
                 posted_by, date, memo=memo, invoice_id=invoice_id,
                 payment_id=payment_id,
                 replaces_entry_id=replaces_entry_id,
                 external_events=[{"event_type": "deposit",
                                   "bank_account_id": trust_bank_id,
                                   "occurred_on": date,
                                   "amount_cents": amount_cents,
                                   "direction": "in", "memo": memo}])


def disburse(conn, trust_bank_id, amount_cents, date, posted_by,
             contact_id=None, matter_id=None, counterparty=None, memo=None):
    """Disburse Funds (fx-0074): offline payment to a third party from a
    client's or matter's trust funds."""
    sub = _resolve_sub(conn, trust_bank_id, contact_id, matter_id)
    return _post(conn, "disbursement",
                 [(sub, "debit", amount_cents),
                  (trust_bank_id, "credit", amount_cents)],
                 posted_by, date, memo=memo,
                 external_events=[{"event_type": "check_cut",
                                   "bank_account_id": trust_bank_id,
                                   "occurred_on": date,
                                   "amount_cents": amount_cents,
                                   "direction": "out",
                                   "counterparty": counterparty,
                                   "memo": memo}])


def earn_out(conn, trust_bank_id, operating_id, amount_cents, date,
             posted_by, contact_id=None, matter_id=None, memo=None,
             invoice_id=None, payment_id=None, replaces_entry_id=None):
    """Pay a bill from trust (fx-0066): the earn-out transfer, one atomic
    4-leg entry -- client claim down, trust down, operating up, fee
    earned (ledger-design.md section 4)."""
    if _account_kind(conn, operating_id) != "operating_bank":
        raise LedgerError("earn_out settles into an operating_bank account")
    sub = _resolve_sub(conn, trust_bank_id, contact_id, matter_id)
    fee = ensure_income_account(conn)
    return _post(conn, "earn_out",
                 [(sub, "debit", amount_cents),
                  (trust_bank_id, "credit", amount_cents),
                  (operating_id, "debit", amount_cents),
                  (fee, "credit", amount_cents)],
                 posted_by, date, memo=memo, invoice_id=invoice_id,
                 payment_id=payment_id,
                 replaces_entry_id=replaces_entry_id,
                 external_events=[
                     {"event_type": "check_cut",
                      "bank_account_id": trust_bank_id, "occurred_on": date,
                      "amount_cents": amount_cents, "direction": "out",
                      "counterparty": "firm operating", "memo": memo},
                     {"event_type": "deposit",
                      "bank_account_id": operating_id, "occurred_on": date,
                      "amount_cents": amount_cents, "direction": "in",
                      "memo": memo}])


def record_bill_direct_payment(conn, operating_id, amount_cents, date,
                               posted_by, memo=None, invoice_id=None,
                               payment_id=None, replaces_entry_id=None):
    if _account_kind(conn, operating_id) != "operating_bank":
        raise LedgerError("direct bill payments land in operating_bank")
    fee = ensure_income_account(conn)
    return _post(conn, "bill_direct_payment",
                 [(operating_id, "debit", amount_cents),
                  (fee, "credit", amount_cents)],
                 posted_by, date, memo=memo, invoice_id=invoice_id,
                 payment_id=payment_id,
                 replaces_entry_id=replaces_entry_id,
                 external_events=[{"event_type": "deposit",
                                   "bank_account_id": operating_id,
                                   "occurred_on": date,
                                   "amount_cents": amount_cents,
                                   "direction": "in", "memo": memo}])


def reverse_entry(conn, entry_id, posted_by, date, memo=None):
    """Post the mirror of an entry (r2: corrections never UPDATE). The
    reversal is availability-checked like any entry: reversing a deposit
    whose funds were already spent must fail, not overdraw."""
    entry = conn.execute("SELECT * FROM journal_entries WHERE id=?",
                         (entry_id,)).fetchone()
    if entry is None:
        raise LedgerError(f"no such entry: {entry_id}")
    legs = [(r["account_id"],
             "credit" if r["side"] == "debit" else "debit",
             r["amount_cents"])
            for r in conn.execute("SELECT * FROM journal_postings"
                                  " WHERE entry_id=?", (entry_id,))]
    allowed = {_account_kind(conn, a) for a, _s, _c in legs}
    return _post(conn, "reversal", legs, posted_by, date,
                 memo=memo or f"reversal of e{entry_id}",
                 reverses_entry_id=entry_id, allowed_kinds=allowed)


# --- settlement recipes (casework-billing P3, U3.3) -------------------
# Settlement entries link to a SHARED pre-created external event (the
# processor batch the bank will witness); create_external_event exists
# for that. The per-recipe events elsewhere stay co-written by _post.

def ensure_expense_account(conn, kind):
    if kind not in ("processor_fee_expense", "chargeback_expense"):
        raise LedgerError(f"not an expense kind: {kind}")
    row = conn.execute("SELECT id FROM ledger_accounts WHERE kind=?"
                       " AND deleted_at IS NULL", (kind,)).fetchone()
    if row:
        return row["id"]
    name = ("Processor Fees" if kind == "processor_fee_expense"
            else "Chargeback Expense")
    return conn.execute("INSERT INTO ledger_accounts (kind, name)"
                        " VALUES (?,?)", (kind, name)).lastrowid


def create_external_event(conn, event_type, bank_account_id, occurred_on,
                          amount_cents, direction, counterparty=None,
                          memo=None, invoice_id=None, payment_id=None):
    return conn.execute(
        "INSERT INTO external_events (event_type, bank_account_id,"
        " occurred_on, amount_cents, direction, counterparty, memo,"
        " invoice_id, payment_id) VALUES (?,?,?,?,?,?,?,?,?)",
        (event_type, bank_account_id, occurred_on, amount_cents, direction,
         counterparty, memo, invoice_id, payment_id)).lastrowid


def post_sim_settlement_trust(conn, trust_bank_id, amount_cents, date,
                              posted_by, event_id, contact_id=None,
                              matter_id=None, invoice_id=None,
                              payment_id=None, memo=None):
    """Gross settlement of an online trust-request payment: GROSS to
    trust, never net (F6)."""
    sub = _resolve_sub(conn, trust_bank_id, contact_id, matter_id)
    return _post(conn, "sim_settlement",
                 [(trust_bank_id, "debit", amount_cents),
                  (sub, "credit", amount_cents)],
                 posted_by, date, memo=memo, invoice_id=invoice_id,
                 payment_id=payment_id, external_event_id=event_id)


def post_sim_settlement_operating(conn, operating_id, amount_cents, date,
                                  posted_by, event_id, invoice_id=None,
                                  payment_id=None, memo=None):
    if _account_kind(conn, operating_id) != "operating_bank":
        raise LedgerError("operating settlement needs an operating account")
    fee = ensure_income_account(conn)
    return _post(conn, "sim_settlement",
                 [(operating_id, "debit", amount_cents),
                  (fee, "credit", amount_cents)],
                 posted_by, date, memo=memo, invoice_id=invoice_id,
                 payment_id=payment_id, external_event_id=event_id)


def post_processor_fee(conn, operating_id, fee_cents, date, posted_by,
                       event_id, memo=None):
    """Processor fees pull from OPERATING; a fee posting against trust
    is the F6 violation this recipe makes unrepresentable."""
    exp = ensure_expense_account(conn, "processor_fee_expense")
    return _post(conn, "processor_fee",
                 [(exp, "debit", fee_cents),
                  (operating_id, "credit", fee_cents)],
                 posted_by, date, memo=memo, external_event_id=event_id)


def post_chargeback(conn, operating_id, amount_cents, date, posted_by,
                    event_id, memo=None):
    """r3 boundary: a chargeback is a posting event debiting OPERATING
    (the firm eats the receivable); it never touches trust."""
    exp = ensure_expense_account(conn, "chargeback_expense")
    return _post(conn, "chargeback",
                 [(exp, "debit", amount_cents),
                  (operating_id, "credit", amount_cents)],
                 posted_by, date, memo=memo, external_event_id=event_id)


# --- views ------------------------------------------------------------

def account_transactions(conn, account_id, type=None, date_from=None,
                         date_to=None, description=None,
                         min_amount_cents=None):
    """Transaction rows for one ledger account: date, type, description,
    amount, side, and client/matter attribution from the entry's
    sub-ledger legs (fx-0053, fx-0069 row fields)."""
    rows = conn.execute(
        """SELECT p.entry_id, p.side, p.amount_cents, e.kind, e.memo,
                  e.posted_at
           FROM journal_postings p JOIN journal_entries e ON e.id=p.entry_id
           WHERE p.account_id=? ORDER BY p.entry_id, p.id""",
        (account_id,)).fetchall()
    out = []
    for r in rows:
        attr = conn.execute(
            """SELECT a.contact_id, a.matter_id
               FROM journal_postings p JOIN ledger_accounts a
                 ON a.id = p.account_id
               WHERE p.entry_id=? AND a.kind IN ('client_trust','matter_trust')
               LIMIT 1""", (r["entry_id"],)).fetchone()
        contact_id = attr["contact_id"] if attr else None
        matter_id = attr["matter_id"] if attr else None
        if matter_id is not None and contact_id is None:
            m = conn.execute("SELECT primary_contact_id FROM matters"
                             " WHERE id=?", (matter_id,)).fetchone()
            contact_id = m["primary_contact_id"] if m else None
        t = {"entry_id": r["entry_id"], "date": r["posted_at"],
             "type": r["kind"], "description": r["memo"],
             "amount_cents": r["amount_cents"], "side": r["side"],
             "contact_id": contact_id, "matter_id": matter_id}
        if type is not None and t["type"] != type:
            continue
        if date_from is not None and t["date"] < date_from:
            continue
        if date_to is not None and t["date"] > date_to:
            continue
        if description is not None and \
           description.lower() not in (t["description"] or "").lower():
            continue
        if min_amount_cents is not None and \
           t["amount_cents"] < min_amount_cents:
            continue
        out.append(t)
    return out


def trust_ledger_overview(conn):
    """The Trust Accounting Ledger's three tabs (fx-0053): firm bank
    accounts; client-level and matter-level sub-accounts, listed only
    when they carry trust activity."""
    firm = [{"account_id": b["id"], "name": b["name"],
             "balance_cents": b["balance_cents"]}
            for b in list_bank_accounts(conn) if b["kind"] == "trust_bank"]
    client, matter = [], []
    for r in conn.execute(
            """SELECT DISTINCT a.id, a.kind, a.contact_id, a.matter_id
               FROM ledger_accounts a
               JOIN journal_postings p ON p.account_id = a.id
               WHERE a.kind IN ('client_trust','matter_trust')
                 AND a.deleted_at IS NULL ORDER BY a.id""").fetchall():
        row = {"account_id": r["id"],
               "balance_cents": account_balance(conn, r["id"])}
        if r["kind"] == "client_trust":
            client.append({**row, "contact_id": r["contact_id"]})
        else:
            matter.append({**row, "matter_id": r["matter_id"]})
    return {"firm": firm, "client": client, "matter": matter}


def trust_account_tab(conn, contact_id=None, matter_id=None):
    """The Trust Acct tab on a client or matter overview (fx-0069,
    fx-0074): available funds at that level plus the transaction list,
    aggregated across trust banks."""
    if matter_id is not None:
        cond, val = "kind='matter_trust' AND matter_id=?", matter_id
    elif contact_id is not None:
        cond, val = "kind='client_trust' AND contact_id=?", contact_id
    else:
        raise LedgerError("trust_account_tab needs contact_id or matter_id")
    accounts = [r["id"] for r in conn.execute(
        f"SELECT id FROM ledger_accounts WHERE {cond}"
        " AND deleted_at IS NULL", (val,)).fetchall()]
    txns = []
    for a in accounts:
        txns.extend(account_transactions(conn, a))
    txns.sort(key=lambda t: (t["date"], t["entry_id"]))
    return {"available_cents": sum(account_balance(conn, a)
                                   for a in accounts),
            "transactions": txns}
