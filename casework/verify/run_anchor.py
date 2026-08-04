"""Anchor workflow runner (verifier 2, goal.md). The live walk.

One scripted cold-start story on a FRESH database -- no seed, no
fixtures: install -> first admin (full MFA enrollment) -> contact ->
matter -> intake invitation -> client completes the questionnaire over
real HTTP -> filled G-28 PDF read back field-by-field -> deadline event
+ reminder fired by the scheduler tick -> audit chain for every step ->
supporting checks against the walked database.

What this proves BEYOND verifier 1 (P5 kickoff, 2026-08-01): the
fresh-db install path works; one fact entered once by the client over
HTTP lands in the produced PDF (single fact store as a lived chain,
not a schema lint); audit continuity across firm/client/system actors
in one narrative; the reminder engine fires from the story's own event.

Unlike spine-report.txt this report is NOT deterministic: it carries
wall-clock timings on purpose (goal.md: "verifier 2 pass with
timings"). Budget: the whole walk under 900s (decision default 6).

Run: python verify/run_anchor.py   (writes anchor-report.txt beside it)
Exit 0 iff every step passes and the budget holds.
"""

import logging
import re
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from app import auth, bootstrap, contacts, events, facts, forms  # noqa: E402
from app import db as appdb  # noqa: E402
from app import invitations, matters, render, scheduler, server, users  # noqa: E402
from verify import checks  # noqa: E402

logging.getLogger("pypdf").setLevel(logging.ERROR)

REPORT = HERE / "anchor-report.txt"
BUDGET_SECONDS = 900  # goal.md decision default 6: 15 minutes

G28_CLIENT_FAMILY = "form1[0].#subform[1].Pt3Line5a_FamilyName[0]"
G28_CLIENT_GIVEN = "form1[0].#subform[1].Pt3Line5b_GivenName[0]"
G28_ATTY_FAMILY = "form1[0].#subform[0].Pt1Line2a_FamilyName[0]"
G28_BAR_NUMBER = "form1[0].#subform[0].Pt2Line1b_BarNumber[0]"


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def http_get(url):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")


def http_post(url, data):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")


def read_pdf_fields(path):
    from pypdf import PdfReader
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fields = PdfReader(path).get_fields() or {}
    return {k: (v.get("/V") or "") for k, v in fields.items()}


class Walk:
    """Carries the story's state between steps."""

    def __init__(self, workdir):
        self.workdir = Path(workdir)
        self.base = datetime.now(timezone.utc).replace(microsecond=0)
        self.now = iso(self.base)
        self.conn = None
        self.admin_id = None
        self.contact_id = None
        self.matter_id = None
        self.smart_form_id = None
        self.token = None
        self.event_id = None
        self.pdf_path = self.workdir / "anchor-g28.pdf"


def step_install(w):
    """Fresh database: schema applies cold, install() loads the
    baseline vocabulary. Nothing here touches the synthetic seed."""
    w.conn = appdb.create_db(str(w.workdir / "anchor.db"))
    bootstrap.install(w.conn, w.now)
    # the walk's own records are synthetic; carry the guard's marker
    w.conn.execute("INSERT INTO synthetic_marker (marker) VALUES"
                   " ('SYNTHETIC')")
    ndefs = w.conn.execute(
        "SELECT count(*) FROM fact_definitions").fetchone()[0]
    assert ndefs == len(bootstrap.BASELINE_FACT_DEFS), \
        f"fact definitions: {ndefs}"
    ed = forms.current_edition(w.conn, "g-28")
    assert ed is not None, "g-28 edition missing after install"
    nforms = w.conn.execute(
        "SELECT count(*) FROM form_definitions").fetchone()[0]
    return f"schema cold-applied; {ndefs} fact defs; {nforms} forms in library"


def step_first_admin(w):
    """First user, real MFA enrollment: create -> password -> login
    (enrollment_required) -> enroll app TOTP -> verify -> live session."""
    uid = users.create_user(w.conn, "anchor.admin@synthetic.test",
                            "Anchor Synthetic", w.now,
                            role_label="Managing Attorney")
    auth.set_password(w.conn, uid, "anchor-synthetic-pass")
    users.update_user(w.conn, uid, is_admin=1, is_owner=1)
    status, token = auth.login(w.conn, "anchor.admin@synthetic.test",
                               "anchor-synthetic-pass", w.now)
    assert status == "enrollment_required", f"first login: {status}"
    secret = auth.enroll_twofa(w.conn, uid, "app", token, w.now)
    assert auth.verify_twofa(w.conn, token, auth.totp_code(secret, w.now),
                             w.now), "TOTP verification failed"
    assert auth.session_user(w.conn, token, w.now) == uid
    w.admin_id = uid
    w.conn.actor.set("user", uid)
    return f"admin id {uid}; MFA enrolled (app); session live"


def step_contact(w):
    """The client, minus the family name -- the client supplies that
    over HTTP later, proving the fact enters exactly once."""
    cid = contacts.create_contact(
        w.conn, "person", w.now, w.admin_id, given_name="Nova",
        email="nova.client@synthetic.test", phone="+1-555-0300")
    row = w.conn.execute("SELECT * FROM contacts WHERE id=?",
                         (cid,)).fetchone()
    assert row is not None and row["display_name"] == "Nova"
    assert facts.get_fact(w.conn, "contact", cid, "bio.family_name") is None
    audit = w.conn.execute(
        "SELECT actor_type, actor_id FROM audit_log WHERE"
        " entity_type='contacts' AND action='insert' AND entity_id=?",
        (cid,)).fetchone()
    assert audit is not None and (audit[0], audit[1]) == ("user", w.admin_id)
    w.contact_id = cid
    return f"contact id {cid} (no family name yet); audit: user {w.admin_id}"


def step_matter(w):
    mid = matters.create_matter(w.conn, "Anchor Synthetic G-28 Matter",
                                w.contact_id, w.now, w.admin_id,
                                assignee_id=w.admin_id)
    row = w.conn.execute("SELECT * FROM matters WHERE id=?", (mid,)).fetchone()
    assert row is not None and row["primary_contact_id"] == w.contact_id
    audit = w.conn.execute(
        "SELECT actor_type, actor_id FROM audit_log WHERE"
        " entity_type='matters' AND action='insert' AND entity_id=?",
        (mid,)).fetchone()
    assert audit is not None and (audit[0], audit[1]) == ("user", w.admin_id)
    w.matter_id = mid
    return f"matter id {mid} on contact {w.contact_id}; audit: user"


def step_invitation(w):
    """Firm identity + preparer defaults, the G-28 smart form, and an
    email invitation. The client's link comes FROM THE EMAIL BODY --
    the same link a real client would click."""
    w.conn.executemany(
        "INSERT INTO firm_settings (key, value) VALUES (?,?)",
        [("firm.name", "Anchor Synthetic Law LLP"),
         ("firm.street", "300 Anchor Plaza"), ("firm.city", "Faketown"),
         ("firm.state", "VA"), ("firm.zip", "00003"),
         ("firm.phone", "+1-555-0301"),
         ("preparer.default_user_id", str(w.admin_id))])
    w.conn.executemany(
        "INSERT INTO user_settings (user_id, key, value) VALUES (?,?,?)",
        [(w.admin_id, "preparer.family_name", "Synthetic"),
         (w.admin_id, "preparer.given_name", "Anchor"),
         (w.admin_id, "preparer.bar_number", "VA-ANCHOR-1"),
         (w.admin_id, "preparer.licensing_authority", "Virginia State Bar")])
    sfid = forms.create_smart_form(w.conn, "Anchor G-28", w.now, w.admin_id,
                                   contact_id=w.contact_id,
                                   matter_id=w.matter_id,
                                   form_codes=["g-28"])
    invitations.invite(w.conn, sfid, w.contact_id, "email", w.now)
    mail = w.conn.execute(
        "SELECT recipient, body FROM email_outbox WHERE"
        " template='intake_invitation'").fetchone()
    assert mail is not None
    assert mail["recipient"] == "nova.client@synthetic.test"
    m = re.search(r"/intake/([0-9a-f]+)", mail["body"])
    assert m is not None, "no intake link in the invitation email"
    w.smart_form_id = sfid
    w.token = m.group(1)
    return (f"smart form {sfid} (g-28); invitation emailed to"
            f" {mail['recipient']}; token from email body")


def step_client_http(w):
    """The client leg, over real HTTP: open the questionnaire, answer
    the client-tab questions (family name enters HERE, once), submit."""
    httpd = server.make_server(w.conn, str(w.workdir))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        base = server.base_url(httpd)
        status, page = http_get(f"{base}/intake/{w.token}")
        assert status == 200 and "Client family name" in page
        answers = [("q.g28.client_family_name", "Anchor-Synthetic"),
                   ("q.g28.client_street", "300 Anchor Way"),
                   ("q.g28.client_city", "Faketown"),
                   ("q.g28.client_state", "VA"),
                   ("q.g28.client_zip", "00003")]
        for qkey, value in answers:
            status, _ = http_post(f"{base}/intake/{w.token}/answer",
                                  {"question": qkey, "value": value})
            assert status == 200, f"{qkey}: HTTP {status}"
        status, _ = http_post(f"{base}/intake/{w.token}/submit", {})
        assert status == 200
    finally:
        httpd.shutdown()
        httpd.server_close()
    # the answers landed in the FACT STORE, attributed to the client
    got = facts.get_fact(w.conn, "contact", w.contact_id, "bio.family_name")
    assert got == "Anchor-Synthetic", f"fact store: {got!r}"
    audit = w.conn.execute(
        "SELECT actor_type, actor_id FROM audit_log WHERE"
        " entity_type='facts' AND action='insert' AND actor_type='contact'"
        " ORDER BY id LIMIT 1").fetchone()
    assert audit is not None and audit[1] == w.contact_id, \
        "client fact write not attributed to the contact actor"
    inv = invitations.track(w.conn, w.smart_form_id)[0]
    assert inv["status"] == "returned", f"invitation: {inv['status']}"
    return (f"{len(answers)} answers over HTTP; bio.family_name in fact"
            f" store, actor contact {w.contact_id}; invitation Returned"
            f" for Review")


def step_render_g28(w):
    """The payoff assertion: the PDF carries BOTH origins -- the fact
    the firm entered at creation (given name) and the fact the client
    entered once over HTTP (family name) -- plus preparer fields."""
    sff = forms.forms_of(w.conn, w.smart_form_id)[0]
    render.render_form(w.conn, sff["id"], w.pdf_path)
    fields = read_pdf_fields(w.pdf_path)
    expected = [(G28_CLIENT_FAMILY, "Anchor-Synthetic", "client via HTTP"),
                (G28_CLIENT_GIVEN, "Nova", "firm at creation"),
                (G28_ATTY_FAMILY, "Synthetic", "preparer settings"),
                (G28_BAR_NUMBER, "VA-ANCHOR-1", "preparer settings")]
    for field, want, origin in expected:
        got = fields.get(field, "")
        assert got == want, f"{origin}: {field} = {got!r}, want {want!r}"
    assert w.pdf_path.stat().st_size > 0
    return (f"G-28 rendered ({w.pdf_path.stat().st_size} bytes); 4 fields"
            f" read back correct across client/firm/preparer origins")


def step_deadline(w):
    """Deadline event + reminder, fired by the one dispatch path."""
    starts = w.base + timedelta(days=7)
    eid = events.create_event(w.conn, "Anchor filing deadline", iso(starts),
                              w.now, w.admin_id, contact_id=w.contact_id,
                              matter_id=w.matter_id)
    events.add_attendee(w.conn, eid, user_id=w.admin_id)
    events.add_reminder(w.conn, eid, 2, "days")
    scheduler.tick(w.conn, w.now)  # before the window: nothing fires
    n = w.conn.execute("SELECT count(*) FROM email_outbox WHERE"
                       " template='event_reminder'").fetchone()[0]
    assert n == 0, f"reminder fired {7 - 2} days early"
    scheduler.tick(w.conn, iso(starts - timedelta(days=2) +
                               timedelta(minutes=1)))
    mails = w.conn.execute(
        "SELECT recipient FROM email_outbox WHERE template='event_reminder'"
        " AND entity_id=?", (eid,)).fetchall()
    assert [m["recipient"] for m in mails] == \
        ["anchor.admin@synthetic.test"], "reminder recipients wrong"
    w.event_id = eid
    return (f"event {eid} at T+7d; 2-day reminder fired by tick into"
            f" outbox, once, to the assignee")


def step_audit_chain(w):
    """Continuity: every leg of the story left audit rows, attributed
    to the right actor class, in story order."""
    def first_id(where, params=()):
        row = w.conn.execute(
            f"SELECT id FROM audit_log WHERE {where} ORDER BY id LIMIT 1",
            params).fetchone()
        return row["id"] if row else None

    chain = [
        ("install (fact_definitions, system)",
         first_id("entity_type='fact_definitions' AND actor_type='system'")),
        ("contact created (user)",
         first_id("entity_type='contacts' AND action='insert'"
                  " AND actor_type='user'")),
        ("matter created (user)",
         first_id("entity_type='matters' AND action='insert'"
                  " AND actor_type='user'")),
        ("smart form created (user)",
         first_id("entity_type='smart_forms' AND action='insert'")),
        ("invitation issued (user)",
         first_id("entity_type='intake_invitations' AND action='insert'")),
        ("client fact write (contact)",
         first_id("entity_type='facts' AND actor_type='contact'")),
        ("event created (user)",
         first_id("entity_type='events' AND action='insert'")),
    ]
    missing = [name for name, aid in chain if aid is None]
    assert not missing, f"audit rows missing: {missing}"
    ids = [aid for _, aid in chain]
    assert ids == sorted(ids), f"audit chain out of story order: {ids}"
    return f"7 legs present, story-ordered (audit ids {ids[0]}..{ids[-1]})"


def step_supporting_checks(w):
    """The verifier-1 supporting checks against the WALKED database --
    including the P5 fact-integrity sweep over the story's own facts."""
    results = checks.run_all(w.conn)
    bad = [f"{name}: {detail}" for name, ok, detail in results if not ok]
    assert not bad, "; ".join(bad)
    return f"all {len(results)} checks pass on the anchor db"


STEPS = [
    ("fresh-db install", step_install),
    ("first admin + MFA login", step_first_admin),
    ("create contact", step_contact),
    ("create matter", step_matter),
    ("smart form + invitation", step_invitation),
    ("client intake over HTTP", step_client_http),
    ("G-28 render + read-back", step_render_g28),
    ("deadline + reminder tick", step_deadline),
    ("audit chain continuity", step_audit_chain),
    ("supporting checks on walked db", step_supporting_checks),
]


def main():
    lines = ["# anchor-report -- verifier 2 (live walk on a fresh db)", ""]
    with tempfile.TemporaryDirectory() as td:
        w = Walk(td)
        lines.append(f"run started: {w.now}")
        lines.append("")
        all_ok = True
        total = 0.0
        for name, fn in STEPS:
            t0 = time.perf_counter()
            try:
                detail = fn(w)
                ok = True
            except Exception as e:
                detail = f"{type(e).__name__}: {e}"
                ok = False
            elapsed = time.perf_counter() - t0
            total += elapsed
            all_ok = all_ok and ok
            lines.append(f"{'PASS' if ok else 'FAIL':4s} {name:32s}"
                         f" {elapsed:8.3f}s  {detail}")
            if not ok:
                break
        if w.conn is not None:
            w.conn.close()
    lines.append("")
    budget_ok = total < BUDGET_SECONDS
    lines.append(f"total: {total:.3f}s  budget: {BUDGET_SECONDS}s"
                 f" ({'within' if budget_ok else 'OVER'})")
    verdict = "PASS" if (all_ok and budget_ok) else "FAIL"
    lines.append(f"verdict: {verdict}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"anchor: {verdict} ({total:.3f}s of {BUDGET_SECONDS}s budget)")
    print(f"report: {REPORT}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
