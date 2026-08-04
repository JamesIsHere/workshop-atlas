"""FeeSplitProcessor interface + deterministic simulator
(casework-billing P3, U3.3; goal.md decision default 3).

NEVER payment processing: SimProcessor moves no real money and accepts
only SYNTHETIC- tokens (schema CHECK backs this). It exists so the
fee-split MECHANICS are real: charges authorize immediately, money
moves at settlement -- gross to the destination bank, fees pulled from
operating -- which is exactly the lag the reconciliation model (F7)
and the F6 linkage assertion feed on. A real fee-split processor
(LawPay/Confido/Gravity) would implement the same interface post-v1
(Approval-required).

Determinism: fee schedule fixed (3% + 30c); a token starting with
SYNTHETIC-DECLINE always declines; no randomness anywhere.
"""

from app import ledger

FEE_BPS = 300
FEE_FIXED_CENTS = 30


class ProcessorError(ValueError):
    pass


def fee_for(amount_cents):
    return amount_cents * FEE_BPS // 10000 + FEE_FIXED_CENTS


def charge(conn, token, amount_cents, kind="card"):
    """Authorize a charge. Money does NOT move here -- settlement does
    that. Returns the processor transaction id, or raises on decline."""
    if kind not in ("card", "echeck"):
        raise ProcessorError(f"unknown payment form: {kind}")
    if not token.startswith("SYNTHETIC-"):
        raise ProcessorError("real payment credentials are forbidden;"
                             " synthetic tokens only (goal.md)")
    txn_kind = "charge" if kind == "card" else "echeck"
    if token.startswith("SYNTHETIC-DECLINE"):
        conn.execute(
            "INSERT INTO processor_transactions (kind, token, amount_cents,"
            " fee_cents, status) VALUES (?,?,?,0,'declined')",
            (txn_kind, token, amount_cents))
        raise ProcessorError("card declined")
    cur = conn.execute(
        "INSERT INTO processor_transactions (kind, token, amount_cents,"
        " fee_cents, status) VALUES (?,?,?,?,'approved')",
        (txn_kind, token, amount_cents, fee_for(amount_cents)))
    return cur.lastrowid


def refund(conn, txn_id):
    """fx-0055: refunding a platform payment triggers the processor
    refund automatically."""
    txn = conn.execute("SELECT * FROM processor_transactions WHERE id=?",
                       (txn_id,)).fetchone()
    if txn is None:
        raise ProcessorError(f"no such transaction: {txn_id}")
    return conn.execute(
        "INSERT INTO processor_transactions (kind, token, amount_cents,"
        " fee_cents, status) VALUES ('refund', ?, ?, 0, 'approved')",
        (txn["token"], txn["amount_cents"])).lastrowid


def settle(conn, settle_date, posted_by=None):
    """Settle every approved, unbatched charge: one batch per
    destination bank. Trust destinations settle GROSS with the batch
    fee pulled from operating (F6); operating destinations honor the
    billing.settlement_mode firm setting (gross default; net keeps the
    fee out of the books and discloses it on the batch row only)."""
    from app import billing
    rows = conn.execute(
        """SELECT t.id AS txn_id, t.amount_cents, t.fee_cents,
                  p.id AS payment_id, p.invoice_id,
                  p.destination_account_id
           FROM processor_transactions t
           JOIN invoice_payments p ON p.processor_txn_id = t.id
           WHERE t.status='approved' AND t.batch_id IS NULL
             AND t.kind IN ('charge','echeck')
             AND p.deleted_at IS NULL AND p.refunded=0
           ORDER BY t.id""").fetchall()
    by_bank = {}
    for r in rows:
        by_bank.setdefault(r["destination_account_id"], []).append(r)
    operating = conn.execute(
        "SELECT id FROM ledger_accounts WHERE kind='operating_bank'"
        " AND deleted_at IS NULL ORDER BY id LIMIT 1").fetchone()
    batches = []
    for bank_id, txns in sorted(by_bank.items()):
        bank_kind = conn.execute("SELECT kind FROM ledger_accounts WHERE"
                                 " id=?", (bank_id,)).fetchone()["kind"]
        gross = sum(t["amount_cents"] for t in txns)
        fees = sum(t["fee_cents"] for t in txns)
        if bank_kind == "trust_bank":
            mode = "gross"  # F6: fees never netted from trust
        else:
            mode = billing.get_setting(conn, "billing.settlement_mode",
                                       "gross")
        net = gross - fees
        batch_id = conn.execute(
            "INSERT INTO settlement_batches (settle_date, bank_account_id,"
            " mode, gross_cents, fee_cents, net_cents) VALUES (?,?,?,?,?,?)",
            (settle_date, bank_id, mode, gross, fees, net)).lastrowid
        posted = gross if mode == "gross" else net
        in_event = ledger.create_external_event(
            conn, "processor_batch", bank_id, settle_date, posted, "in",
            counterparty="SimProcessor", memo=f"settlement batch {batch_id}")
        for t in txns:
            inv = billing.get_invoice(conn, t["invoice_id"])
            amount = t["amount_cents"] if mode == "gross" \
                else t["amount_cents"] - t["fee_cents"]
            if bank_kind == "trust_bank":
                entry = ledger.post_sim_settlement_trust(
                    conn, bank_id, amount, settle_date, posted_by, in_event,
                    contact_id=(inv["contact_id"]
                                if inv["trust_level"] == "client" else None),
                    matter_id=(inv["matter_id"]
                               if inv["trust_level"] == "matter" else None),
                    invoice_id=inv["id"], payment_id=t["payment_id"])
            else:
                entry = ledger.post_sim_settlement_operating(
                    conn, bank_id, amount, settle_date, posted_by, in_event,
                    invoice_id=inv["id"], payment_id=t["payment_id"])
            conn.execute("UPDATE invoice_payments SET journal_entry_id=?"
                         " WHERE id=?", (entry, t["payment_id"]))
            conn.execute("UPDATE processor_transactions SET status='settled',"
                         " batch_id=? WHERE id=?", (batch_id, t["txn_id"]))
        if mode == "gross" and fees > 0:
            if operating is None:
                raise ProcessorError("gross settlement needs an operating"
                                     " account to pull fees from")
            fee_event = ledger.create_external_event(
                conn, "processor_batch", operating["id"], settle_date, fees,
                "out", counterparty="SimProcessor",
                memo=f"settlement batch {batch_id} fees")
            ledger.post_processor_fee(conn, operating["id"], fees,
                                      settle_date, posted_by, fee_event,
                                      memo=f"batch {batch_id} fees")
        batches.append(batch_id)
    return batches


def chargeback(conn, txn_id, date, posted_by=None):
    """r3 boundary: posting event with the fee-split recipe -- clawback
    debits OPERATING, never trust. No dispute workflow exists."""
    txn = conn.execute("SELECT * FROM processor_transactions WHERE id=?",
                       (txn_id,)).fetchone()
    if txn is None or txn["status"] != "settled":
        raise ProcessorError("only settled transactions charge back")
    operating = conn.execute(
        "SELECT id FROM ledger_accounts WHERE kind='operating_bank'"
        " AND deleted_at IS NULL ORDER BY id LIMIT 1").fetchone()
    if operating is None:
        raise ProcessorError("chargeback needs an operating account")
    conn.execute(
        "INSERT INTO processor_transactions (kind, token, amount_cents,"
        " fee_cents, status) VALUES ('chargeback', ?, ?, 0, 'approved')",
        (txn["token"], txn["amount_cents"]))
    conn.execute("UPDATE processor_transactions SET status='charged_back'"
                 " WHERE id=?", (txn_id,))
    event = ledger.create_external_event(
        conn, "chargeback", operating["id"], date, txn["amount_cents"],
        "out", counterparty="SimProcessor", memo=f"chargeback txn {txn_id}")
    return ledger.post_chargeback(conn, operating["id"],
                                  txn["amount_cents"], date, posted_by,
                                  event, memo=f"chargeback txn {txn_id}")
