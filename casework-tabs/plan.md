# plan.md -- casework-tabs (agent-owned strategy; rewritten freely)

Goal RATIFIED 2026-08-10; this phase order is now the working
strategy -- order changes are Approval-required per goal.md.

## Phase order and rationale

P0 HARNESS: verify/ scaffold -- run_tabs_walk.py skeleton (walk
   driver + report + sha script, patterned on billing-ui's rail),
   seed script for a tabs demo db (calling casework/app modules
   only), float/ISO/empty-state sweeps. Oracle-first: the walk
   rail exists and runs RED before any screen changes.
P1 CALENDAR: biggest design lift, most new value; unified view +
   two views + two create forms + provenance rows. Event default
   reminders config ships here (its machinery home arrives in
   Settings phase; interim: seeded defaults).
P2 TASKS: quick wins on ruled requirements; Task Lists builder
   ships HERE (machinery home), since the tab is hollow without
   imports. My-open default, type-and-Enter, one-click complete,
   matter/contact sections.
P3 NOTES: minimal capture + timeline + pins + filters; categories
   management ships here. PDF export wired to existing core.
P4 FILES: matter-centric sections + firm index + upload/rename/
   preview/print/bulk. E-SIGN staged as its own gate within the
   phase (prep editor is the single biggest UI lift; gate P4a
   files mechanics, P4b e-sign flow).
P5 SEARCH: chrome bar (additive shared-chrome change, gate-ruled),
   widened coverage readers, recents, grouped results.
P6 SETTINGS: Users/Permissions/Trash(central + links)/
   Notifications/Firm basics + collect the machinery homes built
   in P1-P3 into the Settings layout.
P7 FINAL: walk sheet drafted + ratified, cross-tab walk attempts
   to signed verdict, x2 report, result.md, retro rides the final
   wind-down (checklist item 6).

Machinery-home note: each home (task lists, categories, reminder
defaults) is BUILT in its owning tab's phase and RE-HOMED into the
Settings layout at P6 -- avoids P6 blocking P1-P3.

## Per-phase rhythm (every tab phase)

1. Extend run_tabs_walk.py with the tab's steps; drive RED.
2. Build screens/readers to green; sweeps green.
3. Standing suites rerun green, quoted.
4. [Q] ruling queue to the gate; James hands-on drives; verdict.
5. Receipt in verify/gate-receipts/; worklog + state.md.

## Unit queue (current)

- U0.1 DONE 2026-08-10 (s2): rail RED (sha e084bd4b x2), seed
  green, sha script canonical, four sabotages proven, suites green.
- U1.1-U1.3 DONE 2026-08-10 (s3): calendar built to the rail, five
  steps green + driven RED, sha d1a45962 x2, suites green.
- U1.4 P1 gate: port-8500 swap (James's call), hands-on verdict,
  [Q1]-[Q8] serialized, receipt in verify/gate-receipts/.
- U2.1 DONE 2026-08-10 (s4): tasks rail refined (due-setter gap,
  vacuous-assert catch) + four steps green, 5 RED drives incl the
  empty-state FAIL arm, sha eb4fc42e x2, suites green, demo
  reseeded (automation linkage content), 8500 up.
- U2.2 P2 gate: hands-on verdict, [Q9]-[Q11] + carried [Q1]-[Q8]
  serialized, receipt in verify/gate-receipts/p2-tasks.md.
- U3.x Notes phase queues after the gate.
