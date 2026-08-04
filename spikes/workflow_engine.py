import json
from datetime import datetime

# 1. State Machine Configuration (The Rulebook)
WORKFLOW_RULES = {
    "DRAFT": {
        "SUBMIT_FOR_REVIEW": {"next_state": "PARALEGAL_REVIEW", "roles": ["Legal Assistant", "Paralegal", "Attorney"]}
    },
    "PARALEGAL_REVIEW": {
        "REJECT_TO_DRAFT":   {"next_state": "DRAFT",            "roles": ["Paralegal", "Attorney"]},
        "ESCALATE_TO_ATTNY": {"next_state": "ATTORNEY_REVIEW",  "roles": ["Paralegal", "Attorney"]}
    },
    "ATTORNEY_REVIEW": {
        "REJECT_TO_DRAFT":   {"next_state": "DRAFT",            "roles": ["Attorney"]},
        "APPROVE_AND_LOCK":  {"next_state": "APPROVED",         "roles": ["Attorney"]}
    },
    "APPROVED": {
        "MARK_AS_FILED":     {"next_state": "FILED",            "roles": ["Attorney", "Admin"]}
    },
    "FILED": {} # Terminal locked state
}

class CaseWorkflowEngine:
    def __init__(self, case_id, current_state="DRAFT", version=1):
        self.case_id = case_id
        self.state = current_state
        self.version = version
        self.audit_log = []
        
    def log_event(self, actor, role, action, details):
        """Appends an immutable entry to the audit trail."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "case_id": self.case_id,
            "version": self.version,
            "state_at_time": self.state,
            "actor": actor,
            "role": role,
            "action": action,
            "details": details
        }
        self.audit_log.append(entry)
        return entry

    def transition_state(self, action, actor, role):
        """Attempts to execute a state transition based on the FSM rulebook."""
        current_rules = WORKFLOW_RULES.get(self.state, {})
        
        # Check 1: Is the action valid from the current state?
        if action not in current_rules:
            error_msg = f"Transition Failed: Action '{action}' is not allowed from state '{self.state}'."
            self.log_event(actor, role, "TRANSITION_REJECTED", {"reason": error_msg})
            raise ValueError(error_msg)
            
        rule = current_rules[action]
        allowed_roles = rule["roles"]
        next_state = rule["next_state"]
        
        # Check 2: Does the actor have the required role?
        if role not in allowed_roles:
            error_msg = f"Permission Denied: User '{actor}' with role '{role}' cannot perform '{action}'."
            self.log_event(actor, role, "PERMISSION_DENIED", {"reason": error_msg})
            raise PermissionError(error_msg)
            
        # Execute valid transition
        old_state = self.state
        self.state = next_state
        self.version += 1 # Increment version for optimistic concurrency
        
        success_details = {
            "from_state": old_state,
            "to_state": next_state,
            "new_version": self.version
        }
        self.log_event(actor, role, action, success_details)
        return self.state

# Quick demonstration execution
if __name__ == "__main__":
    case = CaseWorkflowEngine(case_id="CASE-2026-001")
    print(f"Initial Case State: {case.state} (Version {case.version})\n")
    
    # 1. Legal Assistant submits draft for review
    case.transition_state(action="SUBMIT_FOR_REVIEW", actor="assistant_sam", role="Legal Assistant")
    print(f"After Assistant Submission: {case.state} (Version {case.version})")
    
    # 2. Paralegal escalates to Attorney
    case.transition_state(action="ESCALATE_TO_ATTNY", actor="paralegal_maria", role="Paralegal")
    print(f"After Paralegal Escalation: {case.state} (Version {case.version})")
    
    # 3. Attorney approves case
    case.transition_state(action="APPROVE_AND_LOCK", actor="attorney_rodriguez", role="Attorney")
    print(f"After Attorney Approval: {case.state} (Version {case.version})\n")
    
    # Print Audit Log
    print("=" * 80)
    print("AUDIT TRAIL LOG:")
    print("=" * 80)
    for log in case.audit_log:
        print(f"[{log['timestamp'][:19]}] v{log['version']} | {log['actor']} ({log['role']}) -> Action: {log['action']} -> Details: {log['details']}")
