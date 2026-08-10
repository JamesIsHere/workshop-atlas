# state.md -- billing-ui (session cache, overwritten each wind-down)

## COLD-START POINTER (s14, 2026-08-10)

ATTEMPT 5 WAS DRIVEN AND RECORDED; THE VERDICT IS PENDING.
James drove all 40 steps solo on data/demo-walk-2026-08-09b.db
(sheet lock 85e4e4633a37), 23:43-00:06 firm-local 08/09->08/10.
Close-out ran green this session: check_demo_walk.py on the
walked db = 13/13 PASS, fiduciary 9/0/0 GREEN, closed periods
['2026-07'], exit 0. All 32 snaps (Desktop/snaps, steps 15-40)
reviewed and matched. Marks M1->M6 = 16:56 (UNDER the 20:00
soft budget, first time); M1->M7 = 22:33 (data). Full record:
worklog s14. James's reaction: "This looks pretty good. I have
to sit with it a while and click around for UI" -- he is
REVIEWING; the three sub-verdicts (a)/(b)/(c) are unsigned.
At wind-down he added, verbatim: "I think it's good for a
meeting but I still want to do more work before the meeting
because I still think there's more we can do." Read that as a
LEAN toward (c) bookable, NOT a signature -- and as notice
that a more-work round is coming before any firm meeting. The
next session should expect BOTH: take the formal verdict when
offered, and be ready to scope the more-work round (friction
items, open flags, gated items are the natural candidate
pool).

A resumed session's FIRST job: ask nothing until he volunteers;
when he is ready, take the three-part verdict (a) fiduciary
story lands, (b) nothing embarrassing, (c) bookable -- each
up/down, then P4 closes on his sheet, not before. If he signs
PASS, next is the goal.md close-out (result.md etc. per
contract). If any axis FAILs, the failed-axis reason drives the
next build round, attempt 6 under the standard protocol.

## Status

P4 OPEN. Attempt 5 driven 2026-08-10, record filed (worklog
s14), close-out verifier green and quoted, VERDICT PENDING
James's sit-with-it review. Nothing advances past P4 on
"looks pretty good" -- signed sheet only.

## Watch items and caveats

- Server UP on 8500 over the WALKED attempt-5 db
  data/demo-walk-2026-08-09b.db -- deliberately left up for
  James's review clicking. It is now a walked artifact
  (delete=archive; retained set grows to -04, -04b, -07, -07b,
  -07c, -08, -09, -09b). Do NOT reseed or swap it while his
  review is open. Preview db demo-billing.db remains the
  alternate for gate reviews (verify/seed_demo.py; reseeds wipe
  sessions: demo.reviewer@synthetic.test / demo-seed-pass).
  Swap dbs behind the port, never the port. Restart after ANY
  app_ui or casework/app change. Launcher:
  python billing-ui/serve.py --db <ABS path>.
- FRICTION LOG from attempt 5 (all minor, worklog s14): step-17
  checkpoint conditional read as unconditional stop (sheet
  wording); step-27 Note field not in the sheet, James filled
  it; step-39 refusal clears the form's typed values (product
  polish). None is a stop-rule event; all are candidate work
  if James rules them in.
- JUDGMENT CALLS still open for re-rule: M7/soft-budget
  handling (kept M1->M6 for comparability); PC1 refusal renders
  the period ISO-style ("period 2026-07...") in an MM/DD/YYYY
  surface (core-owned text, casework/app/period.py, inside the
  standing close amendment's write surface).
- FLAGS from s13 sweep, frozen casework-ui screens (gate
  decisions): contact detail card shows raw machine keys as
  labels (bio.family_name etc.); contact Matters card prints
  ISO dates vs MM/DD/YYYY.
- FIRM-LOCAL DATES RULING (s12 cont): business dates stamp
  firm-local, timestamps UTC. Proven live in attempt 5: the
  close signatures stamped 08/10/2026 when James crossed
  midnight mid-walk.
- Pre-close dbs (retained walk dbs except -08, -09b) FAIL LOUD
  on ledger writes and /billing/close (missing period_closes --
  deliberate). migrate_period_close.py before serving one;
  pre--08 dbs are PRE-ENGINE; pre-07c also need
  migrate_invoice_codes.py. check_demo_walk FAILS any
  pre-Part-K walked db on the close receipt -- correct.
- s11 double-bind protocol: netstat before blaming the db;
  single bind verified at the attempt-5 close-out.
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

- THE VERDICT: attempt 5's three sub-verdicts (a)/(b)/(c) --
  James signs when his review is done. Everything else queues
  behind this.
- Friction-log items 1-3 (s14): rule in as work or log-only.
- Marks judgment call (M7/budget) and the refusal-message
  wording: James may re-rule.
- Contact-screen flags from s13 (raw labels, ISO dates): gate
  in or leave.
- Dashboard settling backing list: flagged, unruled.
- Close judgment calls (s12): James may re-rule.
- E-item select wording: James may re-rule any line.
- Empty-invoice list behavior (gated item 3): unchanged.
- Demo-login prefill + no-expiry (gated item 5): queued.
- Client portal: gated item 11, deliberately out of scope.
