# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s16, 2026-08-10)

S16 was the JUDGMENT-CALL SWEEP; the PC froze after the work
and before wind-down, and a recovery session committed it (all
suites rerun green post-freeze, quoted in worklog s16 close).
Five of the map's six clusters are RULED and landed:

- Call 1: soft budget spans the FULL walk, M1->M7 at 25:00 --
  span ruled by James, number RATIFIED ("25 is good!"),
  goal.md restamped by his ruling. drive_sheet.py gained a
  budget_coupling() preflight (sheet's final step, marks
  table, budget prose, verdict template must agree; red/green
  proven). M1->M6 stays recorded as data for attempt 1-4
  lineage.
- Calls 2a-2d: all four s12 close judgment calls ruled --
  month-must-end KEEP, ranking rows LINK (built, rendering-
  only; verifier pins the contact link), approve-on-stale
  auto-void KEEP, one-closable-month KEEP.
- Call 3: sibling messages keep month names; disclose-and-
  extend confirmed as the standing default.
- Call 4: all seven blank-select lines stand as worded; E-item
  wording flag CLOSED.
- Calls 5a-5b: overdue chipnotes KEEP; flow chips got their
  OWN colors (settling teal #ddf1ec/#146c5c, clearing olive
  #eff1d8/#5f6716; CSS single definition site, verifiers
  assert words never colors).

The SIXTH cluster is not named in the s16 log -- unverified
whether deferred or never reached; RE-OFFER THE MAP at the next
touchpoint. Bookkeeping closed in s16: report_sha supersession
recorded (b3aa0a03 SUPERSEDES 30301f88, history ... c59b8e9d ->
30301f88 -> b3aa0a03) covering s15's unrecorded walk rebuild;
CLAUDE.md's stale lock value corrected. Sheet lock stays
7b30fc89c159 -- the walk sheet was never touched in s16; the
s14 walk record keeps its 85e4e4633a37 lineage.

## Prior pointer (s14, 2026-08-10) -- THE VERDICT, still the gate

ATTEMPT 5 WAS DRIVEN AND RECORDED; THE VERDICT IS PENDING.
James drove all 40 steps solo on data/demo-walk-2026-08-09b.db
(sheet lock 85e4e4633a37), 23:43-00:06 firm-local 08/09->08/10.
Close-out ran green: check_demo_walk.py on the walked db =
13/13 PASS, fiduciary 9/0/0 GREEN, closed periods ['2026-07'],
exit 0. All 32 snaps reviewed and matched. Marks M1->M6 =
16:56, M1->M7 = 22:33 (now 90% of the ruled 25:00 full-walk
budget). Full record: worklog s14. James at s14 wind-down,
verbatim: "I think it's good for a meeting but I still want to
do more work before the meeting because I still think there's
more we can do." Read as a LEAN toward (c) bookable, NOT a
signature. The more-work rounds since (s15 friction+flags, s16
judgment calls) are that work.

A resumed session's FIRST job: ask nothing until he volunteers;
when he is ready, take the three-part verdict (a) fiduciary
story lands, (b) nothing embarrassing, (c) bookable -- each
up/down, then P4 closes on his sheet, not before. If he signs
PASS, next is the goal.md close-out (result.md etc. per
contract). If any axis FAILs, the failed-axis reason drives the
next build round, attempt 6 under the standard protocol.

## Status

P4 OPEN. Attempt 5 driven 2026-08-10, record filed (worklog
s14), VERDICT PENDING James's sit-with-it review. Nothing
advances past P4 on "looks pretty good" -- signed sheet only.
More-work rounds complete: s15 (friction 1-3, refusal wording,
contact flags, settling list, empty invoices, demo-login) and
s16 (judgment-call sweep, five clusters ruled). All eight
standing suites green and quoted post-freeze (worklog s16
close). Remaining candidate pool: unswept sixth cluster (if
any), open gated items.

## Watch items and caveats

- Server UP on 8500 over the WALKED attempt-5 db
  data/demo-walk-2026-08-09b.db -- deliberately left up for
  James's review clicking (restarted by the s16 recovery after
  the freeze killed it). It is a walked artifact
  (delete=archive; retained set -04, -04b, -07, -07b, -07c,
  -08, -09, -09b). Do NOT reseed or swap it while his review
  is open. Preview db demo-billing.db remains the alternate
  for gate reviews (verify/seed_demo.py; reseeds wipe
  sessions: demo.reviewer@synthetic.test / demo-seed-pass).
  Swap dbs behind the port, never the port. Restart after ANY
  app_ui or casework/app change. Launcher:
  python billing-ui/serve.py --db <ABS path>.
- JUDGMENT CALLS: s16 swept them -- budget/M7 RULED (25:00
  full-walk), close calls 2a-2d RULED, sibling wording RULED,
  E-item lines RULED, flow markers RULED. The budget figure
  was an agent derivation later ratified verbatim by James.
- FIRM-LOCAL DATES RULING (s12 cont): business dates stamp
  firm-local, timestamps UTC. Proven live in attempt 5.
- Pre-close dbs (retained walk dbs except -08, -09b) FAIL LOUD
  on ledger writes and /billing/close (missing period_closes --
  deliberate). migrate_period_close.py before serving one;
  pre--08 dbs are PRE-ENGINE; pre-07c also need
  migrate_invoice_codes.py. check_demo_walk FAILS any
  pre-Part-K walked db on the close receipt -- correct.
- s11 double-bind protocol: netstat before blaming the db;
  single bind verified at the s16 recovery restart.
- The no-logic lint counts the WORD "SELECT" in app_ui prose.
- billing + fiduciary + anchor-billing run from
  ../casework-billing/; spine from ../casework/; core touches
  trigger the reciprocal guard (ALL suites). period.py imports
  the recon oracle LAZILY.
- drive_sheet.py preflights now: DATE COUPLING + BUDGET
  COUPLING (both exit 2 before the drive).
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

- THE VERDICT: attempt 5's three sub-verdicts (a) fiduciary
  story lands, (b) nothing embarrassing, (c) bookable -- James
  signs when his review is done. Everything else queues behind
  this.
- Sixth sweep cluster: unverified from the s16 log whether it
  was deferred or never reached -- re-offer the judgment-call
  map when James next engages.
- Budget figure re-rule: 25:00 was agent-derived then ratified
  ("25 is good!") -- closed unless James reopens.
- Client portal: gated item 11, deliberately out of scope.
