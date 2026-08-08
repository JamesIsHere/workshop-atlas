# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s10 close, 2026-08-08)

ATTEMPT 4 RAN AND WAS RULED: FAIL on (b) nothing-embarrassing
and (c) bookable; (a) fiduciary-story-lands PASSED. The named
defect -- no status surface, no visible flow -- became gated
item 12; the DESIGN GATE for the home page ran the same
session (7 rulings, billing-ui/status-page.md RATIFIED, sheet
signed) and the HOME PAGE IS BUILT: the firm status page now
IS the dashboard at "/" (money tiles + verdict chips, strict
needs-attention over an in-flight line, money activity with
actors, practice row absorbed; nav Dashboard entry + brand
link home -- gated item 4 CLOSED). All suites green, sha
28a19170 supersedes 301b574d, full record worklog s10.
Pending: James's eyeball of the live page. Still open in item
12: object 2 (flow markers), object 3 (client summary),
period-close act, finish pass -- each needs its own design
pass before build.

## Status

P4 OPEN after attempt 4 (verdict FAIL b/c, (a) PASS,
2026-08-08). Full record: worklog s10; sealed sheet:
walk-artifacts/2026-08-08-attempt4/verdict.md (48 step-named
snaps beside it). Friction log carries 5 entries; the two
verdict drivers are the status/flow gap (item 12) and general
finish ("not beautiful").

## Attempt 5 preconditions (not yet a protocol)

1. Gated item 12 designed with James and built: summary layer
   (client / matter / billing), flow made visible, hidden state
   brought forward.
2. Finish pass against "not beautiful" (his eyes are the bar).
3. Step-29 ledger-link visibility fix (friction entry 1).
4. Then the standard attempt protocol: fresh dated db behind
   8500, sheet drive, three-part verdict. Sheet may need
   amendment if new surfaces change routes -- sheet-lock
   re-sync rules apply.

## Watch items and caveats

- SHEET LOCK f7f821edb1e9 UNCHANGED by s10 (no code, no sheet
  edits this session). Walk-report canonical sha 301b574d
  UNCHANGED (history in worklog s8-s9). ONLY report_sha.py
  output counts.
- Server RUNNING on 8500 (client 8501), PID 71992, over the
  walked data/demo-walk-2026-08-08.db -- the first pure-model
  walk db (s9 engine, no mirror events). Restart after ANY
  app_ui or casework/app change -- stale module code serves
  silently (bitten twice in s7).
- Retained walk dbs (delete=archive): -04, -04b, -07, -07b,
  -07c, -08. All pre--08 dbs are PRE-ENGINE (mirror events on
  their bank records) and pre-07c ones are PRE-CODE (run
  verify/migrate_invoice_codes.py before serving).
- s10 incident, minor: seed_demo.py takes no args -- a --help
  attempt re-seeded data/demo-billing.db (generated file,
  harmless, fiduciary GREEN quoted in worklog s10).
- billing + fiduciary + anchor-billing run from
  ../casework-billing/; spine from ../casework/; core touches
  trigger the reciprocal guard (ALL suites).
- atlas/gated-items.md current as of s10 (item 12 added; item 1
  stays CLOSED -- the walk verdict confirmed the recon axis).
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

- STATUS/FLOW SURFACE design (gated item 12): the next
  conversation. What the surface is, then which child builds
  it. James's gate.
- Step-29 ledger-link visibility: small fix, likely rides the
  item-12 work; not yet authorized.
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged, his
  layer call.
- Demo-login prefill + no-expiry (gated item 5): queued, not
  blocking.
- Client portal: gated item 11, deliberately out of scope.
