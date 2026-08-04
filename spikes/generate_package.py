import fitz
import json
import os
from db_repository import DatabaseRepository

def get_db_value(db_data, db_path):
    parts = db_path.split('.')
    curr = db_data
    for p in parts:
        if isinstance(curr, dict) and p in curr:
            curr = curr[p]
        else:
            return None
    return curr

def generate_multi_form_package(case_id, package_config_file):
    # 1. Fetch domain model DIRECTLY from SQLite Database
    repo = DatabaseRepository()
    db_data = repo.fetch_case_data(case_id)
    if not db_data:
        raise ValueError(f"Case '{case_id}' not found in SQLite Database.")
        
    print(f"Loaded Case Data from SQLite for '{case_id}': Client = {db_data['client']['firstName']} {db_data['client']['lastName']}")

    # 2. Load master package mapping configuration
    with open(package_config_file, 'r') as f:
        pkg_config = json.load(f)
        
    generated_files = []
    os.makedirs('storage/3_exports', exist_ok=True)

    # 3. Iterate over every form in the package and populate into Bucket 3 (Exports)
    for form_code, form_info in pkg_config['forms'].items():
        template_pdf = form_info['pdf_template']
        mappings = form_info['mappings']
        output_pdf = f"storage/3_exports/{form_code.lower()}_package_generated.pdf"
        
        doc = fitz.open(template_pdf)
        filled_count = 0
        
        for page in doc:
            for widget in page.widgets():
                fname = widget.field_name
                if fname in mappings:
                    db_path = mappings[fname]['db_path']
                    val = get_db_value(db_data, db_path)
                    if val is not None:
                        widget.field_value = str(val)
                        widget.update()
                        filled_count += 1
                        
        doc.save(output_pdf)
        generated_files.append((form_code, output_pdf, filled_count))
        print(f"--> Successfully generated {form_code} PDF in Bucket 3 (Exports): {output_pdf} ({filled_count} fields populated)")

    return generated_files

if __name__ == '__main__':
    print("=" * 80)
    print("EXECUTING MULTI-FORM PACKAGE GENERATION FROM SQLITE DATABASE")
    print("=" * 80 + "\n")
    
    files = generate_multi_form_package(
        case_id="CASE-2026-001",
        package_config_file="package_mappings.json"
    )
    print("\nAll forms in the package generated successfully into Bucket 3 (Exports)!")
