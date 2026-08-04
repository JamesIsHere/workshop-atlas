# state.md -- casework-ui

Overwritten each wind-down. Cache over the worklog.

## Status

ON HOLD, 2026-08-03, at the P4/U4.1 recruiting gate -- James's
ruling: no cold runner available; keep the portfolio moving.
Hold is PRE-VERDICT: goal.md's oracle (cold user, unassisted,
inside budget) is unmet and unchanged; James's own testing
satisfies his standards but does not close the contract. P3
COMPLETE (clock gauntlet 19/19; cold-run protocol RATIFIED).
Late-P3 additions banked before the hold: rehearsal 2 (r5,
James solo) check_cold_run.py EXIT 0 9/9 -- first clean run
ever (db data/cold-run-2026-08-03-r5.db; timing void as proof,
clean-leg times meaningful; finding 8 was the dominant cost);
finding 8 FIXED (New deadline form: visible Matter dropdown,
"-- no matter --" last and never default, contact derived from
matter's primary contact); Clients display rename
(presentation-layer only, routes/columns/casework unchanged).
Parking receipt this session: run_ui_walk.py GREEN (13 pass, 0
pending, 0 fail; sweeps pass; exit 0).

## Next actions

1. RESUME CONDITION (James, whenever): a qualified cold runner
   exists -- never operated ANY build of this system; one run
   per person, nobody is cold twice. Agent never recruits.
2. On resume -> U4.1 run day per the RATIFIED protocol
   (verify/cold-run-protocol.md): agent preps setup section
   (fresh dated db, two windows, sheet + cards printed); James
   proctors (stopwatch, M0-M5 marks, friction log); after
   "done": `python verify/check_cold_run.py
   data/cold-run-<date>.db` must exit 0, plus PDF + calendar
   eyeball. Budget 15:00, M1->M5, ceremony outside.
3. PASS -> U4.2 completion proof (fresh walk x2, gauntlet,
   spine + anchor, cold-run-report.md) -> U4.3 result.md +
   self-audit + roster flip. FAIL -> findings logged, fixes
   ruled at a mini-gate, re-recruit.

## Watch items and caveats

- GATE FORMAT (standing): one decision per turn; question LAST.
- Protocol RATIFIED -- verify/cold-run-protocol.md binds; edits
  require a gate. Task sheet verbatim; proctor speech rules
  apply to the agent too during runs.
- ../casework/ FROZEN. 2026-08-03 authorized exception (logged
  both worklogs): esign spine test date literal -> derives from
  signed_at; app code untouched; spine 107 green.
- no-logic lint: SQL only in reads.py (SELECT-only readers);
  1 named ALLOWLIST exemption unchanged.
- MFA = email method, static per-login code; TOTP KILLED.
- Contact CREATE form person-only (ruling); companies browse-
  grade. Preparer/firm WRITE screens out of v1. Display layer
  says "Clients"; seeded browse data may list non-client
  contacts under that label -- acceptable v1, revisit if mixed
  kinds ever reach browse-grade surfaces (worklog 08-03).
- Clock discipline: gauntlet is the standing guard (U4.2 reruns
  it); verifier expectations derive from app-written stamps,
  never wall-clock literals.
- data/demo-p0.db and cold-run/rehearsal dbs (incl. r5) carry
  real-ish PII (James's email/phone; priya@gmail.com): local
  only, wipe before anything travels. Cold runs always use a
  FRESH dated db.
- Rehearsal dbs retained, never deleted (delete = archive).

## Open decisions

- None. Project is parked; next act is James's (recruit), on
  his timeline. Atlas root roster row not updated from this
  child session (one-child rule) -- flag on resume or next
  root-level session.
