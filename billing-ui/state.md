# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s12, 2026-08-09)

THE PERIOD-CLOSE ACT IS DESIGNED, RATIFIED, AND BUILT -- item 12
is objects-complete. Rulings PC1 (hard close: engine refuses
postings dated into a closed month; late facts post
current-dated), PC2 (two-step prepare/approve, same person
allowed and SHOWN on the record), PC3 (tie required, exceptions
carried with per-item acknowledgment). Sheet: period-close.md,
RATIFIED as drafted; flags 9 (billing docs unlocked v1) and 10
(no reopen, ever) stand. Program amendment 2026-08-09 recorded
in ../CLAUDE.md (scoped casework write surface). Build:
period_closes table (gen_schema), casework/app/period.py, lock
guard in ledger._post + create_external_event, /billing/close +
record page + entry links, fiduciary F9 (closed periods must
recompute byte-equal), unit_period_close.py 6/6, walk step 20
(July-coda close; August story untouched). CROSS-PROJECT FIX:
reconcile._sub_ledger_sum now as-of-period_end (was as-of-now;
latent; broke retrospective recomputes) -- under the standing F7
amendment, flagged in worklog s12. ALL suites green and quoted
in worklog s12; sha chain ... c59b8e9d -> 30301f88
(report_sha.py only). Sheet lock f7f821edb1e9 UNCHANGED.

## Status

P4 OPEN after attempt 4 (verdict FAIL b/c, (a) PASS,
2026-08-08). Item 12: ALL FOUR OBJECTS BUILT (home page s10,
flow markers + client summary s11, period-close act s12).
Remaining before attempt 5: the FINISH PASS against "not
beautiful", step-29 ledger-link fix, and attempt prep.
Friction log: 5 entries; step-29 fix still queued.

## Attempt 5 preconditions (updated s12)

1. DONE (s11): objects 1-3 of gated item 12.
2. DONE (s12): period-close act designed with James and built.
3. Finish pass against "not beautiful" (his eyes are the bar).
4. Step-29 ledger-link visibility fix (friction entry 1).
5. Attempt-prep decision: does the demo sheet gain a close act?
   The fresh demo db seeds July dates (seed_demo NOW=07-20), so
   July is closable live at the attempt; a sheet amendment needs
   the sheet-lock re-sync protocol. James's call at prep.
6. Then the standard attempt protocol: fresh dated db behind
   8500, sheet drive, three-part verdict.

## Watch items and caveats

- Server UP at close of s12 on 8500 over the PREVIEW db
  billing-ui/data/demo-billing.db (regenerated on the new
  schema via verify/seed_demo.py; July closable; James drove a
  live close on it -- clicking is consequence-free, it
  regenerates). The migrated walk db (demo-walk-2026-08-08.db,
  all-August facts, honest empty close page) is the alternate;
  swap dbs behind the port, never the port. Restart after ANY
  app_ui or casework/app change. Launcher:
  python billing-ui/serve.py --db <ABSOLUTE path>.
- FIRM-LOCAL DATES RULING (2026-08-09, s12 cont): business
  dates stamp firm-local (system clock), timestamps stay UTC.
  Applied in billing_ui._today, the client pay date in
  casework/app/server.py, and drive_sheet.today. A new date
  surface must follow the ruling.
- FINISH-PASS QUEUE now: step-29 ledger-link visibility;
  carried-item checkbox layout on the prepare page (floats
  away from its text -- James's snap, s12).
- Pre-close dbs (all retained walk dbs except -08) FAIL LOUD on
  any ledger write and on /billing/close (missing period_closes
  table -- deliberate). Run migrate_period_close.py before
  serving one. Pre--08 dbs are PRE-ENGINE; pre-07c ones also
  need migrate_invoice_codes.py.
- s11 double-bind incident protocol still applies: netstat
  before blaming the db (s12 killed the stale s11 server PID
  before relaunch; single bind verified).
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
  assert, no error-tolerant probing. s12 added the design-sheet
  present-tense incident (James hunted for an unbuilt route) to
  the s7 lineage -- sheets phrase proposals as proposals with
  verified ground facts.
- STEP RULE: one step = one screen; every step carries a
  from-scratch re-entry route.
- No levity while the driver is eating friction.

## Open decisions

- FINISH PASS against "not beautiful" (next; James's eyes are
  the bar). Step-29 fix rides it.
- Attempt-prep: demo-sheet close act (precondition 5 above).
- Dashboard settling backing list: flagged, unruled.
- Close judgment calls: see watch items; James may re-rule.
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged.
- Demo-login prefill + no-expiry (gated item 5): queued.
- Client portal: gated item 11, deliberately out of scope.
