import sqlite3
import json
from setup_database import init_database

DB_FILE = 'legal_crm.db'

def print_separator(title):
    print("\n" + "=" * 90)
    print(f"  {title}")
    print("=" * 90)

# Re-initialize for a deterministic starting state (DRAFT, version 1)
init_database()

# -------------------------------------------------------------------
# TEST 1: Inspect Raw SQL Tables
# -------------------------------------------------------------------
print_separator("TEST 1: RAW SQL TABLE INSPECTION")

conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- SELECT * FROM people ---")
cursor.execute("SELECT id, first_name, last_name, person_type, phone, city, state FROM people;")
for row in cursor.fetchall():
    print(dict(row))

print("\n--- SELECT * FROM cases ---")
cursor.execute("SELECT case_id, assigned_attorney_id, form_type, status, version FROM cases;")
for row in cursor.fetchall():
    print(dict(row))

print("\n--- SELECT * FROM case_parties ---")
cursor.execute("SELECT id, case_id, person_id, role_type FROM case_parties;")
for row in cursor.fetchall():
    print(dict(row))

# -------------------------------------------------------------------
# TEST 2: Execute SQL JOIN Query
# -------------------------------------------------------------------
print_separator("TEST 2: SQL RELATIONAL JOIN (cases + case_parties + people)")

sql_join = """
SELECT
    c.case_id, c.form_type, c.status, c.version,
    cp.role_type,
    p.first_name || ' ' || p.last_name AS party_full_name,
    p.phone AS party_phone,
    at.first_name || ' ' || at.last_name AS attorney_full_name
FROM cases c
JOIN case_parties cp ON cp.case_id = c.case_id
JOIN people p ON p.id = cp.person_id
JOIN people at ON at.id = c.assigned_attorney_id;
"""

cursor.execute(sql_join)
join_results = [dict(r) for r in cursor.fetchall()]
print(json.dumps(join_results, indent=2))

# -------------------------------------------------------------------
# TEST 3: Mutate Database Data & Observe Diff Engine Detection
# -------------------------------------------------------------------
print_separator("TEST 3: LIVE DATABASE MUTATION & DIFF DETECTION")

cursor.execute("""
    SELECT person_id FROM case_parties
    WHERE case_id = 'CASE-2026-001' AND role_type = 'PETITIONER';
""")
petitioner_id = cursor.fetchone()["person_id"]

print(f"Executing SQL: UPDATE people SET phone = '202-555-9999' WHERE id = {petitioner_id};")
cursor.execute("UPDATE people SET phone = '202-555-9999' WHERE id = ?;", (petitioner_id,))
conn.commit()

print("--> Database phone updated to '202-555-9999'. Running live DB Diff Engine...\n")

from db_diff_engine import run_pdf_diff_from_db
case_info, diffs = run_pdf_diff_from_db("CASE-2026-001", "storage/2_intake_scans/g-28_filled.pdf", "g-28_mapping.json")

phone_diff = [d for d in diffs if "Mobile" in d['label']][0]
print(f"Field Tested: {phone_diff['label']}")
print(f"SQL DB Value: {phone_diff['raw_db_value']}")
print(f"PDF Value:    {phone_diff['raw_pdf_value']}")
print(f"Status:       {phone_diff['status']}  <-- Engine detected the mismatch from the DB update!")
assert phone_diff['status'] == "MISMATCH", "Diff engine should flag the mutated phone as MISMATCH"

# Revert DB change back to 202-555-0144
cursor.execute("UPDATE people SET phone = '202-555-0144' WHERE id = ?;", (petitioner_id,))
conn.commit()

# -------------------------------------------------------------------
# TEST 4: Execute Versioned State Transition & Inspect Audit Logs
# -------------------------------------------------------------------
print_separator("TEST 4: EXECUTING SQL TRANSACTION & INSPECTING AUDIT_LOGS TABLE")

from db_repository import DatabaseRepository
repo = DatabaseRepository()

cursor.execute("SELECT version FROM cases WHERE case_id = 'CASE-2026-001';")
current_version = cursor.fetchone()["version"]

print(f"Executing Transition: Submitting Case CASE-2026-001 from DRAFT -> PARALEGAL_REVIEW (expected_version={current_version})...")
repo.execute_versioned_transition(
    case_id="CASE-2026-001",
    expected_version=current_version,
    actor="assistant_sam",
    role="Legal Assistant",
    action_name="SUBMIT_FOR_REVIEW"
)

print("\n--- SELECT * FROM audit_logs ---")
cursor.execute("SELECT id, case_id, version, actor, role, action, details, timestamp FROM audit_logs;")
for row in cursor.fetchall():
    print(dict(row))

print("\n--- SELECT case_id, status, version FROM cases ---")
cursor.execute("SELECT case_id, status, version FROM cases WHERE case_id = 'CASE-2026-001';")
final_row = dict(cursor.fetchone())
print(final_row)
assert final_row["status"] == "PARALEGAL_REVIEW"

conn.close()
print("\nALL DATABASE QUERY TESTS PASSED.")
