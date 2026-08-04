# worklog.md -- casework-billing (append-only)

## s1 -- 2026-08-03 -- bootstrap: interview, scaffold, drafts

Session launched from atlas program root (correct launch dir for a
new child; program CLAUDE.md in context). Substrate read before the
interview: corpus invoicing-and-trust-accounting.md (25 entries),
retired next-child-notes.md (strategic flag + standing rule),
casework goal.md + result.md + schema table roster.

### Bootstrap rulings (James, via one-decision-per-turn interview)

1. CODE HOME: extend casework IN PLACE. Child 4 folder holds
   contract/tests/verifiers; billing code lands in casework/app on
   the shared schema. Rationale: single-fact-store invariant (trust
   ledger references the same contacts/matters/audit), one core under
   casework-ui's feet, spine suite becomes a standing regression
   gate. Rejected: fork (core divergence, two homes for every fix);
   separate app on shared db (the exact integration seam the
   module-children rejection of 2026-08-01 was written against).
2. OPERATING MODE: MIXED, casework precedent. Supervised gates at
   ratification / P0 / phase transitions; unattended inside ratified
   phases. Rejected: heavier-gates variant (extra schema gate --
   folded instead into the P0 gate which already ratifies the
   schema); fully-unattended (higher method value on the compaction
   target, but the ledger schema must be right the first time).
3. QUALITY BAR: parity + fiduciary oracle, BOTH gating. The 25-entry
   map passes AND the F1-F8 invariant suite passes. Deliberately
   exceeds Docketwise's attested surface -- the corpus proves a
   ledger UI exists, never double-entry integrity; the fiduciary bar
   IS the thesis (CPA unfair advantage, industry economic soft
   underbelly per the 2026-08-01 strategic flag). Rejected:
   parity-only (differentiating claim would go unverified);
   fiduciary-first with curated parity (breaks no-silent-drop).
4. NAME: casework-billing. Sibling prefix pattern, signals the
   in-place ruling; "billing" spans both module halves.

### Program-level edits executed with ruling 1

- atlas/CLAUDE.md: roster row added; sibling-modification rule
  amended for this child (write access to casework/ with hard
  limits: spine tests immutable, casework/goal.md never edited).
- casework/CLAUDE.md: gotcha pointer added (billing extends the core
  in place; live contract is ../casework-billing/goal.md).

### Drafts for red-pen

goal.md (DRAFT), plan.md, state.md, this file, CLAUDE.md via
project-kit (Data freshness section deleted -- nothing generated
yet). Primed red-pen candidates, flagged not decided (the list
primes the pen, never bounds it):

1. F7 three-way reconciliation requires a synthetic bank-statement
   generator -- a whole artifact for one check. Keep (thesis) or
   thin it?
2. Edit-payment as reversal+repost (append-only journal) vs plain
   UPDATE with audit row. Draft commits to reversal; it is the
   CPA-grade position but costs machinery.
3. SimProcessor scope: chargebacks included in v1 -- real fee-split
   awareness or scope padding?
4. Payment plans with simulated auto-charge: full engine vs park
   the auto-charge sub-behavior behind a trigger.
5. Invoice translation rides casework translations -- confirm the
   attested exclusion list is the boundary, or park the entry.
6. Test/verifier geography (decision default 9): tests here, code
   there -- the split-ownership seam is the price of ruling 1.

### Red-pen round 1 (2026-08-03) -- candidate 1, F7 reconciliation

RULING: KEEP, with two amendments (James). The question that decided
it: is reconciling to a bank statement real work or a tautology?
Answer: real only if the statement is an independent witness.
Amendments applied to goal.md + plan.md:
(a) F7 gains the INDEPENDENCE CLAUSE -- the statement generator may
    never read the journal; it renders the bank's view from the
    external event stream through a clearing-lag model. A
    journal-derived statement is circular and void.
(b) Cleared-vs-posted status + first-class external event stream are
    P0 FIRST-SCHEMA scope (retrofit-hostile), not P5 work. Decision
    default 5 rewritten to name the lag model (checks clear N days,
    deposits T+2, processor batch calendar) so reconciling items
    genuinely occur.
Rationale on record: three-way monthly reconciliation is the actual
IOLTA bar-rule requirement; Docketwise's public surface never
attests it. Work is contained because the synthetic world is
deterministic (no feed formats, no fuzzy matching); the real cost is
the P0 schema, which is exactly why it is decided now.

### Red-pen round 2 (2026-08-03) -- candidate 2, reversal+repost

RULING: KEEP as drafted, no amendments (James). Decision logic on
record: parity alone would accept a plain audited UPDATE (the corpus
criteria test outcomes, not mechanics), but the r1 keep made plain
UPDATE structurally incompatible with the F-suite -- F8 degrades to
casework's existing audit guarantee, F3/F4 would verify rewritten
history instead of what happened, and editing a CLEARED posting
desyncs book from the bank witness in a way no code repairs. Cost is
contained by the two-layer design already in the draft: journal is
append-only (reverse_entry helper + reverses/replaces link columns);
the payment ROW is an ordinary mutable casework record whose versions
point at their current journal entry. Refunds (full-amount-only per
corpus) reduce to a single reversal.
METHOD: red-pen compounding observed -- r1's ruling decided most of
r2 for free (the principle "the bank witness makes history
immutable" carried over); r2 reduced to a cost question.

### Red-pen round 3 (2026-08-03) -- candidate 3, SimProcessor chargebacks

RULING: KEEP with one boundary amendment (James). Provenance made
explicit: no corpus entry attests chargebacks; they enter from the
2026-08-01 strategic flag ("fees/chargebacks to operating"), so they
are beyond-parity scope like the F-suite. Substance: the chargeback
is the only externally-initiated money movement and the sharpest F5
test -- the naive implementation claws back from a pooled trust
account, paying client A's chargeback with client B's funds.
Amendment applied to decision default 3: chargeback = posting event
with fee-split recipe (operating, never trust) riding the external
event stream; NOT a dispute workflow (no states/evidence/deadlines/
representment) -- that named door is where padding would enter.
Marginal cost after r1: one event type, one posting recipe, 2-3
fiduciary cases.

### Red-pen round 4 (2026-08-03) -- candidate 4, payment-plan auto-charge

RULING: KEEP auto-charge, no park; config surface bounded to
attested fields (James). Decision logic: the payment-plans entry is
the module's strongest-attested criterion (8 sources) so the
schedule engine + reminder cadence were never parkable; auto-charge
decomposes after r1-r3 into a composition of three
already-contracted parts (scheduler tick, SimProcessor charge path,
F6 posting recipe), so parking bureaucracy (trigger + gate + adapted
carve) would cost as much as building. Amendment applied to decision
default 10: attested-fields boundary; "Payment Plans 2.0"
customization depth named as the padding door and excluded.
METHOD: same compounding as r2 -- earlier keeps converted this
candidate from build-vs-park into compose-vs-park.

### Red-pen round 5 (2026-08-03) -- candidate 5, invoice translation

RULING: KEEP as direct-class, no amendment (James). The corpus draws
the boundary itself: fx-0052's untranslated list (charge/discount/
invoice descriptions, late fees, custom message text) reads as
"template chrome only, never user content" -- so v1 is a Spanish
string table + language setting + render hook on casework's
translations machinery. The parity test asserts the exclusions STAY
untranslated, guarding the boundary mechanically. Decision default 7
already carried the sentence; nothing to amend. Park rejected on the
r4 asymmetry: bureaucracy would exceed the build.

### Red-pen round 6 (2026-08-03) -- candidate 6, test geography

RULING: KEEP decision default 9 + reciprocal-guard amendment,
option (c) (James, after a deferral-load check -- see below).
The seam's real hazard is temporal and mirror-image to the spine
gate: after close, casework/app/ holds billing modules casework's
own contract never tests; a future core session could break billing
silently. Rejected: (b) moving billing tests into casework/tests --
a COMPLETE project would quietly gain files its ratified contract
never mentions, worse hygiene than the seam. Amendment applied to
completion proof: casework CLAUDE.md "How to run" gains the billing
verifiers at P5 close, contractually owed, so both suites guard the
shared core in both directions.

DEFERRAL-LOAD CHECK (James asked; evidence on record): six rounds,
six keeps, zero kills, zero parks, zero silent skips. Forward
obligations total three, all typed and homed (real processor =
post-v1 Approval-required; reciprocal guard = completion proof;
parked map entries = none yet, P0 gate may propose). Amendments were
fences (never-build), not deferrals (build-later). Lighter than the
casework precedent (closed with 4 parks + disclosed weaknesses).
Counter-pressure named: red-pen has GROWN scope (beyond-parity
keeps), not shrunk it -- watch that, not skipping.

FIRM-MEETING QUEUE (added this round): (1) does the firm run
billing/trust inside Docketwise or in QuickBooks/elsewhere? (2)
what is their fee-structure mix (flat-fee vs hourly)? Context: this
child launched deliberately ahead of the ledger's revisit trigger
"friend feedback surfaces billing/trust pain"; the meeting validates
demo emphasis, not the schema (bar rules and corpus criteria are
feedback-immune).

### RATIFICATION (2026-08-03)

James, after r6 and the invitation to red-pen the verifier sections:
"this is good continue". Treated as explicit ratification per the
prior turn's framing (agent flagged the interpretation openly with a
revert offer). goal.md stamped RATIFIED 2026-08-03. Phase 0 begins.
METHOD: six rounds, six keeps, zero kills -- first trial where the
red-pen GREW scope; the draft arrived pre-shrunk because the
strategic flag (2026-08-01) had already done the scope-cutting a
red-pen normally does. Candidate-list-primes-not-bounds held: r6's
deferral-load check was James's own worry, not a primed candidate.

### P0 execution (2026-08-03, same session as ratification)

Oracle-first, all artifacts in this folder; ../casework untouched
except a read-only spine run. Evidence:

- SPINE BASELINE captured BEFORE any billing work: "spine: 107
  green, 0 red, 0 pending; checks pass" -> verify/spine-baseline.txt.
- billing-map.json DRAFT: 25 entries = 21 direct + 4 adapted
  (online-card-payment, invoice-sharing, bulk-invoice-sharing,
  payment-plans) + 0 parked. Adapted wordings written in full; the
  three design notes record the rate-design hole, the
  payment-method conflict resolution, and the fx-0056 heading
  ambiguity.
- design/ledger-design.md + ledger-schema-draft.sql: liability
  account model (trust funds are liabilities; F2 falls out of
  double-entry), append-only journal with the single
  clearing-annotation exception, external event stream, closed
  recipe vocabulary, enforcement matrix. DDL is standalone-
  instantiable for self-testing; enters gen_schema.py only after
  the gate.
- verify/run_fiduciary.py: F1-F5, F8 implemented; F6 partial by
  design (linkage deepens P3, noted in-file); F7 stub that reports
  NO-STATEMENT and can never read as PASS. Selftest output:
  "selftest: draft DDL instantiated; empty ledger 6/6 non-stub
  checks pass; calibration scenarios: all behaved" -- calibration =
  each check driven RED by a deliberately broken scenario (F1
  unbalanced, F2 control mismatch, F3 overdraft, F4 availability,
  F5 missing sub-leg, F6 arithmetic), F8 probe held under direct
  UPDATE/DELETE attack, clearing allowed exactly once and
  re-clearing blocked.
- verify/run_billing.py harness: runs, "billing: 0 green, 0 red,
  25 pending, 0 parked; verdict: NOT GREEN", exit 1 -- correct
  pre-feature state.

METHOD: oracle calibration (driving each check RED on purpose)
recovers the churn-visibility signal op rule 7 flagged as going
invisible -- the oracle's discriminating power is now evidence on
disk, not an assumption.

### P0 GATE RATIFIED (2026-08-03)

James: "Ratified." -- after reviewing the executed walkthrough (full
lifecycle posted through the recipe vocabulary on the draft DDL:
journal e1-e9, F2 identity holding at 2,750.00 == 2,750.00, suite
7 pass / 0 red / 1 stub, overdraft attack caught RED by F3+F4,
immutability attack blocked by trigger). Gate covered all three
items per ledger-design.md section 7: (1) billing-map.json classes
+ adapted wordings, (2) ledger design incl. the liability account
model, (3) F1-F8 list + enforcement matrix. Zero kills at this
gate.
METHOD: artifact-first at gate scale -- the ratification request
was answered with "give me the raw material," and the raw material
that worked was an EXECUTED scenario (journal + balances + attacks
on screen), not the design prose. Same mechanism as red-pen rule 1,
one level up.

### Post-gate: schema landed in casework (2026-08-03)

- Ratified DDL merged into ../casework/app/schema/gen_schema.py in
  generator idiom (TABLES tuples + BILLING_EXTRA_SQL for the
  immutability wall and partial unique indexes); journal_entries,
  journal_postings, external_events added to APPEND_ONLY.
- GENERATOR FIX (pre-existing latent bug, surfaced by our tables):
  soft-delete columns were appended AFTER table-level ("", ...)
  constraint rows -- invalid SQL the moment a soft table carries a
  table CHECK. generate() now emits real columns + tombstones +
  constraints in that order. No existing table changed shape;
  schema.sql regenerated.
- Evidence: schema.sql builds clean, 80 tables (66 + 14 billing).
  Spine regression: "spine: 107 green, 0 red, 0 pending; checks
  pass" -- matches verify/spine-baseline.txt.
- Generated-schema probe: amount UPDATE blocked, entry DELETE
  blocked, clearing UPDATE allowed once with audit row carrying
  cleared_at, re-clear blocked. The wall behaves identically to the
  ratified draft.
- P1 unit table drafted into plan.md for the phase gate (4 parity
  targets: module-exists, trust-bank-accounts, trust-ledger,
  trust-disbursements).

### P1 GATE RATIFIED (2026-08-03)

James, on the plan.md unit table read in full: "This looks good. I
think you can go ahead and continue work." Unit table U1.1-U1.4
ratified as drafted, zero kills. Unattended execution begins
(MIXED mode: harness is judge inside the phase; next supervised
gate is the P2 transition).

### P1 execution (2026-08-03, unattended after gate)

U1.1 ENGINE: app/ledger.py -- recipes as the only posting surface,
F3/F4 blocks before write (savepoint-atomic), F5 conformance via
RECIPE_ACCOUNT_KINDS (drift-guarded against the verifier's copy by a
unit test), event co-writes, reverse_entry with availability checks
(reversing a spent deposit blocks -- the subtle case, tested).
Engine unit tests: 7/7 PASS FIRST RUN (churn: 0 engine-side red
iterations all phase).

U1.3 PARITY (tests authored before views): trust-bank-accounts,
trust-ledger, trust-disbursements GREEN. Churn: 1 test-side red --
my test misread fx-0053 ("trust transactions AT THAT LEVEL"):
matter-level-only clients do not appear on the client tab; the
implementation was right, the test expectation was wrong. Fixed
test-side, criterion re-quoted in the assertion.

DEVIATION (flagged for the P2 gate, per goal iteration rules):
module-exists promised green in the ratified P1 table, delivered
PENDING. Cause found at implementation: its criterion requires
"invoicing AND trust accounting functions available" -- invoicing
functions are P2 scope; greening it in P1 would test a promise, not
a capability. Moved to P2 targets. P1 delivers 3 of the promised 4.

U1.2 SEED: gen_seed.py billing_section BUILDS the scenario through
the live recipes in-memory and dumps the rows -- the seeded journal
is recipe-produced by construction and cannot drift from ledger.py.
seed.sql sha 539be0f9... byte-identical across two regenerations.
Fiduciary on seeded db: 7 pass, 0 red, 1 stub (F7 NO-STATEMENT by
design), report byte-identical x2 (9ab2fc6e...). Churn: 3 test-side
seed-tolerance iterations (absolute balances -> relative bases;
first-account picks -> own-account lookups). Zero engine-side.

DESIGN NOTE (logged, not built): journal_entries.posted_at carries
the caller-supplied BUSINESS date; wall-clock truth lives in
audit_log.at. A posting-date vs effective-date split would need a
schema change (Approval-required post-gate); flag for James only if
reconciliation work in P5 shows the conflation costing something.

U1.4 CLOSE evidence:
- billing: 3 green, 0 red, 22 pending, 0 parked (report sha
  65dd8275..., deterministic)
- unit_ledger: 7/7 pass
- fiduciary --seeded: 7 pass / 0 red / 1 stub, x2 byte-identical
- spine regression: 107 green, report IDENTICAL to pre-billing
  baseline (diff clean) -> verify/regression-p1.txt
P1 churn total: engine 0, tests 4 (1 criterion misread + 3
seed-tolerance).

METHOD: op rule 7 held again -- the churn concentrated entirely in
test fixtures aging against a changing substrate (the new seed),
never in the oracle-first-designed engine. Same signature as
casework's P0-anticipated-tables effect.

### P2 GATE RATIFIED (2026-08-03)

James: "This is solid. I like it." -- P2 unit table ratified as
drafted, zero kills; the P1 module-exists deviation and its U2.3
resolution path acknowledged in the same ruling (state.md put both
in front of the gate explicitly). trust-requests stays P3.
Unattended P2 execution begins.

### P2 execution (2026-08-03, unattended after gate)

U2.1-U2.3 in app/billing.py -- the distinct billing module
(module-exists resolved per the acknowledged P1 deviation: it
imports the trust family from app/ledger.py and carries the
invoicing family itself). Numbering honors fx-0076's odd corners
(enable = no renumber, counter from firm total, editable start);
Paid is derived, never stored; firm defaults are copied at creation
so they apply forward and stay overridable; late fees ride
scheduler.tick (one additive call added to app/scheduler.py -- spine
untouched by it, verified below); percent fees are basis points of
outstanding balance, integer math.

DESIGN NOTE / small deviation (flag at P3 gate): decision default 7
assumed invoice PDFs ride "the existing casework render machinery"
-- render.py turned out to be AcroForm-fill only (official forms),
no free-document path. Invoice PDFs use fpdf2 (2.8.5, already
installed per-user). Spanish chrome strings live in
billing.INVOICE_STRINGS rather than the intake language packs
(those key on q.* question keys); fx-0052 exclusions asserted by
test.

U2.4 CLOSE evidence:
- billing: 10 green, 0 red, 15 pending -- ALL SEVEN P2 targets
  green FIRST RUN (churn: 0 red iterations this phase, engine and
  tests both)
- billing-report byte-identical x2 (sha 5503e4b5...)
- unit_ledger: 7/7; fiduciary --seeded: 7/0/1-stub
- spine: 107 green, report identical to baseline ->
  verify/regression-p2.txt

METHOD: zero-churn phase. The P1 pattern (churn lives in fixture
assumptions, not oracle-designed code) plus seed-tolerant test
style adopted after P1 left nothing to iterate on.

### P3 GATE RATIFIED (2026-08-03)

James: "Nice P3 looks good. Continue." -- P3 unit table ratified as
drafted, zero kills; the fpdf2-instead-of-render.py deviation
acknowledged in the same ruling (it was named in the gate
presentation and in state.md's open decision). Unattended P3
execution begins.

### P3 execution (2026-08-03, unattended after gate)

U3.1/U3.2 in app/billing.py: record_payment dispatching to ledger
recipes (direct on bill -> operating+fee income; direct on trust
request -> trust deposit at the invoice's level; trust transfer ->
earn_out with available-amount helper); one-charge association with
the fx-0057 larger-than-charge block; edit = row UPDATE + journal
reversal/repost (r2 machinery earning its keep -- the parity test
asserts the old entry is reversed, never mutated, and runs the F8
sweep inline); refund = full-amount toggle + reversal + automatic
processor refund for platform payments (fx-0055).

U3.3: app/processor.py -- FeeSplitProcessor sim (3% + 30c,
SYNTHETIC- tokens only, SYNTHETIC-DECLINE always declines).
Charges authorize immediately; money moves at settle(): one batch
per destination bank, trust batches FORCED gross (F6 made
unrepresentable in code), fees pulled from operating via a separate
fee event + processor_fee entry. Settlement entries link to shared
processor_batch external events via journal_entries.external_event_id
(ledger._post extended additively). Chargeback = posting event
debiting operating, r3 boundary held. Pay page: /invoice/<token>
view/pdf/pay routes added to server.py (additive branches; spine
unaffected). Auto-receipt via email_outbox (fx-0076). F6 DEEPENED
in run_fiduciary: + net-mode-trust-batch detection + event-linkage
assertion (booked postings == event amount per processor_batch).

U3.4: payment plans -- installments generated to cover the balance
at creation (attested fields only, r4), 7-before/due/7-after
reminders via email_outbox on the tick, auto-charge composing
SimProcessor + settlement recipes with a deterministic
SYNTHETIC-AUTOPAY-<plan> token (no stored-payment-method column;
schema change would be Approval-required -- logged design note).

U3.5 CLOSE evidence:
- billing: 18 green, 0 red, 7 pending -- ALL EIGHT P3 targets
  green FIRST RUN. Churn: 0 red iterations; 2 pre-run review fixes
  (declined-attempt ordering vs zero balance; pay route catching
  BillingError) caught by desk-check before any run.
- billing-report byte-identical x2 (sha 65efdb67...)
- unit_ledger 7/7; fiduciary --seeded 7/0/1-stub (F6 deepened,
  still green); spine 107 green identical to baseline ->
  verify/regression-p3.txt

METHOD: two consecutive zero-red-churn phases. Paper-design-first
plus criteria-quoted-in-assertions is holding the iterate loop at
zero; the compaction falsification target stays unreachable at this
token efficiency (same Trial 3 dynamic).

### P4 GATE RATIFIED + P5 PRE-AUTHORIZED (2026-08-03)

James: "Oh yeah U4 looks good and so does U5 if you want to keep
going or P5." -- P4 unit table ratified as drafted; P5 execution
pre-authorized against plan.md's P5 section (recon + anchor walk +
close). The P5 unit table is drafted into plan.md before its
execution per the standing pattern; its gate ruling is this
pre-authorization. Unattended execution through both phases.

### P4 execution (2026-08-03, unattended)

U4.1 app/timekeeping.py: attested duration formats parsed exactly
(2h/36m/2.8h/5.5m), timer start/stop/resume accrual, contact/matter/
firm-wide lists with filters, per-user default rate in user_settings
+ per-entry override, charge = duration x rate half-up integer math.
U4.2 billing.py: email share to any contact with a valid email
(fx-0068 third-party receiver, contact-info confirmation returned),
recurring reminders that stop at zero balance, bulk share both
attested modes (zip-to-one / each-to-own), bulk download zip.
U4.3 invoice access levels on casework's user_permissions
(unlimited/limited/none, limited = no edit/delete on others'
invoices, admin bypass). U4.4 CSV exports (invoices, payments, time
entries, trust ledger) + supporting checks wired into run_billing:
csv round-trip (cols x rows vs table counts) and float sweep (no
REAL columns, no float() on cents paths).

PARITY MAP COMPLETE: billing: 25 green, 0 red, 0 pending, 0 parked;
checks pass; verdict GREEN, exit 0. Churn: 1 red iteration (share
row's wall-clock created_at defeated the deterministic reminder
test; fixed with an explicit share_date parameter -- a real API fix,
not a test patch). Spine: 107 green identical to baseline ->
regression-p4.txt. unit_ledger 7/7.

### P5 unit table (pre-authorized gate; drafted before execution)

| Unit | Deliverable                                             |
| ---- | ------------------------------------------------------- |
| U5.1 | verify/bank_statement.py: statement generator reading   |
|      | ONLY external_events through the clearing-lag model     |
|      | (deposit T+2, check T+3, processor batch T+1) -- the    |
|      | independent witness (F7 independence clause)            |
| U5.2 | verify/reconcile.py + F7 LIVE in run_fiduciary: bank +  |
|      | deposits-in-transit - outstanding = book = sub-ledger   |
|      | sum, per account, at two period ends (mid-lag and       |
|      | all-cleared); every item enumerated with a cause;       |
|      | statement-line/book matching with zero unmatched        |
| U5.3 | verify/run_anchor_billing.py: fresh-db scripted walk    |
|      | (install -> admin -> contact/matter -> accounts -> trust|
|      | request -> HTTP sim payment -> settle -> bill with saved|
|      | charge + imported time entry -> trust-transfer earn-out |
|      | -> disbursement -> invoice PDF read back -> recon       |
|      | artifact -> audit continuity -> fiduciary green) under  |
|      | the 900s budget, timings reported                       |
| U5.4 | Close: x2 byte-identical billing + fiduciary reports,   |
|      | final spine capture (regression-report.txt), map        |
|      | statuses green, reciprocal guard into casework          |
|      | CLAUDE.md, self-audit a-d, result.md                    |

### P5 execution (2026-08-03, unattended; pre-authorized gate)

U5.1 verify/bank_statement.py: statement from external_events ONLY
(independence clause honored structurally -- the module never opens
the journal), clearing lags deposit T+2 / check T+3 / batch T+1.
U5.2 verify/reconcile.py + F7 LIVE: bank + DIT - outstanding = book
= sub-ledger sum, linkage-then-exact matching, zero unmatched
tolerated. Fiduciary on seeded db: 8 pass, 0 red, 0 stub, GREEN
exit 0, with 6 genuine reconciling items enumerated at the mid-lag
period -- the lag model produced real items, not a vacuous pass.
U5.3 verify/run_anchor_billing.py: 12-step fresh-db walk PASS,
1.336s of 900s budget: install -> admin -> contact/matter ->
accounts -> direct-paid consult (funds operating) -> trust request
paid by the client over real HTTP via SimProcessor -> settlement
(gross 5,000.00 to trust, fee 150.30 from operating) -> bill with
saved charge + imported 2h time entry earned out of trust ->
1,200.00 USCIS disbursement -> invoice PDF read back -> three-way
recon HOLDS both banks both periods (recon-report.txt) -> audit
continuity system/user/contact -> fiduciary GREEN on the walked db.
Churn: 1 environment iteration (Windows temp-dir teardown needed
the db connection closed; not a logic red).

U5.4 CLOSE evidence:
- billing-report: GREEN exit 0 x2 byte-identical (acba95b1...)
- fiduciary-report: GREEN exit 0 x2 byte-identical (af2e242f...)
- unit_ledger 7/7; spine 107 green identical to pre-billing
  baseline -> verify/regression-report.txt (completion-proof name)
- billing-map.json: all 25 entries green
- RECIPROCAL GUARD delivered: casework/CLAUDE.md "How to run" now
  requires both suites for any session touching app/ (red-pen r6
  completion-proof item)

### Final self-audit (goal.md operating mode, items a-d)

(a) COMPACTION: no compaction event occurred in this session; the
    build ran bootstrap-through-close in one continuous session
    without context exhaustion. The files were maintained
    compaction-ready throughout (evidence on disk at every unit
    close). The method's #1 falsification target nulls again, same
    cause as Trial 3: paper-design-first collapsed the iterate
    loops that would have burned context.
(b) STATE SUFFICIENCY: no cold resume occurred (single-session
    build), so the 3-for-3 cold-resume record neither grows nor
    shrinks. state.md was rewritten at every phase close and the
    P0->P5 chain re-oriented from files alone at each gate
    presentation without a wrong turn.
(c) BLOCKER RULE: no blocker candidate reached even one full failed
    approach, let alone the three-turn threshold. Untested at n=4.
(d) LOG-DON'T-BUILD: honored in real time -- the fpdf2 deviation
    (P2), the module-exists deviation (P1), the SYNTHETIC-AUTOPAY
    token design note (P3), and the posted_at business-date note
    (P1) were each logged at the moment of decision and carried to
    the next gate. No wind-down backfill was needed.

### Churn record (op rule 7 residual), full run

| Phase | Red iterations | Nature                                 |
| ----- | -------------- | -------------------------------------- |
| P0    | 0              | (selftest calibration by design)       |
| P1    | 4              | 1 criterion misread + 3 seed-tolerance |
|       |                | -- all test-side, engine 0             |
| P2    | 0              | --                                     |
| P3    | 0              | 2 pre-run desk-check fixes, no reds    |
| P4    | 1              | wall-clock share date vs determinism   |
|       |                | (real API fix: share_date param)       |
| P5    | 1              | Windows temp-dir teardown (env, not    |
|       |                | logic)                                 |

Engine/oracle-designed code: zero red iterations across the run.

### METHOD notes

- METHOD: interview ran 4 questions, one decision per turn, each
  with a recommended option; all 4 recommendations accepted. Map
  shown before each ask (collaboration rule held).
- METHOD: op-rule-7 fit is unusually strong here -- double-entry
  invariants are wholesale-assertable, so the fiduciary oracle can
  exist before any feature code. This child is a low-risk place to
  observe oracle-first on a domain the corpus does NOT specify
  (F-checks are ours, not Docketwise parity).
- METHOD: skill guidance "draft strawmen for anything with concrete
  structure" applied to processor stance, rate design, verifier
  shape -- none interviewed, all landed as decision defaults for
  the pen.
