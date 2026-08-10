# result.md -- billing-ui

Written 2026-08-10, after the completion proof was met in full.
Contract: goal.md (ratified 2026-08-04). This file is the
authority on what was achieved; the worklog is the authority on
how.

## Verdict: COMPLETE -- all three outcome clauses met

1. JAMES DROVE THE FULL LIFECYCLE THROUGH SCREENS. Attempt 5,
   2026-08-09 23:43 -> 2026-08-10 00:06 firm-local, all 40
   sheet steps solo on the fresh database
   data/demo-walk-2026-08-09b.db: install -> contact + matter
   -> trust and operating accounts -> trust request -> online
   payment (SimProcessor) -> gross settlement with fee split ->
   invoice (saved charge + imported time entry) -> earn-out
   trust transfer -> disbursement -> invoice PDF -> trust
   ledger and three-way reconciliation visible and holding ->
   period close (Part K, added by ratified sheet amendment).
   No terminal, no SQL, no dev tools mid-walk.
2. FIDUCIARY SUITE GREEN ON THE WALKED DB: "fiduciary: 9 pass,
   0 red, 0 stub; verdict: GREEN" (F1-F9; the suite GREW from
   the contract's F1-F8 during the ruled F7 real-bank-matching
   and F9 period-close strengthenings -- checks strengthened,
   never weakened). Close-out: check_demo_walk.py 13/13 PASS,
   exit 0, closed periods ['2026-07'].
3. DEMO-GRADE VERDICT SIGNED 2026-08-10: (a) fiduciary story
   lands PASS, (b) nothing embarrassing PASS, (c) bookable
   PASS. Record: verify/demo-walk-report.md.

## Completion proof (goal.md table, checked on disk 2026-08-10)

| Path                              | Proof                     |
| --------------------------------- | ------------------------- |
| verify/billing-ui-walk-report.txt | GREEN exit 0, x2          |
|                                   | byte-identical: "21 pass, |
|                                   | 0 pending, 0 fail; float- |
|                                   | sweep pass; verdict       |
|                                   | GREEN", report_sha.py =   |
|                                   | b3aa0a03 both runs        |
| verify/demo-walk-protocol.md      | Ratified 2026-08-05       |
|                                   | before first use; eight   |
|                                   | in-file amendments, each  |
|                                   | ruled; lock 7b30fc89c159  |
| verify/demo-walk-report.md        | James PASS + three-part   |
|                                   | verdict + friction log    |
| data/demo-walk-2026-08-09b.db     | The walked db, retained   |
|                                   | (with -04, -04b, -07,     |
|                                   | -07b, -07c, -08, -09)     |
| verify/gate-receipts/             | Per-gate receipts, gates  |
|                                   | 0-3                       |
| result.md                         | This file, written last   |

## Final suite state (all run 2026-08-10, quoted)

| Suite                         | Result                        |
| ----------------------------- | ----------------------------- |
| billing-ui walk (this child)  | 21 pass, 0 pending, 0 fail;   |
|                               | float-sweep pass; GREEN       |
| drive-sheet (sheet coupling)  | 27/27 groups pass; GREEN      |
| sheet labels                  | 92 labels checked, 0 missing  |
| ui-walk (casework-ui, frozen) | 13 pass, 0 pending, 0 fail;   |
|                               | sweeps pass; GREEN            |
| spine (casework, frozen)      | 107 green, 0 red, 0 pending   |
| billing parity                | 25 green, 0 red, 0 pending,   |
|                               | 0 parked; GREEN               |
| fiduciary (--seeded)          | 9 pass, 0 red, 0 stub; GREEN  |
| anchor-billing                | PASS (1.274s of 900s budget)  |

## What this child built (visibility, not capability)

Billing screens over the frozen casework core in casework-ui/
app_ui (program in-place-extension ruling 2026-08-03): the
tier-1/2 surfaces of all 25 corpus entries, the status-page
home screen + flow markers + client summary (gated item 12),
and -- under ratified cross-project amendments -- the F7
real-bank-matching recon engine, the period-close act
(casework/app/period.py + lock guard), the styled client
invoice/pay/receipt surface, and invoice display codes. Every
extension ran under its own program ruling with hard limits;
spine tests were never modified; fiduciary checks only
strengthened. Sha supersession lineage recorded in the worklog
throughout (final walk-report sha b3aa0a03).

## Boundaries (what this result does NOT claim)

- No cold-run claim: the oracle was a James-driven demo walk by
  contract. Cold users are casework-ui's parked question.
- No real-money claim: SimProcessor is synthetic; payments/rake
  remains a deliberately untriggered strategic flag (gated
  item 9).
- The client portal (gated item 11) is out of scope by ruling;
  the pay surface is per-invoice share tokens only.
- Parked/gated pool at close: gated-items.md is the ledger
  (items 6, 7, 8, 9, 11 open program-side; none owed by this
  contract).

## Successor decisions (new conversations, not queued work)

The firm meeting itself; any attempt to demo to a cold driver;
the payments/rake business decision; the client portal as its
own contract; casework-ui's cold-run resumption. The program
roster row flips to COMPLETE with this file.
