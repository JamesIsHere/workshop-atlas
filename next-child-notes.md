# next-child-notes.md -- RETIRED 2026-08-01

RETIRED at casework/goal.md ratification (2026-08-01). Content folded
into casework/goal.md (scope, constraints, defaults) and the casework
worklog (rulings, live revisit triggers). This file is an archive of
the pre-contract discussion, kept per delete=archive; it is NOT a live
authority. Live authority: casework/goal.md.

# ORIGINAL CONTENT BELOW (pre-scaffold decision ledger)

Running notes from the goal discussion (started 2026-08-01, workshop-root
session). This file exists so decisions survive session boundaries; it is
folded into the new child's goal.md at scaffold time and then retired.
Not a contract -- James ratifies goals, this is working memory.

## Decided

- 2026-08-01 GOAL SHAPE: capability parity on a core spine, zero
  interaction parity. Corpus criteria define what must be POSSIBLE;
  interaction design is explicitly free; training/time cost is a design
  constraint from day one. Literal parity-then-pull-back REJECTED.
- 2026-08-01 SPINE (module-level, live corpus entries): contacts-and-
  matters (14), smart-forms (41), case-tracking (10), files-and-
  documents (18), template-automation (4), events (4), notes (7),
  login + personal-settings (4). Total 102 live entries, 43% of corpus.
- 2026-08-01 CLEAR DEFERS: leads-crm, docketwise-iq, internal-chat,
  integrations (17 of 19 entries), desktop-app, free-trial,
  client-portal (intake loop already lives in smart-forms; portal
  dashboard + HR portal deferred).

- 2026-08-01 INVOICING-AND-TRUST-ACCOUNTING (25 entries): OUT of the
  v1 spine. v1 identity is COMPANION -- the casework core that tests
  the time/training/quality-of-use thesis -- not a Docketwise
  replacement. See the strategic flag below; this is a defer, not a
  kill.

## STRATEGIC FLAG -- payments/trust layer (revisit deliberately)

  [!] BIG MARK, James 2026-08-01: the payments/trust analysis could
  change the whole project. Docketwise's owner (AffiniPay/8am,
  Genstar + TA) is a payments company that bought the software layer;
  the business model is ~3% of firm collections, not software fees.
  The moat is bar-association endorsement + compliance fear, and the
  fee-split mechanics (gross settlement to trust, fees/chargebacks to
  operating) are near-trivial engineering. Trust accounting is where
  a CPA has an unfair advantage and where the industry's economic
  soft underbelly is.

  Standing rule while deferred: if invoicing ever enters scope, the
  ledger must be trust-shaped from the first schema -- client
  sub-ledgers, earn-out transfer as first-class workflow, three-way
  reconciliation, gross-vs-net settlement awareness. Retrofit-hostile.
  Never build payment processing itself; integrate a fee-split
  processor (LawPay, Confido, Gravity).

  Revisit triggers: (a) v1 spine proves the design thesis with the
  friend's firm; (b) friend feedback surfaces billing/trust pain;
  (c) any move from learning-build toward product.

## Parked with triggers

- CALENDAR SYNC (integrations.google-calendar, integrations.outlook-
  calendar): NOT in spine -- adding complication. Trigger: ask the
  friend whether "calendar" means the in-app calendar or Google/
  Outlook staying in sync. If the latter, carve these 2 entries in.

- 2026-08-01 CLIENT-COMMUNICATION (12): OUT of v1, whole module. The
  spine already forces minimal transactional email (smart-forms
  intake invitations, events reminders); the comms HUB (conversations,
  templates, bulk, SMS) is deferred. SMS deferred with prejudice --
  A2P 10DLC registration + consent compliance is heavy plumbing for
  an unproven need. Trigger: ask the friend where client-chasing time
  actually goes (email volume, texting, phone); if email-chasing is
  the top time sink, this module jumps the queue.

- 2026-08-01 FIRM-SETTINGS (17): SPLIT, accepted by James. IN (8):
  managing-users, user-permissions, user-permission-groups, 2FA,
  time-zone-setting, notification-settings, universal-search,
  trash-can (soft delete = schema-level, decide-now). OUT as design
  position (6): custom-dashboard, custom-columns, results-per-page,
  firm-logo, firm-branches, accounting-notes -- config-depth entries
  are complexity-as-feature, the thing the thesis bets against;
  good defaults over customization engines. EXCLUDED as N/A (3):
  subscription-tiers, subscription-management, data-security
  (vendor-side billing + security marketing; data-security maps to
  nonfunctional requirements). Spine now 110 live entries.
  NOTE: first entry-level curation below module level -- principled
  exception: no-curation protects CASEWORK capabilities; these are
  meta-capabilities (customizing the tool itself).

## Goal-writing inputs (for the new child's goal.md)

- Six invariants of case management (first-principles decomposition,
  2026-08-01; converges with the empirically-derived spine): matter
  registry (+conflicts), single fact store (enter once, flow
  everywhere), deadline engine with provenance, document production +
  custody, fiduciary ledger (deferred w/ flag), accountability record.
- Schema-level commitments no corpus entry names (Docketwise's
  internals are not publicly attested): SINGLE FACT STORE and AUDIT
  TRAIL go into goal.md as first-class constraints alongside the
  capability list. Soft delete (trash-can) likewise schema-level.
- The core is a data model, not a feature set; most deferred modules
  (reports, portal, comms hub, config depth) are VIEWS over the
  invariants.

- 2026-08-01 REPORTS (17): OUT except vmax-tracking CARVED IN --
  visa max-out is deadline-engine substance (H-1B six-year clock,
  conditional-PR second year) misfiled as a report; belongs with
  case-tracking's date machinery. Other 16 deferred: report builder
  family + canned reports over deferred modules + mechanics -- all
  views. Revisit trigger: ask the friend which management numbers he
  actually looks at monthly. SPINE FINAL: 111 live entries, every
  module ruled.
- 2026-08-01 DESIGN COMMITMENT (ours, not a corpus carve): v1 ships
  clean CSV export of core entities (contacts, matters, tasks,
  events). Escape hatch instead of a report builder; anti-lock-in
  statement vs the 8am model.

- 2026-08-01 PROJECT SHAPE: ONE build child holding the whole
  111-entry spine, phased internally (data spine -> forms engine ->
  deadline machinery; sequencing is plan.md territory). Module-
  children REJECTED: the single-fact-store invariant means modules
  share one schema/audit-trail/deadline-engine; per-module projects
  would recreate integration seams. MOVE QUESTION RESOLVED AS NO-OP:
  atlas stays a program root (docketwise-spec sealed, spikes
  archived, build child alongside). No flattening.

## Open (goal.md/plan.md drafting content, not pre-scaffold)

1. Child name (pre-scaffold -- determines the folder).
2. Architecture stance: single-firm deployable vs multi-tenant SaaS
   (the "what does cheaper mean structurally" question).
3. Groundwork boundary: what gets built before friend feedback vs
   what waits.
4. Feedback plumbing: structured interview w/ friend; whether the
   queued arctic-shift Reddit market-research idea gets promoted.
5. Spikes reuse: greenfield vs harvest (G-28 mapping, PDF fill,
   workflow engine, server + legal_crm.db in atlas/spikes/).

## Context facts (verified 2026-08-01)

- Friend's firm: 100% immigration law, runs Docketwise, ~17k/yr quote.
  Pain is time / quality-of-use / training, NOT the sticker price.
  Feedback channel pending -- questions queue in parked-triggers above.
- Docketwise owner: AffiniPay, rebranded "8am" Aug 2025 (LawPay,
  MyCase, CASEpeer, Docketwise, CPACharge). PE: Genstar Capital + TA
  Associates. Payments company that bought the software layer, not the
  reverse. Vendor monetizes collections volume (~3% take), not firm
  efficiency -- structural explanation for the training-cost complaint.
