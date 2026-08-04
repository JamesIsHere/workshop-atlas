# Ledger design (P0 paper design -- for gate ratification)

Drafted 2026-08-03. This document + ledger-schema-draft.sql + the
F-check list in goal.md + billing-map.json are what the P0 gate
ratifies together. Nothing here touches ../casework/ until the gate
passes; the draft DDL then enters gen_schema.py verbatim-modulo-
mechanical-merge.

## 1. Account model: trust funds are LIABILITIES

The load-bearing design decision. A trust bank account is an ASSET
(the firm holds the money); the clients' claims on that money are
LIABILITIES (the firm owes it). Every client/matter sub-ledger is a
liability sub-account under its trust bank account's client-funds
control. Fiduciary correctness then falls out of double-entry
identities instead of application discipline:

    trust_bank asset balance == sum of client-funds liability
    balances under it                      (F2, per trust account)

Account kinds (ledger_accounts.kind):

| Kind                  | Type      | Purpose                        |
| --------------------- | --------- | ------------------------------ |
| operating_bank        | asset     | firm operating account         |
| trust_bank            | asset     | one per real trust account     |
|                       |           | (unlimited, corpus parity)     |
| client_trust          | liability | client-level funds, child of a |
|                       |           | trust_bank                     |
| matter_trust          | liability | matter-level funds, child of a |
|                       |           | client_trust                   |
| fee_income            | income    | earned fees                    |
| processor_fee_expense | expense   | processor fees (fee-split)     |
| chargeback_expense    | expense   | chargeback clawbacks (r3: the  |
|                       |           | firm eats the receivable)      |

Postings land on LEAF accounts only (client_trust when funds are
held at client level, matter_trust at matter level; the corpus
attests both levels). Control balances are derived sums, never
posted. "Settings > Bank Accounts" parity is CRUD over
operating_bank / trust_bank rows.

## 2. Journal: append-only, one clearing exception

journal_entries (kind, links, reversal chain) + journal_postings
(entry, account, side, amount_cents). Immutability is SCHEMA-
enforced, not convention:

- BEFORE UPDATE / BEFORE DELETE triggers on journal_entries RAISE.
- BEFORE DELETE on journal_postings RAISES. BEFORE UPDATE RAISES
  unless the ONLY change is cleared_at/statement_ref moving from
  NULL to a value (the bank-witness annotation, r1 first-schema
  ruling). A cleared posting can never be re-cleared or un-cleared.
- Corrections: reverse_entry() posts the mirror entry with
  reverses_entry_id set; a corrected version posts fresh with
  replaces_entry_id set. UI "edit payment" = update the payment ROW
  (ordinary audited mutation) + reversal/repost underneath (r2).
- amount_cents INTEGER CHECK (amount_cents > 0); side is
  debit/credit. No floats anywhere (goal.md constraint; the float
  sweep enforces).

## 3. External event stream (F7 independence substrate)

external_events is the record of externally-visible money facts:
deposit received, check cut, processor settlement batch, processor
chargeback. Append-only like the journal. The bank-statement
generator reads ONLY this table plus the clearing-lag model (checks
clear N days after cut, deposits settle T+2, processor batches on a
batch calendar) -- it never reads the journal (F7 independence
clause). Posting recipes and event writes happen together in the
posting API, so book and bank are two pipelines from one action.

## 4. Posting recipes (the complete money vocabulary)

Every money movement in the system is one of these balanced
recipes. The posting API exposes exactly these; there is no
free-form posting endpoint.

| Recipe                  | Legs                                     |
| ----------------------- | ---------------------------------------- |
| trust_deposit           | DR trust_bank / CR client_trust (or      |
|                         | matter_trust); event: deposit            |
| bill_direct_payment     | DR operating_bank / CR fee_income;       |
|                         | event: deposit                           |
| trust_request_payment   | = trust_deposit (a trust request funds   |
| (direct)                | the sub-ledger, it earns nothing)        |
| earn_out (pay bill from | 4 legs: DR client_trust, CR trust_bank,  |
| trust = trust transfer) | DR operating_bank, CR fee_income;        |
|                         | events: check_cut (trust side) +         |
|                         | deposit (operating side)                 |
| disbursement            | DR client_trust (or matter), CR          |
|                         | trust_bank; event: check_cut             |
| sim_settlement, gross   | DR trust_bank gross / CR client_trust    |
| mode (trust request)    | gross; then DR processor_fee_expense /   |
|                         | CR operating_bank fee; events:           |
|                         | processor batch (gross to trust bank,    |
|                         | fee against operating) (F6)              |
| sim_settlement, net     | forbidden for trust requests (F6: fees   |
| mode                    | never netted from trust); allowed for    |
|                         | bills into operating                     |
| late_fee                | no cash legs -- an invoice CHARGE, not a |
|                         | posting; money moves only when paid      |
| chargeback              | DR chargeback_expense / CR               |
|                         | operating_bank; event: chargeback.       |
|                         | NEVER touches trust (r3)                 |
| refund (direct payment) | reversal of the original entry (r2:      |
|                         | full-amount only, corpus parity)         |

## 5. Enforcement matrix (where each invariant lives)

| Invariant             | Posting API | Schema triggers | Verify sweep |
| --------------------- | ----------- | --------------- | ------------ |
| F1 balanced entries   | yes         | -               | F1           |
| F2 control identity   | by shape    | -               | F2           |
| F3 no negative sub    | yes (block) | -               | F3 replay    |
| F4 funds availability | yes (block) | -               | F4 replay    |
| F5 segregation        | recipes only| -               | F5           |
| F6 gross-vs-net       | recipes only| -               | F6           |
| F7 three-way recon    | -           | -               | F7 engine    |
| F8 immutability       | -           | yes (RAISE)     | F8 audit     |
|                       |             |                 | sweep        |
| integer cents         | yes         | CHECK > 0       | float sweep  |

Posting-time blocks (F3/F4) raise before write; the verify-time
replay re-derives running balances in posting order and asserts the
blocks never lied.

## 6. Invoicing tables (parity machinery over the ledger)

- invoices: invoice_type bill|trust_request, contact, optional
  matter, recipient_contact (fx-0068 third-party receiver), trust
  level + destination for trust requests, numbering (per-client or
  global scope, fx-0076), issued/due dates, preparer, discount,
  footer/color/language, late-fee config, reminder config.
  Tombstoned. "Paid tab at zero balance" is DERIVED from charges
  minus payments -- never a stored status column (single-fact-store
  discipline).
- invoice_charges: service|expense, description, amount_cents,
  date, optional matter, source (manual|saved|time|late_fee),
  optional time_entry link. Tombstoned.
- saved_charges: firm-level, bills-only enforced at import
  (fx-0059).
- invoice_payments: the UX object (r2 two-layer design): method
  direct|trust_transfer|sim_card|sim_echeck, amount, date,
  destination account, trust source (level + account) for
  transfers, optional associated charge (fx-0057, one charge max),
  refunded flag + note, current journal_entry_id. Edits UPDATE this
  row (audited) and swap the journal entry via reversal+repost.
- payment_plans + plan_installments: frequency_days, installment
  amount, start date, auto_charge, accepted forms (r4 attested-
  fields boundary); installments carry the three reminder stamps
  (7-before, due, 7-after) and payment link.
- invoice_shares: email-only channel, share token for the
  view/download/pay page, reminder config, last_reminder_at.
- time_entries: user, contact-or-matter (CHECK at least one),
  date, duration_seconds, optional rate override; billed = link
  from the created invoice_charge. Timer = timer_started_at on an
  open entry.
- processor_transactions + settlement_batches: SimProcessor's
  deterministic record; tokens carry a SYNTHETIC- prefix enforced
  by CHECK (synthetic-data guard extension).

Firm-level invoice settings (numbering mode + next number, default
late fee, reminder days, auto due dates, default preparer, receipt
auto-send, header display, color, footer) ride the existing
firm_settings key-value table. Per-user hourly rate rides
user_settings. Invoice access levels (fx-0075: unlimited / limited
/ none) ride the existing user-permissions machinery; exact
encoding is a P1 detail against casework's permission tables.

## 7. What the gate is ratifying

1. The liability account model (section 1) -- the one decision that
   is expensive to change after postings exist.
2. Append-only journal with the single clearing-annotation
   exception (section 2).
3. The external event stream + independence architecture (section 3).
4. The closed recipe vocabulary (section 4) -- adding a recipe
   post-gate is allowed (additive); changing legs of an existing
   recipe after postings exist is Approval-required.
5. The enforcement matrix (section 5).
6. billing-map.json classes and adapted wordings (25 entries:
   21 direct, 4 adapted, 0 parked).
7. The F1-F8 check list as written in goal.md verifier 2.
