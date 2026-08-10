# state.md -- casework-tabs (session cache, overwritten each wind-down)

## Status

P0 COMPLETE 2026-08-10 (s2). The harness is on disk and proven:
verify/run_tabs_walk.py (30 steps, RED as contracted: 2 pass /
28 pending / 0 fail, exit 1, verdict ON TRACK, sha e084bd4b x2),
verify/seed_tabs.py (demo db green, all six calendar kinds
represented), verify/report_sha.py (canonical sha). Four
verify-the-verifier sabotages driven RED and reverted. All four
standing suites rerun green and quoted in the worklog. No app_ui
file touched -- oracle-first held.

## Next actions

1. P1 CALENDAR: build to the rail's pinned contract --
   /calendar/new-appointment, /calendar/new-deadline, unified view
   with kind-<kind> row classes + ?kind= filter, ?view= toggle
   (sticky, month-grid marker), provenance links, designed empty
   state. Per-phase rhythm: extend/refine the calendar steps,
   drive each RED once, build to green, sweeps green, suites
   green, then the P1 hands-on gate (seeded db on port 8500).
2. [Q1] rides to the P1 gate (see worklog s2): content path for
   derived calendar kinds in a UI-only walk.

## Watch items and caveats

- Gate decision already typed for P5: the chrome search bar grows
  shared chrome (html.py) -- authorized additively by goal.md,
  ruled at the owning phase's gate.
- Typed deferral owed: final-walk TIME BUDGET is ruled at P7
  walk-sheet ratification (billing-ui's 25:00 is precedent).
- billing-ui's demo server may still be UP on port 8500 over the
  walked -09b db (James's asset). Gate dbs here are fresh
  seeded dbs (data/demo-tabs.db, regenerable); coordinate the
  port at gate time.
- casework-ui remains ON HOLD (cold runner); its data/ carries
  real-ish PII -- never seed or demo from it.
- Owed per phase: each tab step's full body + the empty-state
  FAIL arm get a deliberate RED at the phase that builds them.
- Parked with triggers: interleaved notes timeline (rendered-
  artifact gate, named idea); calendar sync (meeting question);
  role ENFORCEMENT (future contract).

## Open decisions

- [Q1] derived-kinds content path -- queued for the P1 gate, not
  blocking the P1 build (the step probes markers only until ruled).
