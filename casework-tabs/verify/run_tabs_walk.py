"""Verifier 1: the per-tab walk rail (goal.md, ratified 2026-08-10).

Oracle-first (goal-method op rule 7, billing-ui precedent): every
tab's core flows are enumerated HERE before the screens exist, and
the route names, form fields, and page markers this file drives ARE
the interface contract for P1-P6. Each phase extends its tab's steps
(plan.md per-phase rhythm step 1) and drives them RED once on
purpose before trusting them (verify-the-verifier).

Two Pending probes, because the six tab routes already exist as
read-only casework-ui screens:
- probe(): authed GET landing on the app_ui 404 page -> the NEW
  route is unbuilt (e.g. /calendar/new-appointment, /settings/users).
- expect_marker(): the route exists today but the ruled redesign has
  not landed; a missing contract marker raises Pending, never FAIL.
  Markers are ADDITIVE -- the frozen run_ui_walk.py assertions about
  these pages must stay true (existing-screen changes are gate
  decisions, goal.md).

Expected at P0 close: setup/auth, empty-state sweep pending, and
contact/matter steps green (existing screens), every tab step
PENDING, exit 1, verdict ON TRACK.

The walk drives the UI exactly as a browser would -- GETs, form
POSTs (urlencoded + multipart), cookies, redirects. Module/db access
is for ASSERTIONS only; walk content is created via the walked
screens themselves. [Q] P1 gate: expiry, vmax, and invoice-due
calendar rows have no UI creation path today (facts come from
intake; billing UI reads due_date but never writes it) -- the
derived-kinds step probes markers only until that ruling.

Goal.md supporting checks live here: float sweep + ISO-stray sweep
ride the report's sweep section; the empty-state sweep is walk step
2 (fresh-db crawl of the list tabs).

Run: python verify/run_tabs_walk.py
Writes tabs-walk-report.txt beside it; the ONLY valid report sha is
python verify/report_sha.py.
"""

import hashlib
import http.cookiejar
import io
import json
import re
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS = HERE.parent.parent
CASEWORK_UI = ATLAS / "casework-ui"
sys.path.insert(0, str(CASEWORK_UI))

import app_ui  # noqa: F401, E402  (wires casework onto sys.path)
from app_ui import server as ui_server  # noqa: E402

REPORT = HERE / "tabs-walk-report.txt"

ADMIN = {"name": "Tabs Walk Admin",
         "email": "tabs.walk@synthetic.test",
         "password": "tabs-walk-pass"}

CODE_RE = re.compile(r"verification code is (\d{6})")
ISO_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
STYLE_RE = re.compile(r"<style>.*?</style>", re.S)
TAG_RE = re.compile(r"<[^>]*>")

# The six calendar kinds (Appendix A: unified date view). Rows carry
# class='kind-<kind>'; the filter is ?kind=<kind>. Visual vocabulary
# (colors/chips) is gate material; these class hooks are mechanical.
KINDS = ("appointment", "deadline", "expiry", "task", "vmax",
         "invoice")

FOUNDATION_STEPS = 3  # pages of later steps feed the ISO-stray sweep


class Pending(Exception):
    """Screen or marker not built yet -- expected before its phase."""


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Browser:
    """Cookie-carrying HTTP client; follows redirects; 404 is a
    return value (the Pending probe), never an exception. Every HTML
    page fetched is captured with the current step index for the
    ISO-stray sweep."""

    def __init__(self, base, page_log=None):
        self.base = base
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar))
        self.page_log = page_log if page_log is not None else []
        self.step_index = -1

    def _open(self, req):
        try:
            with self.opener.open(req, timeout=10) as r:
                status, url = r.status, r.geturl()
                page = r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            status, url = e.code, e.geturl()
            page = e.read().decode("utf-8")
        self.page_log.append((self.step_index, url, page))
        return status, url, page

    def get(self, path):
        return self._open(urllib.request.Request(self.base + path))

    def post(self, path, data):
        body = urllib.parse.urlencode(data, doseq=True).encode("utf-8")
        req = urllib.request.Request(self.base + path, data=body,
                                     method="POST")
        req.add_header("Content-Type",
                       "application/x-www-form-urlencoded")
        return self._open(req)

    def post_multipart(self, path, fields, filefield, filename,
                       content):
        boundary = "SYNTHBOUNDARY7d9f2c"
        parts = []
        for k, v in fields.items():
            parts.append(f"--{boundary}\r\nContent-Disposition:"
                         f" form-data; name=\"{k}\"\r\n\r\n{v}\r\n"
                         .encode("utf-8"))
        parts.append(
            (f"--{boundary}\r\nContent-Disposition: form-data;"
             f" name=\"{filefield}\"; filename=\"{filename}\"\r\n"
             f"Content-Type: application/octet-stream\r\n\r\n")
            .encode("utf-8") + content + b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode("utf-8"))
        body = b"".join(parts)
        req = urllib.request.Request(self.base + path, data=body,
                                     method="POST")
        req.add_header("Content-Type",
                       f"multipart/form-data; boundary={boundary}")
        return self._open(req)

    def get_bytes(self, path):
        with self.opener.open(self.base + path, timeout=10) as r:
            return r.read()


def probe(w, path):
    """GET path; raise Pending on the 404 page (route unbuilt)."""
    status, _url, page = w.browser.get(path)
    if status == 404:
        raise Pending(f"{path} not built")
    assert status == 200, f"{path}: HTTP {status}"
    return page


def expect_marker(page, marker, what):
    """The route exists but the ruled redesign has not landed yet."""
    if marker not in page:
        raise Pending(f"{what} not built (marker {marker!r} absent)")
    return page


def need(value, what):
    """A step whose input never got created (upstream screen still
    unbuilt) is pending, not failed."""
    if value is None:
        raise Pending(f"upstream not walked yet ({what})")
    return value


# Minimal valid single-page PDF, for upload/e-sign candidates.
def tiny_pdf(text):
    objs = ["<</Type /Catalog /Pages 2 0 R>>",
            "<</Type /Pages /Kids [3 0 R] /Count 1>>",
            "<</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]"
            " /Contents 4 0 R /Resources <</Font <</F1 5 0 R>>>>>>",
            None,
            "<</Type /Font /Subtype /Type1 /BaseFont /Helvetica>>"]
    stream = (f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET").encode()
    objs[3] = (f"<</Length {len(stream)}>>\nstream\n".encode()
               + stream + b"\nendstream")
    out = b"%PDF-1.4\n"
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        body = o if isinstance(o, bytes) else o.encode()
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<</Size {len(objs) + 1} /Root 1 0 R>>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    return out


class Walk:
    def __init__(self, workdir):
        self.workdir = Path(workdir)
        self.httpd = None
        self.conn = None
        self.browser = None
        self.contact_id = None
        self.matter_id = None
        self.appt_id = None
        self.deadline_made = None
        self.task_id = None
        self.done_task_id = None
        self.list_id = None
        self.category_id = None
        self.quick_note_id = None
        self.full_note_id = None
        self.file_id = None
        self.file2_id = None
        self.esign_file_id = None
        self.signer_id = None
        self.signer_token = None
        self.invited_uid = None


# --- foundation (existing casework-ui screens; green today) ---

def step_setup_login(w):
    _s, url, page = w.browser.get("/")
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


def step_empty_states(w):
    """Goal.md empty-state sweep, run on the FRESH db before any
    content exists: each list tab renders a DESIGNED empty state --
    <div class='empty-state'> stating what will appear and carrying
    the action (a link or form) that creates it. Old bare 'hint
    empty' paragraphs do not satisfy the bar."""
    missing, bare = [], []
    for path in ("/calendar", "/files", "/tasks", "/notes"):
        _s, _u, page = w.browser.get(path)
        m = re.search(r"<div class='empty-state'>(.*?)</div>", page,
                      re.S)
        if m is None:
            missing.append(path)
        elif "<a " not in m.group(1) and "<form" not in m.group(1):
            bare.append(path)
    assert not bare, f"empty state without its creating action: {bare}"
    if missing:
        raise Pending(f"designed empty states absent: {missing}")
    return "all list tabs show designed empty states with actions"


def step_client_matter(w):
    _s, url, page = w.browser.post("/contacts/new", {
        "given_name": "Talia", "family_name": "Synthetic",
        "email": "talia.client@synthetic.test",
        "phone": "+1-555-0500"})
    m = re.search(r"/contacts/(\d+)$", url)
    assert m is not None, url
    w.contact_id = int(m.group(1))
    _s, url, page = w.browser.post("/matters/new", {
        "name": "Talia Synthetic I-130",
        "contact_id": str(w.contact_id), "description": "tabs walk"})
    m = re.search(r"/matters/(\d+)$", url)
    assert m is not None, url
    w.matter_id = int(m.group(1))
    return (f"contact {w.contact_id} + matter {w.matter_id} via"
            f" existing screens")


# --- P1 calendar (Appendix A: unified view, two create paths) ---

def step_cal_new_appointment(w):
    page = probe(w, "/calendar/new-appointment")
    for field in ("title", "date", "start_time", "end_time",
                  "description"):
        assert f"name='{field}'" in page, \
            f"appointment form missing {field}"
    _s, url, page = w.browser.post("/calendar/new-appointment", {
        "title": "SYNTH USCIS interview prep",
        "date": "2026-08-20", "start_time": "10:00",
        "end_time": "11:00",
        "description": "SYNTH prep session",
        "contact_id": str(w.contact_id),
        "matter_id": str(w.matter_id)})
    m = re.search(r"/calendar/(\d+)$", url)
    assert m is not None, f"appointment create landed on {url}"
    w.appt_id = int(m.group(1))
    assert "08/20/2026" in page, "appointment date not MM/DD/YYYY"
    assert "11:00" in page, "end time not rendered"
    assert "ttendee" in page, "attendees UI missing from detail"
    return f"appointment {w.appt_id} by click; MM/DD/YYYY; end time"


def step_cal_new_deadline(w):
    page = probe(w, "/calendar/new-deadline")
    for field in ("title", "date"):
        assert f"name='{field}'" in page, \
            f"deadline form missing {field}"
    _s, _u, page = w.browser.post("/calendar/new-deadline", {
        "title": "SYNTH I-130 filing deadline",
        "date": "2026-08-28",
        "contact_id": str(w.contact_id),
        "matter_id": str(w.matter_id)})
    assert "SYNTH I-130 filing deadline" in page
    assert "08/28/2026" in page, "deadline date not MM/DD/YYYY"
    w.deadline_made = True
    return "deadline created via its lean pre-shaped form"


def step_cal_unified(w):
    # rendered-badge markers ("class='kind kind-X'"), never the bare
    # kind-X word -- that also lives in the global stylesheet (P1
    # false-PASS finding, worklog s3)
    need(w.appt_id, "appointment")
    need(w.deadline_made, "deadline")
    _s, _u, page = w.browser.get("/calendar")
    expect_marker(page, "class='kind kind-appointment'",
                  "unified calendar rows")
    assert "class='kind kind-deadline'" in page, \
        "deadline row missing its kind"
    assert "SYNTH USCIS interview prep" in page
    assert "SYNTH I-130 filing deadline" in page
    for kind in KINDS:
        assert f"kind={kind}" in page, f"kind filter {kind} missing"
    _s, _u, page = w.browser.get("/calendar?kind=appointment")
    assert "SYNTH USCIS interview prep" in page
    assert "SYNTH I-130 filing deadline" not in page, \
        "kind filter did not narrow to appointments"
    return "unified view: both kinds rendered; single-kind filter"


def step_cal_toggle(w):
    # the marker is the RENDERED grid table's class attribute -- the
    # bare word month-grid also lives in the global stylesheet
    grid = "class='data month-grid'"
    need(w.appt_id, "appointment")
    _s, _u, page = w.browser.get("/calendar")
    expect_marker(page, "view=month", "agenda/month toggle")
    assert "view=agenda" in page, "toggle missing agenda button"
    _s, _u, page = w.browser.get("/calendar?view=month")
    assert grid in page, "month grid not rendered"
    _s, _u, page = w.browser.get("/calendar")
    assert grid in page, \
        "view choice not sticky per user (agenda came back)"
    _s, _u, page = w.browser.get("/calendar?view=agenda")
    assert grid not in page, "agenda did not return"
    return "two-button toggle; month grid; sticky per user"


def step_cal_derived_kinds(w):
    """[Q] P1 gate: expiry, vmax, and invoice-due rows have no UI
    creation path today (facts come from intake; billing UI never
    writes due_date). Until that ruling this step probes the kind
    markers only; the ruling decides how a UI-only walk gets this
    content (mirror the intake flow / a deadline-form fact variant /
    a gate-ruled seeding exemption)."""
    need(w.appt_id, "appointment")
    _s, _u, page = w.browser.get("/calendar")
    expect_marker(page, "class='kind kind-expiry'",
                  "derived calendar kinds")
    assert "class='kind kind-vmax'" in page \
        or "kind=vmax" in page
    assert "class='kind kind-invoice'" in page \
        or "kind=invoice" in page
    return "derived kinds present ([Q] content path rules at gate)"


def step_cal_provenance(w):
    need(w.deadline_made, "deadline")
    _s, _u, page = w.browser.get("/calendar")
    expect_marker(page, "class='provenance'",
                  "provenance on derived rows")
    row = re.search(r"<[^>]*kind-deadline.*?SYNTH I-130 filing"
                    r" deadline.*?</tr>", page, re.S)
    if row is None:  # agenda rows may not be table rows; fall back
        row = re.search(r"kind-deadline.*?filing deadline.*?(?=kind-|"
                        r"</div>)", page, re.S)
    assert row is not None, "deadline row not found for provenance"
    assert f"/matters/{w.matter_id}" in row.group(0), \
        "deadline row does not link its source matter"
    return "derived rows carry provenance links to their source"


# --- P2 tasks (Appendix A: my-open first, quick-add, one-click) ---

def step_tasks_quick_add(w):
    """[Q] P2 gate: the frozen core has NO due-date setter --
    tasks.create_task takes due_date at creation only, and nothing
    updates it. Rendering-only forbids an UPDATE from app_ui, so the
    quick-add form carries an OPTIONAL due date instead of the
    set-due-later route this step first sketched (/tasks/<id>/due,
    refined 2026-08-10 s4); editing an existing task's due date
    would need a core amendment -- the gate rules whether to seek
    one."""
    _s, _u, page = w.browser.get("/tasks")
    expect_marker(page, "action='/tasks/quick'", "type-and-Enter"
                  " quick-add")
    assert "name='due_date'" in page, \
        "quick-add missing its optional due date"
    _s, _u, page = w.browser.post("/tasks/quick", {
        "title": "SYNTH draft I-130 cover letter",
        "due_date": "2026-08-25"})
    assert "SYNTH draft I-130 cover letter" in page, \
        "quick-added task not visible after Enter"
    assert "08/25/2026" in page, "due date not MM/DD/YYYY"
    row = w.conn.execute(
        "SELECT id, due_date FROM tasks WHERE title=?",
        ("SYNTH draft I-130 cover letter",)).fetchone()
    assert row is not None
    assert row["due_date"] == "2026-08-25", \
        f"stored due date not ISO: {row['due_date']!r}"
    w.task_id = row["id"]
    _s, _u, page = w.browser.get("/calendar")
    assert "class='kind kind-task'" in page \
        and "SYNTH draft I-130" in page, \
        "task due date missing from the unified calendar"
    return "quick-add by Enter (due rides the form); on the calendar"


def step_tasks_my_open(w):
    need(w.task_id, "quick-added task")
    _s, _u, page = w.browser.get("/tasks")
    expect_marker(page, "scope=firm", "my-open default + firm toggle")
    assert "done=1" in page, "completed filter link missing"
    assert "SYNTH draft I-130 cover letter" in page, \
        "my open task missing from the default view"
    _s, _u, page = w.browser.get("/tasks?scope=firm")
    assert "SYNTH draft I-130 cover letter" in page
    return "index opens on MY OPEN; firm + completed one click away"


def step_tasks_complete(w):
    """P2 gate r2 (James) SUPERSEDES Appendix A's 'one-click
    complete': a stray click dismissed a task at his live drive, so
    completing is now two actions -- check the row's box, then Done
    (native required checkbox, zero JS; the browser refuses the
    bare submit). The rail's direct POST bypasses client-side
    validation by nature, so the guard is pinned as markup."""
    need(w.task_id, "quick-added task")
    _s, _u, page = w.browser.post("/tasks/quick", {
        "title": "SYNTH check receipt notice"})
    row = w.conn.execute("SELECT id FROM tasks WHERE title=?",
                         ("SYNTH check receipt notice",)).fetchone()
    w.done_task_id = row["id"]
    _s, _u, page = w.browser.get("/tasks")
    expect_marker(page, f"action='/tasks/{w.done_task_id}/complete'",
                  "complete on rows")
    assert "<input type='checkbox' required" in page, \
        "complete lacks its confirm checkbox (stray-click guard)"
    _s, _u, page = w.browser.post(
        f"/tasks/{w.done_task_id}/complete", {})
    assert "SYNTH check receipt notice" not in page, \
        "completed task still in the open view"
    _s, _u, page = w.browser.get("/tasks?done=1")
    assert "SYNTH check receipt notice" in page, \
        "completed task missing under the completed filter"
    # Reopen = the undo (program amendment 2026-08-10: the ONE
    # authorized post-freeze core addition, tasks.reopen_task)
    expect_marker(page, f"action='/tasks/{w.done_task_id}/reopen'",
                  "Reopen on completed rows")
    _s, _u, page = w.browser.post(
        f"/tasks/{w.done_task_id}/reopen", {})
    assert "SYNTH check receipt notice" in page, \
        "reopened task not back in the open view"
    row = w.conn.execute("SELECT completed_at FROM tasks WHERE id=?",
                         (w.done_task_id,)).fetchone()
    assert row["completed_at"] is None, \
        "reopen did not clear completed_at in the core"
    audit = w.conn.execute(
        "SELECT count(*) FROM audit_log WHERE entity_type='tasks'"
        " AND action='update' AND entity_id=?",
        (w.done_task_id,)).fetchone()[0]
    assert audit >= 2, f"complete+reopen audit rows: {audit}"
    return ("check-then-Done from the row; completed view; Reopen"
            " undoes, audited")


def step_tasks_lists(w):
    """Refined 2026-08-10 s4 (verify-the-verifier): the old closing
    assert -- list NAME visible on the matter page as 'automation
    linkage' -- was vacuous: the Import Task List select renders
    every list's name, so it passed with zero linkage rendered. And
    the tasks table stores no source-list column, so a task CANNOT
    name its list post-import (schema truth). Automation linkage per
    the schema is matter_statuses.auto_task_list_id -> the BUILDER
    shows which statuses auto-import each list; no UI creates
    workflows (config-depth kill), so the rail can only probe the
    column marker -- content renders on the seeded demo db at the
    gate. [Q] P2 gate."""
    page = probe(w, "/settings/task-lists")
    _s, _u, page = w.browser.post("/settings/task-lists", {
        "name": "SYNTH I-130 checklist"})
    assert "SYNTH I-130 checklist" in page
    row = w.conn.execute("SELECT id FROM task_lists WHERE name=?",
                         ("SYNTH I-130 checklist",)).fetchone()
    w.list_id = row["id"]
    _s, _u, page = w.browser.post(
        f"/settings/task-lists/{w.list_id}/items", {
            "title": "SYNTH gather civil documents", "position": "1",
            "duration_days": "7"})
    _s, _u, page = w.browser.post(
        f"/settings/task-lists/{w.list_id}/items", {
            "title": "SYNTH file before EAD expiry", "position": "2",
            "ref_fact_key": "imm.ead_expiry",
            "ref_direction": "before", "ref_days": "30"})
    assert "SYNTH gather civil documents" in page
    # the FULL rule phrase, label included -- a bare "EAD" assert was
    # vacuous (the item title contains it; RED drive s4 caught the
    # rail passing with the raw fact key rendered)
    assert "due 30 days before EAD expiry" in page, \
        "reference rule not written out (label + direction + days)"
    assert "due 7 days after import" in page, \
        "duration rule not written out"
    _s, _u, page = w.browser.get("/settings/task-lists")
    expect_marker(page, "class='automations'",
                  "automation linkage on the builder")
    _s, _u, page = w.browser.get(f"/matters/{w.matter_id}")
    expect_marker(page, "import-task-list", "Import Task List on the"
                  " matter page")
    _s, _u, page = w.browser.post(
        f"/matters/{w.matter_id}/import-task-list", {
            "task_list_id": str(w.list_id)})
    assert "SYNTH gather civil documents" in page, \
        "imported task missing from the matter page"
    assert "SYNTH file before EAD expiry" in page, \
        "second imported task missing from the matter page"
    ref = w.conn.execute(
        "SELECT due_date FROM tasks WHERE title=?",
        ("SYNTH file before EAD expiry",)).fetchone()
    assert ref is not None and ref["due_date"] is None, \
        "missing reference fact must yield no due date, not a guess"
    return "list built in its Settings home; imported onto matter"


# --- P3 notes (Appendix A: minimal capture, timeline, pins) ---

def step_notes_categories(w):
    page = probe(w, "/settings/note-categories")
    _s, _u, page = w.browser.post("/settings/note-categories", {
        "name": "SYNTH Strategy"})
    assert "SYNTH Strategy" in page
    row = w.conn.execute(
        "SELECT id FROM note_categories WHERE name=?",
        ("SYNTH Strategy",)).fetchone()
    assert row is not None
    w.category_id = row["id"]
    return "note categories managed in their Settings home"


def step_notes_capture(w):
    _s, _u, page = w.browser.get("/notes")
    expect_marker(page, "action='/notes/quick'", "minimal capture")
    _s, _u, page = w.browser.post("/notes/quick", {
        "body": "SYNTH quick observation about the I-130 filing."})
    assert "SYNTH quick observation" in page
    row = w.conn.execute(
        "SELECT id FROM notes WHERE body LIKE 'SYNTH quick%'"
    ).fetchone()
    w.quick_note_id = row["id"]
    page = probe(w, "/notes/new")
    for field in ("title", "body", "category_id", "notify_all"):
        assert f"name='{field}'" in page, \
            f"expanded form missing {field}"
    _s, _u, page = w.browser.post("/notes/new", {
        "title": "SYNTH strategy memo",
        "body": "SYNTH consular processing is the faster route.",
        "category_id": str(need(w.category_id, "note category")),
        "matter_id": str(w.matter_id)})
    assert "SYNTH strategy memo" in page
    row = w.conn.execute("SELECT id FROM notes WHERE title=?",
                         ("SYNTH strategy memo",)).fetchone()
    w.full_note_id = row["id"]
    return "quick capture = body + save; expanded form for the rest"


def step_notes_timeline_pin(w):
    """Refined 2026-08-10 s5 (verify-the-verifier, the P2 sabotage-4
    lesson applied up front): the P0 check only found the memo
    SOMEWHERE in the timeline -- true before the pin too, so a
    broken pin passed. A second, newer matter note makes ordering
    observable: newest-first before the pin, and pinning the OLDER
    memo must lift it above the newer entry."""
    need(w.full_note_id, "expanded note")
    _s, _u, page = w.browser.post("/notes/new", {
        "title": "SYNTH later filing note",
        "body": "SYNTH RFE response window opens next week.",
        "matter_id": str(w.matter_id)})
    _s, _u, page = w.browser.get(f"/matters/{w.matter_id}")
    expect_marker(page, "notes-timeline", "matter Notes timeline")
    tl = page[page.find("notes-timeline"):]
    memo = tl.find("SYNTH strategy memo")
    later = tl.find("SYNTH later filing note")
    assert memo >= 0, "memo missing from the timeline"
    assert 0 <= later < memo, \
        "timeline not newest-first before the pin"
    _s, _u, page = w.browser.post(
        f"/notes/{w.full_note_id}/pin", {})
    _s, _u, page = w.browser.get(f"/matters/{w.matter_id}")
    tl = page[page.find("notes-timeline"):]
    memo = tl.find("SYNTH strategy memo")
    later = tl.find("SYNTH later filing note")
    assert 0 <= memo < later, "pinned note not lifted to the top"
    row = w.conn.execute("SELECT pinned FROM notes WHERE id=?",
                         (w.full_note_id,)).fetchone()
    assert row["pinned"] == 1, "pin did not reach the core"
    return "timeline newest-first; pinning the older memo lifts it"


def step_notes_index_filters(w):
    need(w.full_note_id, "expanded note")
    need(w.quick_note_id, "quick note")
    _s, _u, page = w.browser.get("/notes")
    expect_marker(page, "mine=1", "index filter chips")
    assert f"category={w.category_id}" in page, \
        "category filter chip missing"
    pinned = page.find("SYNTH strategy memo")
    quick = page.find("SYNTH quick observation")
    assert 0 <= pinned < quick, \
        "pinned note not first in the ALL-notes default"
    _s, _u, page = w.browser.get(
        f"/notes?category={w.category_id}")
    assert "SYNTH strategy memo" in page
    assert "SYNTH quick observation" not in page, \
        "category filter did not narrow"
    return "defaults ALL + pinned first; category + mine chips work"


def step_notes_export(w):
    need(w.full_note_id, "expanded note")
    _s, _u, page = w.browser.get(f"/matters/{w.matter_id}")
    expect_marker(page, f"/matters/{w.matter_id}/notes.pdf",
                  "PDF export on the matter section")
    content = w.browser.get_bytes(f"/matters/{w.matter_id}/notes.pdf")
    assert content[:5] == b"%PDF-", content[:16]
    # gate r2 (James): the export must also be reachable from the
    # individual note's page, scoped to its linkage
    _s, _u, page = w.browser.get(f"/notes/{w.full_note_id}")
    assert f"/matters/{w.matter_id}/notes.pdf" in page, \
        "note page missing its linkage-scoped export"
    return f"notes PDF exported ({len(content)} bytes); on note page"


# --- P4 files (Appendix A: matter-centric, custody, e-sign) ---

def step_files_upload(w):
    """Refined 2026-08-10 s6 (verify-the-verifier): the custody
    assert was a page-wide 'firm' -- vacuous the moment any page
    carries href='/settings/firm' (P6 adds it). Pinned as the
    rendered kv pair instead (the detail page renders it today);
    the db custody assert pins source='firm' (schema CHECK:
    firm|client|produced)."""
    _s, _u, page = w.browser.get("/files")
    expect_marker(page, "action='/files/upload'", "upload from the"
                  " files tab")
    content = b"SYNTH civil document scan (walk).\n"
    _s, _u, page = w.browser.post_multipart(
        "/files/upload", {"matter_id": str(w.matter_id)},
        "file", "SYNTH-civil-documents.txt", content)
    assert "SYNTH-civil-documents.txt" in page
    row = w.conn.execute(
        "SELECT id, sha256, source FROM files WHERE name=?",
        ("SYNTH-civil-documents.txt",)).fetchone()
    assert row is not None
    w.file_id = row["id"]
    sha = hashlib.sha256(content).hexdigest()
    assert row["sha256"] == sha, "stored sha mismatch"
    assert row["source"] == "firm", f"source: {row['source']!r}"
    _s, _u, page = w.browser.get(f"/files/{w.file_id}")
    assert sha in page, "custody: sha256 not visible on the file"
    assert "<dt>Source</dt><dd>firm</dd>" in page, \
        "custody: source not rendered in the detail kv"
    return "upload by click; custody (source + sha256) visible"


def step_files_matter_index(w):
    """Refined s6: the matter-page assert searches INSIDE the
    files-section slice (the P3 timeline pattern) -- a page-wide
    find could pass from any other widget naming the file."""
    need(w.file_id, "uploaded file")
    _s, _u, page = w.browser.get(f"/matters/{w.matter_id}")
    expect_marker(page, "files-section", "matter Files section")
    sect = page[page.find("files-section"):]
    assert "SYNTH-civil-documents.txt" in sect, \
        "matter Files section missing its file"
    pdf = tiny_pdf("SYNTH G-28 candidate")
    _s, _u, page = w.browser.post_multipart(
        "/files/upload", {"contact_id": str(w.contact_id)},
        "file", "SYNTH-g28-candidate.pdf", pdf)
    row = w.conn.execute("SELECT id FROM files WHERE name=?",
                         ("SYNTH-g28-candidate.pdf",)).fetchone()
    w.file2_id = row["id"]
    _s, _u, page = w.browser.get("/files")
    for name in ("matter_id", "contact_id", "source",
                 "esign_status"):
        assert f"name='{name}'" in page, \
            f"firm index missing the {name} filter"
    _s, _u, page = w.browser.get(
        f"/files?matter_id={w.matter_id}")
    assert "SYNTH-civil-documents.txt" in page
    assert "SYNTH-g28-candidate.pdf" not in page, \
        "matter filter did not narrow the firm index"
    return "matter-centric section + firm-wide index with filters"


def step_files_manage(w):
    """Refined s6 (pending-vs-fail): the old step POSTed rename and
    fetched preview bytes BEFORE any marker probe, so an unbuilt
    manage surface read FAIL, not PENDING (get_bytes raises through).
    The controls' home is pinned first: rename form + preview/print
    links live on the file detail page. The bulk zip is now OPENED
    and its entries asserted -- the bare PK magic passed any zip."""
    need(w.file_id, "uploaded file")
    need(w.file2_id, "PDF candidate")
    # P4b gate r1 (James): preview and print view were identical by
    # construction (zero-JS: both serve the same bytes inline), so
    # the detail carries ONE Preview control; printing is the
    # browser's print from that tab. The print asserts left with
    # the second button.
    _s, _u, page = w.browser.get(f"/files/{w.file_id}")
    expect_marker(page, f"action='/files/{w.file_id}/rename'",
                  "rename on the file detail")
    assert f"/files/{w.file_id}/preview" in page, \
        "preview control missing from the detail page"
    _s, _u, page = w.browser.post(f"/files/{w.file_id}/rename", {
        "name": "SYNTH-civil-documents-v2.txt"})
    assert "SYNTH-civil-documents-v2.txt" in page, "rename not shown"
    _s, _u, page = w.browser.get("/files")
    assert "SYNTH-civil-documents-v2.txt" in page
    assert "SYNTH-civil-documents.txt" not in page, \
        "old name still listed after rename"
    content = w.browser.get_bytes(f"/files/{w.file_id}/preview")
    assert b"SYNTH civil document scan" in content, "preview empty"
    _s, _u, page = w.browser.get("/files")
    expect_marker(page, "bulk-download", "bulk download control")
    blob = w.browser.get_bytes(
        f"/files/bulk-download?file_id={w.file_id}"
        f"&file_id={w.file2_id}")
    z = zipfile.ZipFile(io.BytesIO(blob))
    names = set(z.namelist())
    assert names == {"SYNTH-civil-documents-v2.txt",
                     "SYNTH-g28-candidate.pdf"}, \
        f"zip entries: {sorted(names)}"
    assert b"SYNTH civil document scan" in z.read(
        "SYNTH-civil-documents-v2.txt"), "zip content wrong"
    return "rename, preview (= print tab), bulk zip -- all by click"


def step_files_esign_prepare(w):
    """Refined 2026-08-10 s6 against the frozen core (discovery,
    never invention). esign.prepare WRITES a draft row, so the prep
    editor is entered by POST from the PDF's detail page -- a
    writing GET is not a route this surface may grow. Only PDFs can
    be prepared (core rule), so the txt file's detail must NOT offer
    the control -- offering it would 400 at James's live drive. And
    the request email is schema truth: the frozen core mails the
    RELATIVE path /esign/<token> (esign.request_signatures), so the
    old step's scrape of the outbox for an absolute URL could NEVER
    pass -- the live absolute link is the staff page's job
    (client_base, the intake-invite precedent), asserted in the
    sign step."""
    need(w.file2_id, "PDF candidate")
    need(w.file_id, "txt file (the non-PDF arm)")
    _s, _u, page = w.browser.get(f"/files/{w.file2_id}")
    expect_marker(page,
                  f"action='/files/{w.file2_id}/esign/prepare'",
                  "Prepare-for-e-sign on the PDF detail")
    _s, _u, other = w.browser.get(f"/files/{w.file_id}")
    assert f"action='/files/{w.file_id}/esign/prepare'" not in other, \
        "non-PDF detail offers e-sign prepare (core will refuse)"
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/prepare", {})
    for act in ("esign/signers", "esign/fields"):
        assert f"action='/files/{w.file2_id}/{act}'" in page, \
            f"prep editor missing its {act} form"
    # gate r5 (James's drive): Send with ZERO signers locked the
    # file with nobody to sign and no link to show -- the frozen
    # core allows it (request_signatures loops over nobody), so
    # the surface must not offer Send yet AND must refuse the
    # direct POST
    assert f"action='/files/{w.file2_id}/esign/request'" \
        not in page, "editor offers Send with no signers"
    assert "Add a signer before sending" in page, \
        "no-signer editor lacks its hint"
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/request", {})
    st = w.conn.execute(
        "SELECT status FROM esign_files WHERE file_id=?"
        " AND deleted_at IS NULL", (w.file2_id,)).fetchone()
    assert st["status"] == "draft", \
        f"no-signer request went out (status {st['status']!r})"
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/signers", {
            "contact_id": str(w.contact_id)})
    assert f"action='/files/{w.file2_id}/esign/request'" in page, \
        "Send absent after the first signer"
    signer = w.conn.execute(
        "SELECT * FROM esign_signers ORDER BY id DESC").fetchone()
    assert signer is not None, "signer row missing"
    assert signer["access_token"], "contact signer has no link token"
    w.signer_id = signer["id"]
    w.signer_token = signer["access_token"]
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/fields", {
            "signer_id": str(w.signer_id),
            "field_type": "signature", "page": "1",
            "x": "100", "y": "600"})
    # a misplaced field is removable while draft (P4b gate r2:
    # James placed a duplicate live; core remove_field is
    # draft-only and had no button)
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/fields", {
            "signer_id": str(w.signer_id), "field_type": "date",
            "page": "1", "x": "300", "y": "600"})
    stray = w.conn.execute(
        "SELECT id FROM esign_fields WHERE field_type='date'"
        " ORDER BY id DESC").fetchone()
    assert stray is not None, "stray field not placed"
    assert f"esign/fields/{stray['id']}/remove" in page, \
        "placed field has no Remove control"
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/fields/{stray['id']}/remove",
        {})
    assert w.conn.execute(
        "SELECT id FROM esign_fields WHERE id=?",
        (stray["id"],)).fetchone() is None, \
        "removed field still in the core"
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/request", {})
    _s, _u, page = w.browser.get(f"/files/{w.file2_id}")
    assert "equested" in page, "e-sign status not visible on file"
    mail = w.conn.execute(
        "SELECT body FROM email_outbox WHERE template=?"
        " AND recipient=?",
        ("esign_request", "talia.client@synthetic.test")).fetchall()
    assert any(f"/esign/{w.signer_token}" in m_["body"]
               for m_ in mail), \
        "request email does not carry the signer link path"
    # VOID a sent request and redo (P4b gate r4: James needed to
    # undo his locked attempt). Confirm checkbox pinned as markup
    # (P2 stray-click ruling; the direct POST bypasses client
    # validation by nature). The old link must die AT THE CLIENT
    # SURFACE, and the PDF must offer Prepare afresh.
    old_token = w.signer_token
    old_es = w.conn.execute(
        "SELECT id FROM esign_files WHERE file_id=?"
        " AND deleted_at IS NULL", (w.file2_id,)).fetchone()
    _s, _u, page = w.browser.get(f"/files/{w.file2_id}")
    assert f"action='/files/{w.file2_id}/esign/void'" in page, \
        "requested file has no Void control"
    assert "<input type='checkbox' required" in page, \
        "Void lacks its confirm checkbox (stray-click guard)"
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/void", {})
    assert f"action='/files/{w.file2_id}/esign/prepare'" in page, \
        "voided PDF does not offer Prepare afresh"
    row = w.conn.execute(
        "SELECT deleted_at FROM esign_files WHERE id=?",
        (old_es["id"],)).fetchone()
    assert row["deleted_at"] is not None, \
        "void did not tombstone the e-sign row"
    cbase = (f"http://127.0.0.1:"
             f"{w.httpd.client_httpd.server_address[1]}")
    status, _u2, _p = Browser("").get(f"{cbase}/esign/{old_token}")
    assert status == 404, \
        f"voided signer link still alive (HTTP {status})"
    # redo from scratch: the full prep flow again on the same PDF
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/prepare", {})
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/signers", {
            "contact_id": str(w.contact_id)})
    signer = w.conn.execute(
        "SELECT * FROM esign_signers ORDER BY id DESC").fetchone()
    w.signer_id = signer["id"]
    w.signer_token = signer["access_token"]
    assert w.signer_token != old_token, "redo reused the old token"
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/fields", {
            "signer_id": str(w.signer_id),
            "field_type": "signature", "page": "1",
            "x": "100", "y": "600"})
    _s, _u, page = w.browser.post(
        f"/files/{w.file2_id}/esign/request", {})
    _s, _u, page = w.browser.get(f"/files/{w.file2_id}")
    assert "equested" in page, "redo did not reach requested"
    w.esign_file_id = w.file2_id
    return ("PDF-only prepare; stray field removed; request sent,"
            " VOIDED (old link dead), redone to requested")


def step_files_esign_sign(w):
    """The signer flow rides the FROZEN client surface (casework
    server: GET /esign/<token> renders field_<id> inputs; POST
    /esign/<token>/sign; typed mode = JSON {mode:'type',text:...})
    -- all field names discovered from that code, not invented. The
    staff page must hand the firm the LIVE absolute link
    (client_base + /esign/<token>, the intake-invite precedent).
    Completion takes produced custody, which makes the index's
    source filter observable (firm vs produced) for the first
    time -- so its narrowing assert lives here, not in the
    presence-only filter step."""
    need(w.esign_file_id, "requested e-sign file")
    need(w.signer_token, "signer token")
    _s, _u, page = w.browser.get(f"/files/{w.esign_file_id}")
    m = re.search(r"http://127\.0\.0\.1:\d+/esign/[0-9a-f]+", page)
    if m is None:
        raise Pending("live signer link not on the staff page")
    link = m.group(0)
    assert link.endswith(f"/esign/{w.signer_token}"), \
        "staff link is not this signer's"
    outside = Browser("")  # the signer is not logged in
    status, _u2, spage = outside.get(link)
    assert status == 200, f"signer link returned {status}"
    assert "Sign document" in spage, "signer page not the sign form"
    fid_m = re.search(r"name='field_(\d+)'", spage)
    assert fid_m is not None, "signer page shows no field input"
    assert "typing your full name" in spage, \
        "signature box lacks its human prompt"
    # the HUMAN path (program ruling 2026-08-10, gate r3): a plain
    # typed name -- the surface wraps it into the core's typed-mode
    # JSON contract; James's live drive hit the raw contract
    status, _u2, spage = outside.post(
        link + "/sign", {f"field_{fid_m.group(1)}": "Talia Synthetic"})
    assert status == 200 and "recorded" in spage, "sign POST failed"
    es = w.conn.execute(
        "SELECT * FROM esign_files WHERE file_id=?"
        " AND deleted_at IS NULL ORDER BY id DESC",
        (w.esign_file_id,)).fetchone()
    assert es["status"] == "completed", \
        f"esign status: {es['status']!r}"
    signed = w.conn.execute("SELECT * FROM files WHERE id=?",
                            (es["signed_file_id"],)).fetchone()
    assert signed is not None and signed["source"] == "produced", \
        "stamped copy not in produced custody"
    assert signed["name"] == "SYNTH-g28-candidate-signed.pdf", \
        f"stamped name: {signed['name']!r}"
    pdf = w.browser.get_bytes(f"/files/{signed['id']}/download")
    assert pdf[:5] == b"%PDF-", "signed artifact is not a PDF"
    _s, _u, page = w.browser.get(f"/files/{w.esign_file_id}")
    assert "ompleted" in page, "completed status not on the file page"
    _s, _u, page = w.browser.get("/files?source=produced")
    assert "SYNTH-g28-candidate-signed.pdf" in page
    assert "SYNTH-civil-documents-v2.txt" not in page, \
        "source filter did not narrow to produced"
    return ("typed signature via the live link; stamped copy filed"
            " as produced; source filter narrows")


# --- P5 search (Appendix A: chrome bar, coverage, recents) ---

def step_search_chrome(w):
    _s, _u, page = w.browser.get("/")
    expect_marker(page, "chrome-search", "chrome-level search bar")
    for path in ("/tasks", "/notes", "/files"):
        _s, _u, p2 = w.browser.get(path)
        assert "chrome-search" in p2, f"chrome bar missing on {path}"
    return "search bar reachable from every walked page"


def step_search_coverage(w):
    need(w.file_id, "uploaded file")
    need(w.full_note_id, "expanded note")
    need(w.task_id, "quick-added task")
    _s, _u, page = w.browser.get("/search?q=SYNTH-civil-documents")
    expect_marker(page, "result-group", "grouped results")
    assert "SYNTH-civil-documents-v2.txt" in page, \
        "file name not searchable"
    _s, _u, page = w.browser.get("/search?q=consular+processing")
    assert "SYNTH strategy memo" in page, "note BODY not searchable"
    _s, _u, page = w.browser.get("/search?q=cover+letter")
    assert "SYNTH draft I-130 cover letter" in page, \
        "task title not searchable"
    _s, _u, page = w.browser.get("/search?q=interview+prep")
    assert "SYNTH USCIS interview prep" in page, \
        "event title not searchable"
    return "widened coverage: files, note bodies, tasks, events"


def step_search_recents(w):
    _s, _u, page = w.browser.get(f"/contacts/{w.contact_id}")
    _s, _u, page = w.browser.get("/search")
    expect_marker(page, "Recent", "recents on the search page")
    assert "Talia Synthetic" in page, \
        "visited contact missing from recents"
    return "recents surfaced on the search page"


# --- P6 settings (Appendix A: ruled-in set + machinery homes) ---

def step_settings_users(w):
    page = probe(w, "/settings/users")
    _s, _u, page = w.browser.post("/settings/users/invite", {
        "email": "para.legal@synthetic.test",
        "name": "SYNTH Paralegal", "role_label": "Paralegal"})
    assert "SYNTH Paralegal" in page and "Paralegal" in page
    row = w.conn.execute("SELECT id FROM users WHERE email=?",
                         ("para.legal@synthetic.test",)).fetchone()
    w.invited_uid = row["id"]
    _s, _u, page = w.browser.post(
        f"/settings/users/{w.invited_uid}/deactivate", {})
    assert "deactivated" in page, "deactivation not shown"
    _s, _u, page = w.browser.get("/settings/users")
    for control in ("admin", "mfa-reset"):
        assert control in page, f"user control {control} missing"
    return "invite, role label, deactivate; admin + MFA controls"


def step_settings_permissions(w):
    page = probe(w, "/settings/permissions")
    _s, _u, page = w.browser.post("/settings/permissions/groups", {
        "name": "SYNTH Accounting"})
    assert "SYNTH Accounting" in page, "group not created"
    return "permissions/groups screen; group created by click"


def step_settings_trash(w):
    need(w.quick_note_id, "quick note")
    _s, _u, page = w.browser.get("/notes")
    expect_marker(page, "/settings/trash", "View-trash link on lists")
    _s, _u, page = w.browser.post(
        f"/notes/{w.quick_note_id}/delete", {})
    assert "SYNTH quick observation" not in page, \
        "deleted note still listed"
    page = probe(w, "/settings/trash?type=notes")
    assert "SYNTH quick observation" in page or \
        f">{w.quick_note_id}<" in page, "deleted note not in trash"
    _s, _u, page = w.browser.post("/settings/trash/restore", {
        "record_type": "notes",
        "record_id": str(w.quick_note_id)})
    _s, _u, page = w.browser.get("/notes")
    assert "SYNTH quick observation" in page, "restore did not land"
    return "delete = trash; central screen; restored by click"


def step_settings_notify_firm(w):
    page = probe(w, "/settings/notifications")
    assert "action='/settings/notifications'" in page, \
        "routing form missing"
    opts = re.findall(r"<option value='([^']+)'", page)
    if opts:
        _s, _u, page = w.browser.post("/settings/notifications", {
            "rule": opts[0]})
        assert opts[0] in page, "routing choice not reflected"
    page = probe(w, "/settings/firm")
    assert "name='timezone'" in page, "time zone control missing"
    _s, _u, page = w.browser.post("/settings/firm", {
        "timezone": "America/New_York"})
    assert "America/New_York" in page, "time zone not saved"
    return "notification routing + firm basics (time zone) by click"


def step_settings_homes(w):
    _s, _u, page = w.browser.get("/settings")
    expect_marker(page, "/settings/task-lists", "machinery homes in"
                  " the Settings layout")
    for home in ("/settings/note-categories",
                 "/settings/event-reminders",
                 "/settings/expiry-reminders"):
        assert home in page, f"Settings layout missing {home}"
    page = probe(w, "/settings/event-reminders")
    _s, _u, page = w.browser.post("/settings/event-reminders", {
        "value": "1", "unit": "days"})
    assert "1" in page and "day" in page, "default reminder not shown"
    page = probe(w, "/settings/expiry-reminders")
    _s, _u, page = w.browser.post("/settings/expiry-reminders", {
        "fact_key": "imm.ead_expiry", "lead_days": "30",
        "recipients": "admin"})
    assert "30" in page, "expiry reminder rule not shown"
    return "all four homes collected; defaults + rules set by click"


STEPS = [
    ("setup + login", step_setup_login),
    ("empty states designed (fresh db)", step_empty_states),
    ("client + matter (existing UI)", step_client_matter),
    ("calendar: new appointment", step_cal_new_appointment),
    ("calendar: new deadline", step_cal_new_deadline),
    ("calendar: unified view + kind filter", step_cal_unified),
    ("calendar: agenda/month toggle", step_cal_toggle),
    ("calendar: derived kinds [Q]", step_cal_derived_kinds),
    ("calendar: provenance links", step_cal_provenance),
    ("tasks: quick-add + due date", step_tasks_quick_add),
    ("tasks: my-open default + toggles", step_tasks_my_open),
    ("tasks: confirm-complete", step_tasks_complete),
    ("tasks: lists builder + import", step_tasks_lists),
    ("notes: categories home", step_notes_categories),
    ("notes: minimal capture + expanded", step_notes_capture),
    ("notes: matter timeline + pin", step_notes_timeline_pin),
    ("notes: index defaults + filters", step_notes_index_filters),
    ("notes: PDF export", step_notes_export),
    ("files: upload + custody", step_files_upload),
    ("files: matter section + index filters", step_files_matter_index),
    ("files: rename/preview/print/bulk", step_files_manage),
    ("files: e-sign prepare + request", step_files_esign_prepare),
    ("files: e-sign signer + custody", step_files_esign_sign),
    ("search: chrome bar everywhere", step_search_chrome),
    ("search: coverage + grouped results", step_search_coverage),
    ("search: recents", step_search_recents),
    ("settings: users admin", step_settings_users),
    ("settings: permissions groups", step_settings_permissions),
    ("settings: trash + restore", step_settings_trash),
    ("settings: notifications + firm basics", step_settings_notify_firm),
    ("settings: machinery homes collected", step_settings_homes),
]


# --- supporting sweeps (goal.md; empty-state sweep is step 2) ---

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


def iso_sweep(page_log):
    """No raw ISO date reaches the user on a tab page: every page a
    TAB step fetched (foundation pages excluded -- old screens are
    not this child's surface) is tag-stripped, then searched for
    YYYY-MM-DD. Form input values and hrefs vanish with their tags,
    so only visible text can hit."""
    pages = [(u, p) for (i, u, p) in page_log
             if i >= FOUNDATION_STEPS]
    hits = []
    for url, page in pages:
        text = TAG_RE.sub(" ", STYLE_RE.sub(" ", page))
        for m in sorted(set(ISO_RE.findall(text))):
            hits.append(f"{urllib.parse.urlparse(url).path}: {m}")
    detail = (f"no visible ISO dates on {len(pages)} tab pages"
              if not hits else f"strays: {', '.join(hits[:8])}")
    if not pages:
        detail = "0 tab pages walked yet (vacuous until steps land)"
    return ("iso-stray-sweep", not hits, detail)


def main():
    lines = ["# tabs-walk-report -- verifier 1", ""]
    counts = {"PASS": 0, "PENDING": 0, "FAIL": 0}
    total = 0.0
    page_log = []
    with tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True) as td:
        w = Walk(td)
        lines.append(f"run started: {_now()}")
        lines.append("")
        w.httpd = ui_server.make_server(w.workdir / "tabs-walk.db")
        w.conn = w.httpd.app_conn
        thread = threading.Thread(target=w.httpd.serve_forever,
                                  daemon=True)
        thread.start()
        ui_server.serve_client(w.httpd)
        try:
            w.browser = Browser(
                f"http://{w.httpd.server_address[0]}:"
                f"{w.httpd.server_address[1]}", page_log)
            for idx, (name, fn) in enumerate(STEPS):
                w.browser.step_index = idx
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
                lines.append(f"{status:7s} {name:38s} {elapsed:7.3f}s"
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
    lines.append("# supporting sweeps (empty-state sweep = step 2)")
    sweeps_ok = True
    for sname, sok, sdetail in (float_sweep(), iso_sweep(page_log)):
        sweeps_ok = sweeps_ok and sok
        lines.append(f"{'PASS' if sok else 'FAIL':4s} {sname}:"
                     f" {sdetail}")
    lines.append("")
    lines.append(f"steps: {counts['PASS']} pass, {counts['PENDING']}"
                 f" pending, {counts['FAIL']} fail; total {total:.3f}s")
    green = (counts["FAIL"] == 0 and counts["PENDING"] == 0
             and sweeps_ok)
    ok_now = counts["FAIL"] == 0 and sweeps_ok
    verdict = "GREEN" if green else ("ON TRACK (pending screens)"
                                     if ok_now else "FAIL")
    lines.append(f"verdict: {verdict}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8",
                      newline="\n")
    print(f"tabs-walk: {counts['PASS']} pass,"
          f" {counts['PENDING']} pending, {counts['FAIL']} fail;"
          f" sweeps {'pass' if sweeps_ok else 'FAIL'};"
          f" verdict {verdict}")
    print(f"report: {REPORT}")
    return 0 if green else 1


if __name__ == "__main__":
    sys.exit(main())
