# P4a gate receipt -- Files mechanics (hands-on)

Verdict: PASS, signed by James 2026-08-10 ("yes pass"), after a
drive on port 8500 over a fresh-seeded data/demo-tabs.db ("Yeah
this looks good. I like the Files page as is.").

Scope of this staged gate: upload + custody, matter/contact files
sections, firm index with filters, rename/preview/print/bulk zip.
The e-sign flow is the P4b stage and stays gate-pending.

## The drive and the exchange

Zero fix rounds -- first gate with none. The gate carried one
product-purpose exchange, answered from corpus + schema/module
ground truth reads (not memory):

- What files go here / is it a catch-all? YES by design: the
  custody surface over three sources -- firm uploads (evidence,
  civil docs, correspondence), client uploads (arrive via intake
  document requests), produced artifacts (filled form packages,
  signed e-sign copies, notes exports). Corpus:
  files-and-documents.module-exists (fx-0193/0195/0196).
- Do uploads here feed the data model? NO -- the flow runs the
  other way: facts (intake) -> smart forms -> produced PDFs land
  in Files. Nothing in the frozen core reads a PDF and writes
  facts (module list is ground truth; no extraction machinery
  exists). Docketwise itself has PDF-to-data (docketwise-iq AI
  data capture: passport/green card/EAD/I-94, OCR, mandatory
  Review & Edit modal; fx-0204/0261/0264) but it runs through a
  Smart Forms document request, NOT their Files tab -- their
  Files area is storage-only, same as ours. The IQ module has
  zero footprint in the ratified 111-entry casework spine (grep
  of casework/: no reference), so extraction is not owed by any
  current contract; if ever wanted it is a NEW child, attaching
  at the intake document-request flow with review-and-approve
  into facts, never a silent parse.

Disclosures presented with the gate message, accepted with the
verdict ("as is"):

- contact-page Files card (disclose-and-extend; the rail pins
  matter only)
- Preview/Print offered for the core's preview types only (pdf,
  png, jpeg, txt, csv -- other types download-only, no control
  that would error)
- upload from the Files tab lands on the file's custody page;
  upload from a matter/client page returns there

## Mechanical floor at verdict time (full step table -- METHOD
rule s3)

Rail sha 81168b79 x2 (verify/report_sha.py):

    PASS    setup + login
    PASS    empty states designed (fresh db)   [/files landed]
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
    PASS    notes: PDF export
    PASS    files: upload + custody
    PASS    files: matter section + index filters
    PASS    files: rename/preview/print/bulk
    PENDING files: e-sign prepare + request    [P4b]
    PENDING files: e-sign signer + custody     [P4b]
    PENDING search: chrome bar everywhere      [P5]
    PENDING search: coverage + grouped results [P5]
    PENDING search: recents                    [P5]
    PENDING settings: users admin              [P6]
    PENDING settings: permissions groups       [P6]
    PENDING settings: trash + restore          [P6]
    PENDING settings: notifications + firm     [P6]
    PENDING settings: machinery homes          [P6]
    PASS float-sweep
    PASS iso-stray-sweep (65 tab pages)
    steps: 20 pass, 11 pending, 0 fail
    verdict: ON TRACK (pending screens)

Every P1-P4a step PASS except derived-kinds ([Q1] by design);
all 11 pendings name later stages/phases. The empty-state sweep
step went green this stage (/files was its last hold-out).

Standing suites at verdict time, quoted: "ui-walk: 13 pass, 0
pending, 0 fail; sweeps pass; verdict GREEN" / "spine: 107
green, 0 red, 0 pending; checks pass" / "billing: 25 green, 0
red, 0 pending, 0 parked; checks pass; verdict: GREEN" /
"fiduciary: 9 pass, 0 red, 0 stub; verdict: GREEN".

Verify-the-verifier this stage: the rail was refined BEFORE the
build from frozen-core reads -- one structurally unpassable
assert killed (outbox scrape for an absolute URL the core never
writes; the core mails the RELATIVE /esign/<token>), two vacuous
asserts pinned (page-wide "firm"; bulk-zip PK magic that passed
any zip -- the RED drive proved the refined entries assert
catches what the old one missed). Three RED drives, one per
new-green step: truncated sha -> FAIL; matter filter no-op ->
FAIL; single-entry zip -> FAIL. Each reverted, green after.

## Ruling queue disposition

[Q1]-[Q11] + [Q13] CARRY FORWARD to the P4b gate. No new [Q]
opened at this gate; the ingestion question was answered closed
from ground truth (not owed; new-child-if-ever-wanted).

Parked (unchanged): note attachments; single-note PDF; month-cell
overflow; matter/client in month cell; interleaved timeline;
calendar sync; role enforcement.
