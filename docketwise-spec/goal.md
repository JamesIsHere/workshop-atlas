# goal.md -- docketwise-spec

RATIFIED 2026-07-31 by James, explicit, after seven red-pen rounds
(worklog session 1). Edits from here are scope changes and require
approval.

OPERATING MODE (ruled red-pen round 7, 2026-07-31): PHASE-GATED
HYBRID -- unattended execution within phases, human gates at [G1]
(post-pilot: protocol freeze, sparse-module question, fan-out model
ruling) and [G2] (reproduction-audit diff ruling, criterion
spot-check). The gates are CONTRACT, not courtesy: fan-out does not
start without [G1] passage; result.md does not exist without the [G2]
ruling. Between gates, the Decision defaults and Blocker rule govern
exactly as in unattended mode -- no human is assumed present
mid-phase.

## Outcome

A feature-level specification corpus of Docketwise's publicly attested
product surface that an agent can mechanically verify for schema
compliance, citation closure, and cross-source coverage -- so that the
corpus can serve as the acceptance-criteria oracle for downstream atlas
build children. The outcome is the corpus PLUS the proof machinery: an
oracle that answers "is this corpus complete relative to the enumerated
public surface, and is every claim in it attested?" with exit 0.

Not the outcome: any product code, any UI, any design for our own
system, any claim about Docketwise internals not visible from public
sources.

## Baseline

Nothing exists. No corpus, no fixtures, no inventories. atlas/spikes/
holds pre-program build experiments (form filling, workflow engine) --
they are assets for future build children and are out of scope here.
Prior knowledge of Docketwise in this workshop is reputational only;
every corpus claim starts from zero attestation.

## Constraints and quality bar

- PUBLIC SURFACE ONLY (program ruling): docketwise.com marketing pages,
  the public help center / knowledge base, official YouTube channel
  (demos, webinars), published release notes, and third-party review
  corpora (G2, Capterra, lawyer-forum threads). Ordinary page fetches
  only -- nothing behind a login, no robots-hostile crawling, no
  account creation anywhere.
- FEATURE-LEVEL granularity (program ruling): an entry is the smallest
  capability a Docketwise user could notice as present or absent.
  Behavior-level detail is captured opportunistically in the entry's
  detail field when a source offers it cheaply, never hunted.
- CAPTURE-FIRST: every source page/transcript mined is saved to
  fixtures/ before anything cites it. Corpus entries cite fixture ids,
  never live URLs alone. Fixtures are immutable once captured; a
  changed page is re-captured as a NEW fixture with its own date.
- Entry schema (every corpus entry):
  | Field       | Content                                              |
  | ----------- | ---------------------------------------------------- |
  | id          | stable slug, never reused                            |
  | module      | Docketwise's own module vocabulary where public      |
  | name        | Docketwise's term if attested, else NAMED-BY-US flag |
  | description | what the feature does, 1-3 sentences, cited          |
  | criterion   | testable acceptance criterion for a future build     |
  | sources     | fixture ids, one per attestation                     |
  | tier        | confirmed (2+ source families) / provisional (1)     |
  | detail      | optional behavior-level notes, cited                 |
  | gap         | optional SOURCE-GAP note: what is unknown + which    |
  |             | source could resolve it                              |
- The corpus is APPEND-AND-SUPERSEDE for CONTENT: entries are never
  deleted; a re-read source, rewritten criterion, or re-drawn feature
  boundary supersedes the old entry with a pointer to its replacement
  and a one-line why. MECHANICAL SCHEMA MIGRATIONS are exempt (ruled
  red-pen round 6): field renames and format changes are applied in
  place corpus-wide, recorded once in the worklog with the migration
  rule, oracle re-run green after -- no per-entry supersede ceremony.
  The ratchet protects changed READINGS, not changed file formats.
  Oracle counts only live entries for coverage and tiers, but still
  validates superseded entries' pointers -- a dangling replacement
  pointer is a schema failure.
- All files ASCII-only, no emojis, tables padded (workshop rules).

## Decision defaults

- Feature boundary doubt: SPLIT. Two small entries merge cleanly at
  module rollup; one merged entry cannot recover per-feature
  attestation. Splitting is the reversible error.
- Source conflict (two sources disagree): record BOTH with provenance
  in the entry, tier drops to provisional. Never average or pick.
- Marketing-only claims with no help-center corroboration: admitted,
  tier provisional. Marketing exists to overclaim; the tier carries
  that skepticism so admission is safe.
- Video facts: mine transcripts/captions where available; a fact seen
  only on-screen is citable with video fixture id + timestamp.
- A source family that proves unminable (fetch-blocked, paywalled):
  log it in the exclusion log with evidence, proceed on the remaining
  families, and record the coverage consequence. Not a blocker unless
  the minable families fall below three.
- Naming: prefer Docketwise's vocabulary; where sources give none, use
  a neutral descriptive name and flag NAMED-BY-US.

## Allowed without asking

Fetching and capturing public pages; creating/organizing fixtures,
inventories, and corpus files; writing and re-running oracle code;
rewriting plan.md; superseding corpus entries; adding entries to the
exclusion and rejection logs.

## Approval required

Creating an account anywhere; submitting any form on an external site;
contacting any person; adding a source family beyond the five
enumerated; editing this file (scope change); declaring completion.

## Forbidden

Trial-account or any authenticated access; fetching behind logins or
against robots exclusions; inferring or fabricating features no
captured source attests; hand-editing a captured fixture; deleting
corpus entries; building any product code (log-don't-build applies --
temptations go to the worklog).

## Verifiers

Two-verifier pattern: a mechanical corpus oracle (backtest analog,
runs from day one) gating a fresh-eyes reproduction audit (live
analog, final proof).

VERIFIER 1 -- oracle.py, all checks mechanical, exit 0 required:

  1. SCHEMA: every entry parses and carries every required field.
  2. CITATION CLOSURE: every cited fixture id exists on disk and
     appears in fixtures/manifest; no corpus claim cites a live URL
     without a fixture; no orphan fixtures older than the current
     session without either a citing entry or an exclusion-log line.
  3. COVERAGE CLOSURE (the completeness oracle): five inventory
     artifacts are extracted first, one per source family -- marketing
     nav/feature-page tree, help-center category tree, YouTube video
     list, release-notes index, review-site feature checklists. Every
     inventory item maps to >=1 corpus entry OR one exclusion-log
     ruling with rationale. Completeness is defined as closure over
     the union of inventories -- never as a feeling of doneness.
     Inventories bound the COVERAGE CHECK, not the reading: extraction
     reads full sources, and features attested inside an inventoried
     source (e.g. thirty attestations inside one webinar line) are
     captured. The inventory is a floor for completeness, never a
     ceiling on capture.
  4. ATTESTATION TIERS: tier field consistent with the sources field
     (confirmed requires >=2 distinct source families); report counts
     per tier and per module.
  5. CRITERION LINT: every non-gap entry's criterion matches testable
     form (names an observable behavior and a pass condition) --
     structural check only; semantic quality is the audit's job.
  6. SOURCE-GAP INTEGRITY: every gap note names what is unknown AND
     which source class could resolve it; gap entries are counted and
     reported as the trial-account decision inventory.
  7. DETERMINISM: two consecutive oracle runs produce byte-identical
     reports.

VERIFIER 2 -- reproduction audit (final, gates result.md):
A fresh agent -- no corpus in context AND a different model than the
extractor, so shared model priors cannot reproduce the same misreading
-- receives the cited fixtures for a random sample of 15 entries and re-derives feature descriptions from
fixtures alone; diffs against the corpus are reported per entry. James
rules on the diff report and spot-checks criterion semantics. The
corpus passes when James's ruling says the diffs are transcription
noise, not extraction error.

Supporting checks: fixtures/manifest (id, URL, capture date, sha256);
exclusion log (inventory items ruled out-of-scope, with why); rejection
log (candidate entries rejected during extraction and why -- the
Trial 3 invisible-churn counter, kept visible here).

## Completion proof

All of the following exist on disk, or there is no completion:

- corpus/ with one file per module, entries in schema
- fixtures/ + fixtures/manifest with every cited capture
- inventories/ with all five source-family inventories (or an
  exclusion-log ruling for a dead family)
- oracle.py + its exit-0 report, quoted in the worklog
- audit/ with the reproduction-audit diff report and James's ruling
- result.md, written only after both verifiers pass

## Iteration and recovery

- ORACLE-FIRST (method op rule 7): oracle.py is built and green on a
  seed micro-corpus (3-5 hand-made entries + fixtures) BEFORE mass
  extraction starts. Extraction then pre-validates against exactly
  what the oracle checks.
- Rejection reasons are counted and logged per module -- the churn
  signal Trial 3 lost stays observable.
- Compaction-readiness: each module's evidence (entry count, oracle
  state, open questions) is written to disk at module close; state.md
  is rewritten at every wind-down. Assume any session can die
  mid-module and must resume from files alone.

## Blocker rule

Difficulty, long runtime, model uncertainty, and failed first attempts
are not blockers. A real blocker needs concrete evidence, no safe
fallback, and persistence across three consecutive turns. Specifically
pre-ruled: one unminable source family is NOT a blocker (exclusion log
+ proceed); fewer than three minable families IS a blocker candidate
-- halt and surface. Why three is load-bearing, not tunable: two
families is the bare minimum for the confirmed tier to exist, and at
two, every confirmed entry hinges on the same single pair -- one
systematically wrong family poisons the tier; below three, coverage
closure degrades to "we read their website" while the oracle still
exits 0. The halt means "the goal as ratified cannot be met --
re-scope," not "stuck."

## Wind-down self-audit (ratified questions, per method checklist 5)

At final wind-down, answer in the worklog before result.md: (a) did
compaction fire and what survived; (b) did state.md/worklog.md suffice
at every resume; (c) did any blocker candidate reach three turns; (d)
was log-don't-build honored in real time or backfilled; (e) NEW for
this trial: did the coverage-closure definition of "complete" ever
conflict with judgment about actual completeness, and who won.

## State files

goal.md (this contract) / plan.md (strategy, agent-owned) / state.md
(cold-resume snapshot, overwritten) / worklog.md (append-only).
CLAUDE.md State table signposts to state.md and never duplicates it.
