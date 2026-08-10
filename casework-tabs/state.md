# state.md -- casework-tabs (session cache, overwritten each wind-down)

## Status

P4b GATE IN PROGRESS, PAUSED 2026-08-10 (s6) -- James's energy
spent mid-drive; verdict NOT signed. P4a PASSED earlier the same
session (receipt verify/gate-receipts/p4a-files.md). Eight P4b
fix rounds landed live, all rail-proven: r1 preview/print
collapsed to one control; r2 field Remove + coordinate hint; r3
RATIFIED core amendment (client sign surface accepts a plain
typed name; prompts appended to spine-pinned labels -- first
attempt broke spine 106/1, reciprocal guard caught it); r4
void/redo with dead links; r5 empty-send guard; r6 field-less
guard (his drive produced a VACUOUS completed signature --
demo-only, dies at reseed); r7 link orientation; r8 the
STOP-PATCHING round: ONE-CLICK Request signature (prepare +
signer + default field + send, link on landing), duplicate-
signer no-op, editor demoted to manual path. Rail 22 pass / 9
pending / 0 fail, sha 698eca26 x2; 12 RED drives this session,
all caught; all four standing suites green (worklog quotes).
Server UP on 8500.

## Next actions

1. RESUME = James's 3-click drive on http://127.0.0.1:8500:
   (a) /files/5 (SYNTH-g28-anya-filled.pdf): tick Void -> Void
   (clears his 3x-Anya pileup); (b) same page: "Request a
   signature from" (Anya preselected) -> Request signature ->
   live link appears on that page; (c) open link incognito,
   type a name, Sign; refresh -> completed + Signed copy.
   Optional cleanup: /files/6 carries a stray draft (voidable).
2. P4b verdict -> receipt (r1-r8 table + the s6 METHOD retro)
   closes P4. Then P5 SEARCH (rhythm now includes the MISUSE
   PASS before the gate -- new step 4 in plan.md).
3. [Q1]-[Q11] + [Q13] carry to the P4b verdict.

## Watch items and caveats

- HIS FEEDBACK, accepted and institutionalized: 4 of 8 fix
  rounds were machine-findable (empty send, field-less vacuous
  sign, dup signers, box-less page). MISUSE PASS is now rhythm
  step 4: drive wrong-order/double-submit/empty-submit/skip
  per new flow + write the naive walkthrough BEFORE any hands-on
  gate. Machine-findable holes never reach James again.
- Demo server UP on 8500 (this session); servers SURVIVE
  sessions and hold the db lock -- check port, kill before
  reseed. Demo db carries his gate artifacts (3-Anya void
  target on file 5, stray draft on file 6, vacuous completed
  retainer) -- KEEP mid-gate; fresh reseed only at gate close.
- E-sign ground truth: core mails RELATIVE /esign/<token>;
  absolute link = staff page's job (client_base). Client sign
  inputs field_<id>; plain typed name wrapped server-side into
  typed-mode JSON (r3 amendment). Completion auto-files
  <stem>-signed.pdf as produced.
- Program ruling 2026-08-10 (r3, in atlas/CLAUDE.md): client
  e-sign surface amendment -- _esign_page/_esign_sign only;
  spine label "signature (page 1)" is PINNED (append, never
  replace).
- Typography + tab-detail + matter-first rulings cover calendar,
  tasks, notes, files; search/settings adopt at P5/P6.
- Gate receipts quote the FULL step table (METHOD s3).
- Sabotages via Edit-with-known-content ONLY (METHOD s4).
- Typed deferral owed: final-walk TIME BUDGET at P7.
- casework-ui remains ON HOLD; its data/ has real-ish PII --
  never seed or demo from it.
- Parked with triggers (unchanged): note attachments;
  single-note PDF; month-cell overflow; matter/client in month
  cell; interleaved timeline; calendar sync; role ENFORCEMENT.

## Open decisions

- P4b verdict (the resume point). [Q1]-[Q11] + [Q13] queued
  behind it.
