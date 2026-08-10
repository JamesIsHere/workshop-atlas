# P3 gate receipt -- Notes (hands-on)

Verdict: PASS, signed by James 2026-08-10 ("pass"), at the end of
a live drive on port 8500 over a fresh-seeded data/demo-tabs.db.

## The drive and its fix rounds

James drove the notes index, a note detail, and the Anya matter's
Notes timeline with snaps; the gate opened with a product-purpose
exchange (what is a note FOR -- answered as the case file's
narrative memory: call logs, strategy rationale, firm-wide flags,
protective documentation; workpaper-memo analogy) and two
capability questions answered from corpus + schema ground truth
(PDF export: yes, per matter/client, corpus notes.notes-export;
attachments: no -- absent from corpus/notes.md AND the schema has
no note-file linkage). Two fix rounds landed during the drive:

| Round | Commit  | Axis        | Change                             |
| ----- | ------- | ----------- | ---------------------------------- |
| r1    | 1ca3e3d | layout      | note detail kv link was visited    |
|       |         |             | purple (his snap) -> .tab-detail   |
|       |         |             | scope pins firm blue; billing kv   |
|       |         |             | untouched                          |
| r2    | b253ca0 | orientation | pdf option lived only on the       |
|       |         |             | linked-to page (his snap) -> note  |
|       |         |             | detail gains linkage-scoped export |
|       |         |             | button naming whose notes it       |
|       |         |             | makes; tab-detail blue extended to |
|       |         |             | task + event detail (his task snap |
|       |         |             | showed the same purple; disclosed  |
|       |         |             | passed-screen extension)           |

## Mechanical floor at verdict time (full step table -- METHOD
rule s3)

Rail sha d2c65ac8 x2 (verify/report_sha.py):

    PASS    setup + login
    PENDING empty states designed (fresh db)   [/files remains]
    PASS    client + matter (existing UI)
    PASS    calendar: new appointment
    PASS    calendar: new deadline
    PASS    calendar: unified view + kind filter
    PASS    calendar: agenda/month toggle
    PENDING calendar: derived kinds [Q]        [awaits Q1 ruling]
    PASS    calendar: provenance links
    PASS    tasks: quick-add + due date
    PASS    tasks: my-open default + toggles
    PASS    tasks: confirm-complete
    PASS    tasks: lists builder + import
    PASS    notes: categories home
    PASS    notes: minimal capture + expanded
    PASS    notes: matter timeline + pin
    PASS    notes: index defaults + filters
    PASS    notes: PDF export                  [incl note-page export]
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
    PASS iso-stray-sweep (46 tab pages)
    steps: 16 pass, 14 pending, 0 fail
    verdict: ON TRACK (pending screens)

Every P1-P3 step PASS except derived-kinds ([Q1] by design); all
14 pendings name later phases.

Standing suites at verdict time, quoted: "spine: 107 green, 0
red, 0 pending; checks pass" / "billing: 25 green, 0 red, 0
pending, 0 parked; checks pass; verdict: GREEN" / "fiduciary: 9
pass, 0 red, 0 stub; verdict: GREEN" / "ui-walk: 13 pass, 0
pending, 0 fail; sweeps pass; verdict GREEN".

Verify-the-verifier this phase: timeline-pin step REFINED BEFORE
build (P2 vacuity lesson applied up front: ordering made
observable) and the pin-no-op sabotage proved the catch; seven
RED drives total (categories no-op, capture no-op, pin no-op,
filter ignored, fake PDF, suppressed note-page export, plus the
refined-assert proof).

## Ruling queue disposition

Rulings taken LIVE (r1-r2) are RULED. The blue-link and
single-link rulings now cover calendar, tasks, AND notes
surfaces including all three detail pages.

[Q1]-[Q11] + [Q13] (raw ISO inside the core's PDF export -- core
amendment or accept) CARRY FORWARD to the P4 gate.

PARKED with trigger (log-don't-build; James moved on without
ruling): note ATTACHMENTS -- exceeds the Docketwise bar (absent
from corpus and schema); trigger: the final cross-tab walk or
real use shows notes constantly narrating documents they cannot
reach. Single-note PDF parked beside it (same core-amendment
family as [Q9] due-date editing).
