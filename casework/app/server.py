"""Client intake HTTP surface (U2.5, P2 gate ruling 2).

Stdlib localhost server; every client route is token-scoped under
/intake/<token>. Pages are plain HTML forms -- no JavaScript is
required to complete an intake (the mobile-intake mechanical
proxy): any device with a browser can GET the page and POST
answers. The firm side stays module-level until a later UI phase.

Requests serialize on one lock over the app's single connection.
"""

import html
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
        balance = billing.invoice_balance(conn, inv["id"])
        rows = "".join(
            f"<li>{html.escape(c['description'])} "
            f"{c['amount_cents'] / 100:,.2f}</li>"
            for c in billing.invoice_charges(conn, inv["id"]))
        pay = ""
        if balance > 0:
            pay = (f'<form method="post" action="/invoice/{segs[1]}/pay">'
                   '<label>Synthetic payment token '
                   '<input name="sim_token" '
                   'placeholder="SYNTHETIC-VISA-DEMO" '
                   'autocomplete="off"></label>'
                   '<p>Use the demo token shown above. This is not a real '
                   'card number.</p>'
                   '<label>Payment method <select name="kind">'
                   '<option value="card">card</option>'
                   '<option value="echeck">echeck</option></select>'
                   '</label>'
                   '<button type="submit">Pay</button></form>')
        body = (f"<h1>{strings[inv['invoice_type']]} #{inv['number']}</h1>"
                f"<ul>{rows}</ul>"
                f"<p>{strings['balance_due']}: {balance / 100:,.2f}</p>"
                f'<p><a href="/invoice/{segs[1]}/pdf">PDF</a></p>{pay}')
        return self._send(200, _page("Invoice", body))

    def _invoice_pay(self, conn, token):
        from app import billing
        share = billing.share_by_token(conn, token)
        if share is None:
            return self._deny(404, "This link is no longer available.")
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
                billing.pay_online(conn, share["invoice_id"], sim_token,
                                   kind, _now()[:10])
            except (proc.ProcessorError, billing.BillingError) as ex:
                return self._send(200, _page("Payment",
                                             f"<p>Declined: "
                                             f"{html.escape(str(ex))}</p>"))
            return self._send(200, _page("Payment",
                                         "<p>Payment received.</p>"))
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
        rows = []
        for f in esign.fields_of(conn, signer["esign_file_id"],
                                 signer["id"]):
            rows.append(
                f"<label>{html.escape(f['field_type'])} (page {f['page']})"
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
