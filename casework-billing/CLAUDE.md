# casework-billing

## Purpose

Child 4 of the atlas program: BUILD the invoicing and trust accounting
layer over the casework core, extending it IN PLACE (program ruling
2026-08-03) -- billing code lands in ../casework/app/ on the shared
schema; this folder holds the contract, verifiers, tests, and method
files. "Working" means three greens: the 25-entry corpus module passes
as acceptance tests (parity), a fiduciary invariant suite passes
(CPA-grade trust accounting -- the bar Docketwise never publicly
attests), and a scripted anchor billing workflow runs on a fresh
database. goal.md, once ratified, is the contract; this file is a
signpost.

## State

| Field        | Value                                              |
| ------------ | -------------------------------------------------- |
| Status       | COMPLETE 2026-08-03 -- all three verifiers green;  |
|              | result.md written; goal.md contract satisfied      |
| Last session | 2026-08-03 -- P4+P5 solo: parity 25/25, F7 live,   |
|              | anchor walk PASS 1.3s, x2 byte-identical closes    |
| Next action  | None owed. Successor decisions are new             |
|              | conversations. result.md is the authority          |

Keep this table honest at every wind-down. A stale State section is
worse than none -- it tells a cold resume confident lies.

## How to run

Nothing runs yet. After Phase 0: `python verify/run_billing.py` (parity
suite), `python verify/run_fiduciary.py` (invariant suite) from this
folder; regression: `python verify/run_spine.py` from ../casework/.

## Gotchas

- IN-PLACE EXTENSION: billing code is written into ../casework/app/,
  schema additions via ../casework/app/schema/gen_schema.py, seeds via
  gen_seed.py. The sibling-modification rule is amended for this child
  only (../CLAUDE.md ruling 2026-08-03) with hard limits: existing
  spine tests are IMMUTABLE from here, and ../casework/goal.md is
  never edited. A billing change that would require editing a spine
  test is a gate decision, not a code change.
- ../casework-ui is ON HOLD over the same core. Never edit it; keeping
  the spine suite green is what protects its substrate.
- The acceptance oracle is ../docketwise-spec/corpus/
  invoicing-and-trust-accounting.md (25 entries, sealed). Cite entries
  by id; never edit the corpus from this project.
- The trust ledger is append-only double-entry BY CONTRACT: posted
  journal rows are never updated or deleted; corrections are reversing
  entries. UI-level "edit payment" is reversal + repost under the
  hood. This looks like over-engineering; it is the thesis.
- Never build payment processing. The v1 processor is a deterministic
  simulator behind an adapter interface; wiring a real processor is
  post-v1 and Approval-required.
- Capability parity, NOT interaction parity (program constraint):
  corpus criteria say what must be possible, never how the UI works.

## Rules for agents

- goal.md is ratified by James only; agent edits to it are scope
  changes and need approval.
- Do not report success, sync, or completion unless you have run the
  relevant command this session and are quoting its output.
- Generated files are regenerated, never hand-edited.
- Judgment calls get flagged (`confirm`-style), not silently baked in.
- When sources disagree, record the disagreement -- both values, with
  provenance (the trust-request payment-method conflict is the live
  example). Never average a contradiction.
- Method observations get a METHOD: prefix in worklog.md.
- Money is integer cents everywhere. A float touching a monetary
  amount is a defect, not a style choice.
