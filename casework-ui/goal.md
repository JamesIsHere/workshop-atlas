# goal.md -- casework-ui (RATIFIED 2026-08-01)

Status: RATIFIED by James, 2026-08-01, zero red-pen kills
(whole-document approval after review; candidate kills declined).
This is the contract. Edits to it are the scope-change mechanism
and require James's approval. One deferral noted at ratification:
whether first-run account ceremony counts inside the cold user's
time budget is ruled at the P3 gate with the cold-run protocol,
informed by rehearsal data.

## Outcome

A firm-facing web UI over the verified casework core, verified two
ways:

1. MECHANICAL: a scripted walk completes the anchor workflow by
   driving the UI's own HTTP routes -- the same GETs and form POSTs
   a human's clicks produce, never module calls -- on a fresh
   database, asserting the same artifacts as casework's
   verify/run_anchor.py (contact row, matter row, returned intake,
   filled G-28 field values, deadline event, fired reminder, audit
   chain). Plus a browse sweep: every ratified surface renders with
   real data, no dead ends on any reachable link.
2. LIVE: at least one COLD USER -- a person who has never operated
   the system -- completes the anchor task sheet unassisted, by
   clicking, on a fresh database, within the time budget (default
   15 minutes). James's own runs are rehearsal, never proof.

This child is where the program's design thesis (Docketwise's
time/training/quality-of-use cost is a product defect that can be
designed out) meets its instrument. The thesis VERDICT -- Amin's
firm's reaction -- remains outside this contract: v1 completes when
the two verifiers pass. A passing cold run is evidence for the
thesis, not the verdict.

## Baseline

- ../casework/: COMPLETE, both verifiers green (its result.md is
  the authority). Provides every capability this UI surfaces: 34
  app modules, app/bootstrap.py install path, client HTTP surface
  (intake + e-sign), verify/run_anchor.py as the module-level
  regression for the exact chain this UI makes clickable.
- ../docketwise-spec/corpus/: sealed oracle for WHAT must be
  possible. This child adds no capabilities, so the corpus binds
  nothing new here; it is cited only when a screen's capability
  needs its source.
- No UI code exists. casework's firm side is module-level only;
  its client surface (intake/e-sign) already speaks HTTP and is
  NOT rebuilt here.

## Scope (rulings 1-2)

- Operating mode: MIXED with SCREEN-REVIEW GATES. Supervised gates
  between phases include James eyeballing the running UI; the
  red-pen artifact at gates is the rendered screen, not only a
  unit table. Unattended execution inside ratified phases.
- ANCHOR-PLUS-BROWSE: the anchor walk is fully clickable (login
  through filled G-28 with deadline visible); everything else in
  the database gets browse-grade surfaces -- read-only index and
  detail screens -- so free exploration always lands on a real
  page. Mutation surfaces beyond the anchor path are OUT of v1;
  adding one is a goal.md edit.

## Constraints and quality bar

- UI OWNS NO BUSINESS LOGIC. Every mutation and every read goes
  through casework's app modules, the way run_anchor.py does. If a
  screen seems to need new business logic, that is a cross-project
  change: flag it, park it, never build it here or patch it there
  silently.
- ../casework/ IS FROZEN from this project. Its verifiers must
  stay green and untouched; any casework edit is Approval
  required, and both its verifiers run before and after.
- ZERO INTERACTION PARITY: corpus criteria never dictate screens;
  copying Docketwise's interaction model is the program's named
  failure mode. Screen design is free and judged by the gates and
  the cold run.
- REAL AUTH PATH: the UI logs in through casework's auth (password
  + MFA enrollment + session), never a bypass. The cold user logs
  in for real.
- JS DISCIPLINE (ruling 4): server-rendered pages are the
  skeleton; vanilla JS only, no framework, no build step, no new
  dependencies. Each use is justified per-screen by a named
  interaction cost, and every screen still functions (degraded is
  acceptable) with JS off.
- SYNTHETIC DATA ONLY, program-wide rule unchanged. ASCII-safe
  output everywhere. No emojis anywhere in the UI.

## Decision defaults (agent judgment -- red-pen targets)

1. PROCESS SHAPE: casework-ui runs its own stdlib HTTP server
   process that imports casework's app package (sys.path to the
   sibling; casework stays untouched). One process, one SQLite db,
   localhost only. Rationale: cheapest-reversible; matches the
   single-firm deployable story.
2. SESSION TRANSPORT: cookie-carried session token over
   localhost HTTP, riding casework's sessions table. No new auth
   machinery.
3. SCREEN ROSTER (anchor path): login/MFA, dashboard, contact
   create+detail, matter create+detail, form package + invitation
   send, intake review, G-28 render/download, calendar + event
   detail. Browse-grade: contacts index, matters index, files,
   tasks, events, notes, search results, settings (read-only).
   Roster is a strawman -- the phase gates refine it.
4. TIME BUDGET: 15 minutes, inherited from the program's decision
   default. The cold run measures wall clock from first login
   screen to G-28 downloaded + deadline visible.
5. FIXTURE POSTURE: the cold run starts from a FRESH db via
   bootstrap.install() (the UI ships a first-run path: create the
   admin, enroll MFA); rehearsals may use the casework seed.

## Allowed without asking

- Rewriting plan.md; creating/refactoring UI code and tests;
  running both projects' verifiers; worklog/state maintenance;
  screenshots and screen recordings for gate review.

## Approval required

- Any goal.md edit (the scope-change mechanism).
- ANY edit under ../casework/ or ../docketwise-spec/ (foundation
  is frozen; corpus is sealed).
- Any new dependency beyond stdlib + what casework already
  installed (pypdf). Any JS framework (forbidden below is
  stronger: frameworks are out, period, for v1).
- Any network beyond localhost; anything real-data adjacent;
  publishing anything; recruiting the cold user (James does that).

## Forbidden

- Business logic in the UI layer.
- Real client data or real PII in any form.
- Verbatim UI cloning of Docketwise.
- JS frameworks, build tooling, npm.
- Hard deletes (of project files or system data).
- Payment processing of any kind.

## Verifier 1 -- scripted UI walk + browse sweep (STRAWMAN)

verify/run_ui_walk.py, oracle-first (exists before the screens;
red until they land):

- Drives the UI server over HTTP exactly as a browser would:
  GET each screen, parse the form, POST the fields a user would
  type. Session cookie carried throughout. No module-level calls
  for any story action; module access only to ASSERT artifacts
  (same assertions as casework's run_anchor.py, including the
  audit chain and supporting checks on the walked db).
- Story: fresh db -> first-run admin setup + MFA -> login ->
  create contact -> create matter -> form package + invitation ->
  (client leg rides casework's existing intake surface) -> review
  returned intake -> render G-28, assert field values via pypdf ->
  deadline event + reminder via tick -> audit chain.
- BROWSE SWEEP: crawl every link reachable from the dashboard on
  the seeded db; assert every ratified surface returns 200 with
  its expected content marker, and no reachable link 404s or 500s.
- Report: verify/ui-walk-report.txt with per-step timings; exit 0
  iff every step and the sweep pass. Run x2 at close.

## Verifier 2 -- cold-user run (STRAWMAN)

- Protocol artifact: verify/cold-run-protocol.md -- the task sheet
  (a fake client's story: "get this person to a filled G-28 with
  the deadline on the calendar"), the rules (fresh db, no
  assistance, no tutorial, stopwatch from login screen to G-28
  downloaded + deadline visible), and the recording form.
- Proof: verify/cold-run-report.md recording at least one PASSING
  run by a qualifying cold user (ruling 3: never operated the
  system before; James's runs are rehearsal only), wall clock
  under budget, plus observed friction notes (the thesis data).
- A failing cold run is a FINDING, not a contract breach: fix,
  re-recruit, re-run. The contract needs one pass.

## Supporting checks (STRAWMAN)

- Foundation-green: both casework verifiers pass, unmodified, at
  this project's close (proves the UI child never bent its
  foundation).
- No-logic lint: the UI layer contains no SQL against casework
  tables except through casework modules (mechanical grep sweep;
  exact rule drafted with the code).
- JS discipline sweep: every .js asset traces to a per-screen
  justification logged in the worklog; no framework imports.
- Synthetic guard: the UI's own fixtures carry the marker.

## Completion proof (paths that must exist)

- casework-ui/app_ui/ + tests/ -- the UI and its suite
- casework-ui/verify/ui-walk-report.txt -- exit-0 run x2
- casework-ui/verify/cold-run-protocol.md -- the ratified protocol
- casework-ui/verify/cold-run-report.md -- >=1 passing cold run
- casework-ui/result.md -- written only after both verifiers pass

## Operating mode: MIXED with screen-review gates (ruling 1)

- SUPERVISED gates: goal ratification; each phase transition. A
  gate = unit-table red-pen for the next phase PLUS eyeballing the
  running UI built so far (screenshots in the gate package; live
  server on request). Wind-downs when James is present.
- UNATTENDED inside phases once units are ratified, harness as
  judge (verifier 1; verifier 2 is human by definition).
- Final wind-down self-audit (contract, not memory): (a) did
  compaction fire and what survived; (b) did state.md/worklog.md
  suffice at every resume; (c) did any blocker candidate reach the
  three-turn threshold; (d) was log-don't-build honored in real
  time or backfilled.

## Iteration and recovery

- Unit evidence written to disk at unit close (compaction-ready).
  state.md rewritten each wind-down; worklog append-only.
- A failing step iterates inside its unit; a unit failing three
  distinct approaches escalates to the phase gate, not to silent
  scope change. Producer-side churn counted and logged per unit.
- Screen-design disagreement at a gate is a kill like any other:
  recorded with rationale, killed screens stay killed.

## Blocker rule

Difficulty, long runtime, model uncertainty, and failed first
attempts are NOT blockers. A real blocker needs concrete evidence,
no safe fallback, and persistence across three consecutive turns;
it halts the unit, writes the evidence to the worklog, and queues
the decision for the next supervised gate. In unattended stretches
the agent never improvises past an Approval-required boundary.

## State files

goal.md (this contract once ratified) / plan.md (agent-owned) /
state.md (session cache, overwritten) / worklog.md (append-only) /
result.md (only after completion proof).
