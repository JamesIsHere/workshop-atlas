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

METHOD: hybrid mode s3 tally -- three phases built unattended,
three gates closed on decks, zero kills total. Either the
demo-grade calibration from gate 1 held, or the deck medium
under-surfaces kills relative to hands-on (the intake finding
came from hands, not decks). Walk day discriminates: if P4
surfaces shape problems the decks passed, weight future gate
reviews back toward hands-on.
