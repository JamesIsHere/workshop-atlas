# state.md -- casework-tabs (session cache, overwritten each wind-down)

## Status

P2 TASKS BUILT 2026-08-10 (s4), GATE PENDING -- James has not
driven it yet. All four tasks rail steps green + driven RED (a
fifth RED proved the empty-state FAIL arm); rail 11 pass / 19
pending / 0 fail, sha eb4fc42e x2 (supersedes d1a45962); all four
standing suites green and quoted in worklog s4. Demo server UP on
port 8500 over regenerated data/demo-tabs.db (login
demo.tabs@synthetic.test / demo-tabs-pass).

## Next actions

1. P2 GATE: James drives /tasks, /settings/task-lists, and a
   matter page's Tasks card on 8500. Ruling queue serialized one
   per turn: [Q9] due-date-at-creation-only (core has no setter),
   [Q10] automation linkage builder-side only, [Q11] matter-page
   date format extension, then carried [Q1]-[Q8] (worklog s3).
2. After the verdict: receipt with the FULL step table in
   verify/gate-receipts/p2-tasks.md, then P3 NOTES per plan.md.

## Watch items and caveats

- Rail refinements this session (worklog s4): /tasks/<id>/due
  dropped (no core setter -- due rides quick-add), lists step
  asserts tightened after a vacuous-assert catch (sabotage 4 NOT
  caught first run; rail now pins "due 30 days before EAD
  expiry").
- Matter detail dates went MM/DD/YYYY (existing screen, sibling-
  defect extension, [Q11]) -- revert is one edit if the gate says
  no.
- Gate receipts quote the FULL step table (METHOD s3): marker
  regressions demote to PENDING, so the verdict line alone can
  hide a regressed screen.
- Calendar typography rulings (0.85rem tables, links always blue)
  stay SCOPED to calendar surfaces; app-wide needs a ruling.
- Typed deferral owed: final-walk TIME BUDGET at P7 walk-sheet
  ratification.
- casework-ui remains ON HOLD (cold runner); its data/ carries
  real-ish PII -- never seed or demo from it.
- Owed per phase: deliberate RED per new step + the empty-state
  FAIL arm (P2 arm PROVEN this session; owed again only if a
  later phase adds a new designed-empty surface).
- Parked with triggers (unchanged from s3): "+N more" month-cell
  overflow; matter/client in month cell or hover; interleaved
  notes timeline; calendar sync; role ENFORCEMENT.

## Open decisions

- [Q1]-[Q11] queued for the P2 gate. None block P3 if James
  wants to defer them again, but [Q9] and [Q11] shape screens
  James will keep touching -- push for rulings at this gate.
