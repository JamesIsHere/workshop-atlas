"""P3 parity tests: payment recording, corrections, SimProcessor,
payment plans. Seed-tolerant (own accounts, relative bases)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "verify"))

from app import billing, ledger, processor, scheduler
from tests.spine._http import client_surface, get, post_form
import run_fiduciary as fid

D = "2026-08-05"


def _setup(conn):
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    op = conn.execute("SELECT id FROM ledger_accounts WHERE"
                      " kind='operating_bank' AND deleted_at IS NULL"
                      " ORDER BY id LIMIT 1").fetchone()
    op = op["id"] if op else ledger.create_bank_account(
        conn, "operating_bank", "SYNTH Operating", 1)
    return iolta, op


def _bill(conn, contact=1, amount=100000):
    b = billing.create_invoice(conn, "bill", contact, 1, D)
    billing.add_charge(conn, b, "service", "SYNTH services", amount, 1)
    return b


def test_invoicing_and_trust_accounting_direct_payment_recording(conn):
    # criterion: record a Direct Payment -> invoice balance decreases
    # (fx-0062/0070); asks type, destination, date, amount, description
    iolta, op = _setup(conn)
    b = _bill(conn)
    assert billing.invoice_balance(conn, b) == 100000
    p = billing.record_payment(conn, b, "direct", 40000, D, 1,
                               destination_account_id=op,
                               note="SYNTH cash payment")
    assert billing.invoice_balance(conn, b) == 60000
    row = billing.get_payment(conn, p)
    assert row["destination_account_id"] == op
    assert row["note"] == "SYNTH cash payment"
    billing.record_payment(conn, b, "direct", 60000, D, 1,
                           destination_account_id=op)
    assert billing.invoice_status(conn, b) == "paid", \
        "zero balance -> Paid tab (fx-0070)"


def test_invoicing_and_trust_accounting_trust_requests(conn):
    # criterion: create a Trust Request and record a payment -> funds
    # recorded into the selected trust account at the chosen client or
    # matter level (fx-0061/0065/0071)
    iolta, _op = _setup(conn)
    base = billing.available_trust_funds(conn, "client", contact_id=1)
    bank_base = ledger.account_balance(conn, iolta)
    tr = billing.create_invoice(conn, "trust_request", 1, 1, D,
                                trust_level="client",
                                trust_account_id=iolta)
    billing.add_charge(conn, tr, "service", "SYNTH retainer request",
                       250000, 1)
    billing.record_payment(conn, tr, "direct", 250000, D, 1)
    assert ledger.account_balance(conn, iolta) == bank_base + 250000, \
        "payment deposited into the selected trust account"
    assert billing.available_trust_funds(conn, "client", contact_id=1) \
        == base + 250000, "held at the client level"
    assert billing.invoice_status(conn, tr) == "paid", \
        "trust request moves to Paid at zero balance (fx-0071)"

    # matter level: the two pots stay distinct
    m = billing.create_invoice(conn, "trust_request", 1, 1, D,
                               matter_id=1, trust_level="matter",
                               trust_account_id=iolta)
    billing.add_charge(conn, m, "service", "SYNTH matter funds", 50000, 1)
    billing.record_payment(conn, m, "direct", 50000, D, 1)
    assert billing.available_trust_funds(conn, "matter", matter_id=1) \
        >= 50000


def test_invoicing_and_trust_accounting_trust_transfer_payment(conn):
    # criterion: Record Payment of type Trust Transfer from funded
    # trust -> bill paid, amount debited from the trust funds (fx-0066)
    iolta, op = _setup(conn)
    ledger.record_trust_deposit(conn, iolta, 500000, D, 1, contact_id=1)
    avail = billing.available_trust_funds(conn, "client", contact_id=1)
    assert avail >= 500000, "available amount displayed (fx-0066)"
    b = _bill(conn, amount=300000)
    billing.record_payment(conn, b, "trust_transfer", 300000, D, 1,
                           destination_account_id=op,
                           source_account_id=iolta,
                           source_trust_level="client")
    assert billing.invoice_status(conn, b) == "paid"
    assert billing.available_trust_funds(conn, "client", contact_id=1) \
        == avail - 300000, "debited from the selected trust funds"
    # over-available transfer is blocked by the ledger (F4 at write)
    b2 = _bill(conn, amount=900000)
    try:
        billing.record_payment(conn, b2, "trust_transfer", 900000, D, 1,
                               destination_account_id=op,
                               source_account_id=iolta,
                               source_trust_level="client")
        raise AssertionError("transfer beyond available funds accepted")
    except ledger.LedgerError:
        pass


def test_invoicing_and_trust_accounting_payment_charge_association(conn):
    # criterion: associate a payment with a specific charge -> the
    # charge shows an entry with payment date and amount (fx-0057)
    iolta, op = _setup(conn)
    b = billing.create_invoice(conn, "bill", 1, 1, D)
    c1 = billing.add_charge(conn, b, "service", "SYNTH filing", 80000, 1)
    billing.add_charge(conn, b, "expense", "SYNTH courier", 5000, 1)
    p = billing.record_payment(conn, b, "direct", 80000, D, 1,
                               destination_account_id=op,
                               associated_charge_id=c1)
    assert billing.charge_payment_entries(conn, c1) == [(D, 80000)]
    # a payment larger than the charge cannot be associated (fx-0057)
    try:
        billing.record_payment(conn, b, "direct", 5001, D, 1,
                               destination_account_id=op,
                               associated_charge_id=billing.invoice_charges(
                                   conn, b)[1]["id"])
        raise AssertionError("payment larger than charge associated")
    except billing.BillingError:
        pass
    assert p


def test_invoicing_and_trust_accounting_payment_editing(conn):
    # criterion: open a recorded payment, change the amount -> payment
    # and invoice balance update (fx-0077); map note: no journal row
    # may mutate (r2 -- reversal + repost underneath)
    iolta, op = _setup(conn)
    b = _bill(conn)
    p = billing.record_payment(conn, b, "direct", 40000, D, 1,
                               destination_account_id=op)
    old_entry = billing.get_payment(conn, p)["journal_entry_id"]
    billing.edit_payment(conn, p, 1, D, amount_cents=55000)
    row = billing.get_payment(conn, p)
    assert row["amount_cents"] == 55000, "payment updated"
    assert billing.invoice_balance(conn, b) == 45000, "balance updated"
    assert row["journal_entry_id"] != old_entry
    rev = conn.execute("SELECT id FROM journal_entries WHERE"
                       " reverses_entry_id=?", (old_entry,)).fetchone()
    assert rev is not None, "old entry reversed, not mutated"
    ok, line = fid.check_f8(conn)
    assert ok, line


def test_invoicing_and_trust_accounting_payment_refunds(conn):
    # criterion: toggle Refund this payment and save -> the invoice
    # reflects the refunded payment (fx-0055); full-amount only
    iolta, op = _setup(conn)
    b = _bill(conn)
    p = billing.record_payment(conn, b, "direct", 100000, D, 1,
                               destination_account_id=op)
    assert billing.invoice_status(conn, b) == "paid"
    billing.refund_payment(conn, p, 1, D, note="SYNTH refund note")
    assert billing.invoice_balance(conn, b) == 100000, \
        "invoice reflects the refund"
    assert billing.get_payment(conn, p)["refund_note"] == \
        "SYNTH refund note"
    try:
        billing.refund_payment(conn, p, 1, D)
        raise AssertionError("double refund accepted")
    except billing.BillingError:
        pass


def test_invoicing_and_trust_accounting_online_card_payment(conn, tmp=None):
    # adapted criterion: client opens the shared-invoice link, completes
    # the payment form -> processed by the simulated fee-split processor
    # and recorded, gross to trust / fees from operating (F6)
    import tempfile
    iolta, op = _setup(conn)
    billing.set_setting(conn, "billing.receipt_auto_send", "1")
    tr = billing.create_invoice(conn, "trust_request", 1, 1, D,
                                trust_level="client",
                                trust_account_id=iolta)
    billing.add_charge(conn, tr, "service", "SYNTH retainer", 200000, 1)
    token = billing.share_invoice(conn, tr, 1)
    bank_base = ledger.account_balance(conn, iolta)
    op_base = ledger.account_balance(conn, op)

    with tempfile.TemporaryDirectory() as td:
        with client_surface(conn, td) as base:
            status, page = get(f"{base}/invoice/{token}")
            assert status == 200 and "Pay" in page, "pay page served"
            status, page = post_form(f"{base}/invoice/{token}/pay",
                                     {"sim_token": "SYNTHETIC-DECLINE-1",
                                      "kind": "card"})
            assert "Declined" in page, "declined token declines"
            status, page = post_form(f"{base}/invoice/{token}/pay",
                                     {"sim_token": "SYNTHETIC-VISA-1",
                                      "kind": "card"})
            assert status == 200 and "Payment received" in page

    assert billing.invoice_status(conn, tr) == "paid", \
        "payment recorded against the invoice"
    # money moves at settlement: gross to trust, fee from operating
    processor.settle(conn, D, posted_by=1)
    assert ledger.account_balance(conn, iolta) == bank_base + 200000, \
        "GROSS to trust (F6)"
    fee = processor.fee_for(200000)
    assert ledger.account_balance(conn, op) == op_base - fee, \
        "fee pulled from operating, never netted from trust"
    ok, line = fid.check_f6(conn)
    assert ok, line
    # auto-receipt setting (fx-0076)
    n = conn.execute("SELECT COUNT(*) FROM email_outbox WHERE"
                     " template='billing_receipt'").fetchone()[0]
    assert n == 1, "receipt auto-sent on platform payment"
    # chargeback: clawed from operating only (r3)
    txn = conn.execute("SELECT id FROM processor_transactions WHERE"
                       " status='settled' ORDER BY id LIMIT 1").fetchone()
    processor.chargeback(conn, txn["id"], D, posted_by=1)
    assert ledger.account_balance(conn, iolta) == bank_base + 200000, \
        "chargeback never touches trust"
    ok, line = fid.check_f5(conn)
    assert ok, line


def test_invoicing_and_trust_accounting_payment_plans(conn):
    # criterion: activate a Payment Plan with frequency, installment
    # amount, start date -> balance billed on the recurring installment
    # schedule (fx-0072); reminders 7-before/due/7-after; auto-charge
    iolta, op = _setup(conn)
    b = _bill(conn, contact=1, amount=90000)
    plan = billing.create_payment_plan(conn, b, 30, 30000, "2026-09-01",
                                       1, auto_charge=0)
    insts = billing.plan_installments(conn, plan)
    assert [i["amount_cents"] for i in insts] == [30000, 30000, 30000]
    assert [i["due_date"] for i in insts] == \
        ["2026-09-01", "2026-10-01", "2026-10-31"]

    def reminders():
        return conn.execute(
            "SELECT COUNT(*) FROM email_outbox WHERE"
            " template='billing_plan_reminder'").fetchone()[0]

    scheduler.tick(conn, "2026-08-26T02:00:00Z")   # 6 days before
    assert reminders() == 1, "7-day-before reminder"
    scheduler.tick(conn, "2026-09-01T02:00:00Z")   # due day
    assert reminders() == 2, "due-day reminder"
    scheduler.tick(conn, "2026-09-08T02:00:00Z")   # 7 days after, unpaid
    assert reminders() == 3, "7-day-after reminder"

    # auto-charge plan: due installments are charged via SimProcessor
    b2 = _bill(conn, contact=2, amount=60000)
    plan2 = billing.create_payment_plan(conn, b2, 30, 30000, "2026-09-01",
                                        1, auto_charge=1)
    scheduler.tick(conn, "2026-09-01T02:00:00Z")
    assert billing.invoice_balance(conn, b2) == 30000, \
        "installment auto-charged on due day"
    scheduler.tick(conn, "2026-10-01T02:00:00Z")
    assert billing.invoice_balance(conn, b2) == 0, \
        "balance billed on the recurring schedule"
    paid = [i["paid_payment_id"] for i in
            billing.plan_installments(conn, plan2)]
    assert all(paid), paid