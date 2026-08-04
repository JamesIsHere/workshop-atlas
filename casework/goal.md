# goal.md -- casework (RATIFIED 2026-08-01)

Status: RATIFIED by James, 2026-08-01, zero red-pen kills (six primed
candidates all survived; whole-document approval). This is the
contract. Edits to it are the scope-change mechanism and require
James's approval.

## Outcome

A running immigration casework system, verified two ways:

1. MECHANICAL: every in-scope spine criterion (the ratified 111-entry
   spine of ../docketwise-spec/corpus/, as resolved by the Phase 0
   criterion map) passes as an automated acceptance test against the
   running system on seeded synthetic data.
2. LIVE: the anchor workflow -- fresh database -> create contact ->
   create matter -> complete intake -> produce a filled G-28 PDF ->
   deadline and reminder exist -> audit trail shows the whole chain --
   completes unassisted within the time budget (default 15 minutes),
   scripted and repeatable.

The design thesis (Docketwise's time/training/quality-of-use cost is a
product defect that can be designed out) is TESTED BY the friend's
firm's reaction to the running system. That test is explicitly OUTSIDE
this goal's completion proof: v1 completes when the two verifiers pass.
The thesis verdict is the successor decision, not this contract.

## Baseline

- ../docketwise-spec/corpus/: sealed 242-entry oracle (239 live), the
  acceptance-criteria source. Never edited from this project.
- ../next-child-notes.md: pre-contract decision ledger (spine roster,
  defers with triggers, strategic flags). Folds in here; retired at
  ratification.
- ../spikes/: archived assets (G-28 field mapping, PDF fill, workflow
  engine, server + legal_crm.db). Reference material, not foundation.
- No code exists in this project.

## Scope: the spine

111 live corpus entries: contacts-and-matters (14), smart-forms (41),
case-tracking (10 + reports.vmax-tracking carve), files-and-documents
(18), template-automation (4), events (4), notes (7), login +
personal-settings (4), firm-settings subset (8). Module rulings and
revisit triggers live in the ledger and the worklog.

Criterion adaptation classes (Phase 0 resolves every spine entry into
exactly one; the map was RATIFIED by James 2026-08-01: 83 direct / 23
adapted / 1 content / 4 parked = 111):

| Class      | Meaning                             | Expected members     |
| ---------- | ----------------------------------- | -------------------- |
| direct     | criterion tests as written          | most entries         |
| adapted    | criterion adjusted where the        | e-filing family      |
|            | public-surface behavior cannot be   | (~8 smart-forms      |
|            | reproduced without government       | entries): system     |
|            | accounts or third-party services;   | produces the         |
|            | the adapted wording states what v1  | submission-ready     |
|            | proves instead                      | artifact; actual     |
|            |                                     | gov submission out.  |
|            |                                     | SMS sub-behaviors:   |
|            |                                     | email-only v1.       |
|            |                                     | USCIS status sync:   |
|            |                                     | replay adapter over  |
|            |                                     | captured responses   |
| content    | engine is in scope, full content    | forms-library:       |
|            | library is not; v1 ships a starter  | schema-driven engine |
|            | set, growth is post-v1 content work | + starter set of 5   |
|            |                                     | forms (G-28 first)   |
| parked     | out of the green requirement until  | 3 e-filing platform  |
|            | a named trigger fires; reactivation | entries + firm       |
|            | is a gate decision, never silent    | subdomain (gate      |
|            | (added by map ratification,         | rulings 1-2,         |
|            | 2026-08-01)                         | 2026-08-01)          |

No entry may be silently dropped: every one of the 111 lands in the
map with a class and, if adapted, its adapted wording.

## Constraints and quality bar

- CAPABILITY PARITY, ZERO INTERACTION PARITY. Corpus criteria bound
  what must be possible; UI/workflow design is free and judged by the
  time budget, never by resemblance to Docketwise. Verbatim UI cloning
  is forbidden.
- SCHEMA INVARIANTS (first-class, from the six-invariant analysis):
  - Single fact store: a client/case fact is entered once and flows to
    every consumer (forms, deadlines, documents). No duplicated fact
    columns; the Phase 0 schema review enforces this.
  - Audit trail: every mutation records who/what/when. Coverage is
    mechanically checked (see Supporting checks).
  - Soft delete everywhere (trash-can): nothing is destroyed; deletes
    are reversible tombstones.
- SYNTHETIC DATA ONLY. No real client data, no real PII, ever, in any
  fixture, seed, or test (atlas-v1 lesson). A deliberate security pass
  is a precondition to any future real-data decision, which is not
  this project's to make.
- NEVER build payment processing. Invoicing/trust is deferred with a
  strategic flag (ledger); if it enters scope, that is a goal.md edit
  and the ledger must be trust-shaped from the first schema.
- ASCII-safe output everywhere (PS 5.1 environment); no emojis.

## Decision defaults (agent judgment -- red-pen targets)

1. ARCHITECTURE: single-firm deployable, one firm per instance. Not
   multi-tenant SaaS. Rationale: one prospective user; "cheaper" is
   structural (no per-seat rent); multi-tenancy is a later product
   decision. Consequence accepted: tenancy retrofit is expensive.
2. STACK: Python backend, SQLite storage, server-rendered web UI,
   pip per-user installs. Matches operator skills and spikes
   precedent; SQLite is sufficient for single-firm scale and makes
   the deployable story trivial.
3. SPIKES: harvest as REFERENCE, not foundation. Read for lessons;
   g-28_mapping.json may be imported AS DATA after verification
   against the current USCIS G-28 edition; no wholesale code imports.
4. FORMS STARTER SET: 5 forms, G-28 first; remainder chosen for
   coverage of distinct form-mechanics (repeating sections, addenda,
   conditional assembly). The friend's actual practice mix replaces
   this guess when feedback arrives (parked trigger).
5. GROUNDWORK BOUNDARY: build in invariant order (fact store ->
   matter registry -> forms engine -> deadline machinery -> the
   rest). Where a design choice depends on absent feedback, take the
   cheapest-reversible option and log it (log-don't-build applies to
   scope, cheapest-reversible applies to design).
6. TIME BUDGET: anchor workflow in 15 minutes unassisted by a cold
   user. Proxy for the training-cost thesis until the friend's firm
   provides a real signal.

## Allowed without asking

- Rewriting plan.md; creating/refactoring code, tests, synthetic
  seeds; pip installs (per-user); running the verifiers; worklog and
  state maintenance; criterion-map bookkeeping.

## Approval required

- Any goal.md edit (this IS the scope-change mechanism).
- Schema changes to invariant-bearing tables after the Phase 0 gate.
- Adding/removing/reclassing spine entries after the map is ratified.
- Any external account signup, any network service dependency beyond
  localhost, anything real-data adjacent, publishing anything.

## Forbidden

- Real client data or real PII in any form.
- Payment processing of any kind.
- Editing ../docketwise-spec/ (corpus, fixtures, anything).
- Verbatim UI cloning of Docketwise.
- Hard deletes (of project files or of system data -- archive/tombstone
  instead).

## Verifier 1 -- spine suite (mechanical, oracle-first)

Built BEFORE features (op rule 7): Phase 0 delivers the criterion map
(spine-map.json: entry id -> class -> test id -> status) and the test
harness; features then implement to already-written tests. Green =
every in-scope criterion's test passes against the running system on
the synthetic seed, exit 0, two consecutive byte-identical reports at
project close.

## Verifier 2 -- anchor workflow (live)

Scripted cold-start run of the full chain on a fresh database,
asserting artifacts at each step (contact row, matter row, intake
record, filled G-28 PDF with correct field values, deadline event,
reminder record, audit rows for every step), wall-clock under the
time budget. Runs headless; the human-run variant is the demo for the
friend, not part of completion proof.

## Supporting checks

- Audit coverage: a check that every mutating route/operation writes
  audit rows (mechanical sweep, not sampling).
- Fact-store integrity: schema lint -- no duplicated client-fact
  columns across tables; forms consume the fact store, never private
  copies.
- Soft-delete sweep: no DELETE statements outside the tombstone layer.
- CSV export: core entities (contacts, matters, tasks, events) export
  round-trippably; column count and row count asserted.
- Synthetic-data guard: seeds carry a SYNTHETIC marker; the guard
  fails if any seed lacks it.

## Completion proof (paths that must exist)

- casework/spine-map.json -- all 111 entries classed, in-scope green
- casework/verify/spine-report.txt -- exit-0 run x2, byte-identical
- casework/verify/anchor-report.txt -- verifier 2 pass with timings
- casework/app/ + casework/tests/ -- the system and its suite
- casework/result.md -- written only after both verifiers pass

## Operating mode: MIXED

- SUPERVISED gates: goal ratification; Phase 0 schema + criterion map
  ratification; each phase transition (plan units for the next phase
  red-penned before unattended execution begins); wind-downs when
  James is present.
- UNATTENDED inside phases: once a phase's units are ratified,
  execution runs solo with the harness as judge. Decision defaults
  and the Blocker rule below are written for solo operation.
- Final wind-down self-audit (contract, not memory): (a) did
  compaction fire and what survived; (b) did state.md/worklog.md
  suffice at every resume; (c) did any blocker candidate reach the
  three-turn threshold; (d) was log-don't-build honored in real time
  or backfilled.

## Iteration and recovery

- Unit evidence written to disk at unit close (compaction-ready at
  all times). state.md rewritten at every wind-down; worklog is
  append-only.
- A failing test iterates inside its unit; a unit failing three
  distinct approaches escalates to the phase gate, not to silent
  scope change.
- Producer-side rejection/churn (op rule 7 residual) is counted and
  logged per unit so calibration signals stay visible.

## Blocker rule

Difficulty, long runtime, model uncertainty, and failed first
attempts are NOT blockers. A real blocker needs concrete evidence, no
safe fallback, and persistence across three consecutive turns; it
halts the unit, writes the evidence to the worklog, and queues the
decision for the next supervised gate. In unattended stretches the
agent never improvises past an Approval-required boundary; it parks
and proceeds with independent units.

## State files

goal.md (this contract, human-ratified) / plan.md (agent-owned
strategy) / state.md (session cache, overwritten) / worklog.md
(append-only) / result.md (only after completion proof). Data the
project owns (spine-map.json, seeds) sits beside them under its own
rules.
