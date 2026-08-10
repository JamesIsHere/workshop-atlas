# worklog.md -- casework-tabs (append-only)

## 2026-08-10 -- s1: bootstrap from the tab-review ledger

Session context: atlas-root session that ran the six-tab UI review
(../tab-review-notes.md) end to end, then James ruled "bootstrap
the build child now." Interview rulings, each taken one-per-turn:
name casework-tabs (over tabs-ui, surface-ui); mode PHASE-GATED
HYBRID (unattended within phases, hands-on gates between); oracle
per-tab hands-on gate verdicts PLUS a final cross-tab walk on a
fresh db with signed short verdict (over per-tab-only -- James:
tab-local review misses the seams).

Scaffolded via project-kit (folder + CLAUDE.md; Data-freshness
template section deleted -- no generated artifacts yet). goal.md /
plan.md / state.md / this file drafted in one pass from the ledger
per the ledger-as-interview pattern (casework precedent): the
review's rulings land as goal.md Appendix A; the in-place-extension
amendment lands as Appendix B DRAFT for James's ratification.

METHOD: second full ledger-as-interview instance. The interview
collapsed to exactly three questions (name, mode, oracle) because
the review ledger had already banked every design ruling -- the
bootstrap cost moved from interview to the review that produced
the ledger. Phase-gated hybrid chosen BY NAME from the skill's
modes section on its first day as a named mode (promoted this
morning, Trial 4 retro promotion pass).

METHOD: today's new doctrine applied at draft time, not
retrofitted: scope-bounded verdict pendency in Iteration and
recovery; world-blocked arm in the Blocker rule; self-audit
questions ratified in-contract (item e added for the ruling
queue); retro-rides-final-wind-down in P7; deferral-load check
queued for the ratification signature.

goal.md is UNRATIFIED. Red-pen next.

## 2026-08-10 -- s1 cont: RATIFIED after one round + deferral-load
## check

Red-pen round 1: four candidate kills primed (e-sign out of
contract; walk-budget gap; chrome-bar softening; permissions
view-only) -- James: "I say it looks good!" = four KEEPs. Per the
standing deferral-load rule the check ran before the signature:
4 keeps / 0 kills / 0 parks / 1 silent skip converted to a typed
deferral (final-walk time budget -> owed at P7 walk-sheet
ratification). Forward obligations typed and homed (walk budget ->
P7; e-sign P4b gate -> plan.md; interleaved timeline -> rendered-
artifact gate; calendar sync -> meeting queue; Appendix B + roster
+ ledger retirement -> this signature). Fences (config-depth six,
cold-run imports, new business logic, SMS) vs deferrals separated.
Counter-pressure named: second ledger-fed zero-kill ratification;
front-loaded reading has direct evidence this time (the review WAS
the red-pen -- 15+ rulings one call per turn, several against the
agent's lean: "both" on trash, "everything" on calendar reach).
James then signed explicitly: "yes".

Signature acts executed: goal.md header restamped RATIFIED;
Appendix B ratified into atlas/CLAUDE.md (program amendment
2026-08-10) + casework-tabs roster row added; tab-review-notes.md
RETIRED (archive header, next-child-notes precedent); CLAUDE.md
State table + state.md rewritten to pre-P0.

METHOD: deferral-load check's first outing as STANDING procedure
(promoted this morning); it converted a silent skip into a typed
deferral in real time -- the exact failure mode it exists to
catch. Bootstrap-to-ratification ran in one sitting on a ledger
fed by a same-day review; the four-file harness now holds a
ratified contract that has never had an unsupervised session.

## 2026-08-10 -- s2: U0.1 -- P0 harness built, rail driven RED

Built casework-tabs/verify/: run_tabs_walk.py (the rail, 30 steps),
seed_tabs.py (gate-review demo db, casework/app module calls only,
zero SQL writes), report_sha.py (canonical sha, billing-ui recipe).
No app_ui file touched -- oracle-first held: the rail exists and
runs RED before any screen work.

Rail design, on the billing-ui pattern plus one extension: the six
tab routes already exist as read-only casework-ui screens, so the
rail carries TWO Pending probes -- probe() (authed GET landing on
the 404 page = new route unbuilt) and expect_marker() (route lives
but the ruled redesign's contract marker is absent = Pending, never
FAIL). Markers are additive so the frozen run_ui_walk.py stays
true. Walk order follows phase order (P1 calendar ... P6 settings)
so gates see contiguous greens. The route names, form fields, and
marker hooks pinned in the step bodies ARE the P1-P6 interface
contract. Goal.md's three supporting checks live in the rail:
float sweep + ISO-stray sweep (runtime, tag-stripped pages of tab
steps only) in the report's sweep section; the empty-state sweep is
walk step 2 (fresh-db crawl; designed = <div class='empty-state'>
carrying the creating action).

RED run quoted: "tabs-walk: 2 pass, 28 pending, 0 fail; sweeps
pass; verdict ON TRACK (pending screens)", exit 1 -- exactly the
contracted P0 shape (foundation green, every tab step PENDING with
a named reason). x2 stable, canonical sha e084bd4b (report_sha.py).

Verify-the-verifier, four deliberate sabotages, each FAILed then
reverted: (1) setup-step label -> FAIL step 1; (2) client+matter
redirect regex -> "FAIL client + matter ... AssertionError:
http://127.0.0.1:55245/matters/1"; (3) injected page with visible
ISO date -> "FAIL iso-stray-sweep: strays: /leak: 2026-08-10";
(4) scratch file with float() + /100 -> float-sweep caught both
patterns. Owed forward: the empty-state FAIL arm (marker without
action) and each tab step's full body get their own deliberate RED
at the phase that builds them (per-phase rhythm step 1).

seed_tabs.py green: "3 users; 4 contacts; 4 matters; 8 events;
7 tasks; 4 notes; 4 files; 2 invoices" -- appointments with
attendees/end-times, expiry rules -> 3 auto events, 2 vmax dates,
invoices with due dates (all six calendar kinds represented),
task list with a reference-date item imported onto a matter, note
categories + pin + notify-all, e-sign draft + requested states,
recents, trash content. Disclosure: the seed touches billing
modules (operating account + 2 invoices) solely because the ruled
unified calendar shows invoice due dates; module calls only, demo
db lives under casework-tabs/data/ (gitignored).

Standing suites all green, quoted: "spine: 107 green, 0 red,
0 pending; checks pass" / "billing: 25 green ... verdict: GREEN" /
"fiduciary: 9 pass, 0 red, 0 stub; verdict: GREEN" / "ui-walk: 13
pass, 0 pending, 0 fail; sweeps pass; verdict GREEN".

[Q] ruling queue (for the P1 gate):
- [Q1] Derived calendar kinds (expiry, vmax, invoice-due) have NO
  UI creation path today: facts come from client intake, and the
  billing UI reads due_date but never writes it. The rail's
  derived-kinds step probes markers only until ruled. Options:
  (a) mirror the existing intake flow inside the walk, (b) give
  the New-deadline form a fact-writing variant (module call, no
  new logic), (c) a gate-ruled exemption letting the walk seed
  derived-kind content by module call. Agent lean: (b) for expiry/
  vmax -- it makes the deadline form genuinely useful -- plus (c)
  for invoice due dates only.

METHOD: oracle-first rail is now a three-peat pattern (billing-ui
-> period-close -> here); the new marker-probe arm existed because
this child REDESIGNS live screens rather than adding a fresh area
-- 404-probing alone cannot express "route exists, design pending."
Worth folding into the skill at the next retro if it survives P1.

## 2026-08-10 -- s3: P1 CALENDAR built to the rail; gate pending

Build (all inside the amendment's write surface): reads.py grew
five SELECT-only calendar readers (calendar_events with the fact
join for expiry provenance, calendar_vmax, calendar_task_dues,
calendar_invoice_dues, event_attendees); html.py grew the additive
chrome (chips, kind badges, month grid, designed_empty + mdy
helpers); server.py grew the unified /calendar (agenda + month
views, six kind chips, designed empty state), the two pre-shaped
create forms (/calendar/new-appointment, /calendar/new-deadline),
an extended event detail (kind badge, description, MM/DD/YYYY,
attendees section + add form, reminders intact), and POST
/calendar/<id>/attendees. Writes ride events.create_event /
add_attendee only; invoice status on the calendar derives via
billing.invoice_status (module call, fx-0070 discipline).

Design decisions (queued [Q] where interpretive):
- Deadline shape: starts_at = T00:00:00Z with no end -- kind is
  DERIVED (expiry_auto -> expiry; midnight-no-end -> deadline;
  else appointment). Chosen over a bare date string because the
  scheduler parses full timestamps; a date-only starts_at would be
  a data shape the frozen core chokes on.
- Month nav: Earlier/Later jump to the NEAREST MONTH WITH ITEMS --
  no empty scrolling, and the frozen walk's reachability BFS
  (which crawls every href) stays on a finite chain that reaches
  every event from any month.
- Sticky view rides a cal_view cookie (presentation state, no db
  write). [Q4]
- Frozen-walk fences held: /calendar/new untouched (its "New
  deadline" h1, reminder picker, and redirect intact); "2 days
  before" wording preserved on the detail; fresh-db /calendar
  still renders "hint empty" (inside the new designed empty
  state) with zero <td>.

Verify-the-verifier EARNED ITS NAME this session -- three rail
defects found and fixed while driving steps RED:
1. False PASS: the derived-kinds step passed with zero derived
   content because "kind-expiry" matched the global STYLESHEET,
   not a row. All kind markers tightened to the rendered form
   ("class='kind kind-X'"); provenance marker to
   "class='provenance'" (was also substring-weak: "provenanceX"
   and the CSS rule both contained it).
2. ISO-stray false hits: the <style> block's text survives
   tag-stripping; the sweep now strips style blocks first (they
   are never user-visible), and the shipped CSS comment lost its
   date.
3. METHOD: a marker-probe step whose marker REGRESSES away demotes
   to PENDING, not FAIL (same property as billing-ui's 404
   probes). Consequence for gates: the floor is read from the
   per-step table, never the verdict line alone -- a P1 step
   showing PENDING at a later gate is a regression wearing
   pending's clothes. Gate receipts must quote the full table.

Sabotage lineage this session (all reverted): title-field,
date-field, filter-ignored, cookie-ignored, matter-link-corrupted
-- five hard FAILs proven; the two marker-removal sabotages
correctly demoted to PENDING (finding 3).

Rail after build: "tabs-walk: 7 pass, 23 pending, 0 fail; sweeps
pass; verdict ON TRACK (pending screens)", sha d1a45962 x2
(supersedes e084bd4b, this rail's P0 baseline). Standing suites
all green, quoted: "ui-walk: 13 pass, 0 pending, 0 fail; sweeps
pass; verdict GREEN" / "spine: 107 green, 0 red, 0 pending" /
"billing: 25 green ... GREEN" / "fiduciary: 9 pass ... GREEN".

[Q] ruling queue for the P1 gate (serialized one per turn there):
- [Q1] derived-kinds content path (s2; agent lean: deadline-form
  fact variant for expiry/vmax + seeding exemption for invoices).
- [Q2] calendar shows OPEN tasks only; completed drop off.
- [Q3] calendar shows UNPAID invoice due dates only.
- [Q4] sticky view is per browser (cookie), not per user account.
- [Q5] agenda default = full range, no date window; month view is
  the windowed read.
- [Q6] kind badge vocabulary (one rendered proposal: blue
  appointment / red deadline / orange expiry / green task / purple
  vmax / teal invoice).
- [Q7] calendar index leads with the two new create paths; the old
  /calendar/new stays for the matter-page flow (frozen walk).
- [Q8] appointment form carries no per-form reminder picker; firm
  default reminders apply (Settings home lands P6).

Gate logistics: port 8500 is currently held by billing-ui's demo
server (James's asset, PID noted in session); the swap to
data/demo-tabs.db behind the same port is his call at the gate.

## 2026-08-10 -- s3 cont: P1 gate live-drive, spacing axis settled

James authorized the 8500 swap (billing-ui server down -- a stale
watchdog from its old session tried to restart it and failed;
port stayed ours). Demo db regenerated, server up, James drove.

Three gate-fed polish rounds on the crowding/spacing axis (gate
feedback, not agent-judgment iterations -- anti-stall cap
untouched):
- r1 (commit 3a899e9): agenda When column stacks date over muted
  time (mid-range wrap killed); Linked column reduced to ONE
  matter-first link (redundant "matter -- client" pair was the
  wrap driver; flagged for re-rule, James did not object); month
  cells: color dot + title instead of full badge words.
- r2 (fd05d70): server-side 20-char chop removed in favor of CSS
  ellipsis -- DID NOT WORK: auto table layout grows cells, the
  clip never engages, titles bled across day borders. James's
  snap caught it.
- r3 (0fe8d3c): table-layout fixed (ellipsis engages), month view
  renders on a wide main (92rem), color KEY legend under the grid
  (James's direction: "use the colors to reduce the text and add
  a key"). James: "We got the spacing right."

Clarified at his question: month cell text is the item TITLE per
kind (never the matter); matter/client linkage lives in the
agenda's Linked column and on detail pages only.

Parked with triggers (log-don't-build, James: "leave it for now,
things will change"):
- "+N more" cell overflow (Outlook pattern) -- trigger: real
  density makes cells stack past ~3 entries.
- Matter/client name in month cell or hover -- trigger: James
  asks, or the final cross-tab walk shows scan-time confusion
  about whose item is whose.

Rail 7 pass / 0 fail and ui-walk GREEN re-quoted after every
round; sha d1a45962 held through r1 (layout-only), unchanged
through r3 (no asserted strings touched).

METHOD: the r2 miss is a verify-the-verifier lesson in the OTHER
direction -- the rail cannot see CSS-rendering truth (it asserts
markup, not layout), so gate snaps are the only oracle for visual
defects. The hands-on gate medium rule (screenshots support,
James drives) earned its keep three times in one hour.

## 2026-08-10 -- s3 close: P1 GATE PASSED

Two more gate exchanges after the spacing close: (1) James asked
what the month-cell text IS -- answered from code (item title per
kind, never the matter; matter/client rides agenda Linked +
detail only); the matter-in-cell idea was already parked. (2) He
asked for the full font inventory -- answered from the STYLE
block; the table surfaced that in-table links were the only
UNSTYLED text on the page (browser-default blue/purple). His
ruling: one text size for the whole table (the Linked size,
0.85rem) and links firm blue always -- built as r4 (6903336),
scoped to calendar surfaces; app-wide extension flagged as
touching billing-ui's signed tables, not taken.

VERDICT: PASS, signed "Yes we are done." Receipt with the FULL
step table at verify/gate-receipts/p1-calendar.md. [Q1]-[Q8]
carry forward to the P2 gate by his wrap-up call -- all are
implemented defaults that stand unless re-ruled.

First push to the GitHub remote (origin) rides this close at
James's explicit request.

METHOD: the gate produced FOUR ruled outcomes without ever
touching the prepared [Q] queue -- live product questions
("what is this text", "what are the fonts") turned into rulings
faster than the queued abstractions would have. The queue's
value may be as a safety net behind a hands-on drive, not the
agenda for it.

## 2026-08-10 -- s4: P2 TASKS built to the rail, gate staged

Per-phase rhythm held: rail refined first, driven RED per step,
screens built to green, suites rerun.

Rail refinements (verify-the-verifier, both recorded in-step):
- step_tasks_quick_add: the sketched POST /tasks/<id>/due is
  IMPOSSIBLE rendering-only -- the frozen core has no due-date
  setter (tasks.create_task takes due_date at creation; nothing
  updates it). The quick-add form carries an OPTIONAL due date
  instead; the step now asserts the form field, MM/DD/YYYY render,
  ISO storage, and the calendar ride. [Q9]
- step_tasks_lists: the old closing assert (list name on the matter
  page as "automation linkage") was VACUOUS -- the Import select
  renders every list name, so it passed with zero linkage rendered;
  and tasks store no source-list column, so a task cannot name its
  list post-import (schema truth). Automation linkage per the
  schema is matter_statuses.auto_task_list_id -> rendered in the
  BUILDER (Automations column + per-list note); the step probes the
  class='automations' marker, asserts the imported items and the
  missing-ref-fact -> no-due-date behavior instead. [Q10]

Build (all writes ride casework's tasks module; SQL in reads.py):
- /tasks rebuilt: my-open default, Mine/Firm + Open/Completed chips
  (one click, never partitioned), type-and-Enter quick-add with
  optional due date, one-click Done per row (back-field returns the
  driver to the page they pressed it on), assignees column, due
  MM/DD/YYYY, designed empty states per view.
- /settings/task-lists builder (machinery home; re-homes into the
  Settings layout at P6): create list, list detail with add-item
  form (position, duration OR reference rule from contact date
  facts, default assignee), rules written in words ("due 30 days
  before EAD expiry"), Automations column + per-list note.
- Matter + contact pages grow a Tasks card: open tasks + Import
  Task List select (form absent until a list exists -- marker
  stays honest). Task detail: Done button, completed pill with
  date, due MM/DD/YYYY.
- Matter detail's other dates (Form packages Created, Deadlines
  When) went MM/DD/YYYY in the same pass -- an existing-screen
  sibling-defect extension under the goal.md date constraint
  (contact-card precedent, gate ruling 2026-08-10); disclosed for
  re-rule. [Q11] The ISO sweep now covers the matter page (fetched
  by step_tasks_lists) and passes because of it.

RED drives (five, all reverted): ISO due render -> step FAIL +
ISO-sweep FAIL (caught twice); Completed chip removed -> FAIL;
complete no-op -> FAIL; raw fact key in the rule -> NOT CAUGHT
(the item title contains "EAD" -- the assert was vacuous), rail
tightened to pin the full rule phrase, sabotage rerun -> FAIL;
bare /tasks empty state -> step-2 FAIL (the owed empty-state FAIL
arm, now proven).

METHOD: sabotage 4 is the session's verify-the-verifier lesson --
a green-first build hides vacuous asserts; only the RED drive
exposed that "EAD" lived in the item title. The deliberate-RED
owed-per-phase rule caught a rail defect that two clean x2 runs
never would have.

Rail after build: "tabs-walk: 11 pass, 19 pending, 0 fail; sweeps
pass; verdict ON TRACK (pending screens)", sha eb4fc42e x2
(supersedes d1a45962). Standing suites all green, quoted:
"spine: 107 green, 0 red, 0 pending" / "billing: 25 green, 0 red,
0 pending, 0 parked; checks pass; verdict: GREEN" / "fiduciary:
9 pass, 0 red, 0 stub; verdict: GREEN" / "ui-walk: 13 pass,
0 pending, 0 fail; sweeps pass; verdict GREEN".

Gate staging: stale P1 demo server (PID 12364, our own) killed;
seed extended with a workflow automation demo (Evgenia Synthetic:
matter type "SYNTH I-130 Family", status "SYNTH Opened"
auto-imports the checklist at matter creation -> unassigned tasks
show the Mine/Firm split live; her EAD fact drives the computed
reference due date); demo-tabs.db regenerated (3 users, 5
contacts, 5 matters, 10 tasks); server restarted on port 8500,
answering.

[Q] queue for the P2 gate (join carried [Q1]-[Q8]):
- [Q9] due date is create-time only (quick-add field); editing an
  existing task's due date/title/assignees needs a core amendment
  -- seek one or accept create-time-only?
- [Q10] automation linkage renders in the builder (schema truth);
  workflows have no UI (config-depth kill), so linkage content
  appears only on seeded dbs -- accept, or does that argue for a
  workflows surface some phase?
- [Q11] matter-page date format extension (existing screen) --
  ratify or revert.

## 2026-08-10 -- s4 cont: P2 gate live-drive, feedback r1

James: "can we get the fonts to line up with what we did on
calendar." The P1 typography ruling (one td text size at 0.85rem,
links always firm blue) extended to the four tasks tables (/tasks
index, builder index, list-detail items, matter/contact Tasks
cards) via a .tasks-table wrapper -- same scoping pattern as
.agenda; billing-ui's signed tables still untouched. Rail 11
pass/0 fail sha eb4fc42e (unchanged -- no asserted strings moved),
ui-walk GREEN, demo server restarted on 8500 with the change.

P2 gate feedback r2 (James accidentally completed a task at the
live drive): "we need an undo or something... also like a check
box so clicking done is not so easily done." RULING SUPERSESSION:
Appendix A's one-click complete is overridden by the ratifier --
completing is now two actions (row checkbox, native required,
zero JS + Done); rail step renamed tasks: confirm-complete and
pins the checkbox markup. Sha 0193bb09 x2 (supersedes eb4fc42e:
step rename + new assert). ui-walk GREEN. Undo half of the ask is
BLOCKED rendering-only: the frozen core has no reopen function
(completed_at set-only, same family as [Q9]); nothing is lost
(completed tasks live under the Completed view) but un-completing
needs a core amendment -- put to James as the gate question,
[Q12].

METHOD: my first sabotage of the checkbox was a blind
str.replace one-liner whose pattern matched NOTHING -- silent
no-op, rail stayed green, and only suspicion caught it. That is
the evidence-discipline rule (fail loud, no error-tolerant
probing) violated in miniature; sabotages via Edit-with-known-
content only from here.

P2 gate feedback r3 -- [Q12] RULED, core amendment ratified
(James: "yes I think we have to, it will happen"). Program
amendment recorded in ../CLAUDE.md: tasks.reopen_task is the ONE
authorized post-freeze casework touch (clears completed_at; audit
rides trg_tasks_au, verified present before claiming it). UI:
Reopen button on completed rows + completed task detail
(one-click on purpose -- reopening resurfaces work, cannot lose
any); POST /tasks/<id>/reopen. Rail: confirm-complete step drives
reopen through the UI and asserts the machinery (completed_at
NULL + >=2 update audit rows); driven RED via reopen-no-op
sabotage, reverted. Sha ae9bdf90 x2 (supersedes 0193bb09).
RECIPROCAL GUARD rerun after the core touch, all quoted: "spine:
107 green, 0 red, 0 pending; checks pass" / "billing: 25 green,
0 red, 0 pending, 0 parked; checks pass; verdict: GREEN" /
"fiduciary: 9 pass, 0 red, 0 stub; verdict: GREEN" / "ui-walk:
13 pass, 0 pending, 0 fail; sweeps pass; verdict GREEN". Seed
gains a visible completed task ("SYNTH confirm biometrics
attendance" -- the prior completed one rides into trash) as the
gate's Reopen target; demo regenerated (11 tasks), 8500 up.

P2 gate feedback r4 (from James's snaps -- his drive, my catch,
his "yes"): the tasks Linked column carried the redundant
matter+client pair the P1 calendar gate killed; cut to the
matter-first single link (_linked_one) on the tasks index and
task detail. Files/notes indexes keep the old two-link cell until
their own phases rebuild them (scoped discipline, same as the
typography rulings). Rail 11 pass/0 fail, sha ae9bdf90 unchanged
(no asserted strings moved); ui-walk GREEN; server restarted.

## 2026-08-10 -- s4 close: P2 GATE PASSED

VERDICT: PASS, signed "PASS!". Receipt with the FULL step table at
verify/gate-receipts/p2-tasks.md. Four live rounds (r1 typography,
r2 confirm-complete SUPERSEDING Appendix A's one-click, r3 the
RATIFIED reopen_task core amendment + reciprocal-guard rerun, r4
matter-first single link). [Q12] ruled at the gate; [Q1]-[Q11]
carry to P3 by the same standing-defaults disposition as P1.

METHOD: second gate running the P1 pattern -- the prepared [Q]
queue again went untouched while the live drive produced four
rulings, one of them a program-level amendment. Two gates in, the
queue's role is confirmed as safety net, not agenda. His snaps
also earned a new role: r4's defect (redundant link pair) was
visible ONLY in his screenshots -- the rail asserts markup
presence, not visual redundancy.

## 2026-08-10 -- s5: P3 NOTES built to the rail, gate staged

Rhythm held: rail refined first, build to green, five RED drives,
suites, gate staged.

Rail refinement (the P2 sabotage-4 lesson applied BEFORE building
this time): step_notes_timeline_pin's P0 check only found the memo
somewhere in the timeline -- true before the pin too, so a broken
pin would have passed. Refined: a second newer matter note makes
ordering observable (newest-first pre-pin; pinning the OLDER memo
must lift it above the newer entry; core pinned=1 asserted). The
pin-no-op RED drive then proved exactly that catch.

Build (writes ride casework's notes module; SQL in reads.py):
- /notes rebuilt: minimal capture (body textarea + Save; no
  type-and-Enter -- Enter is newline in a textarea, capture is
  body+save per Appendix A), link to the full form (/notes/new:
  title, body, category, matter/client, extra assignees,
  notify-all); ALL default pinned-first; All/Mine + per-category
  chips; ruled table style (0.85rem, blue links, matter-first
  single link, MM/DD/YYYY).
- Matter + contact pages grow a Notes TIMELINE card (pinned on
  top then newest, left-rule accent on pinned), an in-place quick
  capture (hidden scope fields; matter capture associates matter
  + primary contact via the core's own scoping), Pin/Unpin per
  entry, and Export notes PDF as a form BUTTON deliberately --
  an <a href> would put binary bytes in the frozen walk's BFS
  crawl path.
- /settings/note-categories home (machinery home, re-homes at
  P6): create by Enter, table with kind + live note counts.
- Note detail rebuilt: pin toggle, single link, assignees,
  MM/DD/YYYY.

RED drives (five, all reverted): category-create no-op -> FAIL;
quick-capture no-op -> FAIL; pin no-op -> FAIL (the refined
ordering assert; P0's would have passed); category-filter
ignored -> FAIL; fake PDF bytes -> FAIL.

Rail: "tabs-walk: 16 pass, 14 pending, 0 fail; sweeps pass",
sha 157f5ac1 x2 (supersedes ae9bdf90). Standing suites all green,
quoted: "spine: 107 green, 0 red, 0 pending; checks pass" /
"billing: 25 green ... GREEN" / "fiduciary: 9 pass ... GREEN" /
"ui-walk: 13 pass, 0 pending, 0 fail; sweeps pass; verdict
GREEN". Demo regenerated fresh (James's P2 test artifacts wiped
per demos-from-fresh-dbs rule), server restarted on 8500.

[Q] for the P3 gate (joins carried [Q1]-[Q11]):
- [Q13] the notes PDF (frozen core export_notes_pdf) prints raw
  ISO timestamps inside the document -- a user-facing date-format
  defect that would need a core amendment (same shape as Reopen)
  or stays as-is; capability bar is met either way.

P3 gate feedback r1 (James's snap): the note detail's Linked link
rendered browser-default visited purple -- the P1-killed defect
class, but the blue pin was table-scoped and this is a kv line.
Fixed on the note detail (this phase's screen: card gains
tab-detail, .tab-detail .kv a pinned firm blue -- scoped class,
NOT a global .kv a, which would repaint billing-ui's signed kv
surfaces). Task detail and calendar event detail carry the SAME
purple on their kv links; they are passed screens, so extending
the class there is queued for James's call at this gate. Rail 16
pass/0 fail sha 157f5ac1 unchanged; ui-walk GREEN; server
restarted. His questions (PDF / attachments) answered from corpus
+ schema ground truth: notes.notes-export exists and is built;
NO attachment capability anywhere in corpus/notes.md and no
note-file linkage in the schema -- answer stands on both reads.

P3 gate feedback r2 (James's snaps): (a) the pdf option lived
only on the linked-to page -- the note detail now carries the
export scoped to its linkage, button labeled with whose notes it
produces (matter first, else client; unassociated notes get no
button -- the core export is scope-based and a single-note PDF
stays a core-amendment question). Rail pins the note-page export
(driven RED via suppressed-button sabotage). (b) His task-detail
snap showed the same visited-purple kv link queued at r1 -- the
tab-detail blue extends to task detail AND calendar event detail
(both gate-passed screens; extension disclosed here for the
receipt). Sha d2c65ac8 x2 (supersedes 157f5ac1: new assert +
detail message); ui-walk GREEN; server restarted.

## 2026-08-10 -- s5 close: P3 GATE PASSED

VERDICT: PASS, signed "pass". Receipt with the FULL step table at
verify/gate-receipts/p3-notes.md. Two live rounds (r1 detail blue
links, r2 note-page export + task/event detail extension); the
gate also carried a product-purpose exchange (what notes are FOR)
and two capability questions answered from corpus + schema reads,
not memory. Attachments and single-note PDF PARKED with triggers;
[Q1]-[Q11] + [Q13] carry to P4.

METHOD: third gate, same shape -- the queue untouched, rulings
born from his driving + snaps. New this gate: the snap channel
caught TWO defects the rail structurally cannot see (visited
purple, missing affordance on a page the rail asserts by marker
not by completeness). Snaps are now a first-class gate oracle
alongside the hands-on drive.

## 2026-08-10 -- s6: P4a FILES MECHANICS built to the rail

Rail refined FIRST (per-phase rhythm step 1), four steps -> five
(e-sign split prepare/sign to match the staged P4a/P4b gates;
plan.md updated). Refinements, all from ground-truth reads of the
frozen core (files.py, esign.py, the client surface in
casework/app/server.py):
- upload custody assert was a page-wide "firm" -- vacuous once P6
  adds href='/settings/firm'; pinned as the rendered kv pair
  <dt>Source</dt><dd>firm</dd> plus db source='firm'.
- matter-section assert now searches inside the files-section
  slice (the P3 timeline pattern).
- manage step probed nothing before acting -- an unbuilt surface
  read FAIL, not PENDING; the controls' home is pinned first
  (rename form + preview/print links on the detail page). Bulk
  zip now OPENED, entries + content asserted -- the bare PK magic
  passed any zip.
- e-sign step scraped the outbox for an absolute URL: the frozen
  core mails the RELATIVE /esign/<token> (request_signatures), so
  the old assert could NEVER pass against a correct build.
  Refined to schema truth (relative path in the outbox row) plus
  the intake precedent: the STAFF page renders the live absolute
  link (client_base). The sign step now extends THROUGH the
  frozen client surface's real flow (field_<id> inputs,
  typed-mode JSON) to completed status, produced custody of the
  stamped copy, and source-filter narrowing -- observable only
  once a produced file exists, so the narrowing assert lives
  there, not in the presence-only filter step.
- esign.prepare WRITES -- the editor is entered by POST from the
  PDF detail; the txt detail must NOT offer the control (the
  core's PDF-only rule surfaces as absence, not as a 400 at the
  drive).

Refined rail on the unbuilt surface: 16 pass / 15 pending / 0
fail -- clean PENDING, no false arms.

P4a BUILD (casework-ui/app_ui under the 2026-08-10 amendment;
rendering only, writes through app.files):
- /files index rebuilt: multipart upload (matter/client selects),
  filter row (matter, client, source, e-sign status -- source
  filtered in Python over the core reader's rows; list_files has
  no source arg, no new SQL), bulk zip via checkbox form-attr
  (zero JS), e-sign status column, designed empty state carrying
  the upload form, files-table typography (0.85rem + firm blue,
  rulings adopted with the rebuild), mdy dates (the old index
  rendered raw ISO; sweep now covers these pages -- 65 clean).
- file detail rebuilt: SHA-256 kv (custody), rename-in-place,
  Preview/Print links for the core's preview types only (an
  unsupported type never offers a link that would error),
  tab-detail blue links, active nav.
- matter AND contact pages gain a files-section card (the
  scope's files + in-place upload posting back). The contact
  card is a disclose-and-extend: the rail pins matter only --
  flagged for the gate.
- make_server exposes storage_dir; the multipart parser mirrors
  the frozen client surface's (duplicated by design).

RED drives (Edit-with-known-content, one per new-green step):
sha truncated on detail -> FAIL "sha256 not visible"; matter
filter no-op -> FAIL "did not narrow"; bulk zip first-id-only ->
FAIL "zip entries: ['SYNTH-civil-documents-v2.txt']" -- caught by
the refined entries assert; the old PK check passed this exact
sabotage. Each reverted, rail green after.

Rail: "tabs-walk: 20 pass, 11 pending, 0 fail; sweeps pass;
verdict ON TRACK (pending screens)", sha 81168b79 x2 (supersedes
d2c65ac8). Standing suites all green, quoted: "ui-walk: 13 pass,
0 pending, 0 fail; sweeps pass; verdict GREEN" / "spine: 107
green, 0 red, 0 pending; checks pass" / "billing: 25 green, 0
red, 0 pending, 0 parked; checks pass; verdict: GREEN" /
"fiduciary: 9 pass, 0 red, 0 stub; verdict: GREEN". Empty-state
FAIL arm not re-owed (/files is the P2-proven pattern). Seed
gains one produced-custody file (the source filter's produced
arm is live at the gate; the client arm needs the intake flow,
out of a seed's reach by design). Demo reseeded (5 files); s5's
demo server SURVIVED its session and held the db lock (PID
36600, killed); 8500 up over data/demo-tabs.db.

METHOD: the refine pass earned its keep BEFORE the build, twice
-- the outbox-absolute-URL assert was structurally unpassable (a
step that could only ever FAIL against a correct build), and the
zip PK-magic assert provably passed a broken zip. Both defects
were found by READING the frozen code, not by running it:
discovery-against-ground-truth is a rail DESIGN step, not just a
build rule.

## 2026-08-10 -- s6 (cont): P4a GATE PASSED + P4b E-SIGN built

P4a VERDICT: PASS, signed "yes pass" -- FIRST gate with zero fix
rounds. Receipt with the full step table:
verify/gate-receipts/p4a-files.md. The gate carried one
product-purpose exchange (is Files a catch-all / does uploading
feed the data model), answered CLOSED from ground truth: custody
surface over three sources, data flows facts -> produced PDFs
(never the reverse), no extraction machinery in the core, and
docketwise-iq has zero footprint in the ratified spine --
ingestion is a new-child-if-ever-wanted, attaching at intake
document requests, not the Files tab. Disclosures (contact files
card, preview-types-only links, upload landing) accepted with
"as is".

P4b BUILD (same session, straight after the verdict):
- reads.py gains ONE reader (esign_row: latest live e-sign row
  per file -- no core home); signers/fields read via the core's
  own signers_of/fields_of.
- file detail (PDF only): Prepare-for-e-signing POST (the core's
  PDF-only rule surfaces as absence on other types), then an
  e-Signature section per state -- draft: Continue preparing;
  requested: LIVE signer links (client_base + /esign/<token>,
  the intake precedent) + signing status; completed: link to the
  auto-filed signed copy.
- prep editor at GET /files/<id>/esign (entered by POST prepare
  -> redirect; no live row = 404): signers table + add-signer
  (contact select), fields table + place-field (type/page/x/y,
  signer select), Send signature requests. Non-draft states
  render read-only truth (core refuses edits; no control that
  would error).
- POST routes prepare/signers/fields/request all call app.esign
  and redirect; the signer side is the FROZEN client surface,
  untouched.

RED drives (2 owed, both caught): PDF-only gate broken (txt
offers prepare) -> FAIL "non-PDF detail offers e-sign prepare";
staff live link token truncated -> FAIL "staff link is not this
signer's". Reverted, green after.

Rail: "tabs-walk: 22 pass, 9 pending, 0 fail; sweeps pass;
verdict ON TRACK (pending screens)", sha c44c5e31 x2 (supersedes
81168b79). Suites all green, quoted: "ui-walk: 13 pass, 0
pending, 0 fail; sweeps pass; verdict GREEN" / "spine: 107
green, 0 red, 0 pending; checks pass" / "billing: 25 green, 0
red, 0 pending, 0 parked; checks pass; verdict: GREEN" /
"fiduciary: 9 pass, 0 red, 0 stub; verdict: GREEN". Demo
reseeded (unchanged content: g28 draft + retainer requested give
the gate both prep states; James produces the completed state
himself by signing via the live link). 8500 restarted on the new
code.

METHOD: the walk's sign step drives BOTH servers in one assert
chain -- staff surface renders the link, an un-authed Browser
follows it to the frozen client surface, signs, and the staff
surface then shows the produced custody. Cross-surface
round-trips are rail-able; nothing about them requires a human.

P4b gate feedback r1 (James's snaps, mid-drive): preview and
print view were IDENTICAL -- true by construction: for viewable
types both routes serve the same bytes inline; Docketwise's
distinction (modal vs raw tab) does not exist in a zero-JS
build. Fix: ONE Preview control on the detail; the app_ui print
route retired (the capability -- displayable content in a tab,
fx-0195 -- is the preview tab itself; printing is the browser's
print from there; core print_view untouched). Rail manage step
refined to match (print asserts left with the second button).
Rail 22 pass/0 fail sha 35553738 x2 (supersedes c44c5e31);
ui-walk GREEN; 8500 restarted. His drive confirmed download
fine; prep-page question answered (Continue preparing = the
prep editor; his snap showed it working).

P4b gate feedback r2 (James, live drive): he placed a DUPLICATE
field -- no remove/edit existed on the prep editor. The core
already had it (esign.remove_field, draft-only, "the trashcan
icon"); rendering had no button. Fix: Remove control per field
row (draft only; locked editors render none), route + handler
calling the core; rail's prepare step gains a place-stray-then-
remove arm (RED-driven: no-op remove -> FAIL "removed field
still in the core"). Editing-in-place has NO core setter: edit =
remove + re-place, stated in the new hint. ALSO landed, from the
r2 exchange (disclosed, his verdict rules): the coordinate hint
(PDF points, bottom-left origin, 612x792, Y~120 for signatures)
+ a Preview link on the prep editor -- the X/Y opacity was the
one element that failed his "everything justifies itself" bar.
X/Y now render :g (100, not 100.0). Sha fd5ea835 x2 (supersedes
35553738); ui-walk GREEN; 8500 restarted.

P4b gate feedback r3 (James, live drive): he SIGNED and got the
raw core contract back -- "Expecting value: line 1 column 1" --
a human typing a name into the signature box hits json.loads in
esign._validate_value. The client sign surface was built under a
machine oracle (spine tests post the JSON payload; so did this
rail's sign step) -- no oracle ever typed into the box until his
drive. Same shape as Reopen: the hands-on gate exposing a path
automation structurally could not see. RULING ratified ("yes
proceed"), recorded in atlas/CLAUDE.md: the frozen client e-sign
surface (_esign_page + _esign_sign ONLY) opens for one
human-usability change. Fix: the sign handler wraps a plain
typed value for signature/initials into the typed-mode JSON
(structured JSON passes through; esign.py untouched); the sign
page gains human prompts. Reciprocal guard EARNED ITS KEEP: the
first label version replaced the pinned format and spine went
106/1 red (test_esign pins "signature (page 1)" verbatim,
immutable) -- prompts now APPEND to the pinned label instead.
Rail's sign step switched to the PLAIN typed-name path + prompt
assert (RED-driven: wrap disabled -> FAIL "sign POST failed",
reproducing his exact defect). Rail 22 pass/0 fail sha fd5ea835
x2 (report byte-identical to r2 by construction -- the new
asserts live in the rail, not the report; sha unchanged). Suites
all green, quoted: "entries: 111  green: 107  red: 0  pending:
0  parked: 4" / "billing: 25 green, 0 red, 0 pending, 0 parked;
checks pass; verdict: GREEN" / "fiduciary: 9 pass, 0 red, 0
stub; verdict: GREEN" / "ui-walk: 13 pass, 0 pending, 0 fail;
sweeps pass; verdict GREEN". 8500 restarted (client surface
rides the same process).

P4b gate feedback r4 (James, live drive): a SENT request was a
dead end -- he needed to undo and redo his locked attempt. No
core amendment needed: esign_files was declared soft-deletable
in the schema generator from day one and the generic trash
module covers every tombstoned table -- the undo is RENDERING
over existing machinery. Built: Void control on the file
detail's e-sign section (draft + requested; completed is
custody, never voidable), confirm checkbox per the P2
stray-click ruling, handler = trash.soft_delete("esign_files").
DISCLOSED EXTENSION under the r3 ruling (_esign_page in-scope):
the client page's esign_files read gains the deleted filter, so
a VOIDED link 404s ("This link is no longer available") instead
of rendering a form that errors on submit -- esign.sign already
refused deleted rows at the core; the page now matches. Rail's
prepare step gains the full arm: request -> void (markup-pinned
confirm) -> tombstone asserted -> OLD LINK 404s at the client
surface -> full redo to requested on a fresh token (old-token
reuse asserted against). RED-driven: no-op void -> FAIL "voided
PDF does not offer Prepare afresh". Rail 22 pass/0 fail sha
4f3a5880 x2 (supersedes fd5ea835). Suites all green, quoted:
"entries: 111  green: 107  red: 0  pending: 0  parked: 4" /
"billing: 25 green, 0 red, 0 pending, 0 parked; checks pass;
verdict: GREEN" / "fiduciary: 9 pass, 0 red, 0 stub; verdict:
GREEN" / "ui-walk: 13 pass, 0 pending, 0 fail; sweeps pass;
verdict GREEN". 8500 restarted.

P4b gate feedback r5 (James, live drive): after voiding, his
REDO went prepare -> Send with ZERO signers -- the frozen core's
request_signatures loops over nobody, emails no one, and still
locks draft->requested, leaving a request with no link to show.
His question ("wouldn't the link be here?") was answered from
the db, not memory: demo-tabs row 4 = requested, 0 signers, 0
fields. Two rendering fixes: (a) the editor offers Send ONLY
once a signer exists ("Add a signer before sending" hint
otherwise) and the request handler refuses an empty direct POST
(upload-requires-file pattern; core untouched); (b) the file
page's requested state with zero pending signers states the
vacuum ("No one is on this request -- void it and prepare again
with a signer") instead of silence -- reachable only on pre-r5
dbs now. Rail's prepare step restructured: post-prepare editor
asserts Send ABSENT + hint present, direct no-signer POST
asserted refused (status stays draft), Send appears after the
first signer. RED-driven: guard disabled -> FAIL "no-signer
request went out (status 'requested')" -- his exact state
reproduced. Rail 22 pass/0 fail sha 05ffb243 x2 (supersedes
4f3a5880); ui-walk GREEN (app_ui-only round). 8500 restarted.

P4b gate feedback r6 (James's snaps + db forensics): his no-box
signing reconstructed from the db, not memory -- es 5, the
REDONE retainer: signer added, ZERO fields, r5's guard checked
signers only, Send went out, the signer page (his bab89086
snap) rendered no inputs, one button-press "signed", the core
completed and filed a stamped copy with nothing stamped. A
VACUOUS signature in produced custody. Second pre-guard
artifact: es 3 (g28-anya-filled) requested w/ 0 signers.
Fixes (rendering only): (a) Send requires every signer to have
at least one field -- editor hint names who lacks one ("a
signer with nothing to fill would sign an empty page"), handler
refuses the direct POST; (b) his label ask verbatim: the add
button is now "Add signer / get client link" (it took him
forever to realize signer -> Send -> link was the path). Rail's
prepare step: r5's Send-present-after-signer assert FLIPPED
(absent until the field lands), field-less direct POST asserted
refused, Send-present asserted only after the field. RED:
field-guard disabled -> FAIL "field-less request went out
(status 'requested')" -- his exact path reproduced. Rail 22
pass/0 fail sha 3fcf00d3 x2 (supersedes 05ffb243); ui-walk
GREEN (app_ui-only round). 8500 restarted. Demo db keeps his
artifacts mid-gate (fresh reseed at gate close per standing
rule); the vacuous completed retainer is demo-only and dies at
reseed.
