import sqlite3
import os

DB_FILE = 'legal_crm.db'

def init_database():
    # Remove existing db file if we want a fresh start
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Unified People Table (Directory of all Humans: Clients, Attorneys, Paralegals, Sponsors)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        middle_name TEXT,
        phone TEXT,
        street_address TEXT,
        apt_ste_flr TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        a_number TEXT,
        ssn TEXT,
        dob TEXT,
        country_citizenship TEXT,
        uscis_online_acct TEXT,
        person_type TEXT NOT NULL DEFAULT 'CLIENT',
        username TEXT UNIQUE,
        role TEXT
    );
    """)

    # 2. Cases Fact Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        assigned_attorney_id INTEGER NOT NULL,
        form_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'DRAFT',
        version INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (assigned_attorney_id) REFERENCES people(id)
    );
    """)

    # 3. Case Parties Junction / Bridge Table (Associates People with Cases under explicit Roles)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS case_parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        person_id INTEGER NOT NULL,
        role_type TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE,
        FOREIGN KEY (person_id) REFERENCES people(id),
        UNIQUE(case_id, person_id, role_type)
    );
    """)

    # 4. Audit Logs Table (Immutable Change History & Security Record)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        version INTEGER NOT NULL,
        actor TEXT NOT NULL,
        role TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(case_id)
    );
    """)

    # 5. Sessions Table (server-side identity: token -> person. Role is NEVER taken from the client.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        person_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (person_id) REFERENCES people(id)
    );
    """)

    # 6. Insert Rich Seed Data
    # Person 1: Attorney Rodriguez (staff login: attorney_rodriguez)
    cursor.execute("""
    INSERT INTO people (first_name, last_name, middle_name, uscis_online_acct, phone, street_address, apt_ste_flr, city, state, zip_code, person_type, username, role)
    VALUES ('Maria', 'Rodriguez', 'Elena', '987654321098', '202-555-0199', '100 Pennsylvania Ave NW', 'Suite 400', 'Washington', 'DC', '20006', 'ATTORNEY', 'attorney_rodriguez', 'Attorney');
    """)
    attorney_id = cursor.lastrowid

    # Staff members: Legal Assistant and Paralegal (login accounts for the workflow roles)
    cursor.execute("""
    INSERT INTO people (first_name, last_name, phone, city, state, person_type, username, role)
    VALUES ('Sam', 'Carter', '202-555-0101', 'Washington', 'DC', 'STAFF', 'assistant_sam', 'Legal Assistant');
    """)
    cursor.execute("""
    INSERT INTO people (first_name, last_name, phone, city, state, person_type, username, role)
    VALUES ('Maria', 'Lopez', '202-555-0102', 'Washington', 'DC', 'STAFF', 'paralegal_maria', 'Paralegal');
    """)

    # Person 2: Client / Petitioner (Jonathan Smith)
    cursor.execute("""
    INSERT INTO people (first_name, last_name, middle_name, phone, street_address, apt_ste_flr, city, state, zip_code, ssn, dob, country_citizenship, person_type)
    VALUES ('Jonathan', 'Smith', 'Alexander', '202-555-0144', '500 7th Street', 'Apt 2B', 'Washington', 'DC', '20001', '000-12-3456', '1988-04-12', 'United States', 'CLIENT');
    """)
    petitioner_id = cursor.lastrowid

    # Person 3: Client / Beneficiary (Elena Smith)
    cursor.execute("""
    INSERT INTO people (first_name, last_name, middle_name, phone, street_address, apt_ste_flr, city, state, zip_code, a_number, ssn, dob, country_citizenship, person_type)
    VALUES ('Elena', 'Smith', 'Sophia', '202-555-0188', '500 7th Street', 'Apt 2B', 'Washington', 'DC', '20001', 'A999888777', '000-98-7654', '1992-09-25', 'Colombia', 'CLIENT');
    """)
    beneficiary_id = cursor.lastrowid

    # Case 1: CASE-2026-001 (Marriage Package)
    cursor.execute("""
    INSERT INTO cases (case_id, assigned_attorney_id, form_type, status, version)
    VALUES ('CASE-2026-001', ?, 'G-28', 'DRAFT', 1);
    """, (attorney_id,))

    # Bridge Table Connections for CASE-2026-001
    cursor.execute("""
    INSERT INTO case_parties (case_id, person_id, role_type)
    VALUES ('CASE-2026-001', ?, 'PETITIONER');
    """, (petitioner_id,))

    cursor.execute("""
    INSERT INTO case_parties (case_id, person_id, role_type)
    VALUES ('CASE-2026-001', ?, 'BENEFICIARY');
    """, (beneficiary_id,))

    # Audit Log Initial Entry
    cursor.execute("""
    INSERT INTO audit_logs (case_id, version, actor, role, action, details)
    VALUES ('CASE-2026-001', 1, 'system', 'System', 'CASE_CREATED', 'Initialized CASE-2026-001 with Petitioner Jonathan Smith and Beneficiary Elena Smith');
    """)

    conn.commit()
    conn.close()
    print(f"Successfully initialized Option B database schema in '{DB_FILE}'!")

if __name__ == '__main__':
    init_database()
