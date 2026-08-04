# atlas

## Purpose

Program root for the competing immigration practice-management effort.
This is the workshop's first PROGRAM: not a project with one goal, but a
container for goal-method child projects that share one mission --
recreate the verifiable surface of Docketwise-class immigration PM
software, spec-first. Each child carries its own goal/plan/state/worklog
contract; this root holds only what is true across all of them.

Doubles as a goal-method stress test at program scale (recursive
decomposition, oracle construction as a project, amendment under drift).
Method observations belong in child worklogs with a `METHOD:` prefix.

## Program rulings (closed 2026-07-31 -- do not re-propose)

- Target is Docketwise, not Clio: immigration-specific, tractable
  surface, spikes stay relevant.
- Sourcing is PUBLIC SURFACE ONLY: marketing site, help center, YouTube
  demos/webinars, release notes, third-party reviews. No trial account,
  no authenticated access. Gaps only the live product could resolve are
  flagged SOURCE-GAP in the corpus, never guessed. A trial-account pass
  would be a separate, deliberate, supervised decision made later with
  the SOURCE-GAP inventory in hand.
- Corpus granularity is FEATURE LEVEL with opportunistic detail capture:
  take behavior-level precision when a public source offers it cheaply,
  never hunt for it.
- Parent goal.md is DEFERRED: the program root carries no goal contract
  until child 1's retro shows what a program-level artifact would owe
  us. Contract weight lives in the children.
- Build-children roster is an OUTPUT of the spec corpus, not an input:
  do not scaffold build projects before the corpus defines the modules.

## Children

| Child           | Status                    | Contract                    |
| --------------- | ------------------------- | --------------------------- |
| docketwise-spec | COMPLETE 2026-08-01       | docketwise-spec/goal.md     |
| casework        | COMPLETE 2026-08-01       | casework/goal.md (ratified) |
| casework-ui     | ON HOLD 2026-08-03 at the | casework-ui/goal.md         |
|                 | P4 cold-run recruiting    | (ratified 2026-08-01;       |
|                 | gate; pre-verdict         | contract intact)            |
| casework-billing| COMPLETE 2026-08-03 --    | casework-billing/goal.md    |
|                 | all verifiers green,      | (ratified 2026-08-03);      |
|                 | result.md on disk         | result.md is the authority  |
| billing-ui      | ACTIVE -- gates 1-3       | billing-ui/goal.md          |
|                 | closed 2026-08-04; P4     | (ratified 2026-08-04)       |
|                 | walk day remains          |                             |

## Spikes

`spikes/` is the archived pre-program exploration (2026-07-23/24 era):
G-28 field mapping, PDF fill, package generation, workflow/diff engines,
a working server + SQLite db (legal_crm.db). Archived, not dead --
these are candidate assets for future BUILD children, not part of any
current contract. Do not run, extend, or refactor them from a spec
session. Delete = archive applies: nothing in spikes/ is destroyed.

## Rules for agents

- A session works in ONE child. Do not modify a sibling child or the
  program root's rulings from inside a child session.
  AMENDMENT (program ruling 2026-08-03): casework-billing extends the
  casework core IN PLACE. A casework-billing session may write
  casework/app, schema and seed generators, and add new tests, with
  hard limits: existing spine tests are immutable from that child,
  casework/goal.md is never edited, and the 111-entry spine suite
  must stay green at its phase gates. The invoicing strategic flag
  (deferred 2026-08-01) is hereby deliberately revisited; live
  contract: casework-billing/goal.md once ratified.
  AMENDMENT (program ruling 2026-08-03, ratified by James): billing-ui
  extends the casework-ui surface IN PLACE. A billing-ui session may
  write casework-ui/app_ui and add new walk/verifier coverage, with
  hard limits: run_ui_walk.py must stay green at billing-ui's phase
  gates; casework-ui/goal.md is never edited and its cold-run oracle,
  hold status, and ratified protocol are untouched -- a billing screen
  that would require changing an existing casework-ui screen or its
  walk steps is a gate decision, not a code change; casework/ stays
  frozen for this child (billing logic already lives in casework/app;
  billing-ui owns rendering only, no business logic). Its oracle is a
  James-driven demo walk, NOT a cold run. Live contract:
  billing-ui/goal.md once ratified.
  AMENDMENT (program ruling 2026-08-04, ratified by James): the F7
  reconciliation gaps (billing-ui worklog s2, findings 1+2:
  corrections desync bank truth from books; batch matching is 1:1
  only) are authorized as a cross-project fix from billing-ui
  sessions, scope-limited to correction/external-event semantics in
  casework/app (ledger.py, billing.py) and the statement/recon
  model in casework-billing/verify (bank_statement.py,
  reconcile.py, fiduciary F7 scenarios). Hard limits: spine tests
  immutable; fiduciary checks may STRENGTHEN, never weaken; after
  the fix all four standing suites rerun green and new x2 shas
  supersede casework-billing's sealed shas -- supersession recorded
  in casework-billing/state.md and billing-ui's worklog, result.md
  histories unedited.
- Each child's own CLAUDE.md + state.md is the authority on its state;
  this file's roster is a signpost, not a second snapshot.
- The spec corpus records facts about Docketwise with citations -- it is
  a spec, not a brainstorm. Design ideas for our own product go to a
  child's log-don't-build machinery, not into corpus entries.
