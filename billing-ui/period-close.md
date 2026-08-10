# period-close.md -- item-12 period-close act design (RATIFIED 2026-08-09)

Created 2026-08-09 s12 during the period-close design gate. Numbered
elements; James marks by number. Rulings recorded here AND in worklog
s12. Precedent: status-page.md (s10), invoice-codes.md (s8).

Rulings signed in conversation BEFORE this sheet (2026-08-09):

- PC1 HARD CLOSE: closing a month locks it -- the engine refuses any
  posting dated into a closed month; late-arriving facts post
  current-dated into the open month. A closed month's numbers are
  permanently citable. (Soft attestation rejected: it lets the one
  number a firm cites to a bar auditor drift after signing.)
- PC2 TWO-STEP, SAME PERSON ALLOWED AND SHOWN: prepare -> approve as
  distinct recorded acts with recorded signers. One person may sign
  both; the close record then shows that visibly. The control exists
  structurally; real segregation arrives with the future role
  contract, no redesign needed.
- PC3 TIE REQUIRED, EXCEPTIONS CARRIED EXPLICITLY: the three-way
  reconciliation must HOLD for every bank account before close is
  possible; unresolved reconciling items are carried into the close,
  each individually acknowledged by the preparer and listed on the
  close record, visible until cleared in a later month.

Standing rulings inherited: R1 (humans own exceptions and period
close); audience/build-order rulings (s11): owner-sees-all with an
audience tag; SoD asked at design time -- answered here by PC2.

## The sketch

```
CLOSE JULY 2026                              status: OPEN
Step 1 Prepare (not yet run)   Step 2 Approve (waiting on prepare)

THE TIE  (each account must hold to prepare)
  Trust (IOLTA)  bank 5,000.00 + in transit 5,000.00
                 - outstanding 1,200.00 = book 8,800.00
                 = client claims 8,800.00              HOLDS
  Operating      bank 3,349.70 ... = book 3,349.70     HOLDS
  (a BROKEN account blocks close; link to Reconcile)

CARRIED ITEMS  (acknowledge each to prepare)
  [ ] deposit in transit       5,000.00   07/30   e2
  [ ] outstanding check        1,200.00   07/28   e5
  [ ] correction awaiting bank   300.00   07/22   e9
  (empty state: "Nothing carried. The month is clean.")

THE MONTH
  Billed 2,500.00 | Collected 3,000.00 | Into trust 5,800.00
  Out of trust 1,200.00 | Earned from trust 800.00

WHO IS WAY BEHIND            (outstanding, worst first)
  Ana Vera        1,500.00 overdue    oldest 45 days
WHO KEEPS US IN CASH         (collected, trailing 3 months)
  Baltic Shipping 9,000.00   60% of collections

[Prepare close]   then   [Approve close]
  prepared by <user> on <date> / approved by <user> on <date>
  (same signer on both steps: shown on the record)

CLOSED MONTHS
  June 2026   closed 07/02  prepared X  approved Y   -> record
```

## Numbered elements (mark by number)

 1. ROUTE + PLACEMENT (proposed -- nothing exists yet): build the
    close page at /billing/close. Verified this session: no such
    route exists in billing_ui.py's /billing/* inventory, and
    server.py:165-169 dispatches every /billing/* path to
    billing_ui.route, so the route lands in the existing hook.
    Entry points: the dashboard's period line -- which today renders
    "Period August 2026 -- ties as of 08/08/2026" (billing_ui.py
    1400-1403) -- gains a link (additive element on the frozen
    dashboard, s11 matter/contact precedent), plus a link in the
    /billing action row. The closed-month record page is proposed
    at /billing/close/<YYYY-MM>.
 2. CLOSE UNIT + ORDER: the unit is the calendar month; months close
    in strict chronological order; the closable month is the
    earliest month carrying any money fact (journal entry, external
    event, invoice, payment) not yet closed. No skipping.
 3. THE TIE: three_way() per bank account at the month's last day,
    rendered as the recon page renders it. Every account must show
    HOLDS to enable prepare (PC3's mechanical half). A BROKEN
    account shows the break and links to the Reconcile page; the
    close waits.
 4. CARRIED ITEMS: the recon engine's caused items (deposit in
    transit, outstanding disbursement, correction/refund awaiting
    bank) listed with cause, amount, date, entry link. The preparer
    acknowledges each one to proceed (PC3's judgment half). Carried
    items print on the close record and reappear on later closes
    until the bank clears them.
 5. THE MONTH: five story figures, all SELECT-only -- Billed
    (invoices.issued_date in month), Collected
    (invoice_payments.payment_date in month), Into trust / Out of
    trust / Earned from trust (journal entries by recipe kind,
    posted_at in month).
 6. RANKINGS (the deferred firm-wide rollups land HERE, not the
    dashboard): WAY BEHIND ranks clients by outstanding invoice
    balance with age of oldest unpaid bill (issued_date/due_date);
    KEEPS US IN CASH ranks clients by collections over the trailing
    three months with share of total. Rollups across the s11 client
    Money bands, firm-wide.
 7. TWO-STEP ACT (PC2 mechanics): PREPARE recomputes everything,
    stores a snapshot (figures, ties, carried items, and
    acknowledgments) signed by the preparer. APPROVE recomputes live
    and compares against the snapshot -- any drift (a posting landed
    mid-review) VOIDS the prepare with "stale, re-prepare"; a clean
    match locks the month, signed by the approver. Both signers on
    the record; same-person shown per PC2.
 8. THE LOCK (PC1 mechanics): enforcement in casework/app at the two
    write choke points -- ledger._post refuses journal entries with
    posted_at in a closed month (reversals included: correcting a
    closed month posts current-dated), and create_external_event
    refuses occurred_on in a closed month (the bank statement of a
    closed month is frozen; a late bank fact is entered on the date
    the bank showed it).
 9. LOCK SCOPE (FLAGGED judgment call): invoices.issued_date,
    invoice_payments.payment_date, and time_entries.entry_date are
    NOT locked in v1. The citable fiduciary facts are the ledger and
    the bank record (element 8); a backdated invoice would drift the
    element-5 story figures but never the tie. Extending the lock to
    billing documents is a later decision, not folded in silently.
10. NO REOPEN (FLAGGED default): a closed month never reopens.
    Errors discovered later correct current-dated in the open month,
    which the append-only ledger and the recon's correction causes
    already model. (A reopen affordance would make PC1 a soft close
    in disguise.)
11. CLOSE RECORD (proposed): /billing/close/<YYYY-MM> will render
    the stored snapshot -- the immutable meeting artifact: ties, carried items
    with acknowledgments, story figures, rankings, both signatures.
    This page is the "monthly meeting" leave-behind.
12. AUDIENCE TAG: finance seat prepares and consumes; approve is the
    owner/managing-partner seat by intent. Unenforced for now per
    the s11 build-order ruling (owner-sees-all).

## New core logic -- program amendment required (draft scope)

The write path does not exist and billing-ui owns rendering only.
Drafted for ratification alongside this sheet, same shape as the F7
amendment (2026-08-04):

- Authorized surface: new module casework/app/period.py (prepare,
  approve, period_is_closed, close queries); a lock guard called
  from ledger._post and ledger.create_external_event; schema
  addition via casework/app/schema/gen_schema.py -- proposed table
  period_closes (period 'YYYY-MM' unique, status
  prepared|closed|void, prepared_by/at, approved_by/at, snapshot
  JSON, canonical serialization); new tests in casework-billing.
- Hard limits: spine tests immutable; fiduciary checks may
  STRENGTHEN only (new scenario: posting dated into a closed month
  must raise; reversal of a closed-month entry must post
  current-dated); after the work ALL standing suites rerun green
  and quoted; sha supersessions via report_sha.py only, recorded in
  billing-ui's worklog.

## Verifier plan (this child's own coverage)

- Walk grows a close act: visit /billing/close, prepare, approve,
  view the record page (step count grows; sheet-lock re-sync rules
  apply if any pinned label is touched -- none is expected).
- The no-logic lint continues to bind app_ui: the close page renders
  period.py results; SQL stays in reads.py / period.py.

## Explicitly OUT of v1 (queued decisions, do not fold in)

- Role enforcement on prepare vs approve (future role contract).
- Lock on billing documents (element 9 flag).
- Reopen (element 10 flag -- deliberately absent, not deferred).
- Client portal (gated item 11), untouched.

## Ratification

SHEET SIGNED by James 2026-08-09 s12 ("The sheet looks good as
drafted") -- all twelve elements stand, flags 9 and 10 accepted as
flagged, and the program amendment below the elements is ratified
with the sheet. One red-pen round before signing: element 1 was
corrected from present-tense fact to proposal phrasing with
verified ground facts (route free, dispatch hook, real period-line
text) after James hunted for a page that existed only on paper.
Build authorized under the amendment's scope and hard limits.
