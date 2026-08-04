# result.md -- casework

Written 2026-08-01, after both verifiers passed (goal.md: this file
exists only past that bar). Contract: goal.md, RATIFIED 2026-08-01.

## Outcome

The casework v1 system is COMPLETE per the ratified contract: a
running immigration practice-management core with capability parity
on the 111-entry spine of the docketwise-spec corpus, zero
interaction parity, on the three schema invariants (single fact
store, audit trail on every mutation, soft delete everywhere).

The design thesis (Docketwise's time/training/quality-of-use cost is
a product defect that can be designed out) remains UNTESTED BY
DESIGN: its test is the friend's firm's reaction to the running
system, which is a successor decision, not part of this contract.

## Verifier 1 -- spine suite (mechanical)

    spine: 107 green, 0 red, 0 pending; checks pass
    verdict: GREEN, exit 0

- 111 entries = 83 direct + 23 adapted + 1 content + 4 parked;
  107 in scope, all green. No entry silently dropped.
- Run x2 on 2026-08-01: reports byte-identical, sha256
  8339a90768eb4ebf7d5da21251ac8a29aadaf483f57fb9b0bc6ca7b95f8feedd.
- Supporting checks (5): audit-coverage, fact-store-lint,
  fact-integrity-sweep (added P5, see below), soft-delete-sweep,
  synthetic-guard. All pass.
- Seed deterministic: seeds/seed.sql sha256 202445b70671...,
  unchanged through the P5 bootstrap refactor.

## Verifier 2 -- anchor workflow (live)

    anchor: PASS (1.382s of 900s budget)   run 1
    anchor: PASS (1.355s of 900s budget)   run 2, fresh db

Scripted cold-start walk (verify/run_anchor.py), ten steps on a
FRESH database -- no seed: schema install -> first admin with full
MFA enrollment -> contact -> matter -> intake invitation -> client
completes the questionnaire over real localhost HTTP -> filled G-28
read back field-by-field with pypdf -> deadline event + reminder
fired by the scheduler tick -> audit-chain continuity -> supporting
checks against the walked db. Report: verify/anchor-report.txt.

What it proves beyond verifier 1:

- Fresh-install path works (the spine suite rides the seed; the
  anchor db starts empty).
- Single fact store as a lived chain: the client's family name is
  entered exactly once, over HTTP, by the client -- and appears in
  the produced G-28 AcroForm field. The same PDF also carries a
  firm-entered fact and preparer-settings fields (three origins,
  one artifact).
- Audit continuity across actor classes in one story: system
  (install), user (contact/matter/form/invitation/event), contact
  (the client's fact write) -- present and story-ordered.
- The 15-minute budget (decision default 6) is trivially met
  headless; the human-run demo for the friend's firm is the real
  budget test and is outside this proof by contract.

## P5 gate rulings (2026-08-01)

1. SPLIT on the P0 deferred weaknesses: the fact-integrity sweep
   (P0 ruling 6) was BUILT as a verifier-1 supporting check --
   wholesale assertion of no orphan polymorphic subject_id and no
   fact/definition subject_type mismatch. It passes on the seeded
   db and on the anchor-walked db. contact_relations directional
   dedup STAYS DEFERRED -- see Known weaknesses.
2. Unit table ratified as drafted (U5.1 anchor script, U5.2 sweep,
   U5.3 close), zero kills -- fifth consecutive zero-kill gate.

## Findings during P5

- FRESH-INSTALL GAP (found, fixed): baseline fact_definitions lived
  only in the seed generator; a cold deployment had no install path
  and create_contact failed on an empty db. Fix: app/bootstrap.py
  now owns BASELINE_FACT_DEFS + install(); gen_seed.py imports the
  same list so seed and install cannot drift. seed.sql regenerated
  byte-identical (sha256 202445b70671..., unchanged).
- Builtin note categories still load from the seed only (fx-0223
  says they ship with the system). Harmless for v1 -- no spine
  criterion exercises them on a fresh db -- but a real deployment
  would want them in bootstrap.install(). Logged, not built.

## Known weaknesses (disclosed, deliberate)

- contact_relations directional dedup (P0 ruling 7 family): A->B
  and B->A can coexist; unenforced. Deferred at the P5 gate by
  ruling -- peripheral table, no downstream consumer reads
  relations directionally. Trigger: build the sweep when relations
  gain any consumer beyond the contact page.
- Value-encoding validity of facts stays app-layer by design (P0
  ruling 6); the sweep asserts referential shape, not encodings.
- record_access, esign_events, and the other append-only logs are
  audit-exempt by design (they are themselves the record).
- Single-firm, single-instance architecture; tenancy retrofit is
  accepted as expensive (decision default 1).

## Churn record (op rule 7 residual)

| Phase | Red iterations |
| ----- | -------------- |
| 0     | n/a (no tests) |
| 1     | 2              |
| 2     | 2              |
| 3     | 0              |
| 4     | 0              |
| 5     | 0              |

Both P5 verifiers passed first run. The trajectory supports the P3
falsifiable read: churn concentrated where tests were authored
against surfaces that did not yet exist; once the P0 schema
anticipated the tables, phases stopped iterating.

## Self-audit (goal.md operating mode, contract items a-d)

(a) Compaction: no compaction event is recorded in any session's
    worklog; sessions were deliberately ended with /clear and cold
    resumes instead. Nothing was lost to summarization that the
    state files did not carry.
(b) state.md/worklog sufficiency: every cold resume (P2, P4, P5
    kickoffs) re-oriented from CLAUDE.md -> state.md -> plan.md ->
    goal.md alone, each in one orientation pass with no recorded
    wrong turns. The P5 resume (this session) followed the same
    path and reached gate-ready in one pass.
(c) Blocker rule: no blocker candidate reached the three-turn
    threshold in any phase; the rule was never invoked.
(d) Log-don't-build: honored in real time -- deferred weaknesses
    (P0 rulings 6-7), boundary calls (P1), owed test extensions
    (P2->P4), and the note-categories finding (P5) were logged at
    the moment of decision, none backfilled.

## Completion proof (paths)

| Path                     | State                                  |
| ------------------------ | -------------------------------------- |
| spine-map.json           | 111 entries classed, 107 green         |
| verify/spine-report.txt  | exit-0 x2, byte-identical (8339a907..) |
| verify/anchor-report.txt | PASS with per-step timings             |
| app/ + tests/            | 34 app .py files, 22 spine test files  |
| result.md                | this file                              |

## What v1 is not (post-v1 pointers)

- No firm-side UI: the firm surface is module-level; only the
  client intake/e-sign surface speaks HTTP. A UI phase was always
  post-v1.
- Parked (4): 3 e-filing platform entries + firm subdomain;
  reactivation triggers live in spine-map.json.
- Content growth: forms library ships 5 starter forms (G-28 first);
  growth is content work, not engine work.
- Live integrations: visa bulletin and USCIS receipts run replay
  adapters over captured/synthetic datasets; live fetch is post-v1
  and Approval-required.
- Invoicing/trust: strategically flagged in the ledger; if it ever
  enters scope the ledger must be trust-shaped from the first
  schema. Never payment processing.
