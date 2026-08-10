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
4. MISUSE PASS (s6 retro rule): per new flow, deliberately drive
   wrong-order / double-submit / empty-submit / skip-a-step and
   assert refusal or safe handling; write the naive walkthrough
   (clicks-to-goal, visibility from where the user stands).
   Machine-findable holes never reach the human gate.
5. [Q] ruling queue to the gate; James hands-on drives; verdict.
6. Receipt in verify/gate-receipts/; worklog + state.md.

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
- U2.2 DONE 2026-08-10 (s4): P2 gate PASSED live -- 4 fix rounds
  (typography, confirm-complete supersedes one-click, RATIFIED
  reopen_task core amendment + reciprocal-guard rerun, single
  link); sha ae9bdf90 x2; receipt p2-tasks.md; [Q12] ruled,
  [Q1]-[Q11] carry.
- U3.1 DONE 2026-08-10 (s5): notes rail refined (timeline-pin
  ordering made observable) + five steps green, 5 RED drives,
  sha 157f5ac1 x2, suites green, demo reseeded, 8500 up.
- U3.2 DONE 2026-08-10 (s5): P3 gate PASSED live -- 2 fix rounds
  (tab-detail blue links; note-page linkage-scoped export);
  purpose + capability exchange answered from corpus/schema;
  sha d2c65ac8 x2; receipt p3-notes.md; attachments + single-note
  PDF parked w/ triggers; [Q1]-[Q11]+[Q13] carry.
- U4.1 DONE 2026-08-10 (s6): files rail refined four->five steps
  (e-sign split prepare/sign; unpassable outbox-URL assert +
  vacuous PK-magic zip assert fixed from ground-truth reads) +
  P4a mechanics built green (upload/custody, matter+contact
  sections, index filters, rename/preview/print/bulk), 3 RED
  drives, sha 81168b79 x2, suites green, demo reseeded, 8500 up.
- U4.2 DONE 2026-08-10 (s6): P4a gate PASSED ("yes pass"), zero
  fix rounds (first gate with none); ingestion question answered
  closed from corpus+schema (Files is custody, not ingestion; IQ
  has no spine footprint); disclosures accepted with "as is";
  receipt p4a-files.md.
- U4.3 DONE 2026-08-10 (s6): P4b e-sign built to the two refined
  rail steps (prepare POST + editor, live client_base links,
  sign-through on the frozen client surface, produced custody);
  2 RED drives caught; sha c44c5e31 x2; suites green; 8500 up.
- U4.4 P4b gate IN PROGRESS 2026-08-10 (s6, PAUSED -- James's
  energy spent): 8 fix rounds landed and rail-proven (r1
  preview/print collapse, r2 field remove + coord hint, r3
  RATIFIED typed-name amendment, r4 void/redo, r5 empty-send
  guard, r6 field-less guard + vacuous-signature catch, r7 link
  orientation, r8 ONE-CLICK Request signature + dup guard);
  sha 698eca26 x2. Resume: his 3-click drive (state.md),
  verdict + receipt (r1-r8 table) closes P4.
