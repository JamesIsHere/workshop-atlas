from workflow_engine import CaseWorkflowEngine

class ConcurrencyError(Exception):
    """Custom exception raised when an optimistic locking conflict occurs."""
    pass

class ConcurrentWorkflowEngine(CaseWorkflowEngine):
    def transition_state_with_version(self, action, actor, role, expected_version):
        """
        Executes a state transition ONLY IF the user's expected_version matches 
        the current engine version (Optimistic Concurrency Control).
        """
        # Step 1: Check version lock BEFORE checking state/permissions
        if expected_version != self.version:
            error_msg = (
                f"CONCURRENCY CONFLICT: User '{actor}' attempted action '{action}' on version {expected_version}, "
                f"but current case version is {self.version}. Update rejected to prevent overwriting data."
            )
            self.log_event(actor, role, "CONCURRENCY_CONFLICT", {"reason": error_msg, "expected": expected_version, "actual": self.version})
            raise ConcurrencyError(error_msg)
            
        # Step 2: Proceed with standard role & state transition validation
        return self.transition_state(action, actor, role)

if __name__ == "__main__":
    print("=" * 80)
    print("MULTI-USER WORKFLOW & CONCURRENCY CONFLICT SIMULATION")
    print("=" * 80 + "\n")
    
    case = ConcurrentWorkflowEngine(case_id="CASE-2026-999")
    print(f"Case Initialized: State = '{case.state}', Version = {case.version}\n")
    
    # -------------------------------------------------------------------
    # SCENARIO 1: Permission Guard Test
    # -------------------------------------------------------------------
    print("--- SCENARIO 1: Testing Permission Guard ---")
    try:
        # Legal Assistant tries to execute an Attorney-only action
        case.transition_state_with_version(
            action="APPROVE_AND_LOCK", 
            actor="assistant_tom", 
            role="Legal Assistant", 
            expected_version=1
        )
    except Exception as e:
        print(f"--> CAUGHT EXPECTED ERROR: {e}\n")

    # -------------------------------------------------------------------
    # SCENARIO 2: Valid Transition by Legal Assistant
    # -------------------------------------------------------------------
    print("--- SCENARIO 2: Valid Submission by Legal Assistant ---")
    case.transition_state_with_version(
        action="SUBMIT_FOR_REVIEW", 
        actor="assistant_tom", 
        role="Legal Assistant", 
        expected_version=1
    )
    print(f"--> Success! New State: '{case.state}', New Version: {case.version}\n")

    # -------------------------------------------------------------------
    # SCENARIO 3: Race Condition (Optimistic Concurrency Lock)
    # -------------------------------------------------------------------
    print("--- SCENARIO 3: Simulating Concurrent Edits (Race Condition) ---")
    # Paralegal Maria & Attorney Rodriguez BOTH loaded the case at Version 2!
    paralegal_read_version = case.version # 2
    attorney_read_version = case.version  # 2
    
    print(f"Paralegal Maria reads case at Version {paralegal_read_version}")
    print(f"Attorney Rodriguez reads case at Version {attorney_read_version}\n")
    
    # 3a. Paralegal Maria saves her review first!
    print("Action A: Paralegal Maria submits escalation to Attorney...")
    case.transition_state_with_version(
        action="ESCALATE_TO_ATTNY", 
        actor="paralegal_maria", 
        role="Paralegal", 
        expected_version=paralegal_read_version
    )
    print(f"--> Success! Engine Version is now {case.version}\n")
    
    # 3b. Attorney Rodriguez now tries to save her action using her stale Version 2!
    print("Action B: Attorney Rodriguez tries to approve using her initial Version 2 snapshot...")
    try:
        case.transition_state_with_version(
            action="APPROVE_AND_LOCK", 
            actor="attorney_rodriguez", 
            role="Attorney", 
            expected_version=attorney_read_version
        )
    except ConcurrencyError as e:
        print(f"--> CAUGHT CONCURRENCY LOCK SAFETY ERROR:\n    {e}\n")

    # -------------------------------------------------------------------
    # PRINT COMPLETE AUDIT TRAIL LOG
    # -------------------------------------------------------------------
    print("=" * 80)
    print("FINAL SYSTEM AUDIT LOG (Including Security & Concurrency Rejections)")
    print("=" * 80)
    for log in case.audit_log:
        status_flag = "[FAIL]" if "REJECTED" in log['action'] or "DENIED" in log['action'] or "CONFLICT" in log['action'] else "[OK]  "
        print(f"{status_flag} v{log['version']} | {log['actor']} ({log['role']}) -> {log['action']}")
