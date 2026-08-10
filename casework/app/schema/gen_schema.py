"""Schema generator for casework. Emits schema.sql; never hand-edit output.

Invariant enforcement lives HERE (design/schema-design.md is the paper
design):
- soft delete: tables declared soft_delete=True get deleted_at/deleted_by
  columns and a trash partial index appended mechanically.
- audit trail: tables declared audited=True get AFTER INSERT/UPDATE/DELETE
  triggers writing audit_log rows. Actor comes from the app-registered
  SQLite functions casework_actor_type()/casework_actor_id() (per-connection
  closures). Out-of-band writers without those functions fail loudly --
  that is deliberate: no unaudited mutation path exists.

Run: python gen_schema.py   (writes schema.sql beside this file)
"""

from pathlib import Path

# (name, [(col, ddl)], soft_delete, audited)
# Record tables: soft_delete=True, audited=True. Adapter/log/config tables
# carry no tombstones and (for pure datasets) no audit triggers.
TABLES = [
    # --- facts (invariant 1) ---
    ("fact_definitions", [
        ("key", "TEXT PRIMARY KEY"),
        ("subject_type", "TEXT NOT NULL CHECK (subject_type IN ('contact','matter'))"),
        ("value_type", "TEXT NOT NULL CHECK (value_type IN ('text','number','date','boolean','list','expiry'))"),
        ("label", "TEXT NOT NULL"),
        ("is_custom", "INTEGER NOT NULL DEFAULT 0"),
        ("repeating", "INTEGER NOT NULL DEFAULT 0"),
        ("list_options", "TEXT"),
    ], False, True),
    ("facts", [
        ("id", "INTEGER PRIMARY KEY"),
        ("subject_type", "TEXT NOT NULL CHECK (subject_type IN ('contact','matter'))"),
        ("subject_id", "INTEGER NOT NULL"),
        ("key", "TEXT NOT NULL REFERENCES fact_definitions(key)"),
        ("idx", "INTEGER NOT NULL DEFAULT 0"),
        ("value", "TEXT"),
        ("updated_at", "TEXT NOT NULL"),
        ("", "UNIQUE (subject_type, subject_id, key, idx)"),
    ], False, True),
    # --- registry (invariant 2) ---
    # Registry mechanics only (gate ruling 7): fact-like data (email,
    # phone, A-number, unique identifier) lives in the fact store.
    # display_name is the acknowledged derived label, app-composed
    # from name facts for persons.
    ("contacts", [
        ("id", "INTEGER PRIMARY KEY"),
        ("kind", "TEXT NOT NULL CHECK (kind IN ('person','company'))"),
        ("display_name", "TEXT NOT NULL"),
        ("archived_at", "TEXT"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("matter_types", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
    ], True, True),
    ("matter_statuses", [
        ("id", "INTEGER PRIMARY KEY"),
        ("matter_type_id", "INTEGER NOT NULL REFERENCES matter_types(id)"),
        ("name", "TEXT NOT NULL"),
        ("position", "INTEGER NOT NULL"),
        ("duration_days", "INTEGER"),
        ("auto_task_list_id", "INTEGER REFERENCES task_lists(id)"),
        ("auto_email_template", "TEXT"),
        ("auto_advance", "INTEGER NOT NULL DEFAULT 0"),
    ], True, True),
    ("matters", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("description", "TEXT"),
        ("primary_contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("matter_type_id", "INTEGER REFERENCES matter_types(id)"),
        ("matter_status_id", "INTEGER REFERENCES matter_statuses(id)"),
        ("status_entered_at", "TEXT"),
        ("priority_date", "TEXT"),
        ("preference_category", "TEXT"),
        ("chargeability_country", "TEXT"),
        ("assignee_id", "INTEGER REFERENCES users(id)"),
        ("auto_assign_tasks", "INTEGER NOT NULL DEFAULT 0"),
        ("archived_at", "TEXT"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("matter_status_history", [
        ("id", "INTEGER PRIMARY KEY"),
        ("matter_id", "INTEGER NOT NULL REFERENCES matters(id)"),
        ("from_status_id", "INTEGER REFERENCES matter_statuses(id)"),
        ("to_status_id", "INTEGER REFERENCES matter_statuses(id)"),
        ("changed_at", "TEXT NOT NULL"),
        ("changed_by", "INTEGER REFERENCES users(id)"),
    ], False, False),
    ("matter_contacts", [
        ("id", "INTEGER PRIMARY KEY"),
        ("matter_id", "INTEGER NOT NULL REFERENCES matters(id)"),
        ("contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("relationship", "TEXT"),
        ("", "UNIQUE (matter_id, contact_id)"),
    ], False, True),
    ("contact_relations", [
        ("id", "INTEGER PRIMARY KEY"),
        ("contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("related_contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("relation_type", "TEXT NOT NULL"),
        ("", "UNIQUE (contact_id, related_contact_id, relation_type)"),
    ], False, True),
    # --- users / auth / permissions ---
    ("users", [
        ("id", "INTEGER PRIMARY KEY"),
        ("email", "TEXT NOT NULL UNIQUE"),
        ("name", "TEXT NOT NULL"),
        ("password_hash", "TEXT NOT NULL"),
        ("role_label", "TEXT"),
        ("timezone", "TEXT NOT NULL DEFAULT 'America/New_York'"),
        ("is_admin", "INTEGER NOT NULL DEFAULT 0"),
        ("is_owner", "INTEGER NOT NULL DEFAULT 0"),
        ("twofa_method", "TEXT CHECK (twofa_method IN ('app','email'))"),
        ("totp_secret", "TEXT"),
        ("deactivated_at", "TEXT"),
        ("created_at", "TEXT NOT NULL"),
    ], True, True),
    ("sessions", [
        ("id", "INTEGER PRIMARY KEY"),
        ("token", "TEXT NOT NULL UNIQUE"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("created_at", "TEXT NOT NULL"),
        ("expires_at", "TEXT NOT NULL"),
        ("twofa_passed", "INTEGER NOT NULL DEFAULT 0"),
    ], False, False),
    ("password_resets", [
        ("id", "INTEGER PRIMARY KEY"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("token", "TEXT NOT NULL UNIQUE"),
        ("created_at", "TEXT NOT NULL"),
        ("used_at", "TEXT"),
    ], False, False),
    ("twofa_challenges", [
        ("id", "INTEGER PRIMARY KEY"),
        ("session_id", "INTEGER NOT NULL REFERENCES sessions(id)"),
        ("code", "TEXT NOT NULL"),
        ("created_at", "TEXT NOT NULL"),
        ("used_at", "TEXT"),
    ], False, False),
    ("user_permissions", [
        ("id", "INTEGER PRIMARY KEY"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("record_type", "TEXT NOT NULL"),
        ("level", "TEXT NOT NULL CHECK (level IN ('none','view','create','edit','delete'))"),
        ("", "UNIQUE (user_id, record_type)"),
    ], False, True),
    ("user_global_permissions", [
        ("user_id", "INTEGER PRIMARY KEY REFERENCES users(id)"),
        ("can_delete", "INTEGER NOT NULL DEFAULT 0"),
        ("can_export", "INTEGER NOT NULL DEFAULT 0"),
        ("can_archive", "INTEGER NOT NULL DEFAULT 0"),
        ("can_reassign", "INTEGER NOT NULL DEFAULT 0"),
        ("firm_settings_access", "INTEGER NOT NULL DEFAULT 1"),
    ], False, True),
    ("user_groups", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("accounting_notes_permission", "INTEGER NOT NULL DEFAULT 0"),
    ], True, True),
    ("user_group_members", [
        ("id", "INTEGER PRIMARY KEY"),
        ("group_id", "INTEGER NOT NULL REFERENCES user_groups(id)"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("", "UNIQUE (group_id, user_id)"),
    ], False, True),
    ("record_privacy", [
        ("id", "INTEGER PRIMARY KEY"),
        ("entity_type", "TEXT NOT NULL CHECK (entity_type IN ('contact','matter'))"),
        ("entity_id", "INTEGER NOT NULL"),
        ("group_id", "INTEGER NOT NULL REFERENCES user_groups(id)"),
        ("", "UNIQUE (entity_type, entity_id, group_id)"),
    ], False, True),
    # --- files / custody (invariant 5) ---
    ("folders", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("parent_id", "INTEGER REFERENCES folders(id)"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("files", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("folder_id", "INTEGER REFERENCES folders(id)"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("sha256", "TEXT NOT NULL"),
        ("size_bytes", "INTEGER NOT NULL"),
        ("stored_path", "TEXT NOT NULL"),
        ("content_type", "TEXT"),
        ("source", "TEXT NOT NULL DEFAULT 'firm' CHECK (source IN ('firm','client','produced'))"),
        ("produced_from_smart_form_id", "INTEGER REFERENCES smart_forms(id)"),
        ("uploaded_at", "TEXT NOT NULL"),
        ("uploaded_by_user_id", "INTEGER REFERENCES users(id)"),
        ("uploaded_by_contact_id", "INTEGER REFERENCES contacts(id)"),
    ], True, True),
    ("esign_files", [
        ("id", "INTEGER PRIMARY KEY"),
        ("file_id", "INTEGER NOT NULL REFERENCES files(id)"),
        ("status", "TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','requested','completed'))"),
        ("signed_file_id", "INTEGER REFERENCES files(id)"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("esign_signers", [
        ("id", "INTEGER PRIMARY KEY"),
        ("esign_file_id", "INTEGER NOT NULL REFERENCES esign_files(id)"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("user_id", "INTEGER REFERENCES users(id)"),
        ("access_token", "TEXT UNIQUE"),
        ("signed_at", "TEXT"),
    ], False, True),
    ("esign_fields", [
        ("id", "INTEGER PRIMARY KEY"),
        ("esign_file_id", "INTEGER NOT NULL REFERENCES esign_files(id)"),
        ("signer_id", "INTEGER NOT NULL REFERENCES esign_signers(id)"),
        ("field_type", "TEXT NOT NULL CHECK (field_type IN ('signature','initials','text','date'))"),
        ("page", "INTEGER NOT NULL"),
        ("x", "REAL NOT NULL"),
        ("y", "REAL NOT NULL"),
        ("value", "TEXT"),
    ], False, True),
    ("esign_events", [
        ("id", "INTEGER PRIMARY KEY"),
        ("esign_file_id", "INTEGER NOT NULL REFERENCES esign_files(id)"),
        ("signer_id", "INTEGER REFERENCES esign_signers(id)"),
        ("event", "TEXT NOT NULL"),
        ("at", "TEXT NOT NULL"),
    ], False, False),
    # --- forms engine (skeleton; evolves in Phase 2) ---
    ("form_definitions", [
        ("code", "TEXT PRIMARY KEY"),
        ("title", "TEXT NOT NULL"),
        ("agency", "TEXT NOT NULL"),
        ("efilable", "INTEGER NOT NULL DEFAULT 0"),
    ], False, True),
    ("form_editions", [
        ("id", "INTEGER PRIMARY KEY"),
        ("form_code", "TEXT NOT NULL REFERENCES form_definitions(code)"),
        ("edition", "TEXT NOT NULL"),
        ("schema_json", "TEXT NOT NULL"),
        ("is_current", "INTEGER NOT NULL DEFAULT 0"),
        ("", "UNIQUE (form_code, edition)"),
    ], False, True),
    ("smart_forms", [
        ("id", "INTEGER PRIMARY KEY"),
        ("title", "TEXT NOT NULL"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("preparer_id", "INTEGER REFERENCES users(id)"),
        ("language", "TEXT NOT NULL DEFAULT 'en'"),
        ("include_toc", "INTEGER NOT NULL DEFAULT 0"),
        ("kind", "TEXT NOT NULL DEFAULT 'standard' CHECK (kind IN ('standard','lite','custom_intake','h1b_registration'))"),
        ("custom_intake_id", "INTEGER REFERENCES custom_intakes(id)"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("smart_form_forms", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_id", "INTEGER NOT NULL REFERENCES smart_forms(id)"),
        ("form_edition_id", "INTEGER NOT NULL REFERENCES form_editions(id)"),
        ("position", "INTEGER NOT NULL"),
        ("mode", "TEXT NOT NULL DEFAULT 'paper' CHECK (mode IN ('paper','efile_package'))"),
        ("display_name", "TEXT"),
    ], False, True),
    ("form_answers", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_id", "INTEGER NOT NULL REFERENCES smart_forms(id)"),
        ("question_key", "TEXT NOT NULL"),
        ("idx", "INTEGER NOT NULL DEFAULT 0"),
        ("value", "TEXT"),
        ("updated_at", "TEXT NOT NULL"),
        ("", "UNIQUE (smart_form_id, question_key, idx)"),
    ], False, True),
    ("form_field_overrides", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_form_id", "INTEGER NOT NULL REFERENCES smart_form_forms(id)"),
        ("field", "TEXT NOT NULL"),
        ("value", "TEXT"),
        ("", "UNIQUE (smart_form_form_id, field)"),
    ], False, True),
    ("packet_parts", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_id", "INTEGER NOT NULL REFERENCES smart_forms(id)"),
        ("part_type", "TEXT NOT NULL CHECK (part_type IN ('form','file','addendum'))"),
        ("smart_form_form_id", "INTEGER REFERENCES smart_form_forms(id)"),
        ("file_id", "INTEGER REFERENCES files(id)"),
        ("position", "INTEGER NOT NULL"),
        ("display_name", "TEXT"),
    ], False, True),
    ("intake_invitations", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_id", "INTEGER NOT NULL REFERENCES smart_forms(id)"),
        ("contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("channel", "TEXT NOT NULL CHECK (channel IN ('email','link'))"),
        ("token", "TEXT NOT NULL UNIQUE"),
        ("language", "TEXT NOT NULL DEFAULT 'en'"),
        ("status", "TEXT NOT NULL DEFAULT 'sent' CHECK (status IN ('sent','accepted','returned','revoked'))"),
        ("status_at", "TEXT NOT NULL"),
        ("restricted_tabs", "TEXT"),
        ("message", "TEXT"),
    ], False, True),
    ("question_settings", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_id", "INTEGER NOT NULL REFERENCES smart_forms(id)"),
        ("question_key", "TEXT NOT NULL"),
        ("hidden", "INTEGER NOT NULL DEFAULT 0"),
        ("flagged", "INTEGER NOT NULL DEFAULT 0"),
        ("", "UNIQUE (smart_form_id, question_key)"),
    ], False, True),
    ("question_comments", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_id", "INTEGER NOT NULL REFERENCES smart_forms(id)"),
        ("question_key", "TEXT NOT NULL"),
        ("author_type", "TEXT NOT NULL CHECK (author_type IN ('user','contact'))"),
        ("author_id", "INTEGER NOT NULL"),
        ("body", "TEXT NOT NULL"),
        ("created_at", "TEXT NOT NULL"),
    ], False, True),
    ("custom_intakes", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("created_at", "TEXT NOT NULL"),
    ], True, True),
    ("custom_intake_tabs", [
        ("id", "INTEGER PRIMARY KEY"),
        ("custom_intake_id", "INTEGER NOT NULL REFERENCES custom_intakes(id)"),
        ("name", "TEXT NOT NULL"),
        ("position", "INTEGER NOT NULL"),
        ("", "UNIQUE (custom_intake_id, name)"),
    ], False, True),
    ("custom_questions", [
        ("id", "INTEGER PRIMARY KEY"),
        ("prompt", "TEXT NOT NULL"),
        ("qtype", "TEXT NOT NULL CHECK (qtype IN ('text','textarea','number','date','boolean','list','expiry','document_request','premade'))"),
        ("save_to_fact_key", "TEXT REFERENCES fact_definitions(key)"),
        ("list_options", "TEXT"),
    ], True, True),
    ("custom_intake_questions", [
        ("id", "INTEGER PRIMARY KEY"),
        ("custom_intake_id", "INTEGER NOT NULL REFERENCES custom_intakes(id)"),
        ("tab_id", "INTEGER REFERENCES custom_intake_tabs(id)"),
        ("question_id", "INTEGER NOT NULL REFERENCES custom_questions(id)"),
        ("position", "INTEGER NOT NULL"),
    ], False, True),
    ("matter_type_forms", [
        ("id", "INTEGER PRIMARY KEY"),
        ("matter_type_id", "INTEGER NOT NULL REFERENCES matter_types(id)"),
        ("form_code", "TEXT NOT NULL REFERENCES form_definitions(code)"),
        ("position", "INTEGER NOT NULL"),
        ("", "UNIQUE (matter_type_id, form_code)"),
    ], False, True),
    ("smart_form_contacts", [
        ("id", "INTEGER PRIMARY KEY"),
        ("smart_form_id", "INTEGER NOT NULL REFERENCES smart_forms(id)"),
        ("role", "TEXT NOT NULL"),
        ("contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("", "UNIQUE (smart_form_id, role)"),
    ], False, True),
    ("form_collections", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
    ], True, True),
    ("form_collection_forms", [
        ("id", "INTEGER PRIMARY KEY"),
        ("collection_id", "INTEGER NOT NULL REFERENCES form_collections(id)"),
        ("form_code", "TEXT NOT NULL REFERENCES form_definitions(code)"),
    ], False, True),
    ("intake_templates", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("config_json", "TEXT NOT NULL"),
        ("created_at", "TEXT NOT NULL"),
    ], True, True),
    # --- template automation ---
    ("doc_templates", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("stored_path", "TEXT NOT NULL"),
        ("created_at", "TEXT NOT NULL"),
    ], True, True),
    # --- tasks ---
    ("tasks", [
        ("id", "INTEGER PRIMARY KEY"),
        ("title", "TEXT NOT NULL"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("due_date", "TEXT"),
        ("completed_at", "TEXT"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("task_assignees", [
        ("id", "INTEGER PRIMARY KEY"),
        ("task_id", "INTEGER NOT NULL REFERENCES tasks(id)"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("", "UNIQUE (task_id, user_id)"),
    ], False, True),
    ("task_lists", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
    ], True, True),
    ("task_list_items", [
        ("id", "INTEGER PRIMARY KEY"),
        ("task_list_id", "INTEGER NOT NULL REFERENCES task_lists(id)"),
        ("title", "TEXT NOT NULL"),
        ("position", "INTEGER NOT NULL"),
        ("duration_days", "INTEGER"),
        ("ref_fact_key", "TEXT REFERENCES fact_definitions(key)"),
        ("ref_direction", "TEXT CHECK (ref_direction IN ('before','after'))"),
        ("ref_days", "INTEGER"),
        ("default_assignee_id", "INTEGER REFERENCES users(id)"),
    ], False, True),
    # --- notes ---
    ("note_categories", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("builtin", "INTEGER NOT NULL DEFAULT 0"),
    ], True, True),
    ("notes", [
        ("id", "INTEGER PRIMARY KEY"),
        ("title", "TEXT"),
        ("body", "TEXT NOT NULL"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("category_id", "INTEGER REFERENCES note_categories(id)"),
        ("pinned", "INTEGER NOT NULL DEFAULT 0"),
        ("notify_all", "INTEGER NOT NULL DEFAULT 0"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("note_assignees", [
        ("id", "INTEGER PRIMARY KEY"),
        ("note_id", "INTEGER NOT NULL REFERENCES notes(id)"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("", "UNIQUE (note_id, user_id)"),
    ], False, True),
    # --- events / deadlines ---
    ("events", [
        ("id", "INTEGER PRIMARY KEY"),
        ("title", "TEXT NOT NULL"),
        ("description", "TEXT"),
        ("starts_at", "TEXT NOT NULL"),
        ("ends_at", "TEXT"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("source", "TEXT NOT NULL DEFAULT 'manual' CHECK (source IN ('manual','expiry_auto'))"),
        ("source_fact_id", "INTEGER REFERENCES facts(id)"),
        ("created_at", "TEXT NOT NULL"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("event_attendees", [
        ("id", "INTEGER PRIMARY KEY"),
        ("event_id", "INTEGER NOT NULL REFERENCES events(id)"),
        ("user_id", "INTEGER REFERENCES users(id)"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
    ], False, True),
    ("event_reminders", [
        ("id", "INTEGER PRIMARY KEY"),
        ("event_id", "INTEGER NOT NULL REFERENCES events(id)"),
        ("offset_value", "INTEGER NOT NULL"),
        ("offset_unit", "TEXT NOT NULL CHECK (offset_unit IN ('minutes','hours','days','weeks','months'))"),
        ("channel", "TEXT NOT NULL DEFAULT 'email'"),
        ("fired_at", "TEXT"),
    ], False, True),
    ("expiry_reminder_settings", [
        ("id", "INTEGER PRIMARY KEY"),
        ("fact_key", "TEXT NOT NULL REFERENCES fact_definitions(key)"),
        ("lead_days", "INTEGER NOT NULL"),
        ("recipients", "TEXT NOT NULL CHECK (recipients IN ('admin','all','assignees'))"),
        ("include_client", "INTEGER NOT NULL DEFAULT 0"),
    ], False, True),
    # --- case tracking ---
    ("matter_receipts", [
        ("id", "INTEGER PRIMARY KEY"),
        ("matter_id", "INTEGER NOT NULL REFERENCES matters(id)"),
        ("receipt_number", "TEXT NOT NULL"),
        ("description", "TEXT"),
        ("current_status", "TEXT"),
        ("status_as_of", "TEXT"),
        ("last_checked_at", "TEXT"),
    ], True, True),
    ("receipt_status_history", [
        ("id", "INTEGER PRIMARY KEY"),
        ("matter_receipt_id", "INTEGER NOT NULL REFERENCES matter_receipts(id)"),
        ("status", "TEXT NOT NULL"),
        ("recorded_at", "TEXT NOT NULL"),
        ("check_kind", "TEXT NOT NULL CHECK (check_kind IN ('manual','scheduled'))"),
    ], False, False),
    ("uscis_responses", [
        ("id", "INTEGER PRIMARY KEY"),
        ("receipt_number", "TEXT NOT NULL"),
        ("status", "TEXT NOT NULL"),
        ("as_of", "TEXT NOT NULL"),
    ], False, False),
    ("visa_bulletin", [
        ("id", "INTEGER PRIMARY KEY"),
        ("bulletin_month", "TEXT NOT NULL"),
        ("chart", "TEXT NOT NULL CHECK (chart IN ('filing','final_action'))"),
        ("preference_category", "TEXT NOT NULL"),
        ("chargeability", "TEXT NOT NULL"),
        ("cutoff_date", "TEXT"),
        ("", "UNIQUE (bulletin_month, chart, preference_category, chargeability)"),
    ], False, False),
    # --- notifications / outbox ---
    ("notifications", [
        ("id", "INTEGER PRIMARY KEY"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("kind", "TEXT NOT NULL"),
        ("payload", "TEXT"),
        ("created_at", "TEXT NOT NULL"),
        ("read_at", "TEXT"),
    ], False, False),
    ("email_outbox", [
        ("id", "INTEGER PRIMARY KEY"),
        ("recipient", "TEXT NOT NULL"),
        ("subject", "TEXT NOT NULL"),
        ("body", "TEXT NOT NULL"),
        ("template", "TEXT"),
        ("entity_type", "TEXT"),
        ("entity_id", "INTEGER"),
        ("created_at", "TEXT NOT NULL"),
        ("sent_at", "TEXT"),
    ], False, False),
    # --- settings / misc ---
    ("firm_settings", [
        ("key", "TEXT PRIMARY KEY"),
        ("value", "TEXT NOT NULL"),
    ], False, True),
    ("user_settings", [
        ("id", "INTEGER PRIMARY KEY"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("key", "TEXT NOT NULL"),
        ("value", "TEXT NOT NULL"),
        ("", "UNIQUE (user_id, key)"),
    ], False, True),
    ("record_access", [
        ("id", "INTEGER PRIMARY KEY"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("entity_type", "TEXT NOT NULL CHECK (entity_type IN ('contact','matter'))"),
        ("entity_id", "INTEGER NOT NULL"),
        ("at", "TEXT NOT NULL"),
    ], False, False),
    ("synthetic_marker", [
        ("marker", "TEXT PRIMARY KEY"),
    ], False, False),
    # --- billing / trust ledger (casework-billing child, P0 gate
    # ratified 2026-08-03; paper design:
    # ../../casework-billing/design/ledger-design.md). Trust funds are
    # LIABILITIES (client_trust/matter_trust sub-accounts under a
    # trust_bank control); journal is append-only with one clearing
    # exception -- see BILLING_EXTRA_SQL triggers. ---
    ("ledger_accounts", [
        ("id", "INTEGER PRIMARY KEY"),
        ("kind", "TEXT NOT NULL CHECK (kind IN ('operating_bank','trust_bank','client_trust','matter_trust','fee_income','processor_fee_expense','chargeback_expense'))"),
        ("name", "TEXT NOT NULL"),
        ("parent_id", "INTEGER REFERENCES ledger_accounts(id)"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("created_by", "INTEGER REFERENCES users(id)"),
        ("", "CHECK (kind != 'client_trust' OR (contact_id IS NOT NULL AND parent_id IS NOT NULL))"),
        ("", "CHECK (kind != 'matter_trust' OR (matter_id IS NOT NULL AND parent_id IS NOT NULL))"),
        ("", "CHECK (kind NOT IN ('operating_bank','trust_bank','fee_income','processor_fee_expense','chargeback_expense') OR parent_id IS NULL)"),
    ], True, True),
    ("external_events", [
        ("id", "INTEGER PRIMARY KEY"),
        ("event_type", "TEXT NOT NULL CHECK (event_type IN ('deposit','check_cut','processor_batch','chargeback'))"),
        ("bank_account_id", "INTEGER NOT NULL REFERENCES ledger_accounts(id)"),
        ("occurred_on", "TEXT NOT NULL"),
        ("amount_cents", "INTEGER NOT NULL CHECK (amount_cents > 0)"),
        ("direction", "TEXT NOT NULL CHECK (direction IN ('in','out'))"),
        ("counterparty", "TEXT"),
        ("memo", "TEXT"),
        ("invoice_id", "INTEGER"),
        ("payment_id", "INTEGER"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
    ], False, True),
    ("journal_entries", [
        ("id", "INTEGER PRIMARY KEY"),
        ("kind", "TEXT NOT NULL CHECK (kind IN ('trust_deposit','bill_direct_payment','earn_out','disbursement','sim_settlement','processor_fee','chargeback','reversal'))"),
        ("memo", "TEXT"),
        ("invoice_id", "INTEGER"),
        ("payment_id", "INTEGER"),
        ("external_event_id", "INTEGER REFERENCES external_events(id)"),
        ("reverses_entry_id", "INTEGER REFERENCES journal_entries(id)"),
        ("replaces_entry_id", "INTEGER REFERENCES journal_entries(id)"),
        ("posted_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("posted_by", "INTEGER REFERENCES users(id)"),
    ], False, True),
    ("journal_postings", [
        ("id", "INTEGER PRIMARY KEY"),
        ("entry_id", "INTEGER NOT NULL REFERENCES journal_entries(id)"),
        ("account_id", "INTEGER NOT NULL REFERENCES ledger_accounts(id)"),
        ("side", "TEXT NOT NULL CHECK (side IN ('debit','credit'))"),
        ("amount_cents", "INTEGER NOT NULL CHECK (amount_cents > 0)"),
        ("cleared_at", "TEXT"),
        ("statement_ref", "TEXT"),
    ], False, True),
    # period_closes: the hard month-end close (billing-ui
    # period-close.md, ratified 2026-08-09; program amendment same
    # date). One live (non-void) row per period, enforced in
    # app/period.py; months close in strict order. snapshot is the
    # canonical-JSON close record frozen at prepare and verified
    # unchanged at approve (PC2 stale-prepare control).
    ("period_closes", [
        ("id", "INTEGER PRIMARY KEY"),
        ("period", "TEXT NOT NULL CHECK (period GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]')"),
        ("status", "TEXT NOT NULL CHECK (status IN ('prepared','closed','void'))"),
        ("prepared_by", "INTEGER NOT NULL REFERENCES users(id)"),
        ("prepared_at", "TEXT NOT NULL"),
        ("approved_by", "INTEGER REFERENCES users(id)"),
        ("approved_at", "TEXT"),
        ("snapshot", "TEXT NOT NULL"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("", "CHECK (status != 'closed' OR (approved_by IS NOT NULL AND approved_at IS NOT NULL))"),
    ], False, True),
    ("time_entries", [
        ("id", "INTEGER PRIMARY KEY"),
        ("user_id", "INTEGER NOT NULL REFERENCES users(id)"),
        ("contact_id", "INTEGER REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("entry_date", "TEXT NOT NULL"),
        ("description", "TEXT"),
        ("duration_seconds", "INTEGER NOT NULL DEFAULT 0 CHECK (duration_seconds >= 0)"),
        ("rate_cents_per_hour", "INTEGER CHECK (rate_cents_per_hour >= 0)"),
        ("timer_started_at", "TEXT"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("", "CHECK (contact_id IS NOT NULL OR matter_id IS NOT NULL)"),
    ], True, True),
    ("invoices", [
        ("id", "INTEGER PRIMARY KEY"),
        ("invoice_type", "TEXT NOT NULL CHECK (invoice_type IN ('bill','trust_request'))"),
        ("contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("recipient_contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("trust_level", "TEXT CHECK (trust_level IN ('client','matter'))"),
        ("trust_account_id", "INTEGER REFERENCES ledger_accounts(id)"),
        ("number", "INTEGER NOT NULL"),
        ("number_scope", "TEXT NOT NULL CHECK (number_scope IN ('client','global'))"),
        ("display_code", "TEXT NOT NULL CHECK (display_code GLOB '[BT][0-9][0-9][0-9][0-9]*')"),
        ("code_scope", "TEXT NOT NULL CHECK (code_scope IN ('client','global'))"),
        ("preparer_user_id", "INTEGER REFERENCES users(id)"),
        ("issued_date", "TEXT"),
        ("due_date", "TEXT"),
        ("discount_cents", "INTEGER NOT NULL DEFAULT 0 CHECK (discount_cents >= 0)"),
        ("footer", "TEXT"),
        ("color_scheme", "TEXT"),
        ("language", "TEXT NOT NULL DEFAULT 'en' CHECK (language IN ('en','es'))"),
        ("late_fee_enabled", "INTEGER NOT NULL DEFAULT 0"),
        ("late_fee_kind", "TEXT CHECK (late_fee_kind IN ('fixed','percent'))"),
        ("late_fee_value", "INTEGER"),
        ("late_fee_recurring", "INTEGER NOT NULL DEFAULT 0"),
        ("late_fee_recur_days", "INTEGER"),
        ("reminder_enabled", "INTEGER NOT NULL DEFAULT 0"),
        ("reminder_days", "INTEGER"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("created_by", "INTEGER REFERENCES users(id)"),
        ("", "CHECK (invoice_type != 'trust_request' OR (trust_level IS NOT NULL AND trust_account_id IS NOT NULL))"),
    ], True, True),
    ("invoice_charges", [
        ("id", "INTEGER PRIMARY KEY"),
        ("invoice_id", "INTEGER NOT NULL REFERENCES invoices(id)"),
        ("charge_type", "TEXT NOT NULL CHECK (charge_type IN ('service','expense'))"),
        ("description", "TEXT NOT NULL"),
        ("amount_cents", "INTEGER NOT NULL CHECK (amount_cents >= 0)"),
        ("charge_date", "TEXT"),
        ("matter_id", "INTEGER REFERENCES matters(id)"),
        ("source", "TEXT NOT NULL DEFAULT 'manual' CHECK (source IN ('manual','saved','time','late_fee'))"),
        ("time_entry_id", "INTEGER REFERENCES time_entries(id)"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("saved_charges", [
        ("id", "INTEGER PRIMARY KEY"),
        ("description", "TEXT NOT NULL"),
        ("amount_cents", "INTEGER NOT NULL CHECK (amount_cents >= 0)"),
        ("charge_type", "TEXT NOT NULL CHECK (charge_type IN ('service','expense'))"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("invoice_payments", [
        ("id", "INTEGER PRIMARY KEY"),
        ("invoice_id", "INTEGER NOT NULL REFERENCES invoices(id)"),
        ("method", "TEXT NOT NULL CHECK (method IN ('direct','trust_transfer','sim_card','sim_echeck'))"),
        ("amount_cents", "INTEGER NOT NULL CHECK (amount_cents > 0)"),
        ("payment_date", "TEXT NOT NULL"),
        ("note", "TEXT"),
        ("destination_account_id", "INTEGER REFERENCES ledger_accounts(id)"),
        ("source_trust_level", "TEXT CHECK (source_trust_level IN ('client','matter'))"),
        ("source_account_id", "INTEGER REFERENCES ledger_accounts(id)"),
        ("associated_charge_id", "INTEGER REFERENCES invoice_charges(id)"),
        ("refunded", "INTEGER NOT NULL DEFAULT 0"),
        ("refund_note", "TEXT"),
        ("journal_entry_id", "INTEGER REFERENCES journal_entries(id)"),
        ("processor_txn_id", "INTEGER REFERENCES processor_transactions(id)"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("created_by", "INTEGER REFERENCES users(id)"),
        ("", "CHECK (method != 'trust_transfer' OR (source_trust_level IS NOT NULL AND source_account_id IS NOT NULL))"),
    ], True, True),
    ("payment_plans", [
        ("id", "INTEGER PRIMARY KEY"),
        ("invoice_id", "INTEGER NOT NULL REFERENCES invoices(id)"),
        ("frequency_days", "INTEGER NOT NULL CHECK (frequency_days > 0)"),
        ("installment_cents", "INTEGER NOT NULL CHECK (installment_cents > 0)"),
        ("start_date", "TEXT NOT NULL"),
        ("auto_charge", "INTEGER NOT NULL DEFAULT 0"),
        ("accepted_forms", "TEXT NOT NULL DEFAULT 'card,echeck'"),
        ("active", "INTEGER NOT NULL DEFAULT 1"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("plan_installments", [
        ("id", "INTEGER PRIMARY KEY"),
        ("plan_id", "INTEGER NOT NULL REFERENCES payment_plans(id)"),
        ("due_date", "TEXT NOT NULL"),
        ("amount_cents", "INTEGER NOT NULL CHECK (amount_cents > 0)"),
        ("pre_reminder_at", "TEXT"),
        ("due_reminder_at", "TEXT"),
        ("post_reminder_at", "TEXT"),
        ("paid_payment_id", "INTEGER REFERENCES invoice_payments(id)"),
    ], False, True),
    ("invoice_shares", [
        ("id", "INTEGER PRIMARY KEY"),
        ("invoice_id", "INTEGER NOT NULL REFERENCES invoices(id)"),
        ("recipient_contact_id", "INTEGER NOT NULL REFERENCES contacts(id)"),
        ("channel", "TEXT NOT NULL DEFAULT 'email' CHECK (channel IN ('email'))"),
        ("token", "TEXT NOT NULL UNIQUE"),
        ("reminders_enabled", "INTEGER NOT NULL DEFAULT 0"),
        ("reminder_days", "INTEGER"),
        ("last_reminder_at", "TEXT"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
        ("created_by", "INTEGER REFERENCES users(id)"),
    ], True, True),
    ("settlement_batches", [
        ("id", "INTEGER PRIMARY KEY"),
        ("settle_date", "TEXT NOT NULL"),
        ("bank_account_id", "INTEGER NOT NULL REFERENCES ledger_accounts(id)"),
        ("mode", "TEXT NOT NULL CHECK (mode IN ('gross','net'))"),
        ("gross_cents", "INTEGER NOT NULL CHECK (gross_cents >= 0)"),
        ("fee_cents", "INTEGER NOT NULL CHECK (fee_cents >= 0)"),
        ("net_cents", "INTEGER NOT NULL CHECK (net_cents >= 0)"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
    ], False, True),
    ("processor_transactions", [
        ("id", "INTEGER PRIMARY KEY"),
        ("kind", "TEXT NOT NULL CHECK (kind IN ('charge','echeck','refund','chargeback'))"),
        ("token", "TEXT NOT NULL CHECK (token LIKE 'SYNTHETIC-%')"),
        ("amount_cents", "INTEGER NOT NULL CHECK (amount_cents > 0)"),
        ("fee_cents", "INTEGER NOT NULL DEFAULT 0 CHECK (fee_cents >= 0)"),
        ("status", "TEXT NOT NULL CHECK (status IN ('approved','declined','settled','charged_back'))"),
        ("batch_id", "INTEGER REFERENCES settlement_batches(id)"),
        ("invoice_payment_id", "INTEGER"),
        ("created_at", "TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))"),
    ], False, True),
]

SOFT_DELETE_COLS = [("deleted_at", "TEXT"), ("deleted_by", "INTEGER REFERENCES users(id)")]

# Append-only surface (gate ruling 9): never DELETEd by anyone, purge
# layer included. Declared here beside TABLES so the soft-delete sweep
# derives its rules from the schema authority and cannot drift.
APPEND_ONLY = {"audit_log", "matter_status_history", "receipt_status_history",
               "esign_events", "record_access", "synthetic_marker",
               # billing (P0 gate 2026-08-03): journal corrects by
               # reversal, never mutates; events are the bank's witness.
               "journal_entries", "journal_postings", "external_events"}

# Billing ledger extras (P0 gate 2026-08-03): sub-ledger uniqueness and
# the immutability wall. Journal and external_events refuse UPDATE and
# DELETE at the schema layer; the single exception is a posting's
# clearing annotation moving from NULL to a value exactly once (F8 /
# ledger-design.md section 2).
BILLING_EXTRA_SQL = """
CREATE INDEX idx_ledger_accounts_parent ON ledger_accounts (parent_id);
CREATE UNIQUE INDEX uq_client_trust ON ledger_accounts (parent_id, contact_id)
  WHERE kind = 'client_trust' AND deleted_at IS NULL;
CREATE UNIQUE INDEX uq_matter_trust ON ledger_accounts (parent_id, matter_id)
  WHERE kind = 'matter_trust' AND deleted_at IS NULL;
CREATE INDEX idx_postings_entry ON journal_postings (entry_id);
CREATE INDEX idx_postings_account ON journal_postings (account_id);

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
CREATE TRIGGER trg_external_events_no_update BEFORE UPDATE ON external_events
BEGIN SELECT RAISE(ABORT, 'external_events is append-only'); END;
CREATE TRIGGER trg_external_events_no_delete BEFORE DELETE ON external_events
BEGIN SELECT RAISE(ABORT, 'external_events is append-only'); END;
"""

AUDIT_LOG_DDL = """CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY,
  at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  actor_type TEXT NOT NULL,
  actor_id INTEGER,
  action TEXT NOT NULL CHECK (action IN ('insert','update','delete')),
  entity_type TEXT NOT NULL,
  entity_id INTEGER NOT NULL,
  changes TEXT
);"""

FEED_TYPES = "'contacts','matters','smart_forms','tasks','notes','events','files'"


def cols_of(table_cols):
    return [c for c, _ in table_cols if c]


def json_obj(prefix, names):
    parts = ", ".join(f"'{n}', {prefix}.{n}" for n in names)
    return f"json_object({parts})"


def triggers_for(name, names):
    key = "rowid" if not any(n == "id" for n in names) else "id"
    actor = "casework_actor_type(), casework_actor_id()"
    return f"""
CREATE TRIGGER trg_{name}_ai AFTER INSERT ON {name} BEGIN
  INSERT INTO audit_log (actor_type, actor_id, action, entity_type, entity_id, changes)
  VALUES ({actor}, 'insert', '{name}', NEW.{key}, {json_obj('NEW', names)});
END;
CREATE TRIGGER trg_{name}_au AFTER UPDATE ON {name} BEGIN
  INSERT INTO audit_log (actor_type, actor_id, action, entity_type, entity_id, changes)
  VALUES ({actor}, 'update', '{name}', NEW.{key}, json_object('old', {json_obj('OLD', names)}, 'new', {json_obj('NEW', names)}));
END;
CREATE TRIGGER trg_{name}_ad AFTER DELETE ON {name} BEGIN
  INSERT INTO audit_log (actor_type, actor_id, action, entity_type, entity_id, changes)
  VALUES ({actor}, 'delete', '{name}', OLD.{key}, {json_obj('OLD', names)});
END;
"""


def generate():
    out = ["-- GENERATED by gen_schema.py -- do not hand-edit.",
           "-- Requires per-connection functions casework_actor_type()/casework_actor_id()",
           "-- (registered by the app; see app/db.py). PRAGMA foreign_keys=ON per connection.",
           "", AUDIT_LOG_DDL, ""]
    for name, tcols, soft, audited in TABLES:
        cols = list(tcols)
        if soft:
            # column defs must precede table-level ("", ...) constraints
            real = [c for c in cols if c[0]]
            constraints = [c for c in cols if not c[0]]
            cols = real + SOFT_DELETE_COLS + constraints
        body = ",\n  ".join((f"{c} {ddl}" if c else ddl) for c, ddl in cols)
        out.append(f"CREATE TABLE {name} (\n  {body}\n);")
        if soft:
            out.append(f"CREATE INDEX idx_{name}_trash ON {name} (deleted_at) WHERE deleted_at IS NOT NULL;")
        if audited:
            out.append(triggers_for(name, cols_of(cols)))
        out.append("")
    out.append(BILLING_EXTRA_SQL)
    # semantic_action (gate ruling 8): soft-delete/restore live in the
    # changes JSON as deleted_at transitions; this view derives the label
    # ONCE so no consumer hand-rolls the JSON rule (WHERE action='delete'
    # alone misses every soft delete -- always filter on semantic_action).
    out.append(f"""CREATE VIEW activity_feed AS
  SELECT id, at, actor_type, actor_id, action, entity_type, entity_id, changes,
    CASE
      WHEN action = 'update'
        AND json_extract(changes, '$.old.deleted_at') IS NULL
        AND json_extract(changes, '$.new.deleted_at') IS NOT NULL
        THEN 'soft_delete'
      WHEN action = 'update'
        AND json_extract(changes, '$.old.deleted_at') IS NOT NULL
        AND json_extract(changes, '$.new.deleted_at') IS NULL
        THEN 'restore'
      ELSE action
    END AS semantic_action
  FROM audit_log
  WHERE entity_type IN ({FEED_TYPES});
""")
    return "\n".join(out)


if __name__ == "__main__":
    target = Path(__file__).parent / "schema.sql"
    target.write_text(generate(), encoding="utf-8", newline="\n")
    print(f"wrote {target} ({len(generate().splitlines())} lines)")
