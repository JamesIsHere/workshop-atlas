# state.md -- billing-ui (session cache, overwritten each wind-down)

## Status

P4 OPEN after attempt 3 (verdict FAIL a/b/c, 2026-08-07) -- but
s7 (2026-08-07, same day) closed the ENTIRE unlocked backlog
A-I plus two James-authorized core break-ins. The product
attempt 4 will run on is materially different from attempt 3's:

- A: dates MM/DD/YYYY everywhere user-facing (screens, sheet
  typed values, PDF); data stays ISO; drive_sheet scans every
  billing page for ISO strays.
- Break-in 1 (PDF): invoice_pdf rebuilt -- MM/DD/YYYY, footed
  Description|Date|Amount columns, integer-cents (float
  division removed).
- Landing cleanup (his snap): tab counts Outstanding(0)/
  Paid(4)/All(4), tab-aware empty states, underline tabs.
- Back to billing button on Trust accounting / Time / Saved
  charges / Recon (his snaps).
- B: sheet identifies invoices by TYPE + issue date, never
  number; drive locates rows the sheet's way AND permanently
  injects a stray invoice after step 21 (attempt-3 regression).
- Invoice display codes DESIGNED + ratified in conversation:
  B0001/T0001, spec in invoice-codes.md; BUILD is gated-items
  locked item 10 (core schema break-in, awaits his gate).
- C: imported saved charges dated with the bill's issue date
  (existing core APIs only). D: bare "2" = hours (UI-side).
- E: seven blank select options re-worded to plain guidance
  (agent wording, FLAGGED for his re-rule).
- F: known-payee datalist on disburse. G: client link in a
  readonly copy box; sheet step 15 teaches Ctrl+A/Ctrl+C.
- H + break-in 2: "Client funds in trust" on invoice pages and
  the PDF (both languages). INCIDENT: first cut guessed
  m.contact_id (real: primary_contact_id); suites failed loud;
  ground-read fixed. Logged as Evidence Discipline repeat.
- I: both snap labels closed by James (label 1 not a problem;
  label 2 was the number-shift defect item B killed).

All suites green at close: spine 107; billing 25; fiduciary
--seeded 8; anchor-billing PASS; drive-sheet 24/24; billing-ui
walk 17/17 x2; labels 82/0; ui-walk 13.

## Next actions (James's stated order)

1. DRAFT the client-pay-page program-ruling amendment for his
   ratification (he said "then we draft" at context reset).
   Scope agreed in conversation: rendering-only in casework/
   app/server.py client surface -- styles, firm identity, real
   charge table with integer cents (two float divisions live
   there now, lines ~145/163), styled pay form, a receipt worth
   the name. Spine immutable; sheet's quoted client-side labels
   ("Synthetic payment token", "SYNTHETIC-VISA-DEMO", "Pay",
   "Payment received") preserved or re-pinned.
2. Held recon pair (gated item 1): fabricated correction
   events vs real-bank matching; demo period-end placement.
3. Invoice-code build gate (item 10, invoice-codes.md).
4. Attempt 4: fresh db, full walk, his verdict.

## Watch items and caveats

- SHEET LOCK current sha 2c9cac5141af; walk-report canonical
  sha f3f16120 (superseded a506f085 -> de589cbd -> d9074178 ->
  c4555b15 -> f3f16120 across s7, each PDF/report growth
  quoted in worklog). ONLY report_sha.py output counts.
- Server RUNNING on 8500, walked attempt-3 db (casework-ui/
  data/demo-walk-2026-08-07c.db), full s7 batch loaded. Login
  demo.driver@synthetic.test / demo-walk-pass, code on screen.
  Restart after ANY app_ui or casework/app change -- stale
  module code serves silently (bitten twice in s7).
- billing + fiduciary + anchor-billing run from
  ../casework-billing/; spine from ../casework/; core touches
  trigger the reciprocal guard (ALL suites).
- Walk dbs retained (delete=archive): -04, -04b, -07, -07b,
  -07c. Attempt-3 snaps archived in walk-artifacts/.
- atlas/gated-items.md is current as of s7 close (A-I marked
  DONE/CLOSED, item 10 added).
- Anti-stall ledgers: P2 1/2, P3 0/2, F-1 1/2 used. Firm
  question still unasked: flat-fee vs hourly mix.

## Interface rulings (2026-08-04, all standing)

- PRODUCT + ONE plain-language question per touchpoint; the
  question is the LAST sentence; translate jargon inline;
  re-issue the plain map at every gate and on demand.
- ONE-ADDRESS: http://127.0.0.1:8500 forever; dbs swap behind
  the port.
- FULL-PATHS + Evidence Discipline (extended 2026-08-07):
  ground first, read before assert, no error-tolerant probing.
  The s7 column-guess incident is the standing cautionary tale.
- STEP RULE: one step = one screen; every step carries a
  from-scratch re-entry route.
- No levity while the driver is eating friction.

## Open decisions

- Client-pay-page amendment ratification (next action 1).
- Held recon pair (gated item 1).
- Invoice-code build gate (item 10).
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged, his
  layer call.
- Demo-login prefill + no-expiry (gated item 5): queued, not
  blocking.
