# plan.md -- casework-ui

Agent-owned strategy; rewritten freely, judged by results. Phase
detail is COARSE by design -- each phase's units are drafted and
red-penned at its supervised gate (which includes the screen
eyeball, ruling 1), not here. DRAFT until goal.md ratifies.

## Phase roster (invariant order)

| Phase | Delivers                                | Gate output          |
| ----- | --------------------------------------- | -------------------- |
| 0     | UI server skeleton importing casework   | Screen review 1:     |
|       | app package; first-run admin setup +    | login, MFA, empty    |
|       | MFA + login/session over cookies; app   | dashboard. Verifier  |
|       | shell (nav, layout); verify/            | 1 skeleton runs red  |
|       | run_ui_walk.py skeleton (oracle-first,  |                      |
|       | red); no-logic + JS-discipline sweeps   |                      |
| 1     | Anchor-path screens: contact create/    | Screen review 2:     |
|       | detail, matter create/detail, form      | walk the anchor by   |
|       | package + invitation send, intake       | hand together; UI    |
|       | review, G-28 render/download, calendar  | walk green through   |
|       | + deadline visibility                   | the story            |
| 2     | Browse-grade surfaces: indexes +        | Screen review 3:     |
|       | detail pages (contacts, matters,        | free-click session   |
|       | files, tasks, events, notes), search,   | on seeded db; browse |
|       | read-only settings; browse sweep green  | sweep green          |
| 3     | Hardening: full verifier-1 x2, James    | Rehearsal findings   |
|       | rehearsal run (non-proof), friction     | ruled on; cold-run   |
|       | fixes, cold-run-protocol.md ratified    | protocol ratified    |
| 4     | Cold run(s) until one passes; findings  | Both verifiers pass; |
|       | logged; result.md; wind-down            | wind-down            |

## Standing tactics

- Oracle-first: run_ui_walk.py steps exist red before their
  screens (op rule 7).
- Paper-design (wireframe-in-text) before code inside each unit;
  screenshots to disk at unit close for the gate package.
- UI reads/writes ONLY through casework modules; assertion-only
  db access in verifiers.
- Cheapest-reversible choice + log where feedback is absent;
  churn counters per unit.
- Every JS addition logs its per-screen justification at the
  moment it lands (log-don't-build's writing-act trigger).

## Phase 2 units (DRAFT for gate ratification)

P0 and P1 unit tables were ratified and executed; their record is
the worklog (P0: 2026-08-01 gate; P1: ratified as drafted, churn
0). Screen review 2 PASSED 2026-08-02 with a navigation-cluster
finding that shapes this phase: P1 proved the path is clickable,
not that the space is navigable. P2's sweep therefore asserts
REACHABILITY and EMPTY STATES, not just seeded rendering.

Order is dependency order: U2.1's indexes are the click-paths
U2.2's details hang off; U2.3 search and U2.4 settings are leaf
surfaces; U2.5 sweeps everything the earlier units produced.

| Unit | Delivers                                 | Done when            |
| ---- | ---------------------------------------- | -------------------- |
| U2.1 | Indexes go live: contacts, matters,      | every nav item lands |
|      | files, tasks, notes index screens        | on a real screen; no |
|      | (calendar already live); nav stubs       | "Not built yet" left |
|      | replaced; dashboard counter line         | behind the nav;      |
|      | becomes links; every index renders a     | dashboard counters   |
|      | designed empty state (review-2 finding   | click through to     |
|      | 1), person AND company contacts render   | their indexes        |
| U2.2 | Detail pages for browse-new entities:    | every row on every   |
|      | files, tasks, notes (contact/matter/     | index clicks through |
|      | event details exist from P1); cross-     | to a detail page;    |
|      | links (file -> matter, task -> matter,   | every detail links   |
|      | note -> subject) so no entity is a       | back to its matter/  |
|      | click dead-end                           | contact              |
| U2.3 | Search: nav search screen riding         | seeded-db queries    |
|      | casework's universal-search module       | return expected      |
|      | (contacts, matters, forms, receipt       | rows; zero-result    |
|      | numbers); results link to detail pages;  | query renders a      |
|      | empty query and zero-result states       | designed empty state |
|      | designed                                 |                      |
| U2.4 | Read-only settings: firm profile +       | settings screen      |
|      | preparer info + user list displayed      | renders from seeded  |
|      | from casework modules; explicit "edits   | db; no form elements |
|      | are out of v1 scope" surface note        | present (read-only   |
|      | (WRITE screens stay out per P1 ruling)   | by construction)     |
| U2.5 | Browse sweep green + gate package:       | ui-walk exits 0 for  |
|      | sweep asserts (a) every surface renders  | the FIRST time (12+  |
|      | on the SEEDED db, (b) every surface      | browse = all pass);  |
|      | renders its EMPTY state on a fresh db,   | sweeps pass; screen- |
|      | (c) REACHABILITY: every seeded entity    | shots + churn counts |
|      | reachable by clicks from the dashboard   | packaged; SCREEN     |
|      | (BFS over anchor tags); SCREEN REVIEW 3  | REVIEW 3 (free-click |
|      | (supervised free-click on seeded db)     | session)             |

Design notes (agent territory, logged): (1) reachability check is
assertion-only -- a link-graph BFS from / over rendered HTML, no
casework writes; it lands in the browse sweep, not a new runner.
(2) Contact CREATE form stays person-only (P1 ruling); companies
appear browse-grade only. (3) Search scope is contacts + matters
for v1 -- files/tasks/notes search is a P3-candidate friction
item, not owed here. (4) no-logic lint discipline unchanged: new
readers are SELECT-only in reads.py; sweeps ALLOWLIST carries its
1 named exemption.

## Phase 3 units (DRAFT for gate ratification)

P2 closed: screen review 3 PASS 2026-08-03, walk GREEN exit 0.
P3 is hardening + the bridge to the human verifier: the cold-run
protocol becomes an artifact, James rehearses AGAINST that
artifact (testing the task sheet as much as the UI), and the two
queued questions get ruled at the gate with rehearsal data in
hand: (a) goal.md's ratification deferral -- does the first-run
account ceremony count inside the cold user's 15-minute budget;
(b) does the task sheet need preparer fields.

Order: protocol draft precedes rehearsal by design -- the
rehearsal exercises the task sheet and recording form, not just
the screens.

| Unit | Delivers                                 | Done when            |
| ---- | ---------------------------------------- | -------------------- |
| U3.1 | Hardening: CLOCK GAUNTLET -- verify/     | gauntlet exit 0:     |
|      | run_clock_gauntlet.py runs the UI walk   | every verifier green |
|      | AND casework's spine + anchor in         | under every clock;   |
|      | subprocesses under adversarial fake      | report written; any  |
|      | clocks (pre-09Z, post-09Z, +400 days,    | casework red is a    |
|      | midnight straddle, New Year's Eve        | FLAG, never a fix    |
|      | straddle); plus verifier-1 x2 back-to-   | from here; walk x2   |
|      | back on the real clock (completion-      | receipts logged      |
|      | proof form)                              |                      |
| U3.2 | cold-run-protocol.md DRAFT: task sheet   | draft on disk with   |
|      | (fake client story, synthetic data       | the two DECISION     |
|      | card), rules (fresh db, unassisted,      | boxes framed for     |
|      | stopwatch from first login screen),      | the gate; recording  |
|      | recording form, pass criteria; the two   | form usable as-is    |
|      | queued questions framed as DECISION      | in a rehearsal       |
|      | boxes with options + evidence needed     |                      |
| U3.3 | SUPERVISED rehearsal: James runs the     | rehearsal recorded   |
|      | draft task sheet on a fresh db,          | on the form: wall    |
|      | stopwatch on, recorded on the draft      | clock, per-step      |
|      | form (non-proof by contract); friction   | times, friction      |
|      | observations captured per the form      | list                 |
| U3.4 | Friction rulings + fixes: each           | findings table       |
|      | rehearsal finding ruled keep/fix at the  | ruled; ruled fixes   |
|      | gate; ruled fixes applied; walk re-run   | applied; walk GREEN  |
| U3.5 | Gate package: protocol RATIFIED with     | protocol ratified;   |
|      | rulings (a) and (b) inked; P4 unit       | P4 units drafted     |
|      | draft (cold runs + result.md)            |                      |

Design notes (agent territory, logged): (1) rehearsal db is FRESH
(goal.md fixture posture allows the casework seed for rehearsals,
but the deferral question needs setup-ceremony timing data, so
the rehearsal must include the ceremony). (2) Clock gauntlet
mechanism, proven by prototype 2026-08-03: a subprocess shim
replaces datetime.datetime with an offset subclass BEFORE any
app/verifier import, so app and verifier share one consistent
fake clock -- exactly the cold-user invariant (one machine, one
clock). Stdlib only, zero app-code edits, zero new dependencies.
The tested property: verifiers are green under ANY single
consistent clock. Each gauntlet run ends with a real-clock pass
so the reports on disk stay truthful. Runs at phase close (P3)
and inside P4's completion proof, not on every walk.

## Phase 4 units (DRAFT for gate ratification)

P3 closed at the 2026-08-03 gate: gauntlet GREEN 19/19, protocol
hardened by rehearsal 1's findings (db-artifact pass criteria via
check_cold_run.py), decisions (a) M1->M5 budget and (b) no
preparer step both RULED. P4 is the contract's endgame: one
passing cold run, completion proof, result.md.

| Unit | Delivers                                 | Done when            |
| ---- | ---------------------------------------- | -------------------- |
| U4.1 | Cold run(s): James recruits the runner   | one run with: form   |
|      | (Approval-required lane -- agent never   | complete, zero       |
|      | recruits); James proctors per protocol;  | assist violations,   |
|      | agent supports setup only. FAIL loops    | M1->M5 within 15:00, |
|      | per contract: findings logged, fixes     | check_cold_run exit  |
|      | ruled at a mini-gate, re-recruit         | 0, PDF + calendar    |
|      |                                          | verified             |
| U4.2 | Completion proof assembly: fresh walk    | every goal.md        |
|      | x2 receipts, clock gauntlet green,       | completion-proof     |
|      | foundation green (spine + anchor),       | path exists with     |
|      | cold-run-report.md carrying the passing  | receipts quoted from |
|      | run's form                               | THIS phase's runs    |
| U4.3 | result.md (only after both verifiers     | result.md written;   |
|      | pass) + final wind-down self-audit       | self-audit answered; |
|      | (goal.md's four questions) + program     | atlas roster row     |
|      | roster update                            | flipped              |
## Next actions

1. James ratifies the cold-run protocol + P4 unit table (gate).
2. U4.1 blocks on James recruiting a cold runner.
