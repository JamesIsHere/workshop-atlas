# worklog.md -- casework-ui (append-only)

## 2026-08-01 -- Bootstrap: scaffold + interview + drafts

Origin: casework closed same day (both verifiers pass, result.md
written); James's read: "we have a prototype" -> the gap named in
that exchange is exactly this child -- capability was proven, the
thesis (interaction cost) needs a clickable instrument. James
declared the build ("make something people can click around in")
and invoked project-kit + goal-method by name.

Scaffold: atlas/casework-ui created via project-kit (name chosen
by James from candidates: casework-ui over ui/frontdesk); atlas
roster row added (ACTIVE -- PRE-CONTRACT).

Interview rulings (one decision per turn, four rounds):

1. OPERATING MODE: MIXED with SCREEN-REVIEW GATES -- James
   eyeballs the running UI at each phase gate; the gate artifact
   is the rendered screen, not only a unit table. ("I do like the
   eyeballing.")
2. SCOPE: ANCHOR-PLUS-BROWSE -- anchor walk fully clickable (the
   verifier), browse-grade read-only surfaces everywhere else so
   free exploration never dead-ends. Full-spine clickable rejected
   (product surface before thesis signal); anchor-only rejected
   (Amin would click off the paved road in two minutes).
3. COLD USER DEFINITION: anyone who has never operated the system;
   proof = at least one passing run; James's runs are rehearsal,
   never proof; Amin's staff eligible as run 2 after run 1's
   findings are fixed (keeps verifier and demo separate).
4. STACK: vanilla-sprinkle JS -- server-rendered skeleton, no
   framework/npm/build step, each JS use justified per-screen by a
   named interaction cost, every screen functions with JS off.
   Zero-JS rejected: risks refuting the thesis by austerity (the
   handicap, not the design, would be measured).

Drafts written for red-pen: goal.md (verifier sections flagged as
strawmen -- primary pen targets), plan.md (coarse 5-phase roster),
this file, state.md. Self-audit questions ratified into goal.md's
operating-mode section per method checklist item 5.

METHOD: first project bootstrapped against the method's updated
skill (post-Trial-3). Notable: the interview honored the skill's
"mode early" ordering and James's one-decision-per-turn rule
simultaneously -- four single-question rounds, each answered in
one turn with explicit agreement. Verifier detail skipped the
interview entirely and went straight to strawman (red-pen
mechanism 1), untested until the pen hits it. This child also
edges toward the method's open falsification target 3 (fuzzy
goal): verifier 2's instrument is a human with a stopwatch --
concrete enough to write, but the first verifier in the program
whose pass/fail depends on a person's live performance.

## 2026-08-01 -- goal.md RATIFIED; P0 gate opens

James ratified the whole document after review, ZERO red-pen kills
-- the primed candidate list (first-run ceremony, browse-sweep
placement, roster breadth, finish-line wording) drew no pen; he
asked for agent questions instead, and the only live one (does
account ceremony count inside the cold user's budget) was deferred
to its scheduled home, the P3 protocol ratification, rather than
guessed now. Deferral recorded in goal.md's status block.

METHOD: second consecutive whole-document ratification with zero
kills (casework's goal went the same way). The kills in this
program land at phase gates and in dialogue (casework P5's split
ruling), not on goal documents -- consistent with drafts built
from interviews that already carried the load-bearing rulings.

Next: P0 unit table for gate ratification, then unattended P0.

## 2026-08-01 -- P0 ratified ("Drafted.") and executed unattended

GATE: James ratified the P0 unit table as drafted, zero kills
(sixth consecutive zero-kill gate across the program).

EXECUTION. U0.1 app_ui/ package: stdlib ThreadingHTTPServer over
one casework connection + lock (casework client-surface pattern);
html.py layout w/ inline style block, zero JS, zero static routes;
sys.path wiring APPENDS casework (see churn 1). U0.2 first-run +
auth: fresh-db detect -> /setup (admin create via users/auth
modules) -> mandatory TOTP enrollment (secret shown base32 +
otpauth, code typed back, auth.py path, no bypass) -> login/
session cookie (HttpOnly, SameSite=Lax) -> /mfa on every login;
all routes auth-gated except the setup/login/MFA set. U0.3
verify/run_ui_walk.py oracle-first: all 13 story steps enumerated;
4 green (setup, MFA enrollment incl. computed-TOTP verify, login
round-trip incl. wrong-code refusal, auth gate incl. anonymous
redirect x4 + bad-password), 9 PENDING with named landing phases;
report + verdict "ON TRACK (pending screens)", exit 1 as specified
until all green. U0.4 sweeps: no-logic lint (SQL only in reads.py,
SELECT-only; named-exemption allowlist w/ rationale) +
js-discipline (zero JS; justification registry empty by design);
both wired into the walk report.

CHURN: 2 red iterations, both structural, both fixed same unit.
(1) Package collision: casework's verify/ shadowed casework-ui's
-- casework was INSERTED at sys.path[0]; fix = append casework +
make local verify/ a regular package. Lesson: sibling-import
wiring must keep the consumer project first on path. (2) The
no-logic lint FAILED ITS OWN PROJECT first run: the synthetic-
marker INSERT in server.make_server is raw SQL in the UI layer.
Ruled provenance-not-logic; casework is frozen so no helper can be
added there without an approval cycle; fix = named allowlist entry
in sweeps.py carrying the rationale. The sweep catching the
author's own code on day one is the mechanism working.

DESIGN NOTES (agent territory, logged): MFA method is app-TOTP
only in P0 (email 2FA reads the outbox, which has no UI yet --
revisit if a cold user lacks an authenticator app; queue at P3
protocol gate). Marker exemption above. reads.py is the drafted
exact form of goal.md's no-logic rule.

Gate package: server live at 127.0.0.1:8500 (fresh db
data/demo-p0.db -> setup flow visible end-to-end), walk report on
disk. SCREEN REVIEW 1 pending James's eyeball.

## 2026-08-01 -- SCREEN REVIEW 1: MFA killed and replaced live

James's review hit the wall immediately: no authenticator app --
the P0 design note's queued risk (app-TOTP-only) fired on the
FIRST human login, at the gate reviewer himself. Unblocked him
with a computed code, then RULING (his words: "make it static"):
TOTP is KILLED for v1; MFA = casework's email method -- static
per-login 6-digit code, no expiry, no rotation -- with the
challenge email rendered in a labeled "Synthetic mailbox" panel
on the /mfa page itself (this system sends no real email; in
production the message lands in the user's inbox, so the panel
disappears and the flow shape survives). Real auth path
constraint intact: enroll_twofa('email') + verify_twofa, zero
bypass, zero casework edits.

Implementation: reads.latest_twofa_email (SELECT-only, lint
clean); enroll page = one "Email me a code" button; walk runner
steps rewritten to read the code from the mailbox panel like a
human would (fresh challenge at re-login; wrong code refused;
static code survives the failed try). Receipt: "ui-walk: 4 pass,
9 pending, 0 fail; sweeps pass" -- green on the new flow first
run. James's demo account 2FA reset via auth.reset_twofa (module
call); server restarted on :8500; his next login re-enrolls
under the new flow.

METHOD: the screen-review gate did exactly what it was added for
-- caught in 60 seconds of human contact what four green
mechanical steps could not see (the walk runner COMPUTED its TOTP
codes, so the no-authenticator-app failure mode was structurally
invisible to it). Churn count P0: 3 (path collision, lint
self-catch, MFA replacement -- the third is gate-driven redesign,
not red-test iteration).

## 2026-08-01 -- Screen review 1, round 2: code was hidden, not absent

James hit /mfa, read "emailed to you," checked his REAL inbox
(nothing there -- outbox-only system), and concluded the flow was
broken; his screenshot shows the code ("Your verification code is
121143") sitting in the panel BELOW the fold the whole time. Not
an auth failure -- a presentation failure: the screen buried its
own answer and the copy pointed at the wrong mailbox.

Fix (no ruling needed -- his "make it static" intent stands, and
"switch it back" dissolved once shown nothing was broken): /mfa
now LEADS with the code -- "Your login code" panel first, 6
digits at 2.2rem centered, synthetic-environment fine print
after; entry field labeled "Type the code above"; enroll copy no
longer promises email ("Show me my code"); error copy matched.
Walk churn: 1 (runner asserted the old panel heading; updated
with the layout -- the oracle tracking a ruled redesign, not a
regression). Receipt: "ui-walk: 4 pass, 9 pending, 0 fail; sweeps
pass" on the new layout.

METHOD: two review rounds, two findings the mechanical verifier
was structurally blind to (no-authenticator-app; below-the-fold
code + misleading copy). The gate's value so far is entirely in
the class of failure a script cannot have: wrong expectations,
not wrong behavior. Both were interaction-cost defects -- the
exact defect class this child exists to design out. Worth
carrying to the P3 cold-run protocol: the reviewer reading copy
literally IS the test.

## 2026-08-01 -- P1 ratified ("looks good please proceed") + built

GATE: P1 unit table ratified as drafted, zero kills (seventh
consecutive). Flagged judgment call accepted: casework's client
surface mounted IN-PROCESS on a second port, same connection and
SAME lock object as the UI server (assigned after make_server --
zero casework edits), one command runs both.

EXECUTION (unattended). U1.1-U1.6 in one stretch: contact create/
detail (facts via casework modules; family name deliberately
optional -- the client supplies it), matter create/detail (the
story's home base: form packages, deadlines, primary contact
accumulate there), form package + invitation (checkbox form
picker g-28 default; copyable client link rendered from
client_base + token; status pills Sent/Returned), intake review
(per-question answers resolved through PUBLIC module APIs:
schema_of + role_contact + get_fact + get_answer -- preparer/firm
questions skipped as auto-populated), G-28 download (render to
temp, application/pdf attachment), calendar/deadline (date+time
+reminder-offset form; event detail shows reminders; matter and
calendar both list it). reads.py grew 12 SELECT-only display
readers; router became a segment tree w/ _NotFound; html.py
gained table/actions/kv/pill primitives. Walk steps 5-12
implemented: client leg drives the mounted intake surface with a
separate cookie-less browser; G-28 read back via pypdf (client-
entered family name + firm-entered given name both asserted in
the PDF); tick fires exactly one reminder; audit chain 6 legs
story-ordered.

Receipt: "ui-walk: 12 pass, 1 pending, 0 fail; sweeps pass" --
FIRST RUN, total 0.499s. Churn P1: 0 red iterations.

DESIGN NOTES (logged): (1) preparer/firm-settings WRITE screens
are out of ratified scope (settings is P2 read-only), so the UI
walk asserts client+firm fact fields in the PDF, not preparer
fields -- preparer machinery stays covered by casework's own
verifiers. Queue for P3 protocol: does the cold-run task sheet
need preparer fields at all. (2) Contact form is person-only;
company contacts exist module-level, browse-grade in P2.

NEXT GATE: screen review 2 -- James walks the anchor story by
hand end to end.

## 2026-08-01 -- Screen review 2, finding 1: empty-state dead end

James went dashboard -> New matter BEFORE creating any contact
(db check: contacts = []) and hit a required dropdown with zero
options and no way forward -- a dead end built on a happy-path-
order assumption. Fix: /matters/new with no contacts now explains
("a matter needs a primary contact") and routes to /contacts/new;
with contacts present, the picker gains an or-create-new escape
link. Walk re-run after fix: "12 pass, 1 pending, 0 fail; sweeps
pass" -- no regression.

METHOD: review finding 3, third defect class invisible to the
scripted walk (it creates entities in dependency order by
construction; a human wanders). The browse-sweep design for P2
should include EMPTY-STATE rendering of every surface, not just
seeded-data rendering -- queued for the P2 unit draft.

## 2026-08-02 -- Screen review 2, finding 2: space not navigable

James's hand-walk (live session). Three hits, one root cause:
(1) opened nav "Matters" expecting to start there -- P2 stub;
(2) created contacts, then could not click BACK to them -- the
dashboard counter line ("2 contacts, 3 matters") is plain text,
nav Contacts is a stub, and a contact with no matter is orphaned
from the UI (only live inbound links are from matter pages);
(3) noticed Calendar is the only live index -- because it is the
only index the anchor ASSERTS (deadline visible); contacts/
matters only needed creating-and-chaining, so their indexes fell
to P2.

DISPOSITION (James): same issue, one cluster -- logged as
review-2 findings, resolved by the P2 unit table (indexes are
literally the P2 roster). No P1 patch; continue the walk.

METHOD: generalization of finding 1's lesson. P1's slicing
criterion was verifier-driven (what the scripted walk touches),
not navigation-driven (what a human can reach). The walk proves
the PATH is clickable, never that the SPACE is navigable -- it
never turns around. P2 browse sweep should assert reachability:
every created entity reachable by clicks from the dashboard,
plus empty-state rendering (finding 1's queue item stands).

## 2026-08-02 -- Screen review 2: PASS

James completed the anchor story by hand end to end: contact ->
matter -> form package -> invitation -> client intake -> review
-> G-28 download -> deadlines + reminders visible on calendar.
PDF receipt (pypdf over his downloaded g-28.pdf): 4 pages, 113
fields, 8 filled -- FamilyName McCoy, GivenName, email, phone,
4 barcodes. A doubled given name ("James James") was ruled USER
ERROR by James, not a fill defect. Verdict: PASS with the
finding-2 navigation cluster logged (P2 resolves).

DATA NOTE: James typed his real email/phone into demo-p0.db
during the walk (synthetic-only rule). Ruled low-stakes for a
local disposable db; wipe demo-p0.db (delete + re-setup) before
the db travels anywhere (e.g. a demo).

NEXT GATE: P2 unit table ratification.

## 2026-08-03 -- P2 ratified ("looks good") + built; walk GREEN

GATE: P2 unit table ratified as drafted, zero kills (eighth
consecutive). Sweep design encodes both review-2 findings: empty
states and reachability are now VERIFIED properties.

EXECUTION (unattended). U2.1-U2.4: contacts/matters/files/tasks/
notes indexes (nav stubs gone; dashboard counters are links; every
index has a designed empty state via html.empty_state -- class
'hint empty' is the sweep's marker); file/task/note detail pages
with cross-links; file download; search screen; read-only settings
(firm_settings + user list) added to nav. reads.py grew 7 readers
(now 22, SELECT-only). "Not built yet" page reworded to "Not
found" -- nothing behind the nav is unbuilt anymore. U2.5: browse
sweep implemented as walk step 13, three legs: (a) seeded render
12 checks incl. search hits and file-download bytes; (b)
reachability BFS over rendered hrefs from / -- all 7 seeded
entities clickable from the dashboard; (c) fresh-db server:
every surface renders its designed empty state, zero data rows.

Receipt: "ui-walk: 13 pass, 0 pending, 0 fail; sweeps pass;
verdict GREEN" -- exit 0 for the FIRST time. Foundation:
run_anchor.py "anchor: PASS (1.322s of 900s budget)".

DESIGN NOTES (logged): (1) drafting correction -- search rides
casework's search module (fx-0090 universal search), not new
reads.py SQL; strictly better under the no-logic rule; plan.md
U2.3 cell updated to match. (2) files/tasks/notes have no create
UI in scope, so browse-sweep seeds ride casework modules --
setup, not assertion. (3) Settings added to NAV_ITEMS (reachable
by clicks, per the BFS bar).

CHURN P2: 1 red walk run, 0 P2 code defects -- the red was a
LATENT P1 verifier bug: step_deadline_reminder computed the tick
fire-time from wall-clock now but posts the event at 09:00 UTC,
so any run before 09:00 UTC failed (first tripped 04:20 UTC).
Fixed in-project: fire-time now derives from the posted start.

CROSS-PROJECT FLAG (not fixed from here): casework spine is RED
today -- tests/spine/test_esign.py:153 hardcodes the esign auto-
date as "2026-08-01" (suite-writing day) while the app fills the
real signing date. Same defect class as the walk bug (verifier
clock != app clock). One-line fix in casework's test, needs
James's authorization; until then run_spine.py exits NOT GREEN
on any date after 2026-08-01.

METHOD: two independent verifiers both carried wall-clock
assumptions that held on writing day and expired silently. A
"runs green at 04:00 UTC on a later day" check belongs in cold-
run protocol design (P3).

NEXT GATE: screen review 3 -- free-click session on a seeded db.

## 2026-08-03 -- cross-project flag CLOSED: spine test fix applied

James authorized the one-line fix ("please fix the red issue
now"). tests/spine/test_esign.py now derives the expected auto-
date from the signer's own signed_at stamp instead of the expired
literal; casework app code untouched. Receipts: "spine: 107
green, 0 red, 0 pending; checks pass"; "anchor: PASS (1.371s of
900s budget)". Change logged in casework's worklog as well.

## 2026-08-03 -- Screen review 3: PASS

James free-clicked the seeded db on the P2 build: "the site looks
good." No findings raised. Browse layer accepted; gate cleared for
P3 drafting.

## 2026-08-03 -- P3 ratified; U3.1 + U3.2 built

GATE: P3 unit table ratified (ninth consecutive zero-kill) with
one James-driven amendment BEFORE ratification: the cheap grep
"clock audit" was toughened into a behavioral CLOCK GAUNTLET at
his push ("let's actually do a test") -- the right call; the
grep could never catch a helper-routed comparison.

U3.1 CLOCK GAUNTLET: verify/run_clock_gauntlet.py -- property:
every verifier green under ANY single consistent clock. Subprocess
shim swaps datetime.datetime for an offset subclass before any
import; app + verifier share one fake clock (the cold-user
invariant). 5 arms x 3 verifiers (ui-walk, casework spine,
casework anchor, read-only): pre-09Z, post-09Z (control), +400d,
midnight straddle, New Year's Eve straddle; closing real-clock
runs keep on-disk reports truthful and double as the walk-x2
completion receipt. Harness churn: 2 fixes found by READING MY
OWN REPORT -- (1) offsets computed at gauntlet start had drifted
past midnight by the time straddle arms ran (runs landed after
the flip, not across it); (2) per-block offsets meant only the
first verifier in a block straddled. Both fixed: offsets are now
computed per RUN; report shows each run's start clock (straddles
start 23:59:59, cross mid-run).

Receipt: "clock-gauntlet: GREEN" exit 0 -- 19/19 runs green
(15 fake-clock + 4 closing; walk x2 among them). Would have
caught both 08-03 clock bugs by construction.

U3.2 COLD-RUN PROTOCOL DRAFT: verify/cold-run-protocol.md --
roles (runner/proctor, proctor speech rules), fresh-db setup,
verbatim task sheet (Priya Synthetic story; firm + client data
cards, synthetic throughout), 6 timing marks M0-M5 recorded
ALWAYS so either budget ruling has its number, pass criteria,
friction log form. DECISION boxes framed for the gate: (a)
ceremony in/out of the 15:00 budget (goal.md deferral; needs
M0->M1 rehearsal data); (b) preparer fields on the task sheet
(needs rehearsal friction note on the attorney block).

NEXT: U3.3 SUPERVISED rehearsal -- James runs the draft task
sheet on a fresh db, stopwatch on, recorded on the form.

## 2026-08-03 -- U3.3 rehearsal 1 + U3.4 protocol hardening

U3.3 REHEARSAL (James, solo, db data/cold-run-2026-08-03.db).
Surface verdict from the runner: "process is fine and fast";
three findings reported (phone clipping, Bob-Priya family name,
email correct). Receipts told a bigger story:

- Phone: NO truncation -- PDF field value carries the full
  '777 888 9999' (maxlen None); the clip is the G-28 template's
  visual field width. No fix; friction note.
- Bob-Priya: user input, not a merge -- audit shows all 5 facts
  written by actor 'user' at contact creation. System faithful.
- Runner ruled both: user error / no defect ("I agree").
- UNREPORTED, found by db check: intake_invitations EMPTY,
  form_answers EMPTY, zero contact-actor writes -- steps 4-5
  (invitation + client leg) were SKIPPED and nothing looked
  wrong because the firm side had typed all client data.
  events + event_reminders EMPTY -- the deadline was never
  saved despite "those function adequately". Data cards ignored
  (PriyaTest / priya@gmail.com / "Bob Stuck Again"); real gmail
  domains where .test addresses were carded. Marks unrecorded
  (solo runner cannot proctor). <date> placeholder in the setup
  command pasted verbatim -> opaque sqlite error.
- Timing reconstructed from snap mtimes + db stamps: M0
  ~06:19:19Z (setup loaded), account 06:23:06Z, facts 06:23:57,
  matter 06:24:29, package 06:25:01, PDF review by 06:27.
  CEREMONY ~4:00 of the 15:00 budget (~27%). Working leg
  (dashboard -> package -> PDF) ~2-4 min. Evidence for gate
  decision (a).

METHOD: the rehearsal's real product was breaking the PROTOCOL,
not the UI -- eyeball pass criteria let a run that skipped the
anchor's defining leg look complete. Ruling (James): proceed, no
re-rehearsal; harden instead.

U3.4 HARDENING (built):
- verify/check_cold_run.py -- 9 read-only db-artifact checks
  (cards followed, invitation exists, contact-actor fact writes,
  invitation returned, deadline tied to matter, reminder
  attached, synthetic marker). Receipt against the rehearsal db:
  "INCOMPLETE (7 missing)" exit 1 -- catches every gap of run 1
  by construction. Wired into pass criteria + recording form.
- Protocol setup: concrete dated command example (placeholder
  finding); solo-runner rule (proof requires live proctor;
  rehearsals must screen-record or timestamp).
- James hand-edited the protocol (iff -> if, roles section);
  edit preserved.

NEXT GATE (U3.5): ink decisions (a) ceremony in/out of budget
(evidence: ~4:00 ceremony) and (b) preparer fields; ratify
protocol; draft P4 units.

## 2026-08-03 -- P3 GATE CLOSED: protocol ratified, P4 ratified

Gate sequence, all James: decision (a) RULED Option 2 (budget
M1->M5; ceremony outside, ~4:00 rehearsal evidence; both pairs
always recorded). Decision (b) RULED Option 1 (no preparer step;
cold run is an interaction-cost instrument, not a second
correctness oracle). BUDGET CHALLENGE at ratification: James
proposed tightening 15:00 -> 2:00 off his rehearsal pace; agent
pushback with receipts (his 2-4 min warm leg SKIPPED invitation,
client intake, and deadline -- the slow legs; one run per person
makes a blown budget cost a recruit; counter-proposal 5:00).
RULING: 15:00 stands as drafted. Protocol RATIFIED; P4 unit
table RATIFIED as drafted (tenth consecutive zero-kill on unit
tables).

Rehearsal server stopped; data/cold-run-2026-08-03.db retained
(delete = archive). P4 open: U4.1 blocks on James recruiting a
qualifying cold runner (never operated any build).

METHOD: the budget challenge is the first gate where a James
proposal was argued DOWN by agent receipts rather than inked --
the rehearsal db's skipped-legs evidence did the work, not
opinion. The one-decision-per-turn gate format held through a
3-ruling gate without stacking.

## 2026-08-03 -- FREESTYLE EXPLORATION SESSION: 6 findings

James, solo, on data/cold-run-2026-08-04.db (playground: off-sheet
data, Fix Bob matter, contacts Casey Dingus + Bob Dingus). NOT a
rehearsal -- free clicking with a tester's eye. Server restarted
mid-session (terminal closed); agent ran it in background from
the Claude session. Findings, in discovery order:

1. LABEL AMBIGUITY (app_ui/server.py:410-412, contact create):
   "Given name" / "Family name" produced a SWAPPED record from
   the card "Casey Synthetic-Operator" (snap receipt: given=
   Synthetic-Operator, family=Casey). Proposed fix (mini-gate,
   ruling PENDING): USCIS parenthetical labels -- "Given name
   (first name)" / "Family name (last name)" -- matching the
   G-28's own block labels, plus a person-only hint line (v1
   ruling: contact CREATE is person-only). Retreat to bare
   First/Last rejected: immigration practice needs given/family
   (non-Western name order); USCIS solved this with
   parentheticals decades ago.
2. SECONDARY CONTACT INVISIBLE on matter detail: only the
   primary contact renders. Display gap vs scope ruling --
   investigate before the gate.
3. INTAKE SHOWS NO KNOWN VALUES (casework/app/server.py:141,
   value = "" hardcoded): client questionnaire renders every
   input blank regardless of db facts; write-only surface. The
   client cannot VERIFY firm-entered data, only re-type it.
   Docketwise's smart-form prefill is its headline feature --
   thesis-relevant. CROSS-PROJECT (casework frozen): flag only.
4. CLIENT-PAGE CRASH ON FIRM-SIDE FIELD (the heavyweight):
   client questionnaire RENDERS Attorney/Appearance fields as
   editable, but answer_intake refuses them (casework/app/
   intake.py:132 ValueError "firm-side data") -- unhandled ->
   connection drop -> browser ERR_EMPTY_RESPONSE. Never surfaced
   in casework verification: scripted client leg only answers
   client-subject questions. COLD-RUN LANDMINE: a diligent
   runner filling "Name of law firm" gets a dead tab mid-run.
   Candidate no-freeze-violation fix: app_ui sends invitations
   with firm-side tabs restricted (invitations.restricted_tabs_of
   already exists). Gate decision.
5. NO INTAKE RECONCILIATION: client Save writes facts DIRECTLY;
   "Review answers" is a mirror of current facts, not a diff --
   the client silently wins every conflict, and by review time
   there is nothing left to compare. James's engineered test
   (typed "bob" everywhere expecting one-right-two-wrong
   comparison) proved contact 1's facts overwritten in place
   (Casey/Dingus -> bob/bob; db receipts pulled). audit_log
   .changes retains history -> read-only "what changed" view is
   buildable UI-side without touching casework. Gate candidate.
6. STALE DISPLAY NAME: display_name composed once at contact
   create, never recomputed from facts -- contacts list says
   "Casey Dingus" while facts (and the filled PDF) say bob bob.
   Same person, two names, screen-dependent.

Bonus protocol color: "sent forms twice" -> two live invitation
tokens on one package, both valid, harmless; opening a link is
what flips status to accepted (casework/app/server.py:122).

Also RULED EARLIER THIS SESSION (James): no independent runner
available right now; James reruns as rehearsal 2 (fresh dated
db, sheet verbatim, screen-recorded) and recruits separately.
Plan unchanged -- his runs stay rehearsal, proof slot waits.

QUEUE: (a) James rules on finding 1 label fix; (b) rehearsal 2;
(c) gate for findings 2-6 (4 and 5 heavyweight, both frozen-
casework design properties).

FINDING 1 RULED + FIXED (same session): James approved USCIS
parenthetical labels, amended the hint wording to "(individual
person not firm name)". app_ui/server.py _contact_new updated:
"Given name (first name)" / "Family name (last name) -- client
can supply later" / hint line under the heading (.hint class,
already in the stylesheet). Receipt: verify/run_ui_walk.py GREEN
after the edit -- "13 pass, 0 pending, 0 fail; sweeps pass".
Live server restarted on the playground db so the new form
serves. Findings 2-6 remain queued for the gate.

PROTOCOL AMENDED (James, live gate ruling: "Test is not ready,
fix"): rehearsal 2 attempt surfaced that the data cards did not
mirror the screens -- FIRM card said "Name: Casey
Synthetic-Operator" (single field, role-string value; setup
screen actually asks "Your name"; rehearsal-1 swap traced to
this same mapping burden), and one CLIENT card served two
different screens with labels matching neither. Amendment: ONE
CARD PER SCREEN, field names verbatim from the screen -- SETUP
card (Your name: Casey Synthetic / email / password), NEW
CONTACT card (Given name (first name): Priya ...), QUESTIONNAIRE
card (casework's client-question labels, address included).
Task sheet references updated; added "fill only what the card
shows, leave everything else blank" (also defuses finding-4
landmine for runners). check_cold_run.py UNCHANGED -- all pinned
values survived. Firm display name "Casey Synthetic" chosen to
match seed convention (flagged: agent judgment). r2 db
contaminated (account created as James McCoy) -- retained per
delete=archive; rehearsal restarts fresh on
data/cold-run-2026-08-03-r3.db.

REDESIGN ROUND 2 (James, live ruling: "redesign test... FIX
IT"): three fixes. (1) Field labels now match cards VERBATIM --
microcopy moved out of labels into hint lines (html.field grew a
hint= param); contact form labels are bare "Given name (first
name)" / "Family name (last name)" / "Email" / "Phone". (2)
Contact-form concept hint rewritten: "A person -- usually a
client. Not a company." -- the previous wording used "firm" on a
screen where firm is ambiguous (the law firm vs a client's
company); James spun wheels on "is New Contact a person at a
firm or a new firm". (3) Realistic synthetic names: Casey
Morgan / Priya Sharma replace *-Synthetic names -- marker-style
names made runners decode placeholder-vs-value; the synthetic
flag rides the .test email domains + db marker, not the names.
check_cold_run.py CLIENT updated (family_name Sharma). Receipt:
run_ui_walk.py GREEN post-edit (13 pass, sweeps pass). PARKED
(log-don't-build, James product instinct): company-first
contact flows ("sometimes you need to add a firm before its
main contact") -- company CREATE is out of v1 by ruling; the
instinct is recorded for the build-children roster. PII NOTE:
r3 db contains James's real name+yahoo email (he set up as
himself); r3 retained-but-contaminated, same handling as
demo-p0.db (local only, wipe before travel). Rehearsal restarts
on data/cold-run-2026-08-03-r4.db.

REDESIGN ROUND 3 (James, live ruling): protocol cards now
narrate the TRUE LOAD ORDER, titled by each screen's own
heading (verified against app_ui/server.py handlers): Card 1
"Set up your firm's first account" (also serves "Log in"
later; MFA screens noted -- code displayed on-screen, no card),
Card 2 "New contact", Card 3 "Your questionnaire". Task sheet
references updated to Card 1/2/3. NEW RULE inked into the cards
intro: type card values EXACTLY, never your own name/email --
browser autofill is the trap; real data voids the run. Root
cause: r4 (like r3) was set up as James McCoy/yahoo via
autofill, so its first screen was "Log in" not setup, and the
protocol's narration stopped matching the browser. r4 retained-
contaminated (real PII, same handling as r3/demo-p0). Rehearsal
restarts on data/cold-run-2026-08-03-r5.db. Ceremony coaching
(MFA note) is outside the M1->M5 measured leg, so it does not
distort the instrument.

REDESIGN ROUND 4 (James, structural insight): the failure mode
was the DOCUMENT SHAPE, not the wording -- steps in one place,
data cards in an appendix, forward references ("Card 1") to
material the linear reader hasn't reached. A runner executes a
protocol ONCE, top to bottom; reference-doc structure (separate
data section) fits re-reading, not execution. Task sheet
rewritten fully LINEAR: each data table is inlined in the step
that uses it (setup values in step 1 with the MFA narration,
Priya's contact fields in step 2, questionnaire values in step
5); the exactly-these-values / refuse-autofill / leave-blank
rules moved into the sheet preamble. Separate cards section
DELETED; dangling references fixed (setup step 3, pass-criteria
wording). check_cold_run.py unchanged -- values identical.
METHOD: four protocol redesigns tonight, every one triggered by
watching a real user collide with the artifact -- none were
predictable from the armchair. The instrument is being cold-run
before the product is.

VOCABULARY RULING (James, live): firm-facing UI says "Client",
not "Contact" -- the sheet said client (the user's word), the
screens said contact (CRM-speak); the mismatch is exactly the
translation cost the thesis targets. Display-string sweep of
app_ui (nav tab Clients, dashboard button + tally, New client
form heading/button/title, matter form+detail "Client" label,
indexes, empty states, search placeholder, linked-cell
fallback); routes (/contacts), db columns, casework module
names UNCHANGED (minimum edit -- rename is presentation-layer
only). Contact-form hint simplified to "A person -- not a
company." Walk expectation updated (run_ui_walk.py:177 "New
client"). Receipt: walk GREEN post-rename (13 pass, sweeps
pass). CAVEAT flagged: casework's contact model also holds
non-client people (preparers, companies) -- in seeded/demo
browse data a "Clients" index may list non-clients; acceptable
for v1 (cold-run dbs hold only Priya), revisit if browse-grade
surfaces ever carry mixed kinds. r5 run CONTINUES on the same
db (mid-run state clean: Casey Morgan account, Priya Sharma
contact); server restarted with renamed strings -- sessions are
db-backed, James just logs back in.

REHEARSAL 2 COMPLETE (r5, James, solo): check_cold_run.py EXIT 0
-- ARTIFACTS COMPLETE, 9/9, first clean run ever (rehearsal 1
was 7-missing; r2-r4 were contaminated before finishing).
Receipts db: data/cold-run-2026-08-03-r5.db.

Marks reconstructed from db stamps (UTC) + Downloads mtimes:
  install 11:34:14 | account 11:38:03 (M1~11:38:30 post-MFA) |
  contact 11:38:47 | matter 11:52:05 | invitation returned
  11:54:20 (M3) | PDF after-client 11:55 (M4, file mtime) |
  deadline attempts 12:02:44 (unlinked), 12:06:43 (unlinked),
  12:12:13 LINKED (M5).
M1->M5 ~33:40 -- TIMING VOID as instrument data: run was
interrupted by live UI surgery (label fix, Client rename +
server restarts, relogin), snap-taking, and agent coaching
throughout (would void proof many times over; fine for
rehearsal). Clean-leg times ARE meaningful: setup->contact
0:44; matter->returned intake ~2:15; review+download ~1:35.
The deadline leg consumed ~10 min and 3 attempts -- all
finding 8 (calendar-entry New deadline cannot link a matter;
hidden-query-param design). Rehearsal 2's headline: finding 8
is the dominant interaction cost on the anchor path.

Also observed (James experiments): PDF before/after diff proved
client-leg pipeline (3 fields changed, exactly the address adds;
withheld ZIP absent -- per-row Save confirmed, finding 7).
Deadline date arithmetic done correctly by runner (08-17 = two
weeks from 08-03).

FINDING 8 FIX (James ruled "let's try it"): New deadline form's
hidden matter_id param replaced with a VISIBLE Matter dropdown
(all live matters as "name -- client", preselected when arriving
from a matter screen; "-- no matter --" is a deliberate last
option, never the default -- defaulting to none would recreate
the trap). Hint line: "A deadline on a matter shows up on that
matter's screen." Create handler now derives contact_id from
the chosen matter's primary contact (authoritative) instead of
a second hidden param; no-matter events keep the query-param
contact fallback. reads.matter_row/list_matters used -- no new
SQL, no-logic lint intact. Walk POSTs matter_id explicitly so
verifier needed no change. Receipt: run_ui_walk.py GREEN (13
pass, sweeps pass). Server restarted on r5 for James's eyeball.

## 2026-08-03 -- PROJECT ON HOLD at the P4 recruiting gate

James's ruling, verbatim intent: no cold runner available right
now; he has tested the build himself and it meets his standards;
park the project and keep the portfolio moving. Hold, not
completion -- goal.md's binding oracle (a cold user completing
the anchor workflow unassisted inside the budget) is unmet and
UNCHANGED. Nothing in the contract is amended; the project stops
one gate short of verdict, deliberately.

Position at hold: P3 COMPLETE (gauntlet 19/19; protocol
ratified). P4 U4.1 blocked on recruiting, the one step goal.md
keeps in James's lane. Since the last state.md rewrite, the
prior session (worklog above) had banked: rehearsal 2 (r5,
James solo) -- check_cold_run.py EXIT 0, 9/9 artifacts, first
clean run ever (db data/cold-run-2026-08-03-r5.db; timing void
as proof, interrupted by live surgery, but clean-leg times
meaningful); Clients display rename (presentation-layer only);
finding 8 fix (visible Matter dropdown on New deadline, no-
matter never default). All folded into state.md at this hold.

Parking receipt, run this session: run_ui_walk.py GREEN --
"ui-walk: 13 pass, 0 pending, 0 fail; sweeps pass; verdict
GREEN", exit 0.

Resume condition: a qualified cold runner exists (never
operated ANY build, one run per person). Resume entry point:
state.md Next actions -- U4.1 run day per the ratified
protocol, unchanged.

METHOD: first formal HOLD in a goal-method project. The method
has no named hold state; the wind-down checklist absorbed it
cleanly (hold = wind-down whose status line says ON HOLD +
resume condition instead of a next-session pointer). Note for
retro: external-dependency gates (a human participant only the
human can source) are a blocker class the Blocker rule's
three-turn test never sees -- the agent is not stalled, the
world is. A hold state may deserve a name in the skill.
