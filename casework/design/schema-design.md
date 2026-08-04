# schema design note -- U0.2 (paper design before DDL)

2026-08-01. Maps each goal.md invariant to its enforcing structure.
The DDL authority is app/schema/gen_schema.py (generator); schema.sql
is generated output, never hand-edited. Invariant-bearing tables are
FROZEN at the U0.5 gate; other tables evolve freely inside phases.

## Invariant 1: single fact store

A client/case fact is entered once and flows to every consumer.

- fact_definitions: the fact vocabulary. Columns: key (pk, e.g.
  'bio.family_name', 'imm.a_number', 'imm.vmax_date'), subject_type
  (contact|matter), value_type (text|number|date|boolean|list|expiry),
  label, is_custom (0 built-in, 1 firm-defined custom attribute),
  repeating (0/1 -- children, addresses, trips).
- facts: the single store. Columns: id, subject_type, subject_id,
  key -> fact_definitions, idx (repeating-group instance, default 0),
  value (text-encoded by value_type). UNIQUE(subject_type, subject_id,
  key, idx).
- CONSUMERS NEVER COPY: form instances store only petition-specific
  answers (form_answers); answers to contact-fact questions write
  through to facts. Merge tags resolve fact keys. Deadline machinery
  (expiry dates, VMAX, priority date) reads fact keys. PDF-view manual
  edits are per-instance OVERRIDES (form_field_overrides), a deliberate
  divergence layer, not a copy -- Sync Database Values clears them.
- Custom attributes = fact_definitions rows with is_custom=1, key
  namespaced 'custom.<slug>'. No separate custom-attribute value table.
- ENFORCEMENT (fact-store lint, supporting check): form_answers may
  contain no question key that maps to a fact_definitions key; the
  form-field mapping table decides routing at write time, and the lint
  asserts the disjointness on the seeded db.
- NAME MODEL (gate ruling 7). Four layers, never collapsed:
  1. Component atoms are the stored facts (bio.given_name,
     bio.middle_name, bio.family_name, suffix). Direction of
     derivation is the load-bearing rule: composites are always
     derived from atoms, never stored as authority -- you can compose
     "Family, Given M." from atoms but cannot reliably parse atoms
     back out of a composed string. contacts.display_name is the one
     acknowledged derived label, app-composed from name atoms for
     persons; a cache, never a source.
  2. Distinct name identities are distinct fact keys, not formats:
     name-as-on-green-card, other names used since birth, maiden
     name, native-alphabet name. Repeating composite groups (each
     other-name has given+middle+family) are sibling keys sharing the
     same idx; the idx aligns the group instance across keys.
  3. Formatting variants (middle initial, ordering, capitalization)
     are merge-tag transforms applied at resolution time, never
     stored. A form without a middle-name field simply does not
     consume the key.
  4. Per-filing divergence (e.g. deliberately matching a prior
     filing's typo) is form_field_overrides: per-instance, audited,
     cleared by Sync Database Values.

## Invariant 2: matter registry

- REGISTRY COLUMNS ARE MECHANICS ONLY (gate ruling 7): contacts
  carries kind, display_name (derived label -- see Name model),
  archived_at, and audit/tombstone columns. Fact-like data (email,
  phone, A-number, firm unique identifier) lives in the fact store
  (contact.email, contact.phone, imm.a_number, meta.unique_identifier)
  so form fill, merge tags, and deadline machinery keep a single read
  path.
- contacts (person|company, display_name, archived_at), matters (name,
  primary contact FK, type FK, status FK, priority_date, preference
  category, assignee, archived_at), matter_types, matter_statuses
  (ordered per type, optional duration_days, automation config),
  matter_status_history (who/when/from/to -- feeds the progress bar
  and late computation), matter_contacts (additional linked contacts
  with relationship title), contact_relations (person-person,
  person-company relations, mirrored on both sides by read, stored
  once).
- Archiving (contact-archiving, matter-archiving entries) is a state
  column (archived_at), distinct from soft delete: archived records
  are a working-set filter; deleted records are in the trash can.

## Invariant 3: audit trail (who/what/when on every mutation)

- audit_log: id, at (utc), actor_type (user|contact|system), actor_id,
  action (insert|update|delete -- the PHYSICAL vocabulary, gate ruling
  8), entity_type, entity_id, changes (json: full old/new objects on
  update). Soft delete and restore are updates physically; their
  semantic labels derive from the deleted_at transition in the changes
  json and are computed ONCE in the activity_feed view
  (semantic_action: insert|update|soft_delete|restore|delete). No
  consumer may hand-roll an action filter -- WHERE action='delete'
  alone misses every soft delete; filter on semantic_action.
- ENFORCEMENT IS SCHEMA-LEVEL, NOT DISCIPLINE (as built, gate ruling
  8): the generator emits AFTER INSERT/UPDATE/DELETE triggers for
  every audited table. The acting user comes from per-connection
  SQLite functions casework_actor_type()/casework_actor_id(),
  registered by app/db.py connect() at connection time. A raw
  connection without those functions cannot mutate an audited table
  at all -- the trigger call fails. No unaudited mutation path
  exists; there is no degraded-attribution fallback. (An earlier
  _actor temp-table design with 'system' fallback was discarded on
  paper; this paragraph describes what is built.)
- The activity feed (contacts-and-matters.activity-feeds) is a VIEW
  over audit_log filtered to in-scope entity types, carrying the
  semantic_action derivation above -- no second event table
  (single-fact-store principle applied to events themselves).

## Invariant 4: soft delete everywhere (trash can)

- Every user-visible record table carries deleted_at, deleted_by.
  The generator enforces presence: record tables are declared with
  soft_delete=True and the columns + a partial index are emitted
  mechanically. Restore = clearing the tombstone (audited).
- DELETE VOCABULARY (gate ruling 9): records go to the trash can;
  values and links do not. Tombstoned tables are purge-only (no app
  DELETE, ever; purge layer empty in v1). Non-tombstoned tables
  (facts, join/child rows) take sanctioned hard deletes -- audited
  with full old/new json, recoverable by query, not trash-restorable.
  Append-only surface (audit_log, matter_status_history,
  receipt_status_history, esign_events, synthetic_marker) is never
  deleted by anyone, purge included. The soft-delete sweep derives
  all three rules from gen_schema.py's own declarations (soft_delete
  flags + APPEND_ONLY), so sweep and schema cannot disagree;
  unparseable or unknown DELETE targets fail the sweep loudly.
  SQLite-level deletes by triggers/cascades are avoided: FKs use
  RESTRICT, not CASCADE, so a tombstoned parent never silently
  removes children.

## Invariant 5: document production and custody

- files (name, folder FK, contact FK, matter FK, sha256, size, stored
  path under a content-addressed files/ dir, uploaded_by, source
  firm|client), folders (name, parent FK, contact FK, matter FK).
- e-signature subsystem: esign_files (file FK, status), esign_signers
  (esign_file FK, contact-or-user, order), esign_fields (type
  signature|initials|text|date, page, x, y, signer FK), esign_events
  (requested/viewed/signed timestamps -- custody chain), signed output
  saved as a NEW file row (original preserved).
- Form production: form_instances + packets (ordered parts: form,
  file, addendum; toc flag) -> produced artifacts saved as file rows
  with provenance (produced_from instance FK).

## Invariant 6: accountability record

- Covered by audit_log + esign_events + matter_status_history +
  outbox (below). No separate structure needed.

## Cross-cutting decisions

- EMAIL IS AN OUTBOX, NEVER A SOCKET: email_outbox (recipient,
  subject, body, template, related entity, created_at, sent_at NULL
  in v1). Tests assert outbox rows; real SMTP delivery is deployment
  config, post-v1, approval-gated (network beyond localhost). In-app
  notifications: notifications table (user FK, type, payload, read_at).
- REPLAY ADAPTERS ARE TABLES: uscis_responses (receipt_number,
  status, as_of) and visa_bulletin (bulletin_month, category, country,
  filing_cutoff, final_action_cutoff) hold captured/synthetic
  datasets; the adapter reads them. Live fetchers are post-v1.
- AUTH: users (email, password_hash, timezone, role_label, totp
  secret, twofa_method app|email, deactivated_at), sessions (token,
  user FK, expires), password_resets, twofa_challenges. Real password
  auth (bcrypt/argon2 via passlib or hashlib.scrypt -- stdlib scrypt
  preferred, zero new deps).
- PERMISSIONS: user_permissions (user FK, record_type, level
  none|view|create|edit|delete) + global flags (can_delete, can_export,
  can_archive, can_reassign, is_admin); user_groups + user_group_members
  + record_privacy (entity, group FK) for private contacts/matters.
- SYNTHETIC MARKER: db-level table synthetic_marker(marker TEXT) must
  contain 'SYNTHETIC'; every seed writes it; the synthetic-data guard
  fails any db/seed lacking it. Seed contacts additionally carry
  fact 'meta.synthetic' = 'true'.
- IDs: INTEGER PRIMARY KEY (rowid). Timestamps TEXT ISO-8601 UTC.
  SQLite PRAGMA foreign_keys=ON at every connection.

## Invariant-bearing surface (FROZEN at the U0.5 gate, rulings 6-10)

- fact_definitions, facts, and the Name model (atoms stored,
  composites derived, identities as distinct keys, formats as
  transforms, divergence as overrides)
- contacts under the registry-mechanics-only boundary (fact-like
  data lives in the fact store; display_name is the acknowledged
  derived label)
- matters, matter_types, matter_statuses, matter_status_history,
  matter_contacts, contact_relations
- audit_log + the generated trigger scheme + the actor-function
  protocol (casework_actor_type/casework_actor_id, fail-loudly) +
  the semantic_action derivation in activity_feed
- users
- the soft-delete column contract on all record tables, and the
  delete vocabulary (tombstoned purge-only / non-tombstoned
  sanctioned hard delete / append-only never), with sweep rules
  derived from generator declarations

Frozen rules bind like frozen tables: a frozen table with
renegotiable semantics is not frozen.

Deferred, logged as known weaknesses (gate rulings 6, 7): the
fact-integrity sweep (orphan subject_id from the polymorphic pair;
key subject_type mismatch vs fact_definitions) and contact_relations
directional dedup. Until that sweep exists, the polymorphic
subject_id is unenforced -- the freeze does not claim otherwise.

Everything else (forms engine, esign, packets, tasks, notes, events,
receipts, outbox, settings, auth plumbing, permissions) is v0
skeleton and evolves inside phases without a gate.
