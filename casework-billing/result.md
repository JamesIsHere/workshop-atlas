# result.md -- casework-billing

Written 2026-08-03, after all verifiers passed (goal.md: this file
exists only past that bar). Contract: goal.md, RATIFIED 2026-08-03.

## Outcome

The casework core carries a running invoicing and trust accounting
layer, COMPLETE per the ratified contract: capability parity on all
25 corpus entries of invoicing-and-trust-accounting, PLUS the
fiduciary invariant suite F1-F8 -- the bar Docketwise's public
surface never attests (double-entry integrity, overdraft blocking,
segregation, gross-vs-net fee splitting, three-way reconciliation,
journal immutability) -- both gating, both green.

## Verifier 1 -- billing parity suite (mechanical)

    billing: 25 green, 0 red, 0 pending, 0 parked; checks pass;
    verdict: GREEN, exit 0

- 25 entries = 21 direct + 4 adapted (SimProcessor for LawPay,
  email-only sharing, shared-link for portal paths, bounded payment
  plans), 0 parked. No entry silently dropped.
- Run x2 on 2026-08-03: reports byte-identical, sha256 acba95b1...
- Supporting checks: csv-export round-trip (invoices, payments,
  time entries, trust ledger) and float sweep (no REAL columns, no
  float() on cents paths). All pass.

## Verifier 2 -- fiduciary invariant suite (mechanical, ours)

    fiduciary: 8 pass, 0 red, 0 stub; verdict: GREEN, exit 0

- F1 balance, F2 control identity, F3 point-in-time no-overdraft,
  F4 funds availability, F5 recipe segregation, F6 gross-vs-net
  with settlement-linkage assertion, F7 three-way reconciliation
  (LIVE: independent statement generator reading only external
  events through a clearing-lag model; 6 genuine reconciling items
  enumerated at the mid-lag period; identity holds at both period
  ends), F8 immutability (schema triggers probed under direct
  attack + audit sweep).
- Run x2 on 2026-08-03: reports byte-identical, sha256 af2e242f...
- Oracle calibration on record (P0): every check was deliberately
  driven RED by a broken scenario before any feature existed.

## Verifier 3 -- anchor billing workflow (live)

    anchor-billing: PASS (1.336s of 900s budget)

Twelve-step scripted cold-start walk on a FRESH database: install
-> admin -> contact + matter -> trust and operating accounts ->
direct-paid consult funding operating -> Trust Request paid by the
client over real localhost HTTP against the SimProcessor ->
settlement posting GROSS 5,000.00 to trust with the 150.30 fee
pulled from operating -> Bill (saved charge + imported 2h time
entry) paid by trust-transfer earn-out -> 1,200.00 disbursement ->
invoice PDF read back -> three-way reconciliation HOLDS for both
banks at two period ends (recon-report.txt) -> audit continuity
across system/user/contact actors -> fiduciary suite GREEN on the
walked database.

## Spine regression (standing gate)

    spine: 107 green, 0 red, 0 pending; checks pass

Report diff-identical to the pre-billing baseline captured before
any billing work (verify/spine-baseline.txt == regression-report.txt).
The casework core is provably unbroken by the billing build.

## Beyond-parity scope delivered (sourced to the 2026-08-01 flag)

- Trust funds as liabilities: client/matter sub-ledgers are
  credit-normal accounts under the trust bank control; the F2
  identity is double-entry arithmetic, not application discipline.
- Append-only journal, corrections by reversal (UI edit =
  reversal+repost under the hood); one schema-level clearing
  annotation exception, one-shot, audited.
- Earn-out transfer as a first-class 4-leg atomic recipe.
- Chargebacks as posting events debiting OPERATING only (client A's
  chargeback can never touch client B's funds); no dispute workflow
  by ruling (r3).
- Gross-vs-net settlement awareness: net-to-trust is structurally
  unrepresentable; F6 asserts event linkage.

## Known boundaries (disclosed, deliberate)

- SimProcessor only; real fee-split processor integration is
  post-v1 and Approval-required. No real money can move.
- posted_at carries the business date; wall-clock truth lives in
  audit_log (worklog P1 design note; revisit only if it costs).
- Auto-charge uses deterministic SYNTHETIC-AUTOPAY tokens; a stored
  payment-method column would be a schema change (Approval-required).
- Invoice PDFs use fpdf2, not casework's AcroForm render machinery
  (acknowledged deviation, P3 gate).
- Firm-side surface is module-level, casework precedent; HTTP
  exists exactly where criteria demanded a client actor
  (shared-invoice view/download/pay).

## Completion proof (paths)

| Path                              | State                          |
| --------------------------------- | ------------------------------ |
| billing-map.json                  | 25 entries classed, all green  |
| verify/billing-report.txt         | GREEN exit-0 x2, acba95b1..    |
| verify/fiduciary-report.txt       | GREEN exit-0 x2, af2e242f..    |
| verify/anchor-billing-report.txt  | PASS with per-step timings     |
| verify/recon-report.txt           | identity HOLDS, items          |
|                                   | enumerated                     |
| verify/regression-report.txt      | spine 107 green == baseline    |
| tests/ + billing modules in       | 4 app modules (ledger,         |
| ../casework/app/                  | billing, processor,            |
|                                   | timekeeping), 4 test files     |
| ../casework/CLAUDE.md             | reciprocal guard delivered     |
| result.md                         | this file                      |

## What this build is not (post-v1 pointers)

- No real processor, no real bank, no real money -- by contract.
- No dispute/chargeback workflow (r3 fence).
- No QuickBooks sync (integrations module, deferred).
- Trust-side UI is data-level; a firm UI phase remains casework-ui
  territory (ON HOLD, untouched).
