# worklog.md -- billing-ui (append-only)

## 2026-08-03 -- s1: bootstrap (root-level session -> child scaffold)

Origin: casework-billing wind-down left successor candidates; James
answered the r6 firm-meeting queue item -- the firm runs billing and
trust INSIDE Docketwise; the AffiniPay/8am take is "A" problem
alongside training/usability cost (rake = wedge, interaction cost
remains the core thesis). This fired trigger (b) of the 2026-08-01
strategic flag and resolved demo emphasis toward billing/trust.

Rulings, in order (all James, 2026-08-03):

1. Direction: make billing visible (option 1 of 4 mapped). James:
   "I need to start seeing this thing in a bit better shape... I
   commit to spending some time with UI."
2. PROGRAM RULING ratified: billing-ui extends casework-ui/app_ui
   IN PLACE (mirrors the casework-billing amendment). Hard limits
   recorded in ../CLAUDE.md: run_ui_walk green at gates;
   casework-ui/goal.md + cold-run oracle + hold untouched; casework/
   frozen; rendering only; oracle is James-driven, not cold-run.
3. Operating mode: HYBRID (new mode variant, first trial) -- agent
   builds phases unattended against a mechanical walk verifier;
   every phase gate ends with James reviewing rendered screens.
4. Screen scope: tiers 1+2 interactive (walk path + fiduciary
   visibility + corrections family, 16 entries), tier 3 HELD (9
   config/bulk entries; defaults active invisibly). James: "One and
   two both look good... hold on three."
5. Quality bar: DEMO-GRADE -- billing screens deliberately the best
   surfaces in the product; existing screens not restyled;
   shared-shell changes are gate decisions. James flagged the risk
   himself: "It's not going to go too quickly. I find with AI I end
   up getting stuck sometimes" -> anti-stall default drafted into
   goal.md (2 polish iterations then park for the gate).

Bookkeeping done at root level before scaffold: amendment + roster
row in ../CLAUDE.md; r6 closed in ../casework-billing/state.md
(flat-fee vs hourly mix still unasked, carried forward).

Scaffolded via project-kit (folder + CLAUDE.md). Drafted goal.md
[DRAFT], plan.md, this file, state.md. goal.md NOT ratified; red-pen
next.

METHOD: first HYBRID-mode trial -- neither Trial 1's supervised
cadence nor Trials 2/3's unattended runs. Gate-review cadence is the
new mechanism under test: does James's screen time land efficiently
at gates, and does the anti-stall park rule prevent the polish loops
he predicts?

METHOD: this goal deliberately brushes the fuzzy-goal boundary
(falsification list #3): the final oracle includes a human
demo-grade verdict that no mechanical check can stand in for. The
mechanical walk bounds it from below. Watch whether the verdict
criterion ("would show the firm") stays decidable at walk day.

METHOD: interview honored the Trial-3 ordering -- operating mode
taken early; verifier/oracle detail (walk steps, 20:00 budget,
protocol) drafted as strawmen, not interviewed. Three interview
rounds, one decision each, zero stacked prompts.

## 2026-08-04 -- s1 cont: red-pen rounds on goal.md

- Round 1 (candidate 1, 20:00 soft walk budget): SPARED -- "leave
  for now." Budget stays; friction log still primary; revisit only
  if it reads as noise on walk day.
- Round 2 (candidate 2, dedicated online-card-payment screen):
  KILLED, by agent pick -- James explicitly 50/50, delegated
  ("pick one"). Status folds into invoice + trust-request screens
  as a line/badge; client pay page stays frozen casework code.
  Rationale: status where the object lives beats a navigable page
  that exists to hold one fact; one less surface to polish. [AJ]
  marked in goal.md tier-1 table.
- Round 3 (candidate 3, demo seed script): SPARED -- James agreed
  with the keep lean. Rationale on record: demo-grade browse
  screens judged at n=1 walk data hides layout failure at realistic
  volume; the seed is the cheap insurance. Constraint unchanged:
  seed calls casework/app modules only, no direct SQL writes.
- Round 4 (candidate 4, gate-2 informal lifecycle rehearsal):
  SPARED -- "Keep it. I can keep doing UI... it's found a lot of
  issues." James's own rehearsal history (casework-ui r1-r5) is the
  evidence base: hands-on passes surface findings the mechanical
  walk cannot. Rehearsal stays informal -- not the oracle, no
  stopwatch, findings feed P3.
- Round 5 (candidate 5, demo-grade verdict wording): CONVERTED --
  holistic "would show the firm" restructured into three named
  up/down sub-verdicts, all required: (a) fiduciary story lands,
  (b) nothing embarrassing, (c) bookable. Rationale: keeps the
  human gut check (c) while making a FAIL diagnosable by axis.
  METHOD: this is the fuzzy-goal boundary treatment -- decompose
  the fuzzy verdict into named answerable questions rather than
  pretending a mechanical proxy exists. Watch whether (a)-(c) stay
  decidable on walk day.
- Candidate list exhausted; James invited to review beyond it
  (Trial-3 lesson: the list primes, never bounds). No kills of his
  own raised. RATIFIED 2026-08-04, explicit. Tally: 5 rounds, 1
  kill (r2), 1 conversion (r5), 3 spares (r1, r3, r4), all with
  rationale above. DRAFT header stripped; plan.md swept for the r2
  kill (P2 wording updated). P0 (oracle first: run_billing_ui_walk
  RED before any screen) starts next session, launched from
  billing-ui/ per the goal-method launch rule.

METHOD: bootstrap span -- root-session direction ruling through
ratification in one sitting plus one date boundary; interview 3
rounds + red-pen 5 rounds, every prompt one decision. The primed
candidate list produced 2 of 2 changes this time (no reviewer-side
kill emerged, unlike Trial 3) -- n=1 against the lesson, not a
refutation of it.

## 2026-08-04 -- s2: P0 executed (oracle first); TWO SUBSTRATE
## FINDINGS; gate 0 OPEN

P0 artifacts, all on disk:

- verify/run_billing_ui_walk.py -- 17 steps + float sweep, driven
  RED: 3 pass (setup/login, contact+matter via existing screens,
  tier-3 fence vacuously), 14 PENDING, 0 fail; verdict ON TRACK,
  exit 1 (billing-ui-walk-report.txt). The route names it drives
  are the P1/P2 interface contract (/billing, /billing/trust,
  /billing/invoices/<id>, /billing/recon, ...). Amount story
  mirrors run_anchor_billing.py.
- verify/demo-walk-protocol.md STRAWMAN, cold-run-protocol format:
  12-step walk sheet, M0-M6 marks, soft 20:00 M1->M6, close-out via
  check_demo_walk.py (named, deliberately unbuilt until the
  protocol survives gate 0), three-sub-verdict sheet.
- verify/seed_demo.py -- module-only writes (db created through
  app_ui make_server so install+marker ride the UI's own path);
  4 clients, 4 matters, 9 invoices (paid/partial/outstanding/
  draft), 2 settled retainers, 2 disbursements, 4 time entries.
  GREEN x2, deterministic: "fiduciary: 8 pass, 0 red, 0 stub".
  Login demo.reviewer@synthetic.test / demo-seed-pass.
- verify/gate-receipts/gate-0-*.txt -- all four standing suites,
  run this session, quoted: ui-walk 13 pass GREEN exit 0; spine
  107 green exit 0; billing 25 green exit 0; fiduciary 8 pass
  GREEN exit 0.

FINDING 1 (F7 x corrections): editing OR refunding any
journal-backed payment breaks F7 three-way reconciliation.
Bisect (scratchpad f7_bisect.py, quoted): baseline PASS;
date-only edit -> 1 identity break; refund -> 1 identity break.
Cause read from frozen code: ledger.reverse_entry posts NO
compensating external event, and edit_payment's repost calls the
payment recipe fresh, writing a DUPLICATE external event
(casework/app/billing.py 425-456, ledger.py 283-299). Bank truth
and books diverge on every correction of real money. Latent in
casework-billing because its F7 scenarios never corrected an
external-legged payment.

FINDING 2 (F7 x settlement batches): the recon matcher matches
postings to batch events 1:1 only. A settle() covering two online
payments wrote ONE processor_batch event (1,300,000) against TWO
settlement postings (500,000 + 800,000); arithmetic held but the
second posting reported UNMATCHED -> identity break. Any real
firm's multi-payment settlement day hits this. Latent for the
same reason: prior scenarios settled exactly one payment per
batch.

Both fixes live in FROZEN surfaces: casework/app (ledger/billing)
and the sealed fiduciary suite's statement/recon model
(casework-billing/verify). Cross-project gate decision -> James.
Interim: seed made correction-free and 1:1-settled (green);
protocol step 10 carries a GATE-0 FLAG inline; walk verifier step
10 stays as drafted pending the ruling.

METHOD: op rule 7 earning its keep at program scale -- building
the oracle before any screen surfaced two latent substrate defects
that three green verifier suites (billing 25, fiduciary 8, anchor
walk) never exercised. The demo walk's step combinations (correct
a payment, then reconcile THE SAME BOOKS) are exactly the
cross-feature seams module-scoped scenarios miss.

## 2026-08-04 -- s2 cont: gate-0 decision RULED; cross-project fix
## LANDED and resealed

James ruled option 1 ("approve the recommendation"): fix the model.
Program ruling recorded in ../CLAUDE.md (scope: casework/app
ledger+billing correction semantics; casework-billing/verify
statement/recon model + F7 scenarios; spine tests immutable;
fiduciary strengthens only; full reseal required).

Design as landed (one revision mid-flight): the first cut mutated
external_events in place and was REJECTED BY THE SUBSTRATE -- the
schema enforces append-only on external_events too ("external_events
is append-only" trigger). Correct design, and the one shipped: BOTH
ledgers are append-only; a correction appends mirror bank events
dated the correction, the repost appends its replacement events,
and a refund appends real compensating events. The correction story
is visible on the bank side exactly as reversal+repost is visible
in the books -- better accounting than the in-place idea it
replaced. Mechanics:

- billing.record_payment restructured: the payment row is created
  BEFORE the journal posts (savepoint-guarded), so external events
  carry payment_id from birth -- the linkage corrections need.
- billing._payment_event_specs + _append_mirror_events: bank-event
  shapes reconstructed from the payment row (no event lookups, no
  ambiguity on repeat edits); edit_payment and refund_payment
  append mirrors dated the correction/refund.
- ledger recipes accept replaces_entry_id and stamp it through
  _post (provenance was silently dropped before).
- reconcile.three_way: n:1 linkage-group matching for cleared
  lines AND the pending file (one batch event, several postings;
  signed sums must equal). A pair-cancellation hack written before
  the append-only redesign was REMOVED -- it would have masked real
  discrepancies.
- run_fiduciary.seeded_db: F7-lock overlay (amount edit, full
  refund, 2-payment batch through real billing machinery) rides
  the seeded gate. Deliberately NOT in seed.sql: first attempt put
  invoices in the shared seed and broke parity's
  global-invoice-numbering test (24 green 1 red) -- the parity
  suite's seeded world must stay exactly as sealed. gen_seed.py
  reverted to ledger-only.

Evidence, all run this session:
- bisect (scratchpad): baseline/edit-date/edit-amount/refund/
  multi-batch ALL PASS, 0 identity breaks.
- fiduciary --seeded x2: "8 pass, 0 red, 0 stub; GREEN", sha
  fb5bccda x2 -- SUPERSEDES sealed af2e242f (recorded in
  ../casework-billing/state.md). Selftest: calibration all behaved.
- billing parity x2: "25 green, 0 red", sha acba95b1 x2 --
  IDENTICAL to the sealed sha (report content untouched by fix).
- anchor billing: PASS 1.284s of 900s, fiduciary green on walked db.
- spine: 107 green. ui-walk: 13 pass GREEN.
- billing-ui walk: 3 pass / 14 pending / 0 fail, ON TRACK (correct
  P0 shape). seed_demo GREEN x2 WITH corrections + the
  multi-payment batch restored as regression witnesses.
- gate-receipts/ refreshed with post-fix runs.

Protocol step 10 gate-flag removed: the correction step is fully
walkable. Gate 0 remaining: protocol red-pen + nav approval.

METHOD: the substrate's own append-only trigger vetoed a wrong
design before any test did -- schema-level contracts catching the
agent's first idea is the trust thesis defending itself. Logged as
the session's second-best defect catch after the oracle itself.

## 2026-08-04 -- s2 cont: protocol red-pen (James, remote round):
## mechanical steps are AGENT-EXECUTED

James: "Why not run this headless with puppeteer? ... 'the
recorder runs' -- I feel like that should be a step you take."
Ruling extracted and applied: every mechanical step in the
protocol is EXECUTED by the agent in-session, never typed by
James -- server start (fresh dated db, background, /setup
confirmed), pre-walk oracle run quoted GREEN, close-out
check_demo_walk run quoted. James's surface: a URL, the sheet,
the stopwatch, the verdicts. Setup + Close-out sections rewritten.
Gate mechanics added to plan.md: agent captures per-screen
screenshot decks via the session's Chrome tools before each gate.
Puppeteer itself declined with reasons on record: (a) the walk
verifier already drives the full surface headless -- urllib sees
exactly what Chrome sees on a zero-JS app; (b) node_modules would
fail the ratified js-discipline sweep. The valuable half of the
suggestion (automated visual capture for the demo-grade axis) is
adopted via the Chrome tools instead.

- Ordering ruling (James, same round): "do your run first then
  I'll do my walk sheet... otherwise I'm stuck catching errors
  that you might quickly fix." Encoded as a standing rule in
  plan.md: agent's mechanical run precedes James's hands at EVERY
  touchpoint (gates, rehearsals, walk day) -- his pen judges
  shape, the oracle catches errors, James never debugs by
  walking. Protocol setup already carried the walk-day half.

## 2026-08-04 -- s2 cont: protocol RATIFIED; check_demo_walk built

demo-walk-protocol.md RATIFIED by James at gate 0, as amended
(agent-executed mechanics, ordering rule, live step 10). Strawman
header stripped; edits now require a gate.

check_demo_walk.py built per close-out step 1 (the protocol binds
it): 11 story receipts keyed to walk-sheet steps + fiduciary suite
in place. Tested both ways, quoted: module-built walked-story
replica (scratchpad walked_db_sim.py, same amounts as the sheet)
-> 12/12 PASS exit 0; non-walked db (the seeded browse db) ->
FAIL on correction trail, exit 1. Note: the seed shares story
amounts with the sheet, so several receipts pass coincidentally
there -- the trail + settlement receipts are the discriminators;
acceptable, the checker's job is walked-db verification, not db
identification.

Gate 0 remaining: ONE item -- nav "Billing" shared-shell approval.

## 2026-08-04 -- s2 cont: GATE 0 CLOSED (nav approved); P1 opens

James: "Approved." Nav "Billing" entry authorized (one line in
app_ui/html.py NAV_ITEMS -- the only shared-shell edit; everything
else lands in new files plus one dispatch hook in server.py's
authed router). Gate 0 complete: ruling, protocol ratified,
checker built, ordering rule, launcher, nav. P1 build starts:
read surfaces (landing + tiles, trust/accounts, ledger drill-down,
journal detail w/ correction trail, recon view, invoice list/
detail, time list), billing stylesheet layered per goal.md
default, empty states designed. Gate 1 = screenshot deck on the
seeded db + first demo-grade calibration.

## 2026-08-04 -- s2 cont: P1 BUILT; GATE 1 OPEN

Built (app_ui, per ruling): billing_ui.py (rendering only, zero
SQL; recon screen imports the F7 engine itself from
casework-billing/verify so the screen cannot drift from the
oracle -- design note, deliberate dependency on the verifier, not
the reverse); reads.py extended with SELECT-only billing readers;
NAV_ITEMS "Billing" line (the approved shared-shell edit);
server.py one dispatch hook. Seven screens: landing (tiles: trust
/ operating / outstanding + tabbed invoice list), invoice detail,
trust overview, account ledger (sub-ledgers + entries, negatives
parenthesized), journal detail (dr/cr postings + correction trail
box + bank record), three-way recon (renders reconcile.three_way
per account, HOLDS/BROKEN pills, items with causes), time list.
Every screen has a designed empty state. Dataviz skill consulted
for the tiles (stat-tile form; status pills carry words, money in
ink).

Verified this session, quoted: billing-ui walk "4 pass, 13
pending, 0 fail ... ON TRACK" (landing step green; zero FAIL);
ui-walk "13 pass ... GREEN" (sweeps accept the new files -- SQL
confined, no JS); spine 107; billing 25; fiduciary --seeded 8
GREEN. Smoke: 9 screens 200 + designed 404s on tier-3/unknown
paths. Gate-1 receipts + 7-screen deck banked to
verify/gate-receipts/ (gate-1-deck/).

Anti-stall ledger: 1 of 2 polish iterations spent (method-label
prettify "trust transfer (earn-out)"; time amounts read the
imported charge when billed). Both re-screenshotted.

METHOD: first hybrid-mode gate approaching with the ordering rule
live -- every verifier run preceded the screenshot deck; James
sees pixels only after the oracle passed them.

James hit the module-path failure live (`python -m app_ui.server`
only resolves from casework-ui/) plus a PowerShell paste death on
the protocol's wrapped command line. Fix: billing-ui/serve.py --
any-cwd launcher, all paths resolved from its own location;
defaults to a fresh dated demo-walk db (auto-date kills the
2026-08-XX placeholder trap for good), --seeded opens the gate-
review db, ports default 8500/8501. `atlas-ui` function added to
the PS 5.1 profile (machine config, absolute path lives there,
not in project docs). Verified from Desktop as cwd: / -> /setup
HTTP 200. Protocol setup section rewritten to the one-word
command; single-line, no wrap, no relative paths.

## 2026-08-04 -- s3: GATE 1 CLOSED; P2 opens

James, on the deck and the live seeded screens: "The demo and
live streams are good. I don't think there's anything to change
right now." Gate 1 verdict: PASS, zero kills, zero newly parked
items. The P1 read surfaces stand as the demo-grade visual
standard for everything after (first calibration banked without
correction -- the P1 styling choices are now the reference).
Anti-stall ledger resets per phase: P2 starts at 0 of 2.

P2 build opens (lifecycle writes, per plan.md): invoice creation
(saved charges + time import), time entry screen, trust request
create, record direct payment, trust-transfer earn-out flow,
disbursement flow, online-payment status lines. Walk steps 4-10
target green. Gate 2 = rendered review + James's informal
lifecycle rehearsal on a fresh db.

## 2026-08-04 -- s3 cont: P2 BUILT; GATE 2 OPEN

Built (app_ui, rendering only; every mutation calls a casework
module then commits): billing_ui.py grew the write surfaces --
accounts create; invoice create (bill + trust request as two
forms posting one route); add-charge form on invoice detail;
import card (checkbox picker over saved charges + unbilled time,
posting import_saved_charges/import_time_entries); record-payment
card (direct + trust-transfer earn-out; trust requests get a
deposit form that inherits their trust account); share-with-client
card rendering the client link (server.client_base + frozen
share token); settlement card on trust overview (processor.settle,
date defaults today); disburse form (client- or matter-level);
time entry form (parse_duration formats, rate optional ->
timekeeping default); saved-charges manage screen; invoice PDF
download (billing.invoice_pdf; pulled forward from P3 -- the walk
cannot Pending a missing link on an existing screen). cents_of
integer-cents form parser (float sweep stays clean). reads.py +2
SELECT readers (invoice_shares_of, unbilled_time_entries). Status
pills capitalized (Paid/Outstanding). Errors re-render the source
form with the module's message; rollback on failure.

TWO P0 DRAFTING ERRORS corrected in verify/run_billing_ui_walk.py
(own verifier, not a frozen suite; both were guesses about the
sealed substrate, both fixes assert the same story):
1. share-link regex expected a hex token; frozen share_invoice
   mints SYNTH-INV-<id>-<n>. Regex widened; the follow-through
   client POST still proves the link pays.
2. audit-chain expected entity_type 'bank_accounts'/'payments';
   schema triggers stamp raw table names (ledger_accounts /
   invoice_payments). Names corrected, same chain + ordering.

Verified this session, quoted: billing-ui walk "16 pass, 1
pending, 0 fail ... ON TRACK" (the one pending is payment edit --
P3's corrections family; steps 4-10 plus PDF, drill-down, recon,
audit chain, and fiduciary-on-walked-db all green); ui-walk "13
pass ... GREEN"; spine "verdict: GREEN" (107); billing "25 green
... GREEN"; fiduciary --seeded "8 pass ... GREEN". seed_demo
regenerated fresh, GREEN. Gate-2 receipts (all five reports) +
10-frame deck banked to verify/gate-receipts/ (gate-2-deck/).

Anti-stall ledger P2: 1 of 2 iterations spent (one CSS line --
submit buttons break onto their own line after selects; fixed
payment form + saved-charges form in one stroke; both
re-screenshotted for the deck).

METHOD: ordering rule held -- suites re-ran green AFTER the last
code edit (the CSS line), so the deck James reviews is the code
the oracle passed. The two verifier corrections are the
oracle-first cost surfacing early: contract drafted before the
substrate was read back, wrong guesses caught by the first real
run, fixed with rationale on record instead of silently drifting.

## 2026-08-04 -- s3 cont: gate 2 in progress -- deck half: zero
## kills so far; rehearsal db stood up

James on the gate-2 deck: "No kills yet." Deck red-pen open with
zero kills; gate NOT closed -- the informal lifecycle rehearsal
(spared at red-pen r4) remains. Mechanical setup executed per the
agent-executes ruling: fresh db server launched in background --
data/rehearsal-g2-2026-08-04.db on port 8502 (client surface
8503), / -> /setup confirmed HTTP 200 by probe; seeded browse
server stays on 8500 for deck comparison. Walk verifier standing
quote for this code state: "16 pass, 1 pending, 0 fail" (run
after the last edit, this session). Rehearsal findings will log
here and feed P3.

REHEARSAL FINDING 1 (PARKED, PROGRAM-LEVEL -- James ruled "park"
2026-08-04): the client intake questionnaire (casework/app/
server.py client surface, _intake_page) fails the interaction-
cost bar. James hit it live (snap 032405); code read-back
confirmed and amplified:
  (a) per-field Save: every field is its own form posting
      /intake/<token>/answer, which navigates AWAY to an "Answer
      saved" page -- fill-several-then-save-one silently DISCARDS
      the unsaved fields (natural fill pattern = data loss);
  (b) saved answers never re-render: _intake_page line ~204
      hardcodes value="" -- a returning client sees a blank form
      regardless of what is saved; no way to see what the firm
      received;
  (c) Submit for review saves nothing and verifies nothing --
      flips invitation status, bare thank-you page, no summary,
      no completeness check.
Scope: OUT for billing-ui (casework frozen; client-actor pages =
flagged gate decision by contract; off the P4 billing demo path).
Cause of existence: casework sealed under CAPABILITY parity --
every capability test over this screen passes; no contract has
ever held the client surface to interaction cost. ROUTE: to
whichever contract next owns the client surface (casework-ui
resume or a dedicated client-surface child). Carried in state.md
watch items until handed off; must surface in this child's
wind-down successor notes. An F7-style cross-project fix was
offered and NOT taken (this defect does not break this child's
walk path).

METHOD: second rehearsal-class catch at program scale -- the
mechanical suites are structurally blind to interaction cost
(capability tests pass over a surface that loses user data on the
natural fill pattern). Hands-on passes remain the only detector
for this class; r4's spare keeps paying.

## 2026-08-04 -- s3 cont: GATE 2 CLOSED (deck-only, rehearsal
## waived by ruling); METHOD finding: ratifier context

James, after the intake detour: "I'm losing track of the project"
-- not a screens problem, a program-legibility problem. Ruling
extracted: gate 2 closes on the deck alone ("they're good enough
to keep building on"); the informal rehearsal is WAIVED for this
gate (his hands-on time is still owed and scheduled where the
contract puts it: the P4 walk-day oracle). Rehearsal servers shut
down; rehearsal-g2 db retained.

METHOD (program-scale finding, first of its kind): the method
maintains AGENT continuity (state.md, worklogs, receipts) but
nothing maintains RATIFIER continuity. At five children deep the
gate-keeper lost the map while every file stayed immaculate --
the human context is the scaling bottleneck, not the agent's.
Interface change adopted, effective immediately: James's surface
is the PRODUCT plus ONE plain-language question per touchpoint;
jargon (child names, phase numbers, suite tallies) never appears
in a gate ask without inline translation; the plain-terms program
map is re-issued on demand and at every gate. His early symptom
("it's just too many steps for me to track but if you're saying
you're capable I think that's fine") was a rubber stamp forming
-- the method's gates are worthless if the ratifier signs on
trust. Carry this to the program retro.

## 2026-08-04 -- s3 cont: P3 BUILT (corrections family); walk
## FULLY GREEN x2; GATE 3 OPEN

Built: payment detail screen (payment row + full journal trail
via new reads.entries_of_payment -- own entries plus reversals
linked by reverses_entry_id -- + bank record with compensating
events); correction form (date / amount / charge re-association /
note -> billing.edit_payment, edit_date = today); refund (full
only -> billing.refund_payment); email share button
(billing.send_invoice_share; BillingError surfaces in the error
box when the contact has no email). Invoice payments table rows
now link to payment pages. Share card: two inline buttons
(create link / email).

FOURTH P0 drafting error corrected in the walk verifier (same
class as the first three -- guessed substrate): step 11 asserted
edit creates a SECOND payment row; the sealed model is ONE
payment row updated (audited) with the JOURNAL correcting by
reversal + repost. Assertion rewritten to the stronger true
claim: >=1 reversal entry, >=1 repost entry, and ZERO update
audit rows on journal_entries (posted entries never mutated).

Verified, quoted: billing-ui walk "17 pass, 0 pending, 0 fail
... verdict GREEN" exit 0 -- FIRST full green -- run x2,
timing-stripped sha a506f085 IDENTICAL both runs (report format
carries wall-clock; the x2 seal is on stripped content, noted in
plan.md). ui-walk 13 GREEN; spine 107 green; billing 25 GREEN;
fiduciary --seeded 8 GREEN. Gate-3 receipts + 3-frame deck
banked (payment-7 corrected trail, payment-4 refunded, invoice
share/email card) -- seeded db's own edited/refunded payments
are the demo witnesses.

Anti-stall ledger P3: 0 of 2 iterations spent.

Remaining to contract: gate 3 (deck red-pen + protocol final
red-pen + schedule walk day), then P4 walk day -- James drives
the ratified protocol on a fresh dated db, fiduciary green on
the walked db, three-part demo-grade verdict, completion proof,
result.md.

## 2026-08-04 -- s3 cont: GATE 3 CLOSED; git initialized;
## wind-down (James context reset)

James on the corrections deck: "I like this. It's starting to
feel like a thing. Yes we are good to continue" -- gate 3
verdict PASS, zero kills (third consecutive zero-kill deck).
Protocol final red-pen: no changes raised; demo-walk-protocol.md
stands AS RATIFIED at gate 0 (amended). One dead-link friction
mid-gate (the torn-down 8502 rehearsal server) produced the
ONE-ADDRESS RULE, recorded in state.md: James's URL is 8500,
always; db swaps happen behind the port.

All three build phases closed same-day with zero kills across
three decks. Remaining to contract: P4 only -- schedule walk
day, James drives the protocol on a fresh dated db, fiduciary
on the walked db, three-part verdict, completion proof,
result.md.

Wind-down at James's request (context reset). Git initialized at
the atlas program root per his commit-and-push instruction (the
workshop's git-when-earned ruling: this is the earning event).
Remote: github.com/JamesIsHere/workshop-atlas (PRIVATE; the name
'atlas' was taken on his account by an unrelated July project,
inspected and left untouched). Root commit 65b1dfb, 571 files;
*.db, data/, storage/, .env ignored -- cold-run dbs carry
real-ish PII and never leave the machine. Interface-lesson
memory saved to auto-memory
(james-interface-product-plus-one-question).

METHOD: hybrid mode s3 tally -- three phases built unattended,
three gates closed on decks, zero kills total. Either the
demo-grade calibration from gate 1 held, or the deck medium
under-surfaces kills relative to hands-on (the intake finding
came from hands, not decks). Walk day discriminates: if P4
surfaces shape problems the decks passed, weight future gate
reviews back toward hands-on.

## 2026-08-04 -- s4: P4 walk day STARTED, PARKED at step 2;
## sheet label drift found and closed

Walk day launched per protocol: walk verifier quoted GREEN first
("17 pass, 0 pending, 0 fail ... verdict GREEN" exit 0), fresh
data/demo-walk-2026-08-04.db served on 8500, sheet handed over.
James completed steps 1-2 (setup, client + matter) and STOPPED at
step 3: the sheet said "set up the firm's two bank accounts" with
no location. He then paused the walk entirely -- "I am so sick of
doing this walkthrough" -- after repeated instruction-quality
friction. WALK PARKED, not failed: db intact through step 2,
verdict sheet blank, no sub-verdict touched.

Root cause found on his "something's wrong with the system" push:
demo-walk-protocol.md was the program's ONLY human-facing artifact
with no oracle. Verifiers check behavior (routes, POSTs, db
state), never the sheet's wording, so drafting drift surfaced
exclusively in James's browser, every time. NOT a folder-structure
problem (his hypothesis, checked and cleared with him).

Fixes, all landed this session:
- Sheet amended twice (recorded in its header, ordered by James
  mid-walk as ratifier): (1) every step now names menu path +
  control; (2) full label audit -- five defects fixed, including
  an invented "choose Bill/Trust Request" control, "Issued date"
  vs the rendered "Issue date", step 6's card title ("Processor
  settlement"), step 10's control ("Save correction", not "Edit")
  plus the unmentioned "Paid" tab. Steps 7-12 brought to uniform
  sub-step grain. Data values and step semantics unchanged; walk
  validity preserved.
- NEW VERIFIER verify/check_sheet_labels.py: every quoted label
  in the sheet's walk steps must exist in the rendering source
  (app_ui/*.py + casework/app/server.py, adjacent f-string
  literals joined). Quoted green: "sheet-label audit: 58 labels
  checked, 0 not found" exit 0. Deliberately a SEPARATE file:
  run_billing_ui_walk.py untouched, so the sealed x2 sha
  a506f085 stands unbroken.
- Feedback memory saved (full-paths-always): file paths absolute,
  instruction steps name menu path + control label, verified
  never guessed. His words: "for like the 10th time."

METHOD: the oracle-first discipline was applied to everything
EXCEPT the artifact facing the ratifier -- and that is exactly
where all the friction accumulated. Human-facing prose needs
oracles too; check_sheet_labels.py is the pattern (extract
claims from prose, assert against source). Candidate for
casework-ui's cold-run sheet when that child resumes.

Resume note (recorder): timing marks were disrupted by the sheet
defects; at resume, treat M0-M6 as N/A-with-cause or restart
fresh -- driver's call at resume, not now. Friction log so far:
(1) step 3 location missing [sheet defect, fixed]; sheet-defect
class now closed by the new verifier.

METHOD (s4, James, mid-park): "its exactly this why AI adoption
is lagging." Generalized finding from the walk-day friction: an
optimizing agent optimizes against the oracles it has; error
mass migrates to unverified seams; the human at the seam becomes
residual QA and experiences only exceptions, so the tool reads
as a net slowdown even with output objectively up. One wrong
label taxes trust in every future claim (multiplicative), so the
human re-verifies everything and the automation dividend erodes.
Implication for the method: every artifact/surface facing the
ratifier gets an oracle, same as code (label audit is the first
instance; demo-login fix queued as the second). Binding
constraint on adoption is verification architecture at the human
seam, not model capability. This program is now deliberately a
testbed for that claim.

## 2026-08-04 -- s4 cont: PAPERCUT LEDGER (James: "death by a
## fucking million papercuts tonight" -- log each one)

Running tally of every friction hit tonight, each with status:

 # | Papercut                          | Status
---+-----------------------------------+---------------------------
 1 | Sheet step 3 named no location    | FIXED -- every step now
   | ("where?"); driver left hunting   | carries menu path +
   | menus mid-walk                    | control label
 2 | File referenced by partial path;  | FIXED -- full-paths rule
   | had to ask for the full one       | (state.md + auto-memory)
 3 | Sheet labels wrong 5 ways         | FIXED -- sheet re-drafted;
   | (invented "choose Bill" control,  | check_sheet_labels.py now
   | "Issued date", wrong card title,  | standing verifier, 58/58
   | "Edit" vs "Save correction",      | green
   | unmentioned "Paid" tab)           |
 4 | Resume died at login wall --      | SPECCED, QUEUED -- demo-
   | forgot a password the sheet       | login prefill + no-expiry
   | invented; MFA ceremony on a       | sessions on synthetic dbs;
   | synthetic db                      | gate decision, awaiting
   |                                   | James
 5 | Half-walked db on resume ("too    | FIXED for tonight -- fresh
   | confusing"); parked state made    | db swapped behind 8500.
   | re-entry cognitively expensive    | FINDING: demo walks should
   |                                   | default to fresh-restart,
   |                                   | not mid-db resume; resume
   |                                   | is agent economy, not
   |                                   | driver economy
 6 | Agent quipped "frictionless"      | NOTED -- interface: no
   | mid-frustration                   | levity while the driver is
   |                                   | eating friction

Papercut 7 (fresh-restart attempt, step 2): sheet gave Vera's
data as a bare slash-tuple "(Vera / Synthetic / email / phone)"
-- no field mapping; "Synthetic" reads as a company name against
a form split into Given name / Family name. FIXED: steps 1-2
rewritten as "Field" = value lines (all labels source-verified,
audit now 70 checked / 0 missing), plus explicit "Synthetic is
her last name, not a company." AUDIT GAP EXPLAINED: the label
audit checks that quoted labels EXIST on screens; data values
were exempt, so a missing value->field mapping was invisible --
absence of a claim can't fail an existence check. New fence
added to check_sheet_labels.py: any slash-separated value tuple
in the walk steps is now a FAIL; values must be pinned to field
labels. Fence is pattern-scoped (catches the tuple form, not
every conceivable unmapped value); full closure would mean
generating the sheet from the same source as the forms --
logged as an option, not built.

Papercut 8 (step 2, restructured sheet): steps were not atomic
-- step 2 spanned two screens (create client AND create matter),
so finishing a screen left the driver expecting the next number
while the sheet still owed work on the old one. James's rule,
now the STEP RULE on the sheet: one step = one screen; "Go:" for
navigation, "Field" = value lines, exactly one "End:" click (or
"Observe:") per step. 12 narrative steps re-based into 32 atomic
steps in parts A-J; timing marks re-pointed. Basis of the old
numbering, honestly: story beats inherited from the machine
verifier's checkpoints, never re-derived when screen-grain
detail arrived -- unit-of-narration vs unit-of-execution
mismatch. Audit extended with an atomicity fence (a step with
two "End:" clicks FAILS); fence immediately caught the STEP
RULE preamble's own notation quotes (exempted as NOTATION) --
the audit now audits the sheet's structure, not just its
labels. Post-restructure: 78 labels checked, 0 not found,
0 fence failures, exit 0.

WALK FINDING F-1 (step 12, James's hands, 2026-08-04): the
invoice detail page fails the demo bar. His words: "this page
has too much ... you feel like you finish an invoice and expect
to add a bill but it just sits right below the invoice like its
not attached or not in that billing family ... This page is a
mess." Diagnosis: the page is MODEL-shaped, not TASK-shaped --
six equal-weight cards (header / Charges + always-open add form
/ Import (empty-state) / Payments (empty-state) / Record a
payment with trust-only fields visible on direct payments /
Client link), everything rendered in every state. This is
interaction parity with Docketwise's defect creeping back in
through "render every table as a card" -- in the exact module
claiming CPA-grade superiority. Also a noun mismatch: screen
says "Invoice #1", pill and sheet say bill.

METHOD: the s3 discriminator FIRED. Gates 1-3 passed this page
in three zero-kill decks; James's hands called it a mess at
first contact. Deck review under-surfaces interaction findings;
weight future gate reviews toward hands-on, as s3 predicted.

## 2026-08-04 -- s4 cont: F-1 REDESIGN BUILT; mini-gate deck
## banked; awaiting James's red-pen

James's ruling on F-1: "Stop the walk and redesign now. When
something's broken you have to fix it." Built same session:

The invoice detail page is now STATE-shaped -- three lives:
building (header + Charges card with the add form, nothing
else); awaiting money (charges table with "Add another charge" /
"Import saved charges and time" folds, then ONE "Collect $X"
card whose paths each show only their own fields: "Record a
direct payment (check, cash, wire)" / "Pay from client trust
(earn-out)" / "Send the client a payment link"; trust requests:
"Send the request to the client" [auto-open until first share] /
"Record the deposit (received directly by the firm)"); paid
(charges + payments history + client link -- no forms). All
disclosure is native <details>/<summary>: zero-JS discipline
holds. Rendering only: same POST routes, frozen casework
modules untouched. Noun unified: pages title Bill #N / Trust
request #N (sheet finding: screen said Invoice, sheet said
bill).

Defects found and fixed DURING the rebuild:
- Shadowing bug (mine): payments-table loop reused `status` for
  its refund pill and clobbered the invoice status after I
  hoisted the computation; pill rendered empty. Renamed to
  refund_pill; caught by the walk verifier's paid assertion.
- Empty-bill "Paid" pill (pre-existing, surfaced by frame 1 of
  the deck): zero balance derives "paid" in the core, so an
  EMPTY bill wore a Paid pill. Rendering fix: no status pill
  until charges exist.

VERIFIER EDITS DISCLOSED (run_billing_ui_walk.py, own coverage;
routes/behavior checks untouched): 3 content assertions track
the redesign -- state A asserts "Charges build the bill" and NO
"<h1>Collect" (was: pay-card empty-state text); post-charge
asserts "<h1>Collect $500.00</h1>" (was: "Record a payment");
trust request state A asserts "Charges build the trust request".

All suites green after rebuild, quoted this session:
billing-ui walk 17/17 x2, timing-stripped sha 485b2463 IDENTICAL
both runs -- SUPERSEDES a506f085 (F-1 redesign is the delta);
ui-walk 13; spine 107; billing 25; fiduciary --seeded 8.
Sheet steps 10-15/21-23 rewritten for the new page; label audit
79 checked / 0 not found, exit 0.

Mini-gate deck (5 frames) banked to
verify/gate-receipts/gate-f1-deck/: bill empty / bill awaiting
(folds closed) / direct fold open / bill paid / trust request.
Gate db data/gate-f1-2026-08-04.db SERVING ON 8500 for James's
own hands (billing.walk@synthetic.test / billing-walk-pass).
GATE OPEN: James red-pens the deck + clicks; PASS -> fresh walk
on the atomic sheet; kills -> iterate (anti-stall: 2 per screen).

GATE F-1 CLOSED (2026-08-04, James): "Designs better" -- PASS,
zero kills on the redesigned page. The F-1 fail axis is cleared
pending the re-walk. Remaining to contract: ONE item -- the
fresh P4 walk on the atomic 32-step sheet, James driving, then
fiduciary on the walked db, eyeball, three-part verdict.

Wind-down at James's request ("park it"): fresh walk queued for
a new session. Gate server left on 8500 (gate-f1 db). state.md
rewritten clean; commit + push ordered by James.

## 2026-08-06 -- s5: pre-walk end-to-end drive of the sheet;
## 9 coupling defects found and fixed; all suites green

James, resuming: "a lot of amendments and a lot of work just to
get to step 12 ... Before I try to start I want to run
end-to-end ... do a full review" -- explicit order to get the
sheet/UI coupling into best shape before his fresh walk.

METHOD: the 08-04 label audit checked labels against SOURCE;
this session drove every one of the 32 steps against the LIVE
screens by script (scratchpad drive_sheet.py; scratch db,
ephemeral ports, 8500 untouched), checking each Go: target,
field, fold (existence AND open state), button, and Observe: on
the page the click actually lands on. That closes the gap the
label oracle cannot see: a label can exist in source yet be
absent (or collapsed) in the STATE the driver reaches --
check_sheet_labels.py greps a corpus of all branches, and
run_billing_ui_walk.py POSTs routes directly, so neither renders
the in-between states James's hands meet. Two prior escapes
(steps 15 and 22 below) were exactly that class.

NINE defects found; steps 1-9, 11-14, 16-21, 24, 26-28, 30-31
verified clean label-for-label. Fixes in three artifacts:

UI (app_ui/billing_ui.py, rendering-only, disclosed -- the F-1
page passed its mini-gate 08-04, so these are post-gate edits):
1. Step 15 walk-killer: "Create client link" reloaded the page
   with the fold holding the new URL COLLAPSED (s4's auto-open-
   until-first-share rule backfired: creating the first share
   closed the fold at the exact moment its content mattered).
   The trust "Send the request to the client" fold is now always
   open while a balance is due; the bill-side "Send the client a
   payment link" fold opens once a share exists.
2. Step 22 walk-killer: an EMPTY bill rendered the import
   checkboxes bare in the Charges card -- the sheet's named fold
   "Import saved charges and time" did not exist in that state
   (it only wrapped the checkboxes once a charge existed). The
   fold now wears the same label in both states.

Sheet (verify/demo-walk-protocol.md, wording re-pinned to what
the screens render; amendment block added; data values, step
semantics, and numbering unchanged):
3. Steps 10/13: "side by side"/LEFT/RIGHT -> the two New-invoice
   cards are STACKED; TOP = "New bill", LOWER = "New trust
   request". (The 08-04 audit had introduced "side by side" from
   source-reading -- .card divs are block elements.)
4. Steps 25/29: "open the 500.00 / 3,000.00 bill" -> paid rows
   all show Balance 0.00, no amount column identifies them; the
   sheet now says open Bill #1 / #3 by the Invoice column. The
   25 tab-click also moved from End: into Go: (STEP RULE: one
   End per screen of work; navigation compresses into Go:).
5. Step 18 Observe pinned to visible numbers: Trust (IOLTA) tile
   $5,000.00, Operating tile $349.70 (150.30 itself renders
   nowhere on that screen; 3% + 0.30 on 5,000.00 verified
   against processor.py).
6. Step 22 Observe: "Charges table now totals 3,000.00" -> the
   table has no totals row; now reads "both rows land ... page
   says Balance due: $3,000.00".
7. Step 23 Observe claimed Vera's remaining 2,000.00 on the bill
   page -- it renders only on Trust accounting; observation
   moved into step 24's pass-through of that screen.
8. Step 32: operating recon card carries no "= client claims"
   leg (no sub-ledger); sheet now says which card shows which
   identity. Plus minor: steps 1/2 name their on-screen
   headings; step 7 notes the prefilled Client box.

Close-out checker (verify/check_demo_walk.py):
9. BUG, would have failed a PERFECT walk at close-out: the
   earn-out receipt keyed the bill on matter_id IS NOT NULL, but
   the sheet's consultation bill ALSO carries the matter (the
   automated walk's doesn't -- the two artifacts diverge there),
   so the query grabbed Bill #1 (1 charge, no trust transfer).
   Now keyed on THE bill paid by trust_transfer. Check labels
   also re-numbered from the dead 12-step narrative to the
   atomic sheet's step ranges. This was state.md's standing
   watch item ("REVIEW IT before the walk") -- confirmed real.

Verified, quoted this session, post-fix:
- drive_sheet.py full 32-step drive: 0 findings.
- check_demo_walk.py on the sheet-driven db: all receipts PASS +
  "fiduciary: 8 pass, 0 red, 0 stub; verdict: GREEN" exit 0 --
  first proof of the checker against a db produced by the SHEET's
  exact data (matter on Bill #1) rather than the verifier's.
- check_sheet_labels.py: "84 labels checked, 0 not found" exit 0.
- run_billing_ui_walk.py: "17 pass, 0 pending, 0 fail;
  float-sweep pass; verdict GREEN" x2, timing-stripped sha
  d7ee3ace IDENTICAL both runs -- SUPERSEDES 485b2463 (delta =
  UI fixes 1-2; strip recipe this session: drop "run started:"
  line, per-step elapsed column, total figure; sha256 first 8).
- ui-walk 13 GREEN; spine 107 green; billing 25 GREEN; fiduciary
  --seeded 8 GREEN.

The fresh P4 walk remains the only contract item and can start
from step 1 on a fresh dated db behind 8500.

## 2026-08-07 -- s5 cont: exploratory notes banked (no build)

PAYMENTS LANDSCAPE (James-directed exploration, web-sourced, for
the strategic flag's file): LawPay powered Clio Payments from
2015; Clio went native 2021-22 and is discontinuing the LawPay
integration entirely end of Aug 2026 (LawSites, 2026-05).
AffiniPay answered by buying distribution: MyCase 2022,
Docketwise 2023, rebrand 8am 2025. Paradigm (PracticePanther/
Bill4Time/MerusCase) bought Headnote 2020 -> PantherPayments.
Independent trust-safe processor: Confido Legal -- which IS
Gravity Legal renamed (Dec 2023, spun out of Gravity Payments;
$9M raise Feb 2026, Aquiline) -- CORRECTION to the 2026-08-01
ledger's candidate list, which named "Confido, Gravity" as two.
Card rails are commodity (Stripe Connect / Adyen / Finix /
Payrix class); the legal product is the wrapper: IOLTA-safe
gross settlement + fee-pull from operating -- exactly the shape
our simulator's adapter models. Business answer to the rake:
deliberately undecided, untriggered.

PROGRAM ORIENTATION (same sitting): corpus totals 242 entries;
built+verified 136 (spine 111 + billing 25) = 56% by count; the
number is true and misleading (entry grain hides the form-library
treadmill, productization mass, and distribution moats). James's
personal gap map written OUTSIDE the program at
C:\Users\james\Desktop\atlas-untouched-map.md (his state file,
not a contract artifact). Payments cleared from working memory
by his ruling; fresh P4 walk remains the only open contract item.

## 2026-08-07 -- s6: walk attempt 2 FAIL; sheet-UI coupling built

ATTEMPT 2 (James driving, fresh data/demo-walk-2026-08-07.db on
8500): stalled at step 12, diverged at step 14, stopped at 17.
Audit-log reconstruction (walked db, read-only): steps 1-11 all
correct. Step 12's payment landed dated 2026-08-07 (the Date
field prefills today; the prefill beat the sheet's typed
2026-08-01). At step 14 the retainer was recorded as a FIRM-SIDE
direct deposit -- the fold the sheet said "do NOT open" -- two
seconds before the client link was created, so the request went
Paid before Vera saw it, processor_transactions stayed empty,
and Part F had nothing to settle. Db unwalkable from step 18;
retained (delete=archive) as the attempt-2 record. James's
verdict on the artifact: driving it was "like taking the CPA
audit test with no background" -- procedures without goals, in
agent vocabulary (card/fold/Collect "button") no screen shows.

FINDINGS (all artifact defects, none driver error):
1. Sheet vocabulary unexplained; no button named Collect exists.
2. No recovery rail: reorienting via the menu (which has no
   active-section marker -- his finding) strands the driver.
3. Date prefills silently beat typed sheet values.
4. Negative instruction lost to a visible prefilled affordance.
5. Steps stated procedures, never goals.
6. (Found by the new drive) an invoice with NO charges derives
   status paid, so a just-created bill is on NEITHER default
   list tab -- the old If-lost route to steps 11/14/22 dead-ends.
   Product observation parked for James: is empty-bill-counts-as-
   paid acceptable list behavior? Sheet routes via All for now.

FIXES (James ratified the gate in-session; edit surfaces: sheet
+ UI both authorized by him verbatim):
- demo-walk-protocol.md AMENDED (6th amendment, recorded in the
  header): vocabulary block (card/fold/tab/tile/crumb line + "no
  Collect button exists"); Goal line under every part; Go: or If
  lost: route on every step, always starting from menu/address
  bar; every date field states its prefill (change it / leave
  it); Part E rewritten positively -- deposit fold never named,
  CHECKPOINT at step 17 stops the walk if the payment method
  reads direct; crumb-line anchors on the create steps; empty-
  state routes via tab All. Steps still 32, data values and
  semantics unchanged, no renumbering.
- UI (rendering-only): html.page() gains active_href; billing
  screens pass /billing -> the top menu underlines Billing on
  every billing screen. Shared-chrome change ratified by James
  in-session; inert for all non-billing callers (default None).
- verify/drive_sheet.py NEW, PERMANENT (the 08-06 drive was
  scratch and evaporated -- lesson recorded): drives all 32
  steps entering EVERY step from scratch via its own sheet
  route (the recovery rail attempt 2 lacked), asserts the
  sheet's quoted labels on the landing pages, locks the
  attempt-2 regressions (prefill claims, request-unpaid-before-
  client-link, checkpoint-17 card-not-direct), and carries a
  SHEET LOCK: sha256 of the walk-sheet section; sheet edits
  without a driver re-sync fail loudly (exit 2).
  First runs caught: my own crumb needle written against
  rendered text not markup; bare #N needles false-matching CSS
  hex colors (#1a1d21); finding 6 above. All fixed, then GREEN.
- verify/report_sha.py NEW: canonical timing-strip sha recipe
  as code. Evidence this session: the s4-COMMITTED walk report
  and today's report strip to the SAME sha under one recipe,
  zero diff -- so the worklog's a506f085 -> 485b2463 -> d7ee3ace
  lineage was RECIPE drift across sessions, not report deltas.
  The walk report content has been stable since the s4 commit.
  Canonical sha of that stable content: a506f085. result.md
  must disclose this reconciliation; prior histories unedited.

VERIFIED, quoted this session, post-fix:
- drive_sheet: 24/24 groups pass; verdict GREEN.
- check_sheet_labels: 82 labels checked, 0 not found.
- run_billing_ui_walk: "17 pass, 0 pending, 0 fail; float-sweep
  pass; verdict GREEN" x2; report_sha.py -> a506f085 both runs.
- ui-walk 13 GREEN; spine 107 GREEN; billing 25 GREEN;
  fiduciary --seeded 8 GREEN.

Session hygiene: dead 8500 server stopped; fresh
data/demo-walk-2026-08-07b.db serving on 8500, /setup confirmed
answering -- attempt 3 starts at sheet step 1. CLAUDE.md "How to
run" corrected: run_billing.py / run_fiduciary.py live in
../casework-billing/verify, not ../casework/verify (verified on
disk today; the old line failed when run).

METHOD: three instances of ONE defect class surfaced today, all
"generated artifact verified against its own assumptions":
(a) the sheet's happy-path drive could not model a human
reorienting mid-walk (deck-vs-hands, one layer deeper: script-
vs-hands); (b) the sha receipts compared incomparable hand-made
normalizations; (c) the agent itself queried guessed table
names mid-investigation (James caught it live). Standing cure
in all three: the procedure becomes versioned code with a loud
failure mode (drive_sheet + sheet lock; report_sha; Evidence
Discipline block added to James's global CLAUDE.md -- read
before assert, ground first, fail loud, no error-tolerant
probing). James's framing worth keeping: agent claims are
management representations; verification is segregation of
duties -- the generator never solely attests its own work.

## 2026-08-07 -- s6 cont: attempt 3 COMPLETE end to end; verdict FAIL

Attempt 3 (fresh demo-walk-2026-08-07c.db behind 8500): James
drove ALL 32 steps -- the first complete James-driven walk.
Deviations en route: an extra empty bill took the #2 slot, so
every downstream invoice number shifted +1 (sheet hardcodes
numbers = new finding; recorder remapped mid-walk at his
request -- assistance disclosed for the verdict); the trust
request issue date, time entry, earn-out and disbursement dates
stayed on today's prefill. Root cause visible in his snaps: date
inputs display/accept US MM/DD/YYYY while the sheet speaks ISO
-- a format conversion at every field. His ruling: COUPLE to
MM/DD/YYYY user-facing, data stays ISO (gated-items queue A).

Close-out quoted: check_demo_walk PASS on the walked db -- all
receipts held THROUGH the number offset (s5's structural keying
paid off: "trust request 3 paid via processor", "bill 4 ...
trust_transfer paid"); "fiduciary: 8 pass, 0 red, 0 stub;
verdict: GREEN" in place; exit 0. Eyeball leg: his 25 labeled
snaps, copied to walk-artifacts/2026-08-07-attempt3/ (standing
home for walk documentation).

VERDICT (James, all three axes): (a) FAIL -- "reconciliation
was not adequate and I think incorrect"; (b) FAIL -- "I'd
apologize for many"; (c) FAIL -- "no chance, this suckers
half-baked not up to my internal standards even." P4 stays
open; iteration ordered. Contract note: the walk MECHANICS now
survive his hands end to end (close-out green); the FAIL is
product quality, which is exactly what the three-axis verdict
exists to measure.

Friction ledger from the snaps: no route back to dashboard
(brand not a link); client pay page bare HTML beside the styled
firm surface (frozen casework -- gated); date format mismatch
(root cause above); inconsistent date defaults (charge dates
copy issue date, payment/time/disburse default today);
"unrecognized duration: '2'" (strict field, good error); blank
select options read as noise; Pay to free text; copy-link
button wanted (zero-JS -> select-on-click box); imported saved
charge shows blank DATE cell; show client trust balance on the
bill/PDF (his 800.00 idea); two snap labels awaiting one-line
clarifications.

BACKLOG AGGREGATED at his order: atlas/gated-items.md -- every
locked/parked item program-wide, plus the break-in method
(F7-amendment precedent formalized: name item, scope-limited
in-session authorization, hard limits restated, all suites
rerun green, canonical shas, worklog carries the incident).
Axis-(a) recon work is ALREADY AUTHORIZED under the 2026-08-04
F7 amendment; blocked only on his specifics (asked, one
question, end of session message).

METHOD: the three-attempt arc is the finding. Attempt 1 died at
step 12 on a model-shaped page; attempt 2 died at 14 on sheet-
reality decoupling; attempt 3 ran 32/32 with a green close-out
after the coupling machinery landed -- and STILL failed the
human verdict on quality. Oracles bound correctness; only the
ratifier's hands bound demo-grade. Both layers are needed;
neither substitutes.

## 2026-08-07 -- s6 cont 2: recon rebuilt vertical (axis-(a) fix 1)

James's diagnosis on the recon screen, confirmed against the
engine in a plain-text CLI walkthrough: (1) no visible bank
side -- the statement never appeared as its own artifact, so the
rec read as books reconciling to themselves; (2) horizontal
identity sentence where a CPA reads vertical footing columns;
(3) unsigned amounts -- the items column footed to nothing; (4)
the 500.00 "check" he never wrote = the correction machinery's
fabricated compensating bank events (s2 fix's trade-off),
surfaced to him for a held decision.

REBUILD (F7-authorized, rendering-only, billing_ui.py): the
recon card is now three vertical panes per account -- Bank
statement (independent; cleared lines, then in-transit /
outstanding items, footing Statement balance -> Adjusted bank),
Books (posted entries, system corrections labeled, footing
Books balance), Client claims (trust only, footing total) --
with parenthesized outflows, a tie line (adjusted bank = books
= client claims), and an error box enumerating any unmatched
lines/postings. bank_statement.py now imported by the renderer
(same witness the engine reads; never the journal). Sheet step
32 re-pinned to the new screen (amendment recorded); drive s32
STRENGTHENED: asserts all three pane titles, all four foot
labels, the (system correction) tag, Adjusted bank on BOTH
cards, claims column on the trust card only.

Quoted green after rebuild: drive-sheet 24/24; labels 82/0;
billing-ui walk 17/17 x2 report_sha a506f085; ui-walk 13; spine
107; billing 25; fiduciary --seeded 8. Server on 8500 restarted
over the WALKED db (demo-walk-2026-08-07c) so James eyeballs
the new screen on his own books.

HELD DECISIONS (gated-items updated): fabricated correction
events vs real-bank-matching engine (his call after eyeball);
period-end placement so statements show a cleared/pending mix.

## 2026-08-07 -- s6 wind-down

James's eyeball on the rebuilt recon: "solid for where we are
at" -- axis-(a) presentation accepted for this stage; the two
engine-level decisions stay held on gated-items item 1. Session
closed with commit + push (this commit carries s5's uncommitted
pre-walk fixes AND all of s6: coupling machinery, attempt-3
walk artifacts, verdict record, recon rebuild, gated-items.md,
Evidence Discipline incident). Server left on 8500 over the
walked attempt-3 db. state.md is the resume authority.

## 2026-08-07 -- s7: gated item A -- date coupling (MM/DD/YYYY)

James's order: work the unlocked queue top-down, A first. Root
cause of 4 of attempt 3's 5 date misses: US-locale date inputs
DISPLAY MM/DD/YYYY while the sheet typed ISO values, and every
rendered date on the billing screens was raw ISO from the db.

FIX (three coupled layers, data stays ISO end to end):
1. billing_ui.py: fmt_date() -- strict presentation formatter
   (ISO in, MM/DD/YYYY out; anything else raises -- fail loud,
   same boundary as fmt_cents). Applied at all 17 user-facing
   render sites: invoice list Issued; invoice detail Issued/Due
   kv, charge rows, payment links, time-entry import labels;
   account ledger dates; journal detail Posted kv + bank
   record; recon period hint, statement lines, reconciling
   items, book postings; time index; payment detail Date kv,
   journal trail, bank record. Date INPUT value attributes stay
   ISO (HTML spec; the browser localizes the widget).
2. demo-walk-protocol.md: every typed and named date in the
   walk sheet re-expressed MM/DD/YYYY (13 substitutions, same
   calendar days, no step semantics changed); preamble states
   the convention; amendment header recorded. One ruling-date
   citation in the STEP RULE preamble also re-expressed so the
   invariant is absolute: ZERO ISO dates in the sha-locked
   sheet section.
3. drive_sheet.py asserts the claim both ways: the lock check
   scans the sheet section for ISO strays (exit 2), and a
   DateScanBrowser scans EVERY billing page the drive fetches
   for visible ISO dates (value attributes exempt). Step pins
   updated (payment-date links 08/01/2026 -> 08/02/2026 after
   correction; s22 asserts the 08/02/2026 time-entry label).
   POST constants stay ISO -- documented as what a browser
   submits from a date input, not what the driver types.
   run_billing_ui_walk.py's two rendered-ISO pins re-pinned to
   08/01/2026. SHEET LOCK re-synced deliberately:
   308332708dd1 -> 847e4aaf2364 after step-by-step verify.

Quoted green after fix: drive-sheet 24/24 (date scanner live on
every fetch); billing-ui walk 17/17 x2 report_sha a506f085
(report content unchanged -- step details carry no dates);
labels 82/0; ui-walk 13; spine 107; billing 25; fiduciary
--seeded 8. Server on 8500 restarted over demo-walk-2026-08-07c
so the walked books now render MM/DD/YYYY.

FLAGGED, not fixed (frozen core, out of item-A scope): the
invoice PDF (casework/app/billing.py) still prints ISO dates --
a bill page reading 08/02/2026 hands James a PDF reading
2026-08-02. Queued as a note under gated-items item 2's class
(core rendering); his call whether it rides the pay-page
break-in. The client pay page renders no dates (checked).

## 2026-08-07 -- s7 cont: BREAK-IN -- invoice PDF (frozen core)

AUTHORIZATION (James, in-session, the gated-items method, F7
precedent): "make a special edit to fix the invoice or an
alignment... I'm giving you permission... make sure you record
it." Named scope: casework/app/billing.py, invoice_pdf function
ONLY, presentation semantics only. Hard limits restated in the
authorization reply: spine + anchor suites immutable and rerun
green; PDF assertions strengthen never weaken; contracts
untouched; all standing suites quoted; supersessions via
canonical sha scripts only.

DEFECTS (ground-read before the cut): (1) header dates printed
raw ISO (the item-A residue flagged same session); (2) charge
lines were description and amount jammed inline with two
spaces -- no columns, no charge date, nothing footed: the
"alignment"; (3) amount_cents / 100 -- FLOAT division touching
money at the presentation boundary, against the program's own
integer-cents rule (the suites' float-sweep greps float() and
REAL columns, so /100 sailed under it).

FIX (presentation only, no schema, no data change): _pdf_date
(strict ISO -> MM/DD/YYYY, fails loud) and _pdf_cents (divmod
integer math, parenthesized negatives); header Issued/Due
through _pdf_date; charges as a Description | Date | Amount
table -- header row underlined, amounts right-aligned, Balance
Due right-aligned over a top rule, single cell so the
"Balance Due: 0.00" assertion string stays contiguous in
extraction. Column chrome reuses existing fx-0052 translated
strings (en+es both carry description/date/amount) -- no new
untranslated labels. Discount rides the amount column.
Rendered Bill-from-07c PDF eyeballed in-session: columns foot,
dates MM/DD/YYYY.

Quoted green after the cut: spine verdict GREEN (exit 0 in
chain); anchor-billing PASS (1.253s) -- the suite that reads
the PDF back; billing 25 green, checks pass; fiduciary
--seeded 8 pass; ui-walk 13 pass GREEN; billing-ui walk 17
pass GREEN x2; drive-sheet 24/24 GREEN; labels 82/0.
SUPERSESSION: billing-ui walk-report sha a506f085 ->
de589cbd (the report's PDF byte count changed 1159 -> 1401;
content-honest change), stable across both runs, quoted from
report_sha.py only. Server on 8500 restarted so Download PDF
serves the new layout on the walked db.

Note for James's eyeball: on the 07c books invoice #3 is the
TRUST REQUEST (his mid-walk extra invoice shifted numbers) --
the number-shift gated item B exists to kill.

## 2026-08-07 -- s7 cont 2: billing landing cleanup (James's snap)

His snap of the landing on the walked db: the Outstanding tile
said 0 open invoices while the list below (Outstanding tab,
empty, all four invoices paid) showed the blank-database copy
"No invoices here yet" -- one screen, two contradictory claims.
Second finding on the same snap: the selected tab and the New
invoice action rendered as near-identical filled chips, two
rows of same-looking controls. James: fix everything in the
snap, full cleanup where it makes sense.

FIX (rendering-only, billing_ui.py, unlocked surface):
1. Tab-aware empty states: blank-db copy only when NO invoices
   exist; empty Outstanding now reads "Nothing outstanding --
   every invoice is collected. The Paid tab has the full
   record."; empty Paid reads "Nothing collected yet -- every
   invoice is still outstanding."
2. Tabs carry live counts -- Outstanding (0) | Paid (4) |
   All (4) -- so an empty tab names where the invoices are.
   One status query per invoice, reused for tile + tabs +
   filter (status_of map).
3. Tabs restyled as underline tabs (selected: bold, dark,
   2px underline on a hairline rule), visually distinct from
   the filled action buttons. Sheet's TAB vocabulary
   ("highlighted one is selected") still holds; no sheet edit,
   no sha re-sync.
drive_sheet waypoint needle re-pinned ">Paid<" -> ">Paid ("
(label-plus-count prefix, tally-proof).

Quoted green: billing-ui walk 17 pass GREEN x2, report_sha
de589cbd both runs (unchanged -- the report carries no tab
markup); drive-sheet 24/24 GREEN; labels 82/0; ui-walk 13
GREEN. Server on 8500 restarted over the walked db.

## 2026-08-07 -- s7 cont 3: Back to billing button (James's snaps)

His ask, from the trust-accounting snap: the crumbs and the top
menu work, but the four billing sub-areas (Trust accounting,
Time, Saved charges, Reconciliation) need a big obvious
"Back to billing" button up top.

FIX (rendering-only, billing_ui.py): _back_to_billing() -- a
quiet-styled button floated top-right in each screen's action
row (rows created on Saved charges and Reconciliation, which
had none; both recon branches covered). Quiet style + right
float so it never competes with the screen's primary action.
BILLING_STYLE gains .actions{overflow:auto} and .actions
a.back{float:right} -- billing-only override, shared html.py
untouched. drive_sheet STRENGTHENED: "Back to billing" pinned
on trust accounting (s18), saved charges (s20), and recon
(s32); the Time index renders it via the same helper.

Quoted green: drive-sheet 24/24 GREEN; billing-ui walk 17
pass 0 FAIL x2, report_sha de589cbd both; labels 82/0;
ui-walk 13 GREEN. Server on 8500 restarted over the walked db.

## 2026-08-07 -- s7 cont 4: gated item B + invoice-code design

DESIGN (ratified in conversation, recorded in invoice-codes.md,
gated as item 10): invoice display codes B0001/T0001 -- type
letter + 4-digit zero-padded per-type series, scope follows the
active numbering mode, stored at creation, immutable. Ruled OUT
of the code, with James driving the reasoning: client (implicit
in the stored number's scope; initials collide; attribute not
identity), date (dates are CORRECTABLE in this system -- Part I
is the proof -- and identifiers may not embed correctable
facts), hyphen (unquoted-context arithmetic hazard; B0001 is
one double-clickable token; leading zeros also kill the Excel
cell-reference collision unpadded B1 would have). His spread-
sheet concern resolved by the join key: internal id + the CSV
export columns carry every analysis dimension; the code stays
dumb. Constraint found first by ground-read: the stored number
is corpus-pinned (global-invoice-numbering, confirmed) with an
immutable billing-suite test -- codes must be ADDITIVE. Build
is a core break-in awaiting its own gate.

ITEM B LANDED (sheet + driver, no product change): the sheet
never identifies an invoice by absolute number. Preamble rule
(INVOICE NUMBERS block); steps 10-29 re-worded to TYPE + issue
date (the consult bill = Bill row issued 08/01/2026; the trust
request = the Trust Request row; the work bill = Bill row
issued 08/02/2026); crumb checks pin the prefix Billing / Bill
#<n> with "any number is correct there" said outright.
drive_sheet: invoice_row()/enter_invoice() locate rows exactly
the sheet's way and cross-check against the created ids; crumb
asserts prefix-only; and a STRAY INVOICE is permanently
injected after step 21 -- attempt 3's exact failure condition
-- which every later route must survive. Sheet lock re-synced
deliberately: 847e4aaf2364 -> efea8538b68e.

Quoted green: drive-sheet 24/24 GREEN (stray live); labels
82/0; billing-ui walk 17 pass GREEN, report_sha de589cbd
(unchanged -- no app change this round); ui-walk 13 GREEN.
No server restart needed.

## 2026-08-07 -- s7 cont 5: gated item C -- imported saved charge date

Root cause (ground-read): billing.import_saved_charges calls
add_charge without charge_date (NULL -> blank cell); time
imports pass the entry's date, which is why the time row was
dated and the saved charge was not.

FIX -- existing core APIs only, zero core change: the import
returns the new charge ids; the UI handler (invoice_import,
billing_ui.py) now dates each one via billing.update_charge
with the bill's issue date -- the SAME default the manual Add
form prefills (judgment call, flagged: imported saved charges
inherit the bill's issue date; James can re-rule if service
date should differ). drive_sheet s22 STRENGTHENED: asserts the
imported saved charge's full row renders description | type |
08/02/2026 -- a blank Date cell is now a driver FAIL.

Quoted green: drive-sheet 24/24 GREEN; billing-ui walk 17 pass
GREEN x2; labels 82/0; ui-walk 13 GREEN. SUPERSESSION:
report_sha d9074178 (was de589cbd) -- the work bill's PDF grew
1401 -> 1406 bytes carrying the new date cell; stable x2.
Server on 8500 restarted.

## 2026-08-07 -- s7 cont 6: gated item D -- bare-number time entry

Core parse_duration is corpus-pinned (fx-0064 formats: 2h, 36m,
2.8h, 5.5m) -- so the fix is UI-side normalization at the same
boundary cents_of holds for amounts: in time_create, a bare
number ("2", "1.5") becomes hours ("2h", "1.5h") before the
core parser; everything else passes verbatim so the core's own
error stays the teacher. Form hint now says a bare number means
hours. run_billing_ui_walk STRENGTHENED: posts a bare "2" at
100.00/h and asserts the 200.00 entry lands.

Quoted green: billing-ui walk 17 pass GREEN x2, report_sha
superseded c4555b15 (step detail line changed; stable x2);
drive-sheet 24/24 GREEN; labels 82/0; ui-walk 13 GREEN.

## 2026-08-07 -- s7 cont 7: gated item E -- blank select options

The seven dash-noise blank options across billing selects now
say what leaving the field means (agent wording, FLAGGED for
James's re-rule): time Client "No client (use the matter
below)"; time Matter "No matter"; bill Matter "No matter (bill
the client directly)"; trust Matter "Client-level funds (no
specific matter)"; disburse client "No client (pick a matter
below)"; disburse matter "No matter (funds are client-level)";
payment-edit charge "The whole invoice". Sheet lines quoting
the old options re-pinned (steps 13/19/24, sixth-amendment
header); driver needles re-pinned; SHEET LOCK re-synced
efea8538b68e -> 39f124b41e01.

Quoted green: drive-sheet 24/24 GREEN; labels 82/0; billing-ui
walk 17 pass GREEN x2 report_sha c4555b15 (unchanged); ui-walk
13 GREEN.

## 2026-08-07 -- s7 cont 8: gated items F + G

F (Pay to known payees): reads.known_counterparties() (distinct
external_events counterparties, SELECT-only) feeds a native
<datalist> on the disburse form -- known payees suggest as you
type, free entry stays. Zero JS.

G (client link copy box): the share link renders in a readonly
<input class='copylink'> -- click, Ctrl+A, Ctrl+C grabs the
whole link; the zero-JS stand-in for the requested copy button.
Sheet step 15 now teaches the box (seventh-amendment note
below); SHEET LOCK re-synced 39f124b41e01 -> 2c9cac5141af.
drive s15 STRENGTHENED: asserts the copylink box.

Quoted green: drive-sheet 24/24 GREEN; labels 82/0; billing-ui
walk 17 pass GREEN x2 report_sha c4555b15 (unchanged); ui-walk
13 GREEN.

## 2026-08-07 -- s7 cont 9: gated item H -- trust balance on the bill

BREAK-IN (item H's own wording names the PDF; protocol
followed): casework/app/billing.py, invoice_pdf + the
INVOICE_STRINGS chrome table only, presentation additions --
"Client funds held in trust: <sum>" under Balance Due, chrome
key added in BOTH languages (fx-0052 discipline), rendered only
when the client has trust sub-ledgers. Bill page (rendering):
same figure as a kv line via reads.trust_sub_accounts_of_
contact (SELECT-only; balances summed through
ledger.account_balance so money math stays in the core).

INCIDENT (Evidence Discipline, recorded honestly): the first
cut guessed the matter-ownership column as m.contact_id; the
schema's column is primary_contact_id. anchor-billing FAILED
LOUD (OperationalError) and billing dropped 3 entries red; one
ground-read of schema.sql fixed both queries. The suites did
exactly what fail-loud machinery is for; the lesson (ground
first, also for column names) was already the s6 METHOD note --
this is a repeat offense logged against it.

STRENGTHENED: run_billing_ui_walk asserts "Client funds held in
trust: 800.00" in the extracted PDF text; drive s29 pins
"Client funds in trust" + 800.00 on the work bill's page.

Quoted green after fix: spine 107; billing 25 GREEN; fiduciary
--seeded 8; anchor-billing PASS; drive-sheet 24/24 GREEN;
billing-ui walk 17 GREEN x2; labels 82/0; ui-walk 13 GREEN.
SUPERSESSION: report_sha c4555b15 -> f3f16120 (PDF grew with
the trust line), stable x2. Server on 8500 restarted with the
full E-H batch.

## 2026-08-07 -- s7 cont 10: item I closed; unlocked queue DONE

James ruled both snap labels: (1) "difference in paid versus
recorded" was his double-check note, not a defect; (2)
"Collect card already exists" was the sheet's number-pinned
row-#2 route landing him on the wrong invoice after his +1
offset -- the defect item B's type+date routing already
killed, confirmed against the snap (it photographs the sheet's
step 14, and "recall its Trust 3 since I made 2 invoices" sits
beside it).

THE UNLOCKED QUEUE A-I IS CLOSED, one session. Remaining on
gated-items: the locked list (client pay page styling first,
his axis-(b) driver; held recon pair; invoice codes item 10)
and then attempt 4.

## 2026-08-07 -- s8: client pay page amendment ratified + built

Scope talk first: James brainstormed the CLIENT-PORTAL view
(payment history, bill browsing, export, trust statement,
retainer replenishment). Ruled: go NARROW now; portal logged as
gated item 11 (access-model blocker named: clients exist only
per-invoice via share tokens; a portal is new access-control
logic in the frozen core, likely its own child).

AMENDMENT ratified (program ruling 2026-08-07, text in
atlas/CLAUDE.md): casework/app/server.py's shared-invoice
surface (view/pay/receipt) opened to billing-ui sessions,
RENDERING-ONLY. Gated item 2 marked unlocked.

Built, all in casework/app/server.py:
- CLIENT_STYLE chrome mirroring app_ui's stylesheet (duplicated
  by design -- the core cannot import app_ui); firm-branded
  header via firm.name setting (default SYNTH Firm).
- _invoice_get: footed Description|Date|Amount table, MM/DD/
  YYYY via billing._pdf_date, integer cents via
  billing._pdf_cents (BOTH /100 float divisions gone -- the
  lines ~145/163 defect); kv block (client, issued, due);
  trust-held line, same reader as invoice_pdf (item H); Paid
  pill at zero balance; payments table on the page; styled pay
  form -- pinned labels byte-identical; footer + es strings
  carried (new chrome labels in CLIENT_STRINGS en/es).
- _invoice_pay: declined page styled (Declined: prefix kept);
  receipt page with invoice #, date, method, amount, reference
  (processor txn id), remaining balance, link back.

JUDGMENT CALLS, flagged:
1. conn.commit() ADDED after pay_online -- every sibling POST
   handler commits; this one never did (payment sat uncommitted
   on the shared connection until a firm-side action committed
   it). Persistence fix, arguably a hair past rendering-only;
   James may strike it.
2. Pay-form labels stay English-only on es invoices (pinned
   demo machinery); new receipt/payments chrome IS bilingual.
3. Trust-held line added to the client page (not explicitly in
   the amendment list; same class as item H, same reader as
   the PDF).
4. Receipt reference renders the processor txn id (integer).

Verifier STRENGTHENED (drive_sheet.py s16): client page pins
firm brand, retainer line, footed total, no-trust-line-before-
funds; receipt pins amount/method/Reference/Remaining balance;
client fetches ISO-scanned (_client_no_iso); post-pay re-fetch
pins Payments + Paid pill.

METHOD: Grep output rendered the scan guard as "\billing",
which reads as a dead backspace escape; Read showed the file
truly says "/billing". Tool-display output is not file ground
truth -- ground a defect claim in Read before acting. (No fix
was needed; retracted before touching the file.)

Suites at close, all run this session: spine 107 green;
billing 25 GREEN; fiduciary --seeded 8 GREEN; anchor-billing
PASS; ui-walk 13 GREEN; billing-ui-walk 17 GREEN; drive-sheet
24/24 GREEN (strengthened s16 included); labels 82/0.
report_sha: f3f16120 -- UNCHANGED, no supersession (walk
report byte-identical; client surface is outside it).

Server restarted on the walked 07c db (stale-module rule);
8500 firm / 8501 client both answering. Live spot-check of
/invoice/SYNTH-INV-3-1: SYNTH Firm brand, Trust Request #3,
Paid pill, 5,000.00 charge + payment, trust held 800.00.

## 2026-08-07 -- s8 cont: two snaps -- trust relabel; codes absent

Snaps archived to walk-artifacts/2026-08-07-s8-snaps/ ("no
clean version of our bill number here ex 000B1", "relabel -
client funds in trust").

1. RELABEL, James's order: "Client funds in trust" -> "Remaining
   in Trust". Applied to the staff bill page (billing_ui.py kv),
   the client page + PDF (billing.py INVOICE_STRINGS trust_held;
   es -> "Restante en fideicomiso"). Core touch authorized by
   the order itself, same item-H presentation class. The Trust
   accounting OVERVIEW tile "Client funds in trust" was left --
   it is the firm-wide IOLTA client-money total, not a per-
   client remainder; flagged for his re-rule if he wants one
   word across both. Verifier pins updated to the new label
   (run_billing_ui_walk PDF assert; drive_sheet s29 + s16
   negative). Sheet quotes the label nowhere -- no re-sync.
2. Bill display codes: his snap is correct -- NO B0001/T0001
   renders anywhere. That is by design: the format is ratified
   (invoice-codes.md) but the BUILD is gated item 10 (schema
   column + per-type counter, core break-in, walk-db migration
   story). Raised to him as the turn's question.

Suites after the relabel, all rerun: spine 107 green; billing
25 GREEN; fiduciary 8 GREEN; anchor-billing PASS; ui-walk 13
GREEN; billing-ui-walk 17 GREEN; drive-sheet 24/24 GREEN;
labels 82/0. report_sha: c61ea17a SUPERSEDES f3f16120 (the
walk report's PDF-assert line carries the new label). Server
restarted; live client page shows "Remaining in Trust".

## 2026-08-07 -- s8 cont 2: gated item 10 BUILT -- invoice codes

James authorized in-session ("Yes, please add codes"). Spec
followed without deviation: invoice-codes.md.

Core (casework/app):
- gen_schema.py: invoices gains display_code (GLOB-checked
  [BT] + 4 digits, growable) and code_scope (client/global);
  schema.sql + audit triggers regenerated, never hand-edited.
- billing.py: _next_code beside _next_number -- same scope
  logic, per-TYPE gapless series, global flip continues from
  per-type firm totals via billing.code_global_next.<B|T>
  (fx-0076 mirror); create_invoice stamps both columns.
  Smoke-proved in-memory: B0001/T0001/B0002 per client;
  second client starts its own B0001; global flip -> B0004/
  T0002, nothing renumbered.
- Renders swapped to the code as identity: PDF header, share/
  reminder/receipt/installment emails, zip entry names,
  invoices CSV (new display_code column; suite checks width,
  not names). Client page title + receipt line (server.py).

app_ui: list INVOICE column, page title (and crumb via it),
payment-page kv + crumb, PDF download filename; reads.py
invoice_rows selects the column. JUDGMENT CALL flagged: the
corpus-pinned stored number stays human-visible as a "Number
#n (scope)" kv row on the invoice page -- identity is the
code, the number is an attribute.

Sheet (sixth amendment, in-file history): INVOICE NUMBERS
preamble -> INVOICE CODES; steps 10-29 name B0001/T0001/B0002;
crumb examples exact. INCIDENT, caught by the drive: I wrote
"Trust Request T0001" in the sheet's step-13 crumb; the screen
noun is "Trust request" (lowercase r) -- drive FAILED 23/24,
sheet corrected to match the screen. Product casing is
inconsistent (TYPE pill "Trust Request" vs noun "Trust
request"); left as-is, one more E-class wording for James.
Sheet lock re-synced 2c9cac5141af -> 6032f70b79ca ->
73240eb76cc7 (the middle sha lived only between the two edits).

drive_sheet.py: ROW_RE reads the code link, invoice_row/
enter_invoice locate BY CODE (type+date locate superseded),
crumb pins EXACT codes, stray-invoice regression retained --
the codes shrug it off, which is the whole point.

Migration: verify/migrate_invoice_codes.py (fail-loud: refuses
a coded db, resumes a torn run assert-matching replayed codes;
opens via casework db.connect -- first cut used raw sqlite3 and
the audit triggers failed LOUD on the missing actor functions).
Walked 07c db migrated: 4 invoices, 2 series, verified gapless
(B0001/B0002/T0001/B0003 in creation order). Other retained
walk dbs deliberately NOT migrated (delete=archive; migrate
before ever serving one).

Suites at close, all rerun this session: spine 107 green;
billing 25 GREEN; fiduciary --seeded 8 GREEN; anchor-billing
PASS; ui-walk 13 GREEN; billing-ui-walk 17 GREEN; drive-sheet
24/24 GREEN; labels 82/0. report_sha: 301b574d SUPERSEDES
c61ea17a. Server restarted on the migrated 07c db; live client
page renders "Trust Request T0001".

## 2026-08-07 -- s8 close: codes approved; RECON RULING; clear

James on the s8 batch (codes, relabel, client page): "That all
looks good." His eyeball closes the item-10 presentation.

RULING (James, closing gated item 1's held sub-decision): "Yes
we need to do the engine work." REAL-BANK MATCHING replaces
the synchronized-bank shortcut. Meaning, for the next session:

- Corrections/refunds touch BOOKS ONLY (reversal + repost).
  _append_mirror_events dies: the bank record keeps exactly
  what the bank saw, corrections never fabricate bank events.
- The recon engine (casework-billing/verify: bank_statement.py,
  reconcile.py) matches statement lines to book entries and
  explains differences as reconciling items (outstanding /
  in-transit / timing), instead of relying on mirrored events
  keeping both sides trivially equal.
- Fiduciary F7 scenarios rewritten to assert the REAL model --
  this STRENGTHENS the checks (per the F7 amendment's only
  allowed direction). Note: the 2026-08-04 F7 amendment's
  mirror-event design is superseded BY JAMES'S RULING; the
  amendment's authorization (files, limits) still governs.
- Then demo period-end placement (sub-decision ii, now plain
  build work): statement cut so the walk shows cleared items
  plus an in-transit deposit and an outstanding check.
- Then attempt 4.

All work is pre-authorized (F7 amendment 2026-08-04); no gate
stands between here and attempt 4 except his walk verdict.
Session cleared for context immediately after this entry;
state.md is the cold-start authority.

## 2026-08-07 -- s9: the banking engine (real-bank matching built)

James's ruled task from s8 close, executed end to end. The
mirror-event shortcut is dead; the reconciliation now earns its
HOLDS.

CORE (F7 amendment scope, casework/app):
- _append_mirror_events and _payment_event_specs DELETED from
  billing.py. edit_payment and refund_payment touch books only.
- ledger.py recipes (record_trust_deposit, earn_out,
  record_bill_direct_payment) gained witness_bank=True; a
  correction repost passes False and posts NO bank event. The
  bank record now holds exactly what the bank saw, forever.

ENGINE (casework-billing/verify):
- bank_statement.py lines/pending now carry invoice_id and
  payment_id (matching linkage; still event-derived only).
- reconcile.py rebuilt as a staged matcher: (A) entry linkage
  n:1 groups (settlement batches, unchanged rule), (B) exact
  date+direction+amount with payment-linked-then-original
  preference, (C) pending events -> timing items, (D) payment-
  family deltas -- remaining book net vs bank net per payment
  (a reversal joins its reversed entry's family; lineage chains
  collapse), explained as "correction awaiting bank" (repost
  present) or "refund awaiting bank" (payment reversal alone).
  A family netting zero (the walk's date-only edit) matches
  CLEAN -- no noise item. Every item carries cause, direction,
  amount, date, entry. Anything unexplained still BREAKS the
  identity: bank + in-items - out-items = book = claims.
- check_f7 STRENGTHENED (the amendment's only allowed
  direction): (a) identity at both periods; (b) closed cause
  vocabulary + direction on every item; (c) at the all-cleared
  period timing items must have resolved -- only books-only
  correction/refund items may persist; (d) BANK-RECORD PURITY:
  events linked to a payment must be exactly its birth shape
  (direct 1, trust_transfer 2, sim 0) -- a fabricated or
  destroyed bank event is RED regardless of the identity.

RENDERING (authorized: recon + payment page):
- recon items sign by the engine's direction field (the old
  cause-string guess broke on new causes); correction causes
  render verbatim in the bridge.
- payment-page Bank record hint rewritten: "The bank record
  keeps exactly what the bank saw. Corrections live in the
  books; the reconciliation explains any difference."

PERIOD-END PLACEMENT (sub-decision ii): the sheet's step 24
disbursement now rides the form's today prefill (was a typed
08/04/2026 that has since CLEARED -- the outstanding check
would have vanished from the demo). At the default period (max
event date = run date) the SYNTH IOLTA statement shows the
ruled mix on ANY run date: cleared earn-out check, settlement
deposit in transit (clears tomorrow), disbursement check
outstanding. Sheet steps 24/28/32 re-worded (28: bank shows
what it saw; 32: names the mix); drive s24 posts today(), s32
ASSERTS the mix (no empty statement pane, in-transit 5,000.00,
outstanding (1,200.00)). Seventh sheet amendment: sheet-lock
re-synced 73240eb76cc7 -> f7f821edb1e9.

SUITES (all run this session, quoted):
- fiduciary --selftest: "calibration scenarios: all behaved";
  --seeded x2: "8 pass, 0 red, 0 stub; verdict: GREEN", sha
  e6c64593 x2 (SUPERSEDES fb5bccda; recorded in
  casework-billing/state.md). F7 line now: "2 accounts x 2
  periods, 7 reconciling items enumerated, 0 identity breaks;
  strengthened: 0 unknown-cause items, 0 timing items surviving
  all-cleared, 0 payments with fabricated/missing bank events".
  Item arithmetic foots: mid-lag 5 (fee outstanding, correction
  in 150, refund out 300, 2x settlement in transit) +
  all-cleared 2 (the books-only pair persists, by design).
- billing parity x2: "25 green, 0 red" GREEN, sha c53f262b x2
  (supersedes acba95b1; drift is s8's display_code CSV column,
  not this session).
- anchor-billing: PASS 1.250s, recon HOLDS both banks x 2
  periods.
- spine: "107 green, 0 red, 0 pending; checks pass".
- billing-ui walk x2: "17 pass, 0 pending, 0 fail; float-sweep
  pass; verdict GREEN"; report_sha.py = 301b574d UNCHANGED (the
  walk verifier's own output is untouched by the engine).
- drive_sheet: "24/24 groups pass; verdict GREEN" including the
  strengthened s32 mix assertions.
- check_sheet_labels: "82 labels checked, 0 not found".
- ui-walk: "13 pass, 0 pending, 0 fail; sweeps pass; GREEN".

Server RESTARTED on 8500/8501 (new core code), walked 07c db
still behind the port; 8500 answers 303 (login), client link
SYNTH-INV-3-1 answers 200. Note: 07c predates the engine (its
mirror events remain on that db's bank record); the new matcher
still reconciles it HOLDS because mirrors mirror the books.
Attempt 4 runs on a FRESH db and will carry the pure model.

METHOD: the ruled scope note in state.md survived /clear intact
-- a one-line "banking engine" prompt cold-started straight
into build with zero re-litigating. The state-file contract is
doing its job at program scale.

Next: attempt 4 -- fresh db, code-routed sheet, his verdict.
No gate stands before it.

## 2026-08-08 -- s10: ATTEMPT 4 RUN (James driving); verdict
## FAIL b/c, (a) PASS -- the failure moved up a layer

Pre-flight per protocol setup rules (all agent-executed):
- No server was listening (machine restarted since s9); launched
  serve.py fresh -> data/demo-walk-2026-08-08.db created, PID
  71992 on 8500 + 8501, / answers 303 -> /setup (fresh-db shape
  confirmed by probe). First db carrying the pure s9 bank model.
- Oracles quoted GREEN before handover: billing-ui walk "17 pass,
  0 pending, 0 fail; float-sweep pass; verdict GREEN";
  drive_sheet "24/24 groups pass; verdict GREEN".
- Incident (minor, logged for evidence discipline): agent ran
  seed_demo.py with --help expecting usage; the script takes no
  args and re-seeded data/demo-billing.db (generated file,
  regenerated -- harmless; fiduciary on it quoted GREEN in the
  same output).

THE WALK: James drove all 32 steps solo, 05:44 -> 06:07 local,
recording 48 step-named snaps instead of chat marks. Snaps moved
from Desktop/snaps to walk-artifacts/2026-08-08-attempt4/ (his
order; snaps folder emptied). Marks derived from snap mtimes:
M0 05:44:02, M1 05:44:28, M2 05:53:52, M3 05:55:05, M4 05:59:23,
M5 06:04:46, M6 06:07:47; elapsed M1->M6 23:19 vs 20:00 soft
budget (friction entry, not a fail). One friction note rode a
snap filename: step-29 ledger links under the dollar tiles are
low-visibility, "always miss them".

CLOSE-OUT (untimed): check_demo_walk.py on the walked db -- all
12 receipt lines PASS (accounts, client+matter, consult paid,
retainer via processor, settlement 500000/15030c, time entry
7200s@25000c, bill 3 earn-out, disbursement SYNTH-USCIS 120000c,
client funds 80000c, correction trail 1 reversal + 1 repost,
audit actors, fiduciary in place "8 pass, 0 red, 0 stub; verdict:
GREEN"); "check-demo-walk: PASS"; EXIT CODE: 0. Step-32 snap
shows both accounts HOLDS, every reconciling item caused,
adjusted bank = books = claims 800.00 footed on screen.

VERDICT (James, sealed in walk-artifacts/2026-08-08-attempt4/
verdict.md): (a) PASS -- "I think it's just the product around
it"; the ledger / correction trail / recon trio made the case,
recon traversed "easily". (b) FAIL -- "it's not beautiful".
(c) FAIL -- "I'd be hesitant to show a demo". Overall FAIL b/c.
The attempt-3 axes HELD: reconciliation correctness (s9 engine)
and the s7/s8 polish batch survived his eyes.

THE NAMED DEFECT (new class -- information architecture, not
polish, not correctness): no overall status surface and no
visible flow. His specifics, quoted in the friction log: no
project / client / matter / billing summary layer ("I don't feel
like I have an overall status"); hidden state must be brought
forward so the user can follow the order (add client -> matter
-> bill -> which type / which account -> collect vs disburse);
"The UI does not bring out the structure of the actual code in
a way that the user can logically follow and reinforce a
narrative." Recorded as gated item 12 (STATUS/FLOW SURFACE) --
adjacent to but much bigger than item 4 (no route to dashboard).
Design gate with James BEFORE any build.

His calibration hedge ("I don't practice development... I don't
know what needs to be good enough") was answered on the record:
sub-verdict (c) is deliberately his own willingness to book the
firm meeting -- hesitance is the answer; no dev-team calibration
required. His E&Y migration-friction lens is the right
instrument: the demo audience is a firm in system-change pain,
and a surface needing nativeness fails exactly that audience.

METHOD: the three-sub-verdict design proved itself this attempt.
James: "functionally... it passed everything. We don't really
have a test that it could have passed" -- exactly; the machine
suites clear correctness so the human verdict measures the only
untestable axis (does the story LAND). (a)'s narrow scope (three
screens, not app-wide flow) let him rule PASS on the fiduciary
trio while the app-wide gap went to b/c -- the verdict sheet
localized the defect instead of smearing it. Also: snap-mtime
marks worked fine; chat marks were never needed.

METHOD: failure-class progression across attempts is the story
of P4: attempt 3 failed on correctness + polish; attempt 4
failed on orientation. Each attempt converts vague discomfort
into a named, buildable defect one layer up.

Server left RUNNING on 8500/8501 over the walked
demo-walk-2026-08-08.db. Retained walk dbs now: -04, -04b, -07,
-07b, -07c, -08. Sheet lock f7f821edb1e9 UNCHANGED; walk-report
canonical sha 301b574d UNCHANGED (no code touched this session).

Next: design conversation on the status/flow surface (gated
item 12) -- James's gate, his call on when.

## 2026-08-08 -- s10 cont: ITEM-12 DESIGN CONVERSATION (live;
## rulings recorded as they land)

RULING 1 (James, accepted in his words -- "I accept the
reframe"): reconciliation in this product is a STANDING
CONDITION the system maintains (recomputed on view, statement
leg independent, every difference caused), NOT a task a person
performs. Humans own exactly two things: EXCEPTIONS (ruling on
what the rec surfaces) and PERIOD CLOSE (the judgment act "this
period is done, locked" -- does not exist in the product yet).
Consequences: the status surface is a controller's standing
view (where the money is, what ties, what's unruled, what
period we're in), not a task list; permissions, when they
come, attach at "who rules on exceptions" and "who closes a
period"; ledger events already carry actors, so attribution
predates roles. Viewer persona settled en route: the managing
attorney wearing the controller hat (trust ownership is
non-delegable under bar rules; operating is delegable
controller territory; in the target firm size both hats sit
on one head).

RULING 2 (James, gate decision per the in-place amendment's
carve-out -- "You have permission because the home screen is
right. That's where we need to get"): the firm status page IS
the home screen at "/", replacing the current dashboard
content; authorization extends to modifying existing
casework-ui screens/chrome where the home-screen change needs
it, workaround-if-needed explicitly offered by James.
Feasibility grounded THIS session (run_ui_walk.py read): the
frozen suite pins only (i) post-login URL "/" with the string
"Dashboard" in the page and (ii) click-reachability of all
screens from the landing page (BFS over hrefs). Both are
satisfiable by construction: the new home keeps the Dashboard
name and carries at least the old dashboard's outbound links
(New client, New matter, Calendar, six count-links -- current
_dashboard read at casework-ui/app_ui/server.py:380-400).
Hard limits restated (break-in method): run_ui_walk.py and all
standing suites stay green and get quoted; casework-ui/goal.md
never edited; rendering only, SELECT-only readers, no business
logic; sheet-lock re-sync rules apply if walk routes change.
Side effect: gated item 4 (no route to dashboard) dies
naturally -- the home gains a nav route as part of this work.

RULINGS 3-7 (element red-pen, one per turn; full record in
billing-ui/status-page.md, RATIFIED 2026-08-08): R3 verdict
chips on tiles, tie-out one click away; R4 client-funds tile
links to the recon claims pane until object 3 exists; R5
two-level attention (strict NEEDS ATTENTION over a quiet IN
FLIGHT count line; thresholds are flagged defaults); R6 recent
activity is money events only; R7 header/practice-row/order
approved as sketched. Sheet SIGNED -- the item-12 design gate
is CLOSED for the home page; objects 2 and 3, period-close
act, and the finish pass remain open.

METHOD: mid-red-pen incident -- a ruling request arrived
wrapped in its full analysis (alarm-fatigue theory, threshold
policy, demo staging at once); James: "This feels like 10
different thoughts in one thing. What are you asking me?" The
stripped A/B re-ask got an instant ruling. Standing lesson
saved to auto-memory (decision-prompts-stay-terse): ruling
requests carry choice + options + one-line why; analysis only
on request.

HOME PAGE BUILT (same session, James: "please build"):
- reads.py: recent_money_entries (journal + posting amount +
  invoice code + audit actor; SELECT-only).
- billing_ui.py: dashboard_screen -- money row (kind-summed
  tiles, HOLDS/BROKEN chips from reconcile.three_way at the
  recon screen's own default period, promoted Ledger/Reconcile
  button-links per R3, client-funds tile -> recon claims pane
  per R4); strict NEEDS ATTENTION over quiet IN FLIGHT line
  (R5; thresholds STALE_CHECK_DAYS=30, UNBILLED_NAG_DAYS=30 as
  flagged defaults); thesis empty state "Nothing needs you.
  Everything ties."; money-only activity table with actors
  (R6); practice card absorbing the old dashboard verbatim
  (R7); period line. Unbilled value uses the time_index
  rounding idiom ((secs*rate+1800)//3600) -- integer math.
- html.py: NAV_ITEMS gains ("Dashboard", "/") first; brand is
  a link home for authed users (gated item 4 CLOSED).
- server.py: _dashboard delegates to billing_ui.dashboard_screen.
- Verifier: new step_home_status (after recon step) asserts
  chips, tiles, attention/in-flight, activity actors, practice
  frags, period line -> billing-ui walk is now 18 steps.
Judgment calls flagged: activity amounts render unsigned (the
kind word carries direction); no-bank empty state wording;
attention severity styling (amber left-border).

SUITES (all run this session, quoted):
- billing-ui walk: "18 pass, 0 pending, 0 fail; float-sweep
  pass; verdict GREEN". report_sha.py = 28a19170 SUPERSEDES
  301b574d (new step line; history: ... c61ea17a -> 301b574d
  -> 28a19170).
- ui-walk (frozen): "13 pass, 0 pending, 0 fail; sweeps pass;
  verdict GREEN".
- drive-sheet: "24/24 groups pass; verdict GREEN" (sheet
  UNCHANGED; lock f7f821edb1e9 stands).
- check_sheet_labels: "82 labels checked, 0 not found".
- spine: "107 green, 0 red, 0 pending; checks pass".
- billing: "25 green, 0 red, 0 pending, 0 parked; checks pass;
  verdict: GREEN".
- fiduciary --seeded: "8 pass, 0 red, 0 stub; verdict: GREEN".
- anchor-billing: "PASS (1.261s of 900s budget)".
Server RESTARTED on 8500/8501 over the walked 08-08 db (old
PID 71992 killed; / -> 303, /login -> 200 probed). James's
eyeball of the live page is the remaining acceptance.

## 2026-08-09 -- s11: home-page eyeball DONE; audience + build-order
## rulings (design conversation, no build)

Server incident first: James hit 8500 and saw first-run setup.
Ground truth: a serve.py started 16:30 with NO --db had created
demo-walk-2026-08-09.db (fresh, empty) and held the port; a second
instance on the correct 08-08 walk db double-bound alongside it
(Windows allows it; requests land unpredictably). Stale PID 74736
killed; single listener verified; /login 200 with the login form
quoted. The empty -09 db retained (delete=archive). Login
confusion resolved from the walk sheet: demo.driver@synthetic.test
/ demo-walk-pass (his own Part-A account), MFA code on the demo
mailbox screen.

EYEBALL LANDED: James viewed the s10 home page live (snap
2026-08-09 164020). His read, unprompted: this is the head of
finance's page; the CEO/founding attorney consumes it secondhand,
narrated, e.g. at a weekly/monthly meeting; further screens would
serve the performance views (who is way behind, who keeps the firm
in cash, is billing up to date).

RULING (audience, item-12 context): the dashboard's owner is the
FINANCE SEAT. Lead attorney/CEO reads it only via that seat. Agent
refinement accepted: the page as built does the CONTROLS job
(daily: does it tie); the PERFORMANCE job (periodic, comparative:
AR aging, client concentration, WIP/unbilled) is distinct, does
not exist yet, and maps onto the open item-12 queue -- client
summary (object 3) seeds the per-client views; the period-close
act is the formal monthly meeting. No scope added.

RULING (build order, roles): screens are built OWNER-SEES-ALL for
now; every screen gets an AUDIENCE TAG at its design pass
(dashboard: finance seat -- first tag); multi-user enforcement is
a FUTURE CONTRACT that inherits the tags (permission substrate
tables already exist in the casework schema, verified in the
walked db this session). Read surfaces restrict late (overlay);
write flows get the segregation-of-duties question AT DESIGN TIME
-- flagged now for the period-close act (maker-checker or single
actor is a design question, not an assumption).

METHOD: the audience question ("who would look at this page?")
came from James cold off the live product, not from the design
deck -- the eyeball produced a ratifiable ruling the sheet pass
did not surface. Product-first gates keep earning their cost.

No code, no sheet, no suite runs this session (design only).
Sheet lock f7f821edb1e9 and walk sha 28a19170 stand.

## 2026-08-09 -- s11 cont: FLOW MARKERS design pass (item-12
## object 2) -- scope + vocabulary RULED

Grounding ran before any question: eight money-in-motion states
enumerated from the walked db schema + reconcile.py causes +
invoice_status source (all quoted this session). Inventory table
in chat; all eight facts already exist in the data layer --
object 2 is pure visibility.

RULING (scope): WIDE -- full revenue lifecycle, all eight states,
not just the bank window. Rationale accepted: the attempt-4
defect was the practice's flow (invisible sent-invoice, silent
settlement), and the client-summary object needs the lifecycle
vocabulary anyway. Build STAGES by demo relevance -- payment
plans (0 rows in every walk db) carry the vocabulary but earn no
build until a walk exercises them.

DESIGN TURN (James's find): the first five-word draft labeled
OBJECTS and broke on partials ("could be partially billed...
awaiting could have paid a partial") plus a word collision
(Scheduled reads as calendar work). Reframe ratified: markers
label DOLLARS, not objects -- every dollar in exactly one bucket
at any moment; objects may straddle; totals foot.

RULING (vocabulary, signed): four buckets + rest --
  Unbilled    earned, on no invoice (state 7; fee-side)
  Outstanding on an invoice, unpaid (states 5,6,8; inherits the
              app's existing invoice-status word; checks move OUT
              of "outstanding" -> one word one meaning)
  Settling    client paid, processor holds (state 4)
  Clearing    booked, bank unconfirmed (states 1,2,3; both
              directions; all trust in-motion money lives here)
  at rest     landed + reconciled; carries NO marker
Scheduled is DISSOLVED to an annotation on Outstanding ("on
plan, next due ..."). Principle: bucket = position; annotations
carry story (age, sent date, plan promise, check #, expected
settle). Derived free: Unbilled + Outstanding + Settling = the
inbound pipeline, a sum over quotable facts, never stored.
Client-funds tile is a stock, untouched by flow.

Audience tag (per s11 build-order ruling): flow markers serve
the FINANCE/COLLECTIONS seat; rendered inline on shared screens.

RULING (placement, signed): three layers, no new screens --
L1 dashboard pipeline line (AMENDS home-gate R5: the quiet
in-flight line renders DOLLARS by bucket instead of counts;
two-level attention structure unchanged; each amount links to
its backing list and foots to it); L2 amount splits on object
pages (invoice balance split by bucket incl. partials; matter
page unbilled line; recon screen untouched); L3 row chips on
existing lists (invoice rows, ledger rows, payment rows;
at-rest rows carry NO chip). Staging: plan annotations render
only when plan rows exist. Chip styling / wording / thresholds
are flagged judgment calls. James: "I agree. Proceed." -> BUILD
authorized this session.

FLOW MARKERS BUILT (same session, James: "I agree. Proceed."):
- reads.py: settling_payments (processor-held online payments;
  journal_entry_id-null test, same authority as the invoice
  page's status line; SELECT-only).
- billing_ui.py L1: dashboard "In flight" counts line replaced
  by the "On the way:" pipeline dollar line (unbilled /
  outstanding / settling / clearing; empty buckets absent;
  rate-less unbilled time shows hours, never a fabricated zero).
  Links: time index, billing outstanding tab, recon; a single
  settling payment links to its own page.
- billing_ui.py L2: invoice header gains the dollars-in-buckets
  split (collected / settling / outstanding + overdue-or-sent
  annotation), rendered only when money straddles buckets;
  foots by construction to charges - discount (same identity as
  billing.invoice_balance). Payment rows + payment detail carry
  a Settling pill while the processor holds the money.
- billing_ui.py L3: billing-list outstanding pills carry
  overdue-Nd / sent-date chipnotes; bank-ledger rows the bank
  has not confirmed carry a Clearing chip (same reconcile
  engine, recon default period; at-rest rows unmarked).
- server.py (_matter_detail): one unbilled-time hint line when
  the matter has time on no invoice (placement L2 as signed;
  frozen ui-walk stayed green -- gate satisfied by suite).
- CSS: .pill.settling, .pill.clearing, span.chipnote, p.split.
Judgment calls flagged: settling has no backing list screen
(single payment links to its page, plural renders unlinked);
overdue beats sent when both apply; chip colors reuse existing
pill families (settling=refunded purple, clearing=trust blue).

Verifier: step_settlement now asserts the settling moment at
three surfaces (pipeline line 5,000.00 settling; invoice row
chip; payment detail chip) before extinguishing it; ledger
drilldown asserts Clearing chips; home step asserts the
pipeline line with THIS walk's own end figures (200.00 unbilled
-- the bare-number entry is never imported; 5,150.30 clearing
-- the disbursement bank event IS recorded) and that empty
buckets render no segment. First assertion draft copied the
08-08 walked db's end state (6,350.30) -- the two walks differ
there; caught by the suite, fixed to the verifier's own truth.

SUITES (all run this session, quoted):
- billing-ui walk: "18 pass, 0 pending, 0 fail; float-sweep
  pass; verdict GREEN". report_sha.py = e6ae695b SUPERSEDES
  28a19170 (history: ... 301b574d -> 28a19170 -> e6ae695b).
- ui-walk (frozen): "13 pass, 0 pending, 0 fail; sweeps pass;
  verdict GREEN".
- drive-sheet: "24/24 groups pass; verdict GREEN"; sheet lock
  f7f821edb1e9 UNCHANGED (no pinned label touched).
- check_sheet_labels: "82 labels checked, 0 not found".
- spine: "107 green, 0 red, 0 pending; checks pass".
- billing: "25 green, 0 red, 0 pending, 0 parked; checks pass;
  verdict: GREEN".
- fiduciary --seeded: "8 pass, 0 red, 0 stub; verdict: GREEN".
- anchor-billing: "PASS (1.266s of 900s budget)".

## 2026-08-09 -- s11 cont 2: CLIENT SUMMARY design pass (item-12
## object 3) -- placement RULED

Grounding: contact page today is casework-only (profile facts,
matters, one action; _contact_detail quoted). Every per-client
money fact already exists behind proven readers (trust subs,
invoice balances + due dates, unbilled by contact, settling,
posted payments) -- object 3 is assembly, not machinery.

RULING (placement, signed): Option A with C's deferral -- a
MONEY BAND on the existing client page. One client, one page
(a separate billing-side client page recreates the split-brain
interaction cost; rejected). Touching the frozen casework-ui
contact screen is the gate decision and this signature makes
it, matter-page precedent applies (additive band; frozen
ui-walk must stay green at the suite). The band is the
AUDIENCE BOUNDARY (finance-seat content on a shared page;
droppable per-role later without redesign). Firm-wide rankings
(way behind / keeps-us-in-cash) are NOT this object: they are
rollups across client summaries, queued for the period-close
design pass. James: "I agree. A with C's deferral built in."

RULING (band contents, signed): three headline figures (Held in
trust -> recon claims pane per R4; Outstanding; Collected to
date = lifetime posted payments, the keeps-us-in-cash seed);
a client-scoped pipeline line in the dashboard grammar
(unbilled / outstanding+overdue / settling); their invoice
table with the billing-list chips. CLEARING deliberately
omitted from the client band -- bank-side fact, weak client
attribution; it lives on bank surfaces. James: "Yes this looks
good. Continue." -> BUILD authorized.

CLIENT MONEY BAND BUILT (same session):
- billing_ui.py: client_money_band -- headline figures (Held in
  trust -> recon per R4; Outstanding; Collected to date =
  posted non-refunded payments, settling excluded so buckets
  never double-count), client-scoped pipeline line (unbilled
  scopes by contact OR the client's matters; outstanding
  carries worst-overdue; settling links to a lone payment's
  page), invoice table with billing-list chips. Returns ""
  until the client has any money story; carries its own
  BILLING_STYLE block (contact page renders outside billing's
  _page).
- server.py (_contact_detail): band inserted between profile
  and Matters cards; rendering only.
Judgment calls flagged: empty-band suppression (casework-pure
page until money exists); headline zeros always render once
the band exists (zeros are information); band styling rides
the existing card/pill families.

Verifier: new step_client_money (after home status; 19 steps
now) asserts the three figures on the walk's Vera (800.00 held
/ 0.00 outstanding / 8,500.00 collected), the client-scoped
200.00 unbilled (the bare-number entry rides her matter), the
three invoice codes, and that clearing does NOT leak into the
band (ruled omission enforced by suite).

SUITES (all rerun this session, quoted):
- billing-ui walk: "19 pass, 0 pending, 0 fail; float-sweep
  pass; verdict GREEN". report_sha.py = 5ba384cc SUPERSEDES
  e6ae695b (history: ... 28a19170 -> e6ae695b -> 5ba384cc).
- ui-walk (frozen): "13 pass, 0 pending, 0 fail; sweeps pass;
  verdict GREEN" (contact-page band additive; gate satisfied).
- drive-sheet: "24/24 groups pass; verdict GREEN"; lock
  f7f821edb1e9 UNCHANGED. check_sheet_labels: "82 labels
  checked, 0 not found".
- spine: "entries: 111  green: 107  red: 0  pending: 0
  parked: 4".
- billing: "25 green, 0 red, 0 pending, 0 parked; checks pass;
  verdict: GREEN".
- fiduciary --seeded: "8 pass, 0 red, 0 stub; verdict: GREEN".
- anchor-billing: "PASS (1.281s of 900s budget)".
Server restarted on 8500 over the 08-08 walked db; Vera's live
band quoted in-session (800.00 / 0.00 / 8,500.00, three
invoices listed). Item-12 remaining after this: period-close
act design pass, then the finish pass; step-29 ledger-link fix
still queued.

## 2026-08-09 -- s11 cont 3: footed payments drill (James's catch
## on the live band)

James, off the live page: "why no link to drill on the $ value
for Collected to date". Verdict accepted as a defect -- the
figure had no backing list anywhere (payments render only
per-invoice); the same gap flagged for the dashboard settling
segment had slipped through UNFLAGGED here. Options offered
(A build the footed listing / B accept two-click drill);
RULING: A.

BUILT: client_payments screen at /billing/clients/<id>/payments
(new route; tier-3 fence unaffected -- path not reserved).
Every payment on the client's invoices, date-ordered, each row
linking payment + invoice; foot "Collected to date: $X" equals
the band headline by construction (settling and refunded rows
chipped and excluded from the foot, each called out in a hint
under it when present). Band: Collected figure now links to
the listing; the band's settling segment links there too
(retiring that flagged judgment call band-side; the DASHBOARD
settling segment's no-list gap still stands flagged).

Verifier: step_client_money extended -- asserts the linked
figure, drills the listing, asserts the foot ties to the
headline and all three method words render; chip-absence
asserted on rendered spans, not raw words (the style block
itself names the pill classes -- first draft tripped on it).

Incidents, both caught by suites: (1) frozen ui-walk no-logic
lint flagged the WORD "SELECT" in the new function's docstring
(comments count as SQL-outside-reads.py); reworded, lint has
zero tolerance and that is correct. (2) band assertion needed
re-pinning to the now-linked figure.

SUITES (rerun after fixes, quoted): billing-ui walk "19 pass,
0 pending, 0 fail; float-sweep pass; verdict GREEN";
ui-walk (frozen) "13 pass, 0 pending, 0 fail; sweeps pass;
verdict GREEN"; earlier this round and unaffected by the
docstring-only fix: spine "entries: 111  green: 107  red: 0
pending: 0  parked: 4", billing "25 green ... verdict: GREEN",
fiduciary "8 pass ... verdict: GREEN", anchor-billing "PASS
(1.301s of 900s budget)", drive-sheet "24/24 groups pass;
verdict GREEN", labels "82 checked, 0 not found"; sheet lock
f7f821edb1e9 unchanged. report_sha.py = c59b8e9d SUPERSEDES
5ba384cc (history: ... e6ae695b -> 5ba384cc -> c59b8e9d).
Server restarted; live listing quoted: three payments
(500 direct / 3,000 earn-out / 5,000 card) footing to
$8,500.00 = the band headline.

## 2026-08-09 -- s12: period-close act -- designed, ratified, BUILT

DESIGN GATE (the last item-12 object). Three rulings signed in
conversation before the sheet:
- PC1 HARD CLOSE: closing locks the month; the engine refuses
  postings dated into it; late facts post current-dated.
- PC2 TWO-STEP, SAME PERSON ALLOWED AND SHOWN: prepare -> approve,
  recorded signers; one person may sign both, the record says so.
- PC3 TIE REQUIRED, EXCEPTIONS CARRIED: every account's three-way
  identity must HOLD; each reconciling item individually
  acknowledged and printed on the record.
Sheet: period-close.md, 12 numbered elements, SIGNED as drafted
("The sheet looks good as drafted"); flags 9 (billing documents
not locked in v1) and 10 (no reopen, ever) accepted as flagged.
One red-pen round: element 1 was present-tense fact about an
unbuilt route; James hunted for a page that existed only on paper.
Evidence-discipline class, s7 lineage; corrected to proposal
phrasing with verified ground facts. PROGRAM AMENDMENT recorded in
../CLAUDE.md (2026-08-09, ratified via the signed sheet): scoped
casework write surface for the close.

BUILT, all layers:
- Schema: period_closes via gen_schema.py (audited, no soft
  delete, canonical-JSON snapshot column); schema.sql regenerated.
- Core: casework/app/period.py (closable_month strict-order,
  compute over the recon oracle, prepare/approve with PC2
  stale-void, assert_open); lock guard called from ledger._post
  (posted_at + co-written events) and create_external_event.
- UI: /billing/close (step-1 ack checkboxes each required, step-2
  approve, broken-tie block linking Reconcile), record page
  /billing/close/<YYYY-MM>, closed-months card, dashboard
  period-line + billing action-row links. Rendering only; the two
  writes route through period.prepare/approve.
- Verifiers: fiduciary check F9 (closed periods must recompute
  byte-equal; calibration scenario added, selftest counts 7/7);
  unit_period_close.py 6/6 (unit_ convention -- parity discovery
  is corpus-map-bound); walk step 20 "period close: July coda".

CROSS-PROJECT FIX (flagged prominent): reconcile._sub_ledger_sum
computed client claims AS OF NOW while bank and book legs were as
of period_end -- latent, because suites only reconciled at period
ends covering all activity; any retrospective recompute (closing
July from August; F9's drift check) falsely broke the tie. Fixed
to as-of-period_end under the standing F7 amendment (recon-model
file, strengthen-only); current-period recons byte-unchanged, all
suites requoted below.

WALK DESIGN CALL: the walk's amount story is August-dated and
August is still running, so the close step is a JULY CODA created
at walk END (one 100.00 consult billed + paid direct 07/01) --
the ratified August story stays exactly as the anchor mirrors it,
and July closes through the UI: prepare (clean carried state),
approve, record page (same-signer disclosure asserted), then PC1
proven UI-level (July-dated disbursement refuses visibly, moves
no money) and at the bank-record choke point; fiduciary rerun on
the closed walked db inside the step.

Judgment calls flagged, unruled: a month is closable only after
it ENDS (not in the sheet; accounting default); ranking rows are
plain text, no contact links in v1; approve-on-stale COMMITS the
void before rendering the error (the void must survive);
closable_month returns one month (strict order) -- the close page
never offers a choice.

SUITES (all rerun this session, quoted):
- billing-ui walk: "20 pass, 0 pending, 0 fail; float-sweep
  pass; verdict GREEN".
- ui-walk (frozen): "13 pass, 0 pending, 0 fail; sweeps pass;
  verdict GREEN".
- spine: "107 green, 0 red, 0 pending; checks pass".
- billing: "25 green, 0 red, 0 pending, 0 parked; checks pass;
  verdict: GREEN".
- fiduciary --seeded: "9 pass, 0 red, 0 stub; verdict: GREEN"
  (F9 live); --selftest: "calibration scenarios: all behaved".
- anchor-billing: "PASS (1.275s of 900s budget)".
- drive-sheet: "24/24 groups pass; verdict GREEN"; labels: "82
  labels checked, 0 not found"; sheet lock UNCHANGED.
report_sha.py = 30301f88 SUPERSEDES c59b8e9d (history:
... 5ba384cc -> c59b8e9d -> 30301f88).

OPS: migrate_period_close.py written (lifts DDL from generated
schema.sql, fail-loud); run on demo-walk-2026-08-08.db ("added,
0 rows, 3 audit triggers"). Stale s11 server killed (single bind
verified by netstat before and after), restarted on 8500 over the
migrated db. Demo-db ground truth quoted: all money facts are
August 2026, so /billing/close shows the honest empty state until
September; the attempt-5 fresh db seeds July dates (seed_demo
NOW=2026-07-20), so James can drive the close live at the
attempt. Sheet amendment for a close act in the drive is an
attempt-prep decision, queued in state.md.

## 2026-08-09 -- s12 cont: live eyeball + firm-local dates ruling

EYEBALL LANDED: James swapped to a July-seeded preview db
(regenerated demo-billing.db on the new schema -- July closable,
both ties HOLD, two genuine carried items) and drove the FULL act
himself: prepare with both acknowledgments, approve, record page.
Verdict on the populated page: "seems pretty good".

Two defects off his snaps:
1. Carried-item CHECKBOXES float away from their text on the
   prepare page (label layout). Mechanical; queued for the finish
   pass alongside step-29.
2. His close record read "Prepared on 08/10/2026" -- TOMORROW.
   Cause verified: _today() stamped business dates in UTC, which
   rolls at 8pm Eastern; app-wide (every form default), first
   prominent on the close signature line. RULING (James): business
   dates stamp FIRM-LOCAL. Applied at both sites: billing_ui
   _today() and the client pay date in casework/app/server.py
   (same business-date class, rides the ruling -- disclosed;
   audit/session TIMESTAMPS stay UTC). Judgment call flagged:
   firm-local = server system clock, not the users.timezone
   column.

Reciprocal guard (casework/app touched), ALL suites requoted:
spine "107 green, 0 red, 0 pending; checks pass"; billing "25
green ... verdict: GREEN"; fiduciary --seeded "9 pass, 0 red,
0 stub; verdict: GREEN"; anchor-billing "PASS (1.295s of 900s
budget)"; ui-walk (frozen) "verdict: GREEN"; billing-ui walk
"20 pass, 0 pending, 0 fail; float-sweep pass; verdict GREEN";
labels "82 checked, 0 not found". drive-sheet first went 23/24
FAIL -- its own today() helper was still UTC while the app went
firm-local; the sheet's "issue date starts on today" means the
human driver's today, so the DRIVER was aligned to the ruling
(sheet text untouched, lock intact) -> "24/24 groups pass;
verdict GREEN". report_sha.py = 30301f88 UNCHANGED (walk report
is date-free; no supersession).

Server restarted on 8500 over data/demo-billing.db (single bind
verified). NOTE for cold resume: 8500 currently serves the
PREVIEW db, not a walk db; James may click Prepare/Approve
freely -- it regenerates via verify/seed_demo.py.

## 2026-08-09 -- s13: FINISH PASS (James's eyes first, agent pass second)

James ruled on his own pass before the session: "I think it looks
good" -- his half of the finish pass is done. This session ran the
agent pass: the two queued mechanical defects, a full-screen sweep
in the browser, one sweep catch, all suites.

FIX 1 (step-29, friction entry 1): the ledger links under the
trust-overview dollar tiles were small underlined .sub text --
"always miss them". Promoted to the .go button affordance the
dashboard tiles already use (billing_ui.trust_overview); link text
and hrefs byte-identical (drive_sheet pins "SYNTH IOLTA ledger",
the walk pins /billing/trust/<id>). Verified on-screen: chips
render, chip navigates.

FIX 2 (carried-item checkbox float, James's s12 snap): root cause
is the base stylesheet's input { width: 100% } -- the ack
checkbox went full-width and shoved its label text to the next
line. Override added in BILLING_STYLE: label.ackrow input,
label.pick input { width: auto; padding: 0; margin-right:
0.45rem; }. Covers the same latent defect on the invoice import
card's .pick rows. Verified on-screen: checkbox inline with its
text on the prepare page.

FIX 3 (sweep catch): Vera's B0001 charge rendered a blank DATE
cell -- seed_demo never passed charge_date, predating gated item
C's ruling that charges carry real dates at the write path (not
cell filler). All six seed add_charge calls now date to their
invoice's issue date. seed_demo.py is this child's own generated-
artifact seeder; regenerated. Verified on-screen: 07/21/2026 in
the cell.

SWEEP (preview db, July-seeded): dashboard, billing home, invoice
B0001, client page Money band, footed payments listing, trust
overview, IOLTA ledger, recon (three panes, identity footed),
time, saved charges, and the FULL close act driven end to end --
prepare with both acknowledgments, approve, record page. Firm-
local dates verified live: both signature lines read 08/09/2026
(the s12 defect showed tomorrow). Three B0001s in the firm-wide
invoice list checked against invoice-codes.md: per-client series,
by design, not a defect.

FLAGS (outside this child's write surface -- gate decisions, not
code changes from here): (1) the contact detail card renders raw
machine keys as labels (bio.family_name, bio.given_name,
contact.email); (2) the contact page's Matters card prints ISO
dates (2026-07-20) against the MM/DD/YYYY convention everywhere
else. Both live on frozen casework-ui screens James has walked
through four attempts without naming, but attempt 5's verdict is
beauty-sensitive; James may gate them in or leave them.

SUITES (all rerun this session, quoted):
- billing-ui walk: "20 pass, 0 pending, 0 fail; float-sweep pass;
  verdict GREEN".
- drive-sheet: "24/24 groups pass; verdict GREEN"; labels: "82
  labels checked, 0 not found"; sheet lock UNCHANGED.
- ui-walk (frozen): "13 pass, 0 pending, 0 fail; sweeps pass;
  verdict GREEN".
- spine: "107 green, 0 red, 0 pending; checks pass".
- billing: "25 green, 0 red, 0 pending, 0 parked; checks pass;
  verdict: GREEN".
- fiduciary --seeded: "9 pass, 0 red, 0 stub; verdict: GREEN".
- anchor-billing: "PASS (1.300s of 900s budget)".
report_sha.py = 30301f88 UNCHANGED -- rendering-only changes left
the walk report byte-identical; no supersession.

OPS: netstat single-bind protocol followed at every relaunch
(stale s12 server killed first). Preview db regenerated TWICE:
once mid-session to restore July-closable state for the checkbox
eyeball (the s12 live close had already sealed July), once at
close so the served db carries the dated charges and an open
July. Server left UP on 8500 over
billing-ui/data/demo-billing.db; reseeds wipe sessions, so the
next login is demo.reviewer@synthetic.test / demo-seed-pass with
the code shown on-screen.

Next: attempt-5 prep -- James's call on the demo-sheet close act
(precondition 5), then the standard attempt protocol.

## 2026-08-09 -- s13 cont: ATTEMPT-PREP RULED -- the sheet gains the
## close act (Part K) and the lock re-syncs

RULING (James, precondition 5): "I think we should include a
period close step and re-sync. I think that is the right way to
do this to be thorough." The demo sheet gains the period-close
act; the sheet-lock re-sync protocol applies.

BUILT (seventh sheet amendment, recorded in the sheet's header):
Part K, steps 33-40, mirroring walk-verifier step 20's July coda
-- the walk's story is August (still running; a month closes
only after it ends), so Part K first has the driver bill and
collect one 100.00 July consult (07/01/2026, the Part-D moves),
making July the closable month; then the act: prepare (clean
carried state), approve, the permanent record page (same-signer
disclosure), and the PC1 lock proven from the driver's chair --
a July-dated 1.00 disbursement typed on purpose, refused on
screen, Vera's 800.00 unmoved. Marks: M7 added (step 40 is now
"done"); the 20:00 soft budget stays defined over M1->M6 so
attempts stay comparable, M1->M7 recorded as data -- judgment
call, flagged for re-rule. Close-out: check_demo_walk.py gains
the Part-K receipt (the 07/01-issued bill paid + exactly one
closed period 2026-07, both signers recorded); smoke-tested
against the attempt-4 walked db -- fails ONLY the new receipt
(that db predates the act), exit 1.

METHOD: the drive's injected stray (attempt-3 regression, step
21) caught my first draft red-handed: the sheet pinned the coda
bill as B0003, a code predicted for a FUTURE invoice -- exactly
the failure class item B taught for numbers. Codes are stable
once STAMPED, never as predictions. The sheet now has the driver
NOTE the code from the crumb at creation (B0003 on a clean walk)
and steps 34-35 locate by the noted code; the drive reads the
crumb the same way and its coda lands on B0004 behind the stray,
proving the rule. The regression paid for itself twice.

Also caught by the oracles: four Part-K quotes were COMPUTED
strings (month headings, the signer line, the core refusal
message) -- the label audit requires quoted text to be literal
in rendering source; re-phrased unquoted per the sheet's own
Collect $500.00 precedent. Judgment call, flagged: the refusal
error renders the period as 2026-07 (ISO-style, core-owned text
in casework/app/period.py) inside an otherwise MM/DD/YYYY
surface; the sheet quotes it verbatim with a translation line.
James may re-rule the message's wording (period.py is inside the
standing close amendment's write surface).

SHEET LOCK: f7f821edb1e9 -> 85e4e4633a37 (re-synced via the
protocol: drive extended first, sheet verified against it,
EXPECTED_SHEET_SHA updated; two intra-session intermediates as
the draft hardened).

SUITES (all rerun after the amendment, quoted):
- drive-sheet: "27/27 groups pass; verdict GREEN" (was 24
  groups; +3 Part-K groups).
- labels: "91 labels checked, 0 not found" (was 82).
- billing-ui walk: "20 pass, 0 pending, 0 fail; float-sweep
  pass; verdict GREEN"; report_sha.py = 30301f88 UNCHANGED (no
  app code touched this round).
- ui-walk (frozen): "13 pass, 0 pending, 0 fail; sweeps pass;
  verdict GREEN".
- spine: "107 green, 0 red, 0 pending; checks pass".
- billing: "25 green, 0 red, 0 pending, 0 parked; checks pass;
  verdict: GREEN".
- fiduciary --seeded: "9 pass, 0 red, 0 stub; verdict: GREEN".
- anchor-billing: "PASS (1.294s of 900s budget)".

Attempt-5 preconditions are now ALL MET. Next: the standard
attempt protocol -- agent seeds a fresh dated db behind 8500,
runs the walk verifier green, hands over the URL and the sheet;
James drives all 40 steps; close-out; three-part verdict.

## 2026-08-10 -- s14: ATTEMPT 5 DRIVEN -- all 40 steps, record filed,
## verdict PENDING James's sit-with-it review

James drove the full 40-step walk solo on the fresh
data/demo-walk-2026-08-09b.db (sheet lock 85e4e4633a37), 23:43 -
00:06 firm-local, crossing midnight mid-walk. The resumed session
acted as RECORDER only. One mid-walk pause: at the step-17
CHECKPOINT he read the conditional STOP ("if the payment line
reads direct") as an instruction and halted; recorder clarified
sheet mechanics only (allowed: wording questions about the
sheet), he confirmed the line read card, walk resumed. Ground
truth pulled before clarifying: payment 2 was sim_card via
processor txn 1 -- the data was never in doubt.

CLOSE-OUT (quoted, this session):
- check_demo_walk.py data/demo-walk-2026-08-09b.db: 13/13 PASS
  incl. "july coda closed (33-40): coda bill 4 paid; closed
  periods ['2026-07']" and "fiduciary in place: 9 pass, 0 red,
  0 stub; verdict: GREEN". "check-demo-walk: PASS", exit 0.
- Snap review: James snapped from step 15 on (32 images,
  Desktop/snaps, steps 15-40); every snap matches its step's
  promised labels, figures, and pills. Dollar spine foots end to
  end: 5,000.00 gross to trust / 349.70 operating after fee /
  2,000.00 post-earn-out / 800.00 after disbursement / 3,449.70
  operating at close. Correction trail e1 + e6 "reverses e1" +
  e7 "replaces e1". Recon ties 800.00 = 800.00 = 800.00 with
  in-transit settlement and outstanding check shown. Part K:
  B0003 July coda, two-signature close (prepared + approved
  Demo Driver 08/10/2026 -- firm-local, correct under the s12
  ruling), refusal verbatim "period 2026-07 is closed (hard
  close through 2026-07): post the fact current-dated in the
  open month", Vera's 800.00 unmoved on the final screen.

MARKS (firm-local EDT; M2-M7 snap mtimes per attempt-4
precedent, M0/M1 from the walked db's audit timestamps --
no snaps exist before step 15):
  M0 ~23:43:26 | M1 ~23:43:30 | M2 23:48:21 | M3 23:51:52 |
  M4 23:55:32 | M5 23:58:30 | M6 00:00:26 | M7 00:06:03.
  M1->M6 = 16:56 -- UNDER the 20:00 soft budget (first time).
  M1->M7 = 22:33 (data; no budget).

FRICTION LOG (all minor, none a stop-rule event):
1. Step-17 checkpoint wording read as an unconditional stop
   (sheet wording).
2. Step-27 "Correct this payment" card has a Note field the
   sheet never mentions; James filled it ("Was not told to
   leave note...") -- harmless to the books (sheet gap).
3. Step-39 refusal renders the correct verbatim error but
   CLEARS the form's typed values -- client, amount, payee all
   reset (product polish; from snap 39B).

VERDICT: PENDING. James's reaction: "This looks pretty good. I
have to sit with it a while and click around for UI" -- the
three sub-verdicts (a)/(b)/(c) are deliberately unsigned; a
verdict signed on trust is worthless (interface ruling). The
walked db stays behind 8500 for his review clicking. P4 stays
OPEN until he signs the sheet.

METHOD: the recorder-silence rule survived contact with a live
driver misread -- the sheet's own carve-out ("wording questions
about this sheet may be clarified") was exactly the release
valve needed; the screens were never discussed mid-walk. The
step-17 checkpoint phrasing goes to the friction log, not a
mid-walk sheet edit.

## 2026-08-10 -- s15: friction items 1-3 knocked out (James ruled them
## in as the more-work round's first slice); verdict still PENDING

James ruled the three attempt-5 friction items in as work. All
three fixed this session, each grounded before editing:

ITEM 1 (step-17 checkpoint wording). Root cause: the CHECKPOINT
block carried only failure language ("STOP here"); the pass
outcome lived up in the Observe line, so a driver scanning the
block saw an instruction to stop. Steps 16 and 39 never misread
because they state the pass state first and gate STOP behind
"if anything else." Step 17 reworded to match that pattern:
"CHECKPOINT: card is the expected reading -- continue to Part
F. Only if the line reads direct instead has the walk diverged:
STOP and record it; do not continue." James approved the
wording before the edit.

ITEM 2 (step-27 Note field absent from the sheet). Ground truth
first: a typed Note becomes the memo on the reversal/repost
journal entries (billing.edit_payment, casework/app/billing.py
~508; route passes it through at billing_ui.py payment_edit)
and renders in the Journal trail's Memo column James observes
at step 28. James chose option (b): use the field as a demo
beat rather than just acknowledge it. Sheet step 27 gains
'- "Note" = Deposit date corrected per bank record' (placed in
the card's on-screen field order); step 28's Observe now reads
"...and the corrected entry's Memo carries your note -- the
correction's written reason lives in the books." Driver
s27_28_correct now posts that note and asserts it renders.

ITEM 3 (step-39 refusal wiped typed values). Root cause: the
refused post re-rendered disburse_form with no values --
every field reset to default. Fix, rendering-only, in
casework-ui/app_ui/billing_ui.py: disburse_form gains a
values= param (the submitted form on a refused post); all
three selects prefill via selected=, Amount/Date/Memo via
value=, the Pay-to input gains an escaped value attr;
disburse_post's error path passes values=f. No new business
logic, no new write path. Driver s39_40_lock_proof now asserts
the refusal page still carries value='1.00',
value='2026-07-05', value='SYNTH late vendor', and the client
selection. Sheet step 39's Observe gains "The form still holds
everything you typed -- client, amount, date, payee -- a
refusal never costs you your work."

SHEET LOCK: three re-syncs this session, each verified against
the driver before updating EXPECTED_SHEET_SHA:
85e4e4633a37 -> dabaf08073ee (item 1) -> abb07dcfa753 (item 2)
-> 7612d81b8aad (items 1-3 final). Attempt 5's record keeps its
85e4e4633a37 lineage untouched; a future attempt 6 drives the
7612d81b8aad sheet.

SUITES (all run this session, quoted):
- drive_sheet.py: "drive-sheet: 27/27 groups pass; verdict
  GREEN" (final run, with the new note + kept-values asserts
  live; step 39-40 detail now reads "typed values kept").
- check_sheet_labels.py: "sheet-label audit: 92 labels
  checked, 0 not found" (grew 91 -> 92 with the Note label).
- casework-ui run_ui_walk.py: "ui-walk: 13 pass, 0 pending,
  0 fail; sweeps pass; verdict GREEN".
- casework-billing run_billing.py: "billing: 25 green, 0 red,
  0 pending, 0 parked; checks pass; verdict: GREEN".
- run_fiduciary.py --selftest: "selftest: draft DDL
  instantiated; empty ledger 7/7 non-stub checks pass;
  calibration scenarios: all behaved", exit 0. (Argless run
  prints usage, exit 2 -- it wants a db path; the walked db's
  9/0/0 GREEN from the s14 close-out stands, untouched by
  today's rendering-only edits.)
- casework run_spine.py: "spine: 107 green, 0 red, 0 pending;
  checks pass".

SERVER: 8500 restarted on the SAME walked db
data/demo-walk-2026-08-09b.db (standing rule: restart after any
app_ui change; the db was not reseeded or swapped -- James's
review clicking and his db session survive). Old PID 51612
killed, new PID 59724, single bind verified by netstat, HTTP
303 on /. The step-39 kept-values behavior is live for his
review.

VERDICT: still PENDING -- the three sub-verdicts (a)/(b)/(c)
remain unsigned; this was more-work-round work, not a
substitute for the sheet.

## 2026-08-10 -- s15 cont: PC1 refusal speaks month names (open
## judgment call ruled in by James)

James took the flagged judgment call next: the period-close
refusal rendered ISO ("period 2026-07 is closed...") on an
MM/DD/YYYY surface. Fixed in casework/app/period.py (inside the
2026-08-09 period-close amendment's authorized write surface):
new _month_name() helper ('2026-07' -> 'July 2026'); the
assert_open refusal now reads "July 2026 is closed (hard close
through July 2026): post the fact current-dated in the open
month".

SCOPE EXTENSION, disclosed: three sibling PeriodError messages
in the same module carried the same ISO defect and got the same
helper -- "cannot close July 2026: reconciliation broken for
...", "July 2026 has no prepared close to approve", "stale
prepare for July 2026: ...". James ruled in the refusal
specifically; the siblings are the same defect in the same
authorized file. Flagged here for his re-rule if unwanted.
Grounded first: no test anywhere pins any of these strings
(grep across atlas *.py; unit_period_close.py asserts types,
not text).

RIPPLE: sheet step 39's verbatim quote updated to the new
refusal; the "(2026-07 is the app's internal name for July
2026.)" explainer deleted -- the message speaks English now.
Driver assert requoted. Sheet lock re-synced 7612d81b8aad ->
04f8db62ec6d.

SUITES (core touch -> reciprocal guard, ALL suites, quoted):
- drive_sheet.py: "drive-sheet: 27/27 groups pass; verdict
  GREEN"
- check_sheet_labels.py: "sheet-label audit: 92 labels checked,
  0 not found"
- casework run_spine.py: "spine: 107 green, 0 red, 0 pending;
  checks pass"
- casework-billing run_billing.py: "billing: 25 green, 0 red,
  0 pending, 0 parked; checks pass; verdict: GREEN"
- run_fiduciary.py --selftest: "calibration scenarios: all
  behaved"; --seeded: "fiduciary: 9 pass, 0 red, 0 stub;
  verdict: GREEN", exit 0
- casework-ui run_ui_walk.py: "ui-walk: 13 pass, 0 pending,
  0 fail; sweeps pass; verdict GREEN"
- tests/unit_period_close.py: "6/6 pass", exit 0

SERVER: 8500 restarted again (period.py is loaded code); same
walked db, not reseeded; old PID 59724 -> new PID 76416, single
bind, HTTP 303. The English refusal is live: Billing -> Trust
accounting -> Disburse funds, date it into July.

NOTE: the s14 attempt-5 record quotes the OLD refusal verbatim
as observed -- that history stands unedited; attempt 6 (if any)
observes the new text via the 04f8db62ec6d sheet.

## 2026-08-10 -- s15 cont: contact-screen flags fixed under an explicit
## gate ruling (frozen casework-ui screen opened for two cosmetic fixes)

GATE RULING (James, this session, verbatim "Yes, premission
granted"): the frozen casework-ui contact detail screen may be
touched for exactly two fixes -- (1) fact labels render human
text from fact_definitions.label instead of raw machine keys
(bio.family_name -> Family name), falling back to the raw key
when no definition exists (a visible gap, never a blank);
(2) the Matters card's Created column renders MM/DD/YYYY via
billing_ui.fmt_date instead of raw ISO. Both flags were from
the s13 sweep; both grounded before the ask: the defect lived
in _contact_detail (app_ui/server.py), the label data already
existed (fact_definitions.label, seeded), and run_ui_walk pins
neither (its bio.family_name asserts are db-level get_fact
calls, never page labels).

BUILD NOTE, method-relevant: the first cut put the label SELECT
inline in server.py and the no-logic lint FAILED the ui-walk
sweeps exactly as designed ("SQL outside reads.py",
server.py:437-438). Moved the query to reads.fact_labels();
sweeps green. METHOD: the lint guarded the frozen surface's
discipline against the very session authorized to touch it --
the guard earned its keep.

PROOF (scratch db, live render through the final code path):
contact with bio.family_name fact + one matter; page shows
"Family name" TRUE, raw key FALSE; Matters date MM/DD/YYYY
TRUE, ISO cell FALSE.

SUITES (all rerun after the reads.py refactor, quoted):
- casework-ui run_ui_walk.py: "ui-walk: 13 pass, 0 pending,
  0 fail; sweeps pass; verdict GREEN"
- drive_sheet.py: "drive-sheet: 27/27 groups pass; verdict
  GREEN"; check_sheet_labels.py: "92 labels checked, 0 not
  found" (no sheet change this item; lock stays 04f8db62ec6d)
- casework run_spine.py: "spine: 107 green, 0 red, 0 pending;
  checks pass"
- casework-billing run_billing.py: "billing: 25 green ...
  verdict: GREEN"; run_fiduciary.py --seeded: "fiduciary:
  9 pass, 0 red, 0 stub; verdict: GREEN"

SERVER: 8500 restarted (server.py is loaded code); same walked
db, not reseeded; PID 76416 -> 57812, single bind, HTTP 303.
Vera's contact page now shows human labels and MM/DD/YYYY.

## 2026-08-10 -- s15 cont: dashboard settling backing list BUILT
## (s11 flagged judgment call, James: "same ruling" as the client
## band's Collected listing)

RULING: James ruled BUILD, explicitly the same ruling as the s11
client-side twin (client_payments). The dashboard pipeline's
settling figure was the last figure on the "On the way" line
with no list behind it: one settling payment linked to its own
page, plural rendered unlinked text.

BUILT (all rendering-only):
- reads.settling_payments() gains contact columns (i.contact_id,
  c.display_name via JOIN contacts) -- same reader, same filter,
  one consumer before, two after.
- New screen settling_list at /billing/settling
  (app_ui/billing_ui.py, placed by client_payments): every
  processor-held payment firm-wide -- Date (links payment),
  Invoice (links), Client (links), Method, Amount; foot
  "Settling: $X" ties to the pipeline figure BY CONSTRUCTION
  (both sum reads.settling_payments); empty state explains the
  bucket's lifecycle; hint points at Run settlement on Trust
  accounting.
- Dashboard segment now ALWAYS links to /billing/settling; the
  flagged single-payment special case is retired.
- Router: literal GET ["billing","settling"] before the recon
  line; tier-3 fence untouched (path was unrouted -> 404
  before, route-listed now).

VERIFIER: step_settlement (run_billing_ui_walk.py) extended --
the settling moment now asserts FOUR surfaces before
extinguishing: pipeline dollars, invoice chip, payment chip,
and the new backing list (href asserted on the dashboard,
"Settling: $5,000.00" foot tie, T0001 row, method text).

SHEET: untouched -- the demo walk never visits the dashboard at
the settling moment. Lock stays 04f8db62ec6d.

SUITES (all rerun, quoted):
- run_billing_ui_walk.py: "billing-ui-walk: 20 pass, 0 pending,
  0 fail; float-sweep pass; verdict GREEN" (new asserts live)
- drive_sheet.py: "drive-sheet: 27/27 groups pass; verdict
  GREEN"; check_sheet_labels.py: "92 labels checked, 0 not
  found"
- casework-ui run_ui_walk.py: "ui-walk: 13 pass, 0 pending,
  0 fail; sweeps pass; verdict GREEN"
- casework run_spine.py: "spine: 107 green, 0 red, 0 pending;
  checks pass"
- casework-billing run_billing.py: "billing: 25 green ...
  verdict: GREEN"; run_fiduciary.py --seeded: "fiduciary:
  9 pass, 0 red, 0 stub; verdict: GREEN"

SERVER: 8500 restarted; same walked db, not reseeded; PID 57812
-> 50960, single bind, HTTP 303; /billing/settling answers 303
(auth redirect, not 404 -- route live). On the walked db
everything is settled, so the screen shows its empty state --
correct.

## 2026-08-10 -- s15 cont: gated item 3 DONE (empty invoice visible;
## James picked the rendering layer)

RULING: layer choice put to James per the gated ledger's unlock
condition; he chose (a) rendering-side, agreeing the core's
corpus-pinned derivation (paid at zero balance, fx-0070/0071)
is defensible bookkeeping and the lie was presentational.

GROUND-TRUTH CORRECTION recorded (evidence discipline, sources
disagree): gated-items.md and sheet step 11 both said a
chargeless bill is on NEITHER default tab. Executed probe
(scratch db, this session): it sat ON the Paid tab, count 1,
wearing a Paid pill -- absent only from Outstanding. Both
values recorded here; the sheet text was stale against the
product either way and is now superseded by the fix.

BUILT (rendering-only):
- reads.charged_invoice_ids(): invoice ids with >= 1 live
  charge, one query.
- billing_landing: bucket_of overlays status_of -- a chargeless
  invoice buckets to Outstanding regardless of derived status.
  Tabs, tab counts, the Outstanding tile count, and the shown
  filter all follow the bucket (tile count == tab count, the
  2026-08-07 tile/list contradiction cannot recur; empty rows
  add 0.00 to the tile sum). Row renders Empty pill (new
  .pill.empty, neutral gray family) + chipnote "no charges
  yet", balance 0.00, no overdue/sent chipnotes.
- Derived status untouched: invoice pages, client band, and
  core list_invoices still say paid-at-zero -- landing only.
  FLAG (new, unruled): the client money band's invoice rows
  and the invoice detail title still show a Paid pill on a
  chargeless invoice (same lie, other surfaces); candidate
  follow-up, not touched under this ruling.

SHEET: step 11's if-lost route now rides the DEFAULT tab
("row B0001, right on the default Outstanding tab -- a bill
with no charges yet sits there marked Empty until you charge
it"); the stale neither-tab justification for "Use All" is
gone. Steps 12/14 keep their All routes (still valid). Lock
re-synced 04f8db62ec6d -> 7b30fc89c159.

DRIVER: s11_add_charge now drives the new route -- lands on the
default landing, asserts the Empty pill and "no charges yet",
asserts the Paid tab does NOT claim B0001, then locates the row
tab-less. The drive's step-21 stray (chargeless by design) now
lives on Outstanding with the Empty marker; no locate ever
targeted it, so nothing else moved.

SUITES (all rerun, quoted): drive-sheet "27/27 groups pass;
verdict GREEN"; labels "92 checked, 0 not found";
billing-ui-walk "20 pass ... verdict GREEN"; ui-walk "13 pass
... sweeps pass; verdict GREEN"; spine "107 green"; billing
"25 green ... GREEN"; fiduciary --seeded "9 pass, 0 red,
0 stub; verdict: GREEN".

SERVER: 8500 restarted, same walked db (all its invoices are
charged, so no Empty rows show there -- correct); PID 50960 ->
70784, single bind, HTTP 303.

## 2026-08-10 -- s15 cont: gated item 5 DONE (demo-login prefill;
## James gated it in via the option prompt)

RULING: James gated item 5 IN ("Yes, build it"), shape as
proposed: prefill only when launched via billing-ui/serve.py,
which serves synthetic dbs exclusively; no core changes. (He
flagged mid-session that a long message buried the gate
question -- it was re-put as a bare option prompt. Interface
note: keep gate asks SHORT or use the option prompt.)

GROUND FINDING that shrank the item: the six-digit-code wall
never existed -- the /mfa screen already renders the current
code on every login (synthetic outbox shown on-page,
server.py _mfa_page). Item 5 reduced to login prefill alone;
the no-expiry half is moot (14-day sessions + a zero-typing
login) and stays untouched in core.

BUILT:
- serve.py: sets httpd.demo_prefill after make_server --
  demo.reviewer@synthetic.test / demo-seed-pass when --seeded,
  demo.driver@synthetic.test / demo-walk-pass otherwise (both
  pinned conventions: seed_demo.py and the sheet's setup step).
  New --no-prefill opt-out.
- casework-ui server.py _login_page (frozen surface, opened by
  this gate ruling): when the server object carries
  demo_prefill, the email and password fields render prefilled
  with a one-line hint ("Demo database: the seeded credentials
  are filled in -- click Continue"). Unset -- every other
  launcher, including every verifier's make_server -- renders
  the plain form, byte-identical to before.
- run_billing_ui_walk gains step 21 "demo-login prefill":
  asserts no leak without the flag, sets the attr, asserts both
  values + hint render, unsets, asserts it retires.

SHEET: untouched (the walk starts at /setup on a fresh db and
never sees the login screen); lock stays 7b30fc89c159.

SUITES (all rerun, quoted): billing-ui-walk "21 pass, 0
pending, 0 fail; float-sweep pass; verdict GREEN"; drive-sheet
"27/27 groups pass; verdict GREEN"; labels "92 checked, 0 not
found"; ui-walk "13 pass ... sweeps pass; verdict GREEN";
spine "107 green"; billing "25 green ... GREEN"; fiduciary
--seeded "9 pass, 0 red, 0 stub; verdict: GREEN".

SERVER: 8500 relaunched through serve.py (PID 70784 -> 46392,
single bind); LIVE PROOF quoted from the running server:
curl /login shows value='demo.driver@synthetic.test',
value='demo-walk-pass', "credentials are filled in". If
James's cookie ever dies, login is now zero typing.

## 2026-08-10 -- s15 cont: Paid-pill-on-chargeless flag closed
## (James: keep going)

FLAG CORRECTION first (evidence discipline): the s15 flag said
"invoice detail + client band" both showed Paid on a chargeless
invoice. Grounding found invoice detail ALREADY suppressed the
pill deliberately (in-code comment: "presenting that pill on an
empty bill is a lie of rendering, so no status pill until
charges exist"). Only the client money band actually lied. Flag
recorded as half-stale.

BUILT (rendering-only, both one-liners):
- _status_pill: derived paid + zero live charges now renders
  the Empty pill -- fixes the client money band, the one lying
  surface. Landing rows are unaffected (empty rows short-
  circuit before _status_pill).
- invoice_detail title: the deliberate no-pill state upgraded
  to the Empty pill -- since gated item 3 the truthful marker
  exists, so absence is no longer the best truth. All three
  surfaces (landing, detail, band) now say Empty with one
  vocabulary.

PROOF (scratch db, live render): chargeless bill -- detail
title Empty TRUE / Paid FALSE; client band Empty TRUE / Paid
FALSE.

SHEET: untouched (step 10's End pins the crumb only; no step
observes a pre-charge title pill). Lock stays 7b30fc89c159.

SUITES (all rerun, quoted): billing-ui-walk "21 pass ...
verdict GREEN"; drive-sheet "27/27 groups pass; verdict
GREEN"; labels "92 checked, 0 not found"; ui-walk "13 pass ...
sweeps pass; verdict GREEN"; spine "107 green"; billing "25
green ... GREEN"; fiduciary --seeded "9 pass, 0 red, 0 stub;
verdict: GREEN".

SERVER: 8500 restarted, same walked db; PID 46392 -> 57704,
single bind, HTTP 303.
