"""Verifier 1: the scripted UI walk (goal.md strawman, ratified).

Oracle-first (op rule 7): every story step is enumerated HERE,
before its screens exist. Steps whose screens are unbuilt raise
Pending and report PENDING; the runner exits 0 only when every
step PASSES and both sweeps pass. At P0 close the expected state
is: setup/auth steps green, anchor-path steps pending, exit 1.

The walk drives the UI exactly as a browser would -- GETs, form
POSTs, cookies, redirects. Module access is for ASSERTIONS only.

Run: python verify/run_ui_walk.py   (writes ui-walk-report.txt)
"""

import http.cookiejar
import re
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import app_ui  # noqa: F401, E402  (wires casework onto sys.path)
from app_ui import server as ui_server  # noqa: E402
from verify import sweeps  # noqa: E402

REPORT = HERE / "ui-walk-report.txt"

ADMIN = {"name": "Anchor Synthetic Admin",
         "email": "anchor.admin@synthetic.test",
         "password": "anchor-synthetic-pass"}


class Pending(Exception):
    """Screen not built yet -- expected in early phases."""


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Browser:
    """Cookie-carrying HTTP client; follows redirects like a browser."""

    def __init__(self, base):
        self.base = base
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar))

    def get(self, path):
        with self.opener.open(self.base + path, timeout=10) as r:
            return r.status, r.geturl(), r.read().decode("utf-8")

    def post(self, path, data):
        body = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(self.base + path, data=body,
                                     method="POST")
        req.add_header("Content-Type",
                       "application/x-www-form-urlencoded")
        with self.opener.open(req, timeout=10) as r:
            return r.status, r.geturl(), r.read().decode("utf-8")

    def get_bytes(self, path):
        with self.opener.open(self.base + path, timeout=10) as r:
            return r.read()


class Walk:
    def __init__(self, workdir):
        self.workdir = Path(workdir)
        self.httpd = None
        self.conn = None
        self.browser = None
        self.contact_id = None
        self.matter_id = None
        self.smart_form_id = None
        self.client_link = None
        self.event_id = None


# --- steps: P0 (built) ---

def step_first_run_setup(w):
    """A cold GET lands on /setup; creating the admin lands on MFA
    enrollment with a live (pre-MFA) session."""
    status, url, page = w.browser.get("/")
    assert status == 200 and url.endswith("/setup"), url
    assert "first account" in page
    status, url, page = w.browser.post("/setup", {
        "name": ADMIN["name"], "email": ADMIN["email"],
        "password": ADMIN["password"]})
    assert status == 200 and url.endswith("/enroll-mfa"), url
    n = w.conn.execute("SELECT count(*) FROM users").fetchone()[0]
    assert n == 1, f"users: {n}"
    row = w.conn.execute("SELECT is_admin, is_owner FROM users").fetchone()
    assert (row[0], row[1]) == (1, 1)
    return "cold GET -> /setup; admin created; landed on MFA enrollment"


CODE_RE = re.compile(r"verification code is (\d{6})")


def step_mfa_enrollment(w):
    """Enroll email-method 2FA (screen review 1 ruling: static code,
    no authenticator app); read the code from the synthetic mailbox
    panel, verify, land on the dashboard."""
    status, url, page = w.browser.post("/enroll-mfa", {})
    assert url.endswith("/mfa"), url
    assert "Your login code" in page, "code panel missing"
    m = CODE_RE.search(page)
    assert m is not None, "code not shown in code panel"
    status, url, page = w.browser.post("/mfa", {"code": m.group(1)})
    assert url.endswith("/") and "Dashboard" in page, url
    method = w.conn.execute(
        "SELECT twofa_method FROM users").fetchone()[0]
    assert method == "email", method
    passed = w.conn.execute(
        "SELECT twofa_passed FROM sessions ORDER BY id DESC LIMIT 1"
        ).fetchone()[0]
    assert passed == 1
    return ("email 2FA enrolled; static code read from mailbox panel;"
            " dashboard reached")


def step_login_roundtrip(w):
    """Log out, log back in: password -> /mfa (fresh challenge
    auto-issued) -> code -> dashboard. A wrong code is refused, and
    the static code still works after the failed try."""
    w.browser.post("/logout", {})
    status, url, _ = w.browser.get("/")
    assert url.endswith("/login"), url
    status, url, page = w.browser.post("/login", {
        "email": ADMIN["email"], "password": ADMIN["password"]})
    assert url.endswith("/mfa"), url
    m = CODE_RE.search(page)
    assert m is not None, "fresh challenge not shown at login"
    code = m.group(1)
    status, url, page = w.browser.post("/mfa", {"code": "000000"})
    assert "did not verify" in page
    status, url, page = w.browser.post("/mfa", {"code": code})
    assert url.endswith("/") and "Dashboard" in page, url
    return ("logout; re-login issued a fresh static code; wrong code"
            " refused; code survived the failed try")


def step_auth_gate(w):
    """A cookie-less client cannot reach any authenticated surface;
    bad credentials are refused."""
    anon = Browser(w.browser.base)
    for path in ("/", "/contacts", "/matters", "/no-such-page"):
        _status, url, _ = anon.get(path)
        assert url.endswith("/login"), f"{path} -> {url}"
    _s, url, page = anon.post("/login", {"email": ADMIN["email"],
                                         "password": "wrong"})
    assert "did not work" in page
    return "4 paths redirect anonymous to /login; bad password refused"


# --- steps: anchor path (P1) ---

G28_CLIENT_FAMILY = "form1[0].#subform[1].Pt3Line5a_FamilyName[0]"
G28_CLIENT_GIVEN = "form1[0].#subform[1].Pt3Line5b_GivenName[0]"


def step_create_contact(w):
    """Firm creates the client with a given name only -- the family
    name deliberately arrives later, from the client, over HTTP."""
    _s, _u, page = w.browser.get("/contacts/new")
    assert "New client" in page
    _s, url, page = w.browser.post("/contacts/new", {
        "given_name": "Nova", "family_name": "",
        "email": "nova.client@synthetic.test", "phone": "+1-555-0300"})
    m = re.search(r"/contacts/(\d+)$", url)
    assert m is not None, url
    w.contact_id = int(m.group(1))
    assert "Nova" in page
    from app import facts
    assert facts.get_fact(w.conn, "contact", w.contact_id,
                          "bio.family_name") is None
    audit = w.conn.execute(
        "SELECT actor_type FROM audit_log WHERE entity_type='contacts'"
        " AND action='insert' AND entity_id=?",
        (w.contact_id,)).fetchone()
    assert audit is not None and audit[0] == "user"
    return (f"contact {w.contact_id} created by click (no family"
            f" name); audit actor user")


def step_create_matter(w):
    _s, _u, page = w.browser.get(f"/matters/new?contact={w.contact_id}")
    assert "New matter" in page and "Nova" in page
    _s, url, page = w.browser.post("/matters/new", {
        "name": "Anchor Synthetic G-28 Matter",
        "contact_id": str(w.contact_id), "description": "UI walk"})
    m = re.search(r"/matters/(\d+)$", url)
    assert m is not None, url
    w.matter_id = int(m.group(1))
    assert "Anchor Synthetic G-28 Matter" in page and "Nova" in page
    return f"matter {w.matter_id} created; detail shows primary contact"


def step_forms_invitation(w):
    _s, _u, page = w.browser.get(f"/matters/{w.matter_id}/forms-new")
    assert "G-28" in page
    _s, url, page = w.browser.post(f"/matters/{w.matter_id}/forms-new",
                                   {"title": "Anchor G-28",
                                    "form_code": "g-28"})
    m = re.search(r"/forms/(\d+)$", url)
    assert m is not None, url
    w.smart_form_id = int(m.group(1))
    _s, _u, page = w.browser.post(f"/forms/{w.smart_form_id}/invite", {})
    assert "sent" in page, "invitation status not shown"
    m = re.search(r"(http://127\.0\.0\.1:\d+/intake/[0-9a-f]+)", page)
    assert m is not None, "client link not shown on the package page"
    w.client_link = m.group(1)
    mail = w.conn.execute(
        "SELECT recipient FROM email_outbox WHERE"
        " template='intake_invitation'").fetchone()
    assert mail is not None
    assert mail["recipient"] == "nova.client@synthetic.test"
    return (f"package {w.smart_form_id} (g-28); invitation emailed;"
            f" client link visible and copyable")


def step_client_intake_leg(w):
    """The client leg: a SEPARATE cookie-less browser follows the
    intake link onto casework's mounted client surface."""
    client = Browser("")
    with client.opener.open(w.client_link, timeout=10) as r:
        page = r.read().decode("utf-8")
    assert "Client family name" in page
    answers = [("q.g28.client_family_name", "Anchor-Synthetic"),
               ("q.g28.client_street", "300 Anchor Way"),
               ("q.g28.client_city", "Faketown"),
               ("q.g28.client_state", "VA"),
               ("q.g28.client_zip", "00003")]
    for qkey, value in answers:
        body = urllib.parse.urlencode(
            {"question": qkey, "value": value}).encode()
        req = urllib.request.Request(f"{w.client_link}/answer",
                                     data=body, method="POST")
        req.add_header("Content-Type",
                       "application/x-www-form-urlencoded")
        with client.opener.open(req, timeout=10) as r:
            assert r.status == 200
    req = urllib.request.Request(f"{w.client_link}/submit", data=b"",
                                 method="POST")
    with client.opener.open(req, timeout=10) as r:
        assert r.status == 200
    from app import facts
    got = facts.get_fact(w.conn, "contact", w.contact_id,
                         "bio.family_name")
    assert got == "Anchor-Synthetic", repr(got)
    _s, _u, page = w.browser.get(f"/forms/{w.smart_form_id}")
    assert "returned" in page, "returned status not visible to firm"
    return ("5 answers over the client surface; fact store updated;"
            " firm sees Returned for Review")


def step_review_returned_intake(w):
    _s, _u, page = w.browser.get(f"/forms/{w.smart_form_id}/review")
    assert "Client family name" in page
    assert "Anchor-Synthetic" in page, "client answer not in review"
    assert "300 Anchor Way" in page
    return "review screen shows the client's answers per question"


def step_render_g28(w):
    _s, _u, page = w.browser.get(f"/forms/{w.smart_form_id}")
    m = re.search(rf"/forms/{w.smart_form_id}/download/(\d+)", page)
    assert m is not None, "download link missing"
    content = w.browser.get_bytes(
        f"/forms/{w.smart_form_id}/download/{m.group(1)}")
    assert content[:5] == b"%PDF-", content[:16]
    import tempfile as tf
    with tf.TemporaryDirectory() as td:
        pdf = Path(td) / "g28.pdf"
        pdf.write_bytes(content)
        from pypdf import PdfReader
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fields = {k: (v.get("/V") or "")
                      for k, v in (PdfReader(pdf).get_fields()
                                   or {}).items()}
    assert fields.get(G28_CLIENT_FAMILY) == "Anchor-Synthetic", \
        fields.get(G28_CLIENT_FAMILY)
    assert fields.get(G28_CLIENT_GIVEN) == "Nova"
    return (f"G-28 downloaded ({len(content)} bytes); client-entered"
            f" family name and firm-entered given name both in the PDF")


def step_deadline_reminder(w):
    from datetime import datetime, timedelta, timezone
    starts = datetime.now(timezone.utc) + timedelta(days=7)
    _s, _u, page = w.browser.get(
        f"/calendar/new?matter={w.matter_id}&contact={w.contact_id}")
    assert "New deadline" in page
    _s, url, page = w.browser.post("/calendar/new", {
        "title": "Anchor filing deadline",
        "date": starts.strftime("%Y-%m-%d"), "time": "09:00",
        "matter_id": str(w.matter_id),
        "contact_id": str(w.contact_id), "reminder": "2|days"})
    m = re.search(r"/calendar/(\d+)$", url)
    assert m is not None, url
    w.event_id = int(m.group(1))
    assert "2 days before" in page, "reminder not visible"
    _s, _u, page = w.browser.get("/calendar")
    assert "Anchor filing deadline" in page
    _s, _u, page = w.browser.get(f"/matters/{w.matter_id}")
    assert "Anchor filing deadline" in page, "deadline not on matter"
    # machinery assertion (module-level allowed for asserts): the
    # reminder actually fires through the one dispatch path. Fire
    # time derives from the POSTED start (date at 09:00), not from
    # wall-clock now -- the old form was time-of-day dependent and
    # failed on any run before 09:00 UTC.
    from app import scheduler
    event_start = datetime.strptime(
        f"{starts.strftime('%Y-%m-%d')}T09:00:00Z",
        "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    fire = event_start - timedelta(days=2) + timedelta(minutes=1)
    scheduler.tick(w.conn, fire.strftime("%Y-%m-%dT%H:%M:%SZ"))
    n = w.conn.execute(
        "SELECT count(*) FROM email_outbox WHERE"
        " template='event_reminder' AND entity_id=?",
        (w.event_id,)).fetchone()[0]
    assert n == 1, f"reminder emails: {n}"
    return ("deadline created by click; visible on calendar, matter,"
            " and event detail; tick fires exactly one reminder")


def step_audit_chain(w):
    def first_id(where, params=()):
        row = w.conn.execute(
            f"SELECT id FROM audit_log WHERE {where} ORDER BY id"
            f" LIMIT 1", params).fetchone()
        return row["id"] if row else None

    chain = [
        ("contact (user)", first_id(
            "entity_type='contacts' AND action='insert'"
            " AND actor_type='user'")),
        ("matter (user)", first_id(
            "entity_type='matters' AND action='insert'")),
        ("smart form (user)", first_id(
            "entity_type='smart_forms' AND action='insert'")),
        ("invitation (user)", first_id(
            "entity_type='intake_invitations' AND action='insert'")),
        ("client fact write (contact)", first_id(
            "entity_type='facts' AND actor_type='contact'")),
        ("event (user)", first_id(
            "entity_type='events' AND action='insert'")),
    ]
    missing = [name for name, aid in chain if aid is None]
    assert not missing, f"audit rows missing: {missing}"
    ids = [aid for _, aid in chain]
    assert ids == sorted(ids), f"chain out of story order: {ids}"
    return f"6 legs present, story-ordered (audit ids {ids[0]}..{ids[-1]})"


def step_browse_sweep(w):
    """P2 browse sweep, three legs (screen review 2 findings made
    mechanical): (a) every index, detail, and search renders the
    SEEDED db; (b) REACHABILITY -- every seeded entity is reachable
    by clicks from the dashboard (link-graph BFS over rendered
    hrefs); (c) every surface renders its DESIGNED empty state on a
    fresh db. Files/tasks/notes have no create UI in scope, so their
    seeds ride casework modules -- setup, not assertion."""
    from app import files as cw_files
    from app import notes as cw_notes
    from app import tasks as cw_tasks
    now = _now()
    uid = w.conn.execute("SELECT id FROM users").fetchone()[0]
    storage = w.workdir / "storage"
    fid = cw_files.upload_file(
        w.conn, "browse-seed.txt", b"synthetic browse seed", now,
        storage, matter_id=w.matter_id, user_id=uid)
    tid = cw_tasks.create_task(w.conn, "Browse seed task", now, uid,
                               matter_id=w.matter_id,
                               due_date="2026-09-01")
    nid = cw_notes.create_note(w.conn, "Synthetic browse note body.",
                               now, uid, title="Browse seed note",
                               matter_id=w.matter_id)
    w.conn.commit()

    # leg (a): seeded rendering -- indexes, details, search, settings
    checks = [
        ("/contacts", "Nova"),
        ("/matters", "Anchor Synthetic G-28 Matter"),
        ("/files", "browse-seed.txt"),
        ("/tasks", "Browse seed task"),
        ("/notes", "Browse seed note"),
        ("/settings", ADMIN["email"]),
        (f"/files/{fid}", "browse-seed.txt"),
        (f"/tasks/{tid}", "Browse seed task"),
        (f"/notes/{nid}", "Synthetic browse note body."),
    ]
    for path, needle in checks:
        _s, _u, page = w.browser.get(path)
        assert needle in page, f"{path}: {needle!r} not rendered"
    content = w.browser.get_bytes(f"/files/{fid}/download")
    assert content == b"synthetic browse seed", content[:32]
    _s, _u, page = w.browser.get("/search?q=Nova")
    assert f"/contacts/{w.contact_id}" in page, "search miss: contact"
    _s, _u, page = w.browser.get("/search?q=Anchor+Synthetic+G-28")
    assert f"/matters/{w.matter_id}" in page, "search miss: matter"
    _s, _u, page = w.browser.get("/search?q=zzz-no-such-record")
    assert "hint empty" in page, "zero-result state not designed"

    # leg (b): reachability BFS from the dashboard over hrefs
    targets = {f"/contacts/{w.contact_id}", f"/matters/{w.matter_id}",
               f"/forms/{w.smart_form_id}", f"/calendar/{w.event_id}",
               f"/files/{fid}", f"/tasks/{tid}", f"/notes/{nid}"}
    seen = set()
    queue = ["/"]
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        if "/download" in path:
            continue  # reached; binary, no links to harvest
        _s, _u, page = w.browser.get(path)
        for href in re.findall(r"href='([^']+)'", page):
            if href.startswith("/") and href not in seen:
                queue.append(href)
    missing = targets - seen
    assert not missing, f"unreachable by clicks from /: {sorted(missing)}"

    # leg (c): designed empty states on a fresh db
    empty = ui_server.make_server(w.workdir / "empty.db")
    ethread = threading.Thread(target=empty.serve_forever, daemon=True)
    ethread.start()
    try:
        eb = Browser(f"http://{empty.server_address[0]}:"
                     f"{empty.server_address[1]}")
        eb.post("/setup", {"name": "Empty Synthetic Admin",
                           "email": "empty.admin@synthetic.test",
                           "password": "empty-synthetic-pass"})
        _s, _u, page = eb.post("/enroll-mfa", {})
        m = CODE_RE.search(page)
        assert m is not None, "empty-db MFA code not shown"
        _s, url, page = eb.post("/mfa", {"code": m.group(1)})
        assert url.endswith("/"), url
        for path in ("/contacts", "/matters", "/files", "/tasks",
                     "/notes", "/calendar", "/search"):
            _s, _u, page = eb.get(path)
            assert "hint empty" in page, f"{path}: empty state missing"
            if path != "/search":
                assert "<td>" not in page, f"{path}: rows on fresh db"
        _s, _u, page = eb.get("/settings")
        assert "hint empty" in page, "/settings: empty state missing"
    finally:
        empty.client_httpd.server_close()
        empty.shutdown()
        empty.server_close()
        empty.app_conn.close()
    return (f"seeded render 12 checks; BFS reached {len(seen)} pages,"
            f" all {len(targets)} entities clickable from /; empty"
            f" states designed on a fresh db")


STEPS = [
    ("first-run setup", step_first_run_setup),
    ("MFA enrollment", step_mfa_enrollment),
    ("login round-trip", step_login_roundtrip),
    ("auth gate", step_auth_gate),
    ("create contact", step_create_contact),
    ("create matter", step_create_matter),
    ("form package + invitation", step_forms_invitation),
    ("client intake leg", step_client_intake_leg),
    ("review returned intake", step_review_returned_intake),
    ("G-28 render + download", step_render_g28),
    ("deadline + reminder visible", step_deadline_reminder),
    ("audit chain", step_audit_chain),
    ("browse sweep", step_browse_sweep),
]


def main():
    lines = ["# ui-walk-report -- verifier 1 (scripted UI walk)", ""]
    counts = {"PASS": 0, "PENDING": 0, "FAIL": 0}
    total = 0.0
    with tempfile.TemporaryDirectory() as td:
        w = Walk(td)
        lines.append(f"run started: {_now()}")
        lines.append("")
        w.httpd = ui_server.make_server(w.workdir / "walk.db")
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
                lines.append(f"{status:7s} {name:30s} {elapsed:7.3f}s"
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
    sweeps_ok = True
    for name, ok, detail in sweeps.run_all():
        sweeps_ok = sweeps_ok and ok
        lines.append(f"{'PASS' if ok else 'FAIL':4s} {name}: {detail}")
    lines.append("")
    lines.append(f"steps: {counts['PASS']} pass, {counts['PENDING']}"
                 f" pending, {counts['FAIL']} fail; total {total:.3f}s")
    green = counts["FAIL"] == 0 and counts["PENDING"] == 0 and sweeps_ok
    ok_now = counts["FAIL"] == 0 and sweeps_ok
    verdict = "GREEN" if green else ("ON TRACK (pending screens)"
                                     if ok_now else "FAIL")
    lines.append(f"verdict: {verdict}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8",
                      newline="\n")
    print(f"ui-walk: {counts['PASS']} pass, {counts['PENDING']} pending,"
          f" {counts['FAIL']} fail; sweeps"
          f" {'pass' if sweeps_ok else 'FAIL'}; verdict {verdict}")
    print(f"report: {REPORT}")
    return 0 if green else 1


if __name__ == "__main__":
    sys.exit(main())
