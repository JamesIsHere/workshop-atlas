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
   green, pending his eyeball.
   RULED 2026-08-07 s8 close (James: "we need to do the engine
   work"): sub-decision (i) goes to REAL-BANK MATCHING --
   corrections touch books only, the bank record keeps what the
   bank saw, the recon engine matches and explains differences
   as reconciling items; the mirror-event shortcut dies;
   fiduciary F7 scenarios strengthen to the real model.
   Sub-decision (ii), demo period-end placement, is now plain
   build work riding the same job. NEXT SESSION'S TASK -- the
   last work item before attempt 4. Worklog s8 close has the
   full scope note.
   BUILT 2026-08-07 s9: mirror events dead (corrections/refunds
   books-only, witness_bank=False reposts); recon engine matches
   for real (linkage -> exact -> pending timing -> payment-family
   deltas, every item caused + directed); F7 strengthened (bank-
   record purity, timing resolves all-cleared, closed causes);
   period-end placed (disbursement rides today, so step 32 shows
   cleared + in-transit deposit + outstanding check, stable on
   any run date). All suites green, quoted in billing-ui worklog
   s9; fiduciary sha e6c64593 supersedes fb5bccda. Item CLOSED
   pending only attempt 4's walk verdict.
2. CLIENT-FACING PAY PAGE is bare unstyled HTML beside the
   styled firm surface (attempt-3 snaps).
   Lives: casework/app/server.py -- frozen core.
   Unlock: program-ruling amendment (rendering-only scope is
   draftable; spine tests immutable).
   ADDED 2026-08-07 s7 (same frozen-core rendering class): the
   invoice PDF (casework/app/billing.py) prints ISO dates while
   the screens now render MM/DD/YYYY (item A residue) -- fold
   into this break-in if drafted.
   PDF PART DONE 2026-08-07 s7 cont, by James-authorized
   break-in (recorded in billing-ui worklog): invoice_pdf now
   renders MM/DD/YYYY dates and a footed Description | Date |
   Amount column table, integer-cents formatting (the /100
   float division is gone). All suites green; billing-ui walk
   sha superseded a506f085 -> de589cbd. The PAY PAGE styling
   itself remains locked -- unlock unchanged.
   UNLOCKED 2026-08-07: the client-pay-page amendment was
   ratified by James (program ruling 2026-08-07, atlas/
   CLAUDE.md) -- rendering-only scope over server.py's client
   surface; work proceeds in billing-ui. The client PORTAL
   remains locked as item 11.
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
   CLOSED 2026-08-08 s10 riding the item-12 home-page build
   (authorized by ruling R2): nav gains a Dashboard entry
   (first position) and the brand word links home for authed
   users. All suites green, quoted in billing-ui worklog s10.
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
10. INVOICE DISPLAY CODES B0001/T0001 -- design RATIFIED in
    conversation 2026-08-07 (James + agent), full record in
    billing-ui/invoice-codes.md: type letter + 4-digit
    zero-padded per-type series, scope follows the active
    numbering mode, stored at creation, immutable; no client,
    date, or separator in the code; internal id is the join
    key. Lives: casework/app (schema column + counter,
    gen_schema.py) + rendering + PDF -- frozen core.
    BUILT + CLOSED 2026-08-07 s8, James's authorization ("Yes,
    please add codes" after his snap showed no code anywhere):
    schema columns display_code/code_scope (gen_schema regen),
    _next_code in the creation path, codes rendered as the
    invoice identity on list/titles/crumbs/PDF/client page/
    emails/CSV/zip names; stored number kept as a Number
    attribute row on the invoice page. Sheet superseded
    type+date routing with codes (sixth amendment; lock
    re-synced 73240eb76cc7); drive locates by code, exact-code
    crumb pins, stray regression retained. Walked 07c db
    migrated (verify/migrate_invoice_codes.py -- the reusable
    migration story; other retained walk dbs stay pre-code,
    migrate on demand before serving). All suites green,
    worklog s8 cont 2 quotes them.

11. CLIENT PORTAL (client-scoped surface) -- James's client-view
    brainstorm 2026-08-07: everything-I-paid history linked to
    bills, full-bill browsing/search, CSV export (opens in
    Excel), outstanding-bills view with due dates, trust
    STATEMENT (deposits, applications to bills, refunds,
    running balance -- the CPA-grade client artifact, stronger
    than the balance line item H shipped), retainer
    replenishment (pay INTO trust; new fiduciary logic).
    Blocked on an access model: today a client exists only
    per-invoice via share tokens (casework/app/server.py); a
    portal needs durable client-scoped access -- new
    access-control logic in the frozen core, arguably its own
    child. The narrow pay-page amendment (item 2) deliberately
    excludes all of this (James 2026-08-07: "go narrow now,
    come back when it becomes an issue").
    Unlock: gate; likely its own contract.

12. STATUS/FLOW SURFACE -- attempt-4 verdict driver (2026-08-08,
    FAIL b/c with (a) PASS; billing-ui worklog s10). No overall
    status page and no visible flow: James wants a summary layer
    (project/client summary, matter summary, billing summary "or
    a flow") and hidden state brought forward so the user can
    follow the order (add client -> matter -> bill -> which type
    / which account -> collect vs disburse). His framing: "The
    UI does not bring out the structure of the actual code in a
    way that the user can logically follow and reinforce a
    narrative." Information-architecture class, not polish --
    adjacent to but much bigger than item 4 (no route to
    dashboard).
    Lives: casework-ui/app_ui shared chrome + new summary
    screens; existing casework-ui screens/walk steps are gate
    territory per the in-place-extension ruling.
    Unlock: DESIGN GATE with James before any build -- what the
    surface is comes first, which child builds it second.
    DESIGN GATE OPENED 2026-08-08 s10 (live; rulings recorded
    in billing-ui worklog s10 cont as they land). Ruling 1:
    recon is a standing condition; humans own exceptions +
    period close only. Ruling 2: the status page IS the home
    screen at "/" (James's gate decision under the in-place
    amendment's carve-out; existing-screen edits authorized,
    scope + hard limits in the worklog). Item 4 rides this
    work and dies with it.
    HOME-PAGE DESIGN RATIFIED 2026-08-08 s10: seven rulings
    sealed in billing-ui/status-page.md (sheet signed). Build
    authorized under ruling 2's scope. Still open within item
    12: flow markers on object screens (object 2), the client/
    matter summary layer (object 3), the period-close act, and
    the attempt-5 finish pass.
    HOME PAGE BUILT 2026-08-08 s10 (same session): dashboard_
    screen per the ratified sheet; billing-ui walk grew a
    home-status step (18 steps); ALL suites green, sha
    28a19170 supersedes 301b574d; record in billing-ui worklog
    s10. Pending James's eyeball on the live page.
    EYEBALL LANDED + OBJECTS 2 AND 3 BUILT 2026-08-09 s11:
    home page eyeballed (audience RULED: finance seat; CEO
    consumes narrated). Flow markers built wide (dollars-in-
    buckets vocabulary Unbilled/Outstanding/Settling/Clearing,
    signed; dashboard pipeline dollar line amends R5; invoice
    splits; row chips; matter unbilled line). Client summary
    built (Money band on the contact page, placement A signed;
    footed payments drill at /billing/clients/<id>/payments --
    James's live catch). Build-order ruling: audience tags now,
    role enforcement is a future contract; SoD asked per
    write-flow at design time. Walk is 19 steps; ALL suites
    green; sha chain ...28a19170 -> e6ae695b -> 5ba384cc ->
    c59b8e9d. Record: billing-ui worklog s11. STILL OPEN in
    item 12: period-close act (carries the maker-checker
    question + deferred firm-wide rankings), then the
    attempt-5 finish pass.

## Unlocked build queue (billing-ui's own surface, no gate needed)

A. DATE COUPLING (James ruled 2026-08-07): user-facing dates
   render MM/DD/YYYY on billing screens AND in the walk sheet's
   typed values; data stays ISO; drive_sheet asserts the claim.
   Root cause of 4 of attempt 3's 5 date misses (US-locale date
   inputs vs ISO sheet values).
   DONE 2026-08-07 s7: fmt_date() at all 17 render sites; sheet
   re-expressed MM/DD/YYYY (lock re-synced 847e4aaf2364);
   drive_sheet scans sheet AND every fetched billing page for
   ISO strays. All suites green, quoted in the worklog.
   RESIDUE -> item 2's class: the invoice PDF (frozen core)
   still prints ISO dates; James rules whether it rides the
   pay-page break-in.
B. SHEET RE-PIN BY TYPE: identify the trust request by its TYPE
   column and created bills relatively, never by absolute
   number (attempt-3 finding: any extra invoice shifts all
   downstream numbers).
   DONE 2026-08-07 s7: sheet identifies every invoice by TYPE +
   issue date (preamble rule, steps 10-29 re-worded, crumbs pin
   the prefix only); drive_sheet locates rows the sheet's way,
   cross-checks against created ids, and permanently injects a
   stray invoice after step 21 as the attempt-3 regression --
   24/24 GREEN through it. Sheet lock re-synced efea8538b68e.
   Product-level cure designed and gated: see locked item 10.
C. Imported saved charge shows a blank DATE cell on the bill.
   DONE 2026-08-07 s7: the UI import handler dates each
   imported saved charge with the bill's issue date via the
   existing core update_charge API (zero core change; same
   default the manual Add form prefills). drive_sheet asserts
   the dated row; report_sha superseded d9074178 (PDF grew
   with the date cell). Judgment call flagged in the worklog.
D. Time spent rejects bare "2" (widen acceptance, keep the
   good error).
   DONE 2026-08-07 s7: UI-side normalization (bare number ->
   hours) before the corpus-pinned core parser, cents_of-style;
   hint updated; walk verifier posts a bare "2" and asserts the
   200.00 entry. report_sha superseded c4555b15.
E. Blank select options read as noise: "-- pick a client or a
   matter --", "-- no matter --" -> plain guidance wording.
   DONE 2026-08-07 s7: all seven blank options re-worded to
   state what leaving the field means; sheet + driver
   re-pinned, lock re-synced 39f124b41e01. Wording is agent
   judgment, flagged for James's re-rule.
F. Pay to: free text; consider known-payee dropdown + free
   entry.
   DONE 2026-08-07 s7: native datalist of prior counterparties
   on the disburse form; free entry stays; zero JS.
G. Client link: select-on-click box (zero-JS stand-in for his
   requested copy button).
   DONE 2026-08-07 s7: readonly copylink input (click, Ctrl+A,
   Ctrl+C); sheet step 15 teaches it; lock re-synced
   2c9cac5141af; drive asserts the box.
H. Show the client's remaining trust balance on the bill page
   and PDF (his 800.00 suggestion; strong fiduciary storytelling).
   DONE 2026-08-07 s7: kv line on the invoice page + PDF line
   (item-H break-in, both languages), shown only when the
   client holds trust funds; walk asserts 800.00 in the PDF
   text; report_sha superseded f3f16120. Incident logged: a
   guessed column name broke two suites loudly before the
   ground-read fix (worklog s7 cont 9).
I. Clarify two snap labels with James (one line each, later):
   "difference in paid versus recorded no update to status";
   "Collect card already exists at bottom do not need to add
   charge".
   CLOSED 2026-08-07 s7, James ruling on both: label 1 was a
   double-check note, not a problem; label 2 was the sheet's
   number-pinned route (row #2) landing him on the wrong
   invoice after his +1 offset -- the exact defect item B's
   type+date routing killed and the stray-invoice regression
   now tests. No further action.
   >> UNLOCKED QUEUE A-I: ALL CLOSED 2026-08-07. <<
