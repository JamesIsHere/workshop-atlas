# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s13, 2026-08-09)

THE FINISH PASS IS DONE, both halves: James ruled "I think it
looks good" on his own pass; the agent pass fixed the two queued
defects and swept every billing screen live. Fixes, all verified
on-screen: step-29 ledger links promoted to the .go button
affordance (text + hrefs byte-identical, sheet lock and pins
untouched); carried-item checkbox float killed by a BILLING_STYLE
override (base input width:100% was the cause; .pick rows covered
too); seed_demo now dates all six seeded charges (blank DATE cell
on invoice Charges, per gated item C's write-path convention).
Full close act driven in-browser on the preview db: prepare ->
approve -> record, firm-local signature dates verified 08/09.
ALL suites green and quoted in worklog s13; report_sha 30301f88
UNCHANGED (rendering-only; no supersession). Sheet lock
f7f821edb1e9 UNCHANGED.

## Status

P4 OPEN after attempt 4 (verdict FAIL b/c, (a) PASS, 2026-08-08).
Item 12: all four objects built (s10-s12); finish pass DONE
(s13). Remaining: the attempt-prep decision, then attempt 5.

## Attempt 5 preconditions (updated s13)

1. DONE (s11): objects 1-3 of gated item 12.
2. DONE (s12): period-close act designed with James and built.
3. DONE (s13): finish pass -- James's eyes + agent sweep, two
   queued defects fixed, one sweep catch fixed.
4. DONE (s13): step-29 ledger-link visibility fix.
5. Attempt-prep decision: does the demo sheet gain a close act?
   The fresh demo db seeds July dates (seed_demo NOW=07-20), so
   July is closable live at the attempt; a sheet amendment needs
   the sheet-lock re-sync protocol. James's call at prep.
6. Then the standard attempt protocol: fresh dated db behind
   8500, sheet drive, three-part verdict.

## Watch items and caveats

- Server UP at close of s13 on 8500 over the PREVIEW db
  billing-ui/data/demo-billing.db (reseeded at close: dated
  charges in, July OPEN and closable; James's s12 live close was
  wiped with the reseed -- clicking is consequence-free, it
  regenerates). Reseeds wipe sessions: login is
  demo.reviewer@synthetic.test / demo-seed-pass, code shown
  on-screen. The migrated walk db (demo-walk-2026-08-08.db,
  all-August facts) is the alternate; swap dbs behind the port,
  never the port. Restart after ANY app_ui or casework/app
  change. Launcher: python billing-ui/serve.py --db <ABS path>.
- NEW FLAGS from the s13 sweep, both on frozen casework-ui
  screens (gate decisions, not billing-ui code changes): contact
  detail card shows raw machine keys as labels (bio.family_name,
  bio.given_name, contact.email); contact Matters card prints
  ISO dates vs the MM/DD/YYYY convention. James may gate them in
  for attempt 5 or leave them.
- FIRM-LOCAL DATES RULING (2026-08-09, s12 cont): business dates
  stamp firm-local (system clock), timestamps stay UTC. Verified
  live on the close signatures this session. A new date surface
  must follow the ruling.
- Pre-close dbs (all retained walk dbs except -08) FAIL LOUD on
  any ledger write and on /billing/close (missing period_closes
  table -- deliberate). Run migrate_period_close.py before
  serving one. Pre--08 dbs are PRE-ENGINE; pre-07c ones also
  need migrate_invoice_codes.py.
- s11 double-bind incident protocol still applies: netstat
  before blaming the db (followed at every s13 relaunch; single
  bind verified each time).
- Close judgment calls flagged, unruled (worklog s12): month
  closable only after it ends; ranking rows unlinked plain
  text; approve-on-stale commits the void; one closable month,
  never a choice. James may re-rule any.
- Flow-marker flags from s11 still open: dashboard settling
  segment has no firm-wide backing list; overdue beats sent on
  chipnotes; chip colors reuse pill families.
- The no-logic lint counts the WORD "SELECT" in app_ui prose --
  keep SQL words out of comments/docstrings outside reads.py.
- billing + fiduciary + anchor-billing run from
  ../casework-billing/; spine from ../casework/; core touches
  trigger the reciprocal guard (ALL suites). period.py imports
  the recon oracle LAZILY (spine keeps zero cross-child
  imports at import time).
- Retained walk dbs (delete=archive): -04, -04b, -07, -07b,
  -07c, -08 (migrated), -09 (empty, incident artifact).
- atlas/gated-items.md current as of s12 (item 12 all four
  objects recorded built).
- Anti-stall ledgers: P2 1/2, P3 0/2, F-1 1/2 used. Firm
  question still unasked: flat-fee vs hourly mix.

## Interface rulings (2026-08-04, all standing)

- PRODUCT + ONE plain-language question per touchpoint; the
  question is the LAST sentence; translate jargon inline;
  re-issue the plain map at every gate and on demand.
- ONE-ADDRESS: http://127.0.0.1:8500 forever; dbs swap behind
  the port.
- FULL-PATHS + Evidence Discipline: ground first, read before
  assert, no error-tolerant probing. Sheets phrase proposals as
  proposals with verified ground facts (s7/s12 lineage).
- STEP RULE: one step = one screen; every step carries a
  from-scratch re-entry route.
- No levity while the driver is eating friction.

## Open decisions

- Attempt-prep: demo-sheet close act (precondition 5 above) --
  NEXT, James's call.
- Contact-screen flags from s13 (raw labels, ISO dates): gate in
  for attempt 5 or leave; James's call.
- Dashboard settling backing list: flagged, unruled.
- Close judgment calls: see watch items; James may re-rule.
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged.
- Demo-login prefill + no-expiry (gated item 5): queued.
- Client portal: gated item 11, deliberately out of scope.
