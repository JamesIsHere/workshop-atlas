# P2 gate receipt -- Tasks (hands-on)

Verdict: PASS, signed by James 2026-08-10 ("PASS!"), at the end of
a live drive on port 8500 over a fresh-seeded data/demo-tabs.db
(reseeded twice during the gate as fixes landed).

## The drive and its fix rounds

James drove the tasks index, builder, and matter cards hands-on
(snaps in his drive confirmed quick-add, check-then-Done, Firm
scope, Completed view, Reopen); four gate-fed rounds landed during
the drive, each rerun green before he continued:

| Round | Commit  | Axis        | Change                             |
| ----- | ------- | ----------- | ---------------------------------- |
| r1    | 306cf0f | typography  | calendar ruling extended to tasks  |
|       |         |             | tables (.tasks-table: 0.85rem td,  |
|       |         |             | links firm blue)                   |
| r2    | c83d9a5 | correctness | stray click dismissed a task ->    |
|       |         |             | complete is check-then-Done        |
|       |         |             | (required checkbox, zero JS);      |
|       |         |             | SUPERSEDES Appendix A one-click    |
| r3    | b71fc03 | correctness | RATIFIED CORE AMENDMENT: tasks.    |
|       |         |             | reopen_task (the one post-freeze   |
|       |         |             | casework touch); Reopen button on  |
|       |         |             | completed rows + detail; full      |
|       |         |             | reciprocal-guard rerun             |
| r4    | c054793 | layout      | Linked column cut to matter-first  |
|       |         |             | single link (P1 ruling extended;   |
|       |         |             | the pair showed in his snaps)      |

r3 is the gate's landmark: James ratified opening the frozen core
("yes I think we have to, it will happen") for exactly one
function; the amendment text lives in atlas/CLAUDE.md.

## Mechanical floor at verdict time (full step table -- METHOD
rule s3: the verdict line alone can hide a marker regression)

Rail sha ae9bdf90 x2 (verify/report_sha.py), run of
2026-08-10T13:24:58Z:

    PASS    setup + login
    PENDING empty states designed (fresh db)   [/files /notes remain]
    PASS    client + matter (existing UI)
    PASS    calendar: new appointment
    PASS    calendar: new deadline
    PASS    calendar: unified view + kind filter
    PASS    calendar: agenda/month toggle
    PENDING calendar: derived kinds [Q]        [awaits Q1 ruling]
    PASS    calendar: provenance links
    PASS    tasks: quick-add + due date
    PASS    tasks: my-open default + toggles
    PASS    tasks: confirm-complete            [incl Reopen, audited]
    PASS    tasks: lists builder + import
    PENDING notes: categories home             [P3]
    PENDING notes: minimal capture + expanded  [P3]
    PENDING notes: matter timeline + pin       [P3]
    PENDING notes: index defaults + filters    [P3]
    PENDING notes: PDF export                  [P3]
    PENDING files: upload + custody            [P4]
    PENDING files: matter section + filters    [P4]
    PENDING files: rename/preview/print/bulk   [P4]
    PENDING files: e-sign flow                 [P4]
    PENDING search: chrome bar everywhere      [P5]
    PENDING search: coverage + grouped results [P5]
    PENDING search: recents                    [P5]
    PENDING settings: users admin              [P6]
    PENDING settings: permissions groups       [P6]
    PENDING settings: trash + restore          [P6]
    PENDING settings: notifications + firm     [P6]
    PENDING settings: machinery homes          [P6]
    PASS float-sweep
    PASS iso-stray-sweep (39 tab pages)
    steps: 11 pass, 19 pending, 0 fail
    verdict: ON TRACK (pending screens)

Every P1 calendar step still PASS (no regression wearing pending's
clothes); every P2 tasks step PASS; all 19 pendings name later
phases or [Q1].

Standing suites at verdict time, quoted (rerun after the r3 core
touch -- reciprocal guard): "spine: 107 green, 0 red, 0 pending;
checks pass" / "billing: 25 green, 0 red, 0 pending, 0 parked;
checks pass; verdict: GREEN" / "fiduciary: 9 pass, 0 red, 0 stub;
verdict: GREEN" / "ui-walk: 13 pass, 0 pending, 0 fail; sweeps
pass; verdict GREEN".

Verify-the-verifier this phase: six RED drives (ISO due render,
missing Completed chip, complete no-op, raw fact key -- which
EXPOSED a vacuous assert, since tightened -- bare empty state =
the owed FAIL arm, reopen no-op). Worklog s4 records the silent
no-op sabotage incident and its METHOD lesson.

## Ruling queue disposition

Four rulings taken LIVE at this gate (r1-r4 above) are RULED, not
queued. [Q12] (undo) was ruled by the r3 ratification.

[Q1]-[Q11] CARRY FORWARD to the P3 gate; each is an implemented
default that stands as built unless re-ruled. [Q1] alone gates a
rail step (calendar derived kinds). [Q9] (due dates are set at
creation only; editing needs another small core amendment, same
shape as Reopen) was flagged to James at the verdict ask and rode
his PASS -- it stands until it bites in use.

Scoping notes carried: typography + single-link rulings now cover
calendar AND tasks surfaces; files/notes tables adopt them when
their phases rebuild those screens; billing-ui's signed tables
stay untouched.
