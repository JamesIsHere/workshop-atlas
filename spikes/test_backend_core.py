import os
import json
import sqlite3
from setup_database import init_database
from db_repository import DatabaseRepository
from workflow_engine import CaseWorkflowEngine

def test_backend_core_engine():
    print("=" * 80)
    print("RUNNING BACKEND CORE ENGINE INTEGRATION & STATE AUDIT SUITE")
    print("=" * 80 + "\n")

    # Step 1: Re-initialize fresh SQLite database
    init_database()
    repo = DatabaseRepository()
    case_id = "CASE-2026-001"

    # Verify initial state
    data = repo.fetch_case_data(case_id)
    print(f"[TEST 1] Initial Case State: {data['case_info']['status']} (Version {data['case_info']['version']})")
    assert data['case_info']['status'] == "DRAFT"
    assert data['case_info']['version'] == 1
    print("--> PASSED: Initial state is DRAFT (v1)\n")

    # Step 2: Test Field Editing & Audit Logging (old_value -> new_value)
    print("[TEST 2] Updating client field 'phone' from '202-555-0144' to '202-555-9999'...")
    repo.update_client_field(case_id, field="phone", value="202-555-9999", actor="assistant_sam", role="Legal Assistant")
    
    updated_data = repo.fetch_case_data(case_id)
    print(f"--> Updated Phone in DB: {updated_data['client']['phone']} (New Version: {updated_data['case_info']['version']})")
    assert updated_data['client']['phone'] == "202-555-9999"
    assert updated_data['case_info']['version'] == 2

    # Check audit log entry
    logs = repo.fetch_audit_logs(case_id)
    latest_log = logs[0]
    print(f"--> Audit Log Recorded: [{latest_log['action']}] {latest_log['details']} (by {latest_log['actor']})")
    assert latest_log['action'] == "FIELD_UPDATED"
    assert "202-555-0144" in latest_log['details'] and "202-555-9999" in latest_log['details']
    print("--> PASSED: Field edit and audit provenance accurately captured.\n")

    # Step 2b: Test Optimistic Concurrency on Field Edits (stale expected_version)
    print("[TEST 2b] Field edit with stale expected_version=1 (current is 2) must be rejected...")
    try:
        repo.update_client_field(case_id, field="phone", value="202-555-0000", actor="assistant_sam", role="Legal Assistant", expected_version=1)
        assert False, "Stale field edit should have been rejected!"
    except ValueError as e:
        print(f"--> CAUGHT EXPECTED CONCURRENCY ERROR: {e}")
    fresh = repo.fetch_case_data(case_id)
    assert fresh['client']['phone'] == "202-555-9999", "Phone must be unchanged after rejected edit"
    assert fresh['case_info']['version'] == 2, "Version must not bump on rejected edit"
    print("--> PASSED: Stale field edit blocked, data and version unchanged.\n")

    # Step 3: Test FSM Guard (Legal Assistant trying to APPROVE_AND_LOCK from DRAFT)
    print("[TEST 3] Testing FSM Guard (Legal Assistant trying to APPROVE_AND_LOCK)...")
    try:
        repo.execute_versioned_transition(
            case_id=case_id,
            expected_version=2,
            action_name="APPROVE_AND_LOCK",
            actor="assistant_sam",
            role="Legal Assistant"
        )
        assert False, "FSM guard should have raised an exception!"
    except (PermissionError, ValueError) as e:
        print(f"--> CAUGHT EXPECTED FSM GUARD ERROR: {e}")
        print("--> PASSED: Unauthorized transition blocked.\n")

    # Step 4: Valid FSM Progression (Assistant -> Paralegal -> Attorney)
    print("[TEST 4] Executing valid sequential FSM state transitions...")
    # 4a. Assistant submits for review (v2 -> v3)
    s1 = repo.execute_versioned_transition(case_id, expected_version=2, action_name="SUBMIT_FOR_REVIEW", actor="assistant_sam", role="Legal Assistant")
    print(f"--> Transition 1: {s1} (v3)")
    assert s1 == "PARALEGAL_REVIEW"

    # 4b. Paralegal escalates to attorney (v3 -> v4)
    s2 = repo.execute_versioned_transition(case_id, expected_version=3, action_name="ESCALATE_TO_ATTNY", actor="paralegal_maria", role="Paralegal")
    print(f"--> Transition 2: {s2} (v4)")
    assert s2 == "ATTORNEY_REVIEW"

    # 4c. Attorney approves and locks (v4 -> v5)
    s3 = repo.execute_versioned_transition(case_id, expected_version=4, action_name="APPROVE_AND_LOCK", actor="attorney_rodriguez", role="Attorney")
    print(f"--> Transition 3: {s3} (v5)")
    assert s3 == "APPROVED"
    print("--> PASSED: FSM pipeline completed through APPROVED state.\n")

    # Step 5: Test Concurrency Lock Safety (Stale expected_version)
    print("[TEST 5] Testing Optimistic Concurrency Lock (Using stale expected_version=3)...")
    try:
        repo.execute_versioned_transition(case_id, expected_version=3, action_name="MARK_AS_FILED", actor="attorney_rodriguez", role="Attorney")
        assert False, "Concurrency check should have rejected stale version 3!"
    except Exception as e:
        print(f"--> CAUGHT EXPECTED CONCURRENCY LOCK ERROR: {e}")
        print("--> PASSED: Stale version write blocked.\n")

    # Step 6: Test Locked State Field Mutation Guard
    print("[TEST 6] Testing Locked State Guard (Attempting to edit client address on APPROVED case)...")
    try:
        repo.update_client_field(case_id, field="street_address", value="123 Malicious St", actor="assistant_sam", role="Legal Assistant")
        assert False, "Mutation guard should have blocked editing an APPROVED case!"
    except PermissionError as e:
        print(f"--> CAUGHT EXPECTED LOCKED STATE MUTATION ERROR: {e}")
        print("--> PASSED: Field edit on APPROVED case blocked.\n")

    # Step 7: Final Audit Trail Review
    print("[TEST 7] Printing Full Immutable Audit Trail Log from SQLite...")
    print("-" * 80)
    audit_trail = repo.fetch_audit_logs(case_id)
    for entry in reversed(audit_trail):
        print(f"[{entry['timestamp'][:19]}] v{entry['version']} | {entry['actor']} ({entry['role']}) -> {entry['action']}: {entry['details']}")
    print("-" * 80)
    print("\nALL BACKEND CORE ENGINE TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_backend_core_engine()
