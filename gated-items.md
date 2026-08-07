# gated-items.md -- the aggregated backlog of locked and parked items

Created 2026-08-07 at James's order (billing-ui P4 attempt 3,
verdict FAIL a/b/c): one list of everything we are dragging --
what it is, where it is locked, and what unlocking takes. This
file records STATE, not rulings; rulings stay in atlas/CLAUDE.md
and child contracts. Any child session may update it, dated.

## The break-in method (James, 2026-08-07: "a special edit")

Precedent: the F7 amendment (program ruling 2026-08-04), used
once, worked. To fix a locked file NOW instead of dragging it:

1. Name the item from this list; James authorizes in-session,
   scope-limited to named files and named semantics.
2. Hard limits restated in the authorization: existing suites
   immutable, checks may STRENGTHEN never weaken, contracts
   (goal.md) never edited by agents.
3. After the fix: ALL standing suites rerun green and quoted;
   supersessions recorded via canonical sha scripts only; the
   child worklog carries the incident; this file updates.

## Locked items (need a break-in or a gate)

1. RECONCILIATION adequacy/correctness -- James's axis-(a) FAIL
   2026-08-07: "not adequate and I think incorrect."
   Lives: casework-billing/verify/reconcile.py +
   bank_statement.py; rendering casework-ui/app_ui/billing_ui.py.
   Lock status: ALREADY AUTHORIZED by the F7 amendment
   (2026-08-04) for statement/recon model work from billing-ui
   sessions. 2026-08-07 PROGRESS: his specifics landed (no bank
   side visible, horizontal, unsigned amounts); screen REBUILT as
   three vertical footing panes with the statement leg, quoted
   green, pending his eyeball. STILL OPEN under this item: (i)
   correction machinery fabricates compensating bank events --
   keep, or move to real-bank matching in the engine (his held
   decision); (ii) demo period-end placement so the statement
   shows a cleared/pending mix, never empty.
2. CLIENT-FACING PAY PAGE is bare unstyled HTML beside the
   styled firm surface (attempt-3 snaps).
   Lives: casework/app/server.py -- frozen core.
   Unlock: program-ruling amendment (rendering-only scope is
   draftable; spine tests immutable).
3. EMPTY INVOICE derives status paid and appears on NEITHER
   default list tab (invisible until charged; drive finding 6).
   Lives: status logic casework core (frozen); a rendering-side
   list-filter fix is possible in billing_ui.py (unlocked).
   Unlock: James picks the layer; rendering-side needs no
   break-in.
4. NO ROUTE TO DASHBOARD -- brand word is not a link, no menu
   entry (attempt-3 snap; the drive hit the same wall).
   Lives: casework-ui/app_ui/html.py shared chrome.
   Unlock: small gate; the 2026-08-07 nav-marker ratification is
   the precedent (additive, inert elsewhere).
5. DEMO-LOGIN PREFILL + no-expiry sessions on synthetic dbs
   (kills the login-memory wall for parked demos; queued s4).
   Lives: casework-ui login screen.
   Unlock: gate decision, still queued, still not blocking.
6. CLIENT INTAKE QUESTIONNAIRE loses unsaved fields, no
   re-render, submit verifies nothing (parked s3, program-level).
   Lives: casework-ui intake screens (own child, ON HOLD).
   Unlock: route to a child + gate; not billing-ui scope.
7. CASEWORK-UI COLD RUN -- ON HOLD at the recruiting gate.
   Not a defect; listed so the drag-list is complete. Unlock:
   James finds a cold runner.
8. TRIAL-ACCOUNT PASS for SOURCE-GAP corpus entries -- standing
   program ruling: separate, deliberate, supervised decision.
   Listed for completeness; no one proposes it unprompted.
9. PAYMENTS/RAKE strategic flag -- deliberately untriggered
   (business decision, not code). Research banked s5 cont.

## Unlocked build queue (billing-ui's own surface, no gate needed)

A. DATE COUPLING (James ruled 2026-08-07): user-facing dates
   render MM/DD/YYYY on billing screens AND in the walk sheet's
   typed values; data stays ISO; drive_sheet asserts the claim.
   Root cause of 4 of attempt 3's 5 date misses (US-locale date
   inputs vs ISO sheet values).
B. SHEET RE-PIN BY TYPE: identify the trust request by its TYPE
   column and created bills relatively, never by absolute
   number (attempt-3 finding: any extra invoice shifts all
   downstream numbers).
C. Imported saved charge shows a blank DATE cell on the bill.
D. Time spent rejects bare "2" (widen acceptance, keep the
   good error).
E. Blank select options read as noise: "-- pick a client or a
   matter --", "-- no matter --" -> plain guidance wording.
F. Pay to: free text; consider known-payee dropdown + free
   entry.
G. Client link: select-on-click box (zero-JS stand-in for his
   requested copy button).
H. Show the client's remaining trust balance on the bill page
   and PDF (his 800.00 suggestion; strong fiduciary storytelling).
I. Clarify two snap labels with James (one line each, later):
   "difference in paid versus recorded no update to status";
   "Collect card already exists at bottom do not need to add
   charge".
