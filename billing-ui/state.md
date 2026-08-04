# state.md -- billing-ui (session cache, overwritten each wind-down)

## Status

P4 attempt 1 (2026-08-04): FAIL at step 12 on axis (b), finding
F-1 -- the invoice page was model-shaped. Protocol followed:
findings -> redesign -> mini-gate. F-1 REDESIGN BUILT and GATE
CLOSED PASS same day (James: "Designs better", zero kills):
state-shaped Bill / Trust request page (building -> awaiting
money -> paid), one "Collect $X" card with per-method folds,
native <details> (zero-JS), rendering-only, nouns unified.
Extra defects fixed en route: status-shadowing bug (caught by
walk verifier), empty bill wore a Paid pill (caught by deck
frame 1 -- first hands/deck-visible state no deck had shown).

All suites green post-rebuild, quoted in worklog: billing-ui
walk 17/17 x2, timing-stripped sha 485b2463 SUPERSEDES a506f085
(F-1 redesign is the delta; disclose both in result.md);
ui-walk 13; spine 107; billing 25; fiduciary --seeded 8.

The SHEET is now an oracle-checked artifact: atomic STEP RULE
(one step = one screen; 32 steps, parts A-J), verify/
check_sheet_labels.py green (79 labels / 0 missing; fences:
slash-tuples, multi-End steps, labels must exist in rendering
source). Papercut ledger (8 entries) + walk finding F-1 in
worklog s4.

## Next actions

1. FRESH P4 WALK -- the only remaining contract item. One
   sitting, ~15 min. Recorder order: fresh dated db served ON
   8500 (stop the gate server first), quote run_billing_ui_walk
   AND check_sheet_labels green, hand James the sheet at step 1
   (fresh db = account creation, NO login-memory wall). He
   drives to step 32; then check_demo_walk.py + fiduciary on the
   walked db, PDF/ledger/recon eyeball, three-part verdict.
   PASS -> completion proof, result.md, roster flip.

## Watch items and caveats

- Gate server LEFT RUNNING on 8500 with
  data/gate-f1-2026-08-04.db (billing.walk@synthetic.test /
  billing-walk-pass, code on screen) for James's solo clicking.
  Swap a fresh db behind 8500 at walk time. Machine restart:
  serve per CLAUDE.md "How to run", always 8500.
- Dead walk dbs retained (delete=archive): demo-walk-2026-08-04
  (steps 1-2), demo-walk-2026-08-04b (steps 1-5-ish, F-1 db).
- Verifier assertion edits + sha supersession disclosed in
  worklog s4 cont -- result.md must carry both shas.
- check_demo_walk.py predates the redesign and the atomic sheet
  -- REVIEW IT before the walk (it asserts db-state receipts,
  likely fine, but verify no stale page-content assertions).
- Standing gates at every close: ui-walk 13, spine 107, billing
  25, fiduciary 8 -- all green post-rebuild this session.
- Anti-stall ledgers: P2 1/2, P3 0/2, F-1 redesign 1/2 used.
- Firm question still unasked: flat-fee vs hourly mix.
- PARKED PROGRAM-LEVEL FINDING (unchanged): client intake
  questionnaire loses unsaved fields / no re-render / submit
  verifies nothing (worklog s3). Not this child's scope; carry
  until routed.
- METHOD: deck-vs-hands discriminator FIRED (s3 predicted it) --
  three zero-kill decks passed a page James's hands failed in
  one minute. Weight future gates toward hands-on. Also: prose
  facing the ratifier needs oracles (label-audit pattern is
  portable; casework-ui's cold-run sheet should get one).

## Interface rulings (2026-08-04, all standing)

- PRODUCT + ONE plain-language question per touchpoint; question
  is the LAST sentence; translate jargon inline; re-issue the
  plain map at every gate and on demand.
- ONE-ADDRESS: James's URL is http://127.0.0.1:8500, forever.
  Dbs swap behind the port. Other ports are agent-internal.
- FULL-PATHS: absolute file paths always; instruction steps name
  menu path + control label, verified never guessed.
- STEP RULE: one step = one screen ("when the user loads a new
  page its a new step"); Go:/Field = value/one End: per step.
- No levity while the driver is eating friction.

## Open decisions

- Walk scheduling (James) -- fresh sitting, next session.
- QUEUED GATE DECISION: demo-login prefill + no-expiry sessions
  on synthetic dbs only (kills the login-memory wall for parked/
  resumed demos; touches casework-ui's login screen -> needs
  James's ratification). Not blocking a fresh single-sitting
  walk.
