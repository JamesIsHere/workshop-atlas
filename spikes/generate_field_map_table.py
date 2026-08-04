import fitz

doc = fitz.open('forms/g-28.pdf')
page0 = doc[0]

rows = []
for w in page0.widgets():
    full_name = w.field_name or ''
    # Extract short name
    short_name = full_name.split('.')[-1] if '.' in full_name else full_name
    field_type = w.field_type_string
    
    # Get PDF dictionary tooltip (/TU)
    # in fitz, tooltip is w.field_label
    tooltip = w.field_label or ''
    
    rows.append((short_name, full_name, field_type, tooltip))

print(f"Total fields on page 1: {len(rows)}")
for r in rows[:10]:
    print(r)
