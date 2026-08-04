# result.md -- docketwise-spec

Written 2026-08-01, after both goal.md verifiers passed. This file
exists only because the completion proof is on disk.

## Outcome delivered

A feature-level specification corpus of Docketwise's publicly
attested product surface, mechanically verifiable, with the proof
machinery to answer "complete relative to the enumerated public
surface, and every claim attested?" with exit 0.

| Measure            | Value                                        |
| ------------------ | -------------------------------------------- |
| Corpus             | 242 entries (239 live) across 20 modules     |
| Tiers              | confirmed 123 / provisional 116 (live)       |
| Fixtures           | 281 captured, sha256-manifested, immutable   |
| Inventories        | 5 source families, 167 items, 0 unmapped     |
| SOURCE-GAP         | 1 (trust-request payment methods)            |
| Rejection log      | populated per module (churn kept visible)    |
| Exclusion log      | all out-of-scope inventory rulings           |

## Verifier evidence

VERIFIER 1 (oracle.py, 7 mechanical checks): FULL-mode GREEN exit
0, run twice, byte-identical reports -- audit/run5.txt = run6.txt
(post-[G2]-edit state; earlier green pairs run1/run2 at Phase 4
close, run3/run4 after the supersede). Quoted in the worklog.

VERIFIER 2 (reproduction audit): fresh Sonnet agent (non-Fable per
[G1] ruling 8), 15 random live entries (seed 20260801), re-derived
descriptions from cited fixtures alone in an isolated package.
Diffs: MATCH 12 / VARIANCE 3 / DIVERGENCE 0. James's ruling
(2026-08-01): transcription noise, not extraction error -- PASSED.
Report: audit/reproduction-audit.md. Criterion semantics
spot-check (fresh random 10, seed 20260802): PASSED same date.

[G2] interpretive rulings 1-19 recorded in the worklog (diff
ruling, two micro-fixes applied with oracle re-green, and
ratification of every queued Phase 3/4 interpretive call).

## Completion proof paths

- corpus/ -- one file per module, entries in schema
- fixtures/ + fixtures/manifest.json -- every cited capture
- inventories/ -- all five source-family inventories
- oracle.py + exit-0 reports (audit/run1..run6.txt)
- audit/reproduction-audit.md -- diff report + James's ruling
- result.md -- this file

## Known limits (by design, not defects)

- Public surface only: 1 SOURCE-GAP is the entire trial-account
  decision inventory; nothing behind a login was guessed.
- YouTube back-catalog: the oldest ~85 of a stated 185 uploads are
  unreachable by ordinary fetch (documented cap; webinar playlist
  ids recorded in inventories/youtube.md for future routes).
- G2/Capterra/TrustRadius bot-walled; the reviews family lives
  through old.reddit static HTML (8 threads, all ruled).
- integrations.everify is permanently provisional absent a new
  public source (scoped external check exhausted at [G2]).
- Provisional tier (116 entries) is the marketing-overclaim
  skepticism carrier, not an error bucket.

## Downstream use

The corpus is the acceptance-criteria oracle for future atlas
build children: every live entry carries a testable criterion; the
module roster is the candidate build-children roster (program
ruling: roster is an OUTPUT of this corpus). The SOURCE-GAP
inventory is the input to any future supervised trial-account
decision.
