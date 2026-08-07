# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s9 close, 2026-08-07)

The banking engine is BUILT (James's real-bank ruling, s8 close;
executed s9, worklog s9 has the full record). Corrections and
refunds touch books only; the bank record keeps exactly what the
bank saw; the recon engine matches statement lines to book
entries and explains every difference as a caused reconciling
item; F7 is strengthened (bank-record purity, timing resolves
all-cleared, closed causes); the demo period-end shows a
cleared / in-transit / outstanding mix stable on any run date.
ALL suites green, shas superseded and recorded. NOTHING stands
between here and ATTEMPT 4: fresh db, code-routed sheet, James
drives, his three-part verdict. That is the next session's whole
job -- do not start new build work before the walk.

## Status

P4 OPEN after attempt 3 (verdict FAIL a/b/c, 2026-08-07). Since
then, same day: s7 closed the unlocked backlog A-I + two core
break-ins; s8 built the client pay page, trust relabel, invoice
codes B0001/T0001; s9 built the recon engine (gated item 1,
CLOSED pending walk verdict). The product attempt 4 runs on is
materially different from attempt 3's on every axis of the FAIL:
(a) reconciliation is adequate and correct by construction now;
(b)/(c) the s7/s8 polish batch.

## Attempt 4 protocol (when James says go)

1. Fresh db: serve a NEW data/demo-walk-<date>.db on port 8500
   (one-address rule; kill the running server first).
2. James drives demo-walk-protocol.md's 32 steps; agent records
   marks M0-M6 and the friction log.
3. Close-out: agent runs check_demo_walk.py on the walked db,
   quotes output (exit 0 required); James eyeballs PDF + ledger
   + recon; verdict sheet, all three sub-verdicts up/down.

## Watch items and caveats

- SHEET LOCK current sha f7f821edb1e9 (re-synced s9, seventh
  sheet amendment: step 24 disburse rides today's prefill, step
  28 books-only correction wording, step 32 names the mix).
  Walk-report canonical sha 301b574d UNCHANGED by s9 (history:
  a506f085 -> de589cbd -> d9074178 -> c4555b15 -> f3f16120 s7 ->
  c61ea17a s8 -> 301b574d s8 cont 2). ONLY report_sha.py output
  counts.
- casework-billing seal supersession s9: fiduciary e6c64593 x2
  (supersedes fb5bccda), billing c53f262b x2 (supersedes
  acba95b1; drift is s8's display_code column). Recorded in
  casework-billing/state.md.
- Walk dbs other than 07c are PRE-CODE schema (run
  verify/migrate_invoice_codes.py before serving one) and ALL
  retained dbs including 07c are PRE-ENGINE (mirror events on
  their bank records; new matcher still reconciles them HOLDS,
  but F7 purity would flag them -- attempt 4's fresh db is the
  first pure one).
- Server RUNNING on 8500 (client surface 8501), walked 07c db,
  s9 engine code loaded (restarted this session; 8500 -> 303
  login, client link /invoice/SYNTH-INV-3-1 -> 200). Login
  demo.driver@synthetic.test / demo-walk-pass, code on screen.
  Restart after ANY app_ui or casework/app change -- stale
  module code serves silently (bitten twice in s7).
- billing + fiduciary + anchor-billing run from
  ../casework-billing/; spine from ../casework/; core touches
  trigger the reciprocal guard (ALL suites).
- Walk dbs retained (delete=archive): -04, -04b, -07, -07b,
  -07c. Attempt-3 snaps archived in walk-artifacts/.
- atlas/gated-items.md current as of s9 (item 1 BUILT/CLOSED
  pending walk verdict).
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

- ATTEMPT 4 go/no-go: James's call, the only thing owed.
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged, his
  layer call.
- Demo-login prefill + no-expiry (gated item 5): queued, not
  blocking.
- Client portal: gated item 11, deliberately out of scope.
