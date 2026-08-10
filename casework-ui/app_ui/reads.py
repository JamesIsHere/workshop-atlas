"""The ONE module allowed to read casework tables with SQL.

goal.md's no-logic rule, made mechanical (see verify/sweeps.py):
every other app_ui file contains zero SQL and zero .execute calls;
mutations NEVER happen here or anywhere else in app_ui -- they go
through casework's app modules. This file is SELECT-only display
reads that casework's modules do not expose; the sweep fails the
build if anything else creeps in.
"""


def user_count(conn):
    return conn.execute("SELECT count(*) FROM users").fetchone()[0]


def get_user(conn, user_id):
    return conn.execute("SELECT * FROM users WHERE id=?",
                        (user_id,)).fetchone()


def session_row(conn, token):
    """Session + user join for the pre-MFA states (twofa_passed=0),
    which auth.session_user deliberately refuses."""
    return conn.execute(
        "SELECT s.token, s.user_id, s.twofa_passed, u.twofa_method,"
        " u.email, u.name FROM sessions s JOIN users u ON u.id=s.user_id"
        " WHERE s.token=?", (token,)).fetchone()


def latest_twofa_email(conn, user_id):
    """The current login-code email, for the synthetic-mailbox panel.
    In production this message arrives in the user's real inbox."""
    return conn.execute(
        "SELECT subject, body FROM email_outbox WHERE template='twofa_code'"
        " AND entity_type='users' AND entity_id=? ORDER BY id DESC LIMIT 1",
        (user_id,)).fetchone()


# --- P1 display reads (anchor-path screens) ---

def counts(conn):
    return {name: conn.execute(
        f"SELECT count(*) FROM {table} WHERE deleted_at IS NULL"
        ).fetchone()[0]
        for name, table in (("contacts", "contacts"),
                            ("matters", "matters"),
                            ("events", "events"),
                            ("files", "files"),
                            ("tasks", "tasks"),
                            ("notes", "notes"))}


def list_contacts(conn):
    return conn.execute(
        "SELECT id, kind, display_name, created_at FROM contacts"
        " WHERE deleted_at IS NULL ORDER BY display_name").fetchall()


def contact_row(conn, contact_id):
    return conn.execute(
        "SELECT * FROM contacts WHERE id=? AND deleted_at IS NULL",
        (contact_id,)).fetchone()


def charged_invoice_ids(conn):
    """Invoice ids carrying at least one live charge. The landing
    list separates 'empty, never charged' from 'genuinely settled'
    (gated item 3, ruled rendering-side by James 2026-08-10): the
    derived status stays corpus-pinned (paid at zero balance,
    fx-0070/0071); only the presentation reclassifies."""
    return {r["invoice_id"] for r in conn.execute(
        "SELECT DISTINCT invoice_id FROM invoice_charges"
        " WHERE deleted_at IS NULL")}


def fact_labels(conn):
    """{key: human label} from fact_definitions -- the contact card
    renders labels, never machine keys (gate ruling 2026-08-10)."""
    return dict(conn.execute("SELECT key, label FROM fact_definitions"))


def contact_matters(conn, contact_id):
    return conn.execute(
        "SELECT id, name, created_at FROM matters WHERE"
        " primary_contact_id=? AND deleted_at IS NULL ORDER BY id",
        (contact_id,)).fetchall()


def matter_row(conn, matter_id):
    return conn.execute(
        "SELECT * FROM matters WHERE id=? AND deleted_at IS NULL",
        (matter_id,)).fetchone()


def matter_smart_forms(conn, matter_id):
    return conn.execute(
        "SELECT id, title, created_at FROM smart_forms WHERE matter_id=?"
        " AND deleted_at IS NULL ORDER BY id", (matter_id,)).fetchall()


def matter_events(conn, matter_id):
    return conn.execute(
        "SELECT id, title, starts_at FROM events WHERE matter_id=?"
        " AND deleted_at IS NULL ORDER BY starts_at, id",
        (matter_id,)).fetchall()


def smart_form_row(conn, smart_form_id):
    return conn.execute(
        "SELECT * FROM smart_forms WHERE id=? AND deleted_at IS NULL",
        (smart_form_id,)).fetchone()


def invitations_of(conn, smart_form_id):
    """Invitation rows WITH tokens -- the firm's copyable link."""
    return conn.execute(
        "SELECT id, token, channel, status, status_at FROM"
        " intake_invitations WHERE smart_form_id=? ORDER BY id",
        (smart_form_id,)).fetchall()


def event_row(conn, event_id):
    return conn.execute(
        "SELECT * FROM events WHERE id=? AND deleted_at IS NULL",
        (event_id,)).fetchone()


def event_reminders(conn, event_id):
    return conn.execute(
        "SELECT offset_value, offset_unit, channel FROM event_reminders"
        " WHERE event_id=? ORDER BY id", (event_id,)).fetchall()


# --- P2 display reads (browse surfaces) ---

def list_matters(conn):
    return conn.execute(
        "SELECT m.id, m.name, m.created_at, c.id AS contact_id,"
        " c.display_name FROM matters m JOIN contacts c ON"
        " c.id = m.primary_contact_id WHERE m.deleted_at IS NULL"
        " ORDER BY m.id").fetchall()


def task_row(conn, task_id):
    return conn.execute(
        "SELECT * FROM tasks WHERE id=? AND deleted_at IS NULL",
        (task_id,)).fetchone()


def note_row(conn, note_id):
    return conn.execute(
        "SELECT * FROM notes WHERE id=? AND deleted_at IS NULL",
        (note_id,)).fetchone()


def note_categories(conn):
    return conn.execute(
        "SELECT id, name FROM note_categories WHERE deleted_at IS NULL"
        ).fetchall()


def firm_settings_all(conn):
    return conn.execute(
        "SELECT key, value FROM firm_settings ORDER BY key").fetchall()


def list_users(conn):
    return conn.execute(
        "SELECT id, name, email, role_label, is_admin, deactivated_at"
        " FROM users WHERE deleted_at IS NULL ORDER BY id").fetchall()


# --- billing display reads (billing-ui P1; program ruling 2026-08-04:
# SQL stays here, rendering in billing_ui.py, writes in casework) ---

def invoice_rows(conn):
    """Invoice list joined to contact display names; status/balance
    are computed by billing module calls in the view (derived, never
    stored -- fx-0070)."""
    return conn.execute(
        "SELECT i.id, i.invoice_type, i.number, i.number_scope,"
        " i.display_code, i.issued_date, i.due_date, i.matter_id,"
        " i.contact_id,"
        " c.display_name FROM invoices i JOIN contacts c ON"
        " c.id = i.contact_id WHERE i.deleted_at IS NULL"
        " ORDER BY i.id DESC").fetchall()


def invoice_payments_of(conn, invoice_id):
    return conn.execute(
        "SELECT * FROM invoice_payments WHERE invoice_id=? AND"
        " deleted_at IS NULL ORDER BY id", (invoice_id,)).fetchall()


def settling_payments(conn):
    """Online payments the processor still holds (flow markers,
    s11): the client has paid, the money is not yet at the bank.
    journal_entry_id is set only at settlement (processor.settle),
    so null-with-a-processor-txn IS the settling fact -- the same
    test invoice_detail's status line has always used."""
    return conn.execute(
        "SELECT p.id, p.invoice_id, p.amount_cents, p.payment_date,"
        " p.method, i.display_code, i.contact_id, c.display_name"
        " FROM invoice_payments p JOIN invoices i ON"
        " i.id = p.invoice_id JOIN contacts c ON c.id = i.contact_id"
        " WHERE p.deleted_at IS NULL AND p.refunded = 0"
        " AND p.processor_txn_id IS NOT NULL"
        " AND p.journal_entry_id IS NULL ORDER BY p.id").fetchall()


def sub_accounts_of(conn, bank_id):
    """Client/matter sub-accounts under a trust bank, with the
    owning entity's name."""
    return conn.execute(
        "SELECT a.id, a.kind, a.name, a.contact_id, a.matter_id,"
        " c.display_name AS contact_name, m.name AS matter_name"
        " FROM ledger_accounts a LEFT JOIN contacts c ON"
        " c.id = a.contact_id LEFT JOIN matters m ON m.id = a.matter_id"
        " WHERE a.parent_id=? AND a.deleted_at IS NULL ORDER BY a.id",
        (bank_id,)).fetchall()


def ledger_account_row(conn, account_id):
    return conn.execute(
        "SELECT * FROM ledger_accounts WHERE id=? AND deleted_at IS"
        " NULL", (account_id,)).fetchone()


def account_entries(conn, account_id):
    """This account's postings, entry context attached, newest first."""
    return conn.execute(
        "SELECT p.id AS posting_id, p.side, p.amount_cents,"
        " e.id AS entry_id, e.kind, e.memo, e.posted_at,"
        " e.reverses_entry_id, e.replaces_entry_id, e.invoice_id"
        " FROM journal_postings p JOIN journal_entries e ON"
        " e.id = p.entry_id WHERE p.account_id=?"
        " ORDER BY e.posted_at DESC, e.id DESC", (account_id,)).fetchall()


def journal_entry_row(conn, entry_id):
    return conn.execute(
        "SELECT * FROM journal_entries WHERE id=?",
        (entry_id,)).fetchone()


def journal_postings_of(conn, entry_id):
    return conn.execute(
        "SELECT p.side, p.amount_cents, a.id AS account_id, a.name,"
        " a.kind FROM journal_postings p JOIN ledger_accounts a ON"
        " a.id = p.account_id WHERE p.entry_id=? ORDER BY p.id",
        (entry_id,)).fetchall()


def entry_reversed_by(conn, entry_id):
    return conn.execute(
        "SELECT id FROM journal_entries WHERE reverses_entry_id=?",
        (entry_id,)).fetchall()


def entry_replaced_by(conn, entry_id):
    return conn.execute(
        "SELECT id FROM journal_entries WHERE replaces_entry_id=?",
        (entry_id,)).fetchall()


def events_of_payment(conn, payment_id):
    return conn.execute(
        "SELECT * FROM external_events WHERE payment_id=? ORDER BY id",
        (payment_id,)).fetchall()


def time_entry_rows(conn):
    """Time entries with billed linkage (a charge imported from the
    entry) and the entity names."""
    return conn.execute(
        "SELECT t.id, t.entry_date, t.description, t.duration_seconds,"
        " t.rate_cents_per_hour, t.contact_id, t.matter_id,"
        " c.display_name AS contact_name, m.name AS matter_name,"
        " (SELECT COUNT(*) FROM invoice_charges ic WHERE"
        "  ic.time_entry_id = t.id AND ic.deleted_at IS NULL) AS billed,"
        " (SELECT ic.amount_cents FROM invoice_charges ic WHERE"
        "  ic.time_entry_id = t.id AND ic.deleted_at IS NULL"
        "  ORDER BY ic.id LIMIT 1) AS billed_cents"
        " FROM time_entries t LEFT JOIN contacts c ON c.id=t.contact_id"
        " LEFT JOIN matters m ON m.id=t.matter_id"
        " WHERE t.deleted_at IS NULL ORDER BY t.entry_date DESC, t.id"
        " DESC").fetchall()


def max_event_date(conn):
    return conn.execute(
        "SELECT MAX(occurred_on) FROM external_events").fetchone()[0]


# --- billing display reads (billing-ui P2: lifecycle write screens) ---

def invoice_shares_of(conn, invoice_id):
    """Share rows WITH tokens -- the firm's copyable client link
    (mirrors invitations_of; the client link is the firm's to hand
    out)."""
    return conn.execute(
        "SELECT id, token, created_at FROM invoice_shares WHERE"
        " invoice_id=? AND deleted_at IS NULL ORDER BY id",
        (invoice_id,)).fetchall()


def entries_of_payment(conn, payment_id):
    """The payment's full journal story: its own entries plus the
    reversal entries that corrected them (reversals carry
    reverses_entry_id, not payment_id)."""
    return conn.execute(
        "SELECT e.* FROM journal_entries e WHERE e.payment_id=?"
        " OR e.reverses_entry_id IN (SELECT id FROM journal_entries"
        " WHERE payment_id=?) ORDER BY e.id",
        (payment_id, payment_id)).fetchall()


def unbilled_time_entries(conn):
    """Time entries with no live imported charge -- the import
    picker's choices (importing a billed entry is a module-level
    error; the picker never offers one)."""
    return conn.execute(
        "SELECT t.id, t.entry_date, t.description, t.duration_seconds,"
        " t.rate_cents_per_hour, t.user_id, t.contact_id, t.matter_id,"
        " c.display_name AS contact_name, m.name AS matter_name"
        " FROM time_entries t LEFT JOIN contacts c ON c.id=t.contact_id"
        " LEFT JOIN matters m ON m.id=t.matter_id"
        " WHERE t.deleted_at IS NULL AND NOT EXISTS"
        " (SELECT 1 FROM invoice_charges ic WHERE ic.time_entry_id=t.id"
        "  AND ic.deleted_at IS NULL)"
        " ORDER BY t.entry_date, t.id").fetchall()


def known_counterparties(conn):
    """Distinct payees from prior bank events -- the disburse form's
    known-payee datalist (gated item F). Free entry stays allowed;
    this only feeds suggestions."""
    return [r[0] for r in conn.execute(
        "SELECT DISTINCT counterparty FROM external_events"
        " WHERE counterparty IS NOT NULL AND counterparty != ''"
        " ORDER BY counterparty")]


def recent_money_entries(conn, limit=8):
    """The home page's activity feed (status-page.md R6: money
    events only). Journal entries newest first, with the entry's
    posting amount, the invoice's display code when one is
    attached, and the acting party from the audit log (actor
    attribution predates roles -- item-12 ruling R1)."""
    return conn.execute(
        "SELECT e.id, e.kind, e.memo, e.posted_at, e.invoice_id,"
        " i.display_code,"
        " (SELECT MAX(p.amount_cents) FROM journal_postings p"
        "  WHERE p.entry_id = e.id) AS amount_cents,"
        " a.actor_type, u.name AS actor_name"
        " FROM journal_entries e"
        " LEFT JOIN invoices i ON i.id = e.invoice_id"
        " LEFT JOIN audit_log a ON a.entity_type='journal_entries'"
        "  AND a.entity_id = e.id AND a.action='insert'"
        " LEFT JOIN users u ON a.actor_type='user'"
        "  AND u.id = a.actor_id"
        " ORDER BY e.posted_at DESC, e.id DESC LIMIT ?",
        (limit,)).fetchall()


# --- casework-tabs P1 display reads (calendar; program amendment
# 2026-08-10: SQL stays here, rendering in server.py, writes ride
# casework modules) ---

def calendar_events(conn):
    """Every live event with its linkage names. Expiry auto events
    (source='expiry_auto') carry their source fact for provenance;
    the view derives kind (appointment / deadline / expiry) -- kind
    is presentation, never stored."""
    return conn.execute(
        "SELECT e.id, e.title, e.starts_at, e.ends_at, e.source,"
        " e.contact_id, e.matter_id, f.key AS fact_key,"
        " c.display_name AS contact_name, m.name AS matter_name"
        " FROM events e"
        " LEFT JOIN facts f ON f.id = e.source_fact_id"
        " LEFT JOIN contacts c ON c.id = e.contact_id"
        " LEFT JOIN matters m ON m.id = e.matter_id"
        " WHERE e.deleted_at IS NULL"
        " ORDER BY e.starts_at, e.id").fetchall()


def calendar_vmax(conn):
    """VMAX clocks: the imm.vmax_date fact per contact (the vmax
    report's source, reports.py) rendered as a calendar kind."""
    return conn.execute(
        "SELECT f.subject_id AS contact_id, f.value AS due_on,"
        " c.display_name AS contact_name FROM facts f"
        " JOIN contacts c ON c.id = f.subject_id"
        " AND c.deleted_at IS NULL"
        " WHERE f.subject_type='contact' AND f.key='imm.vmax_date'"
        " AND f.idx=0 AND f.value IS NOT NULL AND f.value != ''"
        " ORDER BY f.value, f.subject_id").fetchall()


def calendar_task_dues(conn):
    """Open tasks with due dates -- completed tasks leave the
    calendar ([Q] gate ruling pending)."""
    return conn.execute(
        "SELECT t.id, t.title, t.due_date, t.contact_id, t.matter_id,"
        " c.display_name AS contact_name, m.name AS matter_name"
        " FROM tasks t"
        " LEFT JOIN contacts c ON c.id = t.contact_id"
        " LEFT JOIN matters m ON m.id = t.matter_id"
        " WHERE t.deleted_at IS NULL AND t.completed_at IS NULL"
        " AND t.due_date IS NOT NULL"
        " ORDER BY t.due_date, t.id").fetchall()


def calendar_invoice_dues(conn):
    """Invoices carrying a due date; the view keeps outstanding ones
    only (status derived via billing.invoice_status, fx-0070 -- the
    module call stays in the view, money math never here)."""
    return conn.execute(
        "SELECT i.id, i.display_code, i.due_date, i.contact_id,"
        " c.display_name AS contact_name FROM invoices i"
        " JOIN contacts c ON c.id = i.contact_id"
        " WHERE i.deleted_at IS NULL AND i.due_date IS NOT NULL"
        " ORDER BY i.due_date, i.id").fetchall()


def event_attendees(conn, event_id):
    return conn.execute(
        "SELECT a.id, a.user_id, a.contact_id, u.name AS user_name,"
        " c.display_name AS contact_name FROM event_attendees a"
        " LEFT JOIN users u ON u.id = a.user_id"
        " LEFT JOIN contacts c ON c.id = a.contact_id"
        " WHERE a.event_id=? ORDER BY a.id", (event_id,)).fetchall()


# --- casework-tabs P2 display reads (tasks; program amendment
# 2026-08-10: SQL stays here, rendering in server.py, writes ride
# casework modules) ---

def tasks_rows(conn, assignee_id=None, completed=False):
    """Task rows for the tab with linkage names: open or completed,
    optionally narrowed to one assignee (the my-open default,
    Appendix A)."""
    q = ("SELECT t.id, t.title, t.due_date, t.completed_at,"
         " t.contact_id, t.matter_id,"
         " c.display_name AS contact_name, m.name AS matter_name"
         " FROM tasks t"
         " LEFT JOIN contacts c ON c.id = t.contact_id"
         " LEFT JOIN matters m ON m.id = t.matter_id"
         " WHERE t.deleted_at IS NULL AND t.completed_at IS "
         + ("NOT NULL" if completed else "NULL"))
    params = []
    if assignee_id is not None:
        q += (" AND EXISTS (SELECT 1 FROM task_assignees ta"
              " WHERE ta.task_id = t.id AND ta.user_id = ?)")
        params.append(assignee_id)
    return conn.execute(
        q + " ORDER BY t.due_date IS NULL, t.due_date, t.id",
        params).fetchall()


def task_assignee_names(conn):
    """{task_id: 'name, name'} across live tasks -- one query, the
    index composes cells from it."""
    out = {}
    for r in conn.execute(
            "SELECT ta.task_id, u.name FROM task_assignees ta"
            " JOIN users u ON u.id = ta.user_id ORDER BY ta.task_id,"
            " ta.user_id"):
        out.setdefault(r["task_id"], []).append(r["name"])
    return {tid: ", ".join(names) for tid, names in out.items()}


def task_lists_rows(conn):
    return conn.execute(
        "SELECT tl.id, tl.name,"
        " (SELECT COUNT(*) FROM task_list_items i"
        "  WHERE i.task_list_id = tl.id) AS item_count"
        " FROM task_lists tl WHERE tl.deleted_at IS NULL"
        " ORDER BY tl.id").fetchall()


def task_list_row(conn, task_list_id):
    return conn.execute(
        "SELECT * FROM task_lists WHERE id=? AND deleted_at IS NULL",
        (task_list_id,)).fetchone()


def task_list_items(conn, task_list_id):
    return conn.execute(
        "SELECT i.*, u.name AS assignee_name FROM task_list_items i"
        " LEFT JOIN users u ON u.id = i.default_assignee_id"
        " WHERE i.task_list_id=? ORDER BY i.position, i.id",
        (task_list_id,)).fetchall()


def task_list_automations(conn):
    """{task_list_id: ['type / status', ...]} -- the matter statuses
    that auto-import each list (matter_statuses.auto_task_list_id is
    the automation linkage the schema stores)."""
    out = {}
    for r in conn.execute(
            "SELECT s.auto_task_list_id AS tl, mt.name AS type_name,"
            " s.name AS status_name FROM matter_statuses s"
            " JOIN matter_types mt ON mt.id = s.matter_type_id"
            " WHERE s.auto_task_list_id IS NOT NULL"
            " AND s.deleted_at IS NULL ORDER BY mt.name, s.position"):
        out.setdefault(r["tl"], []).append(
            f"{r['type_name']} / {r['status_name']}")
    return out


def contact_date_fact_defs(conn):
    """Contact-level date/expiry fact definitions -- the reference
    choices tasks.add_list_item accepts (its own validation rule)."""
    return conn.execute(
        "SELECT key, label FROM fact_definitions"
        " WHERE subject_type='contact'"
        " AND value_type IN ('date','expiry')"
        " ORDER BY label").fetchall()


def trust_sub_accounts_of_contact(conn, contact_id):
    """Trust sub-ledger account ids belonging to a contact: their
    client-level funds plus funds held for their matters (gated
    item H -- the bill page shows the client's remaining trust).
    Balances are summed by the caller via ledger.account_balance;
    money math stays in the core module."""
    return [r[0] for r in conn.execute(
        "SELECT a.id FROM ledger_accounts a"
        " JOIN ledger_accounts p ON p.id = a.parent_id"
        " AND p.kind = 'trust_bank'"
        " LEFT JOIN matters m ON m.id = a.matter_id"
        " WHERE a.deleted_at IS NULL"
        " AND (a.contact_id = ? OR m.primary_contact_id = ?)"
        " ORDER BY a.id", (contact_id, contact_id))]
