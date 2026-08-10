"""Demo seed for gate reviews (goal.md decision default, spared at
red-pen round 3): realistic synthetic billing volume so demo-grade
browse screens are judged at n>1, not against near-empty tables.

Casework/app modules ONLY -- this file writes zero SQL. The db is
created through app_ui's own make_server path (install + synthetic
marker included), then populated by module calls, exactly the way
the UI itself writes. The DEMO WALK never uses this db; walks run
on fresh empty databases by contract.

Deterministic by design: fixed dates, fixed amounts -- regenerating
yields the same books. Regenerated, never hand-edited.

Run (from billing-ui/): python verify/seed_demo.py
Writes data/demo-billing.db and prints the summary + fiduciary
verdict. Login for gate reviews: demo.reviewer@synthetic.test /
demo-seed-pass (code shown in the mailbox panel).
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS = HERE.parent.parent
CASEWORK_UI = ATLAS / "casework-ui"
CWB_VERIFY = ATLAS / "casework-billing" / "verify"
sys.path.insert(0, str(CASEWORK_UI))
sys.path.insert(0, str(CWB_VERIFY))

import app_ui  # noqa: F401, E402  (wires casework onto sys.path)
from app_ui import server as ui_server  # noqa: E402
from app import auth, billing, contacts, matters  # noqa: E402
from app import processor, timekeeping, users  # noqa: E402
import run_fiduciary as fid  # noqa: E402

DB = HERE.parent / "data" / "demo-billing.db"

ADMIN_EMAIL = "demo.reviewer@synthetic.test"
ADMIN_PASS = "demo-seed-pass"

NOW = "2026-07-20T00:00:00Z"
D = ["2026-07-2%d" % i for i in range(1, 10)]  # D[0]=07-21 ...


def main():
    if DB.exists():
        DB.unlink()  # generated artifact; regenerated every run
    httpd = ui_server.make_server(DB)
    conn = httpd.app_conn
    try:
        # --- firm: admin who can log into app_ui ---
        admin = users.create_user(conn, ADMIN_EMAIL, "Demo Reviewer",
                                  NOW, role_label="Managing Attorney")
        users.update_user(conn, admin, is_admin=1, is_owner=1)
        auth.set_password(conn, admin, ADMIN_PASS)
        status, token = auth.login(conn, ADMIN_EMAIL, ADMIN_PASS, NOW)
        assert status == "enrollment_required", status
        auth.enroll_twofa(conn, admin, "email", token, NOW)
        conn.actor.set("user", admin)

        # --- clients and matters ---
        c = {}
        for given in ("Vera", "Omar", "Lena", "Petra"):
            c[given] = contacts.create_contact(
                conn, "person", NOW, admin, given_name=given,
                family_name="Synthetic",
                email=f"{given.lower()}.client@synthetic.test")
        m = {
            "vera": matters.create_matter(
                conn, "Vera Synthetic I-130", c["Vera"], NOW, admin),
            "omar": matters.create_matter(
                conn, "Omar Synthetic H-1B", c["Omar"], NOW, admin),
            "lena": matters.create_matter(
                conn, "Lena Synthetic N-400", c["Lena"], NOW, admin),
            "petra": matters.create_matter(
                conn, "Petra Synthetic I-485", c["Petra"], NOW, admin),
        }

        # --- accounts, saved charges, rates ---
        iolta = billing.create_bank_account(conn, "trust_bank",
                                            "SYNTH IOLTA", admin)
        op = billing.create_bank_account(conn, "operating_bank",
                                        "SYNTH Operating", admin)
        saved_i130 = billing.create_saved_charge(
            conn, "SYNTH I-130 preparation", 250000, "service", admin)
        saved_h1b = billing.create_saved_charge(
            conn, "SYNTH H-1B preparation", 350000, "service", admin)
        billing.create_saved_charge(
            conn, "SYNTH RFE response", 120000, "service", admin)
        timekeeping.set_user_default_rate(conn, admin, 25000)

        # --- time entries (some billed later, some open) ---
        t_vera = timekeeping.create_entry(
            conn, admin, D[1], duration="2h",
            description="SYNTH case work",
            contact_id=c["Vera"], matter_id=m["vera"])
        t_lena1 = timekeeping.create_entry(
            conn, admin, D[2], duration="4.5h",
            description="SYNTH N-400 preparation",
            contact_id=c["Lena"], matter_id=m["lena"])
        t_lena2 = timekeeping.create_entry(
            conn, admin, D[3], duration="2.4h",
            description="SYNTH interview prep",
            contact_id=c["Lena"], matter_id=m["lena"])
        timekeeping.create_entry(
            conn, admin, D[5], duration="1h",
            description="SYNTH status call (unbilled)",
            contact_id=c["Petra"], matter_id=m["petra"])

        # --- Vera: the full anchor story ---
        consult = billing.create_invoice(conn, "bill", c["Vera"],
                                         admin, D[0])
        billing.add_charge(conn, consult, "service",
                           "SYNTH consultation", 50000, admin,
                           charge_date=D[0])
        billing.record_payment(conn, consult, "direct", 50000, D[0],
                               admin, destination_account_id=op)
        tr_vera = billing.create_invoice(
            conn, "trust_request", c["Vera"], admin, D[0],
            trust_level="client", trust_account_id=iolta)
        billing.add_charge(conn, tr_vera, "service",
                           "SYNTH retainer request", 500000, admin,
                           charge_date=D[0])
        billing.share_invoice(conn, tr_vera, admin, share_date=D[0])
        billing.pay_online(conn, tr_vera, "SYNTHETIC-VISA-SEED-V",
                           "card", D[0])
        bill_vera = billing.create_invoice(conn, "bill", c["Vera"],
                                           admin, D[1],
                                           matter_id=m["vera"])
        billing.import_saved_charges(conn, bill_vera, [saved_i130],
                                     admin)
        billing.import_time_entries(conn, bill_vera, [t_vera], admin)

        # --- Omar: retainer, prep bill, small refunded consult ---
        tr_omar = billing.create_invoice(
            conn, "trust_request", c["Omar"], admin, D[1],
            trust_level="client", trust_account_id=iolta)
        billing.add_charge(conn, tr_omar, "service",
                           "SYNTH retainer request", 800000, admin,
                           charge_date=D[1])
        billing.share_invoice(conn, tr_omar, admin, share_date=D[1])
        billing.pay_online(conn, tr_omar, "SYNTHETIC-VISA-SEED-O",
                           "card", D[1])
        consult_o = billing.create_invoice(conn, "bill", c["Omar"],
                                           admin, D[1])
        billing.add_charge(conn, consult_o, "service",
                           "SYNTH strategy consult", 30000, admin,
                           charge_date=D[1])
        billing.record_payment(conn, consult_o, "direct", 30000,
                               D[1], admin,
                               destination_account_id=op)

        # --- ONE settlement batch covering BOTH retainers: the
        # regression witness for P0 finding 2 (n:1 batch matching,
        # fixed under program ruling 2026-08-04) ---
        processor.settle(conn, D[2], posted_by=admin)

        # --- earn-outs after settlement ---
        billing.record_payment(conn, bill_vera, "trust_transfer",
                               300000, D[3], admin,
                               destination_account_id=op,
                               source_account_id=iolta,
                               source_trust_level="client")
        bill_omar = billing.create_invoice(conn, "bill", c["Omar"],
                                           admin, D[3],
                                           matter_id=m["omar"])
        billing.import_saved_charges(conn, bill_omar, [saved_h1b],
                                     admin)
        billing.record_payment(conn, bill_omar, "trust_transfer",
                               350000, D[4], admin,
                               destination_account_id=op,
                               source_account_id=iolta,
                               source_trust_level="client")

        # --- disbursements ---
        billing.disburse(conn, iolta, 120000, D[5], admin,
                         contact_id=c["Vera"],
                         counterparty="SYNTH-USCIS",
                         memo="SYNTH I-130 filing fee")
        billing.disburse(conn, iolta, 46000, D[6], admin,
                         contact_id=c["Omar"],
                         counterparty="SYNTH-USCIS",
                         memo="SYNTH H-1B filing fee")

        # --- Lena: partial payment, then a corrected amount (the
        # correction-trail browse data; regression witness for P0
        # finding 1, fixed under program ruling 2026-08-04) ---
        bill_lena = billing.create_invoice(conn, "bill", c["Lena"],
                                           admin, D[4],
                                           matter_id=m["lena"])
        billing.import_time_entries(conn, bill_lena,
                                    [t_lena1, t_lena2], admin)
        pay_lena = billing.record_payment(
            conn, bill_lena, "direct", 100000, D[5], admin,
            destination_account_id=op)
        billing.edit_payment(conn, pay_lena, admin, D[6],
                             amount_cents=90000)

        # --- Omar's consult refunded (second correction shape) ---
        pay_o = conn.execute(
            "SELECT id FROM invoice_payments WHERE invoice_id=?"
            " ORDER BY id", (consult_o,)).fetchone()[0]
        billing.refund_payment(conn, pay_o, admin, D[7],
                               note="SYNTH consult refunded")

        # --- Petra: outstanding trust request + draft bill ---
        tr_petra = billing.create_invoice(
            conn, "trust_request", c["Petra"], admin, D[6],
            trust_level="client", trust_account_id=iolta)
        billing.add_charge(conn, tr_petra, "service",
                           "SYNTH retainer request", 200000, admin,
                           charge_date=D[6])
        billing.share_invoice(conn, tr_petra, admin, share_date=D[6])
        draft = billing.create_invoice(conn, "bill", c["Petra"],
                                       admin, D[7],
                                       matter_id=m["petra"])
        billing.add_charge(conn, draft, "service",
                           "SYNTH I-485 preparation", 400000, admin,
                           charge_date=D[7])
        conn.commit()

        # --- verify the books we just wrote ---
        ok, lines = fid.run_suite(conn)
        counts = {}
        for label, table in (("contacts", "contacts"),
                             ("matters", "matters"),
                             ("invoices", "invoices"),
                             ("payments", "invoice_payments"),
                             ("time entries", "time_entries"),
                             ("journal entries", "journal_entries")):
            counts[label] = conn.execute(
                "SELECT count(*) FROM " + table).fetchone()[0]
    finally:
        httpd.client_httpd.server_close()
        httpd.server_close()
        conn.close()

    print("seed_demo: " + "; ".join(
        f"{v} {k}" for k, v in counts.items()))
    print("fiduciary on seeded db: " + lines[-1])
    print(f"db: {DB}")
    print(f"login: {ADMIN_EMAIL} / {ADMIN_PASS}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
