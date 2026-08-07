"""Billing area (casework-billing P2): the distinct module carrying
BOTH function families of corpus entry module-exists -- invoicing
(this file) and trust accounting (re-exported from app.ledger, the
posting engine underneath every money movement here).

Invoice mechanics honor the corpus at capability level: Bill vs Trust
Request (fx-0065/0070/0071), builder ops, per-client vs global
numbering (fx-0076/0078), saved charges bills-only (fx-0059),
firm-default settings copied at creation so they apply forward and
stay overridable per invoice (fx-0076), automatic late fees on the
scheduler tick (fx-0058), Spanish invoice rendering translating
template chrome only (fx-0052 exclusions stay verbatim).

Invoice PDFs are generated with fpdf2: casework's render.py is
AcroForm-fill machinery for official forms and has no free-document
path (deviation from decision default 7's assumption, logged in the
worklog; flagged for the P3 gate).

Paid is DERIVED (zero balance, fx-0070/0071) -- never a stored
status column.
"""

from datetime import date as _date

from fpdf import FPDF

from app.ledger import (  # noqa: F401  (trust accounting family)
    LedgerError, account_balance, account_transactions,
    create_bank_account, disburse, earn_out, ensure_client_trust,
    ensure_matter_trust, list_bank_accounts, record_bill_direct_payment,
    record_trust_deposit, reverse_entry, trust_account_tab,
    trust_ledger_overview)


class BillingError(ValueError):
    pass


# Template chrome translations (fx-0052): labels only. Charge
# descriptions, discount descriptions, late-fee descriptions, and
# custom text are NEVER translated -- they render as stored.
INVOICE_STRINGS = {
    "en": {"invoice": "Invoice", "bill": "Bill",
           "trust_request": "Trust Request", "client": "Client",
           "matter": "Matter", "description": "Description",
           "amount": "Amount", "date": "Date", "discount": "Discount",
           "balance_due": "Balance Due", "issued": "Issued",
           "due": "Due", "charges": "Charges",
           "trust_held": "Remaining in Trust"},
    "es": {"invoice": "Factura", "bill": "Factura",
           "trust_request": "Solicitud de fondos de fideicomiso",
           "client": "Cliente", "matter": "Caso",
           "description": "Descripcion", "amount": "Importe",
           "date": "Fecha", "discount": "Descuento",
           "balance_due": "Saldo pendiente", "issued": "Emitida",
           "due": "Vence", "charges": "Cargos",
           "trust_held": "Restante en fideicomiso"},
}

SETTINGS_COLUMNS = ("preparer_user_id", "issued_date", "due_date",
                    "discount_cents", "footer", "color_scheme", "language",
                    "late_fee_enabled", "late_fee_kind", "late_fee_value",
                    "late_fee_recurring", "late_fee_recur_days",
                    "reminder_enabled", "reminder_days")


# --- firm defaults ----------------------------------------------------

def get_setting(conn, key, default=None):
    row = conn.execute("SELECT value FROM firm_settings WHERE key=?",
                       (key,)).fetchone()
    return row["value"] if row else default


def set_setting(conn, key, value):
    conn.execute("INSERT INTO firm_settings (key, value) VALUES (?,?)"
                 " ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                 (key, str(value)))


def _auto_due_date(issued):
    """fx-0076: due on the 15th or the last day of the month, whichever
    comes sooner after the issue date."""
    y, m, d = (int(x) for x in issued.split("-"))
    if d < 15:
        return f"{y:04d}-{m:02d}-15"
    nxt_y, nxt_m = (y + 1, 1) if m == 12 else (y, m + 1)
    last = (_date(nxt_y, nxt_m, 1) - _date.resolution).day
    return f"{y:04d}-{m:02d}-{last:02d}"


def _next_number(conn, contact_id):
    """Per-client by default; firm-wide when global numbering is on.
    Enabling never renumbers: the counter starts from the firm total
    unless the editable beginning number says otherwise (fx-0076)."""
    if get_setting(conn, "billing.global_numbering", "0") == "1":
        stored = get_setting(conn, "billing.global_next")
        total = conn.execute("SELECT COUNT(*) FROM invoices").fetchone()[0]
        number = int(stored) if stored is not None else total + 1
        set_setting(conn, "billing.global_next", number + 1)
        return number, "global"
    n = conn.execute("SELECT COUNT(*) FROM invoices WHERE contact_id=?"
                     " AND number_scope='client'",
                     (contact_id,)).fetchone()[0]
    return n + 1, "client"


_CODE_LETTER = {"bill": "B", "trust_request": "T"}


def _next_code(conn, invoice_type, contact_id):
    """Display code (billing-ui invoice-codes.md, build gated in by
    James 2026-08-07): one letter per type, 4-digit zero-padded,
    independent gapless series per type. Scope mirrors _next_number's
    active mode; a flip to global continues from the per-type firm
    total and never renumbers (fx-0076 mirror). Stored at creation,
    immutable; deleted invoices keep their code -- a series never
    reuses."""
    letter = _CODE_LETTER[invoice_type]
    if get_setting(conn, "billing.global_numbering", "0") == "1":
        key = f"billing.code_global_next.{letter}"
        stored = get_setting(conn, key)
        total = conn.execute(
            "SELECT COUNT(*) FROM invoices WHERE invoice_type=?",
            (invoice_type,)).fetchone()[0]
        n = int(stored) if stored is not None else total + 1
        set_setting(conn, key, n + 1)
        return f"{letter}{n:04d}", "global"
    n = conn.execute(
        "SELECT COUNT(*) FROM invoices WHERE contact_id=?"
        " AND invoice_type=? AND code_scope='client'",
        (contact_id, invoice_type)).fetchone()[0]
    return f"{letter}{n + 1:04d}", "client"


# --- invoice core -----------------------------------------------------

def create_invoice(conn, invoice_type, contact_id, created_by, issued_date,
                   matter_id=None, recipient_contact_id=None,
                   trust_level=None, trust_account_id=None, language=None):
    if invoice_type not in ("bill", "trust_request"):
        raise BillingError(f"unknown invoice type: {invoice_type}")
    if invoice_type == "trust_request" and not (trust_level
                                                and trust_account_id):
        raise BillingError("a trust request needs trust_level and a"
                           " destination trust account (fx-0061)")
    number, scope = _next_number(conn, contact_id)
    display_code, code_scope = _next_code(conn, invoice_type, contact_id)
    due = None
    if get_setting(conn, "billing.auto_due_date", "0") == "1":
        due = _auto_due_date(issued_date)
    cur = conn.execute(
        "INSERT INTO invoices (invoice_type, contact_id, matter_id,"
        " recipient_contact_id, trust_level, trust_account_id, number,"
        " number_scope, display_code, code_scope,"
        " preparer_user_id, issued_date, due_date, footer,"
        " color_scheme, language, late_fee_enabled, late_fee_kind,"
        " late_fee_value, late_fee_recurring, late_fee_recur_days,"
        " reminder_enabled, reminder_days, created_by)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (invoice_type, contact_id, matter_id,
         recipient_contact_id or contact_id, trust_level, trust_account_id,
         number, scope, display_code, code_scope,
         get_setting(conn, "billing.default_preparer"),
         issued_date, due,
         get_setting(conn, "billing.default_footer"),
         get_setting(conn, "billing.default_color"),
         language or "en",
         int(get_setting(conn, "billing.default_late_fee_enabled", "0")),
         get_setting(conn, "billing.default_late_fee_kind"),
         int(v) if (v := get_setting(
             conn, "billing.default_late_fee_value")) else None,
         int(get_setting(conn, "billing.default_late_fee_recurring", "0")),
         int(v) if (v := get_setting(
             conn, "billing.default_late_fee_recur_days")) else None,
         int(get_setting(conn, "billing.default_reminder_enabled", "0")),
         int(v) if (v := get_setting(
             conn, "billing.default_reminder_days")) else None,
         created_by))
    return cur.lastrowid


def get_invoice(conn, invoice_id):
    row = conn.execute("SELECT * FROM invoices WHERE id=?"
                       " AND deleted_at IS NULL", (invoice_id,)).fetchone()
    if row is None:
        raise BillingError(f"no such invoice: {invoice_id}")
    return row


def update_invoice_settings(conn, invoice_id, **fields):
    """Per-invoice Invoice Settings tab (fx-0061/fx-0065): overrides
    the copied firm defaults, whitelisted columns only."""
    bad = set(fields) - set(SETTINGS_COLUMNS)
    if bad:
        raise BillingError(f"not invoice settings: {sorted(bad)}")
    get_invoice(conn, invoice_id)
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE invoices SET {sets} WHERE id=?",
                 (*fields.values(), invoice_id))


def add_charge(conn, invoice_id, charge_type, description, amount_cents,
               created_by, charge_date=None, matter_id=None,
               source="manual", time_entry_id=None):
    if charge_type not in ("service", "expense"):
        raise BillingError(f"unknown charge type: {charge_type}")
    get_invoice(conn, invoice_id)
    cur = conn.execute(
        "INSERT INTO invoice_charges (invoice_id, charge_type, description,"
        " amount_cents, charge_date, matter_id, source, time_entry_id,"
        " created_by) VALUES (?,?,?,?,?,?,?,?,?)",
        (invoice_id, charge_type, description, amount_cents, charge_date,
         matter_id, source, time_entry_id, created_by))
    return cur.lastrowid


def update_charge(conn, charge_id, description=None, amount_cents=None,
                  charge_date=None):
    sets, vals = [], []
    for col, v in (("description", description),
                   ("amount_cents", amount_cents),
                   ("charge_date", charge_date)):
        if v is not None:
            sets.append(f"{col}=?")
            vals.append(v)
    if sets:
        conn.execute(f"UPDATE invoice_charges SET {', '.join(sets)}"
                     " WHERE id=? AND deleted_at IS NULL",
                     (*vals, charge_id))


def invoice_charges(conn, invoice_id):
    return conn.execute(
        "SELECT * FROM invoice_charges WHERE invoice_id=?"
        " AND deleted_at IS NULL ORDER BY id", (invoice_id,)).fetchall()


def invoice_balance(conn, invoice_id):
    inv = get_invoice(conn, invoice_id)
    charges = conn.execute(
        "SELECT COALESCE(SUM(amount_cents),0) FROM invoice_charges"
        " WHERE invoice_id=? AND deleted_at IS NULL",
        (invoice_id,)).fetchone()[0]
    payments = conn.execute(
        "SELECT COALESCE(SUM(amount_cents),0) FROM invoice_payments"
        " WHERE invoice_id=? AND refunded=0 AND deleted_at IS NULL",
        (invoice_id,)).fetchone()[0]
    return charges - inv["discount_cents"] - payments


def invoice_status(conn, invoice_id):
    """Paid at zero balance (fx-0070/0071) -- derived, never stored."""
    return "paid" if invoice_balance(conn, invoice_id) <= 0 else "outstanding"


def list_invoices(conn, tab="outstanding"):
    rows = conn.execute("SELECT id FROM invoices WHERE deleted_at IS NULL"
                        " ORDER BY id").fetchall()
    if tab == "all":
        return [r["id"] for r in rows]
    return [r["id"] for r in rows
            if invoice_status(conn, r["id"]) == ("paid" if tab == "paid"
                                                 else "outstanding")]


# --- saved charges ----------------------------------------------------

def create_saved_charge(conn, description, amount_cents, charge_type,
                        created_by):
    if charge_type not in ("service", "expense"):
        raise BillingError(f"unknown charge type: {charge_type}")
    cur = conn.execute(
        "INSERT INTO saved_charges (description, amount_cents, charge_type,"
        " created_by) VALUES (?,?,?,?)",
        (description, amount_cents, charge_type, created_by))
    return cur.lastrowid


def list_saved_charges(conn):
    return conn.execute("SELECT * FROM saved_charges WHERE deleted_at IS"
                        " NULL ORDER BY id").fetchall()


def import_saved_charges(conn, invoice_id, saved_ids, created_by):
    """Bulk import into the Invoice Charges tab; Bills only, never
    Trust Requests (fx-0059)."""
    inv = get_invoice(conn, invoice_id)
    if inv["invoice_type"] != "bill":
        raise BillingError("saved charges can be added to Bills only,"
                           " not Trust Requests (fx-0059)")
    out = []
    for sid in saved_ids:
        s = conn.execute("SELECT * FROM saved_charges WHERE id=?"
                         " AND deleted_at IS NULL", (sid,)).fetchone()
        if s is None:
            raise BillingError(f"no such saved charge: {sid}")
        out.append(add_charge(conn, invoice_id, s["charge_type"],
                              s["description"], s["amount_cents"],
                              created_by, source="saved"))
    return out


# --- automatic late fees (scheduler tick) -----------------------------

def scheduled_work(conn, now):
    """Called by app.scheduler.tick as the system actor."""
    apply_late_fees(conn, now)
    plan_work(conn, now)
    share_reminder_work(conn, now)


def apply_late_fees(conn, now):
    """fx-0058: fixed or percent-of-outstanding fee once the due date
    passes unpaid; optional recurring fee every N days until paid.
    Idempotent per tick: applies only when no fee exists yet or the
    recurrence interval has elapsed since the last one."""
    today = now[:10]
    for inv in conn.execute(
            "SELECT * FROM invoices WHERE deleted_at IS NULL"
            " AND late_fee_enabled=1 AND due_date IS NOT NULL"
            " AND due_date < ?", (today,)).fetchall():
        balance = invoice_balance(conn, inv["id"])
        if balance <= 0:
            continue
        last = conn.execute(
            "SELECT MAX(charge_date) FROM invoice_charges WHERE"
            " invoice_id=? AND source='late_fee' AND deleted_at IS NULL",
            (inv["id"],)).fetchone()[0]
        if last is not None:
            if not inv["late_fee_recurring"] or not inv["late_fee_recur_days"]:
                continue
            gap = (_date.fromisoformat(today)
                   - _date.fromisoformat(last)).days
            if gap < inv["late_fee_recur_days"]:
                continue
        if inv["late_fee_kind"] == "percent":
            # late_fee_value is basis points of the outstanding balance
            amount = balance * inv["late_fee_value"] // 10000
        else:
            amount = inv["late_fee_value"] or 0
        if amount <= 0:
            continue
        add_charge(conn, inv["id"], "service", "Late fee", amount,
                   None, charge_date=today, source="late_fee")


# --- payments (P3 U3.1/U3.2) ------------------------------------------

def available_trust_funds(conn, level, contact_id=None, matter_id=None):
    """The 'available amount displayed' when paying from trust
    (fx-0066)."""
    if level == "matter":
        return trust_account_tab(conn, matter_id=matter_id)["available_cents"]
    return trust_account_tab(conn, contact_id=contact_id)["available_cents"]


def _validate_association(conn, invoice_id, charge_id, amount_cents):
    """fx-0057: a payment associates with ONE charge and may not exceed
    it."""
    if charge_id is None:
        return
    ch = conn.execute("SELECT * FROM invoice_charges WHERE id=? AND"
                      " deleted_at IS NULL", (charge_id,)).fetchone()
    if ch is None or ch["invoice_id"] != invoice_id:
        raise BillingError("associated charge must belong to the invoice")
    if amount_cents > ch["amount_cents"]:
        raise BillingError("a payment larger than the charge cannot be"
                           " associated with it (fx-0057)")


def _journal_for_payment(conn, inv, method, amount_cents, payment_date,
                         created_by, destination_account_id,
                         source_account_id, source_trust_level, note,
                         payment_id=None, replaces_entry_id=None,
                         witness_bank=True):
    """Dispatch a payment to its ledger recipe; returns the entry id.
    Sim payments post nothing here -- settlement does (processor.py).
    witness_bank=False posts books-only (a correction repost: the bank
    record keeps what the bank saw; real-bank ruling 2026-08-07)."""
    if method == "direct":
        if inv["invoice_type"] == "trust_request":
            dest = destination_account_id or inv["trust_account_id"]
            kwargs = ({"contact_id": inv["contact_id"]}
                      if inv["trust_level"] == "client"
                      else {"matter_id": inv["matter_id"]})
            return record_trust_deposit(
                conn, dest, amount_cents, payment_date, created_by,
                memo=note, invoice_id=inv["id"], payment_id=payment_id,
                replaces_entry_id=replaces_entry_id,
                witness_bank=witness_bank, **kwargs)
        if destination_account_id is None:
            raise BillingError("a direct bill payment needs a destination"
                               " account (fx-0070)")
        return record_bill_direct_payment(
            conn, destination_account_id, amount_cents, payment_date,
            created_by, memo=note, invoice_id=inv["id"],
            payment_id=payment_id, replaces_entry_id=replaces_entry_id,
            witness_bank=witness_bank)
    if method == "trust_transfer":
        if inv["invoice_type"] != "bill":
            raise BillingError("trust transfers pay Bills (fx-0066)")
        if not (source_account_id and source_trust_level
                and destination_account_id):
            raise BillingError("trust transfer needs source level, source"
                               " trust account, and destination (fx-0066)")
        kwargs = ({"contact_id": inv["contact_id"]}
                  if source_trust_level == "client"
                  else {"matter_id": inv["matter_id"]})
        return earn_out(conn, source_account_id, destination_account_id,
                        amount_cents, payment_date, created_by, memo=note,
                        invoice_id=inv["id"], payment_id=payment_id,
                        replaces_entry_id=replaces_entry_id,
                        witness_bank=witness_bank, **kwargs)
    raise BillingError(f"unknown payment method: {method}")


def record_payment(conn, invoice_id, method, amount_cents, payment_date,
                   created_by, destination_account_id=None,
                   source_account_id=None, source_trust_level=None,
                   note=None, associated_charge_id=None,
                   processor_txn_id=None):
    inv = get_invoice(conn, invoice_id)
    _validate_association(conn, invoice_id, associated_charge_id,
                          amount_cents)
    if method not in ("direct", "trust_transfer", "sim_card",
                      "sim_echeck"):
        raise BillingError(f"unknown payment method: {method}")
    # The payment row is created BEFORE the journal posts so external
    # events carry their payment_id from birth -- the reconciliation
    # matcher groups bank events and book entries by that linkage
    # (real-bank ruling 2026-08-07). The savepoint keeps a failed post
    # from leaving an orphan row.
    conn.execute("SAVEPOINT record_payment")
    try:
        cur = conn.execute(
            "INSERT INTO invoice_payments (invoice_id, method,"
            " amount_cents, payment_date, note, destination_account_id,"
            " source_trust_level, source_account_id,"
            " associated_charge_id, journal_entry_id, processor_txn_id,"
            " created_by) VALUES (?,?,?,?,?,?,?,?,?,NULL,?,?)",
            (invoice_id, method, amount_cents, payment_date, note,
             destination_account_id, source_trust_level,
             source_account_id, associated_charge_id, processor_txn_id,
             created_by))
        payment_id = cur.lastrowid
        if method in ("direct", "trust_transfer"):
            entry = _journal_for_payment(
                conn, inv, method, amount_cents, payment_date,
                created_by, destination_account_id, source_account_id,
                source_trust_level, note, payment_id=payment_id)
            conn.execute("UPDATE invoice_payments SET journal_entry_id=?"
                         " WHERE id=?", (entry, payment_id))
    except Exception:
        conn.execute("ROLLBACK TO record_payment")
        conn.execute("RELEASE record_payment")
        raise
    conn.execute("RELEASE record_payment")
    return payment_id


def get_payment(conn, payment_id):
    row = conn.execute("SELECT * FROM invoice_payments WHERE id=? AND"
                       " deleted_at IS NULL", (payment_id,)).fetchone()
    if row is None:
        raise BillingError(f"no such payment: {payment_id}")
    return row


def charge_payment_entries(conn, charge_id):
    """fx-0057: the entry shown under an associated charge -- payment
    date and amount."""
    return [(r["payment_date"], r["amount_cents"]) for r in conn.execute(
        "SELECT payment_date, amount_cents FROM invoice_payments"
        " WHERE associated_charge_id=? AND refunded=0 AND deleted_at IS"
        " NULL ORDER BY id", (charge_id,))]


def edit_payment(conn, payment_id, edited_by, edit_date, amount_cents=None,
                 payment_date=None, note=None, associated_charge_id=None):
    """fx-0077/fx-0055: open the payment, change values, save. The ROW
    updates (audited); the journal corrects by reversal + repost (r2)
    -- posted rows never mutate."""
    p = get_payment(conn, payment_id)
    if p["refunded"]:
        raise BillingError("refunded payments are not editable")
    inv = get_invoice(conn, p["invoice_id"])
    new_amount = amount_cents if amount_cents is not None \
        else p["amount_cents"]
    new_date = payment_date or p["payment_date"]
    if associated_charge_id is not None:
        _validate_association(conn, p["invoice_id"], associated_charge_id,
                              new_amount)
    entry = p["journal_entry_id"]
    money_changed = (new_amount != p["amount_cents"]
                     or new_date != p["payment_date"])
    if money_changed and entry is not None:
        reverse_entry(conn, entry, edited_by, edit_date,
                      memo=f"edit payment {payment_id}")
        # BOOKS ONLY (real-bank ruling, James 2026-08-07): the bank
        # record keeps exactly what the bank saw at the original
        # recording. The repost posts no bank events; the recon
        # engine explains any bank-vs-book difference as a
        # reconciling item instead.
        entry = _journal_for_payment(
            conn, inv, p["method"], new_amount, new_date, edited_by,
            p["destination_account_id"], p["source_account_id"],
            p["source_trust_level"], note if note is not None else p["note"],
            payment_id=payment_id, replaces_entry_id=p["journal_entry_id"],
            witness_bank=False)
    conn.execute(
        "UPDATE invoice_payments SET amount_cents=?, payment_date=?,"
        " note=COALESCE(?, note), associated_charge_id=COALESCE(?,"
        " associated_charge_id), journal_entry_id=? WHERE id=?",
        (new_amount, new_date, note, associated_charge_id, entry,
         payment_id))


def refund_payment(conn, payment_id, refunded_by, refund_date, note=None):
    """fx-0055: full-amount only; the toggle plus an optional internal
    note. Platform payments trigger the processor refund automatically."""
    from app import processor as proc
    p = get_payment(conn, payment_id)
    if p["refunded"]:
        raise BillingError("payment already refunded")
    if p["journal_entry_id"] is not None:
        reverse_entry(conn, p["journal_entry_id"], refunded_by, refund_date,
                      memo=f"refund payment {payment_id}")
        # BOOKS ONLY (real-bank ruling, James 2026-08-07): the refund
        # is on the books; the bank record keeps what the bank saw.
        # Until a bank ever witnesses the money going back, the recon
        # engine carries it as a "refund awaiting bank" item.
    if p["processor_txn_id"] is not None:
        proc.refund(conn, p["processor_txn_id"])
    conn.execute("UPDATE invoice_payments SET refunded=1, refund_note=?"
                 " WHERE id=?", (note, payment_id))


# --- sharing machinery + online payment (P3 U3.3) ---------------------
# Share MACHINERY only: the email-sharing criterion is P4; this token
# is the substrate the pay page (and P4 sharing) rides on.

def share_invoice(conn, invoice_id, created_by, recipient_contact_id=None,
                  reminders_enabled=0, reminder_days=None,
                  share_date=None):
    inv = get_invoice(conn, invoice_id)
    n = conn.execute("SELECT COUNT(*) FROM invoice_shares WHERE"
                     " invoice_id=?", (invoice_id,)).fetchone()[0]
    token = f"SYNTH-INV-{invoice_id}-{n + 1}"
    if share_date is None:
        conn.execute(
            "INSERT INTO invoice_shares (invoice_id, recipient_contact_id,"
            " token, reminders_enabled, reminder_days, created_by)"
            " VALUES (?,?,?,?,?,?)",
            (invoice_id, recipient_contact_id or inv["recipient_contact_id"],
             token, reminders_enabled, reminder_days, created_by))
    else:
        conn.execute(
            "INSERT INTO invoice_shares (invoice_id, recipient_contact_id,"
            " token, reminders_enabled, reminder_days, created_by,"
            " created_at) VALUES (?,?,?,?,?,?,?)",
            (invoice_id, recipient_contact_id or inv["recipient_contact_id"],
             token, reminders_enabled, reminder_days, created_by,
             share_date))
    return token


def share_by_token(conn, token):
    return conn.execute("SELECT * FROM invoice_shares WHERE token=? AND"
                        " deleted_at IS NULL", (token,)).fetchone()


def _contact_email(conn, contact_id):
    row = conn.execute(
        "SELECT value FROM facts WHERE subject_type='contact' AND"
        " subject_id=? AND key='contact.email' AND idx=0",
        (contact_id,)).fetchone()
    return row["value"] if row else None


def pay_online(conn, invoice_id, token, kind, pay_date,
               amount_cents=None):
    """Adapted online-card-payment criterion: the simulated processor
    authorizes now; money moves at settlement (processor.settle). A
    firm setting auto-sends a receipt (fx-0076)."""
    from app import processor as proc
    inv = get_invoice(conn, invoice_id)
    amount = amount_cents or invoice_balance(conn, invoice_id)
    if amount <= 0:
        raise BillingError("nothing to pay")
    dest = inv["trust_account_id"] if inv["invoice_type"] == "trust_request" \
        else conn.execute(
            "SELECT id FROM ledger_accounts WHERE kind='operating_bank'"
            " AND deleted_at IS NULL ORDER BY id LIMIT 1").fetchone()["id"]
    txn = proc.charge(conn, token, amount, kind=kind)
    payment = record_payment(
        conn, invoice_id, "sim_card" if kind == "card" else "sim_echeck",
        amount, pay_date, None, destination_account_id=dest,
        processor_txn_id=txn)
    if get_setting(conn, "billing.receipt_auto_send", "0") == "1":
        email = _contact_email(conn, inv["recipient_contact_id"])
        if email:
            conn.execute(
                "INSERT INTO email_outbox (recipient, subject, body,"
                " template, entity_type, entity_id, created_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (email, f"Receipt: payment of {amount / 100:,.2f}",
                 f"Payment of {amount / 100:,.2f} received on invoice"
                 f" {inv['display_code']}. SYNTHETIC receipt.",
                 "billing_receipt", "invoice_payments", payment, pay_date))
    return payment


# --- payment plans (P3 U3.4) ------------------------------------------

def create_payment_plan(conn, invoice_id, frequency_days, installment_cents,
                        start_date, created_by, auto_charge=0,
                        accepted_forms="card,echeck"):
    """fx-0072, r4 boundary: attested fields only (frequency,
    installment amount, start date, accepted forms)."""
    balance = invoice_balance(conn, invoice_id)
    if balance <= 0:
        raise BillingError("nothing to schedule")
    cur = conn.execute(
        "INSERT INTO payment_plans (invoice_id, frequency_days,"
        " installment_cents, start_date, auto_charge, accepted_forms,"
        " created_by) VALUES (?,?,?,?,?,?,?)",
        (invoice_id, frequency_days, installment_cents, start_date,
         auto_charge, accepted_forms, created_by))
    plan_id = cur.lastrowid
    due = _date.fromisoformat(start_date)
    remaining = balance
    while remaining > 0:
        amt = min(installment_cents, remaining)
        conn.execute("INSERT INTO plan_installments (plan_id, due_date,"
                     " amount_cents) VALUES (?,?,?)",
                     (plan_id, due.isoformat(), amt))
        remaining -= amt
        due = _date.fromordinal(due.toordinal() + frequency_days)
    return plan_id


def plan_installments(conn, plan_id):
    return conn.execute("SELECT * FROM plan_installments WHERE plan_id=?"
                        " ORDER BY due_date", (plan_id,)).fetchall()


def _plan_reminder(conn, plan, inst, stage, now_date):
    inv = get_invoice(conn, plan["invoice_id"])
    email = _contact_email(conn, inv["recipient_contact_id"])
    if email:
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, f"Installment {stage}: invoice {inv['display_code']}",
             f"Installment of {inst['amount_cents'] / 100:,.2f} due"
             f" {inst['due_date']} on invoice {inv['display_code']}."
             " SYNTHETIC reminder.",
             "billing_plan_reminder", "plan_installments", inst["id"],
             now_date))
    conn.execute(f"UPDATE plan_installments SET {stage}_reminder_at=?"
                 " WHERE id=?", (now_date, inst["id"]))


def plan_work(conn, now):
    """Scheduler-tick work for payment plans (fx-0072): reminders 7
    days before, on the due day, 7 days after if unpaid; auto-charge
    debits the synthetic payment method on the due day."""
    from app import processor as proc  # noqa: F401 (auto-charge path)
    today = _date.fromisoformat(now[:10])
    for plan in conn.execute("SELECT * FROM payment_plans WHERE active=1"
                             " AND deleted_at IS NULL").fetchall():
        if invoice_balance(conn, plan["invoice_id"]) <= 0:
            continue
        for inst in plan_installments(conn, plan["id"]):
            if inst["paid_payment_id"] is not None:
                continue
            due = _date.fromisoformat(inst["due_date"])
            days = (due - today).days
            if plan["auto_charge"] and days <= 0 \
                    and inst["due_reminder_at"] is None:
                token = f"SYNTHETIC-AUTOPAY-{plan['id']}"
                payment = pay_online(conn, plan["invoice_id"], token,
                                     "card", today.isoformat(),
                                     amount_cents=inst["amount_cents"])
                conn.execute("UPDATE plan_installments SET"
                             " paid_payment_id=?, due_reminder_at=?"
                             " WHERE id=?",
                             (payment, today.isoformat(), inst["id"]))
                continue
            if days <= 7 and days > 0 and inst["pre_reminder_at"] is None:
                _plan_reminder(conn, plan, inst, "pre", today.isoformat())
            elif days == 0 and inst["due_reminder_at"] is None:
                _plan_reminder(conn, plan, inst, "due", today.isoformat())
            elif days <= -7 and inst["post_reminder_at"] is None:
                _plan_reminder(conn, plan, inst, "post", today.isoformat())


# --- time entry import (P4 U4.1) --------------------------------------

def import_time_entries(conn, invoice_id, entry_ids, created_by):
    """fx-0063/0073: selected time entries import as Professional
    Services charges. Amount = duration x rate (decision default 4)."""
    from app import timekeeping
    get_invoice(conn, invoice_id)
    out = []
    for eid in entry_ids:
        e = conn.execute("SELECT * FROM time_entries WHERE id=? AND"
                         " deleted_at IS NULL", (eid,)).fetchone()
        if e is None:
            raise BillingError(f"no such time entry: {eid}")
        billed = conn.execute(
            "SELECT 1 FROM invoice_charges WHERE time_entry_id=? AND"
            " deleted_at IS NULL", (eid,)).fetchone()
        if billed:
            raise BillingError(f"time entry {eid} is already billed")
        amount = timekeeping.charge_amount(conn, e)
        desc = "Professional Services: " + (e["description"] or
                                            f"time entry {eid}")
        out.append(add_charge(conn, invoice_id, "service", desc, amount,
                              created_by, charge_date=e["entry_date"],
                              matter_id=e["matter_id"], source="time",
                              time_entry_id=eid))
    return out


# --- email sharing + reminders (P4 U4.2) -------------------------------

def send_invoice_share(conn, invoice_id, created_by,
                       recipient_contact_id=None, message=None,
                       reminders_enabled=0, reminder_days=None,
                       share_date=None):
    """fx-0060/0067/0068: share by email to a chosen contact (need not
    be the matter's primary -- spouse, sponsor, third party), link to
    view and download. Returns (token, recipient row) so the caller can
    confirm the contact's information (fx-0068)."""
    inv = get_invoice(conn, invoice_id)
    recipient = recipient_contact_id or inv["recipient_contact_id"]
    email = _contact_email(conn, recipient)
    if not email:
        raise BillingError("the receiving contact needs a valid email"
                           " address (fx-0068)")
    if reminder_days is None:
        v = get_setting(conn, "billing.reminder_frequency_days")
        reminder_days = int(v) if v else None
    token = share_invoice(conn, invoice_id, created_by,
                          recipient_contact_id=recipient,
                          reminders_enabled=reminders_enabled,
                          reminder_days=reminder_days,
                          share_date=share_date)
    body = (f"Invoice {inv['display_code']} is available:"
            f" /invoice/{token} (view, download, pay)."
            + (f" {message}" if message else "") + " SYNTHETIC email.")
    conn.execute(
        "INSERT INTO email_outbox (recipient, subject, body, template,"
        " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (email, f"Invoice {inv['display_code']}", body, "billing_share",
         "invoices", invoice_id, inv["created_at"]))
    name = conn.execute("SELECT display_name FROM contacts WHERE id=?",
                        (recipient,)).fetchone()["display_name"]
    return token, {"contact_id": recipient, "display_name": name,
                   "email": email}


def share_reminder_work(conn, now):
    """fx-0060/0068/0070: recurring reminders with the invoice until
    the balance reaches zero, then they stop automatically."""
    today = _date.fromisoformat(now[:10])
    for s in conn.execute(
            "SELECT * FROM invoice_shares WHERE reminders_enabled=1 AND"
            " reminder_days IS NOT NULL AND deleted_at IS NULL").fetchall():
        if invoice_balance(conn, s["invoice_id"]) <= 0:
            continue  # reminders stop at zero balance
        last = s["last_reminder_at"] or s["created_at"][:10]
        if (today - _date.fromisoformat(last[:10])).days \
                < s["reminder_days"]:
            continue
        inv = get_invoice(conn, s["invoice_id"])
        email = _contact_email(conn, s["recipient_contact_id"])
        if not email:
            continue
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, f"Reminder: invoice {inv['display_code']}",
             f"Invoice {inv['display_code']} has an outstanding balance of"
             f" {invoice_balance(conn, inv['id']) / 100:,.2f}:"
             f" /invoice/{s['token']}. SYNTHETIC reminder.",
             "billing_share_reminder", "invoice_shares", s["id"],
             today.isoformat()))
        conn.execute("UPDATE invoice_shares SET last_reminder_at=?"
                     " WHERE id=?", (today.isoformat(), s["id"]))


def _invoice_pdf_bytes(conn, invoice_id):
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / f"invoice-{invoice_id}.pdf"
        invoice_pdf(conn, invoice_id, str(p))
        return p.read_bytes()


def bulk_download_invoices(conn, invoice_ids, out_path):
    """fx-0056: More Actions > Download Invoice(s) -> one zip."""
    import zipfile
    with zipfile.ZipFile(out_path, "w") as z:
        for iid in invoice_ids:
            inv = get_invoice(conn, iid)
            z.writestr(f"invoice-{inv['display_code']}-{iid}.pdf",
                       _invoice_pdf_bytes(conn, iid))
    return out_path


def bulk_share_invoices(conn, invoice_ids, mode, created_by,
                        contact_id=None, zip_dir=None):
    """fx-0056, both attested modes: 'one_contact' delivers every
    selected invoice to one contact as a zip (sponsoring-company
    pattern); 'each_own' sends each invoice to its own recipient as an
    individual link."""
    if mode == "one_contact":
        if contact_id is None:
            raise BillingError("one_contact mode needs the contact")
        email = _contact_email(conn, contact_id)
        if not email:
            raise BillingError("the contact needs a valid email address")
        from pathlib import Path
        zdir = Path(zip_dir) if zip_dir else Path(".")
        zpath = str(zdir / f"invoices-contact-{contact_id}.zip")
        bulk_download_invoices(conn, invoice_ids, zpath)
        conn.execute(
            "INSERT INTO email_outbox (recipient, subject, body, template,"
            " entity_type, entity_id, created_at) VALUES (?,?,?,?,?,?,?)",
            (email, f"{len(invoice_ids)} invoices",
             f"Attached zip with {len(invoice_ids)} invoices: {zpath}."
             " SYNTHETIC email.", "billing_bulk_share", "contacts",
             contact_id, "bulk"))
        return zpath
    if mode == "each_own":
        return [send_invoice_share(conn, iid, created_by)[0]
                for iid in invoice_ids]
    raise BillingError(f"unknown bulk share mode: {mode}")


# --- invoice access permissions (P4 U4.3; fx-0075) ---------------------

INVOICE_ACCESS_LEVELS = ("unlimited", "limited", "none")


def set_invoice_permission(conn, user_id, level):
    """Settings > User Access, three levels (fx-0075). Stored on
    casework's user_permissions machinery under record_type
    'invoices'."""
    if level not in INVOICE_ACCESS_LEVELS:
        raise BillingError(f"unknown invoice access level: {level}")
    conn.execute(
        "INSERT INTO user_permissions (user_id, record_type, level)"
        " VALUES (?,'invoices',?) ON CONFLICT (user_id, record_type)"
        " DO UPDATE SET level=excluded.level",
        (user_id, {"unlimited": "delete", "limited": "create",
                   "none": "none"}[level]))


def invoice_access_level(conn, user_id):
    row = conn.execute(
        "SELECT level FROM user_permissions WHERE user_id=? AND"
        " record_type='invoices'", (user_id,)).fetchone()
    if row is None:
        return "unlimited"  # small-firm default, casework convention
    return {"delete": "unlimited", "create": "limited",
            "none": "none"}[row["level"]]


def can_invoice(conn, user_id, verb, invoice_id=None):
    """verb in view|create|edit|delete. Limited access cannot edit or
    delete OTHER users' invoices (fx-0075)."""
    admin = conn.execute("SELECT is_admin, is_owner FROM users WHERE"
                         " id=?", (user_id,)).fetchone()
    if admin and (admin["is_admin"] or admin["is_owner"]):
        return True
    level = invoice_access_level(conn, user_id)
    if level == "none":
        return False
    if level == "unlimited" or verb in ("view", "create"):
        return True
    if invoice_id is None:
        return False
    return get_invoice(conn, invoice_id)["created_by"] == user_id


def require_invoice_access(conn, user_id, verb, invoice_id=None):
    if not can_invoice(conn, user_id, verb, invoice_id):
        raise BillingError(f"invoice access denied: user {user_id}"
                           f" cannot {verb} (fx-0075)")


# --- CSV exports (P4 U4.4; goal.md anti-lock-in supporting check) ------

def export_invoices_csv(conn):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "type", "number", "display_code", "contact_id",
                "matter_id", "issued_date", "due_date", "discount_cents",
                "balance_cents", "status"])
    for r in conn.execute("SELECT * FROM invoices WHERE deleted_at IS"
                          " NULL ORDER BY id"):
        w.writerow([r["id"], r["invoice_type"], r["number"],
                    r["display_code"],
                    r["contact_id"], r["matter_id"], r["issued_date"],
                    r["due_date"], r["discount_cents"],
                    invoice_balance(conn, r["id"]),
                    invoice_status(conn, r["id"])])
    return buf.getvalue()


def export_payments_csv(conn):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "invoice_id", "method", "amount_cents",
                "payment_date", "refunded", "journal_entry_id"])
    for r in conn.execute("SELECT * FROM invoice_payments WHERE"
                          " deleted_at IS NULL ORDER BY id"):
        w.writerow([r["id"], r["invoice_id"], r["method"],
                    r["amount_cents"], r["payment_date"], r["refunded"],
                    r["journal_entry_id"]])
    return buf.getvalue()


def export_time_entries_csv(conn):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "user_id", "contact_id", "matter_id", "entry_date",
                "duration_seconds", "description"])
    for r in conn.execute("SELECT * FROM time_entries WHERE deleted_at"
                          " IS NULL ORDER BY id"):
        w.writerow([r["id"], r["user_id"], r["contact_id"], r["matter_id"],
                    r["entry_date"], r["duration_seconds"],
                    r["description"]])
    return buf.getvalue()


def export_trust_ledger_csv(conn):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["entry_id", "posted_at", "kind", "account_id",
                "account_kind", "side", "amount_cents", "memo"])
    for r in conn.execute(
            """SELECT e.id AS entry_id, e.posted_at, e.kind AS ekind,
                      p.account_id, a.kind AS akind, p.side,
                      p.amount_cents, e.memo
               FROM journal_postings p
               JOIN journal_entries e ON e.id=p.entry_id
               JOIN ledger_accounts a ON a.id=p.account_id
               ORDER BY p.id"""):
        w.writerow([r["entry_id"], r["posted_at"], r["ekind"],
                    r["account_id"], r["akind"], r["side"],
                    r["amount_cents"], r["memo"]])
    return buf.getvalue()


# --- rendering (fpdf2) ------------------------------------------------

def _pdf_cents(cents):
    """Accounting presentation, integer math only (a float never
    touches money): 1,234.56 / (1,234.56)."""
    neg = cents < 0
    d, c = divmod(abs(cents), 100)
    s = f"{d:,}.{c:02d}"
    return f"({s})" if neg else s


def _pdf_date(iso):
    """User-facing date: MM/DD/YYYY, matching the billing screens
    (2026-08-07 break-in, authorized by James; presentation only,
    data stays ISO). Strict -- a stored date that is not ISO is a
    data defect and fails loud, never renders half-formatted."""
    if not iso:
        return ""
    y, m, d = iso.split("-")
    return _date(int(y), int(m), int(d)).strftime("%m/%d/%Y")


def invoice_pdf(conn, invoice_id, out_path):
    """Render the invoice as a PDF. Language translates template chrome
    only (fx-0052): stored descriptions and custom text stay verbatim.
    Dates MM/DD/YYYY; charges as a footed column table (2026-08-07
    break-in, authorized by James: presentation only -- the inline
    description-amount lines and float division were the defect)."""
    inv = get_invoice(conn, invoice_id)
    strings = INVOICE_STRINGS.get(inv["language"], INVOICE_STRINGS["en"])
    contact = conn.execute("SELECT display_name FROM contacts WHERE id=?",
                           (inv["contact_id"],)).fetchone()
    firm = get_setting(conn, "firm.name", "SYNTH Firm")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=16)
    pdf.cell(0, 10, firm, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=13)
    label = strings[inv["invoice_type"]]
    pdf.cell(0, 8, f"{label} {inv['display_code']}", new_x="LMARGIN",
             new_y="NEXT")
    pdf.set_font("helvetica", size=10)
    pdf.cell(0, 6, f"{strings['client']}: {contact['display_name']}",
             new_x="LMARGIN", new_y="NEXT")
    if inv["issued_date"]:
        pdf.cell(0, 6,
                 f"{strings['issued']}: {_pdf_date(inv['issued_date'])}",
                 new_x="LMARGIN", new_y="NEXT")
    if inv["due_date"]:
        pdf.cell(0, 6, f"{strings['due']}: {_pdf_date(inv['due_date'])}",
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 7, strings["charges"], new_x="LMARGIN", new_y="NEXT")
    # description | date | amount columns, amounts right-aligned --
    # the shape the bill screen and a working paper use; header
    # underlined, balance due over a top rule. Column chrome reuses
    # the translated strings (fx-0052); no new labels invented.
    w_desc, w_date, w_amt = 100, 40, 50
    pdf.set_font("helvetica", "B", size=10)
    pdf.cell(w_desc, 6, strings["description"], border="B")
    pdf.cell(w_date, 6, strings["date"], border="B")
    pdf.cell(w_amt, 6, strings["amount"], border="B", align="R",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=10)
    for ch in invoice_charges(conn, invoice_id):
        pdf.cell(w_desc, 6, ch["description"])
        pdf.cell(w_date, 6, _pdf_date(ch["charge_date"]))
        pdf.cell(w_amt, 6, _pdf_cents(ch["amount_cents"]), align="R",
                 new_x="LMARGIN", new_y="NEXT")
    if inv["discount_cents"]:
        pdf.cell(w_desc, 6, strings["discount"])
        pdf.cell(w_date, 6, "")
        pdf.cell(w_amt, 6, f"-{_pdf_cents(inv['discount_cents'])}",
                 align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 8, f"{strings['balance_due']}: "
                   f"{_pdf_cents(invoice_balance(conn, invoice_id))}",
             border="T", align="R", new_x="LMARGIN", new_y="NEXT")
    # the client's remaining trust on the document itself (2026-08-07
    # break-in, item H, authorized by James: presentation only) --
    # rendered only once the client actually has trust sub-ledgers
    subs = [r[0] for r in conn.execute(
        "SELECT a.id FROM ledger_accounts a"
        " JOIN ledger_accounts p ON p.id = a.parent_id"
        " AND p.kind = 'trust_bank'"
        " LEFT JOIN matters m ON m.id = a.matter_id"
        " WHERE a.deleted_at IS NULL"
        " AND (a.contact_id = ? OR m.primary_contact_id = ?)",
        (inv["contact_id"], inv["contact_id"]))]
    if subs:
        held = sum(account_balance(conn, a) for a in subs)
        pdf.set_font("helvetica", size=10)
        pdf.cell(0, 6, f"{strings['trust_held']}: {_pdf_cents(held)}",
                 align="R", new_x="LMARGIN", new_y="NEXT")
    if inv["footer"]:
        pdf.set_font("helvetica", size=8)
        pdf.cell(0, 6, inv["footer"], new_x="LMARGIN", new_y="NEXT")
    pdf.output(out_path)
    return out_path
