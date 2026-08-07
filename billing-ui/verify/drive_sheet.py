"""Verifier: the sheet-coupling drive (permanent, added 2026-08-07
after walk attempt 2; the 2026-08-06 drive was a scratch script and
evaporated with its session -- this one is standing machinery).

Drives demo-walk-protocol.md's 32 steps against a live server on a
scratch db, with two properties verifier 1 (run_billing_ui_walk.py)
deliberately does not have:

1. RECOVERY RAIL: every step is entered FROM SCRATCH -- address bar,
   then the sheet's own Go:/If lost: route, asserting each named
   waypoint on the page it should appear on -- never from wherever
   the previous step finished. Attempt 2 (2026-08-07) showed a
   human driver reorients via the menu and leaves the scripted
   screen; a sheet route that only works mid-flow is a defect.
2. SHEET LOCK: the drive refuses to run if the walk-sheet section
   of demo-walk-protocol.md changed since this driver was last
   synced to it (sha256 below). Editing the sheet without
   re-syncing the driver fails loudly instead of drifting silently.
   To re-sync: verify the edited sheet's steps against this file,
   then update EXPECTED_SHEET_SHA to the printed value.

Also locked in, the attempt-2 regression set:
- date prefills are exactly what the sheet claims (invoice forms,
  payment folds, time, disburse start on today; charge dates copy
  the issue date);
- DATE COUPLING (gated item A, 2026-08-07): every date the sheet
  types or names is MM/DD/YYYY (the lock check scans the sheet
  section for ISO strays), and every billing page this drive
  fetches is scanned for visible ISO dates -- rendered text must
  be MM/DD/YYYY. Date-input value attributes are exempt: they are
  ISO by HTML spec and the browser localizes the widget. The ISO
  constants in this file's POSTs are exactly what a browser
  submits when the driver types the sheet's MM/DD/YYYY into a
  US-locale date box -- the submitted form, not the typed form;
- INVOICE IDENTIFICATION (item B 2026-08-07, superseded same day
  by the item-10 BUILD): the sheet names invoices by their stored
  display code (B0001/T0001, invoice-codes.md) -- stamped at
  creation, never shifted by a stray invoice (attempt 3's defect,
  twice cured). The driver locates list rows exactly the sheet's
  way (invoice_row, by code), cross-checks the find against the
  id the walk created, and crumb checks pin EXACT codes;
- the trust request is still UNPAID when the client link is
  created (attempt 2 recorded a firm-side deposit first, emptying
  Part F of anything to settle);
- checkpoint 17: the retainer's payment line reads card (online,
  simulated processor), never direct.

Run: python verify/drive_sheet.py
Writes drive-sheet-report.txt beside it.
"""

import hashlib
import re
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent

from run_billing_ui_walk import Browser, ui_server  # noqa: E402

REPORT = HERE / "drive-sheet-report.txt"
SHEET = HERE / "demo-walk-protocol.md"

EXPECTED_SHEET_SHA = "f7f821edb1e9"

CODE_RE = re.compile(r"class='code-display'>(\d{6})<")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
VALUE_ATTR = re.compile(r"value='[^']*'")


class DateScanBrowser(Browser):
    """The firm-side browser, with the date-coupling assertion baked
    into every fetch: no billing page may show an ISO date outside a
    date-input value attribute (those are ISO by HTML spec; the
    widget localizes)."""

    def _open(self, req):
        status, url, page = super()._open(req)
        if "/billing" in url:
            visible = VALUE_ATTR.sub("value=''", page)
            m = ISO_DATE.search(visible)
            assert m is None, (f"ISO date {m.group()} rendered"
                               f" visibly on {url}")
        return status, url, page


def sheet_sha():
    text = SHEET.read_text(encoding="utf-8")
    section = text[text.index("## Walk sheet"):
                   text.index("## Timing marks")]
    return hashlib.sha256(section.encode("utf-8")).hexdigest()[:12]


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class Drive:
    def __init__(self):
        self.b = None
        self.client = None
        self.conn = None
        self.contact_id = None
        self.matter_id = None
        self.iolta = None
        self.op = None
        self.pay_link = None
        self.payment_id = None
        self.consult_inv = None
        self.trust_inv = None
        self.work_inv = None


def _see(page, *needles):
    for n in needles:
        assert n in page, f"expected {n!r} on this page"
    return page


def enter(d, *hops):
    """The recovery rail: start at the address bar (GET /) and walk
    the sheet's route, asserting each waypoint label is present on
    the page you'd be looking at before following its link."""
    _s, _u, page = d.b.get("/")
    for needle, path in hops:
        _see(page, needle)
        _s, _u, page = d.b.get(path)
    return page


# routes as the sheet gives them (menu -> on-page waypoints)
BILLING = [(">Billing<", "/billing")]
TRUST = BILLING + [("Trust accounting", "/billing/trust")]
NEW_INVOICE = BILLING + [("New invoice", "/billing/invoices/new")]


# the invoice list's row shape (billing_landing): display-code link,
# type pill, client link, issued date. The locator reads it the way
# the sheet tells the driver to -- by the stored display code
# (gated item 10 BUILD, 2026-08-07; supersedes the item-B type+date
# locate, which one screen redesign away from ambiguity).
ROW_RE = re.compile(
    r"<tr><td><a href='/billing/invoices/(\d+)'>([BT]\d{4,})</a></td>"
    r"<td><span class='pill [a-z]+'>(Bill|Trust Request)</span></td>"
    r"<td><a href='/contacts/\d+'>[^<]+</a></td>"
    r"<td>(\d{2}/\d{2}/\d{4})</td>")


def invoice_row(page, code):
    """Locate an invoice the sheet's way (item 10, 2026-08-07): by
    its stored display code, which no stray invoice can shift --
    codes are stamped at creation and never reused. Exactly one row
    must match."""
    hits = [m for m in ROW_RE.finditer(page) if m.group(2) == code]
    assert len(hits) == 1, f"code {code}: {len(hits)} rows match"
    return int(hits[0].group(1))


def enter_invoice(d, code, tab=None, expect=None):
    """From scratch to an invoice page by the sheet's route: address
    bar -> Billing (-> tab) -> locate the row by display code ->
    follow its link. expect cross-checks the located id against the
    one the walk created."""
    hops = list(BILLING)
    if tab:
        # tabs carry live counts ("Paid (2)") -- pin the label up to
        # its count so the waypoint survives any invoice tally
        hops.append((f">{tab.capitalize()} (", f"/billing?tab={tab}"))
    page = enter(d, *hops)
    iid = invoice_row(page, code)
    if expect is not None:
        assert iid == expect, \
            f"sheet route found invoice {iid}, walk created {expect}"
    _s, _u, page = d.b.get(f"/billing/invoices/{iid}")
    return iid, page


# --- Part A: first run -------------------------------------------------

def s01_03_first_run(d):
    _s, url, page = d.b.get("/")
    assert url.endswith("/setup"), url
    _see(page, "Set up your firm's first account", "Your name",
         "Email", "Password", "Create account")
    d.b.post("/setup", {"name": "Demo Driver",
                        "email": "demo.driver@synthetic.test",
                        "password": "demo-walk-pass"})
    _s, _u, page = d.b.get("/enroll-mfa")
    _see(page, "Set up two-factor authentication", "Show me my code")
    _s, _u, page = d.b.post("/enroll-mfa", {})
    _see(page, "Type the code above", "Verify")
    m = CODE_RE.search(page)
    assert m, "6-digit code not displayed"
    _s, _u, page = d.b.post("/mfa", {"code": m.group(1)})
    _see(page, "Dashboard")
    return "setup -> code shown on screen -> dashboard"


# --- Part B: Vera and her matter ---------------------------------------

def s04_05_new_client(d):
    page = enter(d)  # step 4: the dashboard IS the address-bar page
    _see(page, "New client")
    _s, url, page = d.b.post("/contacts/new", {
        "given_name": "Vera", "family_name": "Synthetic",
        "email": "vera.client@synthetic.test", "phone": "+1-555-0400"})
    m = re.search(r"/contacts/(\d+)$", url)
    assert m, url
    d.contact_id = int(m.group(1))
    return f"contact {d.contact_id} created from the dashboard route"


def s06_07_new_matter(d):
    page = enter(d, (">Clients<", "/contacts"),
                 ("Vera Synthetic", f"/contacts/{d.contact_id}"))
    _see(page, "New matter for this client")
    _s, url, page = d.b.post("/matters/new", {
        "name": "Vera Synthetic I-130",
        "contact_id": str(d.contact_id), "description": ""})
    m = re.search(r"/matters/(\d+)$", url)
    assert m, url
    d.matter_id = int(m.group(1))
    return "matter reached via Clients -> Vera -> button (If lost route)"


# --- Part C: bank accounts ---------------------------------------------

def s08_09_bank_accounts(d):
    for kind, label in (("trust_bank", "SYNTH IOLTA"),
                        ("operating_bank", "SYNTH Operating")):
        page = enter(d, *TRUST,
                     ("New bank account", "/billing/accounts/new"))
        _see(page, "Kind", "Account name", "Create account")
        d.b.post("/billing/accounts/new", {"kind": kind, "label": label})
    rows = d.conn.execute(
        "SELECT id, kind FROM ledger_accounts WHERE kind IN"
        " ('trust_bank','operating_bank') ORDER BY id").fetchall()
    assert len(rows) == 2, f"accounts: {len(rows)}"
    d.iolta = [r["id"] for r in rows if r["kind"] == "trust_bank"][0]
    d.op = [r["id"] for r in rows if r["kind"] == "operating_bank"][0]
    return "both accounts, each entered via the full menu route"


# --- Part D: consult bill, paid direct ---------------------------------

def s10_new_bill(d):
    page = enter(d, *NEW_INVOICE)
    _see(page, "New bill", "New trust request", "Issue date")
    assert f"value='{today()}'" in page, \
        "sheet claims the issue date starts on today; it does not"
    _s, url, page = d.b.post("/billing/invoices/new", {
        "invoice_type": "bill", "contact_id": str(d.contact_id),
        "matter_id": str(d.matter_id), "issued_date": "2026-08-01"})
    m = re.search(r"/billing/invoices/(\d+)$", url)
    assert m, url
    d.consult_inv = int(m.group(1))
    # the sheet pins only the crumb PREFIX -- the app assigns the
    # number and the sheet says any number is correct there
    _see(page, "Billing</a> / Bill B0001")
    return "consult bill via menu route; issue-date prefill holds"


def s11_add_charge(d):
    iid, page = enter_invoice(d, "B0001", tab="all",
                              expect=d.consult_inv)
    _see(page, "Add a charge", "Description", "Amount", "Type", "Date")
    assert "value='2026-08-01'" in page, \
        "sheet claims the charge date copies the issue date"
    _s, _u, page = d.b.post(f"/billing/invoices/{iid}/charges", {
        "charge_type": "service", "description": "SYNTH consultation",
        "amount": "500.00", "charge_date": "2026-08-01"})
    _see(page, "Collect $500.00")
    return "charge added after type+date re-entry; Collect appears"


def s12_pay_direct(d):
    iid, page = enter_invoice(d, "B0001", tab="all",
                              expect=d.consult_inv)
    _see(page, "Collect $500.00",
         "Record a direct payment (check, cash, wire)", "Deposit to")
    assert f"value='{today()}'" in page, \
        "sheet claims the payment date starts on today (the trap)"
    _s, _u, page = d.b.post(f"/billing/invoices/{iid}/pay", {
        "method": "direct", "amount": "500.00",
        "payment_date": "2026-08-01",
        "destination_account_id": str(d.op)})
    _see(page, "Paid")
    return "paid direct on 2026-08-01; payment-date prefill claim holds"


# --- Part E: retainer, paid by the client ------------------------------

def s13_new_trust_request(d):
    page = enter(d, *NEW_INVOICE)
    _see(page, "New trust request", "Deposits to", "Hold funds for",
         "Client-level funds (no specific matter)",
         "Create trust request")
    _s, url, page = d.b.post("/billing/invoices/new", {
        "invoice_type": "trust_request",
        "contact_id": str(d.contact_id), "issued_date": "2026-08-01",
        "trust_level": "client", "trust_account_id": str(d.iolta)})
    m = re.search(r"/billing/invoices/(\d+)$", url)
    assert m, url
    d.trust_inv = int(m.group(1))
    _see(page, "Billing</a> / Trust request T0001")
    return "trust request via menu route; crumb prefix holds"


def s14_retainer_charge(d):
    # the sheet finds the trust request by its code
    iid, page = enter_invoice(d, "T0001", tab="all",
                              expect=d.trust_inv)
    _s, _u, page = d.b.post(f"/billing/invoices/{iid}/charges", {
        "charge_type": "service",
        "description": "SYNTH retainer request", "amount": "5000.00",
        "charge_date": "2026-08-01"})
    _see(page, "Collect $5,000.00", "Send the request to the client")
    assert re.search(r"<details class='fold' open><summary>Send the"
                     r" request to the client", page), \
        "sheet claims the send fold is already open"
    return "retainer charge in; send fold open as the sheet claims"


def s15_client_link(d):
    iid, page = enter_invoice(d, "T0001", tab="all",
                              expect=d.trust_inv)
    _see(page, "Create client link")
    _see(page, "Outstanding")  # regression: NOT paid before the client pays
    assert "Paid</span>" not in page.split("Payments")[0], \
        "trust request reads Paid before the client paid (divergence)"
    _s, _u, page = d.b.post(f"/billing/invoices/{iid}/share", {})
    m = re.search(r"(http://127\.0\.0\.1:\d+/invoice/[A-Za-z0-9-]+)",
                  page)
    assert m, "client pay link not shown"
    # gated item G: the link lives in the boxed select-all field
    assert "class='copylink'" in page, \
        "client link is not in the boxed copy field the sheet teaches"
    d.pay_link = m.group(1)
    return "link created in the copy box; request still Outstanding"


def _client_no_iso(page):
    """Date coupling (item A) extended to the client surface
    (2026-08-07 amendment): what Vera sees is MM/DD/YYYY too."""
    visible = VALUE_ATTR.sub("value=''", page)
    m = ISO_DATE.search(visible)
    assert m is None, (f"ISO date {m.group()} rendered visibly on the"
                       f" client surface")


def s16_vera_pays(d):
    d.client = Browser("")
    import urllib.request, urllib.parse  # noqa: E401
    status, _u, page = d.client._open(
        urllib.request.Request(d.pay_link))
    assert status == 200
    _see(page, "Synthetic payment token", "SYNTHETIC-VISA-DEMO",
         ">Pay</button>")
    # 2026-08-07 amendment (rendering-only): firm-branded page, footed
    # charge table with the retainer line, trust line only when funds
    # are actually held (none yet at this step)
    _see(page, "SYNTH Firm", "SYNTH retainer request", "5,000.00",
         "Balance Due", "class='total'")
    assert "Remaining in Trust" not in page, \
        "trust line shown before any funds are held"
    _client_no_iso(page)
    status, _u, page = d.client._open(urllib.request.Request(
        d.pay_link + "/pay",
        data=urllib.parse.urlencode(
            {"sim_token": "SYNTHETIC-VISA-DEMO", "kind": "card"}
        ).encode(), method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"}))
    assert status == 200 and "Payment received" in page, page[:200]
    # the receipt worth the name: amount, method, reference, remaining
    _see(page, "5,000.00", ">card<", "Reference", "Remaining balance",
         "0.00")
    _client_no_iso(page)
    # the invoice page now records the payment for the client
    status, _u, page = d.client._open(
        urllib.request.Request(d.pay_link))
    assert status == 200
    _see(page, "Payments", ">card<", "5,000.00", ">Paid</span>")
    _client_no_iso(page)
    return ("Vera paid in her own cookie jar; styled receipt +"
            " payment history on her page")


def s17_checkpoint_card(d):
    _iid, page = enter_invoice(d, "T0001", tab="paid",
                               expect=d.trust_inv)
    _see(page, "Paid", "card (online, simulated processor)")
    return "CHECKPOINT holds: payment line reads card, not direct"


# --- Part F: settlement ------------------------------------------------

def s18_settlement(d):
    page = enter(d, *TRUST)
    _see(page, "Processor settlement", "Run settlement",
         "Settlement date", "Back to billing")
    d.b.post("/billing/settle", {})
    page = enter(d, *TRUST)
    _see(page, "5,000.00", "349.70")
    return "settled: gross 5,000.00 in trust; operating 349.70"


# --- Part G: work, bill, earn out --------------------------------------

def s19_record_time(d):
    page = enter(d, *BILLING, (">Time<", "/billing/time"),
                 ("Record time", "/billing/time/new"))
    _see(page, "Date worked", "Time spent", "Hourly rate")
    assert f"value='{today()}'" in page, \
        "sheet claims the work date starts on today"
    d.b.post("/billing/time/new", {
        "work_date": "2026-08-02", "duration": "2h", "rate": "250.00",
        "description": "SYNTH case work",
        "matter_id": str(d.matter_id)})
    return "2h at 250.00 via the menu route; prefill claim holds"


def s20_saved_charge(d):
    page = enter(d, *BILLING,
                 ("Saved charges", "/billing/charges/saved"))
    _see(page, "Save a charge", "Save charge", "Back to billing")
    d.b.post("/billing/charges/saved", {
        "description": "SYNTH I-130 preparation", "amount": "2500.00",
        "charge_type": "service"})
    return "saved charge stored"


def s21_bill_three(d):
    page = enter(d, *NEW_INVOICE)
    _see(page, "New bill")
    _s, url, page = d.b.post("/billing/invoices/new", {
        "invoice_type": "bill", "contact_id": str(d.contact_id),
        "matter_id": str(d.matter_id), "issued_date": "2026-08-02"})
    m = re.search(r"/billing/invoices/(\d+)$", url)
    assert m, url
    d.work_inv = int(m.group(1))
    _see(page, "Billing</a> / Bill B0002")
    # ITEM-B REGRESSION (attempt 3's failure condition, injected on
    # purpose): a stray invoice -- issued today, never charged --
    # once shifted every downstream #N the sheet pinned. From here
    # on, every type+date locate must survive its presence.
    d.b.post("/billing/invoices/new", {
        "invoice_type": "bill", "contact_id": str(d.contact_id)})
    return "work bill created; STRAY bill injected (item-B regression)"


def s22_import(d):
    iid, page = enter_invoice(d, "B0002", tab="all",
                              expect=d.work_inv)
    _see(page, "Import saved charges and time", "Import selected",
         "08/02/2026")  # the sheet names the time entry by this date
    saved = d.conn.execute("SELECT id FROM saved_charges").fetchone()[0]
    entry = d.conn.execute("SELECT id FROM time_entries").fetchone()[0]
    _s, _u, page = d.b.post(f"/billing/invoices/{iid}/import", {
        "saved_charge": str(saved), "time_entry": str(entry)})
    _see(page, "3,000.00", "Balance due:")
    # gated item C: the imported saved charge carries the bill's
    # issue date -- no blank Date cell on the charges table
    assert ("<td>SYNTH I-130 preparation</td><td>service</td>"
            "<td>08/02/2026</td>") in page, \
        "imported saved charge is missing its date on the bill"
    return "both rows imported, both dated; balance 3,000.00"


def s23_earn_out(d):
    iid, page = enter_invoice(d, "B0002", tab="all",
                              expect=d.work_inv)
    _see(page, "Collect $3,000.00", "Pay from client trust (earn-out)",
         "From trust account", "Trust funds held for")
    assert f"value='{today()}'" in page, \
        "sheet claims the earn-out date starts on today"
    _s, _u, page = d.b.post(f"/billing/invoices/{iid}/pay", {
        "method": "trust_transfer", "amount": "3000.00",
        "payment_date": "2026-08-03",
        "source_account_id": str(d.iolta),
        "source_trust_level": "client",
        "destination_account_id": str(d.op)})
    _see(page, "Paid")
    return "earned out 3,000.00 from trust"


# --- Part H: disburse --------------------------------------------------

def s24_disburse(d):
    page = enter(d, *TRUST)
    _see(page, "Client funds", "2,000.00", "Disburse funds")
    page = enter(d, *TRUST,
                 ("Disburse funds", "/billing/trust/disburse"))
    _see(page, "From trust account", "Funds held for client",
         "No matter (funds are client-level)", "Pay to", "Memo",
         "Disburse")
    assert f"value='{today()}'" in page, \
        "sheet claims the disburse date starts on today"
    # sheet (real-bank ruling 2026-08-07): the date stays at today's
    # prefill, so the check is still outstanding at step 32's period
    d.b.post("/billing/trust/disburse", {
        "account_id": str(d.iolta), "amount": "1200.00",
        "disburse_date": today(),
        "contact_id": str(d.contact_id),
        "counterparty": "SYNTH-USCIS",
        "memo": "SYNTH I-130 filing fee"})
    page = enter(d, *TRUST)
    _see(page, "800.00")
    return "disbursed 1,200.00; Vera's funds 800.00"


# --- Part I: the correction --------------------------------------------

def s25_26_find_payment(d):
    _iid, page = enter_invoice(d, "B0001", tab="paid",
                               expect=d.consult_inv)
    m = re.search(r"href='/billing/payments/(\d+)'>08/01/2026<", page)
    assert m, "payment date 08/01/2026 is not a link on the consult bill"
    d.payment_id = int(m.group(1))
    _s, _u, page = d.b.get(f"/billing/payments/{d.payment_id}")
    _see(page, "Correct this payment")
    return "payment found by type+date via Paid tab; date link works"


def s27_28_correct(d):
    _s, _u, page = d.b.post(
        f"/billing/payments/{d.payment_id}/edit",
        {"payment_date": "2026-08-02"})
    _see(page, "Journal trail", "Bank record")
    assert "reverses" in page and "replaces" in page, \
        "correction trail does not show reverses/replaces tags"
    # re-enter from scratch (If lost route) and confirm it persists
    _iid, page = enter_invoice(d, "B0001", tab="paid",
                               expect=d.consult_inv)
    m = re.search(r"href='/billing/payments/(\d+)'>08/02/2026<", page)
    assert m, "corrected date 08/02/2026 is not the link now"
    return "corrected in the open; trail survives re-entry"


# --- Part J: the books -------------------------------------------------

def s29_pdf(d):
    iid, page = enter_invoice(d, "B0002", tab="paid",
                              expect=d.work_inv)
    # gated item H: the client's remaining trust shows on the bill
    # (relabeled "Remaining in Trust" at James's order, 2026-08-07 s8)
    _see(page, "Download PDF", "Remaining in Trust", "800.00")
    content = d.b.get_bytes(f"/billing/invoices/{iid}/pdf")
    assert content[:5] == b"%PDF-", content[:16]
    return f"PDF downloads ({len(content)} bytes)"


def s30_31_ledger(d):
    page = enter(d, *TRUST)
    _see(page, "SYNTH IOLTA ledger")
    _s, _u, page = d.b.get(f"/billing/trust/{d.iolta}")
    _see(page, "800.00")
    m = re.search(r"/billing/journal/(\d+)", page)
    assert m, "no journal entry link on the ledger"
    _s, _u, page = d.b.get(f"/billing/journal/{m.group(1)}")
    assert "debit" in page.lower() and "credit" in page.lower()
    return "ledger -> journal entry; debits and credits shown"


def s32_recon(d):
    page = enter(d, *BILLING, ("Reconciliation", "/billing/recon"))
    _see(page, "SYNTH IOLTA", "SYNTH Operating", "client claims",
         "Back to billing",
         "Bank statement (independent)", "Books (ledger)",
         "Client claims", "Statement balance", "Adjusted bank",
         "Books balance", "Client claims total",
         "(system correction)")
    assert "holds" in page.lower(), "identity verdict missing"
    assert page.count("Adjusted bank") == 2,         "both accounts should carry the vertical bank bridge"
    assert page.count("Client claims total") == 1,         "claims column belongs to the trust card only"
    # period-end mix (real-bank ruling 2026-08-07): the statement
    # must show all three line kinds the sheet points at -- cleared
    # activity, the settlement deposit in transit, the outstanding
    # disbursement check
    assert "no cleared activity this period" not in page, \
        "a statement pane has no cleared lines -- the mix is gone"
    assert ">in transit " in page and "5,000.00" in page, \
        "the settlement deposit is not shown in transit"
    assert ">outstanding " in page and "(1,200.00)" in page, \
        "the disbursement check is not shown outstanding"
    return ("three-pane recon: statement leg, footed columns, ties;"
            " cleared/in-transit/outstanding mix on the period")


STEPS = [
    ("steps 1-3   first run", s01_03_first_run),
    ("steps 4-5   new client", s04_05_new_client),
    ("steps 6-7   new matter", s06_07_new_matter),
    ("steps 8-9   bank accounts", s08_09_bank_accounts),
    ("step 10     new bill", s10_new_bill),
    ("step 11     add charge", s11_add_charge),
    ("step 12     pay direct", s12_pay_direct),
    ("step 13     trust request", s13_new_trust_request),
    ("step 14     retainer charge", s14_retainer_charge),
    ("step 15     client link", s15_client_link),
    ("step 16     vera pays", s16_vera_pays),
    ("step 17     CHECKPOINT card", s17_checkpoint_card),
    ("step 18     settlement", s18_settlement),
    ("step 19     record time", s19_record_time),
    ("step 20     saved charge", s20_saved_charge),
    ("step 21     work bill B0002", s21_bill_three),
    ("step 22     import", s22_import),
    ("step 23     earn-out", s23_earn_out),
    ("step 24     disburse", s24_disburse),
    ("steps 25-26 find payment", s25_26_find_payment),
    ("steps 27-28 correct", s27_28_correct),
    ("step 29     pdf", s29_pdf),
    ("steps 30-31 ledger", s30_31_ledger),
    ("step 32     recon", s32_recon),
]


def main():
    actual = sheet_sha()
    if actual != EXPECTED_SHEET_SHA:
        print(f"SHEET LOCK: demo-walk-protocol.md walk-sheet section"
              f" is {actual}, driver is synced to"
              f" {EXPECTED_SHEET_SHA}.")
        print("The sheet changed without a driver re-sync. Verify the"
              " edited steps against this file, then update"
              " EXPECTED_SHEET_SHA.")
        return 2
    text = SHEET.read_text(encoding="utf-8")
    section = text[text.index("## Walk sheet"):
                   text.index("## Timing marks")]
    stray = ISO_DATE.search(section)
    if stray:
        print(f"DATE COUPLING: the walk sheet contains the ISO date"
              f" {stray.group()} -- every driver-facing date must be"
              f" MM/DD/YYYY (gated item A).")
        return 2
    lines = [f"# drive-sheet-report -- sheet-coupling drive",
             f"# sheet sha {actual}", ""]
    failures = 0
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        httpd = ui_server.make_server(Path(td) / "drive-sheet.db")
        conn = httpd.app_conn
        threading.Thread(target=httpd.serve_forever,
                         daemon=True).start()
        ui_server.serve_client(httpd)
        try:
            d = Drive()
            d.conn = conn
            d.b = DateScanBrowser(f"http://{httpd.server_address[0]}:"
                                  f"{httpd.server_address[1]}")
            for name, fn in STEPS:
                t0 = time.perf_counter()
                try:
                    detail = fn(d)
                    status = "PASS"
                except Exception as e:
                    detail = f"{type(e).__name__}: {e}"
                    status = "FAIL"
                    failures += 1
                lines.append(f"{status:5s} {name:28s} {detail}")
                if status == "FAIL":
                    break
        finally:
            httpd.client_httpd.shutdown()
            httpd.client_httpd.server_close()
            httpd.shutdown()
            httpd.server_close()
            conn.close()
    lines.append("")
    verdict = "GREEN" if failures == 0 else "FAIL"
    lines.append(f"drive-sheet: {len(STEPS) - failures}/{len(STEPS)}"
                 f" groups pass; verdict {verdict}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8",
                      newline="\n")
    print("\n".join(lines[3:]))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
