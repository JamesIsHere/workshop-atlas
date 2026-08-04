import sqlite3
import json
import secrets
from workflow_engine import CaseWorkflowEngine, WORKFLOW_RULES

DB_FILE = 'legal_crm.db'

class DatabaseRepository:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file

    def get_connection(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def fetch_case_data(self, case_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 1. Fetch Case & Attorney
        query_case = """
        SELECT 
            c.case_id, c.status, c.version, c.form_type, c.assigned_attorney_id,
            at.first_name as att_first_name, at.last_name as att_last_name, at.middle_name as att_middle_name,
            at.uscis_online_acct as att_uscis, at.phone as att_phone, at.street_address as att_street,
            at.apt_ste_flr as att_apt, at.city as att_city, at.state as att_state, at.zip_code as att_zip
        FROM cases c
        JOIN people at ON c.assigned_attorney_id = at.id
        WHERE c.case_id = ?;
        """
        cursor.execute(query_case, (case_id,))
        case_row = cursor.fetchone()
        
        if not case_row:
            conn.close()
            return None

        # 2. Fetch All Case Parties from Bridge Table
        query_parties = """
        SELECT 
            cp.role_type, p.id as person_id, p.first_name, p.last_name, p.middle_name,
            p.phone, p.street_address, p.apt_ste_flr, p.city, p.state, p.zip_code,
            p.a_number, p.ssn, p.dob, p.country_citizenship
        FROM case_parties cp
        JOIN people p ON cp.person_id = p.id
        WHERE cp.case_id = ?;
        """
        cursor.execute(query_parties, (case_id,))
        party_rows = cursor.fetchall()
        conn.close()

        parties_map = {}
        primary_client = None

        for p in party_rows:
            p_dict = {
                "personId": p["person_id"],
                "firstName": p["first_name"],
                "lastName": p["last_name"],
                "middleName": p["middle_name"],
                "phone": p["phone"],
                "streetAddress": p["street_address"],
                "aptSteFlr": p["apt_ste_flr"],
                "city": p["city"],
                "state": p["state"],
                "zipCode": p["zip_code"],
                "aNumber": p["a_number"],
                "ssn": p["ssn"],
                "dob": p["dob"],
                "countryCitizenship": p["country_citizenship"]
            }
            role_key = p["role_type"].lower()
            parties_map[role_key] = p_dict
            
            # Default primary client to PETITIONER or first party
            if not primary_client or p["role_type"] == "PETITIONER":
                primary_client = p_dict

        return {
            "case_info": {
                "case_id": case_row["case_id"],
                "status": case_row["status"],
                "version": case_row["version"],
                "form_type": case_row["form_type"]
            },
            "attorney": {
                "firstName": case_row["att_first_name"],
                "lastName": case_row["att_last_name"],
                "middleName": case_row["att_middle_name"],
                "uscisOnlineAcct": case_row["att_uscis"],
                "phone": case_row["att_phone"],
                "streetAddress": case_row["att_street"],
                "aptSteFlr": case_row["att_apt"],
                "city": case_row["att_city"],
                "state": case_row["att_state"],
                "zipCode": case_row["att_zip"]
            },
            "client": primary_client or {},
            "parties": parties_map
        }

    def list_all_cases(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            c.case_id, c.status, c.version, c.form_type,
            at.first_name || ' ' || at.last_name as attorney_name,
            p.first_name || ' ' || p.last_name as client_name,
            p.phone as client_phone
        FROM cases c
        JOIN people at ON c.assigned_attorney_id = at.id
        LEFT JOIN case_parties cp ON c.case_id = cp.case_id AND cp.role_type IN ('PETITIONER', 'CLIENT')
        LEFT JOIN people p ON cp.person_id = p.id
        GROUP BY c.case_id
        ORDER BY c.case_id ASC;
        """
        cursor.execute(query)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def fetch_audit_logs(self, case_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, case_id, version, actor, role, action, details, timestamp
            FROM audit_logs
            WHERE case_id = ?
            ORDER BY id DESC;
        """, (case_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def create_new_case(self, first_name, last_name, middle_name="", phone="", street="", apt="", city="", state="", zip_code="", form_type="G-28", attorney_id=1):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Insert Client into people table
            cursor.execute("""
                INSERT INTO people (first_name, last_name, middle_name, phone, street_address, apt_ste_flr, city, state, zip_code, person_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'CLIENT');
            """, (first_name, last_name, middle_name, phone, street, apt, city, state, zip_code))
            person_id = cursor.lastrowid

            # 2. Generate Next Case ID
            cursor.execute("SELECT case_id FROM cases;")
            existing_ids = [r["case_id"] for r in cursor.fetchall()]
            max_num = 0
            for cid in existing_ids:
                if cid.startswith("CASE-2026-"):
                    try:
                        num = int(cid.split("-")[-1])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        pass
            next_num = max_num + 1
            new_case_id = f"CASE-2026-{next_num:03d}"

            # 3. Insert Case record
            cursor.execute("""
                INSERT INTO cases (case_id, assigned_attorney_id, form_type, status, version)
                VALUES (?, ?, ?, 'DRAFT', 1);
            """, (new_case_id, attorney_id, form_type))

            # 4. Link Person to Case via Bridge Table as PETITIONER
            cursor.execute("""
                INSERT INTO case_parties (case_id, person_id, role_type)
                VALUES (?, ?, 'PETITIONER');
            """, (new_case_id, person_id))

            # 5. Audit Log
            cursor.execute("""
                INSERT INTO audit_logs (case_id, version, actor, role, action, details)
                VALUES (?, 1, 'system', 'System', 'CASE_CREATED', ?);
            """, (new_case_id, f"New case created for client {first_name} {last_name}"))

            conn.commit()
            return new_case_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update_person_field(self, case_id, field, value, person_id=None, actor="user", role="Legal Assistant", expected_version=None):
        allowed_fields = {
            'first_name', 'last_name', 'middle_name', 'phone', 'street_address', 
            'apt_ste_flr', 'city', 'state', 'zip_code', 'a_number', 'ssn', 'dob', 'country_citizenship'
        }
        if field not in allowed_fields:
            raise ValueError(f"Invalid field '{field}'")

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Fetch case status & version
            cursor.execute("SELECT status, version FROM cases WHERE case_id = ?;", (case_id,))
            case_row = cursor.fetchone()
            if not case_row:
                raise ValueError(f"Case '{case_id}' not found.")

            status = case_row["status"]
            current_version = case_row["version"]

            # Guard: Optimistic concurrency check, same contract as transitions
            if expected_version is not None and expected_version != current_version:
                error_msg = (
                    f"Concurrency Lock Failure: User '{actor}' tried to edit '{field}' based on version {expected_version}, "
                    f"but current case version is {current_version}. Reload the case before saving."
                )
                cursor.execute("""
                    INSERT INTO audit_logs (case_id, version, actor, role, action, details)
                    VALUES (?, ?, ?, ?, 'CONCURRENCY_REJECTED', ?);
                """, (case_id, current_version, actor, role, error_msg))
                conn.commit()
                raise ValueError(error_msg)

            # Guard: Prevent edit on locked cases (APPROVED / FILED)
            if status in ["APPROVED", "FILED"]:
                raise PermissionError(
                    f"Mutation Blocked: Case '{case_id}' is in '{status}' status and locked against edits. "
                    f"State transition back to DRAFT or review state is required before modifying records."
                )

            # 2. Resolve target person_id if not explicitly provided
            if not person_id:
                cursor.execute("""
                    SELECT person_id FROM case_parties 
                    WHERE case_id = ? AND role_type IN ('PETITIONER', 'BENEFICIARY')
                    LIMIT 1;
                """, (case_id,))
                p_row = cursor.fetchone()
                if not p_row:
                    raise ValueError(f"No party found for case '{case_id}'.")
                person_id = p_row["person_id"]

            # 3. Read old value of field
            cursor.execute(f"SELECT {field} FROM people WHERE id = ?;", (person_id,))
            val_row = cursor.fetchone()
            old_value = val_row[field] if val_row and val_row[field] is not None else ""

            if str(old_value) == str(value):
                return True

            # 4. Perform SQL update on people table
            cursor.execute(f"UPDATE people SET {field} = ? WHERE id = ?;", (value, person_id))

            # 5. Increment case version
            new_version = current_version + 1
            cursor.execute("UPDATE cases SET version = ? WHERE case_id = ?;", (new_version, case_id))

            # 6. Record entry in audit_logs
            cursor.execute("""
                INSERT INTO audit_logs (case_id, version, actor, role, action, details)
                VALUES (?, ?, ?, ?, 'FIELD_UPDATED', ?);
            """, (case_id, new_version, actor, role, f"Updated field '{field}' from '{old_value}' to '{value}'"))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update_client_field(self, case_id, field, value, actor="user", role="Legal Assistant", expected_version=None):
        """Backward compatibility wrapper mapping to update_person_field."""
        return self.update_person_field(case_id=case_id, field=field, value=value, actor=actor, role=role, expected_version=expected_version)

    # ------------------------------------------------------------------
    # Session / Identity layer.
    # The trust boundary: identity is established here, server-side.
    # Handlers derive actor + role from a session token — never from the
    # request body, which the client controls.
    # ------------------------------------------------------------------

    def list_staff_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, first_name, last_name, role
            FROM people WHERE username IS NOT NULL
            ORDER BY id;
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def create_session(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, first_name, last_name, role FROM people WHERE username = ?;", (username,))
            person = cursor.fetchone()
            if not person:
                raise ValueError(f"Unknown user '{username}'.")

            token = secrets.token_hex(16)
            cursor.execute("INSERT INTO sessions (token, person_id) VALUES (?, ?);", (token, person["id"]))
            conn.commit()
            return {
                "token": token,
                "username": person["username"],
                "name": f"{person['first_name']} {person['last_name']}",
                "role": person["role"]
            }
        finally:
            conn.close()

    def resolve_session(self, token):
        if not token:
            return None
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.username, p.first_name, p.last_name, p.role
            FROM sessions s JOIN people p ON p.id = s.person_id
            WHERE s.token = ?;
        """, (token,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return {
            "person_id": row["id"],
            "username": row["username"],
            "name": f"{row['first_name']} {row['last_name']}",
            "role": row["role"]
        }

    def delete_session(self, token):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?;", (token,))
        conn.commit()
        conn.close()

    def reset_case(self, case_id, actor="user", role="Admin"):
        """Returns a case to DRAFT as a versioned, audited mutation. The audit trail is never deleted."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT status, version FROM cases WHERE case_id = ?;", (case_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Case '{case_id}' not found.")

            old_status = row["status"]
            new_version = row["version"] + 1

            cursor.execute("UPDATE cases SET status = 'DRAFT', version = ? WHERE case_id = ?;", (new_version, case_id))
            cursor.execute("""
                INSERT INTO audit_logs (case_id, version, actor, role, action, details)
                VALUES (?, ?, ?, ?, 'CASE_RESET', ?);
            """, (case_id, new_version, actor, role, f"Case reset from '{old_status}' back to 'DRAFT' (version {new_version})"))

            conn.commit()
            return new_version
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute_versioned_transition(self, case_id, expected_version, action_name, actor, role, new_status=None):
        """
        Executes an FSM-validated transition & atomic SQL Transaction.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Step 1: Fetch current case state & version
            cursor.execute("SELECT status, version FROM cases WHERE case_id = ?;", (case_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Case '{case_id}' not found.")
            
            curr_status = row["status"]
            curr_version = row["version"]

            # Step 2: Optimistic Concurrency Lock Check
            if expected_version is not None and expected_version != curr_version:
                error_msg = (
                    f"Concurrency Lock Failure: User '{actor}' requested action '{action_name}' on version {expected_version}, "
                    f"but current case version is {curr_version}."
                )
                cursor.execute("""
                    INSERT INTO audit_logs (case_id, version, actor, role, action, details)
                    VALUES (?, ?, ?, ?, 'CONCURRENCY_REJECTED', ?);
                """, (case_id, curr_version, actor, role, error_msg))
                conn.commit()
                raise ValueError(error_msg)

            # Step 3: Instantiate Workflow FSM Engine and validate transition rules
            fsm = CaseWorkflowEngine(case_id=case_id, current_state=curr_status, version=curr_version)
            try:
                target_state = fsm.transition_state(action=action_name, actor=actor, role=role)
            except (ValueError, PermissionError) as fsm_err:
                cursor.execute("""
                    INSERT INTO audit_logs (case_id, version, actor, role, action, details)
                    VALUES (?, ?, ?, ?, 'TRANSITION_DENIED', ?);
                """, (case_id, curr_version, actor, role, str(fsm_err)))
                conn.commit()
                raise fsm_err

            # Step 4: Atomic SQL UPDATE with version increment
            new_version = curr_version + 1
            cursor.execute("""
                UPDATE cases 
                SET status = ?, version = ? 
                WHERE case_id = ? AND version = ?;
            """, (target_state, new_version, case_id, curr_version))
            
            if cursor.rowcount == 0:
                raise Exception(f"Atomic UPDATE Failed: Concurrency collision during write.")

            # Step 5: Write success entry to audit_logs SQL table
            cursor.execute("""
                INSERT INTO audit_logs (case_id, version, actor, role, action, details)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (case_id, new_version, actor, role, action_name, f"State transitioned from '{curr_status}' to '{target_state}'"))
            
            conn.commit()
            return target_state
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

if __name__ == '__main__':
    repo = DatabaseRepository()
    data = repo.fetch_case_data("CASE-2026-001")
    print(json.dumps(data, indent=2))
