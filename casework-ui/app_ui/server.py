"""The firm-facing UI server (P0: skeleton + first-run + auth).

Stdlib ThreadingHTTPServer over ONE casework connection, serialized
by a lock (the casework client-surface pattern). All business logic
lives in casework's app modules; this file is routing, sessions,
and rendering. Display-only SQL is quarantined in app_ui/reads.py.

Auth is casework's real path -- password + mandatory TOTP
enrollment + session -- no bypass (goal.md: the cold user logs in
for real). Every route except /login, /setup and the MFA pair sits
behind the session cookie.

Run: python -m app_ui.server --db data/ui.db [--port 8500]
A missing db file is created (schema + bootstrap.install + the
synthetic marker): the first visit then enters the /setup flow.
"""

import argparse
import calendar as pycal
import re
import tempfile
import threading
import urllib.parse
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import app_ui  # noqa: F401  (wires casework onto sys.path)
from app import auth, billing, bootstrap, contacts, events, facts
from app import files, forms
from app import db as appdb
from app import invitations, matters, notes, render, search, tasks, users
from app import server as cw_server
from app_ui import html, reads


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class _NotFound(Exception):
    """Raised by views for missing/foreign ids; rendered as the
    'Not built yet / not found' page by the router."""


def _id(seg):
    try:
        return int(seg)
    except ValueError:
        raise _NotFound() from None


def _fmt_size(n):
    if n is None:
        return "-"
    return f"{n} B" if n < 1024 else f"{n / 1024:.1f} KB"


class Handler(BaseHTTPRequestHandler):
    server_version = "casework-ui/0.1"

    def log_message(self, fmt, *args):
        pass  # mutations are audited in-db; no console noise

    # --- plumbing ---

    def _send_page(self, status, content, cookies=None):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        for c in cookies or []:
            self.send_header("Set-Cookie", c)
        self.end_headers()
        self.wfile.write(content)

    def _redirect(self, location, cookies=None):
        self.send_response(303)
        self.send_header("Location", location)
        for c in cookies or []:
            self.send_header("Set-Cookie", c)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _session_token(self):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        morsel = cookie.get("session")
        return morsel.value if morsel else None

    def _form_body(self):
        return {k: v[0] for k, v in self._form_body_multi().items()}

    def _form_body_multi(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        return urllib.parse.parse_qs(raw)

    def _send_file(self, content, filename, ctype="application/pdf"):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Disposition",
                         f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_inline(self, content, ctype):
        """Displayable bytes (preview/print views): no attachment
        disposition, the browser renders in the tab."""
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _multipart_body(self):
        """Multipart parse for the files-tab upload (casework-tabs
        P4a). Mirrors the frozen client surface's parser --
        duplicated by design: the core cannot import app_ui."""
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        head = (f"Content-Type: {self.headers['Content-Type']}\r\n"
                "MIME-Version: 1.0\r\n\r\n").encode()
        msg = BytesParser(policy=policy.default).parsebytes(head + raw)
        fields, uploads = {}, {}
        for part in msg.iter_parts():
            name = part.get_param("name", header="content-disposition")
            filename = part.get_filename()
            if filename:
                uploads[name] = (filename,
                                 part.get_payload(decode=True))
            else:
                fields[name] = part.get_content().strip()
        return fields, uploads

    @staticmethod
    def _cookie(token):
        return f"session={token}; Path=/; HttpOnly; SameSite=Lax"

    # --- request entry ---

    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        self._dispatch("POST")

    def _dispatch(self, method):
        conn = self.server.app_conn
        path = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"
        with self.server.app_lock:
            try:
                self._route(conn, method, path)
            finally:
                conn.actor.set("system", None)

    def _route(self, conn, method, path):
        now = _now()
        open_routes = {
            ("GET", "/login"): self._login_page,
            ("POST", "/login"): self._login_post,
            ("GET", "/setup"): self._setup_page,
            ("POST", "/setup"): self._setup_post,
            ("GET", "/enroll-mfa"): self._enroll_page,
            ("POST", "/enroll-mfa"): self._enroll_post,
            ("GET", "/mfa"): self._mfa_page,
            ("POST", "/mfa"): self._mfa_post,
        }
        handler = open_routes.get((method, path))
        if handler is not None:
            return handler(conn, now)

        # everything else requires a fully-authenticated session
        token = self._session_token()
        uid = auth.session_user(conn, token, now) if token else None
        if uid is None:
            if reads.user_count(conn) == 0:
                return self._redirect("/setup")
            return self._redirect("/login")
        conn.actor.set("user", uid)
        user = reads.get_user(conn, uid)

        if method == "POST" and path == "/logout":
            auth.logout(conn, token)
            conn.commit()
            return self._redirect("/login")
        try:
            return self._route_authed(conn, method, path, now, uid, user)
        except _NotFound:
            return self._not_found(user)

    def _route_authed(self, conn, method, path, now, uid, user):
        segs = [s for s in path.split("/") if s]
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path)
                                      .query)
        if segs and segs[0] == "billing":
            # billing-ui child surface (program ruling 2026-08-04);
            # one dispatch hook, all logic in billing_ui.py
            from app_ui import billing_ui
            return billing_ui.route(self, conn, method, segs, query,
                                    now, uid, user)
        if method == "GET":
            if not segs:
                return self._dashboard(conn, user)
            if segs == ["contacts"]:
                return self._contacts_index(conn, user)
            if segs == ["contacts", "new"]:
                return self._contact_new(conn, user)
            if len(segs) == 2 and segs[0] == "contacts":
                return self._contact_detail(conn, user, _id(segs[1]))
            if segs == ["matters"]:
                return self._matters_index(conn, user)
            if segs == ["matters", "new"]:
                return self._matter_new(conn, user, query)
            if len(segs) == 2 and segs[0] == "matters":
                return self._matter_detail(conn, user, _id(segs[1]))
            if segs == ["files"]:
                return self._files_index(conn, user, query)
            if segs == ["files", "bulk-download"]:
                return self._files_bulk(conn, query)
            if len(segs) == 3 and segs[0] == "files" \
                    and segs[2] == "download":
                return self._file_download(conn, _id(segs[1]))
            if len(segs) == 3 and segs[0] == "files" \
                    and segs[2] == "preview":
                return self._file_preview(conn, _id(segs[1]))
            if len(segs) == 3 and segs[0] == "files" \
                    and segs[2] == "print":
                return self._file_print(conn, _id(segs[1]))
            if len(segs) == 2 and segs[0] == "files":
                return self._file_detail(conn, user, _id(segs[1]))
            if segs == ["tasks"]:
                return self._tasks_index(conn, user, query)
            if len(segs) == 2 and segs[0] == "tasks":
                return self._task_detail(conn, user, _id(segs[1]))
            if segs == ["settings", "task-lists"]:
                return self._task_lists(conn, user)
            if len(segs) == 3 and segs[0] == "settings" \
                    and segs[1] == "task-lists":
                return self._task_list_detail(conn, user,
                                              _id(segs[2]))
            if segs == ["notes"]:
                return self._notes_index(conn, user, query)
            if segs == ["notes", "new"]:
                return self._note_new(conn, user, query)
            if len(segs) == 2 and segs[0] == "notes":
                return self._note_detail(conn, user, _id(segs[1]))
            if segs == ["settings", "note-categories"]:
                return self._note_categories(conn, user)
            if len(segs) == 3 and segs[0] == "matters" \
                    and segs[2] == "notes.pdf":
                return self._notes_pdf(conn, matter_id=_id(segs[1]))
            if len(segs) == 3 and segs[0] == "contacts" \
                    and segs[2] == "notes.pdf":
                return self._notes_pdf(conn, contact_id=_id(segs[1]))
            if segs == ["search"]:
                return self._search(conn, user, query)
            if segs == ["settings"]:
                return self._settings(conn, user)
            if len(segs) == 3 and segs[0] == "matters" \
                    and segs[2] == "forms-new":
                return self._forms_new(conn, user, _id(segs[1]))
            if len(segs) == 2 and segs[0] == "forms":
                return self._form_package(conn, user, _id(segs[1]))
            if len(segs) == 3 and segs[0] == "forms" \
                    and segs[2] == "review":
                return self._form_review(conn, user, _id(segs[1]))
            if len(segs) == 4 and segs[0] == "forms" \
                    and segs[2] == "download":
                return self._form_download(conn, _id(segs[1]),
                                           _id(segs[3]))
            if segs == ["calendar"]:
                return self._calendar(conn, user, query)
            if segs == ["calendar", "new"]:
                return self._event_new(conn, user, query)
            if segs == ["calendar", "new-appointment"]:
                return self._cal_new_appointment(conn, user)
            if segs == ["calendar", "new-deadline"]:
                return self._cal_new_deadline(conn, user)
            if len(segs) == 2 and segs[0] == "calendar":
                return self._event_detail(conn, user, _id(segs[1]))
        if method == "POST":
            if segs == ["contacts", "new"]:
                return self._contact_create(conn, now, uid)
            if segs == ["matters", "new"]:
                return self._matter_create(conn, now, uid)
            if len(segs) == 3 and segs[0] == "matters" \
                    and segs[2] == "forms-new":
                return self._forms_create(conn, now, uid, _id(segs[1]))
            if len(segs) == 3 and segs[0] == "forms" \
                    and segs[2] == "invite":
                return self._form_invite(conn, now, _id(segs[1]), user)
            if segs == ["calendar", "new"]:
                return self._event_create(conn, now, uid)
            if segs == ["calendar", "new-appointment"]:
                return self._cal_new_appointment_create(conn, now, uid)
            if segs == ["calendar", "new-deadline"]:
                return self._cal_new_deadline_create(conn, now, uid)
            if len(segs) == 3 and segs[0] == "calendar" \
                    and segs[2] == "attendees":
                return self._event_attendee_add(conn, _id(segs[1]))
            if segs == ["files", "upload"]:
                return self._file_upload(conn, now, uid)
            if len(segs) == 3 and segs[0] == "files" \
                    and segs[2] == "rename":
                return self._file_rename(conn, _id(segs[1]))
            if segs == ["tasks", "quick"]:
                return self._task_quick_create(conn, now, uid)
            if len(segs) == 3 and segs[0] == "tasks" \
                    and segs[2] == "complete":
                return self._task_complete(conn, now, _id(segs[1]))
            if len(segs) == 3 and segs[0] == "tasks" \
                    and segs[2] == "reopen":
                return self._task_reopen(conn, _id(segs[1]))
            if segs == ["settings", "task-lists"]:
                return self._task_list_create(conn)
            if len(segs) == 4 and segs[0] == "settings" \
                    and segs[1] == "task-lists" and segs[3] == "items":
                return self._task_list_item_create(conn, user,
                                                   _id(segs[2]))
            if len(segs) == 3 and segs[0] == "matters" \
                    and segs[2] == "import-task-list":
                return self._import_task_list(conn, now, uid,
                                              matter_id=_id(segs[1]))
            if len(segs) == 3 and segs[0] == "contacts" \
                    and segs[2] == "import-task-list":
                return self._import_task_list(conn, now, uid,
                                              contact_id=_id(segs[1]))
            if segs == ["notes", "quick"]:
                return self._note_quick_create(conn, now, uid)
            if segs == ["notes", "new"]:
                return self._note_full_create(conn, now, uid)
            if len(segs) == 3 and segs[0] == "notes" \
                    and segs[2] == "pin":
                return self._note_pin_toggle(conn, _id(segs[1]))
            if segs == ["settings", "note-categories"]:
                return self._note_category_create(conn)
        raise _NotFound()

    # --- first-run setup ---

    def _setup_page(self, conn, now, error=None):
        if reads.user_count(conn) > 0:
            return self._redirect("/login")
        body = (f"<div class='card narrow'><h1>Set up your firm's"
                f" first account</h1>{html.error_box(error)}"
                f"<p class='hint'>This system holds SYNTHETIC data only."
                f" You are creating the administrator.</p>"
                f"<form method='post' action='/setup'>"
                + html.field("Your name", "name", autofocus=True)
                + html.field("Email", "email", ftype="email")
                + html.field("Password", "password", ftype="password")
                + "<button class='primary'>Create account</button>"
                  "</form></div>")
        self._send_page(200, html.page("First-run setup", body))

    def _setup_post(self, conn, now):
        if reads.user_count(conn) > 0:
            return self._redirect("/login")
        form = self._form_body()
        name = form.get("name", "").strip()
        email = form.get("email", "").strip().lower()
        password = form.get("password", "")
        if not (name and email and password):
            return self._setup_page(conn, now, error="All fields are"
                                    " required.")
        uid = users.create_user(conn, email, name, now,
                                role_label="Administrator")
        auth.set_password(conn, uid, password)
        users.update_user(conn, uid, is_admin=1, is_owner=1)
        status, token = auth.login(conn, email, password, now)
        conn.commit()
        assert status == "enrollment_required", status
        return self._redirect("/enroll-mfa", cookies=[self._cookie(token)])

    # --- login ---

    def _login_page(self, conn, now, error=None):
        if reads.user_count(conn) == 0:
            return self._redirect("/setup")
        # gated item 5 (ruled IN 2026-08-10): a demo launcher that
        # serves synthetic dbs exclusively (billing-ui/serve.py) may
        # set demo_prefill on the server; the seeded credentials
        # render prefilled. Unset -- every other launcher -- renders
        # the plain form.
        pre = getattr(self.server, "demo_prefill", None)
        pre_email, pre_pw = pre if pre else ("", "")
        note = ("<p class='hint'>Demo database: the seeded"
                " credentials are filled in -- click Continue.</p>"
                if pre else "")
        body = (f"<div class='card narrow'><h1>Log in</h1>"
                f"{html.error_box(error)}"
                f"<form method='post' action='/login'>" + note
                + html.field("Email", "email", ftype="email",
                             value=pre_email, autofocus=True)
                + html.field("Password", "password", ftype="password",
                             value=pre_pw)
                + "<button class='primary'>Continue</button></form></div>")
        self._send_page(200, html.page("Log in", body))

    def _login_post(self, conn, now):
        form = self._form_body()
        status, token = auth.login(conn, form.get("email", "").strip().lower(),
                                   form.get("password", ""), now)
        conn.commit()
        if status in ("bad_credentials", "deactivated"):
            return self._login_page(conn, now, error="That email and"
                                    " password combination did not work.")
        target = ("/enroll-mfa" if status == "enrollment_required"
                  else "/mfa")
        return self._redirect(target, cookies=[self._cookie(token)])

    # --- MFA enrollment (first login) ---

    def _pending(self, conn):
        """Session row for the between-password-and-MFA states."""
        token = self._session_token()
        return reads.session_row(conn, token) if token else None

    def _enroll_page(self, conn, now):
        sess = self._pending(conn)
        if sess is None:
            return self._redirect("/login")
        if sess["twofa_method"] is not None:
            return self._redirect("/mfa")
        body = ("<div class='card narrow'><h1>Set up two-factor"
                " authentication</h1>"
                "<p>Your firm requires a second factor: a static"
                " 6-digit code at each login. Nothing to install,"
                " nothing expires. Your code appears on the next"
                " screen (in production it would arrive by email).</p>"
                "<form method='post' action='/enroll-mfa'>"
                "<button class='primary'>Show me my code</button>"
                "</form></div>")
        self._send_page(200, html.page("Two-factor setup", body))

    def _enroll_post(self, conn, now):
        """Enroll email-method 2FA (screen review 1 ruling: static
        per-login code, no authenticator app; TOTP killed for v1).
        enroll_twofa issues the first challenge immediately."""
        sess = self._pending(conn)
        if sess is None:
            return self._redirect("/login")
        auth.enroll_twofa(conn, sess["user_id"], "email",
                          sess["token"], now)
        conn.commit()
        return self._redirect("/mfa")

    # --- MFA verify (every login) ---

    def _mfa_page(self, conn, now, error=None):
        sess = self._pending(conn)
        if sess is None:
            return self._redirect("/login")
        if sess["twofa_method"] is None:
            return self._redirect("/enroll-mfa")
        mail = reads.latest_twofa_email(conn, sess["user_id"])
        code_lead = ""
        if mail is not None:
            m = re.search(r"(\d{6})", mail["body"])
            code = m.group(1) if m else ""
            code_lead = (f"<div class='mailbox'><h2>Your login code"
                         f"</h2><div class='code-display'>{code}</div>"
                         f"<p class='hint'>Synthetic environment: the"
                         f" code is shown here because this system"
                         f" sends no real email. In production this is"
                         f" the message in your inbox:"
                         f" {html.esc(mail['body'])}</p></div>")
        body = (f"<div class='card narrow'><h1>Enter your code</h1>"
                f"{html.error_box(error)}" + code_lead +
                f"<form method='post' action='/mfa'>"
                + html.field("Type the code above", "code",
                             autofocus=True)
                + "<button class='primary'>Verify</button></form>"
                  "</div>")
        self._send_page(200, html.page("Two-factor check", body))

    def _mfa_post(self, conn, now):
        sess = self._pending(conn)
        if sess is None:
            return self._redirect("/login")
        ok = auth.verify_twofa(conn, sess["token"], self._form_body()
                               .get("code", "").strip(), now)
        conn.commit()
        if not ok:
            return self._mfa_page(conn, now, error="That code did not"
                                  " verify. Type the code shown below"
                                  " and try again.")
        return self._redirect("/")

    # --- authenticated pages ---

    def _dashboard(self, conn, user):
        # item-12 design gate (status-page.md, ratified 2026-08-08):
        # the home screen is the firm status page; the old counts +
        # actions card survives as its Practice section.
        from app_ui import billing_ui
        return billing_ui.dashboard_screen(self, conn, user)

    def _not_found(self, user):
        body = ("<div class='card'><h1>Not found</h1>"
                "<p>No record lives at this address -- it may have been"
                " deleted, or the link is stale.</p>"
                "<p><a href='/'>Back to the dashboard</a></p></div>")
        self._send_page(404, html.page("Not found", body,
                                       user_name=user["name"]))

    # --- contacts (U1.1) ---

    def _contact_new(self, conn, user, error=None):
        body = (f"<div class='card narrow'><h1>New client</h1>"
                f"<p class='hint'>A person -- not a company.</p>"
                f"{html.error_box(error)}"
                f"<form method='post' action='/contacts/new'>"
                + html.field("Given name (first name)", "given_name",
                             autofocus=True)
                + html.field("Family name (last name)", "family_name",
                             required=False,
                             hint="The client can supply this later.")
                + html.field("Email", "email", ftype="email",
                             required=False,
                             hint="Needed to send the intake"
                                  " invitation.")
                + html.field("Phone", "phone", required=False)
                + "<button class='primary'>Create client</button>"
                  "</form></div>")
        self._send_page(200, html.page("New client", body,
                                       user_name=user["name"]))

    def _contact_create(self, conn, now, uid):
        f = self._form_body()
        cid = contacts.create_contact(
            conn, "person", now, uid,
            given_name=f.get("given_name") or None,
            family_name=f.get("family_name") or None,
            email=f.get("email") or None,
            phone=f.get("phone") or None)
        conn.commit()
        return self._redirect(f"/contacts/{cid}")

    def _contact_detail(self, conn, user, cid):
        row = reads.contact_row(conn, cid)
        if row is None:
            raise _NotFound()
        f = facts.facts_of(conn, "contact", cid)
        # human labels from fact_definitions (gate ruling 2026-08-10:
        # James authorized touching this frozen screen for labels +
        # date format only); a key with no definition renders raw --
        # a visible gap, never a blank
        labels = reads.fact_labels(conn)
        kv = "".join(
            f"<dt>{html.esc(labels.get(key) or key)}</dt>"
            f"<dd>{html.esc(str(val))}</dd>"
            for (key, idx), val in sorted(f.items())
            if key != "meta.synthetic")
        from app_ui.billing_ui import fmt_date
        mrows = [[html.link(f"/matters/{m['id']}", m["name"]),
                  html.esc(fmt_date(m["created_at"][:10]))]
                 for m in reads.contact_matters(conn, cid)]
        mtable = (html.table(["Matter", "Created"], mrows) if mrows
                  else "<p class='hint'>No matters yet.</p>")
        # Money band (billing-ui s11, item-12 object 3, placement A
        # signed): rendering only, assembled in billing_ui; empty
        # string until the client has any money story
        from app_ui import billing_ui
        money = billing_ui.client_money_band(conn, cid)
        body = (f"<div class='card'><h1>{html.esc(row['display_name'])}"
                f"</h1><div class='actions'>"
                f"<a href='/matters/new?contact={cid}'>New matter for"
                f" this client</a></div>"
                f"<dl class='kv'>{kv}</dl></div>"
                + money
                + f"<div class='card'><h1>Matters</h1>{mtable}</div>"
                + self._tasks_card(conn, "contacts", cid,
                                   f"/contacts/{cid}")
                + self._notes_card(conn, "contacts", cid,
                                   f"/contacts/{cid}")
                + self._files_card(conn, contact_id=cid,
                                   back=f"/contacts/{cid}"))
        self._send_page(200, html.page(row["display_name"], body,
                                       user_name=user["name"]))

    # --- matters (U1.2) ---

    def _matter_new(self, conn, user, query, error=None):
        pre = query.get("contact", [""])[0]
        contact_rows = reads.list_contacts(conn)
        if not contact_rows:
            body = ("<div class='card narrow'><h1>New matter</h1>"
                    "<p>A matter needs a client, and there"
                    " are no clients yet.</p>"
                    "<div class='actions'><a href='/contacts/new'>"
                    "Create the client first</a></div>"
                    "<p class='hint'>You will land back here in one"
                    " click from their page.</p></div>")
            return self._send_page(200, html.page("New matter", body,
                                                  user_name=user["name"]))
        opts = "".join(
            f"<option value='{c['id']}'"
            f"{' selected' if str(c['id']) == pre else ''}>"
            f"{html.esc(c['display_name'])}</option>"
            for c in contact_rows)
        body = (f"<div class='card narrow'><h1>New matter</h1>"
                f"{html.error_box(error)}"
                f"<form method='post' action='/matters/new'>"
                + html.field("Matter name", "name", autofocus=True)
                + f"<label>Client</label>"
                  f"<select name='contact_id' required>{opts}</select>"
                  f" <a class='hint' href='/contacts/new'>or create a"
                  f" new client</a>"
                + html.field("Description", "description",
                             required=False)
                + "<button class='primary'>Create matter</button>"
                  "</form></div>")
        self._send_page(200, html.page("New matter", body,
                                       user_name=user["name"]))

    def _matter_create(self, conn, now, uid):
        f = self._form_body()
        mid = matters.create_matter(
            conn, f["name"], int(f["contact_id"]), now, uid,
            description=f.get("description") or None, assignee_id=uid)
        conn.commit()
        return self._redirect(f"/matters/{mid}")

    def _matter_detail(self, conn, user, mid):
        row = reads.matter_row(conn, mid)
        if row is None:
            raise _NotFound()
        contact = reads.contact_row(conn, row["primary_contact_id"])
        # dates on this frozen screen go MM/DD/YYYY with the P2 tasks
        # section (goal.md date constraint; sibling-defect extension,
        # disclosed for the P2 gate re-rule)
        frows = [[html.link(f"/forms/{s['id']}", s["title"]),
                  html.mdy(s["created_at"])]
                 for s in reads.matter_smart_forms(conn, mid)]
        ftable = (html.table(["Form package", "Created"], frows) if frows
                  else "<p class='hint'>No form packages yet.</p>")
        erows = [[html.link(f"/calendar/{e['id']}", e["title"]),
                  html.mdy(e["starts_at"])
                  + ("" if e["starts_at"].endswith("T00:00:00Z")
                     else " " + e["starts_at"][11:16])]
                 for e in reads.matter_events(conn, mid)]
        etable = (html.table(["Deadline / event", "When"], erows)
                  if erows else "<p class='hint'>No deadlines yet.</p>")
        # flow markers (billing-ui s11, placement L2): one unbilled
        # line when this matter has time on no invoice -- rendering
        # only, the sum reuses billing_ui's integer rounding idiom
        from app_ui import billing_ui
        unb = [t for t in reads.unbilled_time_entries(conn)
               if t["matter_id"] == mid]
        unb_cents = sum(
            (t["duration_seconds"] * t["rate_cents_per_hour"] + 1800)
            // 3600 for t in unb if t["rate_cents_per_hour"])
        unb_line = ""
        if unb:
            figure = (billing_ui.fmt_cents(unb_cents) if unb_cents
                      else billing_ui.fmt_duration(
                          sum(t["duration_seconds"] for t in unb)))
            unb_line = (f"<p class='hint'>{figure} unbilled time on"
                        f" this matter -- "
                        + html.link("/billing/time", "Time") + "</p>")
        body = (f"<div class='card'><h1>{html.esc(row['name'])}</h1>"
                f"<dl class='kv'><dt>Client</dt><dd>"
                + html.link(f"/contacts/{contact['id']}",
                            contact["display_name"])
                + f"</dd><dt>Description</dt><dd>"
                  f"{html.esc(row['description'] or '-')}</dd></dl>"
                + unb_line
                + f"<div class='actions'>"
                f"<a href='/matters/{mid}/forms-new'>New form package"
                f"</a><a href='/calendar/new?matter={mid}&contact="
                f"{row['primary_contact_id']}'>New deadline</a></div>"
                f"</div>"
                + self._tasks_card(conn, "matters", mid,
                                   f"/matters/{mid}")
                + self._notes_card(conn, "matters", mid,
                                   f"/matters/{mid}")
                + self._files_card(conn, matter_id=mid,
                                   back=f"/matters/{mid}")
                + f"<div class='card'><h1>Form packages</h1>{ftable}"
                  f"</div>"
                  f"<div class='card'><h1>Deadlines</h1>{etable}</div>")
        self._send_page(200, html.page(row["name"], body,
                                       user_name=user["name"]))

    # --- form packages + invitations (U1.3) ---

    def _forms_new(self, conn, user, mid):
        matter = reads.matter_row(conn, mid)
        if matter is None:
            raise _NotFound()
        boxes = "".join(
            f"<label><input type='checkbox' name='form_code'"
            f" value='{r['code']}'"
            f"{' checked' if r['code'] == 'g-28' else ''}"
            f" style='width:auto'> {html.esc(r['code'].upper())} --"
            f" {html.esc(r['title'])}</label>"
            for r in forms.library(conn))
        body = (f"<div class='card narrow'><h1>New form package for"
                f" {html.esc(matter['name'])}</h1>"
                f"<form method='post' action='/matters/{mid}/forms-new'>"
                + html.field("Package title", "title",
                             value=f"{matter['name']} forms",
                             autofocus=True)
                + f"<label>Forms</label>{boxes}"
                + "<button class='primary'>Create package</button>"
                  "</form></div>")
        self._send_page(200, html.page("New form package", body,
                                       user_name=user["name"]))

    def _forms_create(self, conn, now, uid, mid):
        matter = reads.matter_row(conn, mid)
        if matter is None:
            raise _NotFound()
        f = self._form_body_multi()
        codes = f.get("form_code", [])
        title = f.get("title", ["Forms"])[0]
        sfid = forms.create_smart_form(
            conn, title, now, uid,
            contact_id=matter["primary_contact_id"], matter_id=mid,
            form_codes=codes or ["g-28"])
        conn.commit()
        return self._redirect(f"/forms/{sfid}")

    def _form_package(self, conn, user, sfid, error=None):
        sf = reads.smart_form_row(conn, sfid)
        if sf is None:
            raise _NotFound()
        frows = [[html.esc(r["form_code"].upper()),
                  html.link(f"/forms/{sfid}/download/{r['id']}",
                            "Download filled PDF")]
                 for r in forms.forms_of(conn, sfid)]
        invs = reads.invitations_of(conn, sfid)
        irows = []
        for inv in invs:
            link = f"{self.server.client_base}/intake/{inv['token']}"
            status = html.esc(inv["status"])
            irows.append([
                f"<span class='pill {status}'>{status}</span>",
                html.esc((inv["status_at"] or "")[:16].replace("T", " ")),
                f"<code class='copy'>{link}</code>"])
        itable = (html.table(["Status", "When", "Client link"], irows)
                  if irows else "<p class='hint'>Not sent yet.</p>")
        body = (f"<div class='card'><h1>{html.esc(sf['title'])}</h1>"
                f"{html.error_box(error)}"
                f"<div class='actions'>"
                f"<a class='quiet' href='/matters/{sf['matter_id']}'>"
                f"Back to matter</a>"
                f"<a href='/forms/{sfid}/review'>Review answers</a>"
                f"</div>"
                + html.table(["Form", ""], frows)
                + f"</div><div class='card'><h1>Client intake</h1>"
                  f"<form method='post' action='/forms/{sfid}/invite'>"
                  f"<button class='primary'>Send intake invitation"
                  f" (email)</button></form>{itable}</div>")
        self._send_page(200, html.page(sf["title"], body,
                                       user_name=user["name"]))

    def _form_invite(self, conn, now, sfid, user):
        sf = reads.smart_form_row(conn, sfid)
        if sf is None:
            raise _NotFound()
        try:
            invitations.invite(conn, sfid, sf["contact_id"], "email", now)
            conn.commit()
        except ValueError as e:
            return self._form_package(conn, user, sfid, error=str(e))
        return self._redirect(f"/forms/{sfid}")

    def _form_review(self, conn, user, sfid):
        sf = reads.smart_form_row(conn, sfid)
        if sf is None:
            raise _NotFound()
        seen = set()
        sections = {}
        for sff in forms.forms_of(conn, sfid):
            schema = forms.schema_of(conn, sff["form_edition_id"])
            for q in schema["questions"]:
                if q["key"] in seen:
                    continue
                seen.add(q["key"])
                source = q.get("source") or {}
                if "preparer" in source or "firm" in source:
                    continue  # auto-populated, not client answers
                if "fact" in source:
                    spec = source["fact"]
                    cid = forms.role_contact(conn, sfid, spec["role"])
                    val = facts.get_fact(conn, spec["subject"], cid,
                                         spec["key"]) if cid else None
                else:
                    val = render.get_answer(conn, sfid, q["key"])
                sections.setdefault(q["tab"], []).append(
                    (q["label"], val))
        parts = []
        for tab, items in sections.items():
            rows = [[html.esc(label),
                     html.esc(val) if val is not None
                     else "<span class='hint'>-</span>"]
                    for label, val in items]
            parts.append(f"<div class='card'><h1>{html.esc(tab)}</h1>"
                         + html.table(["Question", "Answer"], rows)
                         + "</div>")
        body = (f"<div class='card'><h1>Answers --"
                f" {html.esc(sf['title'])}</h1><div class='actions'>"
                f"<a class='quiet' href='/forms/{sfid}'>Back to"
                f" package</a></div></div>" + "".join(parts))
        self._send_page(200, html.page("Review answers", body,
                                       user_name=user["name"]))

    def _form_download(self, conn, sfid, sff_id):
        sff = next((r for r in forms.forms_of(conn, sfid)
                    if r["id"] == sff_id), None)
        if sff is None:
            raise _NotFound()
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "form.pdf"
            render.render_form(conn, sff_id, out)
            content = out.read_bytes()
        self._send_file(content, f"{sff['form_code']}.pdf")

    # --- calendar + deadlines (U1.6; unified view rebuilt by
    # casework-tabs P1 under the 2026-08-10 program amendment:
    # kind is DERIVED presentation, never stored; SQL in reads.py;
    # writes ride casework modules) ---

    CAL_KINDS = ("appointment", "deadline", "expiry", "task", "vmax",
                 "invoice")

    @staticmethod
    def _event_kind(e):
        """expiry = the auto events facts generate; deadline = the
        all-day shape New deadline writes (T00:00:00Z, no end);
        everything else is a timed appointment."""
        if e["source"] == "expiry_auto":
            return "expiry"
        if e["starts_at"].endswith("T00:00:00Z") and not e["ends_at"]:
            return "deadline"
        return "appointment"

    def _cal_rows(self, conn):
        """The unified date view (Appendix A): six kinds assembled
        from their own readers into one dated list."""
        def linked(cid, cname, mid, mname, prefix=""):
            # matter-first, one link only: the matter name already
            # names the client, and two wrapped links per row was
            # the crowding James flagged at the P1 gate
            if mid:
                part = html.link(f"/matters/{mid}", mname or "matter")
            elif cid:
                part = html.link(f"/contacts/{cid}",
                                 cname or "client")
            else:
                return "-"
            return f"<span class='provenance'>{prefix}{part}</span>"

        items = []
        for e in reads.calendar_events(conn):
            kind = self._event_kind(e)
            date = e["starts_at"][:10]
            time_range = ""
            if kind == "appointment":
                time_range = e["starts_at"][11:16]
                if e["ends_at"]:
                    time_range += "-" + e["ends_at"][11:16]
            prefix = "from " if kind == "expiry" else ""
            items.append({
                "kind": kind, "date": date, "time": time_range,
                "title": e["title"], "href": f"/calendar/{e['id']}",
                "linked": linked(e["contact_id"], e["contact_name"],
                                 e["matter_id"], e["matter_name"],
                                 prefix)})
        for v in reads.calendar_vmax(conn):
            items.append({
                "kind": "vmax", "date": v["due_on"], "time": "",
                "title": f"VMAX date -- {v['contact_name']}",
                "href": f"/contacts/{v['contact_id']}",
                "linked": linked(v["contact_id"], v["contact_name"],
                                 None, None, "from ")})
        for t in reads.calendar_task_dues(conn):
            items.append({
                "kind": "task", "date": t["due_date"], "time": "",
                "title": t["title"], "href": f"/tasks/{t['id']}",
                "linked": linked(t["contact_id"], t["contact_name"],
                                 t["matter_id"], t["matter_name"])})
        for i in reads.calendar_invoice_dues(conn):
            if billing.invoice_status(conn, i["id"]) == "paid":
                continue  # a paid bill's due date is history, not
                # a calendar obligation ([Q] gate ruling pending)
            items.append({
                "kind": "invoice", "date": i["due_date"], "time": "",
                "title": f"{i['display_code']} due",
                "href": f"/billing/invoices/{i['id']}",
                "linked": linked(i["contact_id"], i["contact_name"],
                                 None, None)})
        items.sort(key=lambda r: (r["date"], r["time"], r["title"]))
        return items

    def _calendar(self, conn, user, query):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        stored = cookie.get("cal_view")
        view = query.get("view", [None])[0]
        cookies = None
        if view in ("agenda", "month"):
            cookies = [f"cal_view={view}; Path=/"]
        else:
            view = ("month" if stored is not None
                    and stored.value == "month" else "agenda")
        kind = query.get("kind", [None])[0]
        if kind not in self.CAL_KINDS:
            kind = None
        items = self._cal_rows(conn)
        shown = ([r for r in items if r["kind"] == kind]
                 if kind else items)
        kindq = f"&kind={kind}" if kind else ""
        actions = ("<div class='actions'>"
                   "<a href='/calendar/new-appointment'>New"
                   " appointment</a>"
                   "<a class='quiet' href='/calendar/new-deadline'>"
                   "New deadline</a></div>")
        toggle = (f"<div class='chips'>"
                  f"<a class='chip{' on' if view == 'agenda' else ''}'"
                  f" href='/calendar?view=agenda{kindq}'>Agenda</a>"
                  f"<a class='chip{' on' if view == 'month' else ''}'"
                  f" href='/calendar?view=month{kindq}'>Month</a>"
                  f"</div>")
        chips = ("<div class='chips'>"
                 + f"<a class='chip{' on' if kind is None else ''}'"
                   f" href='/calendar'>all</a>"
                 + "".join(
                     f"<a class='chip{' on' if kind == k else ''}'"
                     f" href='/calendar?kind={k}'>{k}</a>"
                     for k in self.CAL_KINDS)
                 + "</div>")
        if view == "month":
            inner = self._cal_month(query, shown)
        elif shown:
            # date and time stack deliberately: the date line stays
            # one line, the time rides under it muted (P1 gate
            # feedback: the mid-range wrap read as clutter)
            rows = [[f"<span class='nowrap'>{html.mdy(r['date'])}"
                     f"</span>"
                     + (f"<br><span class='hint nowrap'>{r['time']}"
                        f"</span>" if r["time"] else ""),
                     f"<span class='kind kind-{r['kind']}'>"
                     f"{r['kind']}</span>",
                     html.link(r["href"], r["title"]), r["linked"]]
                    for r in shown]
            inner = ("<div class='agenda'>"
                     + html.table(["When", "Kind", "Item", "Linked"],
                                  rows)
                     + "</div>")
        else:
            inner = html.designed_empty(
                "Nothing scheduled yet. Appointments, deadlines,"
                " expirations, task due dates, VMAX clocks, and"
                " invoice due dates all land on this one calendar.",
                "<a href='/calendar/new-appointment'>New"
                " appointment</a>"
                "<a class='quiet' href='/calendar/new-deadline'>New"
                " deadline</a>")
        body = (f"<div class='card'><h1>Calendar</h1>{actions}"
                f"{toggle}{chips}{inner}</div>")
        self._send_page(200, html.page("Calendar", body,
                                       user_name=user["name"],
                                       active_href="/calendar",
                                       wide=(view == "month")),
                        cookies=cookies)

    def _cal_month(self, query, shown):
        """Month grid over the same unified rows. Earlier/Later jump
        to the nearest month that HAS items -- no empty scrolling,
        and the link chain stays finite for the walk's BFS."""
        month = query.get("month", [None])[0] or ""
        if not re.fullmatch(r"\d{4}-\d{2}", month or "") \
                or not 1 <= int(month[5:7]) <= 12:
            month = datetime.now(timezone.utc).strftime("%Y-%m")
        year, mon = int(month[:4]), int(month[5:7])
        by_date = {}
        for r in shown:
            by_date.setdefault(r["date"], []).append(r)
        months_with = sorted({r["date"][:7] for r in shown})
        earlier = [m for m in months_with if m < month]
        later = [m for m in months_with if m > month]

        def label(m):
            return f"{pycal.month_name[int(m[5:7])]} {m[:4]}"

        nav = ""
        if earlier:
            nav += (f"<a class='chip' href='/calendar?view=month"
                    f"&month={earlier[-1]}'>Earlier:"
                    f" {label(earlier[-1])}</a>")
        if later:
            nav += (f"<a class='chip' href='/calendar?view=month"
                    f"&month={later[0]}'>Later: {label(later[0])}</a>")
        nav = f"<div class='chips'>{nav}</div>" if nav else ""
        head = "".join(f"<th>{d}</th>" for d in
                       ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri",
                        "Sat"))
        weeks = pycal.Calendar(firstweekday=6).monthdayscalendar(
            year, mon)
        rows = ""
        for week in weeks:
            cells = ""
            for day in week:
                if day == 0:
                    cells += "<td></td>"
                    continue
                date = f"{year:04d}-{mon:02d}-{day:02d}"
                # full title in the markup; the CELL clips it with a
                # real ellipsis (Outlook-style one-liners, P1 gate
                # feedback r2) and hover carries the details
                entries = "".join(
                    f"<a href='{r['href']}' title='{html.esc(r['title'])}"
                    f"{' ' + r['time'] if r['time'] else ''}'>"
                    f"<span class='dot kind-{r['kind']}'></span>"
                    f"{html.esc(r['title'])}</a>"
                    for r in by_date.get(date, []))
                cells += (f"<td><span class='day'>{day}</span>"
                          f"{entries}</td>")
            rows += f"<tr>{cells}</tr>"
        key = ("<p class='hint legend'>Key: " + "".join(
            f"<span class='item'><span class='dot kind-{k}'></span>"
            f"{k}</span>" for k in self.CAL_KINDS) + "</p>")
        return (f"<h1>{pycal.month_name[mon]} {year}</h1>{nav}"
                f"<table class='data month-grid'><thead><tr>{head}"
                f"</tr></thead><tbody>{rows}</tbody></table>{key}")

    def _event_new(self, conn, user, query):
        mid = query.get("matter", [""])[0]
        cid = query.get("contact", [""])[0]
        opts = "".join(
            f"<option value='{m['id']}'"
            f"{' selected' if str(m['id']) == mid else ''}>"
            f"{html.esc(m['name'])} -- {html.esc(m['display_name'])}"
            f"</option>"
            for m in reads.list_matters(conn))
        body = (f"<div class='card narrow'><h1>New deadline</h1>"
                f"<form method='post' action='/calendar/new'>"
                f"<input type='hidden' name='contact_id' value='{cid}'>"
                f"<label>Matter</label>"
                f"<select name='matter_id'>{opts}"
                f"<option value=''>-- no matter --</option></select>"
                f"<p class='hint'>A deadline on a matter shows up on"
                f" that matter's screen.</p>"
                + html.field("Title", "title", autofocus=True)
                + html.field("Date", "date", ftype="date")
                + html.field("Time (UTC)", "time", ftype="time",
                             value="09:00")
                + f"<label>Email reminder before</label>"
                  f"<select name='reminder'>"
                  f"<option value='2|days' selected>2 days</option>"
                  f"<option value='7|days'>7 days</option>"
                  f"<option value='1|days'>1 day</option>"
                  f"<option value='1|hours'>1 hour</option>"
                  f"<option value=''>No reminder</option></select>"
                + "<button class='primary'>Create deadline</button>"
                  "</form></div>")
        self._send_page(200, html.page("New deadline", body,
                                       user_name=user["name"]))

    def _event_create(self, conn, now, uid):
        f = self._form_body()
        starts = f"{f['date']}T{f.get('time') or '09:00'}:00Z"
        matter_id = int(f["matter_id"]) if f.get("matter_id") else None
        if matter_id is not None:
            matter = reads.matter_row(conn, matter_id)
            contact_id = matter["primary_contact_id"] if matter else None
        else:
            contact_id = (int(f["contact_id"]) if f.get("contact_id")
                          else None)
        eid = events.create_event(
            conn, f["title"], starts, now, uid,
            contact_id=contact_id, matter_id=matter_id)
        events.add_attendee(conn, eid, user_id=uid)
        rem = f.get("reminder", "")
        if rem:
            value, unit = rem.split("|")
            events.add_reminder(conn, eid, int(value), unit)
        conn.commit()
        return self._redirect(f"/calendar/{eid}")

    def _event_detail(self, conn, user, eid):
        e = reads.event_row(conn, eid)
        if e is None:
            raise _NotFound()
        kind = self._event_kind(e)
        when = html.mdy(e["starts_at"])
        if kind == "appointment":
            when += " " + e["starts_at"][11:16]
            if e["ends_at"]:
                when += "-" + e["ends_at"][11:16]
            when += " UTC"
        desc = (f"<p>{html.esc(e['description'])}</p>"
                if e["description"] else "")
        rem = reads.event_reminders(conn, eid)
        rrows = [[f"{r['offset_value']} {r['offset_unit']} before",
                  html.esc(r["channel"])] for r in rem]
        rtable = (html.table(["Reminder", "Channel"], rrows) if rrows
                  else "<p class='hint'>No reminders.</p>")
        att = reads.event_attendees(conn, eid)
        arows = [[html.esc(a["user_name"] or a["contact_name"]
                           or "-"),
                  "staff" if a["user_id"] else "client"]
                 for a in att]
        atable = (html.table(["Attendee", "Who"], arows) if arows
                  else "<p class='hint'>No attendees yet.</p>")
        have_u = {a["user_id"] for a in att if a["user_id"]}
        have_c = {a["contact_id"] for a in att if a["contact_id"]}
        opts = "".join(
            f"<option value='user-{u['id']}'>{html.esc(u['name'])}"
            f" (staff)</option>"
            for u in reads.list_users(conn)
            if not u["deactivated_at"] and u["id"] not in have_u)
        if e["contact_id"] and e["contact_id"] not in have_c:
            c = reads.contact_row(conn, e["contact_id"])
            if c is not None:
                opts += (f"<option value='contact-{c['id']}'>"
                         f"{html.esc(c['display_name'])} (client)"
                         f"</option>")
        aform = ""
        if opts:
            aform = (f"<form method='post' action='/calendar/{eid}"
                     f"/attendees'><label>Add attendee</label>"
                     f"<select name='attendee'>{opts}</select>"
                     f"<button class='primary'>Add attendee</button>"
                     f"</form>")
        links = ""
        if e["matter_id"]:
            links += html.link(f"/matters/{e['matter_id']}",
                               "Matter") + " "
        if e["contact_id"]:
            links += html.link(f"/contacts/{e['contact_id']}",
                               "Client")
        body = (f"<div class='card tab-detail'>"
                f"<h1>{html.esc(e['title'])}</h1>"
                f"<p><span class='kind kind-{kind}'>{kind}</span></p>"
                f"{desc}"
                f"<dl class='kv'><dt>When</dt><dd>{when}</dd>"
                f"<dt>Linked</dt><dd>{links or '-'}</dd></dl>"
                f"<h2>Attendees</h2>{atable}{aform}"
                f"<h2>Reminders</h2>{rtable}"
                f"<div class='actions'><a class='quiet' href='/calendar'>"
                f"Back to calendar</a></div></div>")
        self._send_page(200, html.page(e["title"], body,
                                       user_name=user["name"],
                                       active_href="/calendar"))

    def _cal_new_appointment(self, conn, user):
        mopts = "".join(
            f"<option value='{m['id']}'>{html.esc(m['name'])} --"
            f" {html.esc(m['display_name'])}</option>"
            for m in reads.list_matters(conn))
        copts = "".join(
            f"<option value='{c['id']}'>"
            f"{html.esc(c['display_name'])}</option>"
            for c in reads.list_contacts(conn))
        body = (f"<div class='card narrow'><h1>New appointment</h1>"
                f"<form method='post' action='/calendar/"
                f"new-appointment'>"
                + html.field("Title", "title", autofocus=True)
                + html.field("Date", "date", ftype="date")
                + html.field("Start time (UTC)", "start_time",
                             ftype="time", value="09:00")
                + html.field("End time (UTC)", "end_time",
                             ftype="time", value="10:00",
                             required=False)
                + html.field("Description", "description",
                             required=False)
                + f"<label>Matter</label><select name='matter_id'>"
                  f"<option value=''>-- no matter --</option>{mopts}"
                  f"</select>"
                + f"<label>Client</label><select name='contact_id'>"
                  f"<option value=''>-- no client --</option>{copts}"
                  f"</select>"
                + "<p class='hint'>Attendees are added on the"
                  " appointment after it is created; firm default"
                  " reminders apply.</p>"
                + "<button class='primary'>Create appointment"
                  "</button></form></div>")
        self._send_page(200, html.page("New appointment", body,
                                       user_name=user["name"],
                                       active_href="/calendar"))

    def _cal_new_appointment_create(self, conn, now, uid):
        f = self._form_body()
        starts = f"{f['date']}T{f.get('start_time') or '09:00'}:00Z"
        ends = (f"{f['date']}T{f['end_time']}:00Z"
                if f.get("end_time") else None)
        matter_id = int(f["matter_id"]) if f.get("matter_id") else None
        contact_id = (int(f["contact_id"]) if f.get("contact_id")
                      else None)
        if matter_id is not None and contact_id is None:
            matter = reads.matter_row(conn, matter_id)
            contact_id = (matter["primary_contact_id"] if matter
                          else None)
        eid = events.create_event(
            conn, f["title"], starts, now, uid,
            description=f.get("description") or None, ends_at=ends,
            contact_id=contact_id, matter_id=matter_id)
        events.add_attendee(conn, eid, user_id=uid)
        conn.commit()
        return self._redirect(f"/calendar/{eid}")

    def _cal_new_deadline(self, conn, user):
        mopts = "".join(
            f"<option value='{m['id']}'>{html.esc(m['name'])} --"
            f" {html.esc(m['display_name'])}</option>"
            for m in reads.list_matters(conn))
        copts = "".join(
            f"<option value='{c['id']}'>"
            f"{html.esc(c['display_name'])}</option>"
            for c in reads.list_contacts(conn))
        body = (f"<div class='card narrow'><h1>New deadline</h1>"
                f"<form method='post' action='/calendar/new-deadline'>"
                + html.field("Title", "title", autofocus=True)
                + html.field("Date", "date", ftype="date")
                + f"<label>Matter</label><select name='matter_id'>"
                  f"<option value=''>-- no matter --</option>{mopts}"
                  f"</select>"
                + f"<label>Client</label><select name='contact_id'>"
                  f"<option value=''>-- no client --</option>{copts}"
                  f"</select>"
                + "<p class='hint'>A deadline is all-day: it lands"
                  " on the calendar and its matter, and firm default"
                  " reminders apply.</p>"
                + "<button class='primary'>Create deadline</button>"
                  "</form></div>")
        self._send_page(200, html.page("New deadline", body,
                                       user_name=user["name"],
                                       active_href="/calendar"))

    def _cal_new_deadline_create(self, conn, now, uid):
        f = self._form_body()
        matter_id = int(f["matter_id"]) if f.get("matter_id") else None
        contact_id = (int(f["contact_id"]) if f.get("contact_id")
                      else None)
        if matter_id is not None and contact_id is None:
            matter = reads.matter_row(conn, matter_id)
            contact_id = (matter["primary_contact_id"] if matter
                          else None)
        # the deadline shape: T00:00:00Z, no end -- scheduler-safe
        # all-day semantics (kind derives from this, see _event_kind)
        events.create_event(
            conn, f["title"], f"{f['date']}T00:00:00Z", now, uid,
            contact_id=contact_id, matter_id=matter_id)
        conn.commit()
        return self._redirect("/calendar")

    def _event_attendee_add(self, conn, eid):
        e = reads.event_row(conn, eid)
        if e is None:
            raise _NotFound()
        who = self._form_body().get("attendee", "")
        prefix, _, ident = who.partition("-")
        if prefix == "user" and ident.isdigit():
            events.add_attendee(conn, eid, user_id=int(ident))
        elif prefix == "contact" and ident.isdigit():
            events.add_attendee(conn, eid, contact_id=int(ident))
        conn.commit()
        return self._redirect(f"/calendar/{eid}")

    # --- browse surfaces (U2.1 indexes / U2.2 details) ---

    def _contacts_index(self, conn, user):
        rows = [[html.link(f"/contacts/{c['id']}", c["display_name"]),
                 f"<span class='pill'>{html.esc(c['kind'])}</span>",
                 html.esc(c["created_at"][:10])]
                for c in reads.list_contacts(conn)]
        inner = (html.table(["Client", "Kind", "Created"], rows)
                 if rows else html.empty_state(
                     "No clients yet. Every client relationship"
                     " starts with one."))
        body = (f"<div class='card'><h1>Clients</h1>"
                f"<div class='actions'><a href='/contacts/new'>New"
                f" client</a></div>{inner}</div>")
        self._send_page(200, html.page("Clients", body,
                                       user_name=user["name"]))

    def _matters_index(self, conn, user):
        rows = [[html.link(f"/matters/{m['id']}", m["name"]),
                 html.link(f"/contacts/{m['contact_id']}",
                           m["display_name"]),
                 html.esc(m["created_at"][:10])]
                for m in reads.list_matters(conn)]
        inner = (html.table(["Matter", "Client", "Created"],
                            rows)
                 if rows else html.empty_state(
                     "No matters yet. A matter is the case file --"
                     " forms, deadlines, and files hang off it."))
        body = (f"<div class='card'><h1>Matters</h1>"
                f"<div class='actions'><a href='/matters/new'>New"
                f" matter</a></div>{inner}</div>")
        self._send_page(200, html.page("Matters", body,
                                       user_name=user["name"]))

    def _linked_cell(self, conn, matter_id, contact_id, mnames, cnames):
        parts = []
        if matter_id:
            parts.append(html.link(f"/matters/{matter_id}",
                                   mnames.get(matter_id, "matter")))
        if contact_id:
            parts.append(html.link(f"/contacts/{contact_id}",
                                   cnames.get(contact_id, "client")))
        return " ".join(parts) or "<span class='hint'>-</span>"

    def _name_maps(self, conn):
        mnames = {m["id"]: m["name"] for m in reads.list_matters(conn)}
        cnames = {c["id"]: c["display_name"]
                  for c in reads.list_contacts(conn)}
        return mnames, cnames

    # --- files tab (rebuilt by casework-tabs P4a under the
    # 2026-08-10 program amendment: upload + custody, matter-centric
    # sections, firm index with filters, rename/preview/print/bulk.
    # Writes go through app.files only; the source filter is applied
    # over the core reader's rows in Python (files.list_files has no
    # source arg -- rendering-only, no new SQL) ---

    def _upload_form(self, mnames=None, cnames=None, matter_id=None,
                     contact_id=None, back=None):
        """The one upload control: selects on the firm index, hidden
        scope fields on matter/contact sections."""
        inner = ""
        if mnames is not None:
            mopts = "".join(
                f"<option value='{i}'>{html.esc(n)}</option>"
                for i, n in sorted(mnames.items(),
                                   key=lambda kv: kv[1]))
            copts = "".join(
                f"<option value='{i}'>{html.esc(n)}</option>"
                for i, n in sorted(cnames.items(),
                                   key=lambda kv: kv[1]))
            inner = (f"<div><label>Matter (optional)</label>"
                     f"<select name='matter_id'>"
                     f"<option value=''></option>{mopts}</select>"
                     f"</div><div><label>Client (optional)</label>"
                     f"<select name='contact_id'>"
                     f"<option value=''></option>{copts}</select>"
                     f"</div>")
        if matter_id is not None:
            inner += (f"<input type='hidden' name='matter_id'"
                      f" value='{matter_id}'>")
        if contact_id is not None:
            inner += (f"<input type='hidden' name='contact_id'"
                      f" value='{contact_id}'>")
        if back:
            inner += (f"<input type='hidden' name='back'"
                      f" value='{back}'>")
        return ("<form method='post' action='/files/upload'"
                " enctype='multipart/form-data' class='upload-row'>"
                "<div class='grow'><label>Upload a file</label>"
                "<input type='file' name='file' required></div>"
                + inner
                + "<button class='primary'>Upload</button></form>")

    def _files_index(self, conn, user, query):
        mnames, cnames = self._name_maps(conn)
        args = {}
        for key in ("matter_id", "contact_id"):
            v = query.get(key, [""])[0]
            if v:
                args[key] = _id(v)
        esign_q = query.get("esign_status", [""])[0]
        if esign_q:
            args["esign_status"] = esign_q
        source_q = query.get("source", [""])[0]
        rows_db = files.list_files(conn, **args)
        if source_q:
            rows_db = [f for f in rows_db
                       if f["source"] == source_q]
        filtered = bool(args or source_q)
        rows = []
        for f in rows_db:
            up = f["uploaded_at"] or ""
            rows.append([
                f"<input type='checkbox' name='file_id'"
                f" value='{f['id']}' form='bulk-download'>",
                html.link(f"/files/{f['id']}", f["name"]),
                self._linked_cell(conn, f["matter_id"],
                                  f["contact_id"], mnames, cnames),
                html.esc(f["source"]),
                html.esc(f["esign_status"] or "-"),
                html.esc(_fmt_size(f["size_bytes"])),
                html.esc(html.mdy(up)) if up else "-"])

        def sel(name, label, options, current):
            opts = "<option value=''>all</option>" + "".join(
                f"<option value='{v}'"
                f"{' selected' if str(v) == current else ''}>"
                f"{html.esc(str(t))}</option>" for v, t in options)
            return (f"<div><label>{html.esc(label)}</label>"
                    f"<select name='{name}'>{opts}</select></div>")

        filters = ""
        if rows or filtered:
            filters = (
                "<form method='get' action='/files'"
                " class='filter-row'>"
                + sel("matter_id", "Matter",
                      sorted(mnames.items(), key=lambda kv: kv[1]),
                      query.get("matter_id", [""])[0])
                + sel("contact_id", "Client",
                      sorted(cnames.items(), key=lambda kv: kv[1]),
                      query.get("contact_id", [""])[0])
                + sel("source", "Source",
                      [(s, s) for s in ("firm", "client",
                                        "produced")], source_q)
                + sel("esign_status", "e-sign",
                      [(s, s) for s in ("draft", "requested",
                                        "completed")], esign_q)
                + "<button class='small'>Filter</button>"
                  "</form>")
        upload = self._upload_form(mnames=mnames, cnames=cnames)
        if rows:
            bulk = ("<form id='bulk-download' method='get'"
                    " action='/files/bulk-download'>"
                    "<button class='small'>Download selected (zip)"
                    "</button></form>")
            inner = ("<div class='files-table'>"
                     + html.table(["", "File", "Linked to", "Source",
                                   "e-sign", "Size", "Uploaded"],
                                  rows)
                     + bulk + "</div>")
            body = (f"<div class='card'><h1>Files</h1>{upload}"
                    f"{filters}{inner}</div>")
        elif filtered:
            inner = html.empty_state("No files match these filters.")
            body = (f"<div class='card'><h1>Files</h1>{upload}"
                    f"{filters}{inner}</div>")
        else:
            inner = html.designed_empty(
                "No files yet. Uploads land here with their custody"
                " record (source + SHA-256); filled PDFs join them"
                " when a form package is produced.", upload)
            body = f"<div class='card'><h1>Files</h1>{inner}</div>"
        self._send_page(200, html.page("Files", body,
                                       user_name=user["name"],
                                       active_href="/files"))

    def _files_card(self, conn, matter_id=None, contact_id=None,
                    back="/"):
        """Files section for matter/contact pages (matter-centric
        ruling): the scope's files with in-place upload."""
        rows = []
        for f in files.list_files(conn, contact_id=contact_id,
                                  matter_id=matter_id):
            up = f["uploaded_at"] or ""
            rows.append([html.link(f"/files/{f['id']}", f["name"]),
                         html.esc(f["source"]),
                         html.esc(_fmt_size(f["size_bytes"])),
                         html.esc(html.mdy(up)) if up else "-"])
        form = self._upload_form(matter_id=matter_id,
                                 contact_id=contact_id, back=back)
        inner = ("<div class='files-table'>"
                 + html.table(["File", "Source", "Size", "Uploaded"],
                              rows) + "</div>"
                 if rows else
                 "<p class='hint'>No files here yet. Uploads keep"
                 " their custody record (source + SHA-256).</p>")
        return (f"<div class='card files-section'><h1>Files</h1>"
                f"{form}{inner}</div>")

    def _file_detail(self, conn, user, fid):
        try:
            f = files.get_file(conn, fid)
        except ValueError:
            raise _NotFound() from None
        mnames, cnames = self._name_maps(conn)
        linked = self._linked_cell(conn, f["matter_id"], f["contact_id"],
                                   mnames, cnames)
        up = f["uploaded_at"] or ""
        when = f"{html.mdy(up)} {up[11:16]}" if up else "-"
        ext = ("." + f["name"].rsplit(".", 1)[-1].lower()
               if "." in f["name"] else "")
        view_links = ""
        if ext in files.PREVIEW_TYPES:
            view_links = (f"<a href='/files/{fid}/preview'>Preview"
                          f"</a><a href='/files/{fid}/print'>Print"
                          f" view</a>")
        rename = (f"<form method='post' action='/files/{fid}/rename'"
                  f" class='upload-row'><div class='grow'>"
                  + html.field("Rename", "name", value=f["name"])
                  + "</div><button class='small'>Rename</button>"
                    "</form>")
        body = (f"<div class='card tab-detail'>"
                f"<h1>{html.esc(f['name'])}</h1>"
                f"<dl class='kv'>"
                f"<dt>Size</dt><dd>{html.esc(_fmt_size(f['size_bytes']))}"
                f"</dd><dt>Type</dt><dd>{html.esc(f['content_type'] or '-')}"
                f"</dd><dt>Source</dt><dd>{html.esc(f['source'] or '-')}"
                f"</dd><dt>SHA-256</dt><dd><code class='copy'>"
                f"{html.esc(f['sha256'])}</code>"
                f"</dd><dt>Linked</dt><dd>{linked}</dd>"
                f"<dt>Uploaded</dt><dd>{html.esc(when)}</dd></dl>"
                f"<div class='actions'>"
                f"<a href='/files/{fid}/download'>Download</a>"
                f"{view_links}"
                f"<a class='quiet' href='/files'>Back to files</a>"
                f"</div>{rename}</div>")
        self._send_page(200, html.page(f["name"], body,
                                       user_name=user["name"],
                                       active_href="/files"))

    def _file_upload(self, conn, now, uid):
        fields, uploads = self._multipart_body()
        up = uploads.get("file")
        if up is None or not up[0]:
            return self._redirect("/files")
        filename, content = up

        def opt(key):
            v = fields.get(key) or ""
            return int(v) if v else None

        fid = files.upload_file(
            conn, filename, content or b"", now,
            self.server.storage_dir,
            contact_id=opt("contact_id"), matter_id=opt("matter_id"),
            user_id=uid)
        conn.commit()
        back = fields.get("back") or ""
        return self._redirect(back if back.startswith("/")
                              else f"/files/{fid}")

    def _file_rename(self, conn, fid):
        try:
            files.get_file(conn, fid)
        except ValueError:
            raise _NotFound() from None
        name = self._form_body().get("name", "").strip()
        if name:
            files.rename(conn, "file", fid, name)
            conn.commit()
        return self._redirect(f"/files/{fid}")

    def _file_preview(self, conn, fid):
        try:
            ctype, content = files.preview(conn, fid)
        except (ValueError, OSError):
            raise _NotFound() from None
        self._send_inline(content, ctype)

    def _file_print(self, conn, fid):
        try:
            ctype, content = files.print_view(conn, fid)
        except (ValueError, OSError):
            raise _NotFound() from None
        self._send_inline(content, ctype)

    def _files_bulk(self, conn, query):
        ids = [_id(v) for v in query.get("file_id", [])]
        if not ids:
            return self._redirect("/files")
        try:
            blob = files.bulk_download(conn, file_ids=ids)
        except (ValueError, OSError):
            raise _NotFound() from None
        self._send_file(blob, "files.zip", ctype="application/zip")

    def _file_download(self, conn, fid):
        try:
            f = files.get_file(conn, fid)
            name, content = files.download(conn, fid)
        except (ValueError, OSError):
            raise _NotFound() from None
        self._send_file(content, name,
                        ctype=f["content_type"]
                        or "application/octet-stream")

    # --- tasks tab (rebuilt by casework-tabs P2 under the 2026-08-10
    # program amendment: my-open default, type-and-Enter quick-add,
    # one-click complete, task-list builder + import. SQL in
    # reads.py; every write rides casework's tasks module) ---

    @staticmethod
    def _complete_button(tid, back):
        """Two-action complete (P2 gate r2, James: a stray click
        must not dismiss a task): the browser refuses the submit
        until the box is checked (native required, zero JS), so
        Done takes check-then-click. 'back' returns the driver to
        the page they pressed it on."""
        return (f"<form class='inline' method='post'"
                f" action='/tasks/{tid}/complete'>"
                f"<input type='hidden' name='back' value='{back}'>"
                f"<input type='checkbox' required"
                f" title='Check the box, then press Done'>"
                f"<button class='small'>Done</button></form>")

    @staticmethod
    def _reopen_button(tid, back):
        """The undo behind Done (program amendment 2026-08-10:
        tasks.reopen_task is the one authorized post-freeze core
        addition). One click on purpose -- reopening only resurfaces
        work, it cannot lose any."""
        return (f"<form class='inline' method='post'"
                f" action='/tasks/{tid}/reopen'>"
                f"<input type='hidden' name='back' value='{back}'>"
                f"<button class='small'>Reopen</button></form>")

    @staticmethod
    def _linked_one(matter_id, contact_id, mnames, cnames):
        """Matter-first, ONE link (the P1 calendar ruling, extended
        to tasks at the P2 gate): the matter name already names the
        client; the pair was the crowding James flagged twice."""
        if matter_id:
            return html.link(f"/matters/{matter_id}",
                             mnames.get(matter_id, "matter"))
        if contact_id:
            return html.link(f"/contacts/{contact_id}",
                             cnames.get(contact_id, "client"))
        return "<span class='hint'>-</span>"

    def _tasks_index(self, conn, user, query):
        scope = ("firm" if query.get("scope", [None])[0] == "firm"
                 else "mine")
        done = query.get("done", [None])[0] == "1"
        rows_src = reads.tasks_rows(
            conn,
            assignee_id=None if scope == "firm" else user["id"],
            completed=done)
        mnames, cnames = self._name_maps(conn)
        anames = reads.task_assignee_names(conn)
        mine_href = "/tasks" + ("?done=1" if done else "")
        firm_href = "/tasks?scope=firm" + ("&done=1" if done else "")
        open_href = "/tasks" + ("?scope=firm" if scope == "firm"
                                else "")
        done_href = ("/tasks?done=1"
                     + ("&scope=firm" if scope == "firm" else ""))
        rows = []
        for t in rows_src:
            cells = [html.link(f"/tasks/{t['id']}", t["title"]),
                     html.mdy(t["due_date"]) if t["due_date"] else "-",
                     self._linked_one(t["matter_id"], t["contact_id"],
                                      mnames, cnames),
                     html.esc(anames.get(t["id"], "-"))]
            cells.append(
                html.mdy(t["completed_at"]) + " "
                + self._reopen_button(t["id"], done_href) if done
                else self._complete_button(t["id"], "/tasks"))
            rows.append(cells)
        chips = (
            "<div class='chips'>"
            f"<a class='chip{' on' if scope == 'mine' else ''}'"
            f" href='{mine_href}'>Mine</a>"
            f"<a class='chip{' on' if scope == 'firm' else ''}'"
            f" href='{firm_href}'>Firm</a>"
            f"<a class='chip{' on' if not done else ''}'"
            f" href='{open_href}'>Open</a>"
            f"<a class='chip{' on' if done else ''}'"
            f" href='{done_href}'>Completed</a></div>")
        quick = (
            "<form class='quick-add' method='post'"
            " action='/tasks/quick'>"
            "<div class='grow'><label>Add a task</label>"
            "<input name='title' autofocus required></div>"
            "<div class='due'><label>Due (optional)</label>"
            "<input type='date' name='due_date'></div>"
            "<button class='primary'>Add</button></form>"
            "<p class='hint'>Type and press Enter -- the task lands"
            " in your open list, assigned to you.</p>")
        if rows:
            head = ["Task", "Due", "Linked to", "Assigned to",
                    "Completed" if done else ""]
            inner = ("<div class='tasks-table'>"
                     + html.table(head, rows) + "</div>")
        elif done:
            inner = html.designed_empty(
                "Nothing completed here yet. A task's Done button"
                " moves it to this view.",
                f"<a class='quiet' href='{open_href}'>Open tasks</a>")
        else:
            who = ("in the firm" if scope == "firm"
                   else "assigned to you")
            inner = html.designed_empty(
                f"No open tasks {who}. Add one above and press"
                f" Enter, or import a task list onto a matter.",
                "<a class='quiet' href='/settings/task-lists'>Task"
                " lists</a>")
        body = (f"<div class='card'><h1>Tasks</h1>{quick}{chips}"
                f"{inner}<div class='actions'>"
                f"<a class='quiet' href='/settings/task-lists'>Task"
                f" lists</a></div></div>")
        self._send_page(200, html.page("Tasks", body,
                                       user_name=user["name"],
                                       active_href="/tasks"))

    def _task_detail(self, conn, user, tid):
        t = reads.task_row(conn, tid)
        if t is None:
            raise _NotFound()
        mnames, cnames = self._name_maps(conn)
        linked = self._linked_one(t["matter_id"], t["contact_id"],
                                  mnames, cnames)
        holders = ", ".join(
            html.esc(u["name"]) for uid in tasks.assignees(conn, tid)
            if (u := reads.get_user(conn, uid)) is not None)
        if t["completed_at"]:
            status = (f"<span class='pill returned'>completed"
                      f" {html.mdy(t['completed_at'])}</span>")
            act = self._reopen_button(tid, f"/tasks/{tid}")
        else:
            status = "<span class='pill'>open</span>"
            act = self._complete_button(tid, f"/tasks/{tid}")
        due = html.mdy(t["due_date"]) if t["due_date"] else "-"
        body = (f"<div class='card tab-detail'>"
                f"<h1>{html.esc(t['title'])}</h1>"
                f"<dl class='kv'>"
                f"<dt>Status</dt><dd>{status} {act}"
                f"</dd><dt>Due</dt><dd>{due}"
                f"</dd><dt>Linked</dt><dd>{linked}</dd>"
                f"<dt>Assigned to</dt><dd>{holders or '-'}</dd></dl>"
                f"<div class='actions'><a class='quiet' href='/tasks'>"
                f"Back to tasks</a></div></div>")
        self._send_page(200, html.page(t["title"], body,
                                       user_name=user["name"],
                                       active_href="/tasks"))

    def _task_quick_create(self, conn, now, uid):
        f = self._form_body()
        title = f.get("title", "").strip()
        if title:
            tasks.create_task(conn, title, now, uid,
                              due_date=f.get("due_date") or None)
            conn.commit()
        return self._redirect("/tasks")

    def _task_complete(self, conn, now, tid):
        if reads.task_row(conn, tid) is None:
            raise _NotFound()
        tasks.complete_task(conn, tid, now)
        conn.commit()
        back = self._form_body().get("back", "")
        return self._redirect(back if back.startswith("/") else "/tasks")

    def _task_reopen(self, conn, tid):
        if reads.task_row(conn, tid) is None:
            raise _NotFound()
        tasks.reopen_task(conn, tid)
        conn.commit()
        back = self._form_body().get("back", "")
        return self._redirect(back if back.startswith("/") else "/tasks")

    # --- task lists (built here at P2; re-homed into the Settings
    # layout at P6 -- plan.md machinery-home note) ---

    def _task_lists(self, conn, user):
        autos = reads.task_list_automations(conn)
        rows = [[html.link(f"/settings/task-lists/{tl['id']}",
                           tl["name"]),
                 str(tl["item_count"]),
                 f"<span class='automations'>"
                 f"{html.esc('; '.join(autos.get(tl['id'], [])) or '-')}"
                 f"</span>"]
                for tl in reads.task_lists_rows(conn)]
        inner = ("<div class='tasks-table'>"
                 + html.table(["Task list", "Items", "Automations"],
                              rows) + "</div>"
                 if rows else html.designed_empty(
                     "No task lists yet. A task list is a reusable"
                     " checklist -- build it once, then import it"
                     " onto any matter or client in one click.",
                     "<a class='quiet' href='/tasks'>Back to tasks"
                     "</a>"))
        form = (f"<form method='post' action='/settings/task-lists'>"
                + html.field("New task list name", "name",
                             autofocus=True)
                + "<button class='primary'>Create list</button>"
                  "</form>")
        note = ("<p class='hint'>Automations show which matter"
                " workflow statuses import a list on their own.</p>")
        body = (f"<div class='card'><h1>Task lists</h1>{form}{inner}"
                f"{note}<div class='actions'><a class='quiet'"
                f" href='/tasks'>Back to tasks</a></div></div>")
        self._send_page(200, html.page("Task lists", body,
                                       user_name=user["name"],
                                       active_href="/settings"))

    def _task_list_create(self, conn):
        name = self._form_body().get("name", "").strip()
        if not name:
            return self._redirect("/settings/task-lists")
        lid = tasks.create_task_list(conn, name)
        conn.commit()
        return self._redirect(f"/settings/task-lists/{lid}")

    def _task_list_detail(self, conn, user, lid, error=None):
        tl = reads.task_list_row(conn, lid)
        if tl is None:
            raise _NotFound()
        labels = reads.fact_labels(conn)
        items = reads.task_list_items(conn, lid)
        rows = []
        for i in items:
            if i["ref_fact_key"]:
                what = labels.get(i["ref_fact_key"]) or i["ref_fact_key"]
                rule = (f"due {i['ref_days']} days"
                        f" {i['ref_direction']} {what}")
            elif i["duration_days"] is not None:
                rule = f"due {i['duration_days']} days after import"
            else:
                rule = "no due date"
            rows.append([str(i["position"]), html.esc(i["title"]),
                         html.esc(rule),
                         html.esc(i["assignee_name"] or "importer")])
        table = ("<div class='tasks-table'>"
                 + html.table(["#", "Item", "Due rule",
                               "Assigned to"], rows) + "</div>"
                 if rows else html.designed_empty(
                     "No items yet. Each item becomes one real task"
                     " when this list is imported onto a matter or"
                     " client -- add the first below.",
                     "<a class='quiet' href='/settings/task-lists'>"
                     "All task lists</a>"))
        fopts = "".join(
            f"<option value='{d['key']}'>{html.esc(d['label'])}"
            f"</option>"
            for d in reads.contact_date_fact_defs(conn))
        uopts = "".join(
            f"<option value='{u['id']}'>{html.esc(u['name'])}"
            f"</option>"
            for u in reads.list_users(conn)
            if not u["deactivated_at"])
        form = (
            f"<h2>Add an item</h2>{html.error_box(error)}"
            f"<form method='post'"
            f" action='/settings/task-lists/{lid}/items'>"
            + html.field("Item title", "title")
            + html.field("Position", "position",
                         value=str(len(items) + 1))
            + html.field("Due days after import", "duration_days",
                         required=False,
                         hint="Leave empty for no due date, or use a"
                              " reference date below instead.")
            + f"<label>Reference date (client fact)</label>"
              f"<select name='ref_fact_key'>"
              f"<option value=''>-- none --</option>{fopts}</select>"
            + f"<label>Before or after it</label>"
              f"<select name='ref_direction'>"
              f"<option value='before'>before</option>"
              f"<option value='after'>after</option></select>"
            + html.field("Days before/after", "ref_days",
                         required=False)
            + f"<label>Assign to</label>"
              f"<select name='default_assignee_id'>"
              f"<option value=''>-- whoever imports --</option>"
              f"{uopts}</select>"
            + "<button class='primary'>Add item</button></form>")
        autos = reads.task_list_automations(conn).get(lid, [])
        note = (f"<p class='hint'><span class='automations'>Imported"
                f" automatically by: {html.esc('; '.join(autos))}"
                f"</span></p>" if autos else
                "<p class='hint'><span class='automations'>No matter"
                " workflow imports this list automatically; import"
                " it from any matter or client page.</span></p>")
        body = (f"<div class='card'><h1>{html.esc(tl['name'])}</h1>"
                f"{table}{note}{form}"
                f"<div class='actions'><a class='quiet'"
                f" href='/settings/task-lists'>All task lists</a>"
                f"</div></div>")
        self._send_page(200, html.page(tl["name"], body,
                                       user_name=user["name"],
                                       active_href="/settings"))

    def _task_list_item_create(self, conn, user, lid):
        if reads.task_list_row(conn, lid) is None:
            raise _NotFound()
        f = self._form_body()
        ref_key = f.get("ref_fact_key") or None
        try:
            tasks.add_list_item(
                conn, lid, f.get("title", "").strip(),
                int(f.get("position") or 0),
                duration_days=(int(f["duration_days"])
                               if f.get("duration_days") else None),
                default_assignee_id=(int(f["default_assignee_id"])
                                     if f.get("default_assignee_id")
                                     else None),
                ref_fact_key=ref_key,
                ref_direction=(f.get("ref_direction")
                               if ref_key else None),
                ref_days=(int(f["ref_days"])
                          if ref_key and f.get("ref_days") else None))
        except ValueError as e:
            return self._task_list_detail(conn, user, lid,
                                          error=str(e))
        conn.commit()
        return self._redirect(f"/settings/task-lists/{lid}")

    def _import_task_list(self, conn, now, uid, matter_id=None,
                          contact_id=None):
        if matter_id is not None:
            if reads.matter_row(conn, matter_id) is None:
                raise _NotFound()
            back = f"/matters/{matter_id}"
        else:
            if reads.contact_row(conn, contact_id) is None:
                raise _NotFound()
            back = f"/contacts/{contact_id}"
        f = self._form_body()
        tlid = int(f["task_list_id"]) if f.get("task_list_id") else None
        if tlid is None or reads.task_list_row(conn, tlid) is None:
            raise _NotFound()
        tasks.import_task_list(conn, tlid, now, uid,
                               matter_id=matter_id,
                               contact_id=contact_id)
        conn.commit()
        return self._redirect(back)

    def _tasks_card(self, conn, kind, ent_id, back):
        """The matter/contact Tasks section (Appendix A): open tasks
        + Import Task List. Rendering only; rows via the tasks
        module, names via reads."""
        anames = reads.task_assignee_names(conn)
        open_tasks = tasks.list_tasks(
            conn, matter_id=ent_id if kind == "matters" else None,
            contact_id=ent_id if kind == "contacts" else None)
        rows = [[html.link(f"/tasks/{t['id']}", t["title"]),
                 html.mdy(t["due_date"]) if t["due_date"] else "-",
                 html.esc(anames.get(t["id"], "-")),
                 self._complete_button(t["id"], back)]
                for t in open_tasks]
        table = ("<div class='tasks-table'>"
                 + html.table(["Task", "Due", "Assigned to", ""],
                              rows) + "</div>"
                 if rows else "<p class='hint'>No open tasks here"
                 " yet.</p>")
        lists = reads.task_lists_rows(conn)
        if lists:
            opts = "".join(
                f"<option value='{tl['id']}'>{html.esc(tl['name'])}"
                f"</option>" for tl in lists)
            imp = (f"<form class='quick-add' method='post'"
                   f" action='{back}/import-task-list'>"
                   f"<div class='grow'><label>Import a task list"
                   f"</label><select name='task_list_id'>{opts}"
                   f"</select></div>"
                   f"<button class='primary'>Import</button></form>")
        else:
            imp = ("<p class='hint'>No task lists yet -- <a"
                   " href='/settings/task-lists'>build one</a> and"
                   " its items land here as tasks in one click.</p>")
        return (f"<div class='card'><h1>Tasks</h1>{table}{imp}"
                f"</div>")

    # --- notes tab (rebuilt by casework-tabs P3 under the 2026-08-10
    # program amendment: minimal capture + expandable form, ALL
    # default pinned-first, category + mine chips, matter/contact
    # timelines, categories home, PDF export. SQL in reads.py;
    # writes ride casework's notes module) ---

    @staticmethod
    def _note_label(n):
        if n["title"]:
            return n["title"]
        return (n["body"][:48] + "..." if len(n["body"]) > 48
                else n["body"])

    @staticmethod
    def _pin_button(n, back):
        """Pin lifts a note to the top of every list it lives in;
        the same button unpins."""
        word = "Unpin" if n["pinned"] else "Pin"
        return (f"<form class='inline' method='post'"
                f" action='/notes/{n['id']}/pin'>"
                f"<input type='hidden' name='back' value='{back}'>"
                f"<button class='small'>{word}</button></form>")

    @staticmethod
    def _quick_note_form(back, matter_id=None, contact_id=None):
        """Minimal capture (Appendix A): body + Save. Hidden scope
        fields make the same form work on the index (unassociated,
        spec's dashboard scoping) and on matter/contact sections."""
        hidden = f"<input type='hidden' name='back' value='{back}'>"
        if matter_id is not None:
            hidden += (f"<input type='hidden' name='matter_id'"
                       f" value='{matter_id}'>")
        if contact_id is not None:
            hidden += (f"<input type='hidden' name='contact_id'"
                       f" value='{contact_id}'>")
        return (f"<form class='quick-add' method='post'"
                f" action='/notes/quick'>{hidden}"
                f"<div class='grow'><label>Add a note</label>"
                f"<textarea name='body' rows='2' required></textarea>"
                f"</div><button class='primary'>Save</button></form>")

    def _notes_index(self, conn, user, query):
        cat = query.get("category", [None])[0]
        cat = int(cat) if cat and cat.isdigit() else None
        mine = query.get("mine", [None])[0] == "1"
        rows_src = reads.notes_rows(
            conn, category_id=cat,
            assignee_id=user["id"] if mine else None)
        mnames, cnames = self._name_maps(conn)
        rows = []
        for n in rows_src:
            pin = ("<span class='pill'>pinned</span>" if n["pinned"]
                   else "<span class='hint'>-</span>")
            rows.append([html.link(f"/notes/{n['id']}",
                                   self._note_label(n)),
                         pin,
                         html.esc(n["category_name"] or "-"),
                         self._linked_one(n["matter_id"],
                                          n["contact_id"], mnames,
                                          cnames),
                         html.mdy(n["created_at"])])
        mineq = "&mine=1" if mine else ""
        catq = f"&category={cat}" if cat is not None else ""
        chips = (f"<a class='chip{' on' if cat is None and not mine else ''}'"
                 f" href='/notes'>All</a>"
                 f"<a class='chip{' on' if mine else ''}'"
                 f" href='/notes?mine=1{catq}'>Mine</a>")
        for c in reads.note_categories_rows(conn):
            on = " on" if cat == c["id"] else ""
            chips += (f"<a class='chip{on}' href='/notes?category="
                      f"{c['id']}{mineq}'>{html.esc(c['name'])}</a>")
        chips = f"<div class='chips'>{chips}</div>"
        expand = ("<p class='hint'>Need a title, category, client"
                  " link, or firm-wide notify? "
                  + html.link("/notes/new", "Open the full note form")
                  + ".</p>")
        if rows:
            inner = ("<div class='tasks-table'>"
                     + html.table(["Note", "Pinned", "Category",
                                   "Linked to", "Created"], rows)
                     + "</div>")
        else:
            what = ("in this view" if (cat is not None or mine)
                    else "yet")
            inner = html.designed_empty(
                f"No notes {what}. Notes hold the reasoning a form"
                f" never captures -- type one above and Save.",
                "<a class='quiet' href='/notes/new'>Full note form"
                "</a>")
        body = (f"<div class='card'><h1>Notes</h1>"
                + self._quick_note_form("/notes")
                + expand + chips + inner
                + "<div class='actions'><a class='quiet'"
                  " href='/settings/note-categories'>Note categories"
                  "</a></div></div>")
        self._send_page(200, html.page("Notes", body,
                                       user_name=user["name"],
                                       active_href="/notes"))

    def _note_new(self, conn, user, query, error=None):
        pre_m = query.get("matter", [""])[0]
        mopts = "".join(
            f"<option value='{m['id']}'"
            f"{' selected' if str(m['id']) == pre_m else ''}>"
            f"{html.esc(m['name'])} -- {html.esc(m['display_name'])}"
            f"</option>" for m in reads.list_matters(conn))
        copts = "".join(
            f"<option value='{c['id']}'>"
            f"{html.esc(c['display_name'])}</option>"
            for c in reads.list_contacts(conn))
        catopts = "".join(
            f"<option value='{c['id']}'>{html.esc(c['name'])}"
            f"</option>" for c in reads.note_categories_rows(conn))
        uopts = "".join(
            f"<option value='{u['id']}'>{html.esc(u['name'])}"
            f"</option>" for u in reads.list_users(conn)
            if not u["deactivated_at"] and u["id"] != user["id"])
        body = (f"<div class='card narrow'><h1>New note</h1>"
                f"{html.error_box(error)}"
                f"<form method='post' action='/notes/new'>"
                + html.field("Title", "title", autofocus=True,
                             required=False)
                + f"<label>Note</label>"
                  f"<textarea name='body' rows='5' required>"
                  f"</textarea>"
                + f"<label>Category</label>"
                  f"<select name='category_id'>"
                  f"<option value=''>-- none --</option>{catopts}"
                  f"</select>"
                + f"<label>Matter</label><select name='matter_id'>"
                  f"<option value=''>-- no matter --</option>{mopts}"
                  f"</select>"
                + f"<label>Client</label><select name='contact_id'>"
                  f"<option value=''>-- no client --</option>{copts}"
                  f"</select>"
                + (f"<label>Also assign to</label>"
                   f"<select name='assignee_ids' multiple>{uopts}"
                   f"</select>" if uopts else "")
                + "<label><input type='checkbox' name='notify_all'"
                  " style='width:auto'> Notify the whole firm</label>"
                + "<button class='primary'>Save note</button>"
                  "</form></div>")
        self._send_page(200, html.page("New note", body,
                                       user_name=user["name"],
                                       active_href="/notes"))

    def _note_quick_create(self, conn, now, uid):
        f = self._form_body()
        body = f.get("body", "").strip()
        back = f.get("back", "")
        if body:
            notes.create_note(
                conn, body, now, uid,
                matter_id=int(f["matter_id"])
                if f.get("matter_id") else None,
                contact_id=int(f["contact_id"])
                if f.get("contact_id") else None)
            conn.commit()
        return self._redirect(back if back.startswith("/") else "/notes")

    def _note_full_create(self, conn, now, uid):
        f = self._form_body_multi()
        one = {k: v[0] for k, v in f.items()}
        body = one.get("body", "").strip()
        if not body:
            return self._redirect("/notes/new")
        nid = notes.create_note(
            conn, body, now, uid,
            title=one.get("title", "").strip() or None,
            category_id=int(one["category_id"])
            if one.get("category_id") else None,
            matter_id=int(one["matter_id"])
            if one.get("matter_id") else None,
            contact_id=int(one["contact_id"])
            if one.get("contact_id") else None,
            notify_all=1 if one.get("notify_all") else 0)
        for aid in f.get("assignee_ids", []):
            if aid.isdigit() and int(aid) != uid:
                notes.assign(conn, nid, int(aid))
        conn.commit()
        return self._redirect(f"/notes/{nid}")

    def _note_pin_toggle(self, conn, nid):
        n = reads.note_row(conn, nid)
        if n is None:
            raise _NotFound()
        notes.pin(conn, nid, pinned=not n["pinned"])
        conn.commit()
        back = self._form_body().get("back", "")
        return self._redirect(back if back.startswith("/") else "/notes")

    def _note_detail(self, conn, user, nid):
        n = reads.note_row(conn, nid)
        if n is None:
            raise _NotFound()
        mnames, cnames = self._name_maps(conn)
        linked = self._linked_one(n["matter_id"], n["contact_id"],
                                  mnames, cnames)
        cats = {c["id"]: c["name"] for c in reads.note_categories(conn)}
        cat = cats.get(n["category_id"], "-")
        holders = ", ".join(
            html.esc(u["name"]) for uid in notes.assignees(conn, nid)
            if (u := reads.get_user(conn, uid)) is not None)
        pinned = ("<span class='pill'>pinned</span> " if n["pinned"]
                  else "")
        text = html.esc(n["body"]).replace("\n", "<br>")
        body = (f"<div class='card tab-detail'><h1>"
                f"{html.esc(n['title'] or 'Note')}</h1>"
                f"<p>{pinned}{self._pin_button(n, f'/notes/{nid}')}</p>"
                f"<dl class='kv'>"
                f"<dt>Category</dt><dd>{html.esc(cat)}</dd>"
                f"<dt>Linked</dt><dd>{linked}</dd>"
                f"<dt>Assigned to</dt><dd>{holders or '-'}</dd>"
                f"<dt>Created</dt><dd>{html.mdy(n['created_at'])}"
                f"</dd></dl><p>{text}</p>")
        # export from the note itself (P3 gate r2, James: the pdf
        # option lived only on the linked-to page). The core export
        # is scope-based, so the button names whose notes it makes.
        if n["matter_id"]:
            body += (f"<form class='inline' method='get' action="
                     f"'/matters/{n['matter_id']}/notes.pdf'>"
                     f"<button class='small'>Export this matter's"
                     f" notes (PDF)</button></form>")
        elif n["contact_id"]:
            body += (f"<form class='inline' method='get' action="
                     f"'/contacts/{n['contact_id']}/notes.pdf'>"
                     f"<button class='small'>Export this client's"
                     f" notes (PDF)</button></form>")
        body += (f"<div class='actions'><a class='quiet'"
                 f" href='/notes'>Back to notes</a></div></div>")
        self._send_page(200, html.page(n["title"] or "Note", body,
                                       user_name=user["name"],
                                       active_href="/notes"))

    def _note_categories(self, conn, user):
        rows = [[html.esc(c["name"]),
                 "builtin" if c["builtin"] else "custom",
                 str(c["note_count"])]
                for c in reads.note_categories_rows(conn)]
        inner = ("<div class='tasks-table'>"
                 + html.table(["Category", "Kind", "Notes"], rows)
                 + "</div>"
                 if rows else html.designed_empty(
                     "No categories yet. A category is a label the"
                     " notes index can filter by -- create the first"
                     " below.",
                     "<a class='quiet' href='/notes'>Back to notes"
                     "</a>"))
        form = (f"<form method='post'"
                f" action='/settings/note-categories'>"
                + html.field("New category name", "name",
                             autofocus=True)
                + "<button class='primary'>Create category</button>"
                  "</form>")
        body = (f"<div class='card'><h1>Note categories</h1>{form}"
                f"{inner}<div class='actions'><a class='quiet'"
                f" href='/notes'>Back to notes</a></div></div>")
        self._send_page(200, html.page("Note categories", body,
                                       user_name=user["name"],
                                       active_href="/settings"))

    def _note_category_create(self, conn):
        name = self._form_body().get("name", "").strip()
        if name:
            notes.create_category(conn, name)
            conn.commit()
        return self._redirect("/settings/note-categories")

    def _notes_card(self, conn, kind, ent_id, back):
        """The matter/contact Notes timeline (Appendix A): pinned on
        top then newest, minimal capture, PDF export. Rendering
        only."""
        scope = {"matter_id" if kind == "matters" else "contact_id":
                 ent_id}
        entries = ""
        for n in reads.notes_rows(conn, **scope):
            cls = "note-entry pinned" if n["pinned"] else "note-entry"
            pin_pill = ("<span class='pill'>pinned</span> "
                        if n["pinned"] else "")
            cat = (f"{html.esc(n['category_name'])} -- "
                   if n["category_name"] else "")
            entries += (
                f"<div class='{cls}'>"
                f"<p class='note-meta'>{html.mdy(n['created_at'])}"
                f" -- {cat}{pin_pill}"
                + html.link(f"/notes/{n['id']}",
                            self._note_label(n))
                + f" {self._pin_button(n, back)}</p>"
                f"<p class='note-body'>{html.esc(n['body'])}</p>"
                f"</div>")
        if not entries:
            entries = ("<p class='hint'>No notes here yet -- the"
                       " first one starts this timeline.</p>")
        export = (f"<form class='inline' method='get'"
                  f" action='{back}/notes.pdf'>"
                  f"<button class='small'>Export notes PDF</button>"
                  f"</form>")
        return (f"<div class='card'><h1>Notes</h1>"
                f"<div class='notes-timeline'>{entries}</div>"
                + self._quick_note_form(
                    back,
                    matter_id=ent_id if kind == "matters" else None,
                    contact_id=ent_id if kind == "contacts" else None)
                + f"<div class='actions-row'>{export}</div>"
                  f"</div>")

    def _notes_pdf(self, conn, matter_id=None, contact_id=None):
        if matter_id is not None \
                and reads.matter_row(conn, matter_id) is None:
            raise _NotFound()
        if contact_id is not None \
                and reads.contact_row(conn, contact_id) is None:
            raise _NotFound()
        content = notes.export_notes_pdf(conn, matter_id=matter_id,
                                         contact_id=contact_id)
        self._send_file(content, "notes.pdf")

    # --- search + settings (U2.3 / U2.4) ---

    def _search(self, conn, user, query):
        q = query.get("q", [""])[0].strip()
        form = (f"<form method='get' action='/search'>"
                + html.field("Search clients, matters, forms, and"
                             " receipt numbers", "q", value=q,
                             autofocus=True)
                + "<button class='primary'>Search</button></form>")
        if not q:
            results = html.empty_state(
                "Type part of a name, matter, form title, or USCIS"
                " receipt number.")
        else:
            hits = search.search(conn, q)
            if not hits:
                results = html.empty_state(
                    f'No records match "{q}". Partial names work --'
                    f" try fewer letters.")
            else:
                href = {"contact": "/contacts/{}", "matter":
                        "/matters/{}", "smart_form": "/forms/{}"}
                rows = [[html.esc(h["type"].replace("_", " ")),
                         html.link(href[h["type"]].format(h["id"]),
                                   h["label"]),
                         html.esc(h.get("receipt_number") or "-")]
                        for h in hits]
                results = html.table(["Type", "Record", "Receipt #"],
                                     rows)
        body = (f"<div class='card'><h1>Search</h1>{form}{results}"
                f"</div>")
        self._send_page(200, html.page("Search", body,
                                       user_name=user["name"]))

    def _settings(self, conn, user):
        srows = [[html.esc(r["key"]), html.esc(str(r["value"]))]
                 for r in reads.firm_settings_all(conn)]
        stable = (html.table(["Setting", "Value"], srows) if srows
                  else html.empty_state(
                      "No firm settings recorded yet. Defaults apply"
                      " until a workflow sets one."))
        urows = []
        for u in reads.list_users(conn):
            status = "deactivated" if u["deactivated_at"] else "active"
            urows.append([html.esc(u["name"]), html.esc(u["email"]),
                          html.esc(u["role_label"] or "-"),
                          "yes" if u["is_admin"] else "-",
                          f"<span class='pill'>{status}</span>"])
        body = (f"<div class='card'><h1>Firm settings</h1>"
                f"<p class='hint'>Read-only in v1 -- settings edits"
                f" are out of scope.</p>{stable}</div>"
                f"<div class='card'><h1>Users</h1>"
                + html.table(["Name", "Email", "Role", "Admin",
                              "Status"], urows)
                + "</div>")
        self._send_page(200, html.page("Settings", body,
                                       user_name=user["name"]))


def make_server(db_path, port=0, client_port=0):
    """Open (creating + installing if absent) db_path and bind the UI
    to localhost:port. Also mounts casework's UNMODIFIED client
    surface (intake/e-sign) on client_port, sharing the SAME
    connection and the SAME lock -- one process, one db, no casework
    edits (P1 gate flag). Returns the UI server; the client server
    rides on .client_httpd (start it with serve_client). app_conn is
    exposed for verifier assertions ONLY -- never for UI logic."""
    db_path = Path(db_path)
    if db_path.exists():
        conn = appdb.connect(str(db_path))
    else:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = appdb.create_db(str(db_path))
        bootstrap.install(conn, _now())
        conn.execute("INSERT INTO synthetic_marker (marker)"
                     " VALUES ('SYNTHETIC')")
        conn.commit()
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    httpd.app_conn = conn
    httpd.app_lock = threading.Lock()
    storage = db_path.parent / "storage"
    storage.mkdir(parents=True, exist_ok=True)
    httpd.storage_dir = storage  # files-tab uploads (P4a)
    client = cw_server.make_server(conn, storage, client_port)
    client.app_lock = httpd.app_lock  # ONE lock across both surfaces
    httpd.client_httpd = client
    httpd.client_base = (f"http://127.0.0.1:"
                         f"{client.server_address[1]}")
    return httpd


def serve_client(httpd):
    """Start the mounted client surface on a daemon thread."""
    thread = threading.Thread(
        target=httpd.client_httpd.serve_forever, daemon=True)
    thread.start()
    return thread


def main():
    ap = argparse.ArgumentParser(description="casework-ui server")
    ap.add_argument("--db", default="data/ui.db")
    ap.add_argument("--port", type=int, default=8500)
    ap.add_argument("--client-port", type=int, default=8501)
    args = ap.parse_args()
    httpd = make_server(args.db, args.port, args.client_port)
    host, port = httpd.server_address[:2]
    serve_client(httpd)
    print(f"casework-ui on http://{host}:{port} (db: {args.db};"
          f" client surface: {httpd.client_base})")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
