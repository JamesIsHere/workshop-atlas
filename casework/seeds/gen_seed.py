"""Synthetic seed generator. Emits seed.sql; never hand-edit output.

SYNTHETIC DATA ONLY (goal.md): every identity here is deliberately fake
(surname 'Synthetic', SYNTH- identifiers, example.test addresses). No
real client data, no real PII, ever. The synthetic_marker row is the
guard's hook; removing it fails the harness.

DETERMINISM: fixed ids, fixed timestamps, no randomness -- reruns are
byte-identical. Timestamps use a fixed base date, not wall clock.

Run: python gen_seed.py   (writes seed.sql beside this file)
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.auth import hash_password  # noqa: E402

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "forms" / "schemas"

T0 = "2026-08-01T00:00:00Z"

# Real, usable scrypt hashes (U1.1): password is 'synthetic-password'
# for every seeded staff user; salt derives from the email so reruns
# stay byte-identical. Synthetic-only db -- a shared known password is
# the point, not a defect.
SEED_PASSWORD = "synthetic-password"


def seed_hash(email):
    salt = hashlib.sha256(f"synth-salt:{email}".encode()).digest()[:16]
    return hash_password(SEED_PASSWORD, salt)


def q(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def ins(table, cols, rows):
    out = []
    for row in rows:
        vals = ", ".join(q(v) for v in row)
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({vals});")
    return out


# Baseline fact vocabulary lives with the install path (U5.1): the
# seed and a cold deployment load the same list, so they cannot drift.
from app.bootstrap import BASELINE_FACT_DEFS as FACT_DEFS  # noqa: E402

USERS = [
    # id, email, name, role_label, is_admin, is_owner
    (1, "ada.admin@example.test", "Ada Synthetic", "Managing Attorney", 1, 1),
    (2, "bram.attorney@example.test", "Bram Synthetic", "Attorney", 0, 0),
    (3, "cleo.paralegal@example.test", "Cleo Synthetic", "Paralegal", 0, 0),
]

CONTACTS = [
    # id, kind, display_name, email, phone, a_number, uid
    # (email/phone/a_number/uid land in facts, not contacts columns --
    # gate ruling 7: registry mechanics only)
    (1, "person", "Dana Synthetic", "dana@example.test", "+1-555-0101", "A-SYNTH-0001", "SYNTH-C1"),
    (2, "person", "Emil Synthetic", "emil@example.test", "+1-555-0102", "A-SYNTH-0002", "SYNTH-C2"),
    (3, "person", "Fara Synthetic", "fara@example.test", "+1-555-0103", None, "SYNTH-C3"),
    (4, "person", "Gil Synthetic", "gil@example.test", "+1-555-0104", "A-SYNTH-0004", "SYNTH-C4"),
    (5, "person", "Hana Synthetic", "hana@example.test", "+1-555-0105", None, "SYNTH-C5"),
    (6, "person", "Ivo Synthetic", "ivo@example.test", "+1-555-0106", None, "SYNTH-C6"),
    (7, "company", "Synthetic Staffing LLC", "hr@synthstaffing.example.test", "+1-555-0199", None, "SYNTH-CO1"),
]

MATTER_TYPES = [(1, "I-130 Family Petition"), (2, "N-400 Naturalization"),
                (3, "H-1B Petition"), (4, "PERM Labor Certification")]

# forms-library criterion: case type -> required forms (U2.1)
MATTER_TYPE_FORMS = {1: ["i-130", "g-28"], 2: ["n-400", "g-28"],
                     3: ["i-129", "g-28"], 4: ["eta-9089", "g-28"]}

# firm identity + print/preparer defaults (U2.2)
FIRM_SETTINGS = [
    ("firm.name", "Synthetic Law LLP"),
    ("firm.street", "200 Synthetic Plaza"),
    ("firm.city", "Faketown"),
    ("firm.state", "VA"),
    ("firm.zip", "00002"),
    ("firm.phone", "+1-555-0200"),
    ("preparer.default_user_id", "2"),
]

USER_SETTINGS = [
    (2, "preparer.bar_number", "VA-SYNTH-123"),
    (2, "preparer.licensing_authority", "Virginia State Bar"),
    (2, "preparer.family_name", "Synthetic"),
    (2, "preparer.given_name", "Bram"),
]

# premade note categories ship with the system (fx-0223)
NOTE_CATEGORIES = [(1, "Government Action"), (2, "Memo"),
                   (3, "Meeting"), (4, "Phone Call")]

MATTER_STATUSES = [
    # id, type_id, name, position, duration_days
    (1, 1, "Intake", 1, 14), (2, 1, "Preparing", 2, 30),
    (3, 1, "Filed", 3, None), (4, 1, "Approved", 4, None),
    (5, 2, "Intake", 1, 14), (6, 2, "Preparing", 2, 21),
    (7, 2, "Filed", 3, None), (8, 2, "Interview", 4, None),
    (9, 2, "Oath", 5, None),
]

MATTERS = [
    # id, name, primary_contact, type, status, priority_date, pref_cat, charge, assignee
    (1, "Dana Synthetic I-130", 1, 1, 1, "2022-03-15", "F2A", "Mexico", 2),
    (2, "Emil Synthetic N-400", 2, 2, 5, None, None, None, 2),
    (3, "Fara Synthetic I-130", 3, 1, 2, "2020-11-02", "F1", "India", 3),
    (4, "Gil Synthetic N-400", 4, 2, 6, None, None, None, 3),
]

FACTS = [
    # subject_id, key, idx, value  (all contact-subject)
    (1, "bio.given_name", 0, "Dana"), (1, "bio.family_name", 0, "Synthetic"),
    (1, "bio.date_of_birth", 0, "1990-04-12"),
    (1, "bio.country_of_birth", 0, "Testlandia"),
    (1, "addr.street", 0, "100 Synthetic Way"), (1, "addr.city", 0, "Faketown"),
    (1, "addr.state", 0, "VA"), (1, "addr.zip", 0, "00001"),
    (1, "addr.country", 0, "United States"),
    (1, "imm.us_status", 0, "H-1B"), (1, "imm.vmax_date", 0, "2027-06-30"),
    (1, "imm.status_expiry", 0, "2027-06-30"),
    (2, "bio.given_name", 0, "Emil"), (2, "bio.family_name", 0, "Synthetic"),
    (2, "bio.date_of_birth", 0, "1985-09-01"),
    (2, "bio.country_of_birth", 0, "Examplestan"),
    (2, "imm.us_status", 0, "LPR"),
    (2, "emp.employer_name", 0, "Synthetic Staffing LLC"),
    (2, "emp.job_title", 0, "Test Engineer"),
    # name atoms for the remaining persons: display_name is derived,
    # never authoritative (Name model, schema-design.md)
    (3, "bio.given_name", 0, "Fara"), (3, "bio.family_name", 0, "Synthetic"),
    (4, "bio.given_name", 0, "Gil"), (4, "bio.family_name", 0, "Synthetic"),
    (5, "bio.given_name", 0, "Hana"), (5, "bio.family_name", 0, "Synthetic"),
    (6, "bio.given_name", 0, "Ivo"), (6, "bio.family_name", 0, "Synthetic"),
]


def generate():
    lines = [
        "-- GENERATED by gen_seed.py -- do not hand-edit. SYNTHETIC DATA ONLY.",
        "INSERT INTO synthetic_marker (marker) VALUES ('SYNTHETIC');",
        "",
    ]
    lines += ins("fact_definitions",
                 ["key", "subject_type", "value_type", "label", "repeating"],
                 FACT_DEFS)
    lines.append("")
    lines += ins("users",
                 ["id", "email", "name", "password_hash", "role_label",
                  "is_admin", "is_owner", "created_at"],
                 [(i, e, n, seed_hash(e), r, a, o, T0)
                  for i, e, n, r, a, o in USERS])
    lines.append("")
    lines += ins("contacts",
                 ["id", "kind", "display_name", "created_at", "created_by"],
                 [(i, k, d, T0, 1) for i, k, d, *_ in CONTACTS])
    lines.append("")
    lines += ins("matter_types", ["id", "name"], MATTER_TYPES)
    lines += ins("note_categories", ["id", "name", "builtin"],
                 [(i, n, 1) for i, n in NOTE_CATEGORIES])
    lines += ins("matter_statuses",
                 ["id", "matter_type_id", "name", "position", "duration_days"],
                 MATTER_STATUSES)
    lines.append("")
    lines += ins("matters",
                 ["id", "name", "primary_contact_id", "matter_type_id",
                  "matter_status_id", "status_entered_at", "priority_date",
                  "preference_category", "chargeability_country",
                  "assignee_id", "created_at", "created_by"],
                 [(i, n, c, t, s, T0, pd, pc, ch, a, T0, 1)
                  for i, n, c, t, s, pd, pc, ch, a in MATTERS])
    lines.append("")
    lines += ins("facts",
                 ["subject_type", "subject_id", "key", "idx", "value", "updated_at"],
                 [("contact", sid, k, idx, v, T0) for sid, k, idx, v in FACTS])
    # channel/identifier facts derived from the CONTACTS roster
    channel_keys = ["contact.email", "contact.phone", "imm.a_number",
                    "meta.unique_identifier"]
    lines += ins("facts",
                 ["subject_type", "subject_id", "key", "idx", "value", "updated_at"],
                 [("contact", cid, key, 0, val, T0)
                  for cid, _k, _d, *vals in CONTACTS
                  for key, val in zip(channel_keys, vals)
                  if val is not None])
    # every seeded contact carries the synthetic fact marker
    lines += ins("facts",
                 ["subject_type", "subject_id", "key", "idx", "value", "updated_at"],
                 [("contact", cid, "meta.synthetic", 0, "true", T0)
                  for cid, *_ in CONTACTS])
    # --- forms library (U2.1): schemas dir is the source, db the authority
    lines.append("")
    eid = 0
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        eid += 1
        lines += ins("form_definitions", ["code", "title", "agency", "efilable"],
                     [(schema["code"], schema["title"], schema["agency"],
                       schema.get("efilable", 0))])
        lines += ins("form_editions",
                     ["id", "form_code", "edition", "schema_json", "is_current"],
                     [(eid, schema["code"], schema["edition"],
                       json.dumps(schema), 1)])
    lines.append("")
    lines += ins("firm_settings", ["key", "value"], FIRM_SETTINGS)
    lines += ins("user_settings", ["user_id", "key", "value"], USER_SETTINGS)
    lines.append("")
    lines += ins("matter_type_forms", ["matter_type_id", "form_code", "position"],
                 [(mt, code, pos)
                  for mt, codes in sorted(MATTER_TYPE_FORMS.items())
                  for pos, code in enumerate(codes, 1)])
    lines.append("")
    lines += billing_section("\n".join(lines))
    return "\n".join(lines) + "\n"


def billing_section(seed_so_far):
    """Billing/trust scenario (casework-billing P1 U1.2). Built by
    RUNNING the ledger recipes against an in-memory db seeded with the
    sections above, then dumping the resulting rows -- the seeded
    journal is recipe-produced by construction and cannot drift from
    app/ledger.py. Deterministic: fixed dates, created_at pinned to T0
    in the dump."""
    from app import db as appdb, ledger
    conn = appdb.create_db(":memory:")
    conn.actor.set("system", None)
    conn.executescript(seed_so_far)

    D1, D2, D3 = "2026-08-01", "2026-08-02", "2026-08-03"
    iolta = ledger.create_bank_account(conn, "trust_bank",
                                       "SYNTH IOLTA Trust", 1)
    op = ledger.create_bank_account(conn, "operating_bank",
                                    "SYNTH Operating", 1)
    # Dana (contact 1): client-level retainer, earn-out, disbursement
    ledger.record_trust_deposit(conn, iolta, 500000, D1, 1, contact_id=1,
                                memo="SYNTH retainer Dana")
    ledger.earn_out(conn, iolta, op, 300000, D2, 1, contact_id=1,
                    memo="SYNTH bill 1 paid from trust")
    ledger.disburse(conn, iolta, 120000, D2, 1, contact_id=1,
                    counterparty="SYNTH-USCIS", memo="SYNTH I-130 fee")
    # Emil (matter 2): matter-level filing funds
    ledger.record_trust_deposit(conn, iolta, 200000, D1, 1, matter_id=2,
                                memo="SYNTH filing funds Emil N-400")
    # Fara (contact 3): client-level with a small disbursement
    ledger.record_trust_deposit(conn, iolta, 150000, D2, 1, contact_id=3,
                                memo="SYNTH retainer Fara")
    ledger.disburse(conn, iolta, 25000, D3, 1, contact_id=3,
                    counterparty="SYNTH-Translator", memo="SYNTH translation")
    # operating-only income for contrast
    ledger.record_bill_direct_payment(conn, op, 50000, D3, 1,
                                      memo="SYNTH consult paid direct")

    out = ["-- billing/trust scenario (recipe-produced dump; see"
           " billing_section)"]
    out += ins("ledger_accounts",
               ["id", "kind", "name", "parent_id", "contact_id",
                "matter_id", "created_at", "created_by"],
               [(r["id"], r["kind"], r["name"], r["parent_id"],
                 r["contact_id"], r["matter_id"], T0, r["created_by"])
                for r in conn.execute("SELECT * FROM ledger_accounts"
                                      " ORDER BY id")])
    out += ins("journal_entries",
               ["id", "kind", "memo", "invoice_id", "payment_id",
                "external_event_id", "reverses_entry_id",
                "replaces_entry_id", "posted_at", "posted_by"],
               [(r["id"], r["kind"], r["memo"], r["invoice_id"],
                 r["payment_id"], r["external_event_id"],
                 r["reverses_entry_id"], r["replaces_entry_id"],
                 r["posted_at"], r["posted_by"])
                for r in conn.execute("SELECT * FROM journal_entries"
                                      " ORDER BY id")])
    out += ins("journal_postings",
               ["id", "entry_id", "account_id", "side", "amount_cents",
                "cleared_at", "statement_ref"],
               [(r["id"], r["entry_id"], r["account_id"], r["side"],
                 r["amount_cents"], r["cleared_at"], r["statement_ref"])
                for r in conn.execute("SELECT * FROM journal_postings"
                                      " ORDER BY id")])
    out += ins("external_events",
               ["id", "event_type", "bank_account_id", "occurred_on",
                "amount_cents", "direction", "counterparty", "memo",
                "invoice_id", "payment_id", "created_at"],
               [(r["id"], r["event_type"], r["bank_account_id"],
                 r["occurred_on"], r["amount_cents"], r["direction"],
                 r["counterparty"], r["memo"], r["invoice_id"],
                 r["payment_id"], T0)
                for r in conn.execute("SELECT * FROM external_events"
                                      " ORDER BY id")])
    conn.close()
    return out


if __name__ == "__main__":
    target = Path(__file__).parent / "seed.sql"
    target.write_text(generate(), encoding="utf-8", newline="\n")
    print(f"wrote {target} ({len(generate().splitlines())} lines)")
