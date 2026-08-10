# P1 gate receipt -- Calendar (hands-on)

Verdict: PASS, signed by James 2026-08-10 ("Yes we are done"), at
the end of a live drive on port 8500 over a fresh-seeded
data/demo-tabs.db.

## The drive and its fix rounds

James drove the month grid and agenda hands-on with snaps; four
gate-fed fix rounds landed during the drive, each rerun green
before he continued:

| Round | Commit  | Axis        | Change                             |
| ----- | ------- | ----------- | ---------------------------------- |
| r1    | 3a899e9 | spacing     | When column stacks date over muted |
|       |         |             | time; Linked = one matter-first    |
|       |         |             | link; month cells dot + title      |
| r2    | fd05d70 | spacing     | 20-char chop -> CSS ellipsis (did  |
|       |         |             | not engage; caught by James's snap)|
| r3    | 0fe8d3c | spacing     | table-layout fixed (ellipsis now   |
|       |         |             | real), wide month canvas (92rem),  |
|       |         |             | color KEY legend under the grid    |
| r4    | 6903336 | typography  | agenda table unified at 0.85rem;   |
|       |         |             | calendar links firm blue always    |

James on r3: "We got the spacing right." Typography ruling (r4)
was his: one size for all table text (the Linked size), links
blue always.

## Mechanical floor at verdict time (full step table -- METHOD
rule s3: the verdict line alone can hide a marker regression)

Rail sha d1a45962 (verify/report_sha.py), run of
2026-08-10T11:45:18Z:

    PASS    setup + login
    PENDING empty states designed (fresh db)   [/files /tasks /notes remain]
    PASS    client + matter (existing UI)
    PASS    calendar: new appointment
    PASS    calendar: new deadline
    PASS    calendar: unified view + kind filter
    PASS    calendar: agenda/month toggle
    PENDING calendar: derived kinds [Q]        [awaits Q1 ruling]
    PASS    calendar: provenance links
    PENDING tasks: quick-add + due date        [P2]
    PENDING tasks: my-open default + toggles   [P2]
    PENDING tasks: one-click complete          [P2]
    PENDING tasks: lists builder + import      [P2]
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
    PASS iso-stray-sweep (24 tab pages)
    steps: 7 pass, 23 pending, 0 fail
    verdict: ON TRACK (pending screens)

Every P1 calendar step is PASS except derived-kinds, which is
PENDING by design until [Q1]. All 23 pendings name later phases.

Standing suites at verdict time, quoted: "ui-walk: 13 pass, 0
pending, 0 fail; sweeps pass; verdict GREEN" / "spine: 107 green,
0 red, 0 pending; checks pass" / "billing: 25 green, 0 red, 0
pending, 0 parked ... verdict: GREEN" / "fiduciary: 9 pass, 0
red, 0 stub; verdict: GREEN".

## Ruling queue disposition

James closed the gate without the serialized [Q] walkthrough
(wrap-up call, his time). [Q1]-[Q8] (worklog s3) CARRY FORWARD to
the P2 gate; every one is a decision-default already implemented
one way and stands as built unless re-ruled. [Q1] alone gates a
rail step (derived kinds).

Typography and link-color rulings taken live at this gate (r4)
are RULED, not queued: one table text size, links always blue,
scoped to calendar surfaces (billing tables untouched -- extending
app-wide would touch billing-ui's signed surface and was flagged).
