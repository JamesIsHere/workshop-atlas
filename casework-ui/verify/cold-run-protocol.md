# cold-run-protocol.md -- verifier 2 (RATIFIED)

Status: RATIFIED by James 2026-08-03 at the P3 gate. Decisions
(a) M1->M5 budget and (b) no preparer step ruled the same day,
informed by rehearsal 1. Budget challenge at ratification (2:00
proposed by James, 5:00 counter-proposed) RULED: 15:00 stands.
This document binds verifier 2 as written; edits now require a
gate.

Contract hooks (goal.md, ratified 2026-08-01): at least one COLD
USER -- a person who has never operated the system -- completes
the anchor task sheet unassisted, by clicking, on a fresh
database, within the time budget (default 15 minutes). James's
own runs are rehearsal, never proof. A failing run is a FINDING:
fix, re-recruit, re-run. The contract needs one pass.

## Roles

- RUNNER: the cold user. Qualifies if they have never operated
  this system (any build) before the run. One run per person --
  a second attempt is never cold.
- PROCTOR: starts the stopwatch, records marks and friction,
  plays no other part. The proctor NEVER answers questions about
  the software. Permitted sentences: "That's up to you." /
  "Whatever you think." / "I can't help with that." Anything
  about the task sheet's WORDING may be clarified; anything about
  the SCREENS may not.

## Setup (proctor, before the runner sits down)

1. Fresh database -- from casework-ui/, with TODAY'S date typed
   into the filename (rehearsal 1 finding: a placeholder pasted
   verbatim dies with an opaque sqlite error). Example for a run
   on 2026-08-05:
   `python -m app_ui.server --db data/cold-run-2026-08-05.db
   --port 8500 --client-port 8501`
   The db file must not exist beforehand; first visit lands on
   /setup. Never reuse a db between runs.
2. Two browser windows ready: a normal window at
   http://127.0.0.1:8500 (firm), and an incognito/private window
   OPEN BUT BLANK (client leg; separate cookie jar).
3. Print or display the TASK SHEET below (self-contained: all
   data values are inline in its steps).
   The runner may read them at any time. Nothing else: no demo,
   no tutorial, no second monitor with docs.
4. Stopwatch ready. Recording form (bottom of this file) blank.
5. PROOF RUNS REQUIRE A LIVE PROCTOR (rehearsal 1 finding: a
   solo runner cannot both run and record -- marks went entirely
   unrecorded). Solo rehearsals: screen-record or timestamp
   screenshots so marks can be reconstructed.

## Task sheet (handed to the runner verbatim)

You work at a small immigration law firm. The software in front
of you is the firm's case system. You have never seen it before.
Nobody will help you. Everything you need is on this sheet, in
order -- read top to bottom, no jumping. All data is synthetic:
type the values shown EXACTLY, never your own name or email
(the browser's autofill will offer them -- refuse it; real data
voids the run). Leave any field this sheet does not mention
blank.

A new client, Priya Sharma, has retained the firm for a G-28
(notice of attorney appearance). Using the firm window:

1. Set yourself up. The system is brand new -- it will walk you
   through creating the firm's first account. When it asks:

   | Field     | Value                        |
   | --------- | ---------------------------- |
   | Your name | Casey Morgan                 |
   | Email     | casey.op@synthetic.test      |
   | Password  | coldrun-synthetic-pass       |

   After "Create account", two screens follow on their own:
   "Set up two-factor authentication" (one button) and "Enter
   your code" -- the 6-digit code is DISPLAYED ON THAT SCREEN
   (this synthetic environment sends no real email); type it
   and Verify. If you are ever logged out later, the same
   email and password above log you back in.

2. Put Priya in the system as a client. When a screen asks:

   | Field                    | Value                        |
   | ------------------------ | ---------------------------- |
   | Given name (first name)  | Priya                        |
   | Family name (last name)  | Sharma                       |
   | Email                    | priya.client@synthetic.test  |
   | Phone                    | +1-555-0400                  |

3. Open a matter for her G-28 representation.

4. Send Priya the intake invitation for a G-28 form package.

5. Priya fills in her own details from home: when the system
   gives you a client link, open it in the incognito window
   and answer as Priya. Fill exactly these fields, leave the
   rest blank, then Submit:

   | Field                            | Value                       |
   | -------------------------------- | --------------------------- |
   | Client family name               | Sharma                      |
   | Client given name                | Priya                       |
   | Client daytime telephone number  | +1-555-0400                 |
   | Client email address             | priya.client@synthetic.test |
   | Client street number and name    | 400 Coldrun Way             |
   | Client city or town              | Faketown                    |
   | Client state                     | VA                          |
   | Client ZIP code                  | 00004                       |

6. Back in the firm window: check her returned answers, then
   download the filled G-28 PDF.

7. The firm must file within two weeks: put a filing deadline on
   the calendar two weeks from today, with an email reminder 2
   days before.

You are done when the G-28 is downloaded and the deadline is on
the calendar. Say "done" out loud.

## Timing marks (proctor records all; decision (a) picks the pair)

| Mark | Moment                                             |
| ---- | -------------------------------------------------- |
| M0   | Firm window loads its first screen (setup begins)  |
| M1   | Dashboard first reached (account ceremony done)    |
| M2   | Intake invitation sent (client link visible)       |
| M3   | Client leg submitted (incognito window)            |
| M4   | G-28 PDF downloaded                                |
| M5   | Deadline visible on the calendar ("done")          |

## Pass criteria

- Unassisted: zero proctor help about the screens. One violation
  voids the run as proof (it still counts as friction data).
- Complete: M5 reached; the PDF opens and carries Priya's family
  name; the calendar shows the deadline with its reminder.
- ARTIFACTS COMPLETE (rehearsal 1 finding: a run can LOOK done --
  filled PDF in hand -- while skipping the invitation and client
  leg entirely and never saving the deadline; eyeballs cannot
  catch that). After "done", the proctor runs, untimed:
  `python verify/check_cold_run.py data/cold-run-<their-date>.db`
  Exit 0 required: it asserts the db receipts of every story leg
  -- firm + client sheet values followed, invitation row, fact
  writes by
  actor 'contact' (the client leg is the anchor's defining
  feature), invitation returned, deadline event tied to the
  matter, reminder attached.
- In budget: elapsed time within 15:00 per decision (a).
- Verification after the run (proctor, not timed): open the
  downloaded PDF and the calendar entry; record both.

## DECISION (a) -- RULED 2026-08-03 (James, P3 gate): Option 2

THE BUDGET RUNS M1 -> M5: the account ceremony sits OUTSIDE the
15:00. Rationale: matches goal.md decision default 4 ("from
first login screen"); the thesis measures per-case interaction
cost and the ceremony is a once-per-firm cost. Rehearsal
evidence: ceremony ~4:00 (~27% of budget). Recording rule
stands: BOTH pairs (M0->M5 and M1->M5) are always recorded, so
the report can also state the zero-to-artifact number.

## DECISION (b) -- RULED 2026-08-03 (James, P3 gate): Option 1

NO PREPARER STEP ON THE TASK SHEET. The cold run is an
interaction-cost instrument, not a second correctness oracle --
fill correctness is the mechanical walk's job, and the runner
never touches what the UI cannot edit (preparer WRITE screens
out of v1 scope, P1 ruling). Rehearsal signal: the runner
reviewed the PDF closely enough to report three findings and
never remarked on the attorney block.

## Recording form (one per run; copy into cold-run-report.md)

```
RUN ------------------------------------------------------------
Date (UTC):            ____________
Runner id (initials):  ____________   Cold? (never operated): Y/N
Rehearsal or proof:    ____________
Db file:               data/cold-run-________.db  (fresh: Y/N)

MARKS (HH:MM:SS stopwatch)
M0 setup begins:       ____________
M1 dashboard reached:  ____________
M2 invitation sent:    ____________
M3 client leg done:    ____________
M4 G-28 downloaded:    ____________
M5 deadline visible:   ____________
Elapsed M0->M5:        ____________
Elapsed M1->M5:        ____________

ASSIST VIOLATIONS (each voids proof): ____________

FRICTION LOG (thesis data -- capture everything)
 # | screen/step | what happened | runner said/did | severity
---+-------------+---------------+-----------------+---------
   |             |               |                 |
   |             |               |                 |

POST-RUN VERIFICATION (untimed, proctor)
PDF opens, family name present:   Y/N
Calendar shows deadline+reminder: Y/N
check_cold_run.py exit 0:         Y/N  (paste FAIL lines if any)

VERDICT: PASS / FAIL (reason): ____________
```
