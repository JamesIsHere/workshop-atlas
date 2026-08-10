# casework-tabs

## Purpose

Child 6 of the atlas program: BUILD the six designed tab surfaces --
Calendar, Files, Tasks, Notes, Search, Settings -- over the frozen
casework core, extending casework-ui/app_ui in place (program
amendment pending ratification). The 2026-08-10 tab review
(../tab-review-notes.md, folding into goal.md at ratification) found
five of the six tabs are read-only windows over complete core
machinery; this child is overwhelmingly screens, not logic. "Working"
is defined by goal.md once ratified: per-tab hands-on gate verdicts
plus a final James-driven cross-tab walk on a fresh database. goal.md
is the contract; this file is a signpost.

## State

| Field        | Value                                              |
| ------------ | -------------------------------------------------- |
| Status       | P4a FILES MECHANICS BUILT 2026-08-10, gate         |
|              | PENDING; rail 20 pass/0 fail, sha 81168b79 x2      |
| Last session | 2026-08-10 s6 -- files rail refined (4->5 steps,   |
|              | unpassable+vacuous asserts fixed), P4a built,      |
|              | 3 RED drives, suites green, demo reseeded          |
| Next action  | P4a gate (James drives 8500), then P4b e-sign      |
|              | build. [Q1]-[Q11]+[Q13] carry. See state.md        |

Keep this table honest at every wind-down. A stale State section is
worse than none -- it tells a cold resume confident lies.

## How to run

From casework-tabs/: `python verify/run_tabs_walk.py` runs this
child's rail (exit 0 only when all steps green; pending screens =
exit 1, verdict ON TRACK; float/ISO sweeps ride the report and the
empty-state sweep is walk step 2). `python verify/report_sha.py`
is the ONLY valid report sha. `python verify/seed_tabs.py`
regenerates the gate-review demo db (data/demo-tabs.db; login
demo.tabs@synthetic.test / demo-tabs-pass).

The substrate: from ../casework-ui/,
`python -m app_ui.server --db data/ui.db [--port 8500]` starts the
UI and `python verify/run_ui_walk.py` is the frozen walk guard; from
../casework/, `python verify/run_spine.py`; from ../casework-billing/,
`python verify/run_billing.py` and `python verify/run_fiduciary.py
--seeded`. All must stay green at every gate -- this child never
modifies their tests. This child's own verifiers land in
casework-tabs/verify/ during Phase 0.

## Gotchas

- IN-PLACE EXTENSION (program amendment pending): tab screens land
  in ../casework-ui/app_ui. Hard limits: run_ui_walk.py stays green
  at phase gates; ../casework-ui/goal.md is NEVER edited -- its
  cold-run oracle, ON HOLD status, and ratified protocol untouched.
  A change to an existing casework-ui screen or its walk steps is a
  gate decision, not a code change.
- ../casework/ is FROZEN for this child. RENDERING ONLY: no business
  logic in app_ui; SQL only in SELECT-only readers; writes go
  through existing casework/app modules. A screen that seems to
  need new business logic is a cross-project flag, not code.
- The oracle is per-tab hands-on gates + a final James-driven
  cross-tab walk, NOT a cold run. Cold-run machinery belongs to
  casework-ui's parked contract; do not import it.
- Design rulings from the 2026-08-10 tab review bind (goal.md
  constraints once ratified): unified calendar, matter-centric
  files, my-tasks-first, notes timeline + minimal capture,
  chrome-level search, Settings within the ruled-in set. The six
  killed config-depth entries STAY killed.
- Zero interaction parity; corpus cited by id, never edited; money
  is integer cents, dates render MM/DD/YYYY, data stays ISO.
- Synthetic data only, always; demos from fresh seeded dbs, never
  from casework-ui cold-run/rehearsal dbs (real-ish PII).

## Rules for agents

- goal.md is ratified by James only; agent edits to it are scope
  changes and need approval.
- A session works in ONE child; this child's write surface is
  ../casework-ui/app_ui plus casework-tabs/ itself, nothing else.
- Do not report success, sync, or completion unless you have run
  the relevant command this session and are quoting its output.
- Generated files are regenerated, never hand-edited.
- Judgment calls get flagged (`confirm`-style), not silently baked
  in.
- When sources disagree, record the disagreement -- both values,
  with provenance. Never merge a contradiction into an average.
- Method observations get a METHOD: prefix in worklog.md.
- Secrets live in `.env` (gitignored); never in tracked files.
