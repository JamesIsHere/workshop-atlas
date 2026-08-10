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
| billing-ui      | COMPLETE 2026-08-10 --    | billing-ui/goal.md          |
|                 | verdict PASS/PASS/PASS,   | (ratified 2026-08-04);      |
|                 | all suites green,         | result.md is the authority  |
|                 | result.md on disk         |                             |
| casework-tabs   | IN BUILD -- P1 Calendar   | casework-tabs/goal.md       |
|                 | PASSED 2026-08-10 at a    | (ratified 2026-08-10)       |
|                 | hands-on gate; P2-P6 +    |                             |
|                 | final walk remain         |                             |

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
  AMENDMENT (program ruling 2026-08-07, ratified by James): the
  client-facing invoice surface in casework/app/server.py (shared
  invoice view, pay flow, post-payment page) is opened to billing-ui
  sessions for RENDERING-ONLY work. Scope: page styling and firm
  identity to match the staff surface; the charge list becomes a
  footed Description | Date | Amount table, MM/DD/YYYY, integer-cents
  formatting (both /100 float divisions removed); a styled pay form;
  a real receipt page after payment (amount, date, method, invoice,
  remaining balance) plus payments listed on the invoice page --
  both SELECT-only readers over existing payment facts, reachable
  under the existing share token. Hard limits: no new business
  logic and no access-model changes -- the only write path remains
  billing.pay_online; spine tests immutable; the walk sheet's quoted
  client-side labels ("Synthetic payment token",
  "SYNTHETIC-VISA-DEMO", "Pay", "Payment received") preserved or
  re-pinned with a sheet-lock re-sync; both invoice languages
  carried; after the work ALL standing suites rerun green and
  quoted, sha supersessions via report_sha.py only, recorded in
  billing-ui's worklog. The client portal (gated item 11) is
  explicitly OUT of this ruling's scope.
  AMENDMENT (program ruling 2026-08-09, ratified by James via the
  signed period-close sheet): the PERIOD-CLOSE ACT
  (billing-ui/period-close.md, rulings PC1-PC3) is authorized as a
  cross-project build from billing-ui sessions. Scope: new module
  casework/app/period.py (compute/prepare/approve/closed-month
  queries); a lock guard called from ledger._post and
  ledger.create_external_event refusing journal entries and
  external events dated into a closed month; schema addition
  period_closes via casework/app/schema/gen_schema.py; new tests
  in casework-billing; rendering in casework-ui/app_ui under the
  existing no-logic discipline. Hard limits: spine tests
  immutable; fiduciary checks may STRENGTHEN, never weaken;
  existing ledger recipe signatures unchanged; after the work ALL
  standing suites rerun green and quoted, sha supersessions via
  report_sha.py only, recorded in billing-ui's worklog.
  AMENDMENT (program ruling 2026-08-10, ratified by James at the
  casework-tabs goal ratification): casework-tabs extends the
  casework-ui surface IN PLACE. A casework-tabs session may write
  casework-ui/app_ui (new screens, routes, SELECT-only readers,
  additive shared chrome) and add new walk/verifier coverage under
  casework-tabs/, with hard limits: run_ui_walk.py stays green at
  casework-tabs phase gates; casework-ui/goal.md is never edited
  and its cold-run oracle, hold status, and ratified protocol are
  untouched; a change to an existing casework-ui screen or its
  walk steps is a gate decision, not a code change; casework/
  stays frozen for this child (all six tabs' logic already lives
  in casework/app; casework-tabs owns rendering only); Settings
  write screens call existing casework/app modules exclusively.
  Oracle: per-tab hands-on gates + a final James-driven cross-tab
  walk, NOT a cold run. After any session's work, all standing
  suites rerun green and quoted; sha supersessions via canonical
  scripts only, recorded in the casework-tabs worklog. Live
  contract: casework-tabs/goal.md.
  AMENDMENT (program ruling 2026-08-10, ratified by James at the
  casework-tabs P2 gate: "yes I think we have to, it will
  happen"): the frozen casework core opens for ONE addition from
  casework-tabs sessions -- tasks.reopen_task (clears
  completed_at; the schema's audit trigger records the undo), the
  recovery path behind the tasks tab's Reopen button after his
  live drive proved accidental completes will happen. Hard
  limits: no other casework/app change rides this ruling;
  existing spine tests immutable and untouched; coverage lands in
  casework-tabs' rail, which drives reopen through the UI and
  asserts the machinery state; after the change ALL standing
  suites rerun green and quoted, sha supersessions via canonical
  scripts only, recorded in the casework-tabs worklog.
- Each child's own CLAUDE.md + state.md is the authority on its state;
  this file's roster is a signpost, not a second snapshot.
- The spec corpus records facts about Docketwise with citations -- it is
  a spec, not a brainstorm. Design ideas for our own product go to a
  child's log-don't-build machinery, not into corpus entries.

## Interface with James (ratified 2026-08-04)

James is the ratifier, not a developer. The state files maintain AGENT
continuity, not his -- a multi-child program scales past the human
ratifier's context long before it scales past the agent's. His early
overload symptom is a forming rubber stamp ("if you're saying you're
capable, that's fine"); gate verdicts signed on trust are worthless.
Rules, all incident-born (2026-08-03/04 sessions):

- Refer to children by on-disk folder name (docketwise-spec, casework,
  casework-ui, casework-billing, billing-ui) in ALL user-facing prose.
  "Child N" is roster-internal jargon; he navigates by folder names in
  Explorer and ordinals map to nothing on screen. The Children table
  above may keep its column; conversation may not.
- His surface is the PRODUCT plus ONE plain-language question per
  touchpoint. Translate all jargon inline -- phase numbers, suite
  tallies, verifier names. At a gate, the question is the LAST sentence
  of the message, nothing after it; the decision queue stays in
  state.md, never in chat.
- Re-issue a plain-terms map of the whole program at every gate and on
  demand.
- One stable URL forever: port 8500 always; swap databases behind the
  port, never hand him a new port.
- Dev-practice tips land when translated into audit/finance analogies
  (engagement partner, month-end close, controls) -- offer them when
  process feels bad to him.
