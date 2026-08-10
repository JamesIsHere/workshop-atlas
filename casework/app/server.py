"""Client intake HTTP surface (U2.5, P2 gate ruling 2).

Stdlib localhost server; every client route is token-scoped under
/intake/<token>. Pages are plain HTML forms -- no JavaScript is
required to complete an intake (the mobile-intake mechanical
proxy): any device with a browser can GET the page and POST
answers. The firm side stays module-level until a later UI phase.

The shared-invoice surface (view/pay/receipt) is firm-branded and
styled (program ruling 2026-08-07, ratified by James: rendering-only
-- SELECT-only readers, the only write path is billing.pay_online).
Intake and e-sign pages are outside that ruling and keep _page.

Requests serialize on one lock over the app's single connection.
"""

import html
import json
import threading
import urllib.parse
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from app import custom, esign, intake, invitations, translations


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _page(title, body):
    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,"
            f" initial-scale=1'><title>{html.escape(title)}</title>"
            f"</head><body>{body}</body></html>").encode("utf-8")


# --- client invoice surface chrome (program ruling 2026-08-07,
# ratified by James: rendering-only; the intake/e-sign pages above
# keep _page and are NOT in that ruling's scope) -------------------

# Palette and shapes mirror the staff surface's stylesheet
# (casework-ui/app_ui/html.py STYLE) so the client page reads as the
# same product; duplicated by design -- the core cannot import app_ui.
CLIENT_STYLE = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; margin: 0;
       background: #f4f5f7; color: #1a1d21; }
header { background: #1f2a3d; color: #e8ebf0; padding: 0.6rem 1.2rem; }
header .brand { font-weight: 600; letter-spacing: 0.02em; }
main { max-width: 46rem; margin: 2rem auto; padding: 0 1.2rem; }
.card { background: #ffffff; border: 1px solid #d9dde3;
        border-radius: 6px; padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem; }
h1 { font-size: 1.25rem; margin: 0 0 1rem; }
h2 { font-size: 1rem; margin: 1.4rem 0 0.4rem; color: #4a5261; }
label { display: block; margin: 0.8rem 0 0.25rem; font-size: 0.9rem;
        color: #4a5261; }
input, select { width: 100%; max-width: 22rem;
        padding: 0.45rem 0.6rem; border: 1px solid #c3c9d2;
        border-radius: 4px; font-size: 1rem; }
button.primary { margin-top: 1.2rem; background: #2456a6;
        color: #fff; border: none; border-radius: 4px;
        padding: 0.55rem 1.4rem; font-size: 1rem; cursor: pointer; }
button.primary:hover { background: #1c468a; }
.error { background: #fdecec; border: 1px solid #e5b3b3;
         color: #8a2525; border-radius: 4px; padding: 0.6rem 0.9rem;
         margin-bottom: 1rem; }
.hint { color: #6a7383; font-size: 0.85rem; }
table.data { width: 100%; border-collapse: collapse; margin: 0.8rem 0; }
table.data th { text-align: left; font-size: 0.8rem; color: #6a7383;
                text-transform: uppercase; letter-spacing: 0.05em;
                border-bottom: 2px solid #d9dde3;
                padding: 0.4rem 0.6rem; }
table.data td { border-bottom: 1px solid #e7eaee;
                padding: 0.5rem 0.6rem; }
table.data th.money, table.data td.money { text-align: right;
                font-variant-numeric: tabular-nums; }
table.data tr.total td { border-top: 2px solid #d9dde3;
                border-bottom: none; font-weight: 600; }
.pill { display: inline-block; border-radius: 10px;
        padding: 0.1rem 0.6rem; font-size: 0.8rem; background: #e6f4e6;
        color: #256325; vertical-align: middle; margin-left: 0.5rem; }
.kv dt { float: left; clear: left; width: 11rem; color: #6a7383;
         font-size: 0.9rem; padding: 0.25rem 0; }
.kv dd { margin-left: 12rem; padding: 0.25rem 0; }
.actions { margin: 0.8rem 0 0; }
.actions a { display: inline-block; background: #eef1f5;
             color: #2456a6; border-radius: 4px; padding: 0.45rem 1rem;
             text-decoration: none; margin-right: 0.6rem; }
"""

# Chrome labels billing.INVOICE_STRINGS never needed (fx-0052 covers
# the invoice template only). The pay form's own labels ("Synthetic
# payment token", "SYNTHETIC-VISA-DEMO", "Payment method", "Pay") and
# the en receipt heading "Payment received." are PINNED by the demo
# walk sheet and its verifiers -- change them only with a sheet
# re-sync. The pay form stays English-only as before (synthetic demo
# machinery, not invoice chrome).
CLIENT_STRINGS = {
    "en": {"payments": "Payments", "paid": "Paid", "method": "Method",
           "received": "Payment received.", "reference": "Reference",
           "remaining": "Remaining balance",
           "back": "View the invoice"},
    "es": {"payments": "Pagos", "paid": "Pagada", "method": "Metodo",
           "received": "Pago recibido.", "reference": "Referencia",
           "remaining": "Saldo restante",
           "back": "Ver la factura"},
}

_METHOD_LABELS = {"sim_card": "card", "sim_echeck": "eCheck",
                  "trust_transfer": "trust transfer",
                  "direct": "direct"}


def _client_page(title, firm, body):
    """Firm-branded document for the shared-invoice surface only."""
    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,"
            f" initial-scale=1'><title>{html.escape(title)}</title>"
            f"<style>{CLIENT_STYLE}</style></head><body>"
            f"<header><span class='brand'>{html.escape(firm)}</span>"
            f"</header><main>{body}</main></body></html>").encode("utf-8")


def _kv(pairs):
    """Definition list; keys escaped here, values pre-escaped."""
    return ("<dl class='kv'>" +
            "".join(f"<dt>{html.escape(k)}</dt><dd>{v}</dd>"
                    for k, v in pairs) + "</dl>")


def _intake_items(conn, inv, lang):
    """Invitee view minus the invitation's restricted tabs, in the
    invitation's (or requested) language."""
    items = intake.combined_intake(conn, inv["smart_form_id"],
                                   viewer="invitee")
    restricted = invitations.restricted_tabs_of(inv)
    items = [i for i in items if i["tab"] not in restricted]
    return translations.translate_items(items, lang)


class Handler(BaseHTTPRequestHandler):
    server_version = "casework/0.1"

    # --- plumbing ---

    def log_message(self, fmt, *args):
        pass  # no console noise; requests are audited in-db

    def _send(self, status, content, ctype="text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _deny(self, status=404, msg="Not found"):
        self._send(status, _page("Unavailable", f"<p>{html.escape(msg)}</p>"))

    def _live_invitation(self, conn, token):
        inv = invitations.by_token(conn, token)
        if inv is None or inv["status"] == "revoked":
            return None
        return inv

    def _route(self):
        parts = urllib.parse.urlparse(self.path)
        segs = [s for s in parts.path.split("/") if s]
        query = urllib.parse.parse_qs(parts.query)
        return segs, query

    def _form_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        return urllib.parse.parse_qs(raw.decode("utf-8"))

    def _multipart_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        head = (f"Content-Type: {self.headers['Content-Type']}\r\n"
                "MIME-Version: 1.0\r\n\r\n").encode()
        msg = BytesParser(policy=policy.default).parsebytes(head + raw)
        fields, files = {}, {}
        for part in msg.iter_parts():
            name = part.get_param("name", header="content-disposition")
            filename = part.get_filename()
            if filename:
                files[name] = (filename, part.get_payload(decode=True))
            else:
                fields[name] = part.get_content().strip()
        return fields, files

    # --- GET ---

    def do_GET(self):
        conn = self.server.app_conn
        segs, query = self._route()
        if len(segs) == 2 and segs[0] == "esign":
            with self.server.app_lock:
                return self._esign_page(conn, segs[1])
        if len(segs) >= 2 and segs[0] == "invoice":
            with self.server.app_lock:
                return self._invoice_get(conn, segs)
        if len(segs) < 2 or segs[0] != "intake":
            return self._deny()
        with self.server.app_lock:
            inv = self._live_invitation(conn, segs[1])
            if inv is None:
                return self._deny(404, "This link is no longer available.")
            conn.actor.set("contact", inv["contact_id"])
            try:
                if len(segs) == 2:
                    return self._intake_page(conn, inv, query)
                if segs[2] == "search":
                    return self._search_page(conn, inv, query)
            finally:
                conn.actor.set("system", None)
        self._deny()

    # --- shared invoice (casework-billing P3 U3.3: view/download/pay;
    # the client-side actor the adapted online-card-payment criterion
    # requires; sharing EMAILS are P4) ---

    def _invoice_get(self, conn, segs):
        from app import billing
        share = billing.share_by_token(conn, segs[1])
        if share is None:
            return self._deny(404, "This link is no longer available.")
        inv = billing.get_invoice(conn, share["invoice_id"])
        if len(segs) == 3 and segs[2] == "pdf":
            out = Path(self.server.storage_dir) / f"invoice-{inv['id']}.pdf"
            billing.invoice_pdf(conn, inv["id"], str(out))
            return self._send(200, out.read_bytes(),
                              ctype="application/pdf")
        if len(segs) != 2:
            return self._deny()
        strings = billing.INVOICE_STRINGS.get(inv["language"],
                                              billing.INVOICE_STRINGS["en"])
        cstr = CLIENT_STRINGS.get(inv["language"], CLIENT_STRINGS["en"])
        cents, mdy = billing._pdf_cents, billing._pdf_date
        firm = billing.get_setting(conn, "firm.name", "SYNTH Firm")
        contact = conn.execute(
            "SELECT display_name FROM contacts WHERE id=?",
            (inv["contact_id"],)).fetchone()
        balance = billing.invoice_balance(conn, inv["id"])

        kv = [(strings["client"], html.escape(contact["display_name"]))]
        if inv["issued_date"]:
            kv.append((strings["issued"], mdy(inv["issued_date"])))
        if inv["due_date"]:
            kv.append((strings["due"], mdy(inv["due_date"])))
        # the client's remaining trust, same reader as invoice_pdf
        # (item H, 2026-08-07: fiduciary storytelling; shown only once
        # the client actually has a trust sub-ledger)
        subs = [r[0] for r in conn.execute(
            "SELECT a.id FROM ledger_accounts a"
            " JOIN ledger_accounts p ON p.id = a.parent_id"
            " AND p.kind = 'trust_bank'"
            " LEFT JOIN matters m ON m.id = a.matter_id"
            " WHERE a.deleted_at IS NULL"
            " AND (a.contact_id = ? OR m.primary_contact_id = ?)",
            (inv["contact_id"], inv["contact_id"]))]
        if subs:
            held = sum(billing.account_balance(conn, a) for a in subs)
            kv.append((strings["trust_held"], cents(held)))

        rows = "".join(
            f"<tr><td>{html.escape(c['description'])}</td>"
            f"<td>{mdy(c['charge_date'])}</td>"
            f"<td class='money'>{cents(c['amount_cents'])}</td></tr>"
            for c in billing.invoice_charges(conn, inv["id"]))
        if inv["discount_cents"]:
            rows += (f"<tr><td>{html.escape(strings['discount'])}</td>"
                     f"<td></td><td class='money'>"
                     f"-{cents(inv['discount_cents'])}</td></tr>")
        rows += (f"<tr class='total'>"
                 f"<td>{html.escape(strings['balance_due'])}</td><td></td>"
                 f"<td class='money'>{cents(balance)}</td></tr>")
        charges = (f"<h2>{html.escape(strings['charges'])}</h2>"
                   f"<table class='data'><thead><tr>"
                   f"<th>{html.escape(strings['description'])}</th>"
                   f"<th>{html.escape(strings['date'])}</th>"
                   f"<th class='money'>{html.escape(strings['amount'])}"
                   f"</th></tr></thead><tbody>{rows}</tbody></table>")

        payments = conn.execute(
            "SELECT * FROM invoice_payments WHERE invoice_id=?"
            " AND deleted_at IS NULL ORDER BY id",
            (inv["id"],)).fetchall()
        ptable = ""
        if payments:
            prows = "".join(
                f"<tr><td>{mdy(p['payment_date'])}</td>"
                f"<td>{_METHOD_LABELS.get(p['method'], p['method'])}"
                f"{' (refunded)' if p['refunded'] else ''}</td>"
                f"<td class='money'>{cents(p['amount_cents'])}</td></tr>"
                for p in payments)
            ptable = (f"<h2>{html.escape(cstr['payments'])}</h2>"
                      f"<table class='data'><thead><tr>"
                      f"<th>{html.escape(strings['date'])}</th>"
                      f"<th>{html.escape(cstr['method'])}</th>"
                      f"<th class='money'>{html.escape(strings['amount'])}"
                      f"</th></tr></thead><tbody>{prows}</tbody></table>")

        pay = ""
        if balance > 0:
            # labels pinned by the walk sheet -- see CLIENT_STRINGS note
            pay = (f'<form method="post" action="/invoice/{segs[1]}/pay">'
                   '<label>Synthetic payment token '
                   '<input name="sim_token" '
                   'placeholder="SYNTHETIC-VISA-DEMO" '
                   'autocomplete="off"></label>'
                   "<p class='hint'>Use the demo token shown above. This"
                   ' is not a real card number.</p>'
                   '<label>Payment method <select name="kind">'
                   '<option value="card">card</option>'
                   '<option value="echeck">echeck</option></select>'
                   '</label>'
                   "<button class='primary' type='submit'>Pay</button>"
                   '</form>')
        paid = (f"<span class='pill'>{html.escape(cstr['paid'])}</span>"
                if balance <= 0 else "")
        footer = (f"<p class='hint'>{html.escape(inv['footer'])}</p>"
                  if inv["footer"] else "")
        title = f"{strings[inv['invoice_type']]} {inv['display_code']}"
        body = (f"<div class='card'>"
                f"<h1>{html.escape(title)}{paid}</h1>"
                f"{_kv(kv)}{charges}{ptable}"
                f"<div class='actions'>"
                f"<a href='/invoice/{segs[1]}/pdf'>PDF</a></div>"
                f"{pay}{footer}</div>")
        return self._send(200, _client_page(title, firm, body))

    def _invoice_pay(self, conn, token):
        from app import billing
        share = billing.share_by_token(conn, token)
        if share is None:
            return self._deny(404, "This link is no longer available.")
        inv = billing.get_invoice(conn, share["invoice_id"])
        strings = billing.INVOICE_STRINGS.get(inv["language"],
                                              billing.INVOICE_STRINGS["en"])
        cstr = CLIENT_STRINGS.get(inv["language"], CLIENT_STRINGS["en"])
        cents, mdy = billing._pdf_cents, billing._pdf_date
        firm = billing.get_setting(conn, "firm.name", "SYNTH Firm")
        back = (f"<div class='actions'><a href='/invoice/{token}'>"
                f"{html.escape(cstr['back'])}</a></div>")
        form = self._form_body()
        sim_token = form.get("sim_token", [""])[0].strip()
        kind = form.get("kind", ["card"])[0]
        conn.actor.set("contact", share["recipient_contact_id"])
        try:
            from app import processor as proc
            try:
                if not sim_token:
                    raise proc.ProcessorError(
                        "enter a synthetic payment token beginning with"
                        " SYNTHETIC-")
                # firm-local business date (ruling 2026-08-09): the
                # payment DATE is a books fact; UTC dated evening
                # payments tomorrow. Audit timestamps stay UTC.
                pid = billing.pay_online(conn, share["invoice_id"],
                                         sim_token, kind,
                                         datetime.now().strftime(
                                             "%Y-%m-%d"))
            except (proc.ProcessorError, billing.BillingError) as ex:
                body = (f"<div class='card'><div class='error'>Declined: "
                        f"{html.escape(str(ex))}</div>{back}</div>")
                return self._send(200, _client_page("Payment", firm, body))
            # Every sibling POST handler commits its write; this one
            # never did -- the payment sat uncommitted on the shared
            # connection until some firm-side action committed it.
            # FLAGGED as a judgment call in the worklog (2026-08-07).
            conn.commit()
            p = billing.get_payment(conn, pid)
            remaining = billing.invoice_balance(conn, inv["id"])
            kv = [(strings[inv["invoice_type"]],
                   html.escape(inv["display_code"])),
                  (strings["date"], mdy(p["payment_date"])),
                  (cstr["method"],
                   _METHOD_LABELS.get(p["method"], p["method"])),
                  (strings["amount"], cents(p["amount_cents"])),
                  (cstr["reference"],
                   html.escape(str(p["processor_txn_id"] or
                                   f"payment {pid}"))),
                  (cstr["remaining"], cents(remaining))]
            body = (f"<div class='card'>"
                    f"<h1>{html.escape(cstr['received'])}</h1>"
                    f"{_kv(kv)}{back}</div>")
            return self._send(200, _client_page("Payment", firm, body))
        finally:
            conn.actor.set("system", None)

    def _intake_page(self, conn, inv, query):
        lang = query.get("lang", [inv["language"]])[0]
        invitations.accept(conn, inv["token"], _now())  # opened = accepted
        items = _intake_items(conn, inv, lang)
        token = inv["token"]
        rows = []
        tab = None
        for i in items:
            if i["tab"] != tab:
                tab = i["tab"]
                rows.append(f"<h2>{html.escape(tab)}</h2>")
            flag = " [FLAGGED]" if i["flagged"] else ""
            if i["qtype"] == "document_request":
                rows.append(
                    f"<form method='post' action='/intake/{token}/upload'"
                    f" enctype='multipart/form-data'>"
                    f"<label>{html.escape(i['label'])}{flag}"
                    f"<input type='file' name='file'></label>"
                    f"<input type='hidden' name='question' value='{i['key']}'>"
                    f"<button>Upload</button></form>")
                continue
            value = ""
            rows.append(
                f"<form method='post' action='/intake/{token}/answer'>"
                f"<label>{html.escape(i['label'])}{flag}"
                f" <input name='value' value='{html.escape(value)}'></label>"
                f"<input type='hidden' name='question' value='{i['key']}'>"
                f"<button>Save</button></form>")
        langs = " ".join(
            f"<a href='/intake/{token}?lang={code}'>{code}</a>"
            for code in translations.languages())
        body = (f"<h1>Your questionnaire</h1>"
                f"<p>Language: {langs}</p>"
                f"<form method='get' action='/intake/{token}/search'>"
                f"<input name='q' placeholder='Search questions'>"
                f"<button>Search</button></form>"
                + "".join(rows) +
                f"<form method='post' action='/intake/{token}/submit'>"
                f"<button>Submit for review</button></form>")
        self._send(200, _page("Questionnaire", body))

    def _search_page(self, conn, inv, query):
        kw = query.get("q", [""])[0]
        lang = query.get("lang", [inv["language"]])[0]
        items = _intake_items(conn, inv, lang)
        kw_l = kw.lower()
        hits = [i for i in items if kw_l in i["label"].lower()]
        body = (f"<h1>Search: {html.escape(kw)}</h1><ul>" +
                "".join(f"<li>{html.escape(i['tab'])}:"
                        f" {html.escape(i['label'])}</li>" for i in hits) +
                "</ul>")
        self._send(200, _page("Search", body))

    def _esign_page(self, conn, token):
        """The secure signing link: this signer's required fields as a
        plain form -- signature/initials by drawing (strokes JSON) or
        typing, no JavaScript required (fx-0194/0199)."""
        signer = esign.signer_by_token(conn, token)
        if signer is None:
            return self._deny(404, "This link is no longer available.")
        es = conn.execute("SELECT * FROM esign_files WHERE id=?",
                          (signer["esign_file_id"],)).fetchone()
        if es["status"] != "requested":
            return self._deny(404, "This document is not open for signing.")
        # Human field prompts (program ruling 2026-08-10,
        # casework-tabs P4b gate: a bare field-type label left the
        # signer typing into an unexplained box). APPENDED to the
        # original "type (page N)" label, which a spine test pins
        # verbatim -- spine tests are immutable.
        prompts = {
            "signature": "sign by typing your full name",
            "initials": "type your initials",
            "text": "type the requested text",
            "date": "leave blank to date it today",
        }
        rows = []
        for f in esign.fields_of(conn, signer["esign_file_id"],
                                 signer["id"]):
            prompt = prompts.get(f["field_type"])
            suffix = f" -- {prompt}" if prompt else ""
            rows.append(
                f"<label>{html.escape(f['field_type'])} (page {f['page']})"
                f"{html.escape(suffix)}"
                f"<input name='field_{f['id']}'></label><br>")
        body = (f"<h1>Sign document</h1>"
                f"<form method='post' action='/esign/{token}/sign'>"
                + "".join(rows) + "<button>Sign</button></form>")
        self._send(200, _page("Sign document", body))

    def _esign_sign(self, conn, token):
        signer = esign.signer_by_token(conn, token)
        if signer is None:
            return self._deny(404, "This link is no longer available.")
        conn.actor.set("contact", signer["contact_id"])
        try:
            form = self._form_body()
            values = {}
            for key, vals in form.items():
                if key.startswith("field_"):
                    values[int(key.split("_", 1)[1])] = vals[0]
            # A plain typed value in a signature/initials box is a
            # TYPED signature (program ruling 2026-08-10): wrap it
            # into the core's JSON contract here; structured JSON
            # (e.g. drawn strokes) passes through untouched.
            ftypes = {f["id"]: f["field_type"]
                      for f in esign.fields_of(
                          conn, signer["esign_file_id"],
                          signer["id"])}
            for fid, value in list(values.items()):
                if ftypes.get(fid) in ("signature", "initials"):
                    try:
                        json.loads(value)
                    except ValueError:
                        values[fid] = json.dumps(
                            {"mode": "type", "text": value})
            esign.sign(conn, signer["esign_file_id"], signer["id"], values,
                       _now(), self.server.storage_dir)
            conn.commit()
        except ValueError as e:
            return self._deny(400, str(e))
        finally:
            conn.actor.set("system", None)
        self._send(200, _page("Signed", "<p>Thank you. Your signature was"
                              " recorded.</p>"))

    # --- POST ---

    def do_POST(self):
        conn = self.server.app_conn
        segs, _query = self._route()
        if len(segs) == 3 and segs[0] == "esign" and segs[2] == "sign":
            with self.server.app_lock:
                return self._esign_sign(conn, segs[1])
        if len(segs) == 3 and segs[0] == "invoice" and segs[2] == "pay":
            with self.server.app_lock:
                return self._invoice_pay(conn, segs[1])
        if len(segs) != 3 or segs[0] != "intake":
            return self._deny()
        with self.server.app_lock:
            inv = self._live_invitation(conn, segs[1])
            if inv is None:
                return self._deny(404, "This link is no longer available.")
            conn.actor.set("contact", inv["contact_id"])
            try:
                if segs[2] == "answer":
                    return self._post_answer(conn, inv)
                if segs[2] == "submit":
                    return self._post_submit(conn, inv)
                if segs[2] == "comment":
                    return self._post_comment(conn, inv)
                if segs[2] == "upload":
                    return self._post_upload(conn, inv)
            finally:
                conn.actor.set("system", None)
        self._deny()

    def _post_answer(self, conn, inv):
        form = self._form_body()
        qkey = form.get("question", [None])[0]
        value = form.get("value", [""])[0]
        idx = int(form.get("idx", ["0"])[0])
        # a hidden or tab-restricted question is not writable by link
        allowed = {i["key"] for i in _intake_items(conn, inv, "en")}
        if qkey not in allowed:
            return self._deny(403, "That question is not available.")
        intake.answer_intake(conn, inv["smart_form_id"], qkey, value,
                             _now(), idx)
        conn.commit()
        self._send(200, _page("Saved", "<p>Answer saved.</p>"
                              f"<a href='/intake/{inv['token']}'>Back</a>"))

    def _post_submit(self, conn, inv):
        invitations.return_for_review(conn, inv["token"], _now())
        conn.commit()
        self._send(200, _page("Submitted",
                              "<p>Thank you. Your questionnaire was"
                              " returned for review.</p>"))

    def _post_comment(self, conn, inv):
        blocked = conn.execute(
            "SELECT value FROM firm_settings WHERE"
            " key='invitation.block_comments'").fetchone()
        if blocked and blocked["value"] == "1":
            return self._deny(403, "Commenting is disabled.")
        form = self._form_body()
        qkey = form.get("question", [None])[0]
        body = form.get("body", [""])[0]
        intake.add_comment(conn, inv["smart_form_id"], qkey, "contact",
                           inv["contact_id"], body, _now())
        conn.commit()
        self._send(200, _page("Comment posted", "<p>Comment posted.</p>"))

    def _post_upload(self, conn, inv):
        fields, files = self._multipart_body()
        upload = files.get("file")
        if upload is None:
            return self._deny(400, "No file provided.")
        filename, content = upload
        qkey = fields.get("question")
        question_id = None
        if qkey and qkey.startswith("cq."):
            question_id = int(qkey.split(".", 1)[1])
        custom.save_client_upload(conn, inv["smart_form_id"], filename,
                                  content, _now(),
                                  self.server.storage_dir,
                                  question_id=question_id)
        conn.commit()
        self._send(200, _page("Uploaded",
                              f"<p>{html.escape(filename)} received.</p>"))


def make_server(conn, storage_dir, port=0):
    """Bind the client surface to localhost:port (0 = ephemeral).
    Returns the server; run it with serve_forever on a thread."""
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    httpd.app_conn = conn
    httpd.app_lock = threading.Lock()
    httpd.storage_dir = Path(storage_dir)
    return httpd


def base_url(httpd):
    host, port = httpd.server_address[:2]
    return f"http://{host}:{port}"
