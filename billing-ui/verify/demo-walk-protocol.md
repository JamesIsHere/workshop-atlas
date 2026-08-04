# demo-walk-protocol.md -- verifier 2 (RATIFIED)

Status: RATIFIED by James 2026-08-04 at gate 0, as amended through
the remote red-pen rounds (agent-executed mechanics; ordering rule
-- the agent's run always precedes James's hands; step 10 correction
beat live after the F7 fix). This document binds verifier 2 as
written; edits now require a gate.

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

1. Set up the firm's first account (name Demo Driver, email
   demo.driver@synthetic.test, password demo-walk-pass). The
   6-digit code is displayed on screen.
2. Put Vera in the system as a client (Vera / Synthetic /
   vera.client@synthetic.test / +1-555-0400) and open a matter:
   "Vera Synthetic I-130".
3. Set up the firm's two bank accounts: a trust account
   "SYNTH IOLTA" and an operating account "SYNTH Operating".
4. Vera pays 500.00 for today's consultation directly: bill her
   500.00 ("SYNTH consultation", dated 2026-08-01) and record her
   direct payment into the operating account. The bill should
   show paid.
5. Request a 5,000.00 retainer into trust ("SYNTH retainer
   request", client-level, into SYNTH IOLTA, dated 2026-08-01)
   and share it with her. Open the client link in the incognito
   window and pay AS VERA by card -- card number
   SYNTHETIC-VISA-DEMO. Back in the firm window, her trust
   request should show paid.
6. Run settlement. The trust account should now hold 5,000.00
   GROSS -- the full retainer, untouched -- with the processor's
   150.30 fee taken from operating. (This is the wedge: gross to
   trust, fees firm-side, structurally.)
7. Record 2 hours of case work on Vera's matter at 250.00/hour,
   dated 2026-08-02 ("SYNTH case work").
8. Bill the case: create a saved charge "SYNTH I-130 preparation"
   at 2,500.00, open a new bill on Vera's matter (dated
   2026-08-02), and pull in BOTH the saved charge and the 2 hours
   -- total 3,000.00. Pay it by transfer from her trust funds
   (earn-out, dated 2026-08-03). Her remaining trust funds:
   2,000.00.
9. Disburse 1,200.00 from trust to SYNTH-USCIS for her filing
   fee, dated 2026-08-04, memo "SYNTH I-130 filing fee". Her
   remaining funds: 800.00.
10. The consultation payment was recorded with the wrong date:
    change it to 2026-08-02. Watch what the ledger does -- the
    original entry stays, a reversing entry and a corrected one
    appear, and the bank record shows the correction too. Nothing
    is ever silently rewritten.
    (P0 finding 1 was fixed under program ruling 2026-08-04 --
    corrections now keep three-way reconciliation whole; worklog
    s2. This step is fully walkable.)
11. Download the 3,000.00 invoice as a PDF and open it.
12. Walk the books: open the trust ledger, drill into Vera's
    funds down to a single journal entry, and open the
    reconciliation screen. It should say the identity holds for
    both accounts.

Say "done" out loud.

## Timing marks (recorder; budget is SOFT, M1 -> M6)

| Mark | Moment                                              |
| ---- | --------------------------------------------------- |
| M0   | Firm window loads its first screen                  |
| M1   | Dashboard first reached (ceremony done)             |
| M2   | Retainer paid by client (incognito leg done)        |
| M3   | Settlement run (gross in trust visible)             |
| M4   | Earn-out bill paid (trust at 2,000.00)              |
| M5   | Correction trail seen (step 10)                     |
| M6   | Recon screen open, identity holds ("done")          |

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
