# demo-walk-protocol.md -- verifier 2 (RATIFIED)

Status: RATIFIED by James 2026-08-04 at gate 0, as amended through
the remote red-pen rounds (agent-executed mechanics; ordering rule
-- the agent's run always precedes James's hands; step 10 correction
beat live after the F7 fix). This document binds verifier 2 as
written; edits now require a gate.

AMENDED mid-walk 2026-08-04, ordered by James (ratifier): every
step now names WHERE in the app it happens (menu path, on-page
action). Outcome-only directions were a drafting defect -- this
sheet is a demo script, not a discoverability test (that bar is
casework-ui's cold run). No data values or step semantics changed.

AMENDED a third time 2026-08-04 (STEP RULE, ordered by James):
steps re-based from story beats to SCREENS -- one step per
screen, "Field" = value lines, one "End:" click or an "Observe:"
per step; 12 narrative steps became 32 atomic steps in parts
A-J. Values are now always pinned to their field labels (the
slash-tuple form is a verifier FAIL). Data values and semantics
unchanged throughout.

AMENDED 2026-08-04 (pre-resume label audit, ordered by
James): every quoted heading, button, field, and option label was
checked against the rendering source (app_ui/billing_ui.py and the
client surface in casework/app/server.py). Five defects fixed:
step 4a/5a invented a "choose Bill / Trust Request" control (the
New invoice page is two side-by-side cards); "Issued date" is
rendered "Issue date"; step 6's card is titled "Processor
settlement" (its button is "Run settlement"); step 10's control is
"Save correction" inside "Correct this payment", not "Edit", and
paid bills live under the invoice list's "Paid" tab; step 5d named
the wrong page. Steps 7-12 brought to the same grain as 4-5.

Contract hooks (goal.md): James drives the full billing lifecycle
entirely through screens on a FRESH database -- no terminal, no
SQL, no dev tools mid-walk. The fiduciary suite must run green
against the walked database afterward. PASS additionally requires
all three sub-verdicts (bottom of this file). James driving is the
point, not a compromise: this verifier measures demo-readiness,
not cold interaction cost (that bar belongs to casework-ui's own
protocol, untouched).

## Roles

- DRIVER: James. Screens only. The 20:00 budget is SOFT -- blowing
  it triggers friction-log entries, never a FAIL by itself.
- RECORDER: the agent (or James solo with screen recording). Preps
  setup, records marks and friction, runs the untimed close-out
  checks. During the walk the recorder answers NOTHING about the
  screens; wording questions about this sheet may be clarified.

## Setup (RULED 2026-08-04: the agent EXECUTES every mechanical
## step -- nothing here is typed by James)

1. The agent starts the server in the session (background), on a
   fresh data/demo-walk-<today>.db, and confirms /setup answers
   before handing over. James receives exactly two things: the
   firm URL (http://127.0.0.1:8500) and this sheet. Zero terminal
   contact for the driver. (`atlas-ui` exists for James's own solo
   use outside sessions; it is not part of walk-day protocol.
   Gate reviews: agent starts `--seeded` the same way.)
2. Two browser windows: normal at the firm URL, incognito OPEN
   BUT BLANK (client pay leg; separate cookie jar).
3. This sheet printed or displayed. Stopwatch ready. Recording
   form (bottom) blank. Agent runs the mechanical walk verifier
   BEFORE handing over and quotes it GREEN -- a walk never starts
   on screens the oracle has not just passed.

## Walk sheet (driver reads top to bottom; data values inline)

All data is synthetic: type the values shown EXACTLY. Leave any
field this sheet does not mention blank. A new client, Vera
Synthetic, has retained the firm for an I-130 petition.

STOP RULE: do not guess or substitute labels. If a named heading,
button, field, or expected result is missing, stop the walk at that
screen and record the mismatch. The walk has found a product or
instruction defect; James does not debug it.

STEP RULE (ratified mid-walk 2026-08-04, James: "when the user
loads a new page its a new step"): every step is ONE screen. A
step opens by naming the screen (and the menu path to reach it,
as a "Go:" line, when it is not where the last step left you),
lists what to do there as "Field" = value lines, and ends with
"End:" -- the single click that leaves the screen -- or an
"Observe:" line for look-only steps. If the screen you land on
does not match the next step's name, stop: that is a defect.
Parts group steps by story beat; parts are narration, steps are
the unit you execute.

Part A -- first run (normal window, firm URL)

1. First-run setup (loads by itself at the firm URL)
   - "Your name" = Demo Driver
   - "Email" = demo.driver@synthetic.test
   - "Password" = demo-walk-pass
   End: click "Create account".
2. Two-factor setup
   End: click "Show me my code". A 6-digit code appears.
3. Enter your code
   - "Type the code above" = the 6-digit code on screen
   End: click "Verify" -> the dashboard.

Part B -- Vera and her matter

4. Dashboard
   End: click "New client".
5. New client -- Vera Synthetic is a PERSON; Synthetic is her
   last name, not a company
   - "Given name (first name)" = Vera
   - "Family name (last name)" = Synthetic
   - "Email" = vera.client@synthetic.test
   - "Phone" = +1-555-0400
   End: click "Create client" -> her client page.
6. Vera Synthetic's client page
   End: click "New matter for this client".
7. New matter
   - "Matter name" = Vera Synthetic I-130
   - leave "Description" blank
   End: click "Create matter".

Part C -- the firm's two bank accounts

8. New bank account (Go: menu "Billing" -> "Trust accounting"
   -> "New bank account")
   - "Kind" = Trust (IOLTA)
   - "Account name" = SYNTH IOLTA
   End: click "Create account" -> back on Trust accounting.
9. New bank account, second time (Go: "New bank account")
   - "Kind" = Operating
   - "Account name" = SYNTH Operating
   End: click "Create account".

Part D -- Vera pays 500.00 for today's consultation, directly

10. New invoice (Go: menu "Billing" -> "New invoice"). Two
    forms sit side by side; use the LEFT one, "New bill":
    - "Client" = Vera Synthetic
    - "Matter" = Vera Synthetic I-130
    - "Issue date" = 2026-08-01
    End: click "Create bill" -> the bill's page (titled Bill #1).
11. The bill's page, "Add a charge" form (in the Charges card --
    the only card besides the header while the bill is empty)
    - "Description" = SYNTH consultation
    - "Amount" = 500.00
    - "Type" = Service
    - "Date" = 2026-08-01
    End: click "Add charge". The page reloads -- a "Collect" card
    appears, titled with the amount due. No payment recorded yet.
12. The bill's page, "Collect" card (titled Collect $500.00)
    - open the fold "Record a direct payment (check, cash, wire)"
    - "Amount" = leave at 500.00
    - "Date" = 2026-08-01
    - "Deposit to" = SYNTH Operating
    End: click "Record payment". The bill now shows Paid.

Part E -- the 5,000.00 retainer, paid by Vera through her link

13. New invoice (Go: menu "Billing" -> "New invoice"). This
    time use the RIGHT form, "New trust request":
    - "Client" = Vera Synthetic
    - "Deposits to" = SYNTH IOLTA
    - "Hold funds for" = The client
    - leave "Matter" at -- client-level funds --
    - "Issue date" = 2026-08-01
    End: click "Create trust request" -> the request's page
    (titled Trust request #2).
14. The request's page, "Add a charge" form (in the Charges card)
    - "Description" = SYNTH retainer request
    - "Amount" = 5000.00
    - "Type" = Service
    - "Date" = 2026-08-01
    End: click "Add charge". A "Collect" card appears; do NOT
    open its "Record the deposit" fold -- Vera pays online.
15. The request's page, "Collect" card -- the fold "Send the
    request to the client" is already open
    End: click "Create client link". A URL appears ending in
    /invoice/<token> -- copy it into the blank incognito
    window. (Its address differs from the firm URL; that is
    the client's own surface, expected.)
16. The request as Vera sees it (incognito window)
    - "Synthetic payment token" = SYNTHETIC-VISA-DEMO (exactly,
      no spaces; a demo token, not a card number)
    - "Payment method" = card
    End: click "Pay". The next page must say "Payment
    received." -- if it says "Declined", stop and record it.
17. The request's page, back in the firm window
    End: refresh the page. Observe: Paid, method card (online,
    simulated processor).

Part F -- settlement: gross to trust, fees firm-side

18. Trust accounting (Go: menu "Billing" -> "Trust
    accounting"), "Processor settlement" card at the bottom
    - leave "Settlement date" as shown
    End: click "Run settlement". Observe: trust now holds
    5,000.00 GROSS -- the full retainer, untouched -- and the
    processor's 150.30 fee came out of operating. (This is the
    wedge: gross to trust, fees firm-side, structurally.)

Part G -- work the case, bill it, pay from trust

19. Record time (Go: menu "Billing" -> "Time" -> "Record
    time")
    - "Date worked" = 2026-08-02
    - "Time spent" = 2h
    - "Hourly rate" = 250.00
    - "Description" = SYNTH case work
    - leave "Client" at -- pick a client or a matter --
    - "Matter" = Vera Synthetic I-130
    End: click "Record time".
20. Saved charges (Go: menu "Billing" -> "Saved charges"),
    "Save a charge" form
    - "Description" = SYNTH I-130 preparation
    - "Amount" = 2500.00
    - "Type" = Service
    End: click "Save charge".
21. New invoice (Go: menu "Billing" -> "New invoice"), the
    "New bill" form again
    - "Client" = Vera Synthetic
    - "Matter" = Vera Synthetic I-130
    - "Issue date" = 2026-08-02
    End: click "Create bill" -> the bill's page (titled Bill #3).
22. The bill's page, Charges card
    - open the fold "Import saved charges and time"
    - tick BOTH boxes: the saved charge and the 2026-08-02
      time entry
    End: click "Import selected". Observe: the Charges table
    now totals 3,000.00.
23. The bill's page, "Collect" card (titled Collect $3,000.00)
    - open the fold "Pay from client trust (earn-out)"
    - "Amount" = leave at 3,000.00
    - "Date" = 2026-08-03
    - "From trust account" = SYNTH IOLTA
    - "Trust funds held for" = The client
    - "Deposit to" = SYNTH Operating
    End: click "Record payment". Observe: the bill shows Paid;
    Vera's remaining trust funds: 2,000.00.

Part H -- disburse her filing fee from trust

24. Disburse funds (Go: menu "Billing" -> "Trust accounting"
    -> "Disburse funds")
    - "From trust account" = SYNTH IOLTA
    - "Funds held for client" = Vera Synthetic
    - leave "Funds held for matter" at -- no matter --
    - "Amount" = 1200.00
    - "Date" = 2026-08-04
    - "Pay to" = SYNTH-USCIS
    - "Memo" = SYNTH I-130 filing fee
    End: click "Disburse". Her remaining funds: 800.00.

Part I -- the correction: fix a wrong date, watch the books
(the consultation payment carries the wrong date; it should be
2026-08-02)

25. Billing invoice list (Go: menu "Billing"). It opens on the
    "Outstanding" tab -- paid bills are NOT there.
    End: click the "Paid" tab, then open the 500.00
    consultation bill.
26. The consultation bill, Payments table -- the payment's
    DATE (2026-08-01) is the link
    End: click the date -> the payment's detail page.
27. Payment detail, "Correct this payment" card
    - "Date" = 2026-08-02
    - leave "Amount" and "Apply to charge" as they are
    End: click "Save correction".
28. Payment detail, after the save
    Observe: in "Journal trail" the original entry stays,
    joined by entries tagged "reverses e<n>" / "replaces
    e<n>"; the "Bank record" card shows the correction as
    compensating events. Nothing is ever silently rewritten.

Part J -- the books, end to end

29. The 3,000.00 bill (Go: menu "Billing" -> "Paid" tab ->
    open it)
    End: click "Download PDF" (top card) and open the file.
30. Trust accounting (Go: menu "Billing" -> "Trust
    accounting")
    End: click "SYNTH IOLTA ledger" on the trust tile.
31. SYNTH IOLTA's ledger
    End: click any entry number (e<n>) -> a single journal
    entry. Observe: debits equal credits.
32. Reconciliation (Go: menu "Billing" -> "Reconciliation")
    Observe: each account's card carries the HOLDS badge, with
    the identity spelled out (bank + in transit - outstanding
    = books = client claims).

Say "done" out loud.

## Timing marks (recorder; budget is SOFT, M1 -> M6)

| Mark | Moment                                              |
| ---- | --------------------------------------------------- |
| M0   | Firm window loads its first screen                  |
| M1   | Dashboard first reached (end of step 3)             |
| M2   | Retainer paid by client (step 16)                   |
| M3   | Settlement run (step 18)                            |
| M4   | Earn-out bill paid (step 23)                        |
| M5   | Correction trail seen (step 28)                     |
| M6   | Recon holds, both accounts (step 32, "done")        |

## Close-out (untimed; the AGENT runs 1, quoting output -- James
## only looks and rules)

1. Agent runs `check_demo_walk.py` against the walked db in the
   session and quotes the output: story receipts (accounts, paid
   invoices, settlement, earn-out, disbursement, correction
   trail) plus the fiduciary suite in place. Exit 0 required.
2. James eyeballs: the PDF opens and carries the charges; the
   ledger shows 800.00 client funds; recon says holds.
3. Verdict sheet below, James, all three up/down.

## Verdict sheet (goal.md, ruled 2026-08-04 -- ALL required)

```
WALK ------------------------------------------------------------
Date (UTC):            ____________
Db file:               data/demo-walk-________.db  (fresh: Y/N)
Marks M0..M6:          ____________________________________
Elapsed M1->M6:        ____________  (soft budget 20:00)
Dev-tools touched mid-walk (voids): Y/N

FRICTION LOG (demo-readiness data)
 # | screen/step | what happened | severity
---+-------------+---------------+---------
   |             |               |

CLOSE-OUT
check_demo_walk.py exit 0:        Y/N
PDF + ledger + recon eyeball:     Y/N

SUB-VERDICTS (James, each up/down; ALL required for PASS)
(a) FIDUCIARY STORY LANDS -- ledger, correction trail, and
    reconciliation make the CPA-grade case visibly:     PASS/FAIL
(b) NOTHING EMBARRASSING -- no screen I would apologize
    for mid-demo:                                       PASS/FAIL
(c) BOOKABLE -- I would book the firm meeting on this
    build:                                              PASS/FAIL

VERDICT: PASS / FAIL (failed axis + reason): ____________
```
