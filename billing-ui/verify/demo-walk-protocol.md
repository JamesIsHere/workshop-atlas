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

AMENDED 2026-08-06 (pre-walk end-to-end drive, ordered by James):
every step was executed against the LIVE screens by script (not
source reading -- the 08-04 audit's method missed state-dependent
rendering) on a scratch db, checking each Go: target, field, fold
(existence AND open state), button, and Observe: on the page the
click actually lands on. Eight mismatches fixed. Two were product
defects, fixed in app_ui/billing_ui.py (rendering-only): the URL
from "Create client link" reloaded into a COLLAPSED fold, and an
empty bill rendered the import checkboxes bare, so the named fold
"Import saved charges and time" did not exist in that state. Six
were sheet wording re-pinned to what the screens render: the New
invoice forms are stacked, not side by side (steps 10/13); paid
bills show Balance 0.00, so bills are identified by number, never
by amount (steps 25/29); observations moved onto the screens that
actually show them (settlement figures step 18; Vera's 2,000.00
step 23->24); the operating recon card has no client-claims leg
(step 32). Data values and step semantics unchanged; no steps
renumbered.

AMENDED 2026-08-07 second time (post-verdict, ordered by James;
F7-authorized): the reconciliation screen was rebuilt from the
horizontal identity sentence to three vertical footing columns
with a visible bank-statement leg and parenthesized outflows
(James's axis-(a) critique: "the bank rec falls out of our
numbers, there is no bank side I see"). Step 32's Observe re-pinned
to the new screen. No data values or other steps changed.

AMENDED 2026-08-07 (attempt-2 findings, ordered by James at the
in-session gate): his second walk stalled at step 12 and diverged
at step 14; every root cause was an artifact defect, not driving.
(1) The sheet spoke agent vocabulary -- card, fold, the bill's
page -- that no screen displays; the walk sheet now opens with a
plain description of what each word looks like, and says outright
that no button named Collect exists. (2) The sheet had no
recovery rail: a driver who reorients via the menu leaves the
scripted screen with no route back; every step now carries a Go:
or an If lost: route that starts from the top menu or address
bar, never from where the driver happens to stand. (3) Date
fields prefill today's date and the prefill silently beat the
sheet's typed values (attempt 2's payment landed on 2026-08-07);
every dated field now states its prefill and says change it or
leave it. (4) The do-NOT-open instruction on the trust-deposit
fold lost to a visible prefilled one-click affordance (attempt
2's retainer was recorded firm-side before the client link
existed, emptying Part F of anything to settle); Part E is
rewritten positively -- that fold is never named, the part states
that the firm records no payment, and a CHECKPOINT at step 17
stops the walk if the payment method reads direct. (5) Parts now
open with a Goal line so the driver knows what the steps are for
(James: driving the old sheet was like sitting the CPA audit exam
with no background, deriving the goal from first principles each
step). Same day, UI (rendering-only): the top menu now underlines
Billing on every billing screen -- active-section marker;
shared-chrome change ratified by James in-session. Data values
and step semantics unchanged; no steps renumbered.

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
field this sheet does not mention alone. A new client, Vera
Synthetic, has retained the firm for an I-130 petition.

WHAT THE WORDS MEAN. The app does not use these words on screen;
they are this sheet's names for shapes you will see:

- CARD: a white box with a bold title, sitting on the page's
  gray background. A page is a stack of cards.
- FOLD: a blue line of text with a small triangle at its left,
  inside a card. Clicking the line expands a form under it;
  clicking again closes it. If a form this sheet names is not
  visible, its fold is closed -- click the named blue line.
- TAB: one of the short row of links at the top of the invoice
  list (Outstanding, Paid, All); the highlighted one is
  selected, and the list opens on Outstanding.
- TILE: a small box with a big dollar number (balances).
- CRUMB LINE: the small gray line at the top of Billing pages,
  just under the menu, naming the page you are on. Example of
  one: Billing / Bill #1. The Billing front page has no crumb
  line -- its big Billing heading is the marker.
  Feeling lost? Read the crumb line first, then the menu --
  the Billing entry in the top menu stays underlined on every
  Billing screen.

There is no button named Collect anywhere. Collect is the TITLE
of a card that appears on a bill or trust request once money is
owed. The ways of getting paid are folds inside that card.

STOP RULE: do not guess or substitute labels. If a named heading,
button, field, or expected result is missing, stop the walk at
that screen and record the mismatch. The walk has found a product
or instruction defect; James does not debug it.

STEP RULE (ratified mid-walk 2026-08-04, James: "when the user
loads a new page its a new step"): every step is ONE screen. A
step opens by naming the screen, lists what to do there as
"Field" = value lines, and ends with "End:" -- the single click
that leaves the screen -- or an "Observe:" line for look-only
steps. A step that starts on a NEW screen carries a "Go:" route;
a step that continues on the previous screen carries an If lost:
route instead. Both routes always start from the top menu or the
address bar -- never from wherever you happen to be standing --
so any step can be re-entered from scratch at any time. If the
screen you land on does not match the step's name, stop: that is
a defect. Parts group steps by story beat; parts are narration,
steps are the unit you execute.

Part A -- first run (normal window, firm URL)

Goal: create the firm's one user and reach the dashboard. If
lost anywhere in Part A, go to http://127.0.0.1:8500 in the
address bar -- the app resumes where you left off.

1. First-run setup (loads by itself at the firm URL; headed
   "Set up your firm's first account")
   - "Your name" = Demo Driver
   - "Email" = demo.driver@synthetic.test
   - "Password" = demo-walk-pass
   End: click "Create account".
2. Two-factor setup (headed "Set up two-factor authentication")
   End: click "Show me my code". Your code is on the NEXT screen.
3. Enter your code
   - "Type the code above" = the 6-digit code on screen
   End: click "Verify" -> the dashboard.

Part B -- Vera and her matter

Goal: one client (Vera) and one matter (her I-130 case) on file.

4. Dashboard (Go: put http://127.0.0.1:8500 in the address bar
   -- the dashboard is the app's front page)
   End: click "New client".
5. New client -- Vera Synthetic is a PERSON; Synthetic is her
   last name, not a company (If lost: repeat step 4's route and
   click "New client" again)
   - "Given name (first name)" = Vera
   - "Family name (last name)" = Synthetic
   - "Email" = vera.client@synthetic.test
   - "Phone" = +1-555-0400
   End: click "Create client" -> her client page.
6. Vera Synthetic's client page (If lost: menu "Clients" ->
   click Vera Synthetic in the list)
   End: click "New matter for this client".
7. New matter (If lost: repeat step 6's route, then that button
   again)
   - "Matter name" = Vera Synthetic I-130
   - the "Client" box already shows Vera Synthetic -- leave it
   - leave "Description" blank
   End: click "Create matter".

Part C -- the firm's two bank accounts

Goal: one trust (IOLTA) account and one operating account, both
empty. Every dollar in this walk moves between these two.

8. New bank account (Go: menu "Billing" -> button "Trust
   accounting" -> button "New bank account")
   - "Kind" = Trust (IOLTA)
   - "Account name" = SYNTH IOLTA
   End: click "Create account" -> back on Trust accounting.
9. New bank account, second time (Go: from Trust accounting
   click "New bank account" again; If lost: menu "Billing" ->
   "Trust accounting" -> "New bank account")
   - "Kind" = Operating
   - "Account name" = SYNTH Operating
   End: click "Create account".

Part D -- Vera pays 500.00 for today's consultation, directly

Goal: a 500.00 bill, paid by check straight into the operating
account -- the simplest money path, no trust involved.

10. New invoice (Go: menu "Billing" -> button "New invoice").
    Two form cards, one above the other; use the TOP one,
    titled "New bill":
    - "Client" = Vera Synthetic
    - "Matter" = Vera Synthetic I-130
    - "Issue date" = 2026-08-01 (the box starts on today's
      date -- change it)
    End: click "Create bill" -> Bill #1's page; its crumb
    line reads Billing / Bill #1.
11. Bill #1's page, the "Add a charge" form in the Charges card
    (If lost: menu "Billing" -> tab "All" -> the row #1 link in
    the INVOICE column. Use All: a bill with no charges yet is
    on neither the Outstanding nor the Paid tab)
    - "Description" = SYNTH consultation
    - "Amount" = 500.00
    - "Type" = Service
    - "Date" = already shows 2026-08-01, copied from the issue
      date -- leave it
    End: click "Add charge". The page reloads and a new card
    appears, titled Collect $500.00. No money has moved yet.
12. Bill #1's page, the Collect $500.00 card (If lost: menu
    "Billing" -> tab "All" -> the row #1 link; the card sits
    below the Charges card)
    - click the fold line "Record a direct payment (check,
      cash, wire)" to expand it
    - "Amount" = leave at 500.00
    - "Date" = 2026-08-01 (starts on today's date -- change
      it; this date is wrong on purpose, Part I corrects it)
    - "Deposit to" = SYNTH Operating
    End: click "Record payment". The bill's title now carries
    a Paid pill.

Part E -- the 5,000.00 retainer, paid by Vera herself

Goal: the firm ASKS for money; VERA pays online in the
incognito window. The firm types no payment anywhere in this
part -- your hands only create the request, add the charge, and
create the link. The money sits with the simulated card
processor until Part F settles it.

13. New invoice (Go: menu "Billing" -> "New invoice"). This
    time use the LOWER form card, titled "New trust request":
    - "Client" = Vera Synthetic
    - "Deposits to" = SYNTH IOLTA
    - "Hold funds for" = The client
    - leave "Matter" at -- client-level funds --
    - "Issue date" = 2026-08-01 (starts on today -- change it)
    End: click "Create trust request" -> Trust request #2's
    page; its crumb line reads Billing / Trust request #2.
14. Trust request #2's page, the "Add a charge" form in the
    Charges card (If lost: menu "Billing" -> tab "All" -> the
    row #2 link in the INVOICE column)
    - "Description" = SYNTH retainer request
    - "Amount" = 5000.00
    - "Type" = Service
    - "Date" = already shows 2026-08-01 -- leave it
    End: click "Add charge". A card titled Collect $5,000.00
    appears; its fold "Send the request to the client" is
    already open. Do nothing else on this screen -- step 15
    uses that open fold. Remember the Goal: in this part the
    firm records no payment.
15. Trust request #2's page, inside the open fold "Send the
    request to the client" (If lost: menu "Billing" -> tab
    "All" -> the row #2 link -> the Collect card)
    End: click "Create client link". A web address appears
    ending in /invoice/<token> -- copy it, switch to the blank
    incognito window, paste it there and go. (Its address
    differs from the firm URL; that is Vera's own surface,
    expected.)
16. The request as Vera sees it (incognito window)
    - "Synthetic payment token" = SYNTHETIC-VISA-DEMO (exactly,
      no spaces; a demo token, not a card number)
    - "Payment method" = card
    End: click "Pay". The next page must say "Payment
    received." If it says anything else -- Declined, or
    already paid -- STOP and record it.
17. Trust request #2's page, back in the firm window (If lost:
    menu "Billing" -> tab "Paid" -> the row #2 link)
    End: refresh the page.
    Observe: a Paid pill, and the payment line reads card
    (online, simulated processor). CHECKPOINT: if the payment
    line reads direct instead of card, the walk has diverged
    -- STOP here and record it; do not continue to Part F.

Part F -- settlement: gross to trust, fees firm-side

Goal: the processor is holding Vera's 5,000.00. One click moves
real money: the FULL 5,000.00 lands in trust, and the
processor's fee comes out of the firm's operating money --
never out of client funds. This is the point of the build.

18. Trust accounting (Go: menu "Billing" -> "Trust
    accounting"), the "Processor settlement" card at the bottom
    - "Settlement date" = leave as shown
    End: click "Run settlement".
    Observe: the "Trust (IOLTA)" tile now reads $5,000.00 --
    the full retainer, GROSS, untouched -- and the "Operating"
    tile reads $349.70: the processor's 150.30 fee came out of
    the firm's 500.00, never out of client funds.

Part G -- work the case, bill it, pay from trust

Goal: record 2 hours of work and a flat preparation fee, put
both on a new bill, and pay that bill FROM Vera's trust money
-- the earn-out: trust -> operating as fees are earned.

19. Record time (Go: menu "Billing" -> "Time" -> "Record
    time")
    - "Date worked" = 2026-08-02 (starts on today -- change it)
    - "Time spent" = 2h
    - "Hourly rate" = 250.00
    - "Description" = SYNTH case work
    - leave "Client" at -- pick a client or a matter --
    - "Matter" = Vera Synthetic I-130
    End: click "Record time".
20. Saved charges (Go: menu "Billing" -> "Saved charges"), the
    "Save a charge" form
    - "Description" = SYNTH I-130 preparation
    - "Amount" = 2500.00
    - "Type" = Service
    End: click "Save charge".
21. New invoice (Go: menu "Billing" -> "New invoice"), the TOP
    card "New bill" again
    - "Client" = Vera Synthetic
    - "Matter" = Vera Synthetic I-130
    - "Issue date" = 2026-08-02 (starts on today -- change it)
    End: click "Create bill" -> Bill #3's page; its crumb
    line reads Billing / Bill #3.
22. Bill #3's page, the Charges card (If lost: menu "Billing"
    -> tab "All" -> the row #3 link. Use All: a bill with no
    charges yet is on neither default tab)
    - click the fold line "Import saved charges and time"
    - tick BOTH boxes: the 2,500.00 saved charge and the
      2026-08-02 time entry (500.00)
    End: click "Import selected".
    Observe: both rows land in the Charges table and the page
    says Balance due: $3,000.00.
23. Bill #3's page, the Collect $3,000.00 card (If lost: menu
    "Billing" -> tab "All" -> the row #3 link)
    - click the fold line "Pay from client trust (earn-out)"
    - "Amount" = leave at 3,000.00
    - "Date" = 2026-08-03 (starts on today -- change it)
    - "From trust account" = SYNTH IOLTA
    - "Trust funds held for" = The client
    - "Deposit to" = SYNTH Operating
    End: click "Record payment".
    Observe: the bill shows a Paid pill. (Vera's remaining
    trust money appears on the next screen.)

Part H -- disburse her filing fee from trust

Goal: pay USCIS 1,200.00 out of Vera's remaining 2,000.00 in
trust, leaving her 800.00.

24. Disburse funds (Go: menu "Billing" -> "Trust accounting"
    -- pause there: the "Client funds" table shows Vera
    Synthetic 2,000.00, the retainer after the earn-out --
    then click "Disburse funds")
    - "From trust account" = SYNTH IOLTA
    - "Funds held for client" = Vera Synthetic
    - leave "Funds held for matter" at -- no matter --
    - "Amount" = 1200.00
    - "Date" = 2026-08-04 (starts on today -- change it)
    - "Pay to" = SYNTH-USCIS
    - "Memo" = SYNTH I-130 filing fee
    End: click "Disburse". Her remaining funds: 800.00.

Part I -- the correction: fix a wrong date, watch the books

Goal: the consultation payment was dated 2026-08-01 on purpose;
it should be 2026-08-02. Fix it and watch the books repair
themselves by ADDING entries -- never by rewriting history.

25. The invoice list (Go: menu "Billing", then click the tab
    "Paid" -- the list opens on Outstanding, where paid bills
    are NOT). Paid bills all show balance 0.00, so find the
    consultation bill by its number: the row whose INVOICE
    column reads #1.
    End: click that #1 link -> Bill #1's page.
26. Bill #1's page, the Payments table -- the payment's date
    2026-08-01 is a link (If lost: menu "Billing" -> tab
    "Paid" -> the row #1 link)
    End: click the date link -> the payment's own page.
27. The payment's page, the "Correct this payment" card (If
    lost: repeat step 26's route)
    - "Date" = 2026-08-02
    - leave "Amount" and "Apply to charge" as they are
    End: click "Save correction".
28. The payment's page, after the save (you are still on it)
    Observe: in "Journal trail" the original entry stays,
    joined by entries tagged "reverses e<n>" / "replaces
    e<n>"; the "Bank record" card shows the correction as
    compensating events. Nothing is ever silently rewritten.

Part J -- the books, end to end

Goal: see the same money from every side -- the bill's PDF, the
trust ledger, one journal entry, and the reconciliation
identity tying bank to books to client claims.

29. Bill #3's page (Go: menu "Billing" -> tab "Paid" -> the
    row whose INVOICE column reads #3)
    End: click "Download PDF" (top card) and open the file.
30. Trust accounting (Go: menu "Billing" -> "Trust
    accounting")
    End: click "SYNTH IOLTA ledger" on the trust tile.
31. SYNTH IOLTA's ledger page (If lost: repeat step 30's
    route)
    End: click any entry number (e1, e2, ...) -> a single
    journal entry. Observe: debits equal credits.
32. Reconciliation (Go: menu "Billing" -> "Reconciliation")
    Observe: each account's card carries the HOLDS badge and
    THREE side-by-side columns that each foot like a working
    paper: Bank statement (cleared lines, then in-transit and
    outstanding items, footing to Adjusted bank), Books (the
    ledger entries footing to Books balance), and -- on the
    SYNTH IOLTA card only -- Client claims (whose money the
    trust holds). Outflows are in parentheses. The tie line
    under the columns reads adjusted bank = books, and adds
    = client claims on the trust card; the operating card has
    no client-claims column because it holds no client funds.
    System-made correction entries are labeled (system
    correction).

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
