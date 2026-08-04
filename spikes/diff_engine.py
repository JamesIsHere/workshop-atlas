import fitz
import json
import re

def normalize_value(val, data_type):
    """Normalizes raw input strings based on the data_type hint."""
    if val is None:
        return ""
    val = str(val).strip()
    
    if data_type == "phone":
        # Strip all non-digit characters (e.g., "(202) 555-0199" -> "2025550199")
        return re.sub(r'\D', '', val)
    elif data_type == "zip":
        # Keep only digits, or take first 5 digits of Zip+4
        digits = re.sub(r'\D', '', val)
        return digits[:5] if len(digits) >= 5 else digits
    elif data_type == "numeric_string":
        # Strip non-digits
        return re.sub(r'\D', '', val)
    else: # Default "string"
        # Trim whitespace and normalize to lowercase for case-insensitive comparison
        return val.lower()

def get_db_value(db_data, db_path):
    """Navigates dot-notation paths (e.g. 'attorney.lastName') inside nested JSON dicts."""
    parts = db_path.split('.')
    curr = db_data
    for p in parts:
        if isinstance(curr, dict) and p in curr:
            curr = curr[p]
        else:
            return None
    return curr

def run_pdf_diff(pdf_path, mapping_path, db_path):
    # 1. Load mapping and DB JSON files
    with open(mapping_path, 'r') as f:
        mapping_config = json.load(f)
    mappings = mapping_config['mappings']
    
    with open(db_path, 'r') as f:
        db_data = json.load(f)
        
    # 2. Open PDF and extract actual field values
    doc = fitz.open(pdf_path)
    extracted_pdf_values = {}
    for page in doc:
        for widget in page.widgets():
            if widget.field_name:
                extracted_pdf_values[widget.field_name] = widget.field_value or ""
                
    # 3. Compare DB values vs PDF values
    diff_results = []
    
    for pdf_field_name, rule in mappings.items():
        target_db_path = rule['db_path']
        label = rule['label']
        data_type = rule['data_type']
        
        raw_db_val = get_db_value(db_data, target_db_path) or ""
        raw_pdf_val = extracted_pdf_values.get(pdf_field_name, "")
        
        norm_db_val = normalize_value(raw_db_val, data_type)
        norm_pdf_val = normalize_value(raw_pdf_val, data_type)
        
        # 4. Classify status
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
            "field_label": label,
            "db_path": target_db_path,
            "raw_db_value": raw_db_val,
            "raw_pdf_value": raw_pdf_val,
            "data_type": data_type,
            "status": status
        })
        
    return diff_results

if __name__ == '__main__':
    results = run_pdf_diff(
        pdf_path='forms/g-28_filled.pdf',
        mapping_path='g-28_mapping.json',
        db_path='client_record.json'
    )
    
    # Print formatted summary table
    print(f"{'Field Label':<35} | {'Raw DB Value':<20} | {'Raw PDF Value':<20} | {'Status'}")
    print("=" * 100)
    for r in results:
        print(f"{r['field_label']:<35} | {r['raw_db_value']:<20} | {r['raw_pdf_value']:<20} | {r['status']}")
