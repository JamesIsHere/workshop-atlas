# plan.md -- casework-billing (agent-owned strategy)

Drafted 2026-08-03 alongside the goal draft. Rewritten freely by the
agent; judged by results. Phase unit tables are drafted at each phase
gate for red-pen (MIXED mode), so later phases are deliberately
coarser here.

## Shape of the build

Oracle-first (op rule 7), ledger-first. The ledger schema is the one
retrofit-hostile artifact; everything else (invoices, payments, time)
is machinery that posts to it. Order:

    P0 oracle + schema -> P1 ledger core -> P2 invoice machinery ->
    P3 payments + processor sim -> P4 time, sharing, permissions ->
    P5 anchor walk + reconciliation + close

Casework's churn record supports this: phases stopped iterating once
the P0 schema anticipated the tables. Spend the paper-design budget on
P0.

## P0 -- oracle and schema (gate: James ratifies map + schema + F-list)

- billing-map.json: all 25 entries classed (direct/adapted/parked)
  with adapted wordings written out; every adapted entry cites what
  v1 proves instead. Candidates flagged for the gate, not decided
  silently.
- Ledger schema design ON PAPER first: chart of accounts, journal
  tables, sub-account tree, immutability triggers, posting API
  signatures, cleared-vs-posted status on trust postings, and the
  external event stream (red-pen r1: reconciliation substrate is P0
  schema scope, not P5). Then into gen_schema.py behind the gate.
- Fiduciary suite skeleton: F1-F8 as runnable checks against an empty
  ledger (vacuously green proves the harness runs, not the system).
- Parity test harness: test-per-entry scaffolding, casework pattern.
- Spine regression baseline: run ../casework spine suite BEFORE any
  billing change, capture the green report as the baseline artifact.

## P1 -- ledger core

Accounts CRUD (operating + unlimited trust accounts, Settings > Bank
Accounts parity), journal + postings with balance/overdraft/
segregation enforcement at posting time, client and matter trust
sub-accounts, earn-out transfer workflow, disbursements, trust ledger
three-tab data (firm/matter/client views with transaction drilldown),
audit + soft-delete wiring. F1-F5, F8 go green on seeded data here.

### P1 unit table (DRAFT for phase gate -- red-pen target)

| Unit | Deliverable                                              |
| ---- | -------------------------------------------------------- |
| U1.1 | Posting engine: app/ledger.py -- bank account CRUD,      |
|      | client/matter sub-account auto-provisioning, post() over |
|      | the closed recipe vocabulary with balance assertion and  |
|      | F3/F4 blocking BEFORE write, F5 recipe conformance,      |
|      | reverse_entry() with link columns, external-event        |
|      | co-writes on bank-visible recipes. Engine unit tests     |
|      | authored first (blocks fire, recipes post, reversal      |
|      | chains link); churn counter per test                     |
| U1.2 | Seed extension: gen_seed.py gains a deterministic        |
|      | billing scenario (accounts, deposits, earn-outs,         |
|      | disbursements, matching external events, SYNTHETIC       |
|      | markers). Fiduciary suite green on the seeded db         |
|      | (F1-F6 + F8; F7 stays stub). seed.sql sha recorded       |
| U1.3 | Trust surfaces, tests-first: billing module routes       |
|      | (module-exists), Settings > Bank Accounts parity         |
|      | (trust-bank-accounts), three-tab ledger + drilldown +    |
|      | filters (trust-ledger), client/matter Trust Acct tab +   |
|      | Disburse Funds (trust-disbursements). 4 map entries      |
|      | green at unit close                                      |
| U1.4 | Phase close: fiduciary-report captured, spine regression |
|      | run vs baseline (107 green) captured, churn log,         |
|      | worklog/state wind-down                                  |

P1 parity targets: 4 of 25 entries (module-exists,
trust-bank-accounts, trust-ledger, trust-disbursements). Remaining
21 land P2-P4 per phase roster; trust-requests needs invoice
machinery and is P2.

## P2 -- invoice machinery

Bills and Trust Requests, invoice builder (charges, per-invoice
settings, discounts, due dates, footer/branding fields), saved
charges, global vs per-client numbering, automatic late fees (via
scheduler tick), default invoice settings, invoice PDF render,
Spanish translation hook, paid-tab transition at zero balance.

### P2 unit table (DRAFT for phase gate -- red-pen target)

| Unit | Deliverable                                              |
| ---- | -------------------------------------------------------- |
| U2.1 | Invoice core (app/billing.py): create Bill/Trust Request |
|      | with client + optional matter + recipient contact,       |
|      | builder data ops (charges CRUD, per-invoice settings,    |
|      | discounts, issued/due dates), numbering (per-client      |
|      | default, global toggle with configurable start,          |
|      | no-renumbering rule), derived balance + Paid transition  |
|      | at zero. Tests-first. Entries green: invoice-creation,   |
|      | global-invoice-numbering                                 |
| U2.2 | Firm settings + scheduled charges: saved charges         |
|      | (bills-only import rule), Settings > Invoice Settings    |
|      | defaults (overridable per invoice, apply-forward rule),  |
|      | automatic late fees on the scheduler tick (fixed or      |
|      | percent, optional recurring). Entries green:             |
|      | saved-charges, default-invoice-settings,                 |
|      | automatic-late-fees                                      |
| U2.3 | Render + facade: invoice PDF via casework render         |
|      | machinery, Spanish translation (template chrome only,    |
|      | fx-0052 exclusions asserted untranslated), billing.py    |
|      | module facade -- the deferred module-exists entry greens |
|      | here once both function families exist. Entries green:   |
|      | invoice-translation, module-exists (P1 deviation         |
|      | resolved)                                                |
| U2.4 | Phase close: billing/fiduciary/spine runs captured,      |
|      | churn log, wind-down                                     |
|      |                                                          |

P2 parity targets: 7 entries -> running total 10 of 25.
trust-requests moved to P3 by design: its criterion requires
recording a payment, which is payment machinery; greening it in P2
would smuggle half of P3 forward.

## P3 -- payments and processor simulation

Direct payment recording, trust-transfer payment, payment editing as
reversal+repost, refunds (full-amount, corpus parity), payment-charge
association, SimProcessor (card/eCheck, fee schedule, gross-vs-net,
chargeback), shared-invoice pay page (localhost HTTP), payment plans
(installment schedule + reminders + simulated auto-pay), receipts
setting. F6 goes green here.

### P3 unit table (DRAFT for phase gate -- red-pen target)

| Unit | Deliverable                                              |
| ---- | -------------------------------------------------------- |
| U3.1 | Payment recording core: invoice_payments as the UX       |
|      | object wired to ledger recipes -- direct payment on a    |
|      | bill (operating + fee income) and on a trust request     |
|      | (trust deposit at the chosen level); trust-transfer      |
|      | payment (bill paid from client/matter funds = the        |
|      | earn_out recipe, available amount shown); association    |
|      | to one specific charge (fx-0057, one charge max).        |
|      | Entries green: direct-payment-recording, trust-requests, |
|      | trust-transfer-payment, payment-charge-association       |
| U3.2 | Corrections: payment edit = row UPDATE + journal         |
|      | reversal/repost underneath (r2 two-layer); refund =      |
|      | full-amount toggle with note, reversal underneath.       |
|      | Entries green: payment-editing, payment-refunds          |
| U3.3 | SimProcessor: FeeSplitProcessor interface + sim          |
|      | (card/eCheck on SYNTHETIC- tokens, 3% + 30c, settlement  |
|      | batches gross-to-trust / fees-to-operating, chargeback   |
|      | event per r3 boundary), share-token pay page over        |
|      | localhost HTTP (share MACHINERY only -- the email        |
|      | sharing criterion stays P4), auto-receipt setting.       |
|      | Fiduciary F6 linkage assertion deepened here. Entry      |
|      | green: online-card-payment                               |
| U3.4 | Payment plans: installment schedule from attested fields |
|      | (r4 boundary), 7-before/due/7-after reminders on the     |
|      | tick via email_outbox, auto-charge composing SimProc +   |
|      | posting recipes. Entry green: payment-plans              |
| U3.5 | Phase close: full battery captured, churn log, wind-down |

P3 parity targets: 8 entries -> running total 18 of 25. P4 keeps:
sharing family (3), time tracking (2), permissions (1), bulk
download (1). Carried flag from P2: the fpdf2-instead-of-render.py
deviation (worklog) is before this gate for acknowledgment.

## P4 -- time tracking, sharing, permissions

Time entries (timer + manual, duration parsing per fx-0064 formats),
per-user rates and invoice import (decision default 4), invoice
sharing by email with reminders, bulk share (both modes) and bulk
download (zip), invoice access permission levels, CSV exports
extended.

### P4 unit table (DRAFT for phase gate -- red-pen target)

| Unit | Deliverable                                              |
| ---- | -------------------------------------------------------- |
| U4.1 | Time tracking (app/timekeeping.py): manual entries +     |
|      | timer (start/stop/resume), duration parsing (2h, 36m,    |
|      | 2.8h, 5.5m per fx-0064), contact/matter/firm-wide entry  |
|      | lists with filters; per-user default hourly rate in      |
|      | user_settings + per-entry override (decision default 4); |
|      | invoice import -> Professional Services charges at       |
|      | duration x rate, half-up cents. Entries green:           |
|      | time-tracking, time-entry-invoice-import                 |
| U4.2 | Sharing: share by email (recipient need not be the       |
|      | matter's primary contact, confirmation of contact info,  |
|      | link to view/download -- rides P3 share tokens +         |
|      | email_outbox), recurring reminders until zero balance    |
|      | with stop-at-zero, firm default reminder frequency.      |
|      | Bulk share both modes (zip-to-one-contact /              |
|      | each-to-own) + bulk download zip (stdlib zipfile).       |
|      | Entries green: invoice-sharing, payment-reminders,       |
|      | bulk-invoice-sharing, bulk-invoice-download              |
| U4.3 | Invoice access permissions: three levels (unlimited /    |
|      | limited: no edit-delete of others' invoices / none) on   |
|      | casework's permission machinery. Entry green:            |
|      | invoice-access-permissions                               |
| U4.4 | CSV exports extended (invoices, payments, time entries,  |
|      | trust ledger -- anti-lock-in commitment, goal.md         |
|      | supporting check) + phase close battery + wind-down      |

P4 parity targets: 7 entries -> running total 25 of 25 (parity
COMPLETE). P5 remains: bank-statement generator + three-way recon
(F7 goes live), anchor billing walk, x2 byte-identical closes,
self-audit, result.md.

## P5 -- anchor walk and close

Synthetic bank-statement generator + three-way reconciliation report
(F7 green), anchor billing workflow script (verifier 3), full x2
byte-identical runs of verifiers 1 and 2, spine regression capture,
self-audit, result.md.

## Standing mechanics

- Every unit closes with evidence on disk (compaction-ready).
- Spine regression runs at every phase gate minimum; any red is a
  full stop for the phase, not a note.
- Churn counter per unit (red test iterations + posting-API rejection
  reasons) logged at unit close.
- Log-don't-build: scope temptations land in the worklog at the
  moment the sentence "out of scope" is first written anywhere.
