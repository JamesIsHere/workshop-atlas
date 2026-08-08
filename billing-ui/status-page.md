# status-page.md -- item-12 home-screen design (RATIFIED 2026-08-08)

Created 2026-08-08 s10 during the item-12 design gate. Numbered
elements; James marks by number. Rulings recorded here AND in
worklog s10 cont. Precedent: invoice-codes.md (s8).

Standing rulings shaping this page:
- R1: recon is a standing condition; humans own exceptions and
  period close only.
- R2: this page IS the home screen at "/" (replaces the old
  dashboard; keeps the Dashboard name and the frozen walk's
  reachability -- constraints verified against run_ui_walk.py).

## The sketch

```
DASHBOARD  (period: August 2026, ties as of 08/08/2026)
+----------------------+----------------------+----------------------+
| TRUST (IOLTA)        | OPERATING            | CLIENT FUNDS HELD    |
| $800.00      [HOLDS] | $3,349.70    [HOLDS] | $800.00  (1 client)  |
| Ledger  Reconcile    | Ledger  Reconcile    | -> by client         |
+----------------------+----------------------+----------------------+

NEEDS ATTENTION
  - 1 check outstanding 0 days   (disbursement 1,200.00, e5)
  - 1 deposit in transit         (settlement 5,000.00, e2)
  - 2 bills outstanding          ($X total, oldest MM/DD)
  - 2.0 hrs unbilled time        ($500.00 at current rates)
  (empty state: "Nothing needs you. Everything ties.")

RECENT ACTIVITY
  08/08  payment received  B0003  $3,000.00   (client, online)
  08/08  disbursement      trust  ($1,200.00) (you)
  ...last ~8 events, each linking to its record

PRACTICE
  New client  New matter  Calendar
  4 clients  4 matters  ... (the six count-links)
```

## Numbered elements (mark by number)

 1. HEADER: page keeps the name Dashboard (frozen-suite string);
    carries the current period and "ties as of <date>" computed
    the same way the recon computes its default period. No close
    act in v1 (queued decision).
 2. TRUST TILE: IOLTA balance, recon verdict chip (HOLDS or the
    break), Ledger + Reconcile as prominent controls (kills the
    step-29 "always miss them" friction).
 3. OPERATING TILE: same shape as 2.
 4. CLIENT FUNDS TILE: total client money held + client count --
    the claims leg of the three-way, firm-wide. OPEN: where its
    "by client" link lands (no by-client page exists yet; object
    3 territory).
 5. NEEDS ATTENTION: the R1 exceptions-and-judgment queue --
    uncleared bank items with age, outstanding bills with oldest
    date, unbilled time at current rates. Each line links to its
    record.
 6. EMPTY STATE of 5: "Nothing needs you. Everything ties." --
    the product's thesis sentence; deliberate, not filler.
 7. RECENT ACTIVITY: last ~8 events with date, what, amount,
    actor (attribution already exists in the ledger); each line
    links to its record.
 8. PRACTICE ROW: absorbs the old dashboard verbatim -- New
    client / New matter / Calendar actions + the six count-links
    (clients, matters, events, files, tasks, notes). Also
    satisfies the frozen walk's reachability sweep.
 9. ORDER OF SECTIONS: money verdict first, exceptions second,
    narrative third, practice last -- the controller's question
    outranks the receptionist's.

## Rulings on elements (filled as James marks)

- R3 (2026-08-08, elements 2-4): VERDICT CHIP on the tiles; the
  tie-out equation stays one click away. James: "That's not
  summary and in fact the person that needs that is going to be
  able to find it and look for it." On a BREAK day the chip
  goes red and carries the difference.
- R4 (2026-08-08, element 4): the client-funds tile links to
  the reconciliation page's CLIENT CLAIMS pane in v1; the link
  upgrades to the client summary page when object 3 builds it.
  Never a dead tile.
- R5 (2026-08-08, elements 5-6): OPTION A -- two levels. NEEDS
  ATTENTION holds only real problems (recon break, bill past
  due, stale check, aged unbilled time) and is empty most days;
  empty state "Nothing needs you. Everything ties." Routine
  movement collapses to one quiet IN FLIGHT count line, each
  count linking to its list. Thresholds (stale-check days, bill
  terms, unbilled age): sane defaults now, settings later --
  flagged, not debated.
- R6 (2026-08-08, element 7): RECENT ACTIVITY is money events
  only in v1 (payments, disbursements, corrections -- ledger
  data with actors). All-firm activity would need event sources
  that do not exist yet.
- R7 (2026-08-08, elements 1 + 8 + 9): approved as sketched --
  header keeps the Dashboard name with period + ties-as-of
  line, practice row absorbs the old dashboard verbatim,
  section order money / attention / activity / practice.
  SHEET SIGNED by James ("She is signed") -- design RATIFIED;
  build may proceed under ruling R2's scope and hard limits.

## Build record (2026-08-08 s10, same session)

BUILT as ratified: app_ui/billing_ui.py dashboard_screen +
reads.recent_money_entries + nav/brand chrome + server
delegation; billing-ui walk step 18 (step_home_status) asserts
the ratified elements. All suites green (quoted in worklog
s10); walk-report sha 28a19170 supersedes 301b574d.
R5 threshold defaults chosen (flagged, settings later):
STALE_CHECK_DAYS = 30, UNBILLED_NAG_DAYS = 30; past-due uses
the bill's own due date when set.

## Explicitly OUT of v1 (queued decisions, do not fold in)

- Period-close ACT (lock a month) -- new core logic, own gate.
- Client/matter summary layer (object 3).
- Flow markers on object screens (object 2).
- Client portal (gated item 11).
