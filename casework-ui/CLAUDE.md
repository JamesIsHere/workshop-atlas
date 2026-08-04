# casework-ui

## Purpose

Child 3 of the atlas program: BUILD the firm-facing UI over the
verified casework core -- the clickable surface that lets a human run
the system the anchor script proved. This is the child that actually
tests the program's design thesis (Docketwise's time/training/
quality-of-use cost is a product defect that can be designed out):
capability was proven in casework; interaction cost is proven or
refuted here. "Working" provisionally means a cold user completes the
anchor workflow (fresh db -> contact -> matter -> intake -> filled
G-28 -> deadline + reminder visible) unassisted, by clicking, within
the time budget -- the binding definition lands in goal.md at
ratification. goal.md, once ratified, is the contract; this file is a
signpost.

## State

| Field        | Value                                              |
| ------------ | -------------------------------------------------- |
| Status       | ON HOLD (2026-08-03) at P4/U4.1 recruiting gate;   |
|              | pre-verdict -- contract intact, oracle unmet       |
| Last session | 2026-08-03 -- hold declared; walk GREEN parking    |
|              | receipt; r5 rehearsal + finding-8 fix banked       |
| Next action  | Resume when James has a cold runner (never         |
|              | operated any build); then U4.1. See state.md       |

Keep this table honest at every wind-down. A stale State section is
worse than none -- it tells a cold resume confident lies.

## How to run

From casework-ui/: `python -m app_ui.server --db data/ui.db
[--port 8500]` starts the UI (missing db is created + installed;
first visit enters /setup). `python verify/run_ui_walk.py` runs
verifier 1 (exit 0 only when all steps green; pending screens =
exit 1 with verdict "ON TRACK"). Sweeps ride the walk report.
The foundation runs from ../casework/: `python
verify/run_spine.py` and `python verify/run_anchor.py`. Both must
stay green -- this project never modifies them.

## Gotchas

- ../casework/ is the COMPLETE, verified foundation (result.md is
  its authority). This child consumes its app/ modules the way
  verify/run_anchor.py does; it owns NO business logic. If a UI
  need seems to require changing casework code, that is a
  cross-project change -- flag it, do not make it from here.
- Capability parity was casework's bar; this child's bar is
  interaction cost. Zero interaction parity still binds: copying
  Docketwise's screens/flows is the failure mode the program
  exists to avoid. Corpus criteria never dictate UI.
- The acceptance oracle for WHAT must be possible remains
  ../docketwise-spec/corpus/ (sealed); cite by id, never edit.
- Synthetic data only, always (program-wide; casework seed rules
  apply unchanged).
- Program rulings live in ../CLAUDE.md and are closed -- do not
  re-litigate (public-only sourcing, one child per session, etc.).

## Rules for agents

- goal.md is ratified by James only; agent edits to it are scope
  changes and need approval.
- Do not report success, sync, or completion unless you have run
  the relevant command this session and are quoting its output.
- Generated files are regenerated, never hand-edited.
- Judgment calls get flagged (`confirm`-style), not silently baked
  in.
- When sources disagree, record the disagreement -- both values,
  with provenance. Never merge a contradiction into an average or
  a single smoothed narrative; the mismatch is usually the signal.
- Secrets live in `.env` (gitignored); never in tracked files.
