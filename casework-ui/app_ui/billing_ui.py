"""Billing and trust-accounting screens (billing-ui P1+; program
ruling 2026-08-04: this child extends app_ui in place).

Rendering ONLY: zero SQL here (reads live in reads.py, the one file
the no-logic sweep allows SQL in); every computed money figure comes
from casework's billing/ledger modules; the reconciliation screen
renders what the F7 engine itself computes (reconcile.py imported
from casework-billing/verify -- the screen cannot drift from the
oracle). Writes arrive in P2 and route through casework modules.

Money is integer cents until the moment of formatting. Ledger tables
show plain accounting numbers (negatives parenthesized, no currency
sign per cell); headline tiles carry the $ once.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from app import billing, ledger, period, processor, timekeeping

from app_ui import html, reads

# The recon engine is the fiduciary suite's own (billing-ui goal:
# the screen renders the oracle's numbers, never a reimplementation).
_CWB_VERIFY = Path(__file__).resolve().parent.parent.parent \
    / "casework-billing" / "verify"
if str(_CWB_VERIFY) not in sys.path:
    sys.path.insert(0, str(_CWB_VERIFY))
import reconcile  # noqa: E402
import bank_statement  # noqa: E402  (the statement pane renders the
# same independent witness the recon engine reads -- never the journal)

BILLING_STYLE = """
.tiles { display: flex; gap: 1rem; flex-wrap: wrap; margin: 0 0 1.2rem; }
.tile { background: #ffffff; border: 1px solid #d9dde3; border-radius: 6px;
        padding: 0.9rem 1.3rem; min-width: 11.5rem; flex: 1; }
.tile .label { font-size: 0.78rem; text-transform: uppercase;
               letter-spacing: 0.06em; color: #6a7383; }
.tile .value { font-size: 1.55rem; font-weight: 600; margin-top: 0.2rem;
               font-variant-numeric: tabular-nums; color: #1a1d21; }
.tile .sub { font-size: 0.8rem; color: #6a7383; margin-top: 0.15rem; }
span.money { display: block; text-align: right;
             font-variant-numeric: tabular-nums; white-space: nowrap; }
.pill.paid { background: #e6f4e6; color: #256325; }
.pill.outstanding { background: #fdf3e0; color: #8a5b12; }
.pill.trust { background: #e8eefb; color: #24519e; }
.pill.bill { background: #eef1f5; color: #4a5261; }
.pill.holds { background: #e6f4e6; color: #256325; }
.pill.broken { background: #fdecec; color: #8a2525; }
.pill.refunded { background: #f3e9f7; color: #6b3a86; }
.pill.settling { background: #f3e9f7; color: #6b3a86; }
.pill.clearing { background: #e8eefb; color: #24519e; }
span.chipnote { color: #8a5b12; font-size: 0.8rem;
                white-space: nowrap; }
p.split { color: #6a7383; font-size: 0.95rem; margin: 0.5rem 0 0;
          font-variant-numeric: tabular-nums; }
label.ackrow, p.ackrow { display: block; margin: 0.35rem 0;
                         font-variant-numeric: tabular-nums; }
label.ackrow input, label.pick input { width: auto; padding: 0;
                                       margin-right: 0.45rem; }
.actions { overflow: auto; }
input.copylink { font-family: Consolas, monospace; font-size: 0.9rem;
                 background: #f0f2f5; border: 1px dashed #b9c0cb;
                 margin: 0.4rem 0; }
.actions a.back { float: right; margin-right: 0; }
.tabs { margin: 0 0 0.9rem; border-bottom: 1px solid #d9dde3; }
.tabs a { display: inline-block; padding: 0.3rem 0.2rem;
          margin-right: 1.2rem; text-decoration: none; color: #2456a6; }
.tabs a.on { color: #1a1d21; font-weight: 600; margin-bottom: -1px;
             border-bottom: 2px solid #2456a6; }
.crumbs { font-size: 0.85rem; margin: 0 0 0.8rem; color: #6a7383; }
.crumbs a { color: #2456a6; text-decoration: none; }
.trail { background: #f7f8fa; border-left: 3px solid #2456a6;
         padding: 0.7rem 1rem; margin: 0.9rem 0; }
.trail .why { color: #6a7383; font-size: 0.85rem; }
.identity { font-variant-numeric: tabular-nums; background: #f7f8fa;
            border: 1px solid #d9dde3; border-radius: 6px;
            padding: 0.8rem 1.1rem; margin: 0.6rem 0; }
h2.formhead { font-size: 1rem; margin: 1.2rem 0 0; color: #4a5261;
              border-top: 1px solid #e7eaee; padding-top: 1rem; }
details.fold { border-top: 1px solid #e7eaee; padding: 0.55rem 0 0.3rem; }
details.fold summary { cursor: pointer; color: #2456a6;
                       font-weight: 600; font-size: 0.95rem; }
details.fold summary:hover { text-decoration: underline; }
details.fold .foldbody { padding: 0.6rem 0 0.4rem; }
p.due { font-size: 1.15rem; margin: 0.7rem 0 0;
        font-variant-numeric: tabular-nums; }
label.pick { display: block; margin: 0.35rem 0; font-size: 0.95rem;
             font-variant-numeric: tabular-nums; }
form.inline { display: inline-block; margin-right: 0.6rem; }
form.inline button.primary { margin-top: 0; }
form button.primary { display: block; }
.recon-cols { display: flex; gap: 1.4rem; flex-wrap: wrap;
              align-items: flex-start; margin: 0.6rem 0; }
.recon-col { flex: 1 1 16rem; min-width: 15rem; }
.recon-col h2 { font-size: 0.8rem; text-transform: uppercase;
                letter-spacing: 0.05em; color: #6a7383;
                margin: 0 0 0.4rem; }
table.rec { width: 100%; border-collapse: collapse;
            font-size: 0.9rem; }
table.rec td { padding: 0.3rem 0.4rem; border-bottom: 1px solid
               #eef0f3; vertical-align: top; }
table.rec td.amt { text-align: right; white-space: nowrap;
                   font-variant-numeric: tabular-nums; }
table.rec tr.foot td { border-top: 2px solid #d9dde3;
                       border-bottom: none; font-weight: 600; }
table.rec td.none { color: #6a7383; font-style: italic; }
.tile .go { margin-top: 0.55rem; }
.tile .go a { display: inline-block; background: #eef1f5;
              color: #2456a6; border-radius: 4px;
              padding: 0.25rem 0.7rem; margin-right: 0.4rem;
              text-decoration: none; font-size: 0.85rem; }
.tile .go a:hover { background: #e0e6ee; }
.attend { border-left: 3px solid #8a5b12; background: #fdf3e0;
          padding: 0.7rem 1rem; margin: 0.6rem 0; }
.attend a { color: #2456a6; }
.allties { font-size: 1.05rem; color: #256325; margin: 0.6rem 0; }
p.inflight { color: #6a7383; font-size: 0.9rem; margin: 0.5rem 0 0; }
p.periodline { color: #6a7383; font-size: 0.9rem; margin: 0 0 1rem; }
"""


def cents_of(text):
    """Form amount -> integer cents. Digits, one optional point, up
    to two decimals; $ and , tolerated. Integer math only -- a float
    never touches money (goal.md)."""
    t = (text or "").strip().replace("$", "").replace(",", "")
    if not t:
        raise ValueError("an amount is required")
    whole, _, frac = t.partition(".")
    if len(frac) > 2 or not (whole + frac).isdigit() \
            or not (whole or frac):
        raise ValueError(f"amounts look like 1,234.56 -- not {text!r}")
    return int(whole or "0") * 100 + int((frac + "00")[:2])


def _today():
    """FIRM-LOCAL business date (James's ruling 2026-08-09, s12: a
    signed month-end dated tomorrow is wrong on its face; UTC rolled
    every evening default to the next day). The server runs at the
    firm; system clock = firm clock. Wall-clock TIMESTAMPS (audit,
    sessions) stay UTC -- this is dates only."""
    return datetime.now().strftime("%Y-%m-%d")


def fmt_date(iso):
    """User-facing date: MM/DD/YYYY (gated item A, James 2026-08-07).
    Data stays ISO end to end; this formats at render time only, the
    same boundary fmt_cents is. Date INPUTS are untouched: their
    value attribute is ISO by HTML spec and the browser localizes the
    widget. Strict on purpose -- a value that is not a bare ISO date
    is a data defect and must fail loud, never render half-formatted."""
    if not iso:
        return ""
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%m/%d/%Y")


def fmt_cents(cents):
    """Accounting format, no currency sign: 1,234.56 / (1,234.56)."""
    neg = cents < 0
    d, c = divmod(abs(cents), 100)
    s = f"{d:,}.{c:02d}"
    return f"({s})" if neg else s


def dollars(cents):
    """Headline format: $1,234.56 / ($1,234.56)."""
    neg = cents < 0
    return f"(${fmt_cents(abs(cents))})" if neg else f"${fmt_cents(cents)}"


def fmt_duration(seconds):
    h, m = divmod(seconds // 60, 60)
    return f"{h}h" if m == 0 else f"{h}h {m:02d}m"


def _page(h, title, body, user):
    styled = f"<style>{BILLING_STYLE}</style>" + body
    h._send_page(200, html.page(title, styled, user_name=user["name"],
                                active_href="/billing"))


def _pill(kind, text=None):
    return f"<span class='pill {kind}'>{html.esc(text or kind)}</span>"


def _crumbs(*pairs):
    parts = [html.link(href, text) if href else html.esc(text)
             for text, href in pairs]
    return "<p class='crumbs'>" + " / ".join(parts) + "</p>"


def _status_pill(conn, invoice_id):
    status = billing.invoice_status(conn, invoice_id)
    return _pill(status, status.capitalize())


def _select(label, name, options, selected=None, hint=None,
            blank=None):
    """options: (value, text) pairs; blank adds a '' choice first."""
    h = f"<p class='hint'>{html.esc(hint)}</p>" if hint else ""
    opts = ""
    if blank is not None:
        opts += f"<option value=''>{html.esc(blank)}</option>"
    for value, text in options:
        sel = " selected" if str(value) == str(selected) else ""
        opts += (f"<option value='{html.esc(str(value))}'{sel}>"
                 f"{html.esc(text)}</option>")
    return (f"<label>{html.esc(label)}</label>{h}"
            f"<select name='{name}'>{opts}</select>")


def _type_pill(row):
    return (_pill("trust", "Trust Request")
            if row["invoice_type"] == "trust_request"
            else _pill("bill", "Bill"))


def _noun(inv):
    """One noun per invoice type, everywhere a human reads it (walk
    finding F-1: sheet said bill, screen said Invoice)."""
    return ("Trust request" if inv["invoice_type"] == "trust_request"
            else "Bill")


def _back_to_billing():
    """One obvious route home from every billing sub-area (James's
    snap, 2026-08-07: crumbs and the top menu work, but the four
    sub-area screens need a big button too). Quiet style, floated
    top-right, so it never competes with the screen's primary action."""
    return "<a class='quiet back' href='/billing'>Back to billing</a>"


def _fold(summary, inner, open_=False):
    """Native no-JS disclosure: the page's secondary actions live
    behind <details> so each state shows one primary thing."""
    return (f"<details class='fold'{' open' if open_ else ''}>"
            f"<summary>{summary}</summary>"
            f"<div class='foldbody'>{inner}</div></details>")


# --- screens ----------------------------------------------------------

def billing_landing(h, conn, user, query):
    trust_total = op_total = 0
    for acct in ledger.list_bank_accounts(conn):
        bal = ledger.account_balance(conn, acct["id"])
        if acct["kind"] == "trust_bank":
            trust_total += bal
        else:
            op_total += bal
    rows = reads.invoice_rows(conn)
    status_of = {r["id"]: billing.invoice_status(conn, r["id"])
                 for r in rows}
    outstanding = [r for r in rows
                   if status_of[r["id"]] == "outstanding"]
    out_sum = sum(billing.invoice_balance(conn, r["id"])
                  for r in outstanding)
    tiles = (
        "<div class='tiles'>"
        f"<div class='tile'><div class='label'>Client funds in trust"
        f"</div><div class='value'>{dollars(trust_total)}</div>"
        f"<div class='sub'>held, never the firm's until earned</div>"
        f"</div>"
        f"<div class='tile'><div class='label'>Operating</div>"
        f"<div class='value'>{dollars(op_total)}</div>"
        f"<div class='sub'>firm funds</div></div>"
        f"<div class='tile'><div class='label'>Outstanding</div>"
        f"<div class='value'>{dollars(out_sum)}</div>"
        f"<div class='sub'>{len(outstanding)} open"
        f" invoice{'s' if len(outstanding) != 1 else ''}</div></div>"
        "</div>")

    tab = (query.get("tab", ["outstanding"]))[0]
    if tab not in ("outstanding", "paid", "all"):
        tab = "outstanding"
    # counts on the tabs: an empty filtered tab must say where the
    # invoices ARE, not imply none exist (James's snap, 2026-08-07:
    # tile said 0 open, list said "No invoices here yet" -- a
    # contradiction on one screen)
    counts = {t: sum(1 for s in status_of.values() if s == t)
              for t in ("outstanding", "paid")}
    counts["all"] = len(rows)
    tabs = "<div class='tabs'>" + "".join(
        f"<a class='{'on' if t == tab else ''}'"
        f" href='/billing?tab={t}'>{t.capitalize()}"
        f" ({counts[t]})</a>"
        for t in ("outstanding", "paid", "all")) + "</div>"
    shown = [r for r in rows
             if tab == "all" or status_of[r["id"]] == tab]
    if shown:
        today = _today()
        trows = []
        for r in shown:
            # flow annotation (s11 L3): the outstanding pill carries
            # its age -- overdue beats sent when both apply
            status_cell = _status_pill(conn, r["id"])
            if status_of[r["id"]] == "outstanding":
                if r["due_date"] and r["due_date"] < today:
                    status_cell += (
                        " <span class='chipnote'>overdue"
                        f" {_days_old(r['due_date'], today)}d</span>")
                else:
                    sent = reads.invoice_shares_of(conn, r["id"])
                    if sent:
                        status_cell += (
                            " <span class='chipnote'>sent"
                            f" {fmt_date(sent[0]['created_at'][:10])}"
                            "</span>")
            trows.append([
                html.link(f"/billing/invoices/{r['id']}",
                          r["display_code"]),
                _type_pill(r),
                html.link(f"/contacts/{r['contact_id']}",
                          r["display_name"]),
                html.esc(fmt_date(r["issued_date"])),
                status_cell,
                f"<span class='money'>"
                f"{fmt_cents(billing.invoice_balance(conn, r['id']))}"
                f"</span>",
            ])
        table = html.table(["Invoice", "Type", "Client", "Issued",
                            "Status", "Balance"], trows)
    elif not rows:
        table = html.empty_state(
            "No invoices here yet. Bills and trust requests appear in"
            " this list the moment they are created.")
    elif tab == "outstanding":
        # the good kind of empty -- say so, and say where the rest is
        table = html.empty_state(
            "Nothing outstanding -- every invoice is collected. The"
            " Paid tab has the full record.")
    else:
        table = html.empty_state(
            "Nothing collected yet -- every invoice is still"
            " outstanding.")
    nav = ("<div class='actions'>"
           + f"<a href='/billing/invoices/new'>New invoice</a>"
           + f"<a class='quiet' href='/billing/trust'>Trust"
             f" accounting</a>"
           + f"<a class='quiet' href='/billing/time'>Time</a>"
           + f"<a class='quiet' href='/billing/charges/saved'>Saved"
             f" charges</a>"
           + f"<a class='quiet' href='/billing/recon'>Reconciliation"
             f"</a>"
           + f"<a class='quiet' href='/billing/close'>Period close"
             f"</a></div>")
    body = (f"<h1>Billing</h1>{tiles}"
            f"<div class='card'>{nav}{tabs}{table}</div>")
    _page(h, "Billing", body, user)


def client_money_band(conn, contact_id):
    """The client page's Money card (item-12 object 3; placement A
    ruled s11: one client, one page; the band is the audience
    boundary). Three headline figures, the client-scoped pipeline
    line in the dashboard grammar, and their invoice table.
    Clearing is deliberately absent -- bank-side fact, ruled out of
    the client band. Returns "" until the client has any money
    story (the page stays casework-pure). Carries its own style
    block: the contact page renders outside _page's billing CSS."""
    invs = [r for r in reads.invoice_rows(conn)
            if r["contact_id"] == contact_id]
    trust_subs = reads.trust_sub_accounts_of_contact(conn, contact_id)
    matter_ids = {m["id"] for m in
                  reads.contact_matters(conn, contact_id)}
    unb = [t for t in reads.unbilled_time_entries(conn)
           if t["contact_id"] == contact_id
           or t["matter_id"] in matter_ids]
    if not invs and not trust_subs and not unb:
        return ""

    today = _today()
    held = sum(ledger.account_balance(conn, a) for a in trust_subs)
    out_sum = collected = settling_cents = 0
    worst_overdue = 0
    trows = []
    for r in invs:
        bal = billing.invoice_balance(conn, r["id"])
        status = billing.invoice_status(conn, r["id"])
        status_cell = _status_pill(conn, r["id"])
        if status == "outstanding":
            out_sum += bal
            if r["due_date"] and r["due_date"] < today:
                age = _days_old(r["due_date"], today)
                worst_overdue = max(worst_overdue, age)
                status_cell += (f" <span class='chipnote'>overdue"
                                f" {age}d</span>")
            else:
                sent = reads.invoice_shares_of(conn, r["id"])
                if sent:
                    status_cell += (
                        " <span class='chipnote'>sent"
                        f" {fmt_date(sent[0]['created_at'][:10])}"
                        "</span>")
        for p in reads.invoice_payments_of(conn, r["id"]):
            if p["refunded"]:
                continue
            if (p["processor_txn_id"] is not None
                    and p["journal_entry_id"] is None):
                settling_cents += p["amount_cents"]
            else:
                collected += p["amount_cents"]
        trows.append([
            html.link(f"/billing/invoices/{r['id']}",
                      r["display_code"]),
            _type_pill(r),
            html.esc(fmt_date(r["issued_date"])),
            status_cell,
            f"<span class='money'>{fmt_cents(bal)}</span>"])
    itable = (html.table(["Invoice", "Type", "Issued", "Status",
                          "Balance"], trows) if trows
              else "<p class='hint'>No invoices yet.</p>")

    pay_list = f"/billing/clients/{contact_id}/payments"
    heads = (f"Held in trust: "
             + html.link("/billing/recon", dollars(held))
             + f" &middot; Outstanding: {dollars(out_sum)}"
             + f" &middot; Collected to date: "
             + html.link(pay_list, dollars(collected)))

    unb_cents = sum(
        (t["duration_seconds"] * t["rate_cents_per_hour"] + 1800)
        // 3600 for t in unb if t["rate_cents_per_hour"])
    flight = []
    if unb:
        label = (fmt_cents(unb_cents) if unb_cents
                 else fmt_duration(sum(t["duration_seconds"]
                                       for t in unb)))
        flight.append(html.link("/billing/time",
                                f"{label} unbilled"))
    if out_sum:
        note = (f" -- overdue {worst_overdue}d" if worst_overdue
                else "")
        flight.append(f"{fmt_cents(out_sum)} outstanding{note}")
    if settling_cents:
        flight.append(html.link(
            pay_list, f"{fmt_cents(settling_cents)} settling"))
    inflight = (f"<p class='inflight'>On the way: "
                + " &middot; ".join(flight) + "</p>") if flight else ""

    return (f"<style>{BILLING_STYLE}</style>"
            f"<div class='card'><h1>Money</h1>"
            f"<p class='split'>{heads}</p>{inflight}{itable}</div>")


def client_payments(h, conn, user, contact_id):
    """The footed drill behind the client band's Collected figure
    (s11, James's catch: a stated total must tie to a listing).
    Every payment for this client on one page; the foot equals the
    band's Collected-to-date exactly -- settling and refunded rows
    are chipped and excluded from the foot, each called out below
    it when present. Reader-only; also the landing for the band's
    settling segment."""
    contact = reads.contact_row(conn, contact_id)
    if contact is None:
        raise _nf()
    invs = [r for r in reads.invoice_rows(conn)
            if r["contact_id"] == contact_id]
    dated, collected, settling, refunded = [], 0, 0, 0
    for r in invs:
        for p in reads.invoice_payments_of(conn, r["id"]):
            method = {"sim_card": "card (online)",
                      "sim_echeck": "eCheck (online)",
                      "trust_transfer": "trust transfer (earn-out)",
                      "direct": "direct"}.get(p["method"], p["method"])
            chip = ""
            if p["refunded"]:
                chip = _pill("refunded")
                refunded += p["amount_cents"]
            elif (p["processor_txn_id"] is not None
                    and p["journal_entry_id"] is None):
                chip = _pill("settling", "Settling")
                settling += p["amount_cents"]
            else:
                collected += p["amount_cents"]
            dated.append((p["payment_date"], p["id"], [
                html.link(f"/billing/payments/{p['id']}",
                          fmt_date(p["payment_date"])),
                html.link(f"/billing/invoices/{r['id']}",
                          r["display_code"]),
                html.esc(method), chip,
                f"<span class='money'>{fmt_cents(p['amount_cents'])}"
                f"</span>"]))
    dated.sort(key=lambda t: (t[0], t[1]))
    if dated:
        table = html.table(["Date", "Invoice", "Method", "",
                            "Amount"], [row for _, _, row in dated])
    else:
        table = html.empty_state(
            "No payments from this client yet. Every payment on any"
            " of their invoices will appear here.")
    foot = (f"<p class='due'><strong>Collected to date:"
            f" {dollars(collected)}</strong></p>")
    notes = ""
    if settling:
        notes += (f"<p class='hint'>{dollars(settling)} more is"
                  " settling -- paid by the client, not yet at the"
                  " bank; it joins the total at settlement.</p>")
    if refunded:
        notes += (f"<p class='hint'>{dollars(refunded)} refunded --"
                  " listed above, not in the total.</p>")
    name = contact["display_name"]
    body = (_crumbs(("Billing", "/billing"),
                    (name, f"/contacts/{contact_id}"),
                    ("Payments", None))
            + f"<div class='card'><h1>Payments -- {html.esc(name)}"
            + f"</h1>{table}{foot}{notes}</div>")
    _page(h, f"Payments -- {name}", body, user)


def invoice_detail(h, conn, user, invoice_id, error=None):
    try:
        inv = billing.get_invoice(conn, invoice_id)
    except billing.BillingError:
        raise _nf()
    contact = reads.contact_row(conn, inv["contact_id"])
    charges = billing.invoice_charges(conn, invoice_id)
    payments = reads.invoice_payments_of(conn, invoice_id)
    balance = billing.invoice_balance(conn, invoice_id)
    status = billing.invoice_status(conn, invoice_id)
    noun = _noun(inv)
    title = f"{noun} {inv['display_code']}"
    is_trust = inv["invoice_type"] == "trust_request"

    kv = [("Client", html.link(f"/contacts/{contact['id']}",
                               contact["display_name"]))]
    if inv["matter_id"]:
        matter = reads.matter_row(conn, inv["matter_id"])
        kv.append(("Matter", html.link(f"/matters/{matter['id']}",
                                       matter["name"])))
    # the corpus-pinned stored number stays visible as an attribute;
    # identity is the display code (invoice-codes.md, built 2026-08-07)
    kv.append(("Number", html.esc(
        f"#{inv['number']} ({inv['number_scope']})")))
    kv.append(("Issued", html.esc(fmt_date(inv["issued_date"]))))
    if inv["due_date"]:
        kv.append(("Due", html.esc(fmt_date(inv["due_date"]))))
    if inv["invoice_type"] == "trust_request":
        kv.append(("Deposits to", html.esc(
            reads.ledger_account_row(
                conn, inv["trust_account_id"])["name"])))
    # the client's remaining trust, right where money decisions are
    # made (gated item H: fiduciary storytelling; only shown once
    # the client actually has a trust sub-ledger)
    trust_subs = reads.trust_sub_accounts_of_contact(
        conn, inv["contact_id"])
    if trust_subs:
        held = sum(ledger.account_balance(conn, a)
                   for a in trust_subs)
        kv.append(("Remaining in Trust",
                   f"<span class='money'>{fmt_cents(held)}</span>"))
    kvs = "<dl class='kv'>" + "".join(
        f"<dt>{html.esc(k)}</dt><dd>{v}</dd>" for k, v in kv) + "</dl>"

    if charges:
        crows = [[html.esc(c["description"]),
                  html.esc(c["charge_type"]),
                  html.esc(fmt_date(c["charge_date"])),
                  f"<span class='money'>{fmt_cents(c['amount_cents'])}"
                  f"</span>"] for c in charges]
        ctable = html.table(["Description", "Type", "Date", "Amount"],
                            crows)
    else:
        ctable = ""  # state A renders the add form, not filler

    def _is_settling(p):
        # the processor holds it: authorized, not yet posted to the
        # books (journal_entry_id lands at settlement)
        return (p["processor_txn_id"] is not None
                and p["journal_entry_id"] is None
                and not p["refunded"])

    if payments:
        prows = []
        for p in payments:
            method = {"sim_card": "card", "sim_echeck": "eCheck",
                      "trust_transfer": "trust transfer (earn-out)",
                      "direct": "direct"}.get(p["method"], p["method"])
            note = (" (online, simulated processor)"
                    if p["method"] in ("sim_card", "sim_echeck") else "")
            pills = ((_pill("refunded") if p["refunded"] else "")
                     + (_pill("settling", "Settling")
                        if _is_settling(p) else ""))
            prows.append([html.link(f"/billing/payments/{p['id']}",
                                    fmt_date(p["payment_date"])),
                          html.esc(method + note),
                          pills,
                          f"<span class='money'>"
                          f"{fmt_cents(p['amount_cents'])}</span>"])
        ptable = html.table(["Date", "Method", "", "Amount"], prows)
    else:
        ptable = ""  # the Payments card only exists once one does

    charge_form = (
        f"<form method='post'"
        f" action='/billing/invoices/{invoice_id}/charges'>"
        f"<h2 class='formhead'>Add a charge</h2>"
        f"<p class='hint'>Charges build the {noun.lower()}. Collect"
        f" controls appear once there is a balance due.</p>"
        + html.field("Description", "description")
        + html.field("Amount", "amount",
                     hint="Dollars and cents, e.g. 500.00")
        + _select("Type", "charge_type",
                  [("service", "Service"), ("expense", "Expense")])
        + html.field("Date", "charge_date", ftype="date",
                     value=inv["issued_date"] or _today(),
                     required=False)
        + "<button class='primary'>Add charge</button></form>")

    import_inner = ""
    if inv["invoice_type"] == "bill":
        saved = billing.list_saved_charges(conn)
        open_time = reads.unbilled_time_entries(conn)
        boxes = []
        for s in saved:
            boxes.append(
                f"<label class='pick'><input type='checkbox'"
                f" name='saved_charge' value='{s['id']}'"
                f" style='width:auto'> {html.esc(s['description'])}"
                f" -- {fmt_cents(s['amount_cents'])}"
                f" ({html.esc(s['charge_type'])})</label>")
        for t in open_time:
            rate = t["rate_cents_per_hour"]
            amount = ((t["duration_seconds"] * rate + 1800) // 3600
                      if rate else None)
            tail = (fmt_cents(amount) if amount is not None
                    else "at the user's default rate")
            boxes.append(
                f"<label class='pick'><input type='checkbox'"
                f" name='time_entry' value='{t['id']}'"
                f" style='width:auto'>"
                f" {html.esc(fmt_date(t['entry_date']))}"
                f" {html.esc(t['description'] or 'time entry')}"
                f" ({fmt_duration(t['duration_seconds'])}) -- {tail}"
                f"</label>")
        if boxes:
            import_inner = (
                f"<form method='post'"
                f" action='/billing/invoices/{invoice_id}/import'>"
                + "".join(boxes)
                + "<button class='primary'>Import selected</button>"
                  "</form>")

    shares = reads.invoice_shares_of(conn, invoice_id)
    # readonly input, not a <code> block (gated item G): click the
    # box, Ctrl+A selects the whole link cleanly -- the zero-JS
    # stand-in for a copy button
    share_rows = "".join(
        f"<input class='copylink' readonly"
        f" value='{h.server.client_base}"
        f"/invoice/{html.esc(s['token'])}'>"
        for s in shares)
    online = [p for p in payments
              if p["method"] in ("sim_card", "sim_echeck")]
    online_line = ""
    if online:
        settled = all(p["journal_entry_id"] for p in online)
        online_line = (
            "<p class='hint'>Online payment received via the"
            " simulated processor"
            + (" -- settled to the bank."
               if settled else " -- awaiting settlement.") + "</p>")
    share_block = (
        online_line
        + f"<p class='hint'>A private link lets the client view,"
          f" download, and pay this {noun.lower()} online.</p>"
        + share_rows
        + f"<form class='inline' method='post'"
          f" action='/billing/invoices/{invoice_id}/share'>"
          f"<button class='primary'>Create client link</button>"
          f"</form>"
          f"<form class='inline' method='post'"
          f" action='/billing/invoices/{invoice_id}/email'>"
          f"<button class='primary'>Email to client</button>"
          f"</form>"
          f"<p class='hint'>Email sends the link to the client's"
          f" address on file (synthetic outbox).</p>")

    banks = ledger.list_bank_accounts(conn)
    ops = [b for b in banks if b["kind"] == "operating_bank"]
    trusts = [b for b in banks if b["kind"] == "trust_bank"]
    collect_card = ""
    if balance > 0:
        if not banks:
            paths = ("<p class='hint'>Recording a payment needs the"
                     " firm's bank accounts.</p>"
                     "<div class='actions'>"
                     "<a href='/billing/accounts/new'>Create the"
                     " bank accounts first</a></div>")
        elif is_trust:
            dest = reads.ledger_account_row(conn,
                                            inv["trust_account_id"])
            deposit_form = (
                f"<form method='post'"
                f" action='/billing/invoices/{invoice_id}/pay'>"
                f"<input type='hidden' name='method' value='direct'>"
                f"<p class='hint'>Deposits to"
                f" {html.esc(dest['name'])} -- client funds, held in"
                f" trust until earned.</p>"
                + html.field("Amount", "amount",
                             value=fmt_cents(balance))
                + html.field("Date received", "payment_date",
                             ftype="date", value=_today())
                + "<button class='primary'>Record deposit</button>"
                  "</form>")
            # open always: before a link exists, sending is the
            # primary action; after "Create client link" the page
            # must SHOW the link (a result that hides itself inside
            # a collapsed fold failed the 2026-08-06 sheet drive)
            paths = (
                _fold("Send the request to the client", share_block,
                      open_=True)
                + _fold("Record the deposit (received directly by"
                        " the firm)", deposit_form))
        else:
            direct_form = (
                f"<form method='post'"
                f" action='/billing/invoices/{invoice_id}/pay'>"
                f"<input type='hidden' name='method' value='direct'>"
                + html.field("Amount", "amount",
                             value=fmt_cents(balance))
                + html.field("Date", "payment_date", ftype="date",
                             value=_today())
                + _select("Deposit to", "destination_account_id",
                          [(b["id"], b["name"]) for b in banks],
                          selected=(ops[0]["id"] if ops else None))
                + "<button class='primary'>Record payment</button>"
                  "</form>")
            trust_fold = ""
            if trusts:
                trust_fold = _fold(
                    "Pay from client trust (earn-out)",
                    f"<form method='post'"
                    f" action='/billing/invoices/{invoice_id}/pay'>"
                    f"<input type='hidden' name='method'"
                    f" value='trust_transfer'>"
                    f"<p class='hint'>Earned fees move trust ->"
                    f" operating; the client's sub-ledger releases"
                    f" the funds.</p>"
                    + html.field("Amount", "amount",
                                 value=fmt_cents(balance))
                    + html.field("Date", "payment_date",
                                 ftype="date", value=_today())
                    + _select("From trust account",
                              "source_account_id",
                              [(b["id"], b["name"])
                               for b in trusts])
                    + _select("Trust funds held for",
                              "source_trust_level",
                              [("client", "The client"),
                               ("matter", "The matter")])
                    + _select("Deposit to",
                              "destination_account_id",
                              [(b["id"], b["name"]) for b in banks],
                              selected=(ops[0]["id"] if ops
                                        else None))
                    + "<button class='primary'>Record payment"
                      "</button></form>")
            paths = (
                _fold("Record a direct payment (check, cash, wire)",
                      direct_form)
                + trust_fold
                + _fold("Send the client a payment link",
                        share_block, open_=bool(shares)))
        collect_card = (f"<div class='card'><h1>Collect"
                        f" {dollars(balance)}</h1>{paths}</div>")

    due_line = (f"<p class='due'><strong>Balance due:"
                f" {dollars(balance)}</strong></p>"
                if balance > 0 else "")

    # Dollars-in-buckets split (flow markers, s11 L2): where every
    # dollar of this invoice is right now. Rendered only when the
    # money straddles buckets -- a fully-collected or untouched
    # invoice already tells its story in one line.
    # same authority as the core: balance = charges - discount -
    # non-refunded payments, so collected derives to exactly the
    # posted payments and the three buckets foot to the invoice
    total_cents = (sum(c["amount_cents"] for c in charges)
                   - inv["discount_cents"])
    settling_cents = sum(p["amount_cents"] for p in payments
                         if _is_settling(p))
    collected_cents = total_cents - balance - settling_cents
    split_bits = []
    if collected_cents > 0:
        split_bits.append(f"{fmt_cents(collected_cents)} collected")
    if settling_cents:
        split_bits.append(f"{fmt_cents(settling_cents)} settling")
    if balance > 0:
        today = _today()
        note = ""
        if inv["due_date"] and inv["due_date"] < today:
            note = (" -- overdue"
                    f" {_days_old(inv['due_date'], today)} days")
        elif shares:
            note = f" -- sent {fmt_date(shares[0]['created_at'][:10])}"
        split_bits.append(f"{fmt_cents(balance)} outstanding{note}")
    split_line = ("<p class='split'>" + " &middot; ".join(split_bits)
                  + "</p>") if len(split_bits) > 1 else ""
    pdf_link = (f"<div class='actions'>"
                f"<a class='quiet' href='/billing/invoices/"
                f"{invoice_id}/pdf'>Download PDF</a></div>"
                if charges else "")
    # an invoice with no charges derives "paid" (zero balance) in
    # the core -- presenting that pill on an empty bill is a lie of
    # rendering, so no status pill until charges exist
    status_pill = (_pill(status, status.capitalize()) if charges
                   else "")
    header = (f"<div class='card'><h1>{html.esc(title)} "
              + ("".join((_type_pill(inv), " ", status_pill)))
              + f"</h1>{kvs}{due_line}{split_line}{pdf_link}</div>")

    # One page, three lives (walk finding F-1): building shows the
    # add form and nothing else; awaiting money leads with Collect;
    # paid keeps only the record.
    if not charges:
        # the import options wear the SAME fold label in every state
        # (2026-08-06 sheet drive: the bare-checkbox empty state left
        # the sheet's named fold nonexistent on screen)
        import_fold = (_fold("Import saved charges and time",
                             import_inner) if import_inner else "")
        charges_card = (f"<div class='card'><h1>Charges</h1>"
                        f"{charge_form}{import_fold}</div>")
        rest = ""
    else:
        folds = _fold("Add another charge", charge_form)
        if import_inner:
            folds += _fold("Import saved charges and time",
                           import_inner)
        charges_card = (f"<div class='card'><h1>Charges</h1>"
                        f"{ctable}{folds}</div>")
        payments_card = (f"<div class='card'><h1>Payments</h1>"
                         f"{ptable}</div>") if payments else ""
        if balance > 0:
            rest = collect_card + payments_card
        else:
            rest = payments_card + (
                f"<div class='card'><h1>Client link</h1>"
                f"{share_block}</div>")
    body = (_crumbs(("Billing", "/billing"), (title, None))
            + html.error_box(error) + header + charges_card + rest)
    _page(h, title, body, user)


def trust_overview(h, conn, user, error=None):
    banks = ledger.list_bank_accounts(conn)
    if banks:
        cards = []
        for b in banks:
            bal = ledger.account_balance(conn, b["id"])
            label = ("Trust (IOLTA)" if b["kind"] == "trust_bank"
                     else "Operating")
            cards.append(
                f"<div class='tile'><div class='label'>{label}</div>"
                f"<div class='value'>{dollars(bal)}</div>"
                f"<div class='go'>"
                + html.link(f"/billing/trust/{b['id']}",
                            f"{html.esc(b['name'])} ledger")
                + "</div></div>")
        tiles = "<div class='tiles'>" + "".join(cards) + "</div>"
    else:
        tiles = html.empty_state(
            "No bank accounts yet. Create the firm's trust and"
            " operating accounts to start the books.")

    sub_rows = []
    for b in banks:
        if b["kind"] != "trust_bank":
            continue
        for s in reads.sub_accounts_of(conn, b["id"]):
            owner = s["contact_name"] or s["matter_name"] or s["name"]
            level = "client" if s["contact_id"] else "matter"
            sub_rows.append([html.esc(owner), html.esc(level),
                             html.esc(b["name"]),
                             f"<span class='money'>"
                             f"{fmt_cents(ledger.account_balance(conn, s['id']))}"
                             f"</span>"])
    if sub_rows:
        subs = html.table(["Funds of", "Level", "Trust account",
                           "Balance"], sub_rows)
    else:
        subs = html.empty_state(
            "No client funds held yet. Paid trust requests create a"
            " sub-ledger per client or matter, automatically.")

    actions = ("<div class='actions'>"
               "<a href='/billing/accounts/new'>New bank account</a>"
               "<a class='quiet' href='/billing/trust/disburse'>"
               "Disburse funds</a>"
               + _back_to_billing() + "</div>")
    settle_card = ""
    if banks:
        settle_card = (
            "<div class='card'><h1>Processor settlement</h1>"
            "<p class='hint'>Online payments authorize instantly;"
            " money moves at settlement. One batch per bank: trust"
            " settles gross, processor fees come out of operating --"
            " never out of client funds.</p>"
            "<form method='post' action='/billing/settle'>"
            + html.field("Settlement date", "settle_date",
                         ftype="date", value=_today(),
                         required=False)
            + "<button class='primary'>Run settlement</button>"
              "</form></div>")
    body = (_crumbs(("Billing", "/billing"),
                    ("Trust accounting", None))
            + html.error_box(error)
            + f"<h1>Trust accounting</h1>{actions}{tiles}"
            + f"<div class='card'><h1>Client funds</h1>{subs}</div>"
            + settle_card)
    _page(h, "Trust accounting", body, user)


def account_ledger(h, conn, user, account_id):
    acct = reads.ledger_account_row(conn, account_id)
    if acct is None or acct["kind"] not in ("trust_bank",
                                            "operating_bank"):
        raise _nf()
    bal = ledger.account_balance(conn, account_id)
    subs = reads.sub_accounts_of(conn, account_id) \
        if acct["kind"] == "trust_bank" else []
    if subs:
        srows = [[html.esc(s["contact_name"] or s["matter_name"]
                           or s["name"]),
                  f"<span class='money'>"
                  f"{fmt_cents(ledger.account_balance(conn, s['id']))}"
                  f"</span>"] for s in subs]
        subs_html = ("<div class='card'><h1>Sub-ledgers</h1>"
                     + html.table(["Funds of", "Balance"], srows)
                     + "</div>")
    else:
        subs_html = ""

    # flow markers (s11 L3): rows the bank has not confirmed carry a
    # Clearing chip -- same reconcile engine, recon screen's default
    # period; at-rest rows stay unmarked
    period = reads.max_event_date(conn)
    clearing_ids = set()
    if period is not None:
        clearing_ids = {i["entry_id"] for i in reconcile.three_way(
            conn, account_id, period)["items"]}

    postings = reads.account_entries(conn, account_id)
    if postings:
        rows = []
        for p in postings:
            inflow = (p["side"] == "debit")  # banks are debit-normal
            signed = p["amount_cents"] if inflow else -p["amount_cents"]
            chip = (" " + _pill("clearing", "Clearing")
                    if p["entry_id"] in clearing_ids else "")
            rows.append([html.esc(fmt_date(p["posted_at"])),
                         html.link(f"/billing/journal/{p['entry_id']}",
                                   f"e{p['entry_id']}"),
                         html.esc(p["kind"].replace("_", " ")) + chip,
                         html.esc(p["memo"] or ""),
                         f"<span class='money'>{fmt_cents(signed)}"
                         f"</span>"])
        table = html.table(["Date", "Entry", "Kind", "Memo", "Amount"],
                           rows)
    else:
        table = html.empty_state(
            "No activity in this account yet. Every deposit, payment,"
            " and disbursement will appear here, permanently.")
    body = (_crumbs(("Billing", "/billing"),
                    ("Trust accounting", "/billing/trust"),
                    (acct["name"], None))
            + f"<div class='card'><h1>{html.esc(acct['name'])}</h1>"
            + f"<p><strong>Balance: {dollars(bal)}</strong></p></div>"
            + subs_html
            + f"<div class='card'><h1>Ledger</h1>{table}</div>")
    _page(h, acct["name"], body, user)


def journal_detail(h, conn, user, entry_id):
    e = reads.journal_entry_row(conn, entry_id)
    if e is None:
        raise _nf()
    postings = reads.journal_postings_of(conn, entry_id)
    rows = [[html.esc(p["name"]),
             html.esc(p["kind"].replace("_", " ")),
             f"<span class='money'>"
             f"{fmt_cents(p['amount_cents']) if p['side'] == 'debit' else ''}</span>",
             f"<span class='money'>"
             f"{fmt_cents(p['amount_cents']) if p['side'] == 'credit' else ''}</span>"]
            for p in postings]
    table = html.table(["Account", "Account kind", "Debit", "Credit"],
                       rows)

    trail = []
    if e["reverses_entry_id"]:
        trail.append("This entry REVERSES "
                     + html.link(
                         f"/billing/journal/{e['reverses_entry_id']}",
                         f"entry e{e['reverses_entry_id']}") + ".")
    if e["replaces_entry_id"]:
        trail.append("This entry REPLACES "
                     + html.link(
                         f"/billing/journal/{e['replaces_entry_id']}",
                         f"entry e{e['replaces_entry_id']}")
                     + " (the corrected recording).")
    for r in reads.entry_reversed_by(conn, entry_id):
        trail.append("Reversed by "
                     + html.link(f"/billing/journal/{r['id']}",
                                 f"entry e{r['id']}") + ".")
    for r in reads.entry_replaced_by(conn, entry_id):
        trail.append("Replaced by "
                     + html.link(f"/billing/journal/{r['id']}",
                                 f"entry e{r['id']}") + ".")
    trail_html = ""
    if trail:
        trail_html = ("<div class='trail'>" + "<br>".join(trail)
                      + "<div class='why'>Posted entries are never"
                      " edited or deleted; corrections are new"
                      " entries, so the history is always complete."
                      "</div></div>")

    links = []
    if e["invoice_id"]:
        links.append(("Invoice",
                      html.link(f"/billing/invoices/{e['invoice_id']}",
                                f"invoice {e['invoice_id']}")))
    events = reads.events_of_payment(conn, e["payment_id"]) \
        if e["payment_id"] else []
    ev_html = ""
    if events:
        erows = [[html.esc(fmt_date(ev["occurred_on"])),
                  html.esc(ev["event_type"].replace("_", " ")),
                  html.esc(ev["direction"]),
                  html.esc(ev["memo"] or ""),
                  f"<span class='money'>{fmt_cents(ev['amount_cents'])}"
                  f"</span>"] for ev in events]
        ev_html = ("<div class='card'><h1>Bank record</h1>"
                   + html.table(["Date", "Event", "Direction", "Memo",
                                 "Amount"], erows) + "</div>")

    kvs = "<dl class='kv'>" + "".join(
        f"<dt>{html.esc(k)}</dt><dd>{v}</dd>"
        for k, v in ([("Posted", html.esc(fmt_date(e["posted_at"]))),
                      ("Kind", html.esc(e["kind"].replace("_", " "))),
                      ("Memo", html.esc(e["memo"] or ""))] + links)) \
        + "</dl>"
    body = (_crumbs(("Billing", "/billing"),
                    ("Trust accounting", "/billing/trust"),
                    (f"Entry e{entry_id}", None))
            + f"<div class='card'><h1>Journal entry e{entry_id}</h1>"
            + kvs + trail_html + "</div>"
            + f"<div class='card'><h1>Postings (double-entry)</h1>"
            + table + "</div>" + ev_html)
    _page(h, f"Journal entry e{entry_id}", body, user)


def recon_screen(h, conn, user, query):
    banks = ledger.list_bank_accounts(conn)
    if not banks:
        body = (_crumbs(("Billing", "/billing"),
                        ("Reconciliation", None))
                + f"<div class='actions'>{_back_to_billing()}</div>"
                + "<div class='card'><h1>Three-way reconciliation</h1>"
                + html.empty_state(
                    "Nothing to reconcile yet. Once bank accounts"
                    " carry activity, every account is checked here:"
                    " bank statement = books = client claims.")
                + "</div>")
        return _page(h, "Reconciliation", body, user)

    default_period = reads.max_event_date(conn)
    period = (query.get("period", [None])[0] or default_period)
    sections = []
    if period is None:
        sections.append(html.empty_state(
            "Accounts exist but carry no bank activity yet."))
    else:
        for b in banks:
            r = reconcile.three_way(conn, b["id"], period)
            stmt = bank_statement.statement(conn, b["id"], period)
            books = reconcile._book_postings(conn, b["id"], period)
            badge = (_pill("holds", "HOLDS") if r["identity_holds"]
                     else _pill("broken", "BROKEN"))

            def _amt(cents):
                return f"<td class='amt'>{fmt_cents(cents)}</td>"

            def _foot(label, cents):
                return (f"<tr class='foot'><td></td><td>{label}</td>"
                        f"{_amt(cents)}</tr>")

            def _pane(title, rows):
                return (f"<div class='recon-col'><h2>{title}</h2>"
                        f"<table class='rec'>{''.join(rows)}</table>"
                        f"</div>")

            # Pane 1 -- the bank statement, then the classic vertical
            # bridge: statement balance + in transit - outstanding =
            # adjusted bank. Outflows parenthesized; the column FOOTS.
            rows = []
            for l in stmt["lines"]:
                sign = 1 if l["direction"] == "in" else -1
                what = l["event_type"].replace("_", " ")
                if l["memo"]:
                    what += f" -- {l['memo']}"
                rows.append(f"<tr><td>"
                            f"{html.esc(fmt_date(l['cleared_on']))}</td>"
                            f"<td>{html.esc(what)}</td>"
                            f"{_amt(sign * l['amount_cents'])}</tr>")
            if not stmt["lines"]:
                rows.append("<tr><td colspan='3' class='none'>no"
                            " cleared activity this period</td></tr>")
            rows.append(_foot("Statement balance",
                              stmt["closing_balance_cents"]))
            adjusted = r["bank_balance_cents"]
            for i in r["items"]:
                sign = 1 if i["direction"] == "in" else -1
                adjusted += sign * i["amount_cents"]
                word = {"deposit in transit": "in transit",
                        "outstanding disbursement":
                            "outstanding"}.get(i["cause"], i["cause"])
                rows.append(
                    f"<tr><td>{html.esc(fmt_date(i['date']))}</td>"
                    f"<td>{word} "
                    + html.link(f"/billing/journal/{i['entry_id']}",
                                f"e{i['entry_id']}")
                    + f"</td>{_amt(sign * i['amount_cents'])}</tr>")
            rows.append(_foot("Adjusted bank", adjusted))
            bank_pane = _pane("Bank statement (independent)", rows)

            # Pane 2 -- the books: every posted entry, signed, footing
            # to the ledger balance. System reversals labeled.
            rows = []
            for p in books:
                sign = 1 if p["direction"] == "in" else -1
                kind = p["kind"].replace("_", " ")
                if p["reverses"] or p["kind"] == "reversal":
                    kind += " (system correction)"
                rows.append(
                    f"<tr><td>{html.esc(fmt_date(p['date']))}</td>"
                    f"<td>"
                    + html.link(f"/billing/journal/{p['entry_id']}",
                                f"e{p['entry_id']}")
                    + f" {html.esc(kind)}</td>"
                    f"{_amt(sign * p['amount_cents'])}</tr>")
            rows.append(_foot("Books balance", r["book_balance_cents"]))
            books_pane = _pane("Books (ledger)", rows)

            # Pane 3 -- client claims, trust accounts only.
            claims_pane = ""
            if r["sub_ledger_sum_cents"] is not None:
                rows = []
                for s in reads.sub_accounts_of(conn, b["id"]):
                    owner = (s["contact_name"] or s["matter_name"]
                             or s["name"])
                    rows.append(
                        f"<tr><td></td><td>{html.esc(owner)}</td>"
                        f"{_amt(ledger.account_balance(conn, s['id']))}"
                        f"</tr>")
                rows.append(_foot("Client claims total",
                                  r["sub_ledger_sum_cents"]))
                claims_pane = _pane("Client claims", rows)

            tie = (f"<div class='identity'>adjusted bank"
                   f" {fmt_cents(adjusted)} = books"
                   f" {fmt_cents(r['book_balance_cents'])}"
                   + (f" = client claims"
                      f" {fmt_cents(r['sub_ledger_sum_cents'])}"
                      if r["sub_ledger_sum_cents"] is not None
                      else " (operating account: no client funds, no"
                           " claims leg)")
                   + "</div>")
            trouble = ""
            if (r["unmatched_statement_lines"]
                    or r["unmatched_book_postings"]):
                bits = [f"{len(r['unmatched_statement_lines'])}"
                        f" unmatched statement line(s),"
                        f" {len(r['unmatched_book_postings'])}"
                        f" unmatched posting(s) -- the identity does"
                        f" not account for these"]
                trouble = html.error_box("; ".join(bits))
            sections.append(
                f"<div class='card'><h1>{html.esc(b['name'])}"
                f" {badge}</h1>{trouble}"
                f"<div class='recon-cols'>{bank_pane}{books_pane}"
                f"{claims_pane}</div>{tie}</div>")

    body = (_crumbs(("Billing", "/billing"),
                    ("Reconciliation", None))
            + f"<h1>Three-way reconciliation</h1>"
            + f"<div class='actions'>{_back_to_billing()}</div>"
            + f"<p class='hint'>Period end"
            f" {html.esc(fmt_date(period) if period else '--')}"
            f" -- bank statement (independent, event-derived) against"
            f" the books against client claims. No plug figures:"
            f" every reconciling item carries its cause.</p>"
            + "".join(sections))
    _page(h, "Reconciliation", body, user)


# --- home screen (item-12 design gate, status-page.md RATIFIED
# 2026-08-08; James's gate decision: the firm status page IS the
# dashboard at "/"). Rendering only: verdicts come from the same
# reconcile engine the recon screen renders; money figures from
# ledger/billing module calls; SQL stays in reads.py. ---

# R5 thresholds: sane defaults now, firm settings later (flagged
# in status-page.md, not debated). Days before an uncleared check
# or an unbilled time entry becomes a NEEDS ATTENTION line.
STALE_CHECK_DAYS = 30
UNBILLED_NAG_DAYS = 30


def _days_old(iso, today_iso):
    a = datetime.strptime(iso, "%Y-%m-%d")
    b = datetime.strptime(today_iso, "%Y-%m-%d")
    return (b - a).days


def dashboard_screen(h, conn, user):
    today = _today()
    banks = ledger.list_bank_accounts(conn)
    period_date = reads.max_event_date(conn) if banks else None

    # Money row: balances by kind, recon verdict per bank at the
    # default period (the recon screen's own default).
    trust_total = op_total = 0
    trust_banks, op_banks = [], []
    verdicts = {}          # bank id -> holds (True/False)
    recon_items = []       # (bank, item) across banks
    for b in banks:
        bal = ledger.account_balance(conn, b["id"])
        if b["kind"] == "trust_bank":
            trust_total += bal
            trust_banks.append(b)
        else:
            op_total += bal
            op_banks.append(b)
        if period_date is not None:
            r = reconcile.three_way(conn, b["id"], period_date)
            verdicts[b["id"]] = (r["identity_holds"]
                                 and not r["unmatched_statement_lines"]
                                 and not r["unmatched_book_postings"])
            recon_items.extend((b, i) for i in r["items"])

    def _chip(bank_list):
        if not bank_list or period_date is None:
            return ""
        holds = all(verdicts[b["id"]] for b in bank_list)
        return (_pill("holds", "HOLDS") if holds
                else _pill("broken", "BROKEN"))

    def _ledger_href(bank_list):
        return (f"/billing/trust/{bank_list[0]['id']}"
                if len(bank_list) == 1 else "/billing/trust")

    def _tile(label, value, chip, go):
        return (f"<div class='tile'><div class='label'>{label}"
                f"</div><div class='value'>{value} {chip}</div>"
                f"<div class='go'>{go}</div></div>")

    # Client funds held: trust sub-accounts with money in them.
    holders = set()
    for tb in trust_banks:
        for s in reads.sub_accounts_of(conn, tb["id"]):
            if ledger.account_balance(conn, s["id"]) > 0:
                holders.add(s["id"])
    n = len(holders)
    tiles = "<div class='tiles'>" + _tile(
        "Trust (IOLTA)", dollars(trust_total), _chip(trust_banks),
        (f"<a href='{_ledger_href(trust_banks)}'>Ledger</a>"
         "<a href='/billing/recon'>Reconcile</a>") if trust_banks
        else html.link("/billing/accounts/new", "Add account")) + _tile(
        "Operating", dollars(op_total), _chip(op_banks),
        (f"<a href='{_ledger_href(op_banks)}'>Ledger</a>"
         "<a href='/billing/recon'>Reconcile</a>") if op_banks
        else html.link("/billing/accounts/new", "Add account")) + _tile(
        "Client funds held", dollars(trust_total),
        f"<span class='sub'>{n} client{'s' if n != 1 else ''}</span>",
        "<a href='/billing/recon'>By client</a>") + "</div>"

    # NEEDS ATTENTION (R5, strict): recon breaks, past-due bills,
    # stale checks, aged unbilled time. Empty most days by design.
    attend = []
    for b in banks:
        if period_date is not None and not verdicts[b["id"]]:
            attend.append(
                "Reconciliation BREAK on "
                + html.link("/billing/recon", b["name"]))
    inv_rows = reads.invoice_rows(conn)
    open_bills, open_sum = [], 0
    for r in inv_rows:
        if billing.invoice_status(conn, r["id"]) != "outstanding":
            continue
        open_bills.append(r)
        open_sum += billing.invoice_balance(conn, r["id"])
        if r["due_date"] and r["due_date"] < today:
            code = r["display_code"] or f"#{r['number']}"
            attend.append(
                html.link(f"/billing/invoices/{r['id']}", code)
                + f" past due (due {fmt_date(r['due_date'])})")
    for b, i in recon_items:
        if i["cause"] == "outstanding disbursement":
            age = _days_old(i["date"], today)
            if age > STALE_CHECK_DAYS:
                attend.append(
                    "Check outstanding "
                    f"{age} days ({fmt_cents(i['amount_cents'])}) -- "
                    + html.link(f"/billing/journal/{i['entry_id']}",
                                f"e{i['entry_id']}"))
    unbilled = reads.unbilled_time_entries(conn)
    unbilled_secs = sum(t["duration_seconds"] for t in unbilled)
    unbilled_cents = sum(
        (t["duration_seconds"] * t["rate_cents_per_hour"] + 1800)
        // 3600 for t in unbilled if t["rate_cents_per_hour"])
    for t in unbilled:
        if _days_old(t["entry_date"], today) > UNBILLED_NAG_DAYS:
            attend.append(
                html.link("/billing/time",
                          f"Unbilled time from"
                          f" {fmt_date(t['entry_date'])}")
                + f" ({fmt_duration(t['duration_seconds'])})")
    if attend:
        attention = "".join(f"<p class='attend'>{a}</p>"
                            for a in attend)
    elif banks:
        attention = ("<p class='allties'>Nothing needs you."
                     " Everything ties.</p>")
    else:
        attention = html.empty_state(
            "No bank accounts yet. Billing starts when the first"
            " account exists.")

    # ON THE WAY (flow markers, s11 placement ruling L1 -- amends
    # R5: dollars by bucket instead of counts; same quiet line under
    # the strict attention queue). Every figure is a sum over rows
    # reachable behind its link; buckets follow the ratified
    # vocabulary (unbilled / outstanding / settling / clearing).
    settling_rows = reads.settling_payments(conn)
    settling_cents = sum(p["amount_cents"] for p in settling_rows)
    clearing_cents = sum(i["amount_cents"] for _, i in recon_items)
    flight = []
    if unbilled:
        # rate-less entries have hours but no dollars yet -- show
        # the truthful figure, never a fabricated zero
        label = (fmt_cents(unbilled_cents) if unbilled_cents
                 else fmt_duration(unbilled_secs))
        flight.append(html.link("/billing/time",
                                f"{label} unbilled"))
    if open_bills:
        flight.append(html.link("/billing?tab=outstanding",
                                f"{fmt_cents(open_sum)} outstanding"))
    if settling_cents:
        # no list screen exists for processor money (judgment call,
        # flagged): a single settling payment links to its own page
        one = (settling_rows[0] if len(settling_rows) == 1 else None)
        text = f"{fmt_cents(settling_cents)} settling"
        flight.append(html.link(f"/billing/payments/{one['id']}",
                                text) if one else text)
    if clearing_cents:
        flight.append(html.link("/billing/recon",
                                f"{fmt_cents(clearing_cents)}"
                                " clearing"))
    inflight = (f"<p class='inflight'>On the way: "
                + " &middot; ".join(flight) + "</p>") if flight else ""

    # RECENT ACTIVITY (R6): money events only, with actors.
    acts = reads.recent_money_entries(conn)
    if acts:
        rows = []
        for e in acts:
            what = e["kind"].replace("_", " ")
            if e["display_code"]:
                what += " " + html.link(
                    f"/billing/invoices/{e['invoice_id']}",
                    e["display_code"])
            actor = {"user": e["actor_name"] or "user",
                     "contact": "client",
                     "system": "system"}.get(e["actor_type"] or "", "")
            rows.append([
                html.esc(fmt_date(e["posted_at"])), what,
                f"<span class='money'>"
                + html.link(f"/billing/journal/{e['id']}",
                            fmt_cents(e["amount_cents"] or 0))
                + "</span>",
                html.esc(actor)])
        activity = html.table(["Date", "What", "Amount", "By"], rows)
    else:
        activity = html.empty_state("No money movement yet.")

    # PRACTICE (R7): the old dashboard absorbed verbatim -- same
    # actions, same six count-links (frozen walk reachability).
    c = reads.counts(conn)
    tallies = ", ".join(
        html.link(href, f"{c[key]} {label}")
        for key, label, href in (("contacts", "clients", "/contacts"),
                                 ("matters", "matters", "/matters"),
                                 ("events", "events", "/calendar"),
                                 ("files", "files", "/files"),
                                 ("tasks", "tasks", "/tasks"),
                                 ("notes", "notes", "/notes")))
    practice = (
        "<div class='card'><h2 class='formhead'"
        " style='border-top:none;margin-top:0'>Practice</h2>"
        "<div class='actions'>"
        "<a href='/contacts/new'>New client</a>"
        "<a href='/matters/new'>New matter</a>"
        "<a class='quiet' href='/calendar'>Calendar</a></div>"
        f"<p class='hint'>{tallies}.</p></div>")

    if period_date is not None:
        month = datetime.strptime(period_date,
                                  "%Y-%m-%d").strftime("%B %Y")
        all_hold = all(verdicts.values())
        periodline = (f"<p class='periodline'>Period {month} -- "
                      + (f"ties as of {fmt_date(period_date)}" if all_hold
                         else "reconciliation needs attention")
                      + " -- <a href='/billing/close'>Period close</a>"
                      + "</p>")
    else:
        periodline = ("<p class='periodline'>No bank activity"
                      " yet. <a href='/billing/close'>Period close"
                      "</a></p>")

    body = ("<h1>Dashboard</h1>" + periodline + tiles
            + "<div class='card'><h2 class='formhead'"
            " style='border-top:none;margin-top:0'>Needs attention"
            f"</h2>{attention}{inflight}</div>"
            + "<div class='card'><h2 class='formhead'"
            " style='border-top:none;margin-top:0'>Recent activity"
            f"</h2>{activity}</div>" + practice)
    styled = f"<style>{BILLING_STYLE}</style>" + body
    h._send_page(200, html.page("Dashboard", styled,
                                user_name=user["name"],
                                active_href="/"))


def time_index(h, conn, user):
    rows = reads.time_entry_rows(conn)
    if rows:
        trows = []
        for t in rows:
            rate = t["rate_cents_per_hour"]
            if t["billed_cents"] is not None:
                amount = t["billed_cents"]  # what actually invoiced
            elif rate:
                amount = (t["duration_seconds"] * rate + 1800) // 3600
            else:
                amount = None
            trows.append([
                html.esc(fmt_date(t["entry_date"])),
                html.esc(t["description"] or ""),
                html.esc(t["matter_name"] or t["contact_name"] or ""),
                html.esc(fmt_duration(t["duration_seconds"])),
                f"<span class='money'>"
                f"{fmt_cents(rate) if rate else 'default'}</span>",
                f"<span class='money'>"
                f"{fmt_cents(amount) if amount is not None else '--'}"
                f"</span>",
                _pill("paid", "billed") if t["billed"]
                else _pill("bill", "open"),
            ])
        table = html.table(["Date", "Description", "Matter/Client",
                            "Time", "Rate/h", "Amount", ""], trows)
    else:
        table = html.empty_state(
            "No time recorded yet. Entries logged here can be pulled"
            " into an invoice in one step.")
    body = (_crumbs(("Billing", "/billing"), ("Time", None))
            + f"<div class='card'><h1>Time</h1>"
            f"<div class='actions'><a href='/billing/time/new'>"
            f"Record time</a>{_back_to_billing()}</div>{table}</div>")
    _page(h, "Time", body, user)


def payment_detail(h, conn, user, payment_id, error=None):
    """The corrections surface (tier 2): a payment's full story --
    row, journal trail, bank record -- with edit-as-correction and
    refund. 'Edit' never mutates a posted entry: the module reverses
    and reposts, and this screen shows all of it."""
    try:
        p = billing.get_payment(conn, payment_id)
    except billing.BillingError:
        raise _nf()
    inv = billing.get_invoice(conn, p["invoice_id"])
    charges = billing.invoice_charges(conn, p["invoice_id"])
    method = {"sim_card": "card (online, simulated processor)",
              "sim_echeck": "eCheck (online, simulated processor)",
              "trust_transfer": "trust transfer (earn-out)",
              "direct": "direct"}.get(p["method"], p["method"])
    assoc = next((c for c in charges
                  if c["id"] == p["associated_charge_id"]), None)

    settling = (p["processor_txn_id"] is not None
                and p["journal_entry_id"] is None
                and not p["refunded"])
    kv = [(_noun(inv), html.link(f"/billing/invoices/{inv['id']}",
                                 f"{_noun(inv)} {inv['display_code']}")),
          ("Method", html.esc(method)),
          ("Amount", f"<span class='money'>"
                     f"{fmt_cents(p['amount_cents'])}</span>"
                     + (" " + _pill("settling", "Settling")
                        if settling else "")),
          ("Date", html.esc(fmt_date(p["payment_date"]))),
          ("Applied to", html.esc(assoc["description"]) if assoc
           else "the invoice balance")]
    if p["note"]:
        kv.append(("Note", html.esc(p["note"])))
    if p["refunded"]:
        kv.append(("Refund note", html.esc(p["refund_note"] or "-")))
    kvs = "<dl class='kv'>" + "".join(
        f"<dt>{html.esc(k)}</dt><dd>{v}</dd>" for k, v in kv) + "</dl>"

    entries = reads.entries_of_payment(conn, payment_id)
    if entries:
        erows = []
        for e in entries:
            tags = []
            if e["reverses_entry_id"]:
                tags.append(f"reverses e{e['reverses_entry_id']}")
            if e["replaces_entry_id"]:
                tags.append(f"replaces e{e['replaces_entry_id']}")
            erows.append([
                html.link(f"/billing/journal/{e['id']}", f"e{e['id']}"),
                html.esc(fmt_date(e["posted_at"])),
                html.esc(e["kind"].replace("_", " ")),
                html.esc(", ".join(tags)),
                html.esc(e["memo"] or "")])
        etable = html.table(["Entry", "Posted", "Kind", "Correction",
                             "Memo"], erows)
    else:
        etable = html.empty_state(
            "No journal entries yet -- online payments post at"
            " settlement.")
    trail_card = (
        "<div class='card'><h1>Journal trail</h1>" + etable
        + "<div class='trail'><div class='why'>Posted entries are"
          " never edited or deleted. A correction is a reversal plus"
          " a repost -- every version stays on the books, so the"
          " history is always complete.</div></div></div>")

    events = reads.events_of_payment(conn, payment_id)
    ev_card = ""
    if events:
        evrows = [[html.esc(fmt_date(ev["occurred_on"])),
                   html.esc(ev["event_type"].replace("_", " ")),
                   html.esc(ev["direction"]),
                   html.esc(ev["memo"] or ""),
                   f"<span class='money'>"
                   f"{fmt_cents(ev['amount_cents'])}</span>"]
                  for ev in events]
        ev_card = ("<div class='card'><h1>Bank record</h1>"
                   + html.table(["Date", "Event", "Direction", "Memo",
                                 "Amount"], evrows)
                   + "<p class='hint'>The bank record keeps exactly"
                     " what the bank saw. Corrections live in the"
                     " books; the reconciliation explains any"
                     " difference.</p></div>")

    if p["refunded"]:
        action_cards = (
            "<div class='card'><h1>Corrections</h1>"
            + html.empty_state(
                "This payment is refunded and closed. The reversing"
                " entries above are the permanent record.")
            + "</div>")
    else:
        charge_opts = [(c["id"], f"{c['description']}"
                        f" ({fmt_cents(c['amount_cents'])})")
                       for c in charges]
        edit_form = (
            f"<form method='post'"
            f" action='/billing/payments/{payment_id}/edit'>"
            + html.field("Date", "payment_date", ftype="date",
                         value=p["payment_date"], required=False)
            + html.field("Amount", "amount",
                         value=fmt_cents(p["amount_cents"]),
                         required=False)
            + _select("Apply to charge", "associated_charge_id",
                      charge_opts, selected=p["associated_charge_id"],
                      blank="The whole invoice",
                      hint="Re-associating is a correction like any"
                           " other: recorded, never overwritten.")
            + html.field("Note", "note", required=False)
            + "<button class='primary'>Save correction</button>"
              "</form>")
        refund_form = (
            f"<form method='post'"
            f" action='/billing/payments/{payment_id}/refund'>"
            f"<h2 class='formhead'>Refund</h2>"
            f"<p class='hint'>Full amount only. The books reverse;"
            f" the bank records the money going back.</p>"
            + html.field("Refund note", "note", required=False)
            + "<button class='primary'>Refund in full</button>"
              "</form>")
        action_cards = (
            "<div class='card'><h1>Correct this payment</h1>"
            "<p class='hint'>Change the date, amount, or charge and"
            " save: the original entry is reversed and a corrected"
            " one posted. Nothing is erased.</p>"
            + edit_form + refund_form + "</div>")

    status_pill = _pill("refunded") if p["refunded"] else ""
    body = (_crumbs(("Billing", "/billing"),
                    (f"{_noun(inv)} {inv['display_code']}",
                     f"/billing/invoices/{inv['id']}"),
                    (f"Payment {payment_id}", None))
            + html.error_box(error)
            + f"<div class='card'><h1>Payment {payment_id}"
              f" {status_pill}</h1>" + kvs + "</div>"
            + trail_card + ev_card + action_cards)
    _page(h, f"Payment {payment_id}", body, user)


# --- P2 write surfaces (forms render here; every mutation routes
# through casework modules and commits before redirecting) ----------

def _contact_opts(conn):
    return [(c["id"], c["display_name"])
            for c in reads.list_contacts(conn)]


def _matter_opts(conn):
    return [(m["id"], f"{m['name']} -- {m['display_name']}")
            for m in reads.list_matters(conn)]


def accounts_new(h, conn, user, error=None):
    body = (_crumbs(("Billing", "/billing"),
                    ("Trust accounting", "/billing/trust"),
                    ("New bank account", None))
            + f"<div class='card narrow'><h1>New bank account</h1>"
            + html.error_box(error)
            + "<p class='hint'>Two accounts run the books: client"
              " money lives in trust (IOLTA), the firm's own money"
              " in operating. The ledger keeps them apart --"
              " permanently.</p>"
            + "<form method='post' action='/billing/accounts/new'>"
            + _select("Kind", "kind",
                      [("trust_bank", "Trust (IOLTA)"),
                       ("operating_bank", "Operating")])
            + html.field("Account name", "label", autofocus=True,
                         hint="As it appears on statements, e.g."
                              " 'First Synthetic IOLTA'.")
            + "<button class='primary'>Create account</button>"
              "</form></div>")
    _page(h, "New bank account", body, user)


def accounts_create(h, conn, uid, user):
    f = h._form_body()
    try:
        ledger.create_bank_account(conn, f.get("kind", ""),
                                   f.get("label", "").strip(), uid)
    except ValueError as e:
        conn.rollback()
        return accounts_new(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect("/billing/trust")


def invoice_new(h, conn, user, error=None):
    contact_opts = _contact_opts(conn)
    crumbs = _crumbs(("Billing", "/billing"), ("New invoice", None))
    if not contact_opts:
        body = (crumbs + "<div class='card narrow'>"
                "<h1>New invoice</h1>"
                "<p>An invoice bills a client, and there are no"
                " clients yet.</p>"
                "<div class='actions'><a href='/contacts/new'>"
                "Create the client first</a></div>"
                "<p class='hint'>You will land back here in one"
                " click.</p></div>")
        return _page(h, "New invoice", body, user)
    matter_opts = _matter_opts(conn)
    trusts = [b for b in ledger.list_bank_accounts(conn)
              if b["kind"] == "trust_bank"]
    bill_card = (
        f"<div class='card'><h1>New bill</h1>"
        f"<p class='hint'>Fees and expenses the client pays the"
        f" firm.</p>"
        f"<form method='post' action='/billing/invoices/new'>"
        f"<input type='hidden' name='invoice_type' value='bill'>"
        + _select("Client", "contact_id", contact_opts)
        + _select("Matter", "matter_id", matter_opts,
                  blank="No matter (bill the client directly)")
        + html.field("Issue date", "issued_date", ftype="date",
                     value=_today())
        + "<button class='primary'>Create bill</button></form>"
          "</div>")
    if trusts:
        trust_card = (
            f"<div class='card'><h1>New trust request</h1>"
            f"<p class='hint'>Asks the client to fund their trust"
            f" account -- a retainer. The money stays theirs until"
            f" it is earned out.</p>"
            f"<form method='post' action='/billing/invoices/new'>"
            f"<input type='hidden' name='invoice_type'"
            f" value='trust_request'>"
            + _select("Client", "contact_id", contact_opts)
            + _select("Deposits to", "trust_account_id",
                      [(b["id"], b["name"]) for b in trusts])
            + _select("Hold funds for", "trust_level",
                      [("client", "The client"),
                       ("matter", "A specific matter")])
            + _select("Matter", "matter_id", matter_opts,
                      blank="Client-level funds (no specific matter)",
                      hint="Only needed when holding funds for a"
                           " specific matter.")
            + html.field("Issue date", "issued_date", ftype="date",
                         value=_today())
            + "<button class='primary'>Create trust request"
              "</button></form></div>")
    else:
        trust_card = (
            "<div class='card'><h1>New trust request</h1>"
            + html.empty_state(
                "A trust request needs a trust bank account to"
                " deposit into.")
            + "<div class='actions'>"
              "<a href='/billing/accounts/new'>Create the trust"
              " account</a></div></div>")
    body = crumbs + html.error_box(error) + bill_card + trust_card
    _page(h, "New invoice", body, user)


def invoice_create(h, conn, uid, user):
    f = h._form_body()
    try:
        invoice_id = billing.create_invoice(
            conn, f.get("invoice_type", ""),
            int(f["contact_id"]), uid,
            f.get("issued_date") or _today(),
            matter_id=int(f["matter_id"]) if f.get("matter_id")
            else None,
            trust_level=f.get("trust_level") or None,
            trust_account_id=int(f["trust_account_id"])
            if f.get("trust_account_id") else None)
    except (ValueError, KeyError) as e:
        conn.rollback()
        return invoice_new(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect(f"/billing/invoices/{invoice_id}")


def charge_create(h, conn, uid, user, invoice_id):
    f = h._form_body()
    try:
        billing.add_charge(
            conn, invoice_id, f.get("charge_type", ""),
            f.get("description", "").strip(),
            cents_of(f.get("amount")), uid,
            charge_date=f.get("charge_date") or None)
    except ValueError as e:
        conn.rollback()
        return invoice_detail(h, conn, user, invoice_id,
                              error=str(e))
    conn.commit()
    return h._redirect(f"/billing/invoices/{invoice_id}")


def invoice_import(h, conn, uid, user, invoice_id):
    f = h._form_body_multi()
    saved = [int(x) for x in f.get("saved_charge", [])]
    entries = [int(x) for x in f.get("time_entry", [])]
    try:
        if not saved and not entries:
            raise billing.BillingError(
                "pick at least one saved charge or time entry to"
                " import")
        if saved:
            new_ids = billing.import_saved_charges(conn, invoice_id,
                                                   saved, uid)
            # imported saved charges carry the bill's issue date --
            # the same default the manual Add form prefills (gated
            # item C: the blank Date cell read as missing data).
            # Existing core APIs only: import returns the charge
            # ids; update_charge dates them.
            inv = billing.get_invoice(conn, invoice_id)
            for cid in new_ids:
                billing.update_charge(
                    conn, cid,
                    charge_date=inv["issued_date"] or _today())
        if entries:
            billing.import_time_entries(conn, invoice_id, entries,
                                        uid)
    except ValueError as e:
        conn.rollback()
        return invoice_detail(h, conn, user, invoice_id,
                              error=str(e))
    conn.commit()
    return h._redirect(f"/billing/invoices/{invoice_id}")


def invoice_pay(h, conn, uid, user, invoice_id):
    f = h._form_body()
    method = f.get("method", "")
    kwargs = {}
    try:
        if f.get("destination_account_id"):
            kwargs["destination_account_id"] = \
                int(f["destination_account_id"])
        if method == "trust_transfer":
            if f.get("source_account_id"):
                kwargs["source_account_id"] = \
                    int(f["source_account_id"])
            kwargs["source_trust_level"] = \
                f.get("source_trust_level") or None
        billing.record_payment(
            conn, invoice_id, method, cents_of(f.get("amount")),
            f.get("payment_date") or _today(), uid, **kwargs)
    except ValueError as e:
        conn.rollback()
        return invoice_detail(h, conn, user, invoice_id,
                              error=str(e))
    conn.commit()
    return h._redirect(f"/billing/invoices/{invoice_id}")


def payment_edit(h, conn, uid, user, payment_id):
    f = h._form_body()
    try:
        kwargs = {}
        if f.get("payment_date"):
            kwargs["payment_date"] = f["payment_date"]
        if f.get("amount", "").strip():
            kwargs["amount_cents"] = cents_of(f["amount"])
        if f.get("associated_charge_id"):
            kwargs["associated_charge_id"] = \
                int(f["associated_charge_id"])
        if f.get("note", "").strip():
            kwargs["note"] = f["note"].strip()
        if not kwargs:
            raise billing.BillingError("change at least one field to"
                                       " record a correction")
        billing.edit_payment(conn, payment_id, uid, _today(), **kwargs)
    except ValueError as e:
        conn.rollback()
        return payment_detail(h, conn, user, payment_id, error=str(e))
    conn.commit()
    return h._redirect(f"/billing/payments/{payment_id}")


def payment_refund(h, conn, uid, user, payment_id):
    f = h._form_body()
    try:
        billing.refund_payment(conn, payment_id, uid, _today(),
                               note=f.get("note", "").strip() or None)
    except ValueError as e:
        conn.rollback()
        return payment_detail(h, conn, user, payment_id, error=str(e))
    conn.commit()
    return h._redirect(f"/billing/payments/{payment_id}")


def invoice_email_share(h, conn, uid, user, invoice_id):
    try:
        billing.send_invoice_share(conn, invoice_id, uid)
    except ValueError as e:
        conn.rollback()
        return invoice_detail(h, conn, user, invoice_id, error=str(e))
    conn.commit()
    return h._redirect(f"/billing/invoices/{invoice_id}")


def invoice_pdf_download(h, conn, invoice_id):
    import tempfile
    try:
        inv = billing.get_invoice(conn, invoice_id)
    except billing.BillingError:
        raise _nf()
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "invoice.pdf"
        billing.invoice_pdf(conn, invoice_id, str(out))
        content = out.read_bytes()
    h._send_file(content, f"invoice-{inv['display_code']}.pdf")


def invoice_share(h, conn, uid, user, invoice_id):
    try:
        billing.share_invoice(conn, invoice_id, uid)
    except ValueError as e:
        conn.rollback()
        return invoice_detail(h, conn, user, invoice_id,
                              error=str(e))
    conn.commit()
    return h._redirect(f"/billing/invoices/{invoice_id}")


def settle_post(h, conn, uid, user):
    f = h._form_body()
    try:
        processor.settle(conn, f.get("settle_date") or _today(),
                         posted_by=uid)
    except ValueError as e:
        conn.rollback()
        return trust_overview(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect("/billing/trust")


def time_new(h, conn, user, error=None):
    body = (_crumbs(("Billing", "/billing"),
                    ("Time", "/billing/time"),
                    ("Record time", None))
            + f"<div class='card narrow'><h1>Record time</h1>"
            + html.error_box(error)
            + "<form method='post' action='/billing/time/new'>"
            + html.field("Date worked", "work_date", ftype="date",
                         value=_today())
            + html.field("Time spent", "duration", autofocus=True,
                         hint="Hours or minutes: 2, 2h, 1.5h, 45m."
                              " A bare number means hours.")
            + html.field("Hourly rate", "rate", required=False,
                         hint="Dollars per hour, e.g. 250.00."
                              " Leave blank to bill at your default"
                              " rate.")
            + html.field("Description", "description",
                         required=False)
            + _select("Client", "contact_id", _contact_opts(conn),
                      blank="No client (use the matter below)")
            + _select("Matter", "matter_id", _matter_opts(conn),
                      blank="No matter")
            + "<button class='primary'>Record time</button>"
              "</form></div>")
    _page(h, "Record time", body, user)


def time_create(h, conn, uid, user):
    f = h._form_body()
    duration = f.get("duration", "").strip()
    # bare number = hours (gated item D: "2" bounced while "2h"
    # worked; the billing default unit is the hour). Same boundary
    # cents_of holds for amounts: normalize here, and anything else
    # passes through verbatim so the core's own error stays the
    # teacher (fx-0064 formats are corpus-pinned).
    if duration.replace(".", "", 1).isdigit():
        duration += "h"
    try:
        rate = (cents_of(f["rate"]) if f.get("rate", "").strip()
                else None)
        timekeeping.create_entry(
            conn, uid, f.get("work_date") or _today(),
            duration=duration,
            description=f.get("description", "").strip() or None,
            contact_id=int(f["contact_id"]) if f.get("contact_id")
            else None,
            matter_id=int(f["matter_id"]) if f.get("matter_id")
            else None,
            rate_cents_per_hour=rate)
    except ValueError as e:
        conn.rollback()
        return time_new(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect("/billing/time")


def saved_charges(h, conn, user, error=None):
    rows = billing.list_saved_charges(conn)
    if rows:
        table = html.table(
            ["Description", "Type", "Amount"],
            [[html.esc(s["description"]),
              html.esc(s["charge_type"]),
              f"<span class='money'>{fmt_cents(s['amount_cents'])}"
              f"</span>"] for s in rows])
    else:
        table = html.empty_state(
            "No saved charges yet. Save the fees you bill again and"
            " again -- filing fees, flat fees -- and add them to any"
            " invoice in one step.")
    body = (_crumbs(("Billing", "/billing"),
                    ("Saved charges", None))
            + f"<div class='card'><h1>Saved charges</h1>"
            + f"<div class='actions'>{_back_to_billing()}</div>"
            + html.error_box(error) + table
            + "<form method='post' action='/billing/charges/saved'>"
            + "<h2 class='formhead'>Save a charge</h2>"
            + html.field("Description", "description")
            + html.field("Amount", "amount",
                         hint="Dollars and cents, e.g. 2,500.00")
            + _select("Type", "charge_type",
                      [("service", "Service"),
                       ("expense", "Expense")])
            + "<button class='primary'>Save charge</button>"
              "</form></div>")
    _page(h, "Saved charges", body, user)


def saved_charge_create(h, conn, uid, user):
    f = h._form_body()
    try:
        billing.create_saved_charge(
            conn, f.get("description", "").strip(),
            cents_of(f.get("amount")), f.get("charge_type", ""), uid)
    except ValueError as e:
        conn.rollback()
        return saved_charges(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect("/billing/charges/saved")


def disburse_form(h, conn, user, error=None):
    trusts = [b for b in ledger.list_bank_accounts(conn)
              if b["kind"] == "trust_bank"]
    crumbs = _crumbs(("Billing", "/billing"),
                     ("Trust accounting", "/billing/trust"),
                     ("Disburse funds", None))
    if not trusts:
        body = (crumbs + "<div class='card narrow'>"
                "<h1>Disburse funds</h1>"
                + html.empty_state(
                    "Disbursements pay third parties out of a"
                    " client's trust funds -- and there is no trust"
                    " account yet.")
                + "<div class='actions'>"
                  "<a href='/billing/accounts/new'>Create the trust"
                  " account</a></div></div>")
        return _page(h, "Disburse funds", body, user)
    body = (crumbs
            + f"<div class='card narrow'><h1>Disburse funds</h1>"
            + html.error_box(error)
            + "<p class='hint'>Pays a third party -- USCIS, a"
              " provider -- out of funds held in trust. The client's"
              " sub-ledger and the trust account move together.</p>"
            + "<form method='post' action='/billing/trust/disburse'>"
            + _select("From trust account", "account_id",
                      [(b["id"], b["name"]) for b in trusts])
            + _select("Funds held for client", "contact_id",
                      _contact_opts(conn),
                      blank="No client (pick a matter below)")
            + _select("Funds held for matter", "matter_id",
                      _matter_opts(conn),
                      blank="No matter (funds are client-level)")
            + html.field("Amount", "amount",
                         hint="Dollars and cents, e.g. 1,200.00")
            + html.field("Date", "disburse_date", ftype="date",
                         value=_today())
            # known-payee datalist + free entry (gated item F):
            # native, zero-JS -- prior counterparties suggest,
            # anything typed still goes through
            + "<label>Pay to</label>"
            + "<p class='hint'>Who receives the money, e.g."
              " SYNTH-USCIS. Known payees appear as you type; a new"
              " name is fine.</p>"
            + "<input name='counterparty' list='known-payees'"
              " required>"
            + ("<datalist id='known-payees'>"
               + "".join(f"<option value='{html.esc(p)}'>"
                         for p in reads.known_counterparties(conn))
               + "</datalist>")
            + html.field("Memo", "memo", required=False)
            + "<button class='primary'>Disburse</button>"
              "</form></div>")
    _page(h, "Disburse funds", body, user)


def disburse_post(h, conn, uid, user):
    f = h._form_body()
    try:
        ledger.disburse(
            conn, int(f["account_id"]), cents_of(f.get("amount")),
            f.get("disburse_date") or _today(), uid,
            contact_id=int(f["contact_id"]) if f.get("contact_id")
            else None,
            matter_id=int(f["matter_id"]) if f.get("matter_id")
            else None,
            counterparty=f.get("counterparty", "").strip() or None,
            memo=f.get("memo", "").strip() or None)
    except (ValueError, KeyError) as e:
        conn.rollback()
        return disburse_form(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect("/billing/trust")


# --- period close (period-close.md, RATIFIED 2026-08-09) --------------
# The monthly meeting as a feature. Rendering only: every figure and
# every gate comes from app.period (which itself renders the recon
# oracle's numbers); the two writes route through period.prepare and
# period.approve.


def _month_name(period_str):
    return datetime.strptime(period_str + "-01",
                             "%Y-%m-%d").strftime("%B %Y")


def _close_ties(accounts):
    rows = []
    for a in accounts:
        badge = (_pill("holds", "HOLDS") if a["identity_holds"]
                 else _pill("broken", "BROKEN"))
        cells = [html.esc(a["name"]),
                 fmt_cents(a["bank_balance_cents"]),
                 fmt_cents(a["deposits_in_transit_cents"]),
                 fmt_cents(a["outstanding_disbursements_cents"]),
                 fmt_cents(a["corrections_net_cents"]),
                 fmt_cents(a["book_balance_cents"]),
                 ("--" if a["sub_ledger_sum_cents"] is None
                  else fmt_cents(a["sub_ledger_sum_cents"]))]
        rows.append("<tr><td>" + cells[0] + "</td>"
                    + "".join(f"<td><span class='money'>{c}</span></td>"
                              for c in cells[1:])
                    + f"<td>{badge}</td></tr>")
    return ("<table class='list'><tr><th>Account</th><th>Bank</th>"
            "<th>In transit</th><th>Outstanding</th><th>Corrections"
            "</th><th>Book</th><th>Client claims</th><th>Tie</th></tr>"
            + "".join(rows) + "</table>")


def _close_item_line(item):
    return ("%s -- %s %s, %s, "
            % (html.esc(item["cause"]),
               fmt_cents(item["amount_cents"]),
               "in" if item["direction"] == "in" else "out",
               fmt_date(item["date"]))
            + html.link(f"/billing/journal/{item['entry_id']}",
                        f"e{item['entry_id']}"))


def _close_items(snapshot, ack_boxes):
    lines = []
    for a in snapshot["accounts"]:
        for i in a["items"]:
            if ack_boxes:
                key = period.item_key(a["bank_account_id"], i)
                lines.append(
                    "<label class='ackrow'><input type='checkbox'"
                    f" name='ack' value='{html.esc(key)}' required> "
                    + _close_item_line(i) + "</label>")
            else:
                lines.append("<p class='ackrow'>[x] "
                             + _close_item_line(i) + "</p>")
    if not lines:
        return html.empty_state("Nothing carried. The month is clean.")
    return "".join(lines)


def _close_story(story):
    return ("<p class='split'>Billed %s | Collected %s | Into trust %s"
            " | Out of trust %s | Earned from trust %s</p>"
            % (dollars(story["billed_cents"]),
               dollars(story["collected_cents"]),
               dollars(story["into_trust_cents"]),
               dollars(story["out_of_trust_cents"]),
               dollars(story["earned_from_trust_cents"])))


def _close_rankings(snapshot):
    wb = "".join(
        "<tr><td>%s</td><td><span class='money'>%s</span></td>"
        "<td>oldest %s (%d days)</td></tr>"
        % (html.esc(r["name"]), fmt_cents(r["outstanding_cents"]),
           fmt_date(r["oldest_issued"]), r["age_days"])
        for r in snapshot["way_behind"])
    kc = "".join(
        "<tr><td>%s</td><td><span class='money'>%s</span></td>"
        "<td>%d.%02d%% of collections</td></tr>"
        % (html.esc(r["name"]), fmt_cents(r["collected_cents"]),
           r["share_bp"] // 100, r["share_bp"] % 100)
        for r in snapshot["keeps_in_cash"])
    return (
        "<h2 class='formhead'>Who is way behind</h2>"
        + (f"<table class='list'>{wb}</table>" if wb
           else html.empty_state("No one is behind."))
        + "<h2 class='formhead'>Who keeps us in cash</h2>"
        + (f"<table class='list'>{kc}</table>" if kc
           else html.empty_state("Nothing collected in the trailing"
                                 " three months.")))


def _closed_months_card(conn):
    rows = []
    for r in period.list_closed(conn):
        pby = reads.get_user(conn, r["prepared_by"])
        aby = reads.get_user(conn, r["approved_by"])
        rows.append(
            "<tr><td>%s</td><td>closed %s</td><td>prepared %s,"
            " approved %s</td><td>%s</td></tr>"
            % (html.esc(_month_name(r["period"])),
               fmt_date(r["approved_at"]),
               html.esc(pby["name"]), html.esc(aby["name"]),
               html.link(f"/billing/close/{r['period']}", "record")))
    inner = (f"<table class='list'>{''.join(rows)}</table>" if rows
             else html.empty_state("No months closed yet."))
    return ("<div class='card'><h2 class='formhead'"
            " style='border-top:none;margin-top:0'>Closed months</h2>"
            + inner + "</div>")


def close_screen(h, conn, user, error=None):
    crumbs = _crumbs(("Billing", "/billing"), ("Period close", None))
    closable = period.closable_month(conn, _today())
    if closable is None:
        body = (crumbs + "<h1>Period close</h1>"
                + html.error_box(error)
                + html.empty_state(
                    "Nothing is closable right now. A month closes"
                    " only after it ends, oldest first, once money"
                    " facts exist in the books.")
                + _closed_months_card(conn))
        return _page(h, "Period close", body, user)
    p, pe = closable
    title = f"Close {_month_name(p)}"
    prow = period.get_row(conn, p, statuses=("prepared",))
    if prow is not None:
        snap = json.loads(prow["snapshot"])
        preparer = reads.get_user(conn, prow["prepared_by"])
        step = ("<p class='hint'>Step 2 of 2 -- approve. Prepared by"
                f" {html.esc(preparer['name'])} on"
                f" {fmt_date(prow['prepared_at'])}. Approving locks"
                f" {html.esc(_month_name(p))} permanently; if the"
                " numbers moved since prepare, approval refuses and"
                " voids the prepare instead.</p>")
        act = ("<form method='post' action='/billing/close/approve'>"
               "<button class='primary'>Approve close</button></form>")
        items = _close_items(snap, ack_boxes=False)
    else:
        snap = period.compute(conn, p, pe)
        step = ("<p class='hint'>Step 1 of 2 -- prepare. Every"
                " account must tie; acknowledge each carried item."
                " A second signature approves and locks the month"
                " (one person may do both; the record shows it).</p>")
        if snap["ties_hold"]:
            act = ("<form method='post' action='/billing/close/prepare'>"
                   + _close_items(snap, ack_boxes=True)
                   + "<button class='primary'>Prepare close</button>"
                     "</form>")
            items = ""  # the checkboxes ARE the items list
        else:
            act = ("<div class='attend'>A reconciliation is broken --"
                   " the month cannot close until it ties. "
                   + html.link("/billing/recon", "Reconcile") + "</div>")
            items = _close_items(snap, ack_boxes=False)
    body = (crumbs + f"<h1>{html.esc(title)}</h1>"
            + html.error_box(error) + step
            + "<div class='card'><h2 class='formhead'"
              " style='border-top:none;margin-top:0'>The tie</h2>"
            + _close_ties(snap["accounts"])
            + "<h2 class='formhead'>Carried items</h2>" + items + act
            + "</div><div class='card'>"
            + "<h2 class='formhead' style='border-top:none;"
              "margin-top:0'>The month</h2>" + _close_story(snap["story"])
            + _close_rankings(snap) + "</div>"
            + _closed_months_card(conn))
    return _page(h, title, body, user)


def close_record_screen(h, conn, user, period_str):
    row = period.get_row(conn, period_str, statuses=("closed",))
    if row is None:
        raise _nf()
    snap = json.loads(row["snapshot"])
    pby = reads.get_user(conn, row["prepared_by"])
    aby = reads.get_user(conn, row["approved_by"])
    same = (" Prepared and approved by the same person."
            if row["prepared_by"] == row["approved_by"] else "")
    title = f"Closed: {_month_name(period_str)}"
    body = (_crumbs(("Billing", "/billing"),
                    ("Period close", "/billing/close"),
                    (_month_name(period_str), None))
            + f"<h1>{html.esc(title)}</h1>"
            + "<p class='hint'>The permanent close record: frozen at"
            f" prepare, verified unchanged at approve. Prepared by"
            f" {html.esc(pby['name'])} on {fmt_date(row['prepared_at'])};"
            f" approved by {html.esc(aby['name'])} on"
            f" {fmt_date(row['approved_at'])}.{same}</p>"
            + "<div class='card'><h2 class='formhead'"
              " style='border-top:none;margin-top:0'>The tie</h2>"
            + _close_ties(snap["accounts"])
            + "<h2 class='formhead'>Carried items</h2>"
            + _close_items(snap, ack_boxes=False)
            + "</div><div class='card'>"
            + "<h2 class='formhead' style='border-top:none;"
              "margin-top:0'>The month</h2>" + _close_story(snap["story"])
            + _close_rankings(snap) + "</div>")
    return _page(h, title, body, user)


def close_prepare_post(h, conn, uid, user):
    acks = set(h._form_body_multi().get("ack", []))
    try:
        period.prepare(conn, uid, _today(), acks)
    except ValueError as e:
        conn.rollback()
        return close_screen(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect("/billing/close")


def close_approve_post(h, conn, uid, user):
    try:
        rec = period.approve(conn, uid, _today())
    except ValueError as e:
        conn.commit()  # a stale prepare's VOID must survive the error
        return close_screen(h, conn, user, error=str(e))
    conn.commit()
    return h._redirect(f"/billing/close/{rec['period']}")


# --- router -----------------------------------------------------------

def _nf():
    from app_ui.server import _NotFound
    return _NotFound()


def _id(seg):
    try:
        return int(seg)
    except ValueError:
        raise _nf() from None


def route(h, conn, method, segs, query, now, uid, user):
    """All /billing/* dispatch. Raises server._NotFound for anything
    unrouted -- the tier-3 fence rides on that. Literal segments
    (new / saved / disburse) match before id parses."""
    if method == "GET":
        if segs == ["billing"]:
            return billing_landing(h, conn, user, query)
        if segs == ["billing", "accounts", "new"]:
            return accounts_new(h, conn, user)
        if segs == ["billing", "invoices", "new"]:
            return invoice_new(h, conn, user)
        if segs == ["billing", "charges", "saved"]:
            return saved_charges(h, conn, user)
        if segs == ["billing", "time", "new"]:
            return time_new(h, conn, user)
        if segs == ["billing", "trust", "disburse"]:
            return disburse_form(h, conn, user)
        if segs == ["billing", "trust"]:
            return trust_overview(h, conn, user)
        if len(segs) == 3 and segs[:2] == ["billing", "trust"]:
            return account_ledger(h, conn, user, _id(segs[2]))
        if len(segs) == 4 and segs[:2] == ["billing", "invoices"] \
                and segs[3] == "pdf":
            return invoice_pdf_download(h, conn, _id(segs[2]))
        if len(segs) == 3 and segs[:2] == ["billing", "invoices"]:
            return invoice_detail(h, conn, user, _id(segs[2]))
        if len(segs) == 3 and segs[:2] == ["billing", "journal"]:
            return journal_detail(h, conn, user, _id(segs[2]))
        if len(segs) == 3 and segs[:2] == ["billing", "payments"]:
            return payment_detail(h, conn, user, _id(segs[2]))
        if len(segs) == 4 and segs[:2] == ["billing", "clients"] \
                and segs[3] == "payments":
            return client_payments(h, conn, user, _id(segs[2]))
        if segs == ["billing", "recon"]:
            return recon_screen(h, conn, user, query)
        if segs == ["billing", "close"]:
            return close_screen(h, conn, user)
        if len(segs) == 3 and segs[:2] == ["billing", "close"]:
            s = segs[2]
            if not (len(s) == 7 and s[:4].isdigit() and s[4] == "-"
                    and s[5:7].isdigit()):
                raise _nf()
            return close_record_screen(h, conn, user, s)
        if segs == ["billing", "time"]:
            return time_index(h, conn, user)
    if method == "POST":
        if segs == ["billing", "accounts", "new"]:
            return accounts_create(h, conn, uid, user)
        if segs == ["billing", "invoices", "new"]:
            return invoice_create(h, conn, uid, user)
        if segs == ["billing", "charges", "saved"]:
            return saved_charge_create(h, conn, uid, user)
        if segs == ["billing", "time", "new"]:
            return time_create(h, conn, uid, user)
        if segs == ["billing", "trust", "disburse"]:
            return disburse_post(h, conn, uid, user)
        if segs == ["billing", "settle"]:
            return settle_post(h, conn, uid, user)
        if segs == ["billing", "close", "prepare"]:
            return close_prepare_post(h, conn, uid, user)
        if segs == ["billing", "close", "approve"]:
            return close_approve_post(h, conn, uid, user)
        if len(segs) == 4 and segs[:2] == ["billing", "invoices"]:
            invoice_id = _id(segs[2])
            if segs[3] == "charges":
                return charge_create(h, conn, uid, user, invoice_id)
            if segs[3] == "import":
                return invoice_import(h, conn, uid, user, invoice_id)
            if segs[3] == "pay":
                return invoice_pay(h, conn, uid, user, invoice_id)
            if segs[3] == "share":
                return invoice_share(h, conn, uid, user, invoice_id)
            if segs[3] == "email":
                return invoice_email_share(h, conn, uid, user,
                                           invoice_id)
        if len(segs) == 4 and segs[:2] == ["billing", "payments"]:
            payment_id = _id(segs[2])
            if segs[3] == "edit":
                return payment_edit(h, conn, uid, user, payment_id)
            if segs[3] == "refund":
                return payment_refund(h, conn, uid, user, payment_id)
    raise _nf()
