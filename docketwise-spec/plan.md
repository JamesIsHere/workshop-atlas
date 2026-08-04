# plan.md -- docketwise-spec

EXECUTED IN FULL -- project COMPLETE 2026-08-01 (all phases done,
both verifiers passed, result.md on disk). Kept as the record of the
strategy that ran.

Agent-owned strategy. Rewritten freely; judged by results. Phases gate
on the oracle, not on feelings.

MODE: PHASE-GATED HYBRID (ruled 2026-07-31, red-pen round 7).
Phases 0-2 run unattended to [G1]; Phases 3-4 run unattended to [G2];
the gates are human checkpoints ratified in goal.md as contract.
Mid-phase, Decision defaults and the Blocker rule govern as in
unattended mode.

MODEL ASSIGNMENTS (ruled 2026-07-31, red-pen round 2; [G1] ruling 8
same date): Phases 0-2 ran on Fable. Phase 3 fan-out RULED AT [G1]:
FABLE STAYS -- the error-propagation rationale applies undiminished
to fan-out, and criterion drafting remains the highest-consequence
judgment. Verifier-2 clarification ratified with the ruling: Fable
is the sole extractor across phases 0-3, so the reproduction-audit
agent is any single NON-FABLE model for the whole 15-entry sample
(no per-entry verifier assignment). See goal.md verifier 2.

## Phase 0 -- harness

Folder skeleton (corpus/ fixtures/ inventories/ audit/), entry schema
frozen from goal.md, oracle.py written and exit-0 GREEN on a seed
micro-corpus: 3-5 hand-made entries with real captured fixtures.
Oracle-first: no mass extraction until the checker is green.

## Phase 1 -- inventories

Mine the five source families into inventory artifacts BEFORE
extracting features: marketing nav/feature tree, help-center category
tree, YouTube video list, release-notes index, review-site checklists.
These define the coverage-closure target. Any dead family goes to the
exclusion log with evidence (three minable families minimum or blocker
rule fires).

## Phase 2 -- pilot module

Full extraction of ONE module end-to-end: candidate = Smart Forms
(richest public documentation; overlaps the spikes' domain knowledge).
Oracle green on the pilot corpus. This phase hardens the extraction
protocol, the schema under real data, and per-module oracle behavior.

[G1] Pilot red-pen: James reviews the pilot module's corpus before the
protocol freezes and fan-out replicates it. Cheap to change until
here; expensive after. Standing [G1] questions (ruled at red-pen round
3): (a) would this protocol survive a SPARSE module? -- Smart Forms is
the marquee module and over-documented relative to fan-out targets;
check the protocol against the thinnest module the inventories show.
(b) fan-out model ruling (see MODEL ASSIGNMENTS).

## Phase 3 -- fan-out

Remaining modules by the pilot protocol. Per-module close = oracle
green + module evidence written to disk (compaction-readiness).
Rejection reasons counted per module.

## Phase 4 -- closure

Coverage reconciliation across all inventories; SOURCE-GAP inventory
compiled as the future trial-account decision list; attestation-tier
report; full-corpus oracle exit 0, twice, byte-identical.

## Phase 5 -- reproduction audit

Verifier 2: fresh agent re-derives 15 random entries from fixtures
alone; diff report to audit/.

[G2] James rules on the diff report and spot-checks criterion
semantics. result.md only after his ruling.
