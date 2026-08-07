# invoice-codes.md -- gate artifact: invoice display codes

Status: DESIGN RATIFIED in conversation, James + agent,
2026-08-07 (billing-ui s7). BUILD AUTHORIZED AND LANDED
2026-08-07 s8 (James: "Yes, please add codes"): schema columns
display_code + code_scope, _next_code in the creation path,
rendered as the invoice identity everywhere a human reads one;
walked dbs migrate via billing-ui/verify/migrate_invoice_codes
.py. Gated item 10 is closed; build record in billing-ui
worklog s8 cont 2. The design below is as ratified -- the
build followed it without deviation.

## The scheme

Every invoice carries a display code assigned at creation:

    B0001   bill, first in its series
    T0001   trust request, first in its series

- One alpha type character: B = bill, T = trust request.
  Audibly distinct spoken across a desk; type is the one fact a
  reader needs before the number means anything (a trust
  request is not income).
- Four-digit zero-padded sequence, one independent series per
  type (check-series model: each series runs gapless, so a
  per-series sequential-completeness check is trivial, and an
  extra bill can never shift a trust request's identity).
- Series scope FOLLOWS the active numbering mode of the
  corpus-pinned stored number (global-invoice-numbering,
  confirmed tier): per client by default, firm-wide when Global
  Invoice Numbering is on. Mode flips never renumber anything;
  new codes continue from the per-type totals of the new scope
  (mirror of fx-0076's no-renumber rule).
- No separator. Alphanumeric only: survives every parser
  context (unquoted SQL/Excel where B-0001 can silently parse
  as B minus 1), double-click selects the whole token, and the
  leading zeros make it invalid as an Excel cell reference
  (B0001 errors loudly; unpadded B1 would silently read cell
  B1). Alpha-first keeps every tool treating it as text -- no
  auto-cast eating the zeros.
- Assigned at creation, STORED, immutable. Never derived at
  render time: a derived ordinal is renumbering-in-waiting, and
  identifiers printed on financial documents must survive
  everything (the same principle the append-only ledger
  enforces).

## What is deliberately NOT in the code

- Client: the stored number's default scope already makes the
  client implicit; identity is the pair (client, code). Client
  initials collide; client renders beside the code on every
  list and page. Attribute, not identity.
- Date: dates in this system are CORRECTABLE (the Part I
  correction story is the proof; issue dates are firm-editable
  per fx-0078). A correctable fact embedded in an immutable
  identifier forces either a lying code or a changing code.
  The issue date is a column, filtered and pivoted as a column.
- Year segments, matter, amounts: same reasoning -- columns,
  joined on the internal invoice id. The analysis capability
  lives in the CSV export (id, type, number, contact_id,
  matter_id, dates, ...); the code becomes one more column
  there. Codes stay dumb so the data can stay smart.

## Coexistence with the stored number

The corpus-pinned number (per-client default, global toggle,
editable start, no renumbering -- immutable billing-suite test)
is UNTOUCHED. The code is additive: a new stored column plus
per-type counters, rendered wherever a human reads an invoice
identity (lists, pages, crumbs, PDF, emails). 9,999 per series
per scope before width grows; a firm that outgrows it has long
since paid for the migration.

## Build scope when gated in (for the future authorization)

casework/app: schema column + per-type counter in the creation
path (gen_schema.py regenerated, never hand-edited); rendering
in app_ui/billing_ui.py and the PDF; migration story for
existing walk dbs (additive column, backfill by creation
order). Spine + billing suites immutable and green; the
numbering test's pinned behavior unchanged by construction.
Sheet references then supersede the type+date identification
(demo-walk-protocol.md) with codes.
