# state.md -- billing-ui (session cache, overwritten each wind-down)

## Status

P3 BUILT, 2026-08-04; ALL THREE GATES CLOSED same day, zero
kills across three decks (gate 2 on the deck alone -- rehearsal
waived; hands-on lands at the P4 walk-day oracle). The walk
verifier is FULLY GREEN for the first time: 17/17 x2, exit 0,
timing-stripped sha a506f085 identical both runs. All four
standing suites green after the last code edit. Corrections
family live: payment detail with journal trail + bank record,
edit-as-reversal+repost, refund, charge re-association, email
share. Receipts + 3-frame deck in gate-receipts/gate-3-deck/.
Four P0 drafting errors in the walk verifier corrected across
the session, each with rationale in the worklog (share-token
format, audit table names x2, correction model).

## Interface ruling (2026-08-04, from James's "I'm losing track")

James's surface is the PRODUCT plus ONE plain-language question
per touchpoint. No child names, phase numbers, or suite tallies
in a gate ask without inline translation. Re-issue the
plain-terms program map at every gate and on demand. Rationale
and METHOD finding in worklog s3.

ONE-ADDRESS RULE (added same day after a dead 8502 link): James
gets exactly one URL, ever -- http://127.0.0.1:8500. Different
dbs swap BEHIND that port (stop one server, start the next on
8500); never hand him a new port number. Temporary servers on
other ports are agent-internal only.

## Next actions

1. P4 walk day -- the ONLY remaining contract item. First ask
   next session (plain terms): "when do you want to do the final
   run-through?" Agent starts fresh dated db server ON 8500 + quotes the
   walk verifier green FIRST (ordering rule), James drives the
   12-step protocol sheet unassisted, fiduciary suite runs on the
   walked db, PDF/ledger/recon eyeballed, three-part verdict
   (fiduciary story lands / nothing embarrassing / bookable).
   PASS -> completion proof, result.md, roster flip.

## Watch items and caveats

- x2 byte-identical (goal.md completion table): report carries
  run-timestamp + timings, so the seal is on timing-stripped
  content (sha a506f085) -- disclose in result.md.
- Recon screen imports the F7 engine from casework-billing/verify
  (deliberate, unchanged).
- Standing gates at every phase close: ui-walk 13, spine 107,
  billing 25, fiduciary 8. All green this session post-edit.
- Anti-stall ledgers: P2 spent 1/2, P3 spent 0/2.
- Launcher: atlas-ui / atlas-ui --seeded. Seeded server left
  RUNNING on 8500 with P3 code (login demo.reviewer@synthetic.test
  / demo-seed-pass; MFA code shown on screen). Rehearsal servers
  stopped; data/rehearsal-g2-2026-08-04.db retained.
- Firm question still unasked: flat-fee vs hourly mix.
- PARKED PROGRAM-LEVEL FINDING (rehearsal, 2026-08-04): client
  intake questionnaire loses unsaved fields on per-field Save,
  never re-renders saved answers, submit verifies nothing
  (worklog s3, rehearsal finding 1). NOT this child's scope --
  carry in every wind-down until routed to the contract that
  next owns the client surface.

## Open decisions

- Walk-day scheduling (James). Gate 3 closed 2026-08-04 (pass,
  zero kills; protocol stands as ratified). P4 is the whole
  remainder.
