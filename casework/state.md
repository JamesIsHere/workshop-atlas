# state.md -- casework

Overwritten each wind-down. Cache over the worklog.

## Status

PROJECT COMPLETE, 2026-08-01. Both verifiers pass; result.md
written; goal.md contract satisfied. Same session: P5 gate closed
(ruling 1: SPLIT -- fact-integrity sweep built as supporting
check, contact_relations dedup deferred + disclosed; ruling 2:
unit table ratified, zero kills), then U5.2 sweep (passes first
run -- write-path guard held), U5.1 anchor walk (ten steps, fresh
db, PASS x2: 1.382s / 1.355s of 900s budget), U5.3 close.

Receipts: verifier 1 "spine: 107 green, 0 red, 0 pending; checks
pass", exit 0 x2, byte-identical (sha256 8339a907...; new baseline
-- report carries the sweep line). Verifier 2 anchor-report.txt
PASS with per-step timings. Seed sha256 202445b70671... unchanged
through the bootstrap refactor. Churn P5: ZERO -- third
consecutive no-churn phase (2, 2, 0, 0, 0).

P5 finding, fixed: fresh-install gap -- fact_definitions lived
only in the seed; app/bootstrap.py now owns BASELINE_FACT_DEFS +
install(), gen_seed.py imports it (seed byte-identical, provable
no-op). Logged, not built: builtin note_categories still
seed-only.

## Next actions

1. NONE OWED under the contract. v1 is complete.
2. Successor decisions (James's, not queued work): demo to the
   friend's firm (the thesis test, outside the contract); any
   post-v1 phase (firm UI, parked e-filing entries, content
   growth, live integrations) is a NEW goal.md conversation.
3. If reopened for any reason: orient CLAUDE.md -> this file ->
   result.md -> worklog tail.

## Watch items and caveats

- result.md is the authority on what v1 is and is not; disclosed
  weaknesses live there with reactivation triggers
  (contact_relations dedup; note_categories seed-only; value
  encodings app-layer by design).
- Parked entries (4) reactivate only by gate decision; triggers in
  spine-map.json.
- data/visa_bulletin/ IMMUTABLE; live fetch post-v1 + Approval.
  Corpus sealed. Synthetic data only; email = outbox, never a
  socket. Seeded staff password: 'synthetic-password'.
- Fresh-install path: app/bootstrap.py install() -- fact defs +
  forms library. Anchor walk (verify/run_anchor.py) is the
  regression test for it.
- Python 3.14: open dbs ONLY via app/db.py connect().

## Open decisions

None. The contract is closed; anything further is a new decision,
not a pending one.
