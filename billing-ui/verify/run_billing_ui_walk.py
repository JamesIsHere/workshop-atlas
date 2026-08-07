"""Verifier 1: the scripted billing UI walk (goal.md, ratified
2026-08-04). Oracle-first (op rule 7): every demo-walk step is
enumerated HERE before its screens exist, and the route names this
file drives ARE the interface contract for P1/P2.

Steps whose screens are unbuilt raise Pending (probe: authed GET
returning the app_ui 404 page); the runner exits 0 only when every
step PASSES and the float sweep passes. Expected at P0 close:
setup/auth and contact/matter steps green (casework-ui screens),
every billing step PENDING, exit 1, verdict ON TRACK.

The walk drives the UI exactly as a browser would -- GETs, form
POSTs, cookies, redirects. Module/db access is for ASSERTIONS only.
Amount story mirrors verify/run_anchor_billing.py (casework-billing
verifier 3): consult 500.00 direct -> retainer 5,000.00 online ->
settle gross/fee 150.30 -> bill 3,000.00 earn-out -> disburse
1,200.00 -> client funds 800.00.

Run: python verify/run_billing_ui_walk.py
Writes billing-ui-walk-report.txt beside it.
"""

import http.cookiejar
import re
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS = HERE.parent.parent
CASEWORK_UI = ATLAS / "casework-ui"
CWB_VERIFY = ATLAS / "casework-billing" / "verify"
sys.path.insert(0, str(CASEWORK_UI))
sys.path.insert(0, str(CWB_VERIFY))

import app_ui  # noqa: F401, E402  (wires casework onto sys.path)
from app_ui import server as ui_server  # noqa: E402
import run_fiduciary as fid  # noqa: E402

REPORT = HERE / "billing-ui-walk-report.txt"

ADMIN = {"name": "Billing Walk Admin",
         "email": "billing.walk@synthetic.test",
         "password": "billing-walk-pass"}

CODE_RE = re.compile(r"verification code is (\d{6})")

# Tier-3 fence: deferred entries must have NO route (goal.md scope
# ruling 2026-08-03). Authed GETs here must land on the 404 page.
TIER3_PATHS = ["/billing/settings", "/billing/reminders",
               "/billing/plans", "/billing/late-fees",
               "/billing/bulk", "/billing/numbering",
               "/billing/translations", "/billing/permissions"]


class Pending(Exception):
    """Screen not built yet -- expected before its phase lands."""


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Browser:
    """Cookie-carrying HTTP client; follows redirects; 404 is a
    return value here (the Pending probe), never an exception."""

    def __init__(self, base):
        self.base = base
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar))

    def _open(self, req):
        try:
            with self.opener.open(req, timeout=10) as r:
                return r.status, r.geturl(), r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.geturl(), e.read().decode("utf-8")

    def get(self, path):
        return self._open(self.base + path)

    def post(self, path, data):
        body = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(self.base + path, data=body,
                                     method="POST")
        req.add_header("Content-Type",
                       "application/x-www-form-urlencoded")
        return self._open(req)

    def get_bytes(self, path):
        with self.opener.open(self.base + path, timeout=10) as r:
            return r.read()


def probe(w, path):
    """GET path; raise Pending on the 404 page (screen unbuilt).
    Returns the page for further assertions."""
    status, url, page = w.browser.get(path)
    if status == 404:
        raise Pending(f"{path} not built")
    assert status == 200, f"{path}: HTTP {status}"
    return page


def need(value, what):
    """Upstream-state guard: a step whose input never got created
    (because an upstream screen is unbuilt) is pending, not failed."""
    if value is None:
        raise Pending(f"upstream not walked yet ({what})")
    return value


class Walk:
    def __init__(self, workdir):
        self.workdir = Path(workdir)
        self.httpd = None
        self.conn = None
        self.browser = None
        self.contact_id = None
        self.matter_id = None
        self.iolta = None
        self.op = None
        self.consult_id = None
        self.trust_request_id = None
        self.bill_id = None
        self.settled = None
        self.disbursed = None
        self.edited_payment = None


# --- foundation steps (casework-ui screens; green today) ---

def step_setup_login(w):
    status, url, page = w.browser.get("/")
    assert url.endswith("/setup"), url
    w.browser.post("/setup", {"name": ADMIN["name"],
                              "email": ADMIN["email"],
                              "password": ADMIN["password"]})
    _s, url, page = w.browser.post("/enroll-mfa", {})
    m = CODE_RE.search(page)
    assert m is not None, "MFA code not shown"
    _s, url, page = w.browser.post("/mfa", {"code": m.group(1)})
    assert url.endswith("/") and "Dashboard" in page, url
    return "fresh db; admin created; MFA enrolled; dashboard reached"


def step_client_matter(w):
    _s, url, page = w.browser.post("/contacts/new", {
        "given_name": "Vera", "family_name": "Synthetic",
        "email": "vera.client@synthetic.test", "phone": "+1-555-0400"})
    m = re.search(r"/contacts/(\d+)$", url)
    assert m is not None, url
    w.contact_id = int(m.group(1))
    _s, url, page = w.browser.post("/matters/new", {
        "name": "Vera Synthetic I-130",
        "contact_id": str(w.contact_id), "description": "billing walk"})
    m = re.search(r"/matters/(\d+)$", url)
    assert m is not None, url
    w.matter_id = int(m.group(1))
    return (f"contact {w.contact_id} + matter {w.matter_id} via"
            f" existing screens")


# --- billing steps (routes ARE the P1/P2 contract; Pending today) ---

def step_billing_landing(w):
    page = probe(w, "/billing")
    assert "Billing" in page, "billing landing missing heading"
    _s, _u, dash = w.browser.get("/")
    assert "href='/billing'" in dash, "Billing absent from nav"
    return "billing area reachable; nav carries Billing"


def step_accounts(w):
    probe(w, "/billing/accounts/new")
    w.browser.post("/billing/accounts/new", {
        "kind": "trust_bank", "label": "SYNTH IOLTA"})
    w.browser.post("/billing/accounts/new", {
        "kind": "operating_bank", "label": "SYNTH Operating"})
    rows = w.conn.execute(
        "SELECT id, kind FROM ledger_accounts WHERE kind IN"
        " ('trust_bank','operating_bank') ORDER BY id").fetchall()
    assert len(rows) == 2, f"bank accounts: {len(rows)}"
    w.iolta = [r["id"] for r in rows if r["kind"] == "trust_bank"][0]
    w.op = [r["id"] for r in rows
            if r["kind"] == "operating_bank"][0]
    page = probe(w, "/billing/trust")
    assert "SYNTH IOLTA" in page and "SYNTH Operating" in page
    assert "0.00" in page, "zero balances not rendered"
    return f"trust bank {w.iolta} + operating {w.op} created by click"


def step_consult_bill_direct(w):
    probe(w, "/billing/invoices/new")
    _s, url, page = w.browser.post("/billing/invoices/new", {
        "invoice_type": "bill", "contact_id": str(w.contact_id),
        "issued_date": "2026-08-01"})
    m = re.search(r"/billing/invoices/(\d+)$", url)
    assert m is not None, f"invoice create landed on {url}"
    w.consult_id = int(m.group(1))
    # F-1 redesign (2026-08-04): state A is build-only -- the add
    # form leads, and NO collect surface exists yet.
    assert "Charges build the bill" in page, \
        "new bill does not explain the charge-before-payment sequence"
    assert "<h1>Collect" not in page, \
        "Collect card appeared before the bill had a balance"
    assert ">Record payment</button>" not in page, \
        "payment submission appeared before the bill had a balance"
    _s, _u, page = w.browser.post(
        f"/billing/invoices/{w.consult_id}/charges", {
        "charge_type": "service", "description": "SYNTH consultation",
        "amount": "500.00", "charge_date": "2026-08-01"})
    # rendered dates are MM/DD/YYYY (gated item A); the POST above
    # stays ISO -- that is what a browser submits from a date input
    assert "SYNTH consultation" in page and "08/01/2026" in page
    assert "<h1>Collect $500.00</h1>" in page \
        and ">Record payment</button>" in page, \
        "Collect card did not appear after the charge"
    _s, _u, page = w.browser.post(
        f"/billing/invoices/{w.consult_id}/pay", {
            "method": "direct", "amount": "500.00",
            "payment_date": "2026-08-01",
            "destination_account_id": str(w.op)})
    assert "Paid" in page, "consult bill not marked paid"
    assert "500.00" in page
    return f"consult bill {w.consult_id} paid direct; operating funded"


def step_trust_request_online(w):
    need(w.iolta, "accounts")
    _s, url, page = w.browser.post("/billing/invoices/new", {
        "invoice_type": "trust_request",
        "contact_id": str(w.contact_id), "issued_date": "2026-08-01",
        "trust_level": "client", "trust_account_id": str(w.iolta)})
    m = re.search(r"/billing/invoices/(\d+)$", url)
    assert m is not None, url
    w.trust_request_id = int(m.group(1))
    assert "Trust Request" in page and "Deposits to" in page
    assert "Charges build the trust request" in page
    _s, _u, page = w.browser.post(
        f"/billing/invoices/{w.trust_request_id}/charges", {
        "charge_type": "service",
        "description": "SYNTH retainer request", "amount": "5000.00",
        "charge_date": "2026-08-01"})
    assert "SYNTH retainer request" in page and "08/01/2026" in page
    assert "Record deposit" in page, \
        "firm-side direct-deposit control missing after charge"
    assert "Create client link" in page, \
        "client-link action does not match the walk sheet"
    _s, _u, page = w.browser.post(
        f"/billing/invoices/{w.trust_request_id}/share", {})
    # Share tokens are casework's SYNTH-INV-<id>-<n> format (frozen
    # billing.share_invoice) -- P0 drafted this as hex by analogy to
    # intake tokens; corrected 2026-08-04 (s3). The follow-through
    # client POST below still proves the link actually pays.
    m = re.search(r"(http://127\.0\.0\.1:\d+/invoice/[A-Za-z0-9-]+)",
                  page)
    assert m is not None, "client pay link not shown after share"
    link = m.group(1)
    client = Browser("")
    status, _u, page = client._open(urllib.request.Request(link))
    assert status == 200, f"client invoice GET returned {status}"
    assert "Synthetic payment token" in page, \
        "client payment field lacks its walk-sheet label"
    assert "SYNTHETIC-VISA-DEMO" in page, \
        "client payment field lacks the exact demo token hint"
    assert "This is not a real card number" in page, \
        "client payment form does not explain the simulator boundary"
    assert ">Pay</button>" in page, "client payment action missing"
    status, _u, page = client._open(urllib.request.Request(
        link + "/pay",
        data=urllib.parse.urlencode(
            {"sim_token": "", "kind": "card"}).encode(),
        method="POST", headers={"Content-Type":
                                "application/x-www-form-urlencoded"}))
    assert status == 200
    assert "enter a synthetic payment token beginning with SYNTHETIC-" \
        in page, "blank token does not return an actionable correction"
    status, _u, page = client._open(urllib.request.Request(
        link + "/pay",
        data=urllib.parse.urlencode(
            {"sim_token": "SYNTHETIC-VISA-DEMO",
             "kind": "card"}).encode(),
        method="POST", headers={"Content-Type":
                                "application/x-www-form-urlencoded"}))
    assert status == 200 and "Payment received" in page, page[:200]
    _s, _u, page = w.browser.get(
        f"/billing/invoices/{w.trust_request_id}")
    assert "Paid" in page, "trust request not marked paid firm-side"
    assert "card" in page.lower(), \
        "online payment status line missing (r2 ruling)"
    return ("retainer 5,000.00 paid by the client over the frozen"
            " client surface; firm sees Paid + card status line")


def step_settlement(w):
    need(w.trust_request_id, "trust request")
    page = probe(w, "/billing/trust")
    assert "Run settlement" in page, "settlement affordance missing"
    _s, _u, page = w.browser.post("/billing/settle", {})
    from app import billing as cwb
    assert cwb.account_balance(w.conn, w.iolta) == 500000
    fee = 15030
    assert cwb.account_balance(w.conn, w.op) == 50000 - fee
    page = probe(w, "/billing/trust")
    assert "5,000.00" in page, "trust balance not rendered"
    assert "349.70" in page, "operating net-of-fee not rendered"
    return "settled by click: gross 5,000.00 to trust; fee 150.30"


def step_time_entry(w):
    probe(w, "/billing/time/new")
    _s, _u, page = w.browser.post("/billing/time/new", {
        "work_date": "2026-08-02", "duration": "2h", "rate": "250.00",
        "description": "SYNTH case work",
        "contact_id": str(w.contact_id),
        "matter_id": str(w.matter_id)})
    # gated item D: a bare number is accepted as hours (the UI
    # normalizes "2" -> "2h" before the corpus-pinned core parser)
    w.browser.post("/billing/time/new", {
        "work_date": "2026-08-02", "duration": "2", "rate": "100.00",
        "description": "SYNTH bare-number hours",
        "matter_id": str(w.matter_id)})
    page = probe(w, "/billing/time")
    assert "SYNTH case work" in page and "500.00" in page
    assert "SYNTH bare-number hours" in page and "200.00" in page, \
        "bare-number duration was not accepted as hours"
    return ("2h at 250.00/h entered by click; bare '2' at 100.00/h"
            " accepted as hours (200.00)")


def step_bill_import_earn_out(w):
    need(w.settled if w.settled is not None else
         (True if w.trust_request_id else None), "settlement")
    probe(w, "/billing/charges/saved")
    w.browser.post("/billing/charges/saved", {
        "description": "SYNTH I-130 preparation", "amount": "2500.00",
        "charge_type": "service"})
    _s, url, page = w.browser.post("/billing/invoices/new", {
        "invoice_type": "bill", "contact_id": str(w.contact_id),
        "matter_id": str(w.matter_id), "issued_date": "2026-08-02"})
    m = re.search(r"/billing/invoices/(\d+)$", url)
    assert m is not None, url
    w.bill_id = int(m.group(1))
    saved_id = w.conn.execute(
        "SELECT id FROM saved_charges").fetchone()[0]
    entry_id = w.conn.execute(
        "SELECT id FROM time_entries").fetchone()[0]
    _s, _u, page = w.browser.post(
        f"/billing/invoices/{w.bill_id}/import", {
            "saved_charge": str(saved_id), "time_entry": str(entry_id)})
    assert "3,000.00" in page, "imported total not rendered"
    _s, _u, page = w.browser.post(
        f"/billing/invoices/{w.bill_id}/pay", {
            "method": "trust_transfer", "amount": "3000.00",
            "payment_date": "2026-08-03",
            "source_account_id": str(w.iolta),
            "source_trust_level": "client",
            "destination_account_id": str(w.op)})
    assert "Paid" in page, "bill not paid after earn-out"
    page = probe(w, "/billing/trust")
    assert "2,000.00" in page, "client funds after earn-out missing"
    return "bill 3,000.00 (saved charge + imported 2h) earned out"


def step_disbursement(w):
    need(w.bill_id, "earn-out bill")
    probe(w, "/billing/trust/disburse")
    _s, _u, page = w.browser.post("/billing/trust/disburse", {
        "account_id": str(w.iolta), "amount": "1200.00",
        "disburse_date": "2026-08-04",
        "contact_id": str(w.contact_id),
        "counterparty": "SYNTH-USCIS",
        "memo": "SYNTH I-130 filing fee"})
    w.disbursed = True
    page = probe(w, "/billing/trust")
    assert "800.00" in page, "client funds after disbursement missing"
    return "1,200.00 disbursed to SYNTH-USCIS; client funds 800.00"


def step_payment_edit_trail(w):
    need(w.consult_id, "consult bill")
    pay_id = w.conn.execute(
        "SELECT id FROM invoice_payments WHERE invoice_id=?"
        " ORDER BY id", (w.consult_id,)).fetchone()[0]
    page = probe(w, f"/billing/payments/{pay_id}")
    _s, _u, page = w.browser.post(
        f"/billing/payments/{pay_id}/edit", {
            "payment_date": "2026-08-02"})
    for word in ("reversal", "repost"):
        assert word in page.lower(), f"correction trail: {word} missing"
    w.edited_payment = pay_id
    # Correction model (P0 drafting error 3, corrected 2026-08-04
    # s3): edit_payment UPDATES the one payment row (audited) and
    # corrects the JOURNAL by reversal + repost -- the evidence is
    # journal entries, not extra payment rows.
    reversals = w.conn.execute(
        "SELECT count(*) FROM journal_entries WHERE reverses_entry_id"
        " IS NOT NULL").fetchone()[0]
    reposts = w.conn.execute(
        "SELECT count(*) FROM journal_entries WHERE replaces_entry_id"
        " IS NOT NULL").fetchone()[0]
    assert reversals >= 1 and reposts >= 1, \
        f"edit did not reverse+repost ({reversals} reversals," \
        f" {reposts} reposts)"
    mutated = w.conn.execute(
        "SELECT count(*) FROM journal_entries e JOIN audit_log a ON"
        " a.entity_type='journal_entries' AND a.entity_id=e.id AND"
        " a.action='update'").fetchone()[0]
    assert mutated == 0, f"posted entries mutated: {mutated}"
    return ("payment date edited via UI; screen shows original +"
            " reversing + repost -- no posted row mutated")


def step_invoice_pdf(w):
    need(w.bill_id, "earn-out bill")
    _s, _u, page = w.browser.get(f"/billing/invoices/{w.bill_id}")
    assert f"/billing/invoices/{w.bill_id}/pdf" in page, \
        "PDF download link missing"
    content = w.browser.get_bytes(
        f"/billing/invoices/{w.bill_id}/pdf")
    assert content[:5] == b"%PDF-", content[:16]
    import tempfile as tf
    from pypdf import PdfReader
    with tf.TemporaryDirectory() as td:
        p = Path(td) / "invoice.pdf"
        p.write_bytes(content)
        text = "\n".join(pg.extract_text()
                         for pg in PdfReader(str(p)).pages)
    assert "SYNTH I-130 preparation" in text
    assert "Balance Due: 0.00" in text
    # gated item H: the client's remaining trust rides the document
    # (relabeled "Remaining in Trust" at James's order, 2026-08-07 s8)
    assert "Remaining in Trust: 800.00" in text, \
        "client trust balance missing from the invoice PDF"
    return f"invoice PDF downloaded ({len(content)} bytes), read back"


def step_ledger_drilldown(w):
    need(w.disbursed, "disbursement")
    page = probe(w, f"/billing/trust/{w.iolta}")
    assert "Vera" in page, "client sub-ledger missing"
    assert "800.00" in page, "sub-ledger balance missing"
    assert "(1,200.00)" in page, \
        "disbursement not parenthesized (accounting negatives)"
    m = re.search(r"/billing/journal/(\d+)", page)
    assert m is not None, "journal entry link missing from ledger"
    page = probe(w, f"/billing/journal/{m.group(1)}")
    assert "debit" in page.lower() and "credit" in page.lower(), \
        "journal detail does not show double-entry legs"
    return ("ledger drill-down: account -> sub-ledger -> journal"
            " detail with debit/credit legs; negatives parenthesized")


def step_reconciliation(w):
    need(w.disbursed, "disbursement")
    page = probe(w, "/billing/recon")
    assert "SYNTH IOLTA" in page and "SYNTH Operating" in page
    assert "holds" in page.lower(), "identity verdict not rendered"
    return "three-way reconciliation screen renders; identity holds"


def step_tier3_fence(w):
    leaks = []
    for path in TIER3_PATHS:
        status, _u, _p = w.browser.get(path)
        if status != 404:
            leaks.append(f"{path} ({status})")
    assert not leaks, f"tier-3 routes leaked: {leaks}"
    return f"{len(TIER3_PATHS)} deferred routes correctly absent"


def step_billing_audit_chain(w):
    need(w.disbursed, "disbursement")
    def first_id(where):
        row = w.conn.execute(
            "SELECT MIN(id) FROM audit_log WHERE " + where).fetchone()
        return row[0]
    # entity_type carries the raw table name (schema triggers_for) --
    # P0 drafted logical names; corrected 2026-08-04 (s3).
    chain = [
        ("bank account", first_id("entity_type='ledger_accounts'"
                                  " AND action='insert'")),
        ("invoice", first_id("entity_type='invoices'"
                             " AND action='insert'")),
        ("payment", first_id("entity_type='invoice_payments'"
                             " AND action='insert'")),
    ]
    missing = [name for name, aid in chain if aid is None]
    assert not missing, f"audit rows missing: {missing}"
    ids = [aid for _, aid in chain]
    assert ids == sorted(ids), f"chain out of story order: {ids}"
    return f"billing audit legs present, story-ordered ({ids})"


def step_fiduciary_on_walked(w):
    n = w.conn.execute(
        "SELECT count(*) FROM journal_entries").fetchone()[0]
    if n == 0:
        raise Pending("no billing activity to audit yet")
    ok, lines = fid.run_suite(w.conn)
    assert ok, "fiduciary on walked db: %s" % lines[-1]
    return "fiduciary suite on the UI-walked db: " + lines[-1]


STEPS = [
    ("setup + login", step_setup_login),
    ("client + matter (existing UI)", step_client_matter),
    ("billing landing + nav", step_billing_landing),
    ("bank accounts by click", step_accounts),
    ("consult bill paid direct", step_consult_bill_direct),
    ("trust request paid online", step_trust_request_online),
    ("settlement by click", step_settlement),
    ("time entry", step_time_entry),
    ("bill import + earn-out", step_bill_import_earn_out),
    ("disbursement", step_disbursement),
    ("payment edit = reversal trail", step_payment_edit_trail),
    ("invoice PDF", step_invoice_pdf),
    ("ledger drill-down", step_ledger_drilldown),
    ("reconciliation screen", step_reconciliation),
    ("tier-3 fence", step_tier3_fence),
    ("billing audit chain", step_billing_audit_chain),
    ("fiduciary on walked db", step_fiduciary_on_walked),
]


# --- float sweep (goal.md: floats never touch money) ---

FLOAT_RE = re.compile(r"float\(")
TRUEDIV_100_RE = re.compile(r"[^/]/\s*100(?!\d)")


def float_sweep():
    hits = []
    app_ui_dir = CASEWORK_UI / "app_ui"
    for py in sorted(app_ui_dir.rglob("*.py")):
        for i, line in enumerate(
                py.read_text(encoding="utf-8").splitlines(), 1):
            if FLOAT_RE.search(line):
                hits.append(f"{py.name}:{i} float()")
            if TRUEDIV_100_RE.search(line) and "//" not in line:
                hits.append(f"{py.name}:{i} true division by 100")
    return ("float-sweep", not hits,
            "no float() and no true /100 in app_ui"
            if not hits else f"violations: {', '.join(hits)}")


def main():
    lines = ["# billing-ui-walk-report -- verifier 1", ""]
    counts = {"PASS": 0, "PENDING": 0, "FAIL": 0}
    total = 0.0
    with tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True) as td:
        w = Walk(td)
        lines.append(f"run started: {_now()}")
        lines.append("")
        w.httpd = ui_server.make_server(w.workdir / "billing-walk.db")
        w.conn = w.httpd.app_conn
        thread = threading.Thread(target=w.httpd.serve_forever,
                                  daemon=True)
        thread.start()
        ui_server.serve_client(w.httpd)
        try:
            w.browser = Browser(
                f"http://{w.httpd.server_address[0]}:"
                f"{w.httpd.server_address[1]}")
            for name, fn in STEPS:
                t0 = time.perf_counter()
                try:
                    detail = fn(w)
                    status = "PASS"
                except Pending as p:
                    detail = str(p)
                    status = "PENDING"
                except Exception as e:
                    detail = f"{type(e).__name__}: {e}"
                    status = "FAIL"
                elapsed = time.perf_counter() - t0
                total += elapsed
                counts[status] += 1
                lines.append(f"{status:7s} {name:32s} {elapsed:7.3f}s"
                             f"  {detail}")
                if status == "FAIL":
                    break
        finally:
            w.httpd.client_httpd.shutdown()
            w.httpd.client_httpd.server_close()
            w.httpd.shutdown()
            w.httpd.server_close()
            w.conn.close()

    lines.append("")
    lines.append("# supporting sweeps")
    sname, sok, sdetail = float_sweep()
    lines.append(f"{'PASS' if sok else 'FAIL':4s} {sname}: {sdetail}")
    lines.append("")
    lines.append(f"steps: {counts['PASS']} pass, {counts['PENDING']}"
                 f" pending, {counts['FAIL']} fail; total {total:.3f}s")
    green = (counts["FAIL"] == 0 and counts["PENDING"] == 0 and sok)
    ok_now = counts["FAIL"] == 0 and sok
    verdict = "GREEN" if green else ("ON TRACK (pending screens)"
                                     if ok_now else "FAIL")
    lines.append(f"verdict: {verdict}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8",
                      newline="\n")
    print(f"billing-ui-walk: {counts['PASS']} pass,"
          f" {counts['PENDING']} pending, {counts['FAIL']} fail;"
          f" float-sweep {'pass' if sok else 'FAIL'};"
          f" verdict {verdict}")
    print(f"report: {REPORT}")
    return 0 if green else 1


if __name__ == "__main__":
    sys.exit(main())
