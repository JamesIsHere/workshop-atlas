# worklog.md -- casework-tabs (append-only)

## 2026-08-10 -- s1: bootstrap from the tab-review ledger

Session context: atlas-root session that ran the six-tab UI review
(../tab-review-notes.md) end to end, then James ruled "bootstrap
the build child now." Interview rulings, each taken one-per-turn:
name casework-tabs (over tabs-ui, surface-ui); mode PHASE-GATED
HYBRID (unattended within phases, hands-on gates between); oracle
per-tab hands-on gate verdicts PLUS a final cross-tab walk on a
fresh db with signed short verdict (over per-tab-only -- James:
tab-local review misses the seams).

Scaffolded via project-kit (folder + CLAUDE.md; Data-freshness
template section deleted -- no generated artifacts yet). goal.md /
plan.md / state.md / this file drafted in one pass from the ledger
per the ledger-as-interview pattern (casework precedent): the
review's rulings land as goal.md Appendix A; the in-place-extension
amendment lands as Appendix B DRAFT for James's ratification.

METHOD: second full ledger-as-interview instance. The interview
collapsed to exactly three questions (name, mode, oracle) because
the review ledger had already banked every design ruling -- the
bootstrap cost moved from interview to the review that produced
the ledger. Phase-gated hybrid chosen BY NAME from the skill's
modes section on its first day as a named mode (promoted this
morning, Trial 4 retro promotion pass).

METHOD: today's new doctrine applied at draft time, not
retrofitted: scope-bounded verdict pendency in Iteration and
recovery; world-blocked arm in the Blocker rule; self-audit
questions ratified in-contract (item e added for the ruling
queue); retro-rides-final-wind-down in P7; deferral-load check
queued for the ratification signature.

goal.md is UNRATIFIED. Red-pen next.

## 2026-08-10 -- s1 cont: RATIFIED after one round + deferral-load
## check

Red-pen round 1: four candidate kills primed (e-sign out of
contract; walk-budget gap; chrome-bar softening; permissions
view-only) -- James: "I say it looks good!" = four KEEPs. Per the
standing deferral-load rule the check ran before the signature:
4 keeps / 0 kills / 0 parks / 1 silent skip converted to a typed
deferral (final-walk time budget -> owed at P7 walk-sheet
ratification). Forward obligations typed and homed (walk budget ->
P7; e-sign P4b gate -> plan.md; interleaved timeline -> rendered-
artifact gate; calendar sync -> meeting queue; Appendix B + roster
+ ledger retirement -> this signature). Fences (config-depth six,
cold-run imports, new business logic, SMS) vs deferrals separated.
Counter-pressure named: second ledger-fed zero-kill ratification;
front-loaded reading has direct evidence this time (the review WAS
the red-pen -- 15+ rulings one call per turn, several against the
agent's lean: "both" on trash, "everything" on calendar reach).
James then signed explicitly: "yes".

Signature acts executed: goal.md header restamped RATIFIED;
Appendix B ratified into atlas/CLAUDE.md (program amendment
2026-08-10) + casework-tabs roster row added; tab-review-notes.md
RETIRED (archive header, next-child-notes precedent); CLAUDE.md
State table + state.md rewritten to pre-P0.

METHOD: deferral-load check's first outing as STANDING procedure
(promoted this morning); it converted a silent skip into a typed
deferral in real time -- the exact failure mode it exists to
catch. Bootstrap-to-ratification ran in one sitting on a ledger
fed by a same-day review; the four-file harness now holds a
ratified contract that has never had an unsupervised session.

## 2026-08-10 -- s2: U0.1 -- P0 harness built, rail driven RED

Built casework-tabs/verify/: run_tabs_walk.py (the rail, 30 steps),
seed_tabs.py (gate-review demo db, casework/app module calls only,
zero SQL writes), report_sha.py (canonical sha, billing-ui recipe).
No app_ui file touched -- oracle-first held: the rail exists and
runs RED before any screen work.

Rail design, on the billing-ui pattern plus one extension: the six
tab routes already exist as read-only casework-ui screens, so the
rail carries TWO Pending probes -- probe() (authed GET landing on
the 404 page = new route unbuilt) and expect_marker() (route lives
but the ruled redesign's contract marker is absent = Pending, never
FAIL). Markers are additive so the frozen run_ui_walk.py stays
true. Walk order follows phase order (P1 calendar ... P6 settings)
so gates see contiguous greens. The route names, form fields, and
marker hooks pinned in the step bodies ARE the P1-P6 interface
contract. Goal.md's three supporting checks live in the rail:
float sweep + ISO-stray sweep (runtime, tag-stripped pages of tab
steps only) in the report's sweep section; the empty-state sweep is
walk step 2 (fresh-db crawl; designed = <div class='empty-state'>
carrying the creating action).

RED run quoted: "tabs-walk: 2 pass, 28 pending, 0 fail; sweeps
pass; verdict ON TRACK (pending screens)", exit 1 -- exactly the
contracted P0 shape (foundation green, every tab step PENDING with
a named reason). x2 stable, canonical sha e084bd4b (report_sha.py).

Verify-the-verifier, four deliberate sabotages, each FAILed then
reverted: (1) setup-step label -> FAIL step 1; (2) client+matter
redirect regex -> "FAIL client + matter ... AssertionError:
http://127.0.0.1:55245/matters/1"; (3) injected page with visible
ISO date -> "FAIL iso-stray-sweep: strays: /leak: 2026-08-10";
(4) scratch file with float() + /100 -> float-sweep caught both
patterns. Owed forward: the empty-state FAIL arm (marker without
action) and each tab step's full body get their own deliberate RED
at the phase that builds them (per-phase rhythm step 1).

seed_tabs.py green: "3 users; 4 contacts; 4 matters; 8 events;
7 tasks; 4 notes; 4 files; 2 invoices" -- appointments with
attendees/end-times, expiry rules -> 3 auto events, 2 vmax dates,
invoices with due dates (all six calendar kinds represented),
task list with a reference-date item imported onto a matter, note
categories + pin + notify-all, e-sign draft + requested states,
recents, trash content. Disclosure: the seed touches billing
modules (operating account + 2 invoices) solely because the ruled
unified calendar shows invoice due dates; module calls only, demo
db lives under casework-tabs/data/ (gitignored).

Standing suites all green, quoted: "spine: 107 green, 0 red,
0 pending; checks pass" / "billing: 25 green ... verdict: GREEN" /
"fiduciary: 9 pass, 0 red, 0 stub; verdict: GREEN" / "ui-walk: 13
pass, 0 pending, 0 fail; sweeps pass; verdict GREEN".

[Q] ruling queue (for the P1 gate):
- [Q1] Derived calendar kinds (expiry, vmax, invoice-due) have NO
  UI creation path today: facts come from client intake, and the
  billing UI reads due_date but never writes it. The rail's
  derived-kinds step probes markers only until ruled. Options:
  (a) mirror the existing intake flow inside the walk, (b) give
  the New-deadline form a fact-writing variant (module call, no
  new logic), (c) a gate-ruled exemption letting the walk seed
  derived-kind content by module call. Agent lean: (b) for expiry/
  vmax -- it makes the deadline form genuinely useful -- plus (c)
  for invoice due dates only.

METHOD: oracle-first rail is now a three-peat pattern (billing-ui
-> period-close -> here); the new marker-probe arm existed because
this child REDESIGNS live screens rather than adding a fresh area
-- 404-probing alone cannot express "route exists, design pending."
Worth folding into the skill at the next retro if it survives P1.
