"""P4 parity tests: time tracking, invoice import, sharing family,
permissions, bulk download. Seed-tolerant."""
import tempfile
import zipfile
from pathlib import Path

from app import billing, ledger, scheduler, timekeeping

D = "2026-08-05"


def _op(conn):
    row = conn.execute("SELECT id FROM ledger_accounts WHERE"
                       " kind='operating_bank' AND deleted_at IS NULL"
                       " ORDER BY id LIMIT 1").fetchone()
    return row["id"] if row else ledger.create_bank_account(
        conn, "operating_bank", "SYNTH Operating", 1)


def test_invoicing_and_trust_accounting_time_tracking(conn):
    # criterion: start the timer, stop it, save -> entry with the
    # recorded duration stored against the chosen contact or matter
    # (fx-0064/0073)
    e = timekeeping.start_timer(conn, 2, "2026-08-05T10:00:00Z",
                                description="SYNTH research",
                                contact_id=1)
    timekeeping.stop_timer(conn, e, "2026-08-05T10:36:00Z")
    row = conn.execute("SELECT * FROM time_entries WHERE id=?",
                       (e,)).fetchone()
    assert row["duration_seconds"] == 36 * 60 and row["contact_id"] == 1
    # a stopped timer can resume (fx-0073)
    timekeeping.resume_timer(conn, e, "2026-08-05T11:00:00Z")
    timekeeping.stop_timer(conn, e, "2026-08-05T11:10:00Z")
    row = conn.execute("SELECT duration_seconds FROM time_entries WHERE"
                       " id=?", (e,)).fetchone()
    assert row["duration_seconds"] == 46 * 60, "resume accrues"
    # manual entry with attested duration formats (fx-0064)
    assert timekeeping.parse_duration("2h") == 7200
    assert timekeeping.parse_duration("36m") == 2160
    assert timekeeping.parse_duration("2.8h") == 10080
    assert timekeeping.parse_duration("5.5m") == 330
    m = timekeeping.create_entry(conn, 2, D, duration="2.8h",
                                 description="SYNTH drafting",
                                 matter_id=1)
    # entry lists: contact, matter, firm-wide, with filters (fx-0073)
    assert e in [r["id"] for r in timekeeping.entries(conn, contact_id=1)]
    assert m in [r["id"] for r in timekeeping.entries(conn, matter_id=1)]
    both = [r["id"] for r in timekeeping.entries(conn, user_id=2)]
    assert e in both and m in both
    timekeeping.update_entry(conn, m, duration="3h")
    assert conn.execute("SELECT duration_seconds FROM time_entries WHERE"
                        " id=?", (m,)).fetchone()[0] == 10800, "editable"


def test_invoicing_and_trust_accounting_time_entry_invoice_import(conn):
    # criterion: select time entries in the invoice's picker and import
    # -> they appear as Professional Services charges (fx-0063/0073);
    # amount = duration x rate (decision default 4, our design)
    timekeeping.set_user_default_rate(conn, 2, 25000)  # 250.00/h default
    e1 = timekeeping.create_entry(conn, 2, D, duration="2h",
                                  description="SYNTH interview",
                                  contact_id=1)
    e2 = timekeeping.create_entry(conn, 2, D, duration="5.5m",
                                  description="SYNTH email",
                                  contact_id=1,
                                  rate_cents_per_hour=30000)  # override
    b = billing.create_invoice(conn, "bill", 1, 1, D)
    billing.import_time_entries(conn, b, [e1, e2], 1)
    charges = billing.invoice_charges(conn, b)
    assert all(c["source"] == "time" for c in charges)
    assert all(c["description"].startswith("Professional Services")
               for c in charges), "Professional Services charges"
    assert charges[0]["amount_cents"] == 50000, "2h x default 250.00/h"
    # 330s x 30000c/h = 2750.0 -> half-up 2750
    assert charges[1]["amount_cents"] == (330 * 30000 + 1800) // 3600
    # an entry cannot bill twice
    try:
        billing.import_time_entries(conn, b, [e1], 1)
        raise AssertionError("double-billed a time entry")
    except billing.BillingError:
        pass


def test_invoicing_and_trust_accounting_invoice_sharing(conn):
    # criterion: Share -> chosen contact receives the invoice with a
    # link to view or download (fx-0060/0067/0068); recipient need not
    # be the matter's primary contact
    b = billing.create_invoice(conn, "bill", 1, 1, D)
    billing.add_charge(conn, b, "service", "SYNTH services", 50000, 1)
    # share to a THIRD PARTY (contact 2, not the invoice's client)
    token, recipient = billing.send_invoice_share(
        conn, b, 1, recipient_contact_id=2)
    assert recipient["contact_id"] == 2 and recipient["email"], \
        "contact info confirmed before sending (fx-0068)"
    mail = conn.execute(
        "SELECT * FROM email_outbox WHERE template='billing_share'"
        " ORDER BY id DESC LIMIT 1").fetchone()
    assert mail["recipient"] == recipient["email"]
    assert f"/invoice/{token}" in mail["body"], "link to view/download"


def test_invoicing_and_trust_accounting_payment_reminders(conn):
    # criterion: enable reminders -> recurring messages until the
    # balance reaches zero (fx-0060/0068/0070)
    _op(conn)
    b = billing.create_invoice(conn, "bill", 1, 1, "2026-08-01")
    billing.add_charge(conn, b, "service", "SYNTH services", 60000, 1)
    billing.send_invoice_share(conn, b, 1, reminders_enabled=1,
                               reminder_days=7, share_date="2026-08-01")

    def reminders():
        return conn.execute(
            "SELECT COUNT(*) FROM email_outbox WHERE"
            " template='billing_share_reminder'").fetchone()[0]

    scheduler.tick(conn, "2026-08-09T02:00:00Z")
    assert reminders() == 1, "reminder after the configured frequency"
    scheduler.tick(conn, "2026-08-12T02:00:00Z")
    assert reminders() == 1, "not before the next interval"
    scheduler.tick(conn, "2026-08-16T02:00:00Z")
    assert reminders() == 2, "recurring"
    billing.record_payment(conn, b, "direct", 60000, "2026-08-17", 1,
                           destination_account_id=_op(conn))
    scheduler.tick(conn, "2026-08-23T02:00:00Z")
    assert reminders() == 2, "reminders stop at zero balance (fx-0070)"


def test_invoicing_and_trust_accounting_bulk_invoice_sharing(conn):
    # criterion: share multiple invoices in a chosen mode -> delivered
    # per that mode (fx-0056): all to one contact as a zip, or each to
    # its own contact
    ids = []
    for contact in (1, 2):
        b = billing.create_invoice(conn, "bill", contact, 1, D)
        billing.add_charge(conn, b, "service", "SYNTH services", 10000, 1)
        ids.append(b)
    with tempfile.TemporaryDirectory() as td:
        zpath = billing.bulk_share_invoices(conn, ids, "one_contact", 1,
                                            contact_id=2, zip_dir=td)
        assert len(zipfile.ZipFile(zpath).namelist()) == 2, \
            "zip carries every selected invoice"
        mail = conn.execute(
            "SELECT * FROM email_outbox WHERE template='billing_bulk_share'"
            " ORDER BY id DESC LIMIT 1").fetchone()
        assert mail is not None, "one email to the chosen contact"
    tokens = billing.bulk_share_invoices(conn, ids, "each_own", 1)
    assert len(tokens) == 2
    mails = conn.execute(
        "SELECT COUNT(*) FROM email_outbox WHERE template='billing_share'"
    ).fetchone()[0]
    assert mails >= 2, "each invoice delivered to its own contact"


def test_invoicing_and_trust_accounting_bulk_invoice_download(conn):
    # criterion: Download Invoice(s) on selected invoices -> a zip with
    # the selected invoices (fx-0056)
    ids = []
    for _ in range(3):
        b = billing.create_invoice(conn, "bill", 1, 1, D)
        billing.add_charge(conn, b, "service", "SYNTH services", 5000, 1)
        ids.append(b)
    with tempfile.TemporaryDirectory() as td:
        zpath = billing.bulk_download_invoices(
            conn, ids, str(Path(td) / "invoices.zip"))
        names = zipfile.ZipFile(zpath).namelist()
        assert len(names) == 3 and all(n.endswith(".pdf") for n in names)


def test_invoicing_and_trust_accounting_invoice_access_permissions(conn):
    # criterion: set a user's Invoice Permissions to No Access -> the
    # user cannot view, create, edit, or delete invoices (fx-0075);
    # Limited cannot edit/delete other users' invoices
    own = billing.create_invoice(conn, "bill", 1, 2, D)     # user 2's
    other = billing.create_invoice(conn, "bill", 1, 3, D)   # user 3's
    billing.set_invoice_permission(conn, 2, "none")
    for verb in ("view", "create", "edit", "delete"):
        assert not billing.can_invoice(conn, 2, verb, own), \
            f"No Access still allows {verb}"
    try:
        billing.require_invoice_access(conn, 2, "view", own)
        raise AssertionError("require_invoice_access let none through")
    except billing.BillingError:
        pass
    billing.set_invoice_permission(conn, 2, "limited")
    assert billing.can_invoice(conn, 2, "view", other)
    assert billing.can_invoice(conn, 2, "edit", own), "own invoice"
    assert not billing.can_invoice(conn, 2, "edit", other), \
        "limited cannot edit others' invoices"
    assert not billing.can_invoice(conn, 2, "delete", other)
    billing.set_invoice_permission(conn, 2, "unlimited")
    assert billing.can_invoice(conn, 2, "delete", other)
    # admins bypass (user 1 is the seeded owner/admin)
    billing.set_invoice_permission(conn, 1, "none")
    assert billing.can_invoice(conn, 1, "delete", other), "admin bypass"