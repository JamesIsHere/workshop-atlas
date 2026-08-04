"""P2 parity tests (authored with the module, oracle-first): invoice
creation, numbering, saved charges, default settings, late fees,
translation, module-exists. Criteria from the corpus; seed-tolerant
(relative counts, own objects)."""
import tempfile
from pathlib import Path

from pypdf import PdfReader

from app import billing, ledger, scheduler

D = "2026-08-05"


def _trust_setup(conn):
    iolta = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)
    return iolta


def test_invoicing_and_trust_accounting_invoice_creation(conn):
    # criterion: choose Bill or Trust Request, assign a client -> invoice
    # of the chosen type created and opens in the Builder for charges
    # and settings (fx-0065/0070/0071)
    bill = billing.create_invoice(conn, "bill", 1, 1, D)
    inv = billing.get_invoice(conn, bill)
    assert inv["invoice_type"] == "bill" and inv["contact_id"] == 1
    # builder: charges with description, amount, date, Service/Expense,
    # optional matter association (fx-0065)
    billing.add_charge(conn, bill, "service", "SYNTH I-130 preparation",
                       250000, 1, charge_date=D, matter_id=1)
    billing.add_charge(conn, bill, "expense", "SYNTH courier", 4500, 1)
    assert len(billing.invoice_charges(conn, bill)) == 2
    # builder: per-invoice settings (fx-0061/0065)
    billing.update_invoice_settings(conn, bill, discount_cents=5000,
                                    due_date="2026-09-01",
                                    footer="SYNTH footer")
    inv = billing.get_invoice(conn, bill)
    assert inv["discount_cents"] == 5000 and inv["footer"] == "SYNTH footer"
    assert billing.invoice_balance(conn, bill) == 250000 + 4500 - 5000

    iolta = _trust_setup(conn)
    tr = billing.create_invoice(conn, "trust_request", 1, 1, D,
                                trust_level="client",
                                trust_account_id=iolta)
    assert billing.get_invoice(conn, tr)["invoice_type"] == "trust_request"
    try:
        billing.create_invoice(conn, "trust_request", 1, 1, D)
        raise AssertionError("trust request without account accepted")
    except billing.BillingError:
        pass


def test_invoicing_and_trust_accounting_global_invoice_numbering(conn):
    # criterion: per-client by default; enabling global numbering gives
    # firm-wide incrementing numbers, no renumbering, editable start
    # (fx-0076/0078)
    a1 = billing.create_invoice(conn, "bill", 1, 1, D)
    a2 = billing.create_invoice(conn, "bill", 1, 1, D)
    b1 = billing.create_invoice(conn, "bill", 2, 1, D)
    n = {i: billing.get_invoice(conn, i)["number"] for i in (a1, a2, b1)}
    assert n[a1] == 1 and n[a2] == 2, "per-client sequence"
    assert n[b1] == 1, "each client numbers up from 1"

    billing.set_setting(conn, "billing.global_numbering", "1")
    g1 = billing.create_invoice(conn, "bill", 1, 1, D)
    total_before = 3
    assert billing.get_invoice(conn, g1)["number"] == total_before + 1, \
        "numbers up from firm total on enable (fx-0076)"
    g2 = billing.create_invoice(conn, "bill", 2, 1, D)
    assert billing.get_invoice(conn, g2)["number"] == total_before + 2, \
        "firm-wide increment across clients"
    assert billing.get_invoice(conn, a1)["number"] == 1, "no renumbering"
    billing.set_setting(conn, "billing.global_next", "500")
    g3 = billing.create_invoice(conn, "bill", 1, 1, D)
    assert billing.get_invoice(conn, g3)["number"] == 500, "editable start"


def test_invoicing_and_trust_accounting_saved_charges(conn):
    # criterion: select saved charges -> they import into the invoice
    # (fx-0059); bills only
    s1 = billing.create_saved_charge(conn, "SYNTH Consultation", 15000,
                                     "service", 1)
    s2 = billing.create_saved_charge(conn, "SYNTH I-485 Filing Fee",
                                     144000, "expense", 1)
    bill = billing.create_invoice(conn, "bill", 1, 1, D)
    billing.import_saved_charges(conn, bill, [s1, s2], 1)
    descs = [c["description"] for c in billing.invoice_charges(conn, bill)]
    assert descs == ["SYNTH Consultation", "SYNTH I-485 Filing Fee"]

    iolta = _trust_setup(conn)
    tr = billing.create_invoice(conn, "trust_request", 1, 1, D,
                                trust_level="client",
                                trust_account_id=iolta)
    try:
        billing.import_saved_charges(conn, tr, [s1], 1)
        raise AssertionError("saved charges imported into a Trust Request")
    except billing.BillingError:
        pass


def test_invoicing_and_trust_accounting_default_invoice_settings(conn):
    # criterion: change a firm default -> invoices created thereafter
    # reflect it, overridable per invoice (fx-0076)
    before = billing.create_invoice(conn, "bill", 1, 1, D)
    billing.set_setting(conn, "billing.default_footer", "SYNTH terms")
    billing.set_setting(conn, "billing.default_reminder_enabled", "1")
    billing.set_setting(conn, "billing.default_reminder_days", "14")
    after = billing.create_invoice(conn, "bill", 1, 1, D)
    assert billing.get_invoice(conn, before)["footer"] is None, \
        "defaults apply forward only"
    got = billing.get_invoice(conn, after)
    assert got["footer"] == "SYNTH terms" and got["reminder_days"] == 14
    billing.update_invoice_settings(conn, after, footer="override")
    assert billing.get_invoice(conn, after)["footer"] == "override"
    # automatic due dates: 15th or last day, whichever sooner (fx-0076)
    billing.set_setting(conn, "billing.auto_due_date", "1")
    early = billing.create_invoice(conn, "bill", 1, 1, "2026-08-05")
    late = billing.create_invoice(conn, "bill", 1, 1, "2026-08-20")
    assert billing.get_invoice(conn, early)["due_date"] == "2026-08-15"
    assert billing.get_invoice(conn, late)["due_date"] == "2026-08-31"


def test_invoicing_and_trust_accounting_automatic_late_fees(conn):
    # criterion: enabled invoice passes its due date unpaid -> late fee
    # applied automatically (fx-0058); overnight = scheduler tick
    bill = billing.create_invoice(conn, "bill", 1, 1, "2026-08-01")
    billing.add_charge(conn, bill, "service", "SYNTH services", 100000, 1)
    billing.update_invoice_settings(conn, bill, due_date="2026-08-10",
                                    late_fee_enabled=1,
                                    late_fee_kind="fixed",
                                    late_fee_value=2500,
                                    late_fee_recurring=1,
                                    late_fee_recur_days=7)
    scheduler.tick(conn, "2026-08-11T02:00:00Z")
    fees = [c for c in billing.invoice_charges(conn, bill)
            if c["source"] == "late_fee"]
    assert len(fees) == 1 and fees[0]["amount_cents"] == 2500
    scheduler.tick(conn, "2026-08-11T23:00:00Z")
    fees = [c for c in billing.invoice_charges(conn, bill)
            if c["source"] == "late_fee"]
    assert len(fees) == 1, "no duplicate fee on same-day tick"
    scheduler.tick(conn, "2026-08-18T02:00:00Z")
    fees = [c for c in billing.invoice_charges(conn, bill)
            if c["source"] == "late_fee"]
    assert len(fees) == 2, "recurring fee after the interval (fx-0058)"

    # percent kind: basis points of outstanding balance
    pb = billing.create_invoice(conn, "bill", 2, 1, "2026-08-01")
    billing.add_charge(conn, pb, "service", "SYNTH services", 200000, 1)
    billing.update_invoice_settings(conn, pb, due_date="2026-08-10",
                                    late_fee_enabled=1,
                                    late_fee_kind="percent",
                                    late_fee_value=500)
    scheduler.tick(conn, "2026-08-11T02:00:00Z")
    fees = [c for c in billing.invoice_charges(conn, pb)
            if c["source"] == "late_fee"]
    assert fees[0]["amount_cents"] == 200000 * 500 // 10000


def _pdf_text(path):
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)


def test_invoicing_and_trust_accounting_invoice_translation(conn):
    # criterion: select Spanish -> invoice displays in Spanish for firm
    # and client (fx-0052); chrome only, stored text verbatim
    bill = billing.create_invoice(conn, "bill", 1, 1, D, language="es")
    billing.add_charge(conn, bill, "service", "SYNTH consultation fee",
                       50000, 1)
    with tempfile.TemporaryDirectory() as td:
        out = str(Path(td) / "invoice_es.pdf")
        billing.invoice_pdf(conn, bill, out)
        text = _pdf_text(out)
    assert "Factura" in text and "Saldo pendiente" in text, \
        "template chrome renders in Spanish"
    assert "SYNTH consultation fee" in text, \
        "charge description NOT translated (fx-0052 exclusion)"
    # default language renders English
    en = billing.create_invoice(conn, "bill", 1, 1, D)
    billing.add_charge(conn, en, "service", "SYNTH consultation fee",
                       50000, 1)
    with tempfile.TemporaryDirectory() as td:
        out = str(Path(td) / "invoice_en.pdf")
        billing.invoice_pdf(conn, en, out)
        text = _pdf_text(out)
    assert "Balance Due" in text


def test_invoicing_and_trust_accounting_module_exists(conn):
    # criterion: billing area -> invoicing AND trust accounting
    # functions available as a distinct module (fx-0003/0050)
    invoicing = ("create_invoice", "add_charge", "import_saved_charges",
                 "invoice_balance", "list_invoices", "invoice_pdf")
    trust = ("create_bank_account", "record_trust_deposit", "disburse",
             "earn_out", "trust_ledger_overview", "trust_account_tab")
    for fn in invoicing + trust:
        assert callable(getattr(billing, fn, None)), \
            f"billing module missing {fn}"
    # smoke: one action from each family through the module surface
    bill = billing.create_invoice(conn, "bill", 1, 1, D)
    assert billing.invoice_status(conn, bill) in ("paid", "outstanding")
    iolta = billing.create_bank_account(conn, "trust_bank",
                                        "SYNTH IOLTA M", 1)
    billing.record_trust_deposit(conn, iolta, 10000, D, 1, contact_id=1)
    assert billing.trust_account_tab(conn, contact_id=1)["transactions"]