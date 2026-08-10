# billing-ui

## Purpose

Child 5 of the atlas program: BUILD the billing and trust-accounting
surface over the casework-ui layer -- the clickable screens that make
the casework-billing layer (invoices, trust ledger, three-way
reconciliation) visible to a human, extending casework-ui/app_ui IN
PLACE (program ruling 2026-08-03). This is the child that turns the
r6 finding (the firm runs billing/trust inside Docketwise; the
AffiniPay take is one pain alongside training cost) into something a
firm can see. "Working" is defined by goal.md (RATIFIED 2026-08-04):
a James-driven demo walk through the full billing lifecycle on a
fresh database, entirely via screens, fiduciary suite green on the
walked db, plus his three-part demo-grade verdict. goal.md is the
contract; this file is a signpost.

## State

| Field        | Value                                              |
| ------------ | -------------------------------------------------- |
| Status       | P4 open after attempt 4 (FAIL b/c, (a) PASS).      |
|              | ALL attempt-5 preconditions MET: item 12 built,    |
|              | finish pass done, and the sheet's seventh          |
|              | amendment adds Part K (period-close act, steps     |
|              | 33-40) with the lock re-synced                     |
| Last session | 2026-08-09 s13 cont -- James ruled the close act   |
|              | into the sheet; Part K built mirroring walk step   |
|              | 20; sheet lock f7f821edb1e9 -> 85e4e4633a37;       |
|              | drive-sheet 27/27, labels 91/0, ALL suites green;  |
|              | report sha 30301f88 unchanged                      |
| Next action  | ATTEMPT 5 -- standard protocol, 40 steps, James    |
|              | picks the moment. See state.md cold-start pointer  |

Keep this table honest at every wind-down. A stale State section is
worse than none -- it tells a cold resume confident lies.

## How to run

Nothing runs from here yet. The substrate: from ../casework-ui/,
`python -m app_ui.server --db data/ui.db [--port 8500]` starts the UI
and `python verify/run_ui_walk.py` is the walk guard; from
../casework-billing/, `python verify/run_billing.py` and
`python verify/run_fiduciary.py` are the billing-layer suites
(path corrected 2026-08-07 -- they never lived in ../casework/);
from ../casework/, `python verify/run_spine.py` is the spine
regression. All must stay green -- this child never modifies
their tests. This child's own oracles, from here:
`python verify/drive_sheet.py` (sheet-UI coupling + recovery
rail; refuses to run if the sheet changed without a re-sync),
`python verify/check_sheet_labels.py`, and
`python verify/report_sha.py` (the ONLY valid walk-report sha).

## Gotchas

- IN-PLACE EXTENSION (program ruling 2026-08-03, see ../CLAUDE.md):
  billing screens land in ../casework-ui/app_ui. Hard limits:
  run_ui_walk.py stays green at phase gates; ../casework-ui/goal.md
  is NEVER edited -- its cold-run oracle, ON HOLD status, and
  ratified cold-run protocol are untouched. A billing screen that
  would require changing an existing casework-ui screen or its walk
  steps is a gate decision, not a code change.
- ../casework/ is FROZEN for this child. Billing logic already lives
  in casework/app (casework-billing, COMPLETE); this child owns
  RENDERING ONLY. The no-logic discipline binds: SQL only in
  SELECT-only readers; writes go through existing casework/app
  modules. If a screen seems to need new business logic, that is a
  cross-project flag, not code written from here.
- The oracle is a JAMES-DRIVEN demo walk, not a cold run. Do not
  import cold-run machinery or its recruiting gate; billing screens
  face the demo driver first, cold users (if ever) under a later
  contract.
- Interaction cost is still the thesis: the rake is a wedge, not the
  claim. A trust ledger rendered as a dense accounting grid recreates
  Docketwise's defect in the one module claiming CPA-grade
  superiority. Zero interaction parity binds here as everywhere.
- The trust ledger is append-only double-entry BY CONTRACT
  (casework-billing thesis): UI "edit" affordances over posted rows
  are reversal + repost presentations, never row mutation.
- Money is integer cents in the data layer; formatting to dollars is
  presentation-only. A float touching a monetary amount is a defect.
- Synthetic data only, always. Cold-run/rehearsal dbs under
  ../casework-ui/data/ carry real-ish PII -- never demo from those;
  demos use fresh seeded dbs.
- The acceptance oracle for WHAT must be possible is
  ../docketwise-spec/corpus/invoicing-and-trust-accounting.md
  (sealed, 25 entries); cite by id, never edit. Corpus criteria
  never dictate UI.

## Rules for agents

- goal.md is ratified by James only; agent edits to it are scope
  changes and need approval.
- A session works in ONE child; this child's amended write surface is
  ../casework-ui/app_ui plus new verifier coverage, nothing else
  outside this folder.
- Do not report success, sync, or completion unless you have run the
  relevant command this session and are quoting its output.
- Generated files are regenerated, never hand-edited.
- Judgment calls get flagged (`confirm`-style), not silently baked in.
- When sources disagree, record the disagreement -- both values, with
  provenance. Never merge a contradiction into an average.
- Method observations get a METHOD: prefix in worklog.md.
- Secrets live in `.env` (gitignored); never in tracked files.
