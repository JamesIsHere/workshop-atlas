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
