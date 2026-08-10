# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s13 cont, 2026-08-09)

ATTEMPT 5 IS FULLY PREPPED. The finish pass is done both halves
(James: "I think it looks good"; agent pass fixed step-29 ledger
links, the checkbox float, and undated seed charges -- all
verified on-screen). James then RULED the attempt-prep decision:
the demo sheet gains the period-close act. BUILT as the sheet's
seventh amendment: Part K, steps 33-40 (July coda -- 100.00
consult billed+paid 07/01 -- then prepare, approve, the
permanent record, and the PC1 lock proven on screen by a refused
July-dated disbursement). SHEET LOCK RE-SYNCED: f7f821edb1e9 ->
85e4e4633a37. drive_sheet extended (+3 groups, 27/27 GREEN);
labels 91/0; check_demo_walk gains the Part-K receipt (smoke-
tested: pre-close dbs fail exactly that receipt). ALL suites
green and quoted in worklog s13/s13 cont; report_sha 30301f88
UNCHANGED.

## Status

P4 OPEN after attempt 4 (FAIL b/c, (a) PASS, 2026-08-08). All
attempt-5 preconditions MET: item 12 built (s10-s12), finish
pass done (s13), close act in the sheet + lock re-synced
(s13 cont). NEXT: attempt 5 itself, whenever James is ready.

## Attempt 5 protocol (the standard one; sheet now 40 steps)

1. Agent seeds a FRESH data/demo-walk-<today>.db behind 8500
   (empty -- James creates everything; NOT seed_demo, which is
   the preview/gate-review db), confirms /setup answers, runs
   the walk verifier and quotes it GREEN before handover.
2. James receives exactly two things: http://127.0.0.1:8500 and
   the sheet (verify/demo-walk-protocol.md). Two browser
   windows: normal + incognito blank. He drives all 40 steps
   (Part K closes July at the end).
3. Close-out: check_demo_walk.py on the walked db (now includes
   the close receipt; fiduciary in place includes F9), James's
   PDF/ledger/recon eyeball, then the three-part verdict sheet.
   Marks M0..M7; soft budget still M1->M6 at 20:00.

## Watch items and caveats

- Server UP at close of s13 on 8500 over the PREVIEW db
  billing-ui/data/demo-billing.db (dated charges in, July OPEN
  and closable; clicking is consequence-free -- it regenerates
  via verify/seed_demo.py). Reseeds wipe sessions: login
  demo.reviewer@synthetic.test / demo-seed-pass, code shown
  on-screen. Swap dbs behind the port, never the port. Restart
  after ANY app_ui or casework/app change. Launcher:
  python billing-ui/serve.py --db <ABS path>.
- JUDGMENT CALLS FLAGGED THIS SESSION (James may re-rule):
  (1) marks -- M7 added, soft budget kept at M1->M6 for
  cross-attempt comparability, M1->M7 recorded as data;
  (2) the PC1 refusal error renders the period ISO-style
  ("period 2026-07 is closed...") in an otherwise MM/DD/YYYY
  surface -- core-owned text in casework/app/period.py, inside
  the standing close amendment's write surface if he wants it
  reworded; the sheet quotes it verbatim with a translation.
- FLAGS from the s13 sweep, both on frozen casework-ui screens
  (gate decisions): contact detail card shows raw machine keys
  as labels (bio.family_name etc.); contact Matters card prints
  ISO dates vs MM/DD/YYYY.
- FIRM-LOCAL DATES RULING (s12 cont): business dates stamp
  firm-local, timestamps stay UTC; verified live on the close
  signatures. A new date surface must follow it.
- Pre-close dbs (all retained walk dbs except -08) FAIL LOUD on
  ledger writes and /billing/close (missing period_closes --
  deliberate). migrate_period_close.py before serving one;
  pre--08 dbs are PRE-ENGINE; pre-07c also need
  migrate_invoice_codes.py. check_demo_walk now FAILS any
  pre-Part-K walked db on the close receipt -- correct, not a
  bug.
- s11 double-bind protocol: netstat before blaming the db;
  single bind verified at every s13 relaunch.
- Close judgment calls flagged, unruled (s12): month closable
  only after it ends; ranking rows plain text; approve-on-stale
  commits the void; one closable month, never a choice.
- Flow-marker flags (s11) still open: dashboard settling has no
  firm-wide backing list; overdue beats sent on chipnotes; chip
  colors reuse pill families.
- The no-logic lint counts the WORD "SELECT" in app_ui prose.
- billing + fiduciary + anchor-billing run from
  ../casework-billing/; spine from ../casework/; core touches
  trigger the reciprocal guard (ALL suites). period.py imports
  the recon oracle LAZILY.
- Retained walk dbs (delete=archive): -04, -04b, -07, -07b,
  -07c, -08 (migrated), -09 (empty, incident artifact).
- atlas/gated-items.md current as of s12.
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

- ATTEMPT 5: ready to run; James picks the moment.
- Marks judgment call (M7/budget) and the refusal-message
  wording: flagged above; James may re-rule.
- Contact-screen flags from s13 (raw labels, ISO dates): gate
  in or leave; James's call.
- Dashboard settling backing list: flagged, unruled.
- Close judgment calls (s12): James may re-rule.
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged.
- Demo-login prefill + no-expiry (gated item 5): queued.
- Client portal: gated item 11, deliberately out of scope.
