# goal.md -- billing-ui

Status: RATIFIED by James 2026-08-04, after five red-pen rounds
(worklog s1). This is the contract. Edits are scope changes:
James-ratified only.

## Outcome

casework-ui/app_ui carries a demo-grade billing and trust-accounting
surface. "Working" means, verifiably:

1. James drives the full billing lifecycle -- the substance of the
   anchor billing walk -- entirely through screens on a FRESH
   database: install -> contact + matter -> trust and operating
   accounts -> trust request -> client pays online (SimProcessor) ->
   gross settlement with fee split -> invoice (saved charge +
   imported time entry) -> earn-out trust-transfer payment ->
   disbursement -> invoice PDF -> trust ledger and three-way
   reconciliation visible and holding. No terminal, no SQL, no
   dev-tools assistance mid-walk.
2. The fiduciary suite (F1-F8) runs GREEN against the walked
   database afterward -- the screens produced CPA-grade books.
3. James's demo-grade verdict at the final gate: he would show
   these screens to the firm. This is a human judgment by design
   (see Verifiers); the mechanical checks bound it but cannot
   replace it.

## Baseline (what exists before P0)

- casework-billing COMPLETE 2026-08-03: 25/25 corpus parity, F1-F8
  green x2, anchor billing walk PASS over HTTP (1.336s). All
  billing capability exists at the app layer; this child owes
  VISIBILITY, not capability. result.md is the authority.
- casework-ui ON HOLD pre-verdict: app_ui server runs, 13-step walk
  verifier green, cold-run oracle unmet and UNTOUCHED by this child.
- Zero billing screens exist. The client-actor pages (shared-invoice
  view/download/pay) live in casework/app and are used AS-IS.

## Scope: the 25 entries, tiered (ruled 2026-08-03)

Tier 1 -- interactive screens (walk path + fiduciary visibility):

| Entry                       | Surface owed                        |
| --------------------------- | ----------------------------------- |
| module-exists               | billing area present in app_ui nav  |
| invoice-creation            | create/edit-draft invoice screen    |
| trust-requests              | create + status screen              |
| trust-bank-accounts         | accounts screen (trust + operating) |
| trust-ledger                | ledger browse + drill-down          |
| trust-transfer-payment      | earn-out flow (4-leg recipe)        |
| trust-disbursements         | disbursement flow                   |
| direct-payment-recording    | record-payment screen               |
| online-card-payment         | no own screen [AJ]: status line on  |
|                             | invoice + trust-request screens;    |
|                             | client pay page AS-IS (frozen)      |
| saved-charges               | manage + add-to-invoice             |
| time-tracking               | time entry screen                   |
| time-entry-invoice-import   | import-into-invoice flow            |
| invoice-sharing             | email-only share + PDF download     |

Tier 2 -- interactive screens (corrections family; the CPA demo
moment -- "edit" over posted rows renders as reversal + repost):

| Entry                       | Surface owed                        |
| --------------------------- | ----------------------------------- |
| payment-editing             | edit = reversal+repost, trail shown |
| payment-refunds             | refund flow, reversing entries      |
| payment-charge-association  | re-associate via correction         |

Tier 3 -- DEFERRED, no screens v1 (ruled 2026-08-03: hold). App-layer
defaults stay active invisibly; entries stay green in the parity
suite (capability is casework-billing's, already proven):
payment-reminders, bulk-invoice-sharing, bulk-invoice-download,
automatic-late-fees, payment-plans, invoice-translation,
invoice-access-permissions, default-invoice-settings,
global-invoice-numbering.

## Constraints and quality bar

- IN-PLACE EXTENSION per program ruling 2026-08-03 (../CLAUDE.md):
  screens land in ../casework-ui/app_ui; run_ui_walk.py green at
  every phase gate; ../casework-ui/goal.md never edited; a change to
  an existing casework-ui screen or its walk steps is a GATE
  DECISION, not a code change.
- RENDERING ONLY: no business logic in app_ui. SQL only in
  SELECT-only readers (casework-ui's no-logic lint pattern extends
  to billing readers); all writes go through existing casework/app
  modules. casework/ is FROZEN.
- DEMO-GRADE bar (ruled 2026-08-03): billing screens are
  deliberately the best-looking surfaces in the product. Existing
  casework-ui screens are NOT restyled; shared-shell changes
  (stylesheet, nav) route through gate decisions. The standard set
  here becomes the reference when casework-ui resumes.
- Zero interaction parity: corpus entries say what must be possible,
  never how screens work. Copying Docketwise's billing UI is the
  failure mode.
- Money is integer cents in data; dollars are formatting. A float
  touching a monetary amount is a defect.
- Append-only journal is presented honestly: no screen implies a
  posted row was mutated; correction trails are visible, framed as
  a feature (the audit story), not an apology.
- Synthetic data only. Demos and gate reviews run on fresh seeded
  dbs; never on rehearsal dbs carrying real-ish PII.
- HYBRID operating mode (ruled 2026-08-03): agent builds each phase
  unattended against the mechanical verifier; every phase gate ends
  with James reviewing rendered screens before the next phase
  starts. James's UI time lands at gates.

## Decision defaults (agent judgment marked [AJ])

- Server-rendered pages matching app_ui's existing architecture; no
  new JS frameworks, no build step, no CDN dependencies. CSS-only
  polish plus minimal vanilla JS where a flow needs it. [AJ]
- A dedicated billing stylesheet layered over the app shell; shared
  files untouched without a gate. [AJ]
- Currency renders as $1,234.56; negative amounts parenthesized
  (accounting convention), never minus-sign-only. [AJ]
- Dates render as the business date (posted_at semantics per
  casework-billing worklog P1); wall-clock lives in audit views
  only. [AJ]
- Empty states are designed, not blank tables: each browse screen
  states what will appear there and the action that creates it. [AJ]
- Ledger drill-down order: accounts -> client/matter sub-ledger ->
  journal entries -> entry detail with correction trail. [AJ]
- ANTI-STALL (from James's ruling that AI polish loops stall): max 2
  polish iterations per screen per phase on agent judgment alone;
  the 3rd attempt PARKS the screen with a rendered before/after and
  a one-line statement of what is not working, queued for the next
  gate. A parked screen is not a blocker; the phase proceeds.
- Seed for gate reviews: a billing demo seed script (this child's
  file, calling casework/app modules only -- no direct SQL writes)
  producing enough realistic synthetic activity to judge browse
  screens. The DEMO WALK itself uses a fresh empty db by contract.

## Allowed without asking

- New routes, templates, SELECT-only readers, static assets under
  ../casework-ui/app_ui for billing surfaces.
- New verifier scripts, walk protocol docs, seeds, and tests inside
  billing-ui/.
- New walk/sweep coverage that ADDS checks without touching existing
  casework-ui walk steps.
- plan.md rewrites; state.md overwrites; worklog appends.

## Approval required

- Any edit to an existing casework-ui screen, template, shared
  stylesheet, nav shell, or walk step (gate decision by rule).
- Any change under ../casework/ (frozen; includes the client-actor
  pages -- restyling them is a flagged gate decision).
- Any schema change, new pip dependency, or new background process.
- Real processor integration (standing program rule; post-v1).
- Editing this file. James ratifies; agent edits are scope changes.

## Forbidden

- Business logic or non-SELECT SQL in app_ui.
- Editing frozen suites: casework spine tests, billing parity suite,
  fiduciary suite, existing run_ui_walk steps.
- Touching ../casework-ui/goal.md, its cold-run protocol, or its
  hold status.
- Tier-3 screens, real payment rails, live PII, emoji anywhere.

## Verifiers

Two verifiers per the method: a mechanical walk that runs from day
one, gating a live human-driven proof.

Verifier 1 -- mechanical billing UI walk (billing-ui/verify/
run_billing_ui_walk.py). Scripts the demo walk at HTTP level against
the app_ui server on a fresh db: every step of the Outcome walk
executed via the real routes and forms a browser would hit, asserting
on rendered content (names, amounts, ledger lines -- claims, not
HTTP 200s). Missing screens report PENDING, exit 1, verdict ON TRACK
(casework-ui pattern), so it runs RED on day one and turns green
screen by screen. Rides with sweeps: no-logic lint over billing
readers, float sweep over presentation code, tier-3 fence (no route
exists for deferred entries).

Verifier 2 -- the James demo walk (live). Protocol doc drafted in P0
(billing-ui/verify/demo-walk-protocol.md) and red-penned before
first use: fresh dated db, walk steps as a task sheet, James drives
unassisted by dev tools. Soft budget 25:00 over the full walk,
M1->M7 (ruled by James 2026-08-10; the budget always spans through
the sheet's final step) [AJ -- this is a demo-fluency guard, not a
cold-run stopwatch; blowing it triggers a friction log, not a
FAIL]. After "done": fiduciary suite must
exit 0 against the walked db, invoice PDF eyeballed, ledger and
reconciliation screens shown holding. PASS additionally requires
James's demo-grade verdict, structured as three named up/down
sub-verdicts, ALL required (ruled 2026-08-04):
  (a) FIDUCIARY STORY LANDS -- ledger, correction trail, and
      reconciliation screens make the CPA-grade case visibly;
  (b) NOTHING EMBARRASSING -- no screen James would apologize for
      mid-demo;
  (c) BOOKABLE -- James would book the firm meeting on this build.
A FAIL names which sub-verdict failed; that names the fix axis.

Standing gates at every phase close: run_ui_walk.py green (existing
13 steps), spine 107 green, billing parity 25 green, fiduciary 8
green. Any red = the phase is not closed.

## Supporting checks

- Reversal presentation check: after a payment edit via UI, the
  journal shows original + reversing + replacement rows and the
  screen renders the trail; no UPDATE touched a posted row (F8
  machinery already guards this; the check asserts the UI told the
  truth about it).
- Fresh-db first-visit check: billing nav reachable from /setup
  without seeded data; every tier-1/2 screen renders a designed
  empty state.
- PDF read-back on the walked db (anchor pattern).

## Completion proof (paths that must exist)

| Path                                      | Proof                       |
| ----------------------------------------- | --------------------------- |
| verify/billing-ui-walk-report.txt         | GREEN exit 0, x2            |
|                                           | byte-identical              |
| verify/demo-walk-protocol.md              | ratified before first use   |
| verify/demo-walk-report.md                | James PASS + demo-grade     |
|                                           | verdict + friction log      |
| data/demo-walk-<date>.db                  | the walked db, retained     |
| verify/gate-receipts/                     | per-gate: 4 standing suites |
|                                           | green + James screen review |
|                                           | noted                       |
| result.md                                 | written only past all above |

## Iteration and recovery

- Phase gates are the recovery points (hybrid mode): each gate
  re-runs all standing suites and banks receipts before James's
  screen review.
- A failed demo walk logs findings, fixes are ruled at a mini-gate,
  and the walk re-runs on a fresh db. No fix lands unruled.
- Parked screens (anti-stall default) are ruled at the next gate:
  James either accepts as-is, redirects with a concrete kill, or
  defers the screen.

## Blocker rule

Difficulty, long runtime, model uncertainty, ugly-first-draft
screens, and failed polish attempts are NOT blockers. A real blocker
needs concrete evidence, no safe fallback, and persistence across
three consecutive turns. In hybrid mode a candidate blocker that
survives to a phase gate is presented there instead of halting
mid-phase, unless it blocks the phase's own verifier from running.

## State files

goal.md (this contract) / plan.md (agent's, rewritten freely) /
state.md (overwritten each wind-down) / worklog.md (append-only;
METHOD: prefix for method observations) / result.md (only after
completion proof). Wind-down runs the goal-method checklist,
including the kill-sweep.
