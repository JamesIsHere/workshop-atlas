import fitz
import json
import re
from db_repository import DatabaseRepository

def normalize_value(val, data_type):
    if val is None:
        return ""
    val = str(val).strip()
    
    if data_type == "phone":
        return re.sub(r'\D', '', val)
    elif data_type == "zip":
        digits = re.sub(r'\D', '', val)
        return digits[:5] if len(digits) >= 5 else digits
    elif data_type == "numeric_string":
        return re.sub(r'\D', '', val)
    else:
        return val.lower()

def get_db_value(db_data, db_path):
    parts = db_path.split('.')
    curr = db_data
    for p in parts:
        if isinstance(curr, dict) and p in curr:
            curr = curr[p]
        else:
            return None
    return curr

def run_pdf_diff_from_db(case_id, pdf_path="storage/2_intake_scans/g-28_filled.pdf", mapping_path="g-28_mapping.json"):
    # 1. Fetch domain model DIRECTLY from SQLite Database via Repository!
    repo = DatabaseRepository()
    db_data = repo.fetch_case_data(case_id)
    if not db_data:
        raise ValueError(f"Case '{case_id}' not found in SQLite Database.")
        
    # 2. Load PDF mapping dictionary
    with open(mapping_path, 'r') as f:
        mapping_config = json.load(f)
    mappings = mapping_config['mappings']
    
    # 3. Open PDF and extract values
    doc = fitz.open(pdf_path)
    extracted_pdf_values = {}
    for page in doc:
        for widget in page.widgets():
            if widget.field_name:
                extracted_pdf_values[widget.field_name] = widget.field_value or ""
                
    # 4. Compare DB data vs PDF data
    diff_results = []
    for pdf_field_name, rule in mappings.items():
        target_db_path = rule['db_path']
        label = rule['label']
        data_type = rule['data_type']
        
        raw_db_val = get_db_value(db_data, target_db_path) or ""
        raw_pdf_val = extracted_pdf_values.get(pdf_field_name, "")
        
        norm_db_val = normalize_value(raw_db_val, data_type)
        norm_pdf_val = normalize_value(raw_pdf_val, data_type)
        
        if not raw_pdf_val and raw_db_val:
            status = "MISSING_IN_PDF"
        elif raw_pdf_val and not raw_db_val:
            status = "MISSING_IN_DB"
        elif norm_db_val == norm_pdf_val:
            if raw_db_val == raw_pdf_val:
                status = "MATCH"
            else:
                status = "FORMATTING_MATCH"
        else:
            status = "MISMATCH"
            
        diff_results.append({
            "label": label,
            "raw_db_value": raw_db_val,
            "raw_pdf_value": raw_pdf_val,
            "status": status
        })
        
    return db_data["case_info"], diff_results

if __name__ == '__main__':
    case_info, results = run_pdf_diff_from_db(
        case_id="CASE-2026-001",
        pdf_path="storage/2_intake_scans/g-28_filled.pdf",
        mapping_path="g-28_mapping.json"
    )
    
    print(f"AUTOMATED AUDIT REPORT FOR {case_info['case_id']} (Form: {case_info['form_type']}, Status: {case_info['status']}, Version: {case_info['version']})")
    print(f"Source Data: SQLite Database 'legal_crm.db'\n")
    
    print(f"{'Field Label':<35} | {'SQL DB Value':<20} | {'Raw PDF Value':<20} | {'Status'}")
    print("=" * 100)
    for r in results:
        print(f"{r['label']:<35} | {r['raw_db_value']:<20} | {r['raw_pdf_value']:<20} | {r['status']}")
