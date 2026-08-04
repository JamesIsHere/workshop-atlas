# goal.md -- casework-billing (RATIFIED 2026-08-03)

Status: RATIFIED by James, 2026-08-03, after six red-pen rounds (six
keeps, four with boundary amendments -- worklog s1 r1-r6) and a
verifier-section review invitation; approval statement on record in
worklog s1. This is the contract. Edits to it are the scope-change
mechanism and require James's approval. Bootstrap rulings 2026-08-03:
code home = extend casework in place; operating mode = MIXED; quality
bar = parity plus fiduciary oracle, both gating.

## Outcome

The casework core gains a running invoicing and trust accounting
layer, verified three ways:

1. MECHANICAL, PARITY: every in-scope criterion of the 25-entry
   invoicing-and-trust-accounting corpus module, as resolved by the
   Phase 0 criterion map (billing-map.json), passes as an automated
   acceptance test against the running system on seeded synthetic
   data.
2. MECHANICAL, FIDUCIARY: the fiduciary invariant suite (checks
   F1-F8 below) passes against every database the other verifiers
   produce. This bar deliberately exceeds Docketwise's attested
   surface: the corpus proves a ledger UI exists; it nowhere attests
   double-entry integrity, overdraft blocking, segregation, or
   reconciliation. Those invariants are the thesis (CPA-grade trust
   accounting as the unfair advantage), so they gate completion.
3. LIVE: the anchor billing workflow -- fresh database through trust
   request, trust funding, billing, payment from trust, earn-out
   transfer, third-party disbursement, and three-way reconciliation
   -- completes scripted and unassisted within the time budget
   (default 15 minutes headless, casework precedent).

The casework 111-entry spine suite staying green is a standing
regression gate (supporting check), not a new claim.

## Baseline

- ../casework/: COMPLETE 2026-08-01 (result.md). 66-table schema with
  the three invariants live (single fact store, audit trail, soft
  delete), contacts/matters/users/permissions/notifications/scheduler
  /render machinery, spine suite green x2 byte-identical. Child 4
  extends this in place (program ruling 2026-08-03).
- ../docketwise-spec/corpus/invoicing-and-trust-accounting.md: sealed
  acceptance-criteria source, 25 entries (15 confirmed, 10
  provisional; trust-side entries cap at provisional by design --
  no marketing family reaches them). One recorded source conflict
  (trust-request payment methods, fx-0071 vs fx-0061/fx-0065); one
  known documentation hole (no attested time-to-charge rate
  mechanism).
- Standing rule (ledger 2026-08-01, carried by casework/goal.md):
  entering invoicing scope requires the ledger to be trust-shaped
  from the first schema -- client sub-ledgers, earn-out transfer as
  first-class workflow, three-way reconciliation, gross-vs-net
  settlement awareness. Never build payment processing; a fee-split
  processor is integrated, not reimplemented. This contract is that
  rule's deliberate execution.
- ../casework-ui/: ON HOLD over the same core; its contract is
  intact. This child must not invalidate its substrate.
- No billing code exists.

## Scope

The 25 corpus entries, every one landing in billing-map.json with a
class and, if adapted, its adapted wording. No entry may be silently
dropped. Criterion adaptation classes (casework precedent):

| Class   | Meaning                          | Expected members       |
| ------- | -------------------------------- | ---------------------- |
| direct  | criterion tests as written       | most entries: invoice  |
|         |                                  | machinery, trust       |
|         |                                  | accounts and ledger,   |
|         |                                  | payments, time         |
|         |                                  | tracking, settings     |
| adapted | public-surface behavior needs a  | LawPay-dependent       |
|         | third party or deferred module;  | behaviors (online      |
|         | adapted wording states what v1   | card/eCheck, auto      |
|         | proves instead                   | payment plans, LawPay  |
|         |                                  | receipts): simulated   |
|         |                                  | processor. SMS share   |
|         |                                  | paths: email-only.     |
|         |                                  | Portal share path:     |
|         |                                  | shared-link view       |
|         |                                  | (portal module is      |
|         |                                  | deferred)              |
| parked  | out of the green requirement     | none expected; the map |
|         | until a named trigger fires;     | may propose candidates |
|         | reactivation is a gate decision  | at the Phase 0 gate    |

BEYOND-PARITY SCOPE (deliberate, quality-bar ruling 2026-08-03): the
fiduciary invariants F1-F8, earn-out transfer as a first-class
workflow, and the three-way reconciliation artifact are OUR criteria,
not corpus entries. They are enumerated in this contract precisely so
the oracle has a ratified source; they are in scope exactly as
written, and extending them mid-run is a goal.md edit.

Known unattested-design points (corpus documents the hole; v1 designs
into it, flagged as decision defaults below): time-to-charge rate
mechanism (default 4); trust-request payment methods conflict
(default 3 resolves v1 behavior; the conflict record stays in the
corpus untouched).

## Constraints and quality bar

- CAPABILITY PARITY, ZERO INTERACTION PARITY (program constraint).
  Corpus criteria bound what must be possible; UI/workflow design is
  free. Verbatim UI cloning is forbidden.
- TRUST-SHAPED LEDGER, APPEND-ONLY DOUBLE-ENTRY:
  - Every monetary movement is a balanced journal entry (debits =
    credits) in one journal; client-level and matter-level trust
    sub-ledgers are first-class ledger accounts under their trust
    bank account's control account.
  - Posted journal rows are immutable: never UPDATEd, never deleted.
    Corrections, refunds, and UI-level "edit payment" post reversing
    entries plus a repost; the criterion-visible outcome (payment and
    balance update) is met by the net position.
  - CLEARED-VS-POSTED IS FIRST-SCHEMA (F7 keep ruling, red-pen r1):
    trust postings carry clearing status and clearing date, and
    externally-visible money events (deposits, disbursement checks,
    processor settlements) exist as a first-class external event
    stream from the first migration. Retrofit-hostile; lands in the
    Phase 0 schema, not in a later reconciliation phase.
  - Overdraft and commingling are blocked at posting time (F3-F5),
    not just detected at verification time.
- CASEWORK INVARIANTS INHERITED: single fact store (billing consumes
  contacts/matters/users; no duplicated fact columns), audit trail on
  every mutation, soft delete for non-journal records (invoices,
  time entries, settings rows tombstone; the journal corrects by
  reversal instead).
- MONEY IS INTEGER CENTS, USD-only v1. No floats anywhere in monetary
  paths (schema, code, or fixtures).
- SPINE REGRESSION: ../casework verify/run_spine.py must be green at
  every phase gate and at close. Existing spine tests are immutable
  from this child; a billing change that would require editing one is
  a gate decision.
- SYNTHETIC DATA ONLY. No real client data, no real PII, no real
  payment credentials, ever. The simulated processor accepts only
  synthetic card/account tokens carrying the SYNTHETIC marker.
- NEVER build payment processing. The processor is a deterministic
  in-process simulator behind an adapter interface shaped for a
  fee-split processor (charge, echeck, refund, chargeback, fee
  schedule, gross-vs-net settlement). Wiring a real processor is
  post-v1 and Approval-required.
- ASCII-safe output everywhere (PS 5.1 environment); no emojis.

## Decision defaults (agent judgment -- red-pen targets)

1. LEDGER ARCHITECTURE: one journal (journal_entries +
   journal_postings), chart of accounts with firm accounts (operating
   and trust bank accounts, fee income, processor-fee expense,
   client-funds liability control) plus per-client and per-matter
   trust sub-accounts. Trust bank balance must equal the sum of its
   sub-accounts at all times (F2). Immutability enforced in schema
   (triggers) and verified by sweep (F8).
2. AMOUNTS: integer cents, USD only. Docketwise attests no
   multi-currency; adding it would be scope invention.
3. PROCESSOR SIMULATION: SimProcessor implements the FeeSplitProcessor
   interface deterministically (seeded outcomes, fixed ~3% + 30c fee
   schedule, configurable gross-vs-net settlement). Card and eCheck
   both supported, which resolves the trust-request payment-method
   source conflict for v1 as "both direct and simulated-online
   accepted"; the corpus conflict record is untouched. CHARGEBACK
   BOUNDARY (red-pen r3): a chargeback is a posting event with a
   fee-split recipe -- the clawback debits OPERATING, never trust
   (client A's chargeback must never be paid with client B's funds;
   the firm eats the receivable) -- flowing through the external
   event stream into settlement and reconciliation. It is NOT a
   dispute workflow: no dispute states, evidence, deadlines, or
   representment in v1. Beyond-parity scope, sourced to the
   2026-08-01 strategic flag, not to any corpus entry.
4. TIME-TO-CHARGE RATES: per-user default hourly rate (user settings)
   with per-entry override; charge amount = duration x rate, rounded
   half-up to the cent per entry. Corpus documents no mechanism; this
   is our design, logged as such in the map.
5. RECONCILIATION ARTIFACT: a synthetic bank-statement generator,
   deterministic, driven by the EXTERNAL EVENT STREAM (never the
   journal -- F7 independence clause) through a clearing-lag model:
   disbursement checks clear N days after cutting, book deposits
   settle T+2, processor batches settle on a batch calendar. Lags
   exist deliberately so genuine reconciling items occur and the
   recon engine's classification is exercised, not vacuous. The
   three-way report is produced by script; F7 asserts the identity.
6. TIME BUDGET: anchor billing workflow within 900s headless,
   casework precedent. The human-run demo is outside completion
   proof.
7. INVOICE RENDERING: server-rendered PDF via the existing casework
   render machinery; bulk download is a stdlib zip. Invoice
   translation (Spanish) rides casework's translation machinery;
   untranslated fields match the corpus entry's attested exclusions.
8. SURFACE: firm-side billing is module-level (casework precedent:
   the firm surface is not a full UI); HTTP endpoints exist exactly
   where a criterion requires a client-side actor (shared-invoice
   view/download/pay page against the simulated processor).
9. CODE GEOGRAPHY: billing app code in ../casework/app/ (billing.py,
   ledger.py, timekeeping.py, processor.py or similar), schema via
   gen_schema.py, seed via gen_seed.py; billing tests and verifiers
   live HERE (casework-billing/tests/, casework-billing/verify/) so
   child ownership stays clean. Spine tests remain in
   ../casework/tests/, immutable from here.
10. SCHEDULED BEHAVIORS (late fees overnight, payment-plan
    installments, reminders): ride casework's scheduler-tick pattern;
    tests drive the tick explicitly, no wall-clock waits.
    PAYMENT-PLAN SURFACE BOUNDARY (red-pen r4): auto-charge is IN
    (a scheduler job composing the existing SimProcessor charge path
    and posting recipe; adapted-class, LawPay-gated in the real
    product). The plan config surface is bounded to the attested
    fields -- frequency, installment amount, start date, accepted
    payment forms -- and the attested reminder cadence (7 before /
    due day / 7 after). "Payment Plans 2.0" customization depth has
    no criterion behind it and is not built.

## Allowed without asking

- Rewriting plan.md; creating/refactoring billing code, tests,
  synthetic seeds; regenerating schema.sql and seed.sql via the
  casework generators; pip installs (per-user); running all verifiers
  (this child's and casework's); worklog and state maintenance;
  billing-map bookkeeping.

## Approval required

- Any goal.md edit (this IS the scope-change mechanism).
- Schema changes to ledger or invariant-bearing tables after the
  Phase 0 gate.
- Adding/removing/reclassing map entries after the map is ratified.
- Any change to existing casework behavior that a spine test would
  have to change to accommodate.
- Any external account signup, any network service beyond localhost,
  anything real-data or real-payment adjacent, publishing anything.

## Forbidden

- Payment processing of real money in any form; real payment
  credentials even as test data.
- Real client data or real PII in any form.
- Editing ../docketwise-spec/ (corpus, fixtures, anything).
- Editing ../casework-ui/ or ../casework/goal.md; editing or
  weakening existing spine tests.
- Hard deletes (project files or system data); UPDATE/DELETE on
  posted journal rows.
- Verbatim UI cloning of Docketwise.

## Verifier 1 -- billing parity suite (mechanical, oracle-first)

Built BEFORE features (op rule 7): Phase 0 delivers billing-map.json
(entry id -> class -> test id -> status) and the test harness;
features implement to already-written tests. Green = every in-scope
criterion's test passes against the running system on the synthetic
seed, exit 0, two consecutive byte-identical reports at close.

## Verifier 2 -- fiduciary invariant suite (mechanical, ours)

Runs against every database verifier 1 and verifier 3 produce. All
checks are wholesale assertions over the ledger, not samples:

- F1 BALANCE: every journal entry's debits equal its credits.
- F2 CONTROL: each trust bank account's balance equals the sum of
  its client sub-account balances; each client sub-account equals
  the sum of its matter-level positions plus its client-level
  position.
- F3 NO OVERDRAFT: no client or matter trust sub-account balance is
  negative at ANY point in posting order, not merely at period end.
- F4 FUNDS AVAILABILITY: no trust transfer or disbursement posting
  exceeds the source sub-account's available balance at its posting
  moment (the blocking rule, re-verified after the fact).
- F5 SEGREGATION: every posting to a trust bank account references a
  client/matter sub-account; no operating expense posts against
  trust; earned fees leave trust only via the earn-out transfer
  workflow (trust -> operating with a client sub-account debit).
- F6 GROSS-VS-NET: a simulated online payment on a trust request
  posts the GROSS amount to trust and processor fees to operating;
  fees are never netted out of trust.
- F7 THREE-WAY RECONCILIATION: synthetic bank statement, book
  ledger, and sub-ledger sum reconcile: bank balance + deposits in
  transit - outstanding disbursements = book trust balance = sum of
  client sub-ledgers, per trust account. Every reconciling item is
  enumerated with a cause (deposit in transit, outstanding
  disbursement, settlement lag); no plug. INDEPENDENCE CLAUSE: the
  statement generator may not read the journal -- it renders the
  bank's view from the external event stream (SimProcessor
  settlement batches, deposits, disbursement checks) through the
  clearing-lag model, so book and bank are two witnesses to the
  same events through different pipelines. A statement derived from
  the journal is circular and void.
- F8 IMMUTABILITY: no posted journal row has ever been updated or
  deleted (schema triggers + sweep over the audit trail); every
  correction exists as a reversal pair.

Exit 0, two consecutive byte-identical reports at close.

## Verifier 3 -- anchor billing workflow (live)

Scripted cold-start run on a FRESH database (no seed): install ->
admin -> contact + matter -> trust bank account + operating account
-> Trust Request created and funded (client sub-ledger shows funds)
-> Bill created with a saved charge and an imported time entry ->
Bill paid by trust transfer (earn-out: trust -> operating, client
sub-ledger debited) -> disbursement to a third party (synthetic
USCIS filing fee) -> invoice PDF produced and readable -> three-way
reconciliation report produced -> audit-chain continuity across the
whole story -> fiduciary suite green on the walked database.
Wall-clock under the time budget. Runs headless; the human-run
variant is the demo, not part of completion proof.

## Supporting checks

- Spine regression: ../casework verify/run_spine.py exit 0 at every
  phase gate and at close (report captured to this child's verify/).
- Audit coverage: every new mutating route/operation writes audit
  rows (mechanical sweep, casework pattern extended).
- Soft-delete sweep: no DELETE outside the tombstone layer; journal
  exempt by design (corrects by reversal, never deletes).
- Float sweep: no REAL/float column and no float literal in any
  monetary path.
- Synthetic-data guard: seeds and simulator tokens carry the
  SYNTHETIC marker; guard fails on any unmarked fixture.
- CSV export extended: invoices, payments, time entries, and the
  trust ledger export round-trippably (anti-lock-in commitment).

## Completion proof (paths that must exist)

- casework-billing/billing-map.json -- all 25 entries classed,
  in-scope green
- casework-billing/verify/billing-report.txt -- exit-0 x2,
  byte-identical
- casework-billing/verify/fiduciary-report.txt -- exit-0 x2,
  byte-identical
- casework-billing/verify/anchor-billing-report.txt -- verifier 3
  pass with timings
- casework-billing/verify/regression-report.txt -- spine suite green
  at close
- casework-billing/tests/ + billing modules in ../casework/app/
- RECIPROCAL GUARD (red-pen r6): ../casework/CLAUDE.md "How to run"
  updated at close so the billing verifiers join the core's standing
  regression battery -- any future session touching casework/app/
  runs both suites. Closes the mirror-image hazard of the spine
  regression gate (future core work silently breaking billing).
- casework-billing/result.md -- written only after all verifiers pass

## Operating mode: MIXED (casework precedent)

- SUPERVISED gates: goal ratification; Phase 0 gate (ledger schema +
  criterion map + fiduciary check list ratified together -- the
  schema is the one retrofit-hostile artifact this child owns); each
  phase transition (next phase's units red-penned before unattended
  execution); wind-downs when James is present.
- UNATTENDED inside phases: once a phase's units are ratified,
  execution runs solo with the harness as judge. Decision defaults
  and the Blocker rule are written for solo operation.
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
- Producer-side rejection/churn is counted and logged per unit (op
  rule 7 residual).

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
project owns (billing-map.json, verify reports) sits beside them
under its own rules; billing code lives in ../casework/app/ under
decision default 9.
