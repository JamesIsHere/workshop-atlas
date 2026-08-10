# state.md -- casework-tabs (session cache, overwritten each wind-down)

## Status

P4a FILES MECHANICS PASSED 2026-08-10 (s6, "yes pass", zero fix
rounds -- receipt verify/gate-receipts/p4a-files.md). Rail was
refined four->five files steps (e-sign split prepare/sign; one
structurally unpassable assert and two vacuous ones fixed from
ground-truth reads of the frozen core), then the mechanics built:
upload + custody, matter/contact files sections, firm index with
filters, rename/preview/print/bulk zip. 3 RED drives all caught.
Rail 20 pass / 11 pending / 0 fail, sha 81168b79 x2 (supersedes
d2c65ac8); all four standing suites green, quoted in worklog s6.
Demo reseeded (5 files incl a produced one), server UP on 8500.

## Next actions

1. P4a GATE: James hands-on drives the files mechanics on 8500.
   Disclosures queued for the verdict: contact-page files card
   (disclose-and-extend; the rail pins matter only); Preview/
   Print offered for the core's preview types only (pdf, png,
   jpeg, txt, csv -- others download-only); upload lands on the
   file's custody page unless launched from a matter/client page
   (then it returns there).
2. After the P4a verdict: P4b E-SIGN build to the two refined
   rail steps -- prep editor entered by POST from the PDF detail
   (txt must not offer it), signers/fields/request, staff page
   renders the LIVE absolute signer link via client_base (intake
   precedent), sign-through on the frozen client surface, then
   completed status + produced custody + source-filter narrowing.
   2 RED drives owed.
3. [Q1]-[Q11] + [Q13] carry to the P4 gates.

## Watch items and caveats

- Demo server UP on 8500 over data/demo-tabs.db (background task
  bus99mdap this session). NOTE: s5's server survived its session
  and held the db lock (PID 36600, killed this session) -- check
  the port before reseeding.
- E-sign ground truth (discovered s6, do not re-derive): the
  frozen core mails the RELATIVE /esign/<token>; the absolute
  live link is the staff page's job (client_base, the intake
  precedent). Client sign form inputs are field_<id>; signature
  values are JSON, typed mode {"mode":"type","text":...}.
- Typography (0.85rem td, firm-blue links) + tab-detail kv +
  matter-first rulings now cover calendar, tasks, notes AND files
  surfaces; search/settings adopt at P5/P6; billing-ui's signed
  tables stay untouched.
- Complete is check-then-Done everywhere; Reopen is deliberately
  one-click.
- Gate receipts quote the FULL step table (METHOD s3): marker
  regressions demote to PENDING, so the verdict line alone can
  hide a regressed screen.
- Sabotages via Edit-with-known-content ONLY (METHOD s4).
- Typed deferral owed: final-walk TIME BUDGET at P7 walk-sheet
  ratification.
- casework-ui remains ON HOLD (cold runner); its data/ carries
  real-ish PII -- never seed or demo from it.
- Owed per phase: deliberate RED per new step. Empty-state FAIL
  arm owed only for a NEW designed-empty pattern (/files was the
  P2-proven pattern; not re-owed).
- Parked with triggers (unchanged): note attachments; single-note
  PDF (core-amendment family); "+N more" month-cell overflow;
  matter/client in month cell or hover; interleaved notes
  timeline (rendered-artifact gate); calendar sync; role
  ENFORCEMENT.

## Open decisions

- [Q1]-[Q11] + [Q13] queued for the P4 gates. None block the P4b
  build.
