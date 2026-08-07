# state.md -- billing-ui (session cache, overwritten each wind-down)

## Status

P4 OPEN after attempt 3 (2026-08-07): the FIRST COMPLETE
James-driven walk, all 32 steps, close-out PASS quoted on the
walked db (check_demo_walk exit 0 through his +1 invoice-number
offset; fiduciary 8 GREEN in place) -- but VERDICT FAIL on all
three axes, his words in worklog s6 cont: (a) recon "not
adequate and I think incorrect", (b) "I'd apologize for many",
(c) "half-baked". Walk MECHANICS are proven; the FAIL is
product quality.

Same session, two fix rounds shipped and verified:
- Attempt-2 root causes -> coupling machinery: sheet 6th+7th
  amendments (vocabulary block, Goal per part, Go:/If lost:
  recovery rail on every step, prefill callouts, Part E
  positive-only + step-17 CHECKPOINT, All-tab routes, step 32
  re-pin); nav underlines Billing on billing screens (shared
  chrome, ratified); verify/drive_sheet.py PERMANENT coupling
  oracle (every step entered from scratch; SHEET LOCK sha
  308332708dd1); verify/report_sha.py canonical sha (a506f085;
  prior lineage a506f085->485b2463->d7ee3ace exposed as RECIPE
  drift -- content byte-stable since the s4 commit; result.md
  must disclose).
- Axis-(a) fix 1: recon screen REBUILT as three vertical
  footing panes (Bank statement independent leg / Books with
  system-correction tags / Client claims), parenthesized
  outflows, tie line, unmatched-item error box. James's
  eyeball: "solid for where we are at". Driver s32 strengthened
  to pin all pane titles and foot labels.

All suites green at close (worklog s6 cont 2): drive-sheet
24/24; labels 82/0; billing-ui walk 17/17 x2 sha a506f085;
ui-walk 13; spine 107; billing 25; fiduciary --seeded 8.

## Next actions

1. Work atlas/gated-items.md UNLOCKED queue, A first per his
   ruling: dates render MM/DD/YYYY on billing screens AND in
   the sheet's typed values (root cause of 4 of 5 attempt-3
   date misses), data stays ISO, drive_sheet asserts it. Then
   B (sheet identifies invoices by TYPE, never number), then
   C-H; clarify the two snap labels in I.
2. Held recon decisions (gated item 1, his call): (i) keep
   fabricated compensating bank events on corrections, or move
   the engine to real-bank matching; (ii) place the demo
   period end so statements show a cleared/pending mix.
3. Gate-by-gate through the locked list -- client pay page
   styling first (his axis-(b) driver; needs a program-ruling
   break-in, method in gated-items.md).
4. Attempt 4 (fresh db, full walk, verdict) once the queue
   lands.

## Watch items and caveats

- SHEET LOCK: any walk-sheet edit makes drive_sheet.py exit 2
  until EXPECTED_SHEET_SHA is re-synced after verifying steps
  against the driver. Deliberate friction.
- Sha receipts: ONLY report_sha.py output counts. result.md
  must carry the recipe-drift reconciliation note.
- Server LEFT RUNNING on 8500 serving the WALKED attempt-3 db
  (casework-ui/data/demo-walk-2026-08-07c.db) with the new
  recon screen, for James's eyeballing. Fresh-walk day: swap a
  new dated db behind 8500. Machine restart: serve per
  CLAUDE.md "How to run", always 8500. Login on 07c:
  demo.driver@synthetic.test / demo-walk-pass, code on screen.
- Walk dbs retained (delete=archive): demo-walk-2026-08-04,
  -04b, -07 (attempt 2; audit log = divergence record), -07b
  (staged, unused), -07c (attempt 3, WALKED -- the verdict db).
- Attempt-3 snaps (25, labeled) archived at
  billing-ui/walk-artifacts/2026-08-07-attempt3/ -- the
  friction-log evidence; committed.
- Backlog: atlas/gated-items.md is the ONE list of locked/
  parked items + the break-in method (F7-precedent). Keep it
  current from any child session.
- billing + fiduciary suites run from ../casework-billing/
  (CLAUDE.md corrected s6; they never lived in ../casework/).
- Standing gates at every close: ui-walk 13, spine 107,
  billing 25, fiduciary 8 -- all green at this close.
- Anti-stall ledgers: P2 1/2, P3 0/2, F-1 redesign 1/2 used.
- Firm question still unasked: flat-fee vs hourly mix.
- PARKED PROGRAM-LEVEL FINDING (unchanged): client intake
  questionnaire defects (worklog s3); carried on gated-items.
- METHOD (s6 triple): script-vs-hands, sha recipe drift, and
  the agent guessed-table incident are ONE class -- generated
  artifacts verified against their own assumptions. Cure:
  procedures become versioned code with loud failure modes
  (drive_sheet lock, report_sha, Evidence Discipline in the
  global CLAUDE.md). James's hands stay the decisive oracle:
  three attempts, every stall a real defect.

## Interface rulings (2026-08-04, all standing)

- PRODUCT + ONE plain-language question per touchpoint; question
  is the LAST sentence; translate jargon inline; re-issue the
  plain map at every gate and on demand.
- ONE-ADDRESS: James's URL is http://127.0.0.1:8500, forever.
  Dbs swap behind the port. Other ports are agent-internal.
- FULL-PATHS: absolute file paths always; instruction steps name
  menu path + control label, verified never guessed. EXTENDED
  2026-08-07: binds agent evidence-gathering too -- ground
  first, read before assert, no error-tolerant probing.
- STEP RULE: one step = one screen; Go:/Field = value/one End:
  per step. EXTENDED 2026-08-07: every step carries a
  from-scratch re-entry route (Go: or If lost:).
- No levity while the driver is eating friction.

## Open decisions

- Held recon pair (gated item 1): fabricated correction events
  vs real-bank matching; period-end placement. James rules
  after living with the new screen.
- Empty-invoice list behavior (gated item 3): acceptable, or
  rendering-side list-filter change?
- QUEUED GATE DECISION (unchanged): demo-login prefill +
  no-expiry sessions on synthetic dbs only. Not blocking.
