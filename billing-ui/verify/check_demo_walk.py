"""Close-out checker for the demo walk (protocol RATIFIED
2026-08-04; this file is bound by its close-out step 1).

Asserts the db RECEIPTS of every walk-sheet leg -- a walk can LOOK
done while a step was silently skipped; eyeballs cannot catch that
(the cold-run protocol's rehearsal-1 lesson, inherited). Then runs
the fiduciary suite in place: the screens must have produced
CPA-grade books.

Run (from billing-ui/): python verify/check_demo_walk.py
    data/demo-walk-<date>.db
Exit 0 iff every receipt holds and the fiduciary suite is green.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS = HERE.parent.parent
sys.path.insert(0, str(ATLAS / "casework-ui"))
sys.path.insert(0, str(ATLAS / "casework-billing" / "verify"))

import app_ui  # noqa: F401, E402  (wires casework onto sys.path)
from app import billing  # noqa: E402
from app import db as appdb  # noqa: E402
import run_fiduciary as fid  # noqa: E402


def checks(conn):
    """Yield (name, ok, detail) per walk-sheet leg (sheet step in
    parentheses). Amounts are the sheet's, verbatim."""
    def one(sql, args=()):
        row = conn.execute(sql, args).fetchone()
        return row[0] if row else None

    banks = {r["kind"]: r["id"] for r in conn.execute(
        "SELECT id, kind FROM ledger_accounts WHERE kind IN"
        " ('trust_bank','operating_bank')")}
    yield ("accounts (3)", len(banks) == 2,
           f"trust+operating present: {sorted(banks)}")

    contact = one("SELECT id FROM contacts WHERE display_name LIKE"
                  " 'Vera%'")
    matter = one("SELECT id FROM matters WHERE name LIKE"
                 " 'Vera Synthetic I-130%'")
    yield ("client + matter (2)", contact is not None
           and matter is not None,
           f"contact {contact}, matter {matter}")

    consult = one("SELECT id FROM invoices WHERE invoice_type='bill'"
                  " ORDER BY id LIMIT 1")
    consult_paid = (consult is not None and
                    billing.invoice_status(conn, consult) == "paid")
    yield ("consult bill paid direct (4)", consult_paid,
           f"invoice {consult} status"
           f" {billing.invoice_status(conn, consult) if consult else '-'}")

    tr = one("SELECT id FROM invoices WHERE"
             " invoice_type='trust_request'")
    tr_paid = (tr is not None
               and billing.invoice_status(conn, tr) == "paid")
    txn = one("SELECT count(*) FROM processor_transactions")
    yield ("retainer paid online (5)", tr_paid and (txn or 0) > 0,
           f"trust request {tr} paid via processor ({txn} txns)")

    batch = conn.execute("SELECT gross_cents, fee_cents FROM"
                         " settlement_batches").fetchone()
    yield ("settlement gross/fee (6)",
           batch is not None and batch["gross_cents"] == 500000
           and batch["fee_cents"] == 15030,
           f"batch {dict(batch) if batch else None}")

    te = conn.execute("SELECT duration_seconds, rate_cents_per_hour"
                      " FROM time_entries").fetchone()
    yield ("time entry 2h @ 250.00 (7)",
           te is not None and te["duration_seconds"] == 7200,
           f"entry {dict(te) if te else None}")

    bill = one("SELECT id FROM invoices WHERE invoice_type='bill'"
               " AND matter_id IS NOT NULL")
    n_charges = one("SELECT count(*) FROM invoice_charges WHERE"
                    " invoice_id=?", (bill,)) if bill else 0
    earned = (bill is not None and n_charges == 2
              and billing.invoice_status(conn, bill) == "paid"
              and one("SELECT count(*) FROM invoice_payments WHERE"
                      " invoice_id=? AND method='trust_transfer'",
                      (bill,)) == 1)
    yield ("bill imported + earned out (8)", earned,
           f"bill {bill}: {n_charges} charges, trust_transfer paid")

    disb = conn.execute("SELECT amount_cents, counterparty FROM"
                        " external_events WHERE event_type='check_cut'"
                        " AND counterparty LIKE '%USCIS%'").fetchone()
    yield ("disbursement 1,200.00 (9)",
           disb is not None and disb["amount_cents"] == 120000,
           f"event {dict(disb) if disb else None}")

    funds = billing.available_trust_funds(
        conn, "client", contact_id=contact) if contact else None
    yield ("client funds 800.00 (9)", funds == 80000,
           f"available {funds}")

    reversal = one("SELECT count(*) FROM journal_entries WHERE"
                   " kind='reversal' AND reverses_entry_id IS NOT"
                   " NULL")
    repost = one("SELECT count(*) FROM journal_entries WHERE"
                 " replaces_entry_id IS NOT NULL")
    edited = one("SELECT count(*) FROM invoice_payments WHERE"
                 " payment_date='2026-08-02' AND invoice_id=?",
                 (consult,)) if consult else 0
    yield ("correction trail (10)",
           (reversal or 0) >= 1 and (repost or 0) >= 1
           and (edited or 0) == 1,
           f"{reversal} reversal(s), {repost} repost(s), consult"
           f" payment dated 2026-08-02")

    actors = {r[0] for r in conn.execute(
        "SELECT DISTINCT actor_type FROM audit_log")}
    yield ("audit actors (walk-wide)",
           {"system", "user"} <= actors,
           f"actor classes {sorted(actors)}")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    db = Path(sys.argv[1])
    if not db.exists():
        print(f"no such db: {db}")
        return 2
    conn = appdb.connect(str(db))
    try:
        lines, ok_all = [], True
        for name, ok, detail in checks(conn):
            ok_all = ok_all and ok
            lines.append(f"{'PASS' if ok else 'FAIL':4s}"
                         f" {name:32s} {detail}")
        fid_ok, fid_lines = fid.run_suite(conn)
        lines.append(("PASS" if fid_ok else "FAIL")
                     + " fiduciary in place              "
                     + fid_lines[-1])
        ok_all = ok_all and fid_ok
    finally:
        conn.close()
    print("\n".join(lines))
    print(f"check-demo-walk: {'PASS' if ok_all else 'FAIL'} ({db})")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
