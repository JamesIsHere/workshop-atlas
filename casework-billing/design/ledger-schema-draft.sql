-- ledger-schema-draft.sql -- P0 PAPER DESIGN for the gate.
-- NOT installed anywhere. After gate ratification this enters
-- casework/app/schema/gen_schema.py, which adds the standard
-- per-table audit triggers (AI/AU/AD via casework_actor_*()) for
-- the mutable tables; the journal and external_events get INSERT
-- audit only plus the immutability triggers below. Tombstone
-- columns follow house style (deleted_at/deleted_by + partial
-- index). Money is INTEGER cents everywhere; no REAL columns.

-- ---------------------------------------------------------------
-- Ledger core
-- ---------------------------------------------------------------

CREATE TABLE ledger_accounts (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN
    ('operating_bank','trust_bank','client_trust','matter_trust',
     'fee_income','processor_fee_expense','chargeback_expense')),
  name TEXT NOT NULL,
  parent_id INTEGER REFERENCES ledger_accounts(id),
  contact_id INTEGER REFERENCES contacts(id),
  matter_id INTEGER REFERENCES matters(id),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  created_by INTEGER REFERENCES users(id),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id),
  -- shape rules for the sub-ledger tree:
  CHECK (kind != 'client_trust' OR (contact_id IS NOT NULL AND parent_id IS NOT NULL)),
  CHECK (kind != 'matter_trust' OR (matter_id IS NOT NULL AND parent_id IS NOT NULL)),
  CHECK (kind NOT IN ('operating_bank','trust_bank','fee_income',
                      'processor_fee_expense','chargeback_expense')
         OR parent_id IS NULL)
);
CREATE INDEX idx_ledger_accounts_parent ON ledger_accounts (parent_id);
CREATE UNIQUE INDEX uq_client_trust ON ledger_accounts (parent_id, contact_id)
  WHERE kind = 'client_trust' AND deleted_at IS NULL;
CREATE UNIQUE INDEX uq_matter_trust ON ledger_accounts (parent_id, matter_id)
  WHERE kind = 'matter_trust' AND deleted_at IS NULL;

CREATE TABLE journal_entries (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN
    ('trust_deposit','bill_direct_payment','earn_out','disbursement',
     'sim_settlement','processor_fee','chargeback','reversal')),
  memo TEXT,
  invoice_id INTEGER,             -- REFERENCES invoices(id); soft ref until invoices lands in same migration
  payment_id INTEGER,             -- REFERENCES invoice_payments(id)
  external_event_id INTEGER REFERENCES external_events(id),
  reverses_entry_id INTEGER REFERENCES journal_entries(id),
  replaces_entry_id INTEGER REFERENCES journal_entries(id),
  posted_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  posted_by INTEGER REFERENCES users(id)
);

CREATE TABLE journal_postings (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL REFERENCES journal_entries(id),
  account_id INTEGER NOT NULL REFERENCES ledger_accounts(id),
  side TEXT NOT NULL CHECK (side IN ('debit','credit')),
  amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
  cleared_at TEXT,                -- bank-witness annotation (r1); the ONLY mutable field
  statement_ref TEXT
);
CREATE INDEX idx_postings_entry ON journal_postings (entry_id);
CREATE INDEX idx_postings_account ON journal_postings (account_id);

-- Immutability (F8, schema-enforced):
CREATE TRIGGER trg_journal_entries_no_update BEFORE UPDATE ON journal_entries
BEGIN SELECT RAISE(ABORT, 'journal_entries is append-only'); END;
CREATE TRIGGER trg_journal_entries_no_delete BEFORE DELETE ON journal_entries
BEGIN SELECT RAISE(ABORT, 'journal_entries is append-only'); END;
CREATE TRIGGER trg_journal_postings_no_delete BEFORE DELETE ON journal_postings
BEGIN SELECT RAISE(ABORT, 'journal_postings is append-only'); END;
CREATE TRIGGER trg_journal_postings_clearing_only BEFORE UPDATE ON journal_postings
WHEN NEW.entry_id != OLD.entry_id OR NEW.account_id != OLD.account_id
  OR NEW.side != OLD.side OR NEW.amount_cents != OLD.amount_cents
  OR NEW.id != OLD.id OR OLD.cleared_at IS NOT NULL
BEGIN SELECT RAISE(ABORT, 'postings are immutable except un-cleared -> cleared'); END;

-- ---------------------------------------------------------------
-- External event stream (F7 independence substrate)
-- ---------------------------------------------------------------

CREATE TABLE external_events (
  id INTEGER PRIMARY KEY,
  event_type TEXT NOT NULL CHECK (event_type IN
    ('deposit','check_cut','processor_batch','chargeback')),
  bank_account_id INTEGER NOT NULL REFERENCES ledger_accounts(id),
  occurred_on TEXT NOT NULL,      -- date the external world saw it originate
  amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
  direction TEXT NOT NULL CHECK (direction IN ('in','out')),
  counterparty TEXT,
  memo TEXT,
  invoice_id INTEGER,
  payment_id INTEGER,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TRIGGER trg_external_events_no_update BEFORE UPDATE ON external_events
BEGIN SELECT RAISE(ABORT, 'external_events is append-only'); END;
CREATE TRIGGER trg_external_events_no_delete BEFORE DELETE ON external_events
BEGIN SELECT RAISE(ABORT, 'external_events is append-only'); END;

-- ---------------------------------------------------------------
-- Invoicing machinery (column-level polish allowed pre-merge;
-- table roster and relationships are what the gate fixes)
-- ---------------------------------------------------------------

CREATE TABLE invoices (
  id INTEGER PRIMARY KEY,
  invoice_type TEXT NOT NULL CHECK (invoice_type IN ('bill','trust_request')),
  contact_id INTEGER NOT NULL REFERENCES contacts(id),
  matter_id INTEGER REFERENCES matters(id),
  recipient_contact_id INTEGER NOT NULL REFERENCES contacts(id),
  trust_level TEXT CHECK (trust_level IN ('client','matter')),
  trust_account_id INTEGER REFERENCES ledger_accounts(id),
  number INTEGER NOT NULL,
  number_scope TEXT NOT NULL CHECK (number_scope IN ('client','global')),
  preparer_user_id INTEGER REFERENCES users(id),
  issued_date TEXT,
  due_date TEXT,
  discount_cents INTEGER NOT NULL DEFAULT 0 CHECK (discount_cents >= 0),
  footer TEXT,
  color_scheme TEXT,
  language TEXT NOT NULL DEFAULT 'en' CHECK (language IN ('en','es')),
  late_fee_enabled INTEGER NOT NULL DEFAULT 0,
  late_fee_kind TEXT CHECK (late_fee_kind IN ('fixed','percent')),
  late_fee_value INTEGER,         -- cents if fixed, basis points if percent
  late_fee_recurring INTEGER NOT NULL DEFAULT 0,
  late_fee_recur_days INTEGER,
  reminder_enabled INTEGER NOT NULL DEFAULT 0,
  reminder_days INTEGER,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  created_by INTEGER REFERENCES users(id),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id),
  CHECK (invoice_type != 'trust_request'
         OR (trust_level IS NOT NULL AND trust_account_id IS NOT NULL))
);
-- NOTE: no stored paid/status column -- "moves to Paid at zero
-- balance" is derived (charges - discount - payments), single fact
-- store discipline.

CREATE TABLE invoice_charges (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  charge_type TEXT NOT NULL CHECK (charge_type IN ('service','expense')),
  description TEXT NOT NULL,
  amount_cents INTEGER NOT NULL CHECK (amount_cents >= 0),
  charge_date TEXT,
  matter_id INTEGER REFERENCES matters(id),
  source TEXT NOT NULL DEFAULT 'manual'
    CHECK (source IN ('manual','saved','time','late_fee')),
  time_entry_id INTEGER REFERENCES time_entries(id),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  created_by INTEGER REFERENCES users(id),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id)
);

CREATE TABLE saved_charges (
  id INTEGER PRIMARY KEY,
  description TEXT NOT NULL,
  amount_cents INTEGER NOT NULL CHECK (amount_cents >= 0),
  charge_type TEXT NOT NULL CHECK (charge_type IN ('service','expense')),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  created_by INTEGER REFERENCES users(id),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id)
);

CREATE TABLE invoice_payments (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  method TEXT NOT NULL CHECK (method IN
    ('direct','trust_transfer','sim_card','sim_echeck')),
  amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
  payment_date TEXT NOT NULL,
  note TEXT,
  destination_account_id INTEGER REFERENCES ledger_accounts(id),
  source_trust_level TEXT CHECK (source_trust_level IN ('client','matter')),
  source_account_id INTEGER REFERENCES ledger_accounts(id),
  associated_charge_id INTEGER REFERENCES invoice_charges(id),
  refunded INTEGER NOT NULL DEFAULT 0,
  refund_note TEXT,
  journal_entry_id INTEGER REFERENCES journal_entries(id),  -- current entry (r2 two-layer)
  processor_txn_id INTEGER REFERENCES processor_transactions(id),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  created_by INTEGER REFERENCES users(id),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id),
  CHECK (method != 'trust_transfer'
         OR (source_trust_level IS NOT NULL AND source_account_id IS NOT NULL))
);

CREATE TABLE payment_plans (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  frequency_days INTEGER NOT NULL CHECK (frequency_days > 0),
  installment_cents INTEGER NOT NULL CHECK (installment_cents > 0),
  start_date TEXT NOT NULL,
  auto_charge INTEGER NOT NULL DEFAULT 0,
  accepted_forms TEXT NOT NULL DEFAULT 'card,echeck',
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  created_by INTEGER REFERENCES users(id),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id)
);

CREATE TABLE plan_installments (
  id INTEGER PRIMARY KEY,
  plan_id INTEGER NOT NULL REFERENCES payment_plans(id),
  due_date TEXT NOT NULL,
  amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
  pre_reminder_at TEXT,
  due_reminder_at TEXT,
  post_reminder_at TEXT,
  paid_payment_id INTEGER REFERENCES invoice_payments(id)
);

CREATE TABLE invoice_shares (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  recipient_contact_id INTEGER NOT NULL REFERENCES contacts(id),
  channel TEXT NOT NULL DEFAULT 'email' CHECK (channel IN ('email')),
  token TEXT NOT NULL UNIQUE,
  reminders_enabled INTEGER NOT NULL DEFAULT 0,
  reminder_days INTEGER,
  last_reminder_at TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  created_by INTEGER REFERENCES users(id),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id)
);

CREATE TABLE time_entries (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  contact_id INTEGER REFERENCES contacts(id),
  matter_id INTEGER REFERENCES matters(id),
  entry_date TEXT NOT NULL,
  description TEXT,
  duration_seconds INTEGER NOT NULL DEFAULT 0 CHECK (duration_seconds >= 0),
  rate_cents_per_hour INTEGER CHECK (rate_cents_per_hour >= 0),
  timer_started_at TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  deleted_at TEXT,
  deleted_by INTEGER REFERENCES users(id),
  CHECK (contact_id IS NOT NULL OR matter_id IS NOT NULL)
);

-- ---------------------------------------------------------------
-- SimProcessor (deterministic; synthetic tokens only)
-- ---------------------------------------------------------------

CREATE TABLE processor_transactions (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN ('charge','echeck','refund','chargeback')),
  token TEXT NOT NULL CHECK (token LIKE 'SYNTHETIC-%'),
  amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
  fee_cents INTEGER NOT NULL DEFAULT 0 CHECK (fee_cents >= 0),
  status TEXT NOT NULL CHECK (status IN
    ('approved','declined','settled','charged_back')),
  batch_id INTEGER REFERENCES settlement_batches(id),
  invoice_payment_id INTEGER,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE settlement_batches (
  id INTEGER PRIMARY KEY,
  settle_date TEXT NOT NULL,
  bank_account_id INTEGER NOT NULL REFERENCES ledger_accounts(id),
  mode TEXT NOT NULL CHECK (mode IN ('gross','net')),
  gross_cents INTEGER NOT NULL CHECK (gross_cents >= 0),
  fee_cents INTEGER NOT NULL CHECK (fee_cents >= 0),
  net_cents INTEGER NOT NULL CHECK (net_cents >= 0),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
