# state.md -- casework-tabs (session cache, overwritten each wind-down)

## Status

P1 BUILT 2026-08-10 (s3), GATE PENDING. The calendar tab is live to
the rail's contract: unified agenda + month grid (sticky toggle),
six kind chips, two pre-shaped create forms, extended event detail
(attendees, descriptions, MM/DD/YYYY), provenance links, designed
empty state. Rail: 7 pass / 23 pending / 0 fail, ON TRACK, sha
d1a45962 x2 (supersedes e084bd4b). All four standing suites green
and quoted in worklog s3. Frozen casework-ui walk untouched and
green -- /calendar/new, its wording, and the empty-db markers all
preserved.

## Next actions

1. P1 GATE (James hands-on): swap port 8500 from billing-ui's demo
   server (his asset -- his call) to this child's seeded db:
   from casework-ui/,
   python -m app_ui.server --db ../casework-tabs/data/demo-tabs.db
   --port 8500
   Login demo.tabs@synthetic.test / demo-tabs-pass. He drives the
   Calendar tab; verdict PASS or FAIL naming the fix axis; receipt
   to verify/gate-receipts/p1-calendar.md.
2. At the gate, clear the [Q] queue serialized (worklog s3: Q1-Q8,
   one per turn, product first).
3. Then P2 TASKS per plan.md (quick-add, my-open, one-click
   complete, lists builder -- rail steps already pinned).

## Watch items and caveats

- Regenerate the demo db before the gate if it predates the P1
  screens: python verify/seed_tabs.py (content is module-written;
  screens render it either way -- regen is belt-and-braces only).
- METHOD (s3, binding on receipts): gate receipts quote the FULL
  per-step table -- a marker-probe regression demotes to PENDING,
  so the verdict line alone can hide a regressed screen.
- Typed deferral owed: final-walk TIME BUDGET ruled at P7
  walk-sheet ratification.
- casework-ui remains ON HOLD (cold runner); its data/ carries
  real-ish PII -- never seed or demo from it.
- Owed per phase: each tab step's full body + the empty-state FAIL
  arm get a deliberate RED at the phase that builds them (P1's
  five steps: done, worklog s3).
- Parked with triggers: interleaved notes timeline (rendered-
  artifact gate); calendar sync (meeting question); role
  ENFORCEMENT (future contract).

## Open decisions

- [Q1]-[Q8] queued for the P1 gate (worklog s3 has the full list
  with agent leans). None block P2 build work except [Q1], which
  only blocks the derived-kinds rail step, not screens.
