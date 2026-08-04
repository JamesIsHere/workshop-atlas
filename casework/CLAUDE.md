# casework

## Purpose

Child 2 of the atlas program: BUILD the casework core -- an immigration
practice-management system implementing capability parity on the ratified
111-entry spine of the docketwise-spec corpus, with zero interaction
parity. The design thesis under test: Docketwise's time/training/
quality-of-use cost is a product defect that can be designed out.
"Working" means spine criteria pass against the running system (not the
spec) and the schema honors the invariants (single fact store, audit
trail). goal.md, once ratified, is the contract; this file is a signpost.

## State

| Field        | Value                                              |
| ------------ | -------------------------------------------------- |
| Status       | COMPLETE 2026-08-01 -- both verifiers pass;        |
|              | result.md written; goal.md contract satisfied      |
| Last session | 2026-08-01 -- P5: gate split ruling (fact sweep    |
|              | built, relations dedup disclosed), anchor walk     |
|              | PASS x2 on fresh dbs, spine x2 byte-identical,     |
|              | result.md, wind-down                               |
| Next action  | None owed. Successor decisions (demo to the firm,  |
|              | any post-v1 phase) are new conversations, not      |
|              | queued work. result.md is the authority            |

Keep this table honest at every wind-down. A stale State section is
worse than none -- it tells a cold resume confident lies.

## How to run

From casework/: `python verify/run_spine.py` runs verifier 1 (spine
suite + supporting checks; exit 0 = all green). `python
app/schema/gen_schema.py` regenerates schema.sql; `python
seeds/gen_seed.py` regenerates seed.sql. Generated files are never
hand-edited. Open dbs only via app/db.py connect().

RECIPROCAL GUARD (casework-billing close, 2026-08-03): app/ also
carries the billing/trust layer (ledger, billing, processor,
timekeeping), whose verifiers live in ../casework-billing/verify/.
Any session touching app/ runs BOTH suites: this spine suite AND
`python verify/run_billing.py` + `python verify/run_fiduciary.py
--seeded` from ../casework-billing/. Spine green alone no longer
proves the core unbroken.

## Gotchas

- ../next-child-notes.md is the pre-contract decision ledger (spine
  roster, defers with triggers, strategic flags). It folds into goal.md
  at ratification and is then retired -- do not treat it as a live
  authority after goal.md exists.
- The acceptance oracle is ../docketwise-spec/corpus/ (sealed, append-
  and-supersede). Cite entries by id (module.entry-name); never edit
  the corpus from this project.
- Capability parity, NOT interaction parity: corpus criteria say what
  must be possible, never how the UI works. Copying Docketwise's
  interaction model is the failure mode this project exists to avoid.
- Invoicing/trust-accounting: the strategic flag was deliberately
  revisited 2026-08-03 -- child 4 (../casework-billing/) extends THIS
  core in place per program ruling: billing code lands in app/ on the
  shared schema, its tests/verifiers live in its own folder. The
  111-entry spine suite is its standing regression gate; existing
  spine tests are immutable from that child and this project's
  goal.md is never edited by it. The trust-shaped-ledger rule and
  never-build-payment-processing stand; live contract is
  ../casework-billing/goal.md once ratified.
- Program rulings live in ../CLAUDE.md and are closed -- do not
  re-litigate (public-only sourcing, roster-from-corpus, etc.).

## Rules for agents

- goal.md is ratified by James only; agent edits to it are scope
  changes and need approval.
- Do not report success, sync, or completion unless you have run the
  relevant command this session and are quoting its output.
- Generated files are regenerated, never hand-edited.
- Judgment calls get flagged (`confirm`-style), not silently baked in.
- When sources disagree, record the disagreement -- both values, with
  provenance. Never merge a contradiction into an average or a single
  smoothed narrative; the mismatch is usually the signal.
- Secrets live in `.env` (gitignored); never in tracked files.
