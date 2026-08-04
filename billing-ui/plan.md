# plan.md -- billing-ui (agent's strategy; rewritten freely)

Pre-ratification draft. Phases start only after goal.md is ratified.
Hybrid mode: each phase is agent-unattended against verifier 1; each
GATE is James reviewing rendered screens + all standing suites green
+ receipts banked.

## P0 -- Oracle first (op rule 7) -- BUILT 2026-08-04

Verifier RED on disk (3 pass / 14 pending / ON TRACK exit 1);
protocol strawman drafted; seed GREEN x2; receipts banked.
GATE 0 (OPEN): decision first -- the F7 cross-project gap
(worklog s2 findings 1+2); then James red-pens the protocol +
walk step list. check_demo_walk.py builds after protocol
ratification.

## P1 -- Read surfaces (the fiduciary wedge, visible) -- BUILT
## 2026-08-04; GATE 1 CLOSED (pass, zero kills)

Billing nav area; trust + operating accounts screen; trust ledger
browse -> sub-ledger -> entry detail with correction trail;
reconciliation view (recon identity + reconciling items); invoice
list + detail (read). Empty states designed. Walk steps for these
turn green.
GATE 1 verdict: PASS with zero kills -- P1 styling stands as the
demo-grade reference.

## P2 -- Lifecycle writes -- BUILT 2026-08-04; GATE 2 OPEN

Invoice creation (saved charges + time import); time entry screen;
trust request create; record direct payment; trust-transfer earn-out
flow; disbursement flow; online-payment status lines on invoice +
trust-request screens (no dedicated screen -- red-pen round 2 kill);
invoice PDF download (pulled forward from P3: the walk cannot mark
a missing link on an existing screen Pending, and the route is one
call into frozen billing.invoice_pdf). Walk green through steps
4-10 plus PDF/drill-down/recon/audit/fiduciary: 16 pass, 1 pending
(payment edit -- P3), 0 fail.
GATE 2: rendered review (deck banked); James clicks the lifecycle
himself on a fresh db (informal rehearsal, not the oracle).

## P3 -- Corrections family + finish -- BUILT 2026-08-04; GATE 3
## OPEN

Payment detail screen (row + journal trail + bank record); edit as
reversal+repost with the visible trail; refund; charge
re-association via the same correction form; email share. No
parked screens existed to polish. Verifier 1 fully GREEN: 17/17 x2
(reports identical after stripping run-timestamp and timings --
the report format carries wall-clock, so the x2 seal is on
timing-stripped sha a506f085, both runs).
GATE 3: rendered review (3-frame deck banked); protocol final
red-pen; schedule walk day.

## P4 -- Demo walk day + close

Fresh dated db; James drives the ratified protocol unassisted;
fiduciary suite against walked db; PDF + ledger + recon eyeball;
demo-grade verdict. PASS -> completion proof banked, self-audit
wind-down, result.md, roster flip. FAIL -> findings, mini-gate,
re-run.

## Standing at every gate

run_ui_walk (13) green; spine 107 green; billing 25 green;
fiduciary 8 green; receipts to verify/gate-receipts/; James screen
review noted in worklog.

ORDERING RULE (ruled 2026-08-04, James): the agent's mechanical run
ALWAYS precedes James's hands -- at gates, rehearsals, and walk day
alike, the walk verifier is run and quoted GREEN (or ON TRACK with
the relevant steps green) immediately before any James screen time.
His pen judges shape; the oracle catches errors. James never
debugs by walking.

Gate mechanics (ruled 2026-08-04, from James's automation push):
the agent EXECUTES all mechanical steps -- server start (seeded db,
background), suite runs, close-out checks -- and additionally
drives the real screens with the session's Chrome tools to capture
a per-screen SCREENSHOT DECK before each gate. James red-pens
pixels from the deck and clicks only where he wants to feel the
flow. Puppeteer itself is barred: node_modules trips the ratified
js-discipline sweep, and the walk verifier already IS the headless
driver for a zero-JS app.

## Watch

- F7 substrate gap RESOLVED 2026-08-04 (worklog s2 cont): fix
  landed under program ruling, suites resealed. Corrections
  screens (P3) and walk step 10 are unblocked.
- Anti-stall: 2 polish iterations max per screen, then park for the
  gate (goal.md default).
- Any need to touch existing casework-ui screens/shell/walk or
  casework/ client pages -> flag as gate decision, never just do it
  (P1 needs the nav "Billing" approval -- take it at gate 0).
