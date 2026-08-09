# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s11 close, 2026-08-09)

ITEM-12 OBJECTS 2 AND 3 ARE BUILT AND JAMES-SEEN. The s10 home
page got its eyeball; the audience ruling landed (dashboard =
FINANCE SEAT; CEO consumes it narrated); the build-order ruling
landed (screens owner-sees-all with an AUDIENCE TAG per design
pass; role enforcement is a future contract; segregation-of-
duties asked per write-flow at design time). Flow markers built
WIDE under the signed dollars-in-buckets vocabulary (Unbilled /
Outstanding / Settling / Clearing, rest unmarked; buckets label
DOLLARS never objects -- James's partial-payment catch): dashboard
pipeline dollar line (amends home-gate R5), invoice bucket
splits, row chips, matter-page unbilled line. Client summary
built as the Money band on the contact page (placement A: one
client one page; band = audience boundary) with the FOOTED
PAYMENTS DRILL at /billing/clients/<id>/payments (James's live
catch: a stated total must tie to a listing; ruled option A).
Walk verifier is 19 steps. ALL suites green at close, quoted in
worklog s11; sha chain 28a19170 -> e6ae695b -> 5ba384cc ->
c59b8e9d (report_sha.py output only). Sheet lock f7f821edb1e9
UNCHANGED all session (no pinned label touched).

## Status

P4 OPEN after attempt 4 (verdict FAIL b/c, (a) PASS,
2026-08-08). Item 12 remaining: PERIOD-CLOSE ACT design pass
(next conversation -- it inherits the maker-checker/SoD question
and the deferred firm-wide rankings: who-is-way-behind,
keeps-us-in-cash), then the FINISH PASS against "not beautiful".
Friction log: 5 entries; step-29 ledger-link visibility fix
still queued (rides whichever pass touches that screen).

## Attempt 5 preconditions (updated s11)

1. DONE (s11): status surface + flow visible + client summary --
   objects 1, 2, 3 of gated item 12.
2. Period-close act designed with James and built.
3. Finish pass against "not beautiful" (his eyes are the bar).
4. Step-29 ledger-link visibility fix (friction entry 1).
5. Then the standard attempt protocol: fresh dated db behind
   8500, sheet drive, three-part verdict. Sheet may need
   amendment if new surfaces change routes -- sheet-lock
   re-sync rules apply.

## Watch items and caveats

- Server UP at close on 8500 over
  billing-ui/data/demo-walk-2026-08-08.db (James may browse the
  new surfaces). Restart after ANY app_ui or casework/app change
  -- stale module code serves silently (bitten twice in s7).
  Launcher: python billing-ui/serve.py --db <path> (use ABSOLUTE
  paths from a shell whose cwd has wandered; s11 hit exit-127
  twice on relative paths).
- s11 incident (environment): TWO servers double-bound port 8500
  (Windows allows it; requests land unpredictably) -- a no-args
  serve.py from 16:30 had silently created and served an EMPTY
  demo-walk-2026-08-09.db, which is why James saw first-run
  setup. Diagnose with netstat before blaming the db. The empty
  -09 db is retained (delete=archive).
- Flow-marker judgment calls flagged, unruled: dashboard
  settling segment has NO backing list when plural (band-side
  settling now links to the client payments listing; the
  firm-wide gap stands); overdue beats sent on chipnotes; chip
  colors reuse existing pill families. Client-band judgment
  calls: empty-band suppression (casework-pure page until money
  exists); headline zeros render once the band exists.
- CLEARING is ruled OUT of the client band (bank-side fact);
  the walk verifier enforces the omission.
- Frozen-surface precedent extended: matter page + contact page
  each carry one additive billing-rendered element (signed at
  the s11 design gates); frozen ui-walk green both times. The
  no-logic lint counts the WORD "SELECT" in comments/docstrings
  outside reads.py -- keep SQL words out of app_ui prose.
- billing + fiduciary + anchor-billing run from
  ../casework-billing/; spine from ../casework/; core touches
  trigger the reciprocal guard (ALL suites).
- Retained walk dbs (delete=archive): -04, -04b, -07, -07b,
  -07c, -08, -09 (empty, incident artifact). Pre--08 dbs are
  PRE-ENGINE; pre-07c ones are PRE-CODE (run
  verify/migrate_invoice_codes.py before serving).
- atlas/gated-items.md current as of s11 (item 12 objects 2+3
  recorded built; items 4 and 1 stay CLOSED).
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
  The s7 column-guess incident is the standing cautionary tale;
  s11 added two entries to its class (walk-end dollars copied
  from the wrong walk; raw-word assertions tripping on the
  style block) -- both caught by suites, neither reached James.
- STEP RULE: one step = one screen; every step carries a
  from-scratch re-entry route.
- No levity while the driver is eating friction.

## Open decisions

- PERIOD-CLOSE ACT design (gated item 12, next conversation):
  the monthly meeting as a feature; carries maker-checker/SoD
  and the deferred rankings (way-behind, keeps-us-in-cash).
  James's gate.
- Step-29 ledger-link visibility: small fix, likely rides the
  finish pass; not yet authorized.
- Dashboard settling backing list: flagged, unruled.
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged.
- Demo-login prefill + no-expiry (gated item 5): queued.
- Client portal: gated item 11, deliberately out of scope.
