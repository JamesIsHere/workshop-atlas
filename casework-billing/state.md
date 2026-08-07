# state.md -- casework-billing (session cache, overwritten each wind-down)

## Status

COMPLETE 2026-08-03. All three verifiers green: parity 25/25 (GREEN
exit 0 x2 byte-identical), fiduciary F1-F8 all live (GREEN exit 0 x2
byte-identical, F7 with real reconciling items), anchor billing walk
PASS at 1.336s of 900s. Spine regression identical to the
pre-billing baseline. result.md written; the goal.md contract is
satisfied. Reciprocal guard delivered into casework/CLAUDE.md.

## Next actions

None owed. Successor decisions are new conversations, not queued
work -- candidates on record: firm demo emphasis (see firm-meeting
queue below), real fee-split processor integration
(Approval-required), casework-ui resumption over the extended core.
result.md is the authority.

## Watch items and caveats

- FIRM-MEETING QUEUE (r6): ANSWERED 2026-08-03 (root-level session).
  The firm runs billing/trust INSIDE Docketwise; the AffiniPay/8am
  take is "A" problem alongside training/usability cost -- rake is a
  wedge, training cost remains the core thesis. Demo emphasis
  validated toward billing/trust; drove the billing-ui child
  (program ruling 2026-08-03, see ../CLAUDE.md). Flat-fee vs hourly
  mix still unasked -- carry to future firm conversations.
- Any future session touching casework/app must run BOTH suites
  (reciprocal guard, casework/CLAUDE.md How to run).
- posted_at = business date design note (worklog P1); revisit only
  if it ever costs something.
- Final shas: billing acba95b1 x2, fiduciary af2e242f x2, spine ==
  baseline, seed 539be0f9.
- SUPERSESSION LANDED 2026-08-04 (program ruling 2026-08-04,
  recorded from a billing-ui session as the ruling authorizes):
  billing-ui's P0 oracle found two F7 gaps (corrections desynced
  bank truth; batch matching was 1:1 only -- billing-ui/worklog.md
  s2). Fix delivered same day: corrections append mirror bank
  events (both ledgers stay append-only), refunds compensate, the
  recon matcher aggregates n:1 batches, and run_fiduciary --seeded
  now carries an F7-lock overlay (edit + refund + multi-payment
  batch). Resealed x2 byte-identical: billing acba95b1 (UNCHANGED
  -- report content identical), fiduciary fb5bccda (supersedes
  af2e242f). Anchor billing re-run PASS 1.284s; spine 107 == green;
  selftest calibration all behaved. result.md stays as history.
- SUPERSESSION LANDED 2026-08-07 (James's real-bank ruling, s8 close
  of billing-ui; recorded from a billing-ui session as the F7
  amendment authorizes): the mirror-event correction model is DEAD.
  Corrections/refunds now touch books only (_append_mirror_events
  deleted; correction reposts post with witness_bank=False); the
  recon engine (bank_statement.py + reconcile.py) matches statement
  lines to book entries and explains differences as caused
  reconciling items (timing + correction/refund awaiting bank);
  check_f7 STRENGTHENED: bank-record purity (per-payment event
  birth-shape), timing items must resolve at the all-cleared
  period, closed cause vocabulary. Resealed x2 byte-identical:
  fiduciary e6c64593 (supersedes fb5bccda; the F7 line is the only
  change), billing c53f262b (supersedes acba95b1; drift is the s8
  display_code CSV column only -- today's engine work left parity
  output untouched). Anchor billing re-run PASS 1.250s; spine 107
  green; selftest calibration all behaved. result.md stays as
  history.

## Open decisions

None.
