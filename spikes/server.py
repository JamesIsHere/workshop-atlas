import http.server
import socketserver
import json
import urllib.parse
import os
from db_repository import DatabaseRepository
from db_diff_engine import run_pdf_diff_from_db
from generate_package import generate_multi_form_package

PORT = 8000
ROOT_DIR = r"C:\Users\james\Desktop\workshop\atlas"

class LegalCRMApiHandler(http.server.SimpleHTTPRequestHandler):
    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _get_session(self):
        """Resolve the caller's identity from the Authorization header, server-side.
        Returns a session dict {username, name, role} or None."""
        auth = self.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return None
        token = auth[len('Bearer '):].strip()
        repo = DatabaseRepository()
        return repo.resolve_session(token)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        case_id = query_params.get('case_id', ['CASE-2026-001'])[0]

        if path == '/api/staff':
            repo = DatabaseRepository()
            self._send_json({"staff": repo.list_staff_users()})
            return

        elif path == '/api/whoami':
            session = self._get_session()
            if not session:
                self._send_json({"error": "Not signed in"}, status_code=401)
                return
            self._send_json({"user": session})
            return

        elif path == '/api/cases':
            repo = DatabaseRepository()
            cases = repo.list_all_cases()
            self._send_json({"cases": cases})
            return

        elif path == '/api/case':
            repo = DatabaseRepository()
            data = repo.fetch_case_data(case_id)
            if not data:
                self._send_json({"error": f"Case {case_id} not found"}, status_code=404)
                return
            self._send_json(data)
            return

        elif path == '/api/diff':
            try:
                case_info, diffs = run_pdf_diff_from_db(case_id, "storage/2_intake_scans/g-28_filled.pdf", "g-28_mapping.json")
                self._send_json({"case_info": case_info, "diffs": diffs})
            except Exception as e:
                self._send_json({"error": str(e)}, status_code=400)
            return

        elif path == '/api/db-view':
            repo = DatabaseRepository()
            conn = repo.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.*, cp.role_type FROM people p
                JOIN case_parties cp ON cp.person_id = p.id
                WHERE cp.case_id = ?
                ORDER BY CASE WHEN cp.role_type = 'PETITIONER' THEN 0 ELSE 1 END;
            """, (case_id,))
            party_rows = [dict(r) for r in cursor.fetchall()]
            client_dict = party_rows[0] if party_rows else {}

            cursor.execute("SELECT * FROM cases WHERE case_id = ?;", (case_id,))
            case_row = cursor.fetchone()
            case_dict = dict(case_row) if case_row else {}

            cursor.execute("SELECT * FROM audit_logs WHERE case_id = ? ORDER BY id DESC;", (case_id,))
            audit_rows = [dict(r) for r in cursor.fetchall()]

            conn.close()
            self._send_json({
                "client_table": client_dict,
                "parties_table": party_rows,
                "case_table": case_dict,
                "audit_table": audit_rows
            })
            return

        elif path == '/api/directory':
            try:
                def get_file_tree(dir_path):
                    tree = []
                    descriptions = {
                        "storage": "Root storage directory housing the 3 document lifecycle buckets.",
                        "storage/1_templates": "Bucket 2: Master blank official USCIS fillable PDF forms & field blueprints.",
                        "storage/2_intake_scans": "Bucket 1: Raw incoming client PDF uploads & unverified intake scans.",
                        "storage/3_exports": "Bucket 3: Official court/USCIS-ready filled PDF packages generated from SQLite DB.",
                        "testing": "Automated Puppeteer browser testing suite, screenshots, & execution reports.",
                        "server.py": "Python HTTP Server serving web UI and REST API endpoints.",
                        "db_repository.py": "Repository pattern layer managing SQLite queries, version locks, & audit logs.",
                        "db_diff_engine.py": "Normalization diff engine comparing SQLite DB values against raw PDF fields.",
                        "workflow_engine.py": "Finite State Machine (FSM) governing versioned case status transitions.",
                        "generate_package.py": "Multi-form PDF generator stamping SQLite data into fillable government PDFs.",
                        "package_mappings.json": "Schema mapping dictionary connecting database fields to PDF form widget keys.",
                        "g-28_mapping.json": "Field mapping configuration specifically for Form G-28.",
                        "setup_database.py": "Database initialization script creating SQLite tables and seeding test records.",
                        "legal_crm.db": "Active SQLite database storing relational client, case, & audit log tables.",
                        "index.html": "Main interactive web dashboard for live DB editing, workflow state, & PDF export.",
                        "directory.html": "Live workspace directory browser displaying nested file trees & module descriptions."
                    }

                    try:
                        items = sorted(os.listdir(dir_path))
                    except Exception:
                        return []

                    for item in items:
                        if item in ['node_modules', '.git', '__pycache__', '.tempmediaStorage']:
                            continue
                        full_path = os.path.join(dir_path, item)
                        try:
                            rel_path = os.path.relpath(full_path, ROOT_DIR).replace('\\', '/')
                            is_dir = os.path.isdir(full_path)

                            entry = {
                                "name": item,
                                "path": rel_path,
                                "is_dir": is_dir,
                                "desc": descriptions.get(rel_path, "Directory" if is_dir else "Project File / Asset")
                            }
                            if is_dir:
                                entry["children"] = get_file_tree(full_path)
                            else:
                                entry["size"] = os.path.getsize(full_path)

                            tree.append(entry)
                        except Exception:
                            continue
                    return tree

                tree_data = get_file_tree(ROOT_DIR)
                self._send_json({"status": "SUCCESS", "tree": tree_data})
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, status_code=500)
            return

        return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        body = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}

        if path == '/api/login':
            username = body.get('username')
            repo = DatabaseRepository()
            try:
                session = repo.create_session(username)
                self._send_json({"status": "SUCCESS", "session": session})
            except ValueError as e:
                self._send_json({"status": "ERROR", "message": str(e)}, status_code=401)
            return

        # Every other POST mutates state and requires an authenticated session.
        # actor and role come from the session ONLY — never from the request body.
        session = self._get_session()
        if not session:
            self._send_json({"status": "ERROR", "message": "Authentication required: sign in to perform this action."}, status_code=401)
            return
        actor = session['username']
        role = session['role']

        if path == '/api/logout':
            auth = self.headers.get('Authorization', '')
            token = auth[len('Bearer '):].strip()
            DatabaseRepository().delete_session(token)
            self._send_json({"status": "SUCCESS", "message": f"Signed out {actor}."})
            return

        elif path == '/api/create-case':
            first_name = body.get('first_name')
            last_name = body.get('last_name')
            if not first_name or not last_name:
                self._send_json({"status": "ERROR", "message": "First Name and Last Name are required"}, status_code=400)
                return

            repo = DatabaseRepository()
            try:
                new_case_id = repo.create_new_case(
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=body.get('middle_name', ''),
                    phone=body.get('phone', ''),
                    street=body.get('street_address', ''),
                    apt=body.get('apt_ste_flr', ''),
                    city=body.get('city', ''),
                    state=body.get('state', ''),
                    zip_code=body.get('zip_code', ''),
                    form_type=body.get('form_type', 'G-28')
                )
                self._send_json({
                    "status": "SUCCESS",
                    "message": f"Successfully created case '{new_case_id}' for client '{first_name} {last_name}'",
                    "case_id": new_case_id
                })
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, status_code=500)
            return

        elif path == '/api/update-client':
            field = body.get('field')
            value = body.get('value')
            case_id = body.get('case_id', 'CASE-2026-001')
            expected_version = body.get('expected_version')

            repo = DatabaseRepository()
            try:
                repo.update_client_field(case_id, field, value, actor=actor, role=role, expected_version=expected_version)
                self._send_json({"status": "SUCCESS", "message": f"Updated {field} to '{value}' for {case_id} in SQLite Database"})
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, status_code=400)
            return

        elif path == '/api/transition':
            case_id = body.get('case_id', 'CASE-2026-001')
            action = body.get('action')
            expected_version = body.get('expected_version')

            repo = DatabaseRepository()
            try:
                new_state = repo.execute_versioned_transition(
                    case_id=case_id,
                    expected_version=expected_version,
                    action_name=action,
                    actor=actor,
                    role=role
                )
                self._send_json({"status": "SUCCESS", "message": f"Case {case_id} state transitioned to {new_state}", "new_state": new_state})
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, status_code=400)
            return

        elif path == '/api/reset-case':
            case_id = body.get('case_id', 'CASE-2026-001')
            repo = DatabaseRepository()
            try:
                new_version = repo.reset_case(case_id, actor=actor, role=role)
                self._send_json({"status": "SUCCESS", "message": f"Reset case {case_id} to DRAFT status (Version {new_version}). Audit trail preserved."})
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, status_code=400)
            return

        elif path == '/api/generate-pdf':
            case_id = body.get('case_id', 'CASE-2026-001')
            try:
                files = generate_multi_form_package(
                    case_id=case_id,
                    package_config_file="package_mappings.json"
                )
                file_list = []
                for code, path_out, count in files:
                    file_list.append({
                        "code": code,
                        "url": f"/{path_out.replace('\\\\', '/')}",
                        "fields_filled": count
                    })
                self._send_json({
                    "status": "SUCCESS",
                    "message": f"Generated official PDF package for {case_id} directly from live SQLite Database data!",
                    "files": file_list
                })
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, status_code=500)
            return

        self._send_json({"error": "Endpoint not found"}, status_code=404)

if __name__ == '__main__':
    print(f"Starting Legal CRM Prototype Web Server on http://localhost:{PORT}...")
    with socketserver.TCPServer(("", PORT), LegalCRMApiHandler) as httpd:
        httpd.serve_forever()
