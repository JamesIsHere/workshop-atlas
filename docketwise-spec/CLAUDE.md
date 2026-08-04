# docketwise-spec

## Purpose

Child 1 of the atlas program: extract a feature-level, mechanically
verified specification corpus of Docketwise's public product surface,
to serve as the acceptance-criteria oracle for future atlas build
children. goal.md is the contract; this file is a signpost.

## State

| Field        | Value                                              |
| ------------ | -------------------------------------------------- |
| Status       | COMPLETE 2026-08-01 -- both verifiers passed,      |
|              | [G2] ruled (1-19), result.md on disk               |
| Last session | 2026-08-01 -- Phase 5 audit passed; [G2] cleared   |
|              | one-question-per-turn; project closed              |
| Next action  | none -- resumption = new scope decision            |

Fine-grained authority: state.md. This table is never a second
snapshot.

## How to run

Nothing runs yet. After Phase 0: `python oracle.py` from this folder
validates the corpus (exit 0 = green).

## Gotchas

- Program rulings (public-only sourcing, feature granularity) live in
  ../CLAUDE.md and are closed -- do not re-litigate here.
- fixtures/ is immutable once captured; changed pages get NEW fixture
  ids. Never hand-edit a capture.
- The corpus is append-and-supersede; deleting entries is forbidden
  by goal.md.

## Rules for agents

- goal.md is ratified by James only; agent edits to it are scope
  changes and need approval.
- Verify claims with the oracle before reporting them; quote its
  output.
- Method observations get a METHOD: prefix in worklog.md.
