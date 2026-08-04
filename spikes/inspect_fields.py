import pypdf

reader = pypdf.PdfReader('forms/g-28.pdf')
fields = reader.get_fields()

print(f"Total fields in G-28: {len(fields)}\n")
print(f"{'Internal AcroForm Field Name':<60} | {'Field Type':<12} | {'Tooltip / Alt Text (/TU)'}")
print("-" * 120)

count = 0
for name, obj in fields.items():
    ft = str(obj.get('/FT', 'Unknown'))
    tu = str(obj.get('/TU', '')) # Tooltip / Alternative Text in PDF object which often contains the printed label!
    v = str(obj.get('/V', ''))
    print(f"{name:<60} | {ft:<12} | {tu}")
    count += 1
    if count >= 15:
        break
