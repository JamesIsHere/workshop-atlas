# state.md -- casework-tabs (session cache, overwritten each wind-down)

## Status

P3 NOTES BUILT 2026-08-10 (s5), GATE PENDING -- James has not
driven it yet. All five notes rail steps green + driven RED
(timeline-pin step refined pre-build so ordering is observable);
rail 16 pass / 14 pending / 0 fail, sha 157f5ac1 x2; all four
standing suites green, quoted in worklog s5. Demo server UP on
port 8500 over fresh data/demo-tabs.db. P2 receipt:
verify/gate-receipts/p2-tasks.md.

## Next actions

1. P3 GATE: James drives /notes, a matter page's Notes timeline
   (capture, pin, export), and /settings/note-categories on 8500.
   New [Q13]: the core's notes PDF prints raw ISO timestamps
   inside the document. Carried: [Q1]-[Q11].
2. After the verdict: receipt in verify/gate-receipts/p3-notes.md,
   then P4 FILES per plan.md (staged P4a mechanics / P4b e-sign).

## Watch items and caveats

- Demo server UP on port 8500 over data/demo-tabs.db (background
  task b8wv88mv3 this session). Fresh regen + restart at the P3
  gate; same port always.
- Typography (0.85rem td, links firm blue) + matter-first
  single-link rulings now cover calendar AND tasks surfaces;
  notes/files tables ADOPT THEM when P3/P4 rebuild those screens;
  billing-ui's signed tables stay untouched.
- Complete is check-then-Done everywhere (native required
  checkbox, zero JS); Reopen is deliberately one-click. Rail pins
  both; the direct-POST path bypasses client validation by
  nature, so the guard is pinned as markup.
- Gate receipts quote the FULL step table (METHOD s3): marker
  regressions demote to PENDING, so the verdict line alone can
  hide a regressed screen.
- Sabotages via Edit-with-known-content ONLY (METHOD s4: a blind
  str.replace sabotage was a silent no-op and nearly passed as a
  verified RED).
- Typed deferral owed: final-walk TIME BUDGET at P7 walk-sheet
  ratification.
- casework-ui remains ON HOLD (cold runner); its data/ carries
  real-ish PII -- never seed or demo from it.
- Owed per phase: deliberate RED per new step. The empty-state
  FAIL arm was PROVEN at P2; owed again only if a later phase
  adds a new designed-empty surface pattern.
- Parked with triggers (unchanged): "+N more" month-cell
  overflow; matter/client in month cell or hover; interleaved
  notes timeline (rendered-artifact gate); calendar sync; role
  ENFORCEMENT.

## Open decisions

- [Q1]-[Q11] queued for the P3 gate. None block the P3 build.
