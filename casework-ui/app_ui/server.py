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
import re
import tempfile
import threading
import urllib.parse
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import app_ui  # noqa: F401  (wires casework onto sys.path)
from app import auth, bootstrap, contacts, events, facts, files, forms
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
                return self._files_index(conn, user)
            if len(segs) == 3 and segs[0] == "files" \
                    and segs[2] == "download":
                return self._file_download(conn, _id(segs[1]))
            if len(segs) == 2 and segs[0] == "files":
                return self._file_detail(conn, user, _id(segs[1]))
            if segs == ["tasks"]:
                return self._tasks_index(conn, user)
            if len(segs) == 2 and segs[0] == "tasks":
                return self._task_detail(conn, user, _id(segs[1]))
            if segs == ["notes"]:
                return self._notes_index(conn, user)
            if len(segs) == 2 and segs[0] == "notes":
                return self._note_detail(conn, user, _id(segs[1]))
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
                return self._calendar(conn, user)
            if segs == ["calendar", "new"]:
                return self._event_new(conn, user, query)
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
        body = (f"<div class='card narrow'><h1>Log in</h1>"
                f"{html.error_box(error)}"
                f"<form method='post' action='/login'>"
                + html.field("Email", "email", ftype="email",
                             autofocus=True)
                + html.field("Password", "password", ftype="password")
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
        c = reads.counts(conn)
        tallies = ", ".join(
            html.link(href, f"{c[key]} {label}")
            for key, label, href in (("contacts", "clients", "/contacts"),
                                     ("matters", "matters", "/matters"),
                                     ("events", "events", "/calendar"),
                                     ("files", "files", "/files"),
                                     ("tasks", "tasks", "/tasks"),
                                     ("notes", "notes", "/notes")))
        body = (f"<div class='card'><h1>Dashboard</h1>"
                f"<p>Logged in as {html.esc(user['name'])}"
                f" ({html.esc(user['email'])}).</p>"
                f"<div class='actions'>"
                f"<a href='/contacts/new'>New client</a>"
                f"<a href='/matters/new'>New matter</a>"
                f"<a class='quiet' href='/calendar'>Calendar</a></div>"
                f"<p class='hint'>{tallies}.</p>"
                f"</div>")
        self._send_page(200, html.page("Dashboard", body,
                                       user_name=user["name"]))

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
        kv = "".join(
            f"<dt>{html.esc(key)}</dt><dd>{html.esc(str(val))}</dd>"
            for (key, idx), val in sorted(f.items())
            if key != "meta.synthetic")
        mrows = [[html.link(f"/matters/{m['id']}", m["name"]),
                  html.esc(m["created_at"][:10])]
                 for m in reads.contact_matters(conn, cid)]
        mtable = (html.table(["Matter", "Created"], mrows) if mrows
                  else "<p class='hint'>No matters yet.</p>")
        body = (f"<div class='card'><h1>{html.esc(row['display_name'])}"
                f"</h1><div class='actions'>"
                f"<a href='/matters/new?contact={cid}'>New matter for"
                f" this client</a></div>"
                f"<dl class='kv'>{kv}</dl></div>"
                f"<div class='card'><h1>Matters</h1>{mtable}</div>")
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
        frows = [[html.link(f"/forms/{s['id']}", s["title"]),
                  html.esc(s["created_at"][:10])]
                 for s in reads.matter_smart_forms(conn, mid)]
        ftable = (html.table(["Form package", "Created"], frows) if frows
                  else "<p class='hint'>No form packages yet.</p>")
        erows = [[html.link(f"/calendar/{e['id']}", e["title"]),
                  html.esc(e["starts_at"][:16].replace("T", " "))]
                 for e in reads.matter_events(conn, mid)]
        etable = (html.table(["Deadline / event", "When"], erows)
                  if erows else "<p class='hint'>No deadlines yet.</p>")
        body = (f"<div class='card'><h1>{html.esc(row['name'])}</h1>"
                f"<dl class='kv'><dt>Client</dt><dd>"
                + html.link(f"/contacts/{contact['id']}",
                            contact["display_name"])
                + f"</dd><dt>Description</dt><dd>"
                  f"{html.esc(row['description'] or '-')}</dd></dl>"
                f"<div class='actions'>"
                f"<a href='/matters/{mid}/forms-new'>New form package"
                f"</a><a href='/calendar/new?matter={mid}&contact="
                f"{row['primary_contact_id']}'>New deadline</a></div>"
                f"</div>"
                f"<div class='card'><h1>Form packages</h1>{ftable}</div>"
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

    # --- calendar + deadlines (U1.6) ---

    def _calendar(self, conn, user):
        rows = [[html.link(f"/calendar/{e['id']}", e["title"]),
                 html.esc(e["starts_at"][:16].replace("T", " "))]
                for e in events.list_events(conn)]
        table = (html.table(["Event", "When (UTC)"], rows) if rows
                 else html.empty_state("Nothing scheduled. Deadlines"
                                       " land here from their matter"
                                       " or from New deadline above."))
        body = (f"<div class='card'><h1>Calendar</h1>"
                f"<div class='actions'><a href='/calendar/new'>New"
                f" deadline</a></div>{table}</div>")
        self._send_page(200, html.page("Calendar", body,
                                       user_name=user["name"]))

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
        rem = reads.event_reminders(conn, eid)
        rrows = [[f"{r['offset_value']} {r['offset_unit']} before",
                  html.esc(r["channel"])] for r in rem]
        rtable = (html.table(["Reminder", "Channel"], rrows) if rrows
                  else "<p class='hint'>No reminders.</p>")
        links = ""
        if e["matter_id"]:
            links += html.link(f"/matters/{e['matter_id']}",
                               "Matter") + " "
        body = (f"<div class='card'><h1>{html.esc(e['title'])}</h1>"
                f"<dl class='kv'><dt>When (UTC)</dt><dd>"
                f"{html.esc(e['starts_at'][:16].replace('T', ' '))}"
                f"</dd><dt>Linked</dt><dd>{links or '-'}</dd></dl>"
                f"{rtable}"
                f"<div class='actions'><a class='quiet' href='/calendar'>"
                f"Back to calendar</a></div></div>")
        self._send_page(200, html.page(e["title"], body,
                                       user_name=user["name"]))

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

    def _files_index(self, conn, user):
        mnames, cnames = self._name_maps(conn)
        rows = [[html.link(f"/files/{f['id']}", f["name"]),
                 self._linked_cell(conn, f["matter_id"], f["contact_id"],
                                   mnames, cnames),
                 html.esc(_fmt_size(f["size_bytes"])),
                 html.esc((f["uploaded_at"] or "")[:10])]
                for f in files.list_files(conn)]
        inner = (html.table(["File", "Linked to", "Size", "Uploaded"],
                            rows)
                 if rows else html.empty_state(
                     "No files yet. Filled PDFs land here when a form"
                     " package is produced; uploads join them."))
        body = (f"<div class='card'><h1>Files</h1>{inner}</div>")
        self._send_page(200, html.page("Files", body,
                                       user_name=user["name"]))

    def _file_detail(self, conn, user, fid):
        try:
            f = files.get_file(conn, fid)
        except ValueError:
            raise _NotFound() from None
        mnames, cnames = self._name_maps(conn)
        linked = self._linked_cell(conn, f["matter_id"], f["contact_id"],
                                   mnames, cnames)
        body = (f"<div class='card'><h1>{html.esc(f['name'])}</h1>"
                f"<dl class='kv'>"
                f"<dt>Size</dt><dd>{html.esc(_fmt_size(f['size_bytes']))}"
                f"</dd><dt>Type</dt><dd>{html.esc(f['content_type'] or '-')}"
                f"</dd><dt>Source</dt><dd>{html.esc(f['source'] or '-')}"
                f"</dd><dt>Linked</dt><dd>{linked}</dd>"
                f"<dt>Uploaded</dt><dd>"
                f"{html.esc((f['uploaded_at'] or '-')[:16].replace('T', ' '))}"
                f"</dd></dl><div class='actions'>"
                f"<a href='/files/{fid}/download'>Download</a>"
                f"<a class='quiet' href='/files'>Back to files</a>"
                f"</div></div>")
        self._send_page(200, html.page(f["name"], body,
                                       user_name=user["name"]))

    def _file_download(self, conn, fid):
        try:
            f = files.get_file(conn, fid)
            name, content = files.download(conn, fid)
        except (ValueError, OSError):
            raise _NotFound() from None
        self._send_file(content, name,
                        ctype=f["content_type"]
                        or "application/octet-stream")

    def _tasks_index(self, conn, user):
        mnames, cnames = self._name_maps(conn)
        rows = []
        for t in tasks.list_tasks(conn, include_completed=True):
            status = "done" if t["completed_at"] else "open"
            rows.append([html.link(f"/tasks/{t['id']}", t["title"]),
                         html.esc(t["due_date"] or "-"),
                         self._linked_cell(conn, t["matter_id"],
                                           t["contact_id"], mnames,
                                           cnames),
                         f"<span class='pill'>{status}</span>"])
        inner = (html.table(["Task", "Due", "Linked to", "Status"], rows)
                 if rows else html.empty_state(
                     "No tasks yet. Tasks arrive from task-list"
                     " imports and teammates."))
        body = f"<div class='card'><h1>Tasks</h1>{inner}</div>"
        self._send_page(200, html.page("Tasks", body,
                                       user_name=user["name"]))

    def _task_detail(self, conn, user, tid):
        t = reads.task_row(conn, tid)
        if t is None:
            raise _NotFound()
        mnames, cnames = self._name_maps(conn)
        linked = self._linked_cell(conn, t["matter_id"], t["contact_id"],
                                   mnames, cnames)
        holders = ", ".join(
            html.esc(u["name"]) for uid in tasks.assignees(conn, tid)
            if (u := reads.get_user(conn, uid)) is not None)
        status = "done" if t["completed_at"] else "open"
        body = (f"<div class='card'><h1>{html.esc(t['title'])}</h1>"
                f"<dl class='kv'>"
                f"<dt>Status</dt><dd><span class='pill'>{status}</span>"
                f"</dd><dt>Due</dt><dd>{html.esc(t['due_date'] or '-')}"
                f"</dd><dt>Linked</dt><dd>{linked}</dd>"
                f"<dt>Assigned to</dt><dd>{holders or '-'}</dd></dl>"
                f"<div class='actions'><a class='quiet' href='/tasks'>"
                f"Back to tasks</a></div></div>")
        self._send_page(200, html.page(t["title"], body,
                                       user_name=user["name"]))

    def _notes_index(self, conn, user):
        mnames, cnames = self._name_maps(conn)
        rows = []
        for nid in notes.list_notes(conn):
            n = reads.note_row(conn, nid)
            label = n["title"] or (n["body"][:48] + "..."
                                   if len(n["body"]) > 48 else n["body"])
            pin = ("<span class='pill'>pinned</span>" if n["pinned"]
                   else "<span class='hint'>-</span>")
            rows.append([html.link(f"/notes/{nid}", label), pin,
                         self._linked_cell(conn, n["matter_id"],
                                           n["contact_id"], mnames,
                                           cnames),
                         html.esc(n["created_at"][:10])])
        inner = (html.table(["Note", "Pinned", "Linked to", "Created"],
                            rows)
                 if rows else html.empty_state(
                     "No notes yet. Notes hold the reasoning a form"
                     " never captures."))
        body = f"<div class='card'><h1>Notes</h1>{inner}</div>"
        self._send_page(200, html.page("Notes", body,
                                       user_name=user["name"]))

    def _note_detail(self, conn, user, nid):
        n = reads.note_row(conn, nid)
        if n is None:
            raise _NotFound()
        mnames, cnames = self._name_maps(conn)
        linked = self._linked_cell(conn, n["matter_id"], n["contact_id"],
                                   mnames, cnames)
        cats = {c["id"]: c["name"] for c in reads.note_categories(conn)}
        cat = cats.get(n["category_id"], "-")
        text = html.esc(n["body"]).replace("\n", "<br>")
        body = (f"<div class='card'><h1>"
                f"{html.esc(n['title'] or 'Note')}</h1>"
                f"<dl class='kv'>"
                f"<dt>Category</dt><dd>{html.esc(cat)}</dd>"
                f"<dt>Pinned</dt><dd>{'yes' if n['pinned'] else '-'}</dd>"
                f"<dt>Linked</dt><dd>{linked}</dd>"
                f"<dt>Created</dt><dd>"
                f"{html.esc(n['created_at'][:16].replace('T', ' '))}"
                f"</dd></dl><p>{text}</p>"
                f"<div class='actions'><a class='quiet' href='/notes'>"
                f"Back to notes</a></div></div>")
        self._send_page(200, html.page(n["title"] or "Note", body,
                                       user_name=user["name"]))

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
