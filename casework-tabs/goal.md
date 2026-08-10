# goal.md -- casework-tabs

RATIFIED by James 2026-08-10 ("yes" after the deferral-load check;
one red-pen round, four candidate kills all ruled KEEP, walk-budget
gap typed as a deferral homed at P7 sheet ratification). Appendix B
ratified into atlas/CLAUDE.md the same signature. Interview rulings
(2026-08-10): name casework-tabs; mode PHASE-GATED HYBRID; oracle =
per-tab hands-on gates + final cross-tab walk. Design rulings folded
from ../tab-review-notes.md (retired at this ratification).

## Outcome

The six nav tabs -- Calendar, Files, Tasks, Notes, Search, Settings
-- are DESIGNED working surfaces over the frozen casework core, not
read-only windows. Verification, not a task list:

1. Each tab passes its hands-on gate: James drives the tab's live
   screens at its phase gate and signs PASS, with any FAIL naming
   the fix axis (correctness / layout / orientation / wording).
2. The mechanical floor is green and quoted at every gate: this
   child's per-tab walk verifiers plus ALL standing suites (spine,
   billing, fiduciary --seeded, casework-ui run_ui_walk).
3. The contract closes on a final James-driven CROSS-TAB WALK on a
   fresh seeded database, entirely via screens -- schedule an
   appointment and a deadline, upload and file a document, spawn a
   task list onto a matter, capture and pin a note, search-jump
   across identities, administer users and restore from trash --
   with a signed short verdict (PASS per axis: story lands /
   nothing embarrassing / demoable).

## Baseline (2026-08-10, verified in the tab review)

Five of six tabs are read-only tables with zero write surface;
Search alone works (page-level). The core (casework/app) already
implements essentially all needed capability: events + expiry
auto-calendaring, files custody + e-sign lifecycle, tasks + task
lists + reference-date due dates, notes + categories + pinning +
export, universal search + recents, users/trash/notify/settings.
Ground truth per tab: ../tab-review-notes.md.

## Constraints and quality bar

- RENDERING ONLY: no business logic in app_ui; SQL only in
  SELECT-only readers; every write goes through an existing
  casework/app module call. A screen needing new core logic is a
  gate flag, never code written from here.
- casework/ is FROZEN. Any authorized touch (none anticipated)
  would be a ratified program amendment + full reciprocal-guard
  rerun.
- casework-ui/goal.md never edited; run_ui_walk.py green at every
  gate; existing-screen changes are gate decisions. The shared
  chrome (html.py) MAY grow additively (search bar, nav active
  states) under the nav-marker precedent -- inert elsewhere,
  ruled at the owning phase's gate.
- Design rulings from the tab review BIND as contract (see
  Appendix A). The six killed config-depth entries stay killed.
- Zero interaction parity. Corpus criteria bound capability only,
  cited by id (events, files-and-documents, case-tracking, notes,
  firm-settings.universal-search + ruled-in firm-settings set,
  personal-settings.user-roles); corpus never edited.
- Money integer cents; user-facing dates MM/DD/YYYY, data ISO;
  no floats touching money anywhere.
- Synthetic data only; gate/demo dbs are fresh seeded dbs.
- Interaction cost is the thesis: a dense grid recreating
  Docketwise's defect fails the quality bar even if capability
  passes.

## Operating mode: PHASE-GATED HYBRID

Unattended within phases; James at the gates between them. During
a phase, interpretive judgment calls accumulate tagged [Q] in the
worklog's ruling queue instead of stalling the build; the queue
clears serialized one-question-per-turn at the gate. Gates are
HANDS-ON: James drives the live page on port 8500 over a seeded
demo db; screenshot decks may support but never substitute (gate
medium rule, goal-method op doctrine).

## Decision defaults (pre-answering judgment calls)

- Wording/labels: agent drafts, flags [Q]; gate rules them.
- Visual vocabulary (kind colors/chips on the calendar and
  elsewhere): agent drafts ONE proposal per surface, renders it,
  flags for the gate; never iterates past it unprompted.
- ANTI-STALL: max 2 polish iterations per screen per phase on
  agent judgment alone; the 3rd parks the screen with a rendered
  before/after and a one-line statement of what is not working,
  queued for the gate. A parked screen is not a blocker.
- Empty states are designed, not blank tables: each states what
  will appear and the action that creates it.
- Any capability ambiguity resolves toward the corpus criterion's
  minimum, flagged [Q] for the gate.

## Allowed without asking

- New files under casework-tabs/ (verify/, seeds/, docs).
- New screens, routes, readers, and additive chrome in
  casework-ui/app_ui serving the six tabs.
- New walk-verifier coverage in casework-tabs/verify/.
- Regenerating this child's own generated artifacts.

## Approval required

- The program amendment (Appendix B) before any app_ui write.
- Any edit to an existing casework-ui screen or walk step.
- Any casework/app or casework-billing touch (none anticipated).
- goal.md edits (scope changes), phase-order changes.

## Forbidden

- New business logic in app_ui; direct SQL writes anywhere.
- Cold-run machinery or recruiting-gate imports.
- Config-depth surfaces from the killed six.
- Hand-editing generated files; editing sealed corpus or sibling
  contracts.

## Verifiers

1. PER-TAB WALK VERIFIER (this child's oracle-first floor):
   casework-tabs/verify/run_tabs_walk.py drives each tab's flows
   over HTTP on a fresh db -- create/see/act per the tab's ruled
   requirements -- exit 0 only when all steps green. Built BEFORE
   each tab's screens (oracle-first); every check driven RED on
   purpose once before trusted (verify-the-verifier).
2. STANDING SUITES, all green and quoted at every gate: casework
   spine, casework-billing run_billing + run_fiduciary --seeded,
   casework-ui run_ui_walk. This child modifies none of them.
3. FINAL WALK SHEET: the cross-tab walk runs off a ratified sheet
   (casework-tabs/verify/walk-sheet.md) with claim-extraction
   checks (label audit + sheet-UI coupling lock with re-sync
   protocol, report sha via canonical script only) -- ratified
   before first use, amended only by ruling.
4. Walk report x2 byte-identical (sha script) at completion.

## Supporting checks

- Float sweep over new screens (no /100 renders; cents_of style).
- ISO-stray sweep (no raw ISO dates user-facing).
- Empty-state sweep (every new list has a designed empty state).

## Completion proof (paths that must exist)

| Path                                   | Proof                  |
| -------------------------------------- | ---------------------- |
| casework-tabs/verify/run_tabs_walk.py  | exit 0 x2, quoted      |
| casework-tabs/verify/walk-sheet.md     | ratified + lock synced |
| casework-tabs/verify/tabs-walk-report.txt | GREEN x2 byte-identical, sha quoted |
| casework-tabs/verify/gate-receipts/    | per-gate receipts P1-P6 |
| casework-tabs/verify/final-walk-report.md | James's signed verdict |
| casework-tabs/result.md                | written last           |

## Iteration and recovery

- Gate FAIL names its fix axis; work between attempts is bounded
  by SCOPE: only what the FAIL named plus gate-ruled items
  (verdict-pendency doctrine). Fix, rerun floor, re-gate.
- Worklog-as-you-go; state.md rewritten each wind-down; cold
  resume must work from the four files alone.
- Self-audit questions at final wind-down (ratified here):
  (a) did compaction fire and what survived; (b) did state.md/
  worklog suffice at every resume; (c) did any blocker candidate
  reach three turns; (d) was log-don't-build honored live or
  backfilled; (e) did the ruling queue ever stall a phase.

## Blocker rule

Difficulty, long runtime, model uncertainty, and failed first
attempts are NOT blockers. A real blocker needs concrete evidence,
no safe fallback, and persistence across three consecutive turns.
World-blocked is not agent-blocked: a stall living in the world
(James unavailable for a gate) is ON HOLD with a named resumption
trigger, not a blocker event.

## State files

goal.md (this contract) / plan.md (strategy, agent-owned) /
state.md (session cache, overwritten) / worklog.md (append-only;
METHOD: entries mark method observations; [Q] entries feed the
gate ruling queue).

## Appendix A -- ruled design requirements (from the tab review)

Binding at ratification; full rationale in ../tab-review-notes.md
(which then retires to archive status).

- CALENDAR: unified date view -- events, expirations, task due
  dates, vmax clocks, invoice due dates -- with a kind filter
  (all at once or any single kind). Per-user = filters + seat
  defaults, never partitions; enforcement deferred. Agenda AND
  month-grid views, two-button toggle, sticky per user, agenda on
  first-ever visit. Two create paths: New appointment / New
  deadline (two lean pre-shaped forms). Kinds visibly distinct
  (vocabulary at the gate); provenance on every derived row
  linking to its source. Parity rides: attendees UI, default
  reminders (Settings home), end times, descriptions, windowed
  queries, MM/DD/YYYY. Reminders email-only. Sync stays parked
  (meeting question).
- FILES: matter-centric -- matter/contact pages grow Files
  sections; the global tab is the firm-wide index with filters
  (matter, client, source, e-sign status); folders secondary,
  capability kept. Custody visible (source + sha256). E-sign
  first-class flow (prep editor, request, sign, status,
  auto-filing) -- staging decision at contract time rides
  plan.md. Upload/rename/preview/print/bulk surfaced.
- TASKS: index opens on MY OPEN tasks; Firm toggle + completed
  filter one click, never partitioned. Type-and-Enter quick-add
  kept. One-click complete from rows. Matter/contact task
  sections. Task Lists builder (Settings home) + Import Task
  List on matter/contact; automation linkage visible.
  Reference-date rules surfaced in the builder.
- NOTES: matter-page Notes section is a chronological NOTES
  timeline, pinned on top (interleaved case timeline PARKED as a
  named design idea for a rendered-artifact gate). Minimal
  capture (body + save, expandable for title/category/assignees/
  notify-all); notify-all on the expanded form only. Index
  defaults: ALL notes, pinned first then newest, category + mine
  filter chips. Categories managed in Settings; PDF export on
  matter/contact sections.
- SEARCH: chrome-level bar reachable from every page; coverage =
  contacts, matters, forms, receipt numbers, invoice display
  codes, file names, note titles AND bodies, task titles, event
  titles. Recents surfaced. Grouped results, jump on select;
  /search page stays as full-results fallback.
- SETTINGS: designed within the ruled-in set only -- Users
  (invite, deactivate, role label, admin, MFA reset),
  Permissions/groups, Trash, Notifications, Firm basics (time
  zone), plus machinery homes: Task Lists, note categories,
  event default reminders, expiry reminder rules. Trash: central
  screen in Settings + "View trash" links on each list. The six
  killed entries stay killed.

## Appendix B -- program amendment (DRAFT for James's ratification
into atlas/CLAUDE.md; not in force until ratified)

casework-tabs extends the casework-ui surface IN PLACE. A
casework-tabs session may write casework-ui/app_ui (new screens,
routes, SELECT-only readers, additive shared chrome) and add new
walk/verifier coverage under casework-tabs/, with hard limits:
run_ui_walk.py stays green at casework-tabs phase gates;
casework-ui/goal.md is never edited and its cold-run oracle, hold
status, and ratified protocol are untouched; a change to an
existing casework-ui screen or its walk steps is a gate decision,
not a code change; casework/ stays frozen for this child (all six
tabs' logic already lives in casework/app; casework-tabs owns
rendering only); Settings write screens call existing casework/app
modules exclusively. Oracle: per-tab hands-on gates + a final
James-driven cross-tab walk, NOT a cold run. After any session's
work, all standing suites rerun green and quoted; sha
supersessions via canonical scripts only, recorded in the
casework-tabs worklog.
