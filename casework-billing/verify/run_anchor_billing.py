#!/usr/bin/env python
"""Anchor billing workflow (goal.md verifier 3) -- the live walk.

One scripted cold-start story on a FRESH database, no seed: install
-> admin -> client + matter -> trust and operating accounts -> bill
paid direct (funds operating) -> Trust Request shared and paid by the
client over real localhost HTTP against the simulated processor ->
settlement (gross to trust, fee from operating) -> Bill carrying a
saved charge and an imported time entry -> paid by trust transfer
(earn-out) -> disbursement to a third party -> invoice PDF read back
-> three-way reconciliation artifact -> audit continuity across
system/user/contact actors -> full fiduciary suite green on the
walked database.

The report carries wall-clock timings on purpose (completion proof:
"verifier 3 pass with timings"). Budget: 900s (decision default 6).

Run: python verify/run_anchor_billing.py
Writes anchor-billing-report.txt and recon-report.txt beside it.
Exit 0 iff every step passes and the budget holds.
"""
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASEWORK = HERE.parent.parent / "casework"
sys.path.insert(0, str(CASEWORK))
sys.path.insert(0, str(HERE))

from app import billing, bootstrap, contacts, matters, processor  # noqa: E402
from app import db as appdb  # noqa: E402
from app import server, timekeeping, users  # noqa: E402
import bank_statement  # noqa: E402
import reconcile  # noqa: E402
import run_fiduciary as fid  # noqa: E402

REPORT = HERE / "anchor-billing-report.txt"
RECON_REPORT = HERE / "recon-report.txt"
BUDGET_SECONDS = 900

NOW = "2026-08-01T00:00:00Z"
D1, D2, D3, D4 = "2026-08-01", "2026-08-02", "2026-08-03", "2026-08-04"


class Walk:
    def __init__(self, workdir):
        self.workdir = Path(workdir)
        self.conn = None
        self.admin = None
        self.contact = None
        self.matter = None
        self.iolta = None
        self.op = None
        self.trust_request = None
        self.bill = None


def http_post(url, data):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")


def step_install(w):
    w.conn = appdb.create_db(str(w.workdir / "anchor-billing.db"))
    bootstrap.install(w.conn, NOW)
    w.conn.execute("INSERT INTO synthetic_marker (marker) VALUES"
                   " ('SYNTHETIC')")
    w.admin = users.create_user(w.conn, "billing.admin@synthetic.test",
                                "Billing Synthetic", NOW,
                                role_label="Managing Attorney")
    users.update_user(w.conn, w.admin, is_admin=1, is_owner=1)
    w.conn.actor.set("user", w.admin)
    return "fresh db installed; admin id %d" % w.admin


def step_client_matter(w):
    w.contact = contacts.create_contact(
        w.conn, "person", NOW, w.admin, given_name="Vera",
        family_name="Synthetic", email="vera.client@synthetic.test")
    w.matter = matters.create_matter(w.conn, "Vera Synthetic I-130",
                                     w.contact, NOW, w.admin)
    return "contact %d, matter %d" % (w.contact, w.matter)


def step_accounts(w):
    w.iolta = billing.create_bank_account(w.conn, "trust_bank",
                                          "SYNTH IOLTA", w.admin)
    w.op = billing.create_bank_account(w.conn, "operating_bank",
                                       "SYNTH Operating", w.admin)
    return "trust bank %d, operating %d" % (w.iolta, w.op)


def step_fund_operating(w):
    b = billing.create_invoice(w.conn, "bill", w.contact, w.admin, D1)
    billing.add_charge(w.conn, b, "service", "SYNTH consultation",
                       50000, w.admin)
    billing.record_payment(w.conn, b, "direct", 50000, D1, w.admin,
                           destination_account_id=w.op)
    assert billing.invoice_status(w.conn, b) == "paid"
    return "consult bill paid direct; operating funded 500.00"


def step_trust_request_online(w):
    w.trust_request = billing.create_invoice(
        w.conn, "trust_request", w.contact, w.admin, D1,
        trust_level="client", trust_account_id=w.iolta)
    billing.add_charge(w.conn, w.trust_request, "service",
                       "SYNTH retainer request", 500000, w.admin)
    token = billing.share_invoice(w.conn, w.trust_request, w.admin,
                                  share_date=D1)
    httpd = server.make_server(w.conn, str(w.workdir))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        base = server.base_url(httpd)
        status, page = http_post(f"{base}/invoice/{token}/pay",
                                 {"sim_token": "SYNTHETIC-VISA-ANCHOR",
                                  "kind": "card"})
        assert status == 200 and "Payment received" in page, page[:200]
    finally:
        httpd.shutdown()
        httpd.server_close()
    assert billing.invoice_status(w.conn, w.trust_request) == "paid"
    return "client paid 5,000.00 over HTTP via SimProcessor"


def step_settlement(w):
    batches = processor.settle(w.conn, D2, posted_by=w.admin)
    assert batches, "no settlement batch"
    iolta_bal = billing.account_balance(w.conn, w.iolta)
    assert iolta_bal == 500000, "gross to trust: %d" % iolta_bal
    fee = processor.fee_for(500000)
    op_bal = billing.account_balance(w.conn, w.op)
    assert op_bal == 50000 - fee, "fee from operating: %d" % op_bal
    return "settled gross 5,000.00 to trust; fee %.2f from operating" \
        % (fee / 100)


def step_bill_earn_out(w):
    saved = billing.create_saved_charge(w.conn, "SYNTH I-130 preparation",
                                        250000, "service", w.admin)
    timekeeping.set_user_default_rate(w.conn, w.admin, 25000)
    entry = timekeeping.create_entry(w.conn, w.admin, D2, duration="2h",
                                     description="SYNTH case work",
                                     contact_id=w.contact,
                                     matter_id=w.matter)
    w.bill = billing.create_invoice(w.conn, "bill", w.contact, w.admin, D2,
                                    matter_id=w.matter)
    billing.import_saved_charges(w.conn, w.bill, [saved], w.admin)
    billing.import_time_entries(w.conn, w.bill, [entry], w.admin)
    total = billing.invoice_balance(w.conn, w.bill)
    assert total == 300000, "bill total: %d" % total
    billing.record_payment(w.conn, w.bill, "trust_transfer", 300000, D3,
                           w.admin, destination_account_id=w.op,
                           source_account_id=w.iolta,
                           source_trust_level="client")
    assert billing.invoice_status(w.conn, w.bill) == "paid"
    assert billing.available_trust_funds(w.conn, "client",
                                         contact_id=w.contact) == 200000
    return "bill 3,000.00 (saved charge + 2h imported) earned out of trust"


def step_disbursement(w):
    billing.disburse(w.conn, w.iolta, 120000, D4, w.admin,
                     contact_id=w.contact, counterparty="SYNTH-USCIS",
                     memo="SYNTH I-130 filing fee")
    left = billing.available_trust_funds(w.conn, "client",
                                         contact_id=w.contact)
    assert left == 80000, "client funds after disbursement: %d" % left
    return "1,200.00 disbursed to SYNTH-USCIS; client funds 800.00"


def step_invoice_pdf(w):
    from pypdf import PdfReader
    out = w.workdir / "anchor-invoice.pdf"
    billing.invoice_pdf(w.conn, w.bill, str(out))
    text = "\n".join(p.extract_text() for p in PdfReader(str(out)).pages)
    assert "SYNTH I-130 preparation" in text, "charge missing from PDF"
    assert "Balance Due: 0.00" in text, "balance missing from PDF"
    return "invoice PDF rendered and read back"


def step_reconciliation(w):
    lines = []
    for bank in (w.iolta, w.op):
        stmt = bank_statement.statement(w.conn, bank, D4)
        lines.append("STATEMENT account %d through %s: %d lines,"
                     " %d pending, closing %d"
                     % (bank, D4, len(stmt["lines"]), len(stmt["pending"]),
                        stmt["closing_balance_cents"]))
        for period in (D4, bank_statement._plus_days(D4, 10)):
            r = reconcile.three_way(w.conn, bank, period)
            lines.extend(reconcile.report_lines(r))
            assert r["identity_holds"], "reconciliation broken: %r" % r
    RECON_REPORT.write_text("\n".join(lines) + "\n")
    return "three-way reconciliation HOLDS for both banks at two" \
        " period ends -> recon-report.txt"


def step_audit_continuity(w):
    classes = [r[0] for r in w.conn.execute(
        "SELECT DISTINCT actor_type FROM audit_log").fetchall()]
    for needed in ("system", "user", "contact"):
        assert needed in classes, "missing actor class %s" % needed
    first_user = w.conn.execute(
        "SELECT MIN(id) FROM audit_log WHERE actor_type='user'"
    ).fetchone()[0]
    first_system = w.conn.execute(
        "SELECT MIN(id) FROM audit_log WHERE actor_type='system'"
    ).fetchone()[0]
    assert first_system < first_user, "install precedes user actions"
    return "audit spans system/user/contact actors, story-ordered"


def step_fiduciary(w):
    ok, lines = fid.run_suite(w.conn)
    assert ok, "fiduciary on walked db: %s" % lines[-1]
    return "fiduciary suite on the walked db: " + lines[-1]


STEPS = [step_install, step_client_matter, step_accounts,
         step_fund_operating, step_trust_request_online, step_settlement,
         step_bill_earn_out, step_disbursement, step_invoice_pdf,
         step_reconciliation, step_audit_continuity, step_fiduciary]


def main():
    t0 = time.perf_counter()
    lines = []
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        w = Walk(td)
        try:
            for step in STEPS:
                s0 = time.perf_counter()
                try:
                    msg = step(w)
                except Exception as ex:
                    lines.append("FAIL %-28s %s: %s"
                                 % (step.__name__, type(ex).__name__, ex))
                    lines.append("anchor-billing: FAIL")
                    REPORT.write_text("\n".join(lines) + "\n")
                    print("\n".join(lines))
                    sys.exit(1)
                lines.append("PASS %-28s %6.3fs  %s"
                             % (step.__name__, time.perf_counter() - s0,
                                msg))
        finally:
            if w.conn is not None:
                w.conn.close()
    total = time.perf_counter() - t0
    verdict = "PASS" if total < BUDGET_SECONDS else "OVER BUDGET"
    lines.append("anchor-billing: %s (%.3fs of %ds budget)"
                 % (verdict, total, BUDGET_SECONDS))
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
