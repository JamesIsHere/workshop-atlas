import fitz
import json

# Load mapping and client record
with open('g-28_mapping.json', 'r') as f:
    mapping_data = json.load(f)

mappings = mapping_data['mappings']

# Test values to write into PDF (incorporating intentional test cases)
pdf_fill_values = {
    # Attorney Fields
    "form1[0].#subform[0].Pt1Line2a_FamilyName[0]": "Rodriguez",         # Exact Match
    "form1[0].#subform[0].Pt1Line2b_GivenName[0]": "Maria",             # Exact Match
    "form1[0].#subform[0].Pt1Line2c_MiddleName[0]": "Elena",            # Exact Match
    "form1[0].#subform[0].#area[0].Pt1Line1_USCISOnlineAcctNumber[0]": "987654321098", # Exact Match
    "form1[0].#subform[0].Line4_DaytimeTelephoneNumber[0]": "(202) 555-0199", # Formatting variation! (DB has 202-555-0199)
    "form1[0].#subform[0].Line3a_StreetNumber[0]": "100 Pennsylvania Ave NW",
    "form1[0].#subform[0].Line3b_AptSteFlrNumber[0]": "Suite 400",
    "form1[0].#subform[0].Line3c_CityOrTown[0]": "Washington",
    "form1[0].#subform[0].Line3d_State[0]": "DC",
    "form1[0].#subform[0].Line3e_ZipCode[0]": "20006",
    
    # Client Fields
    "form1[0].#subform[1].Pt3Line5a_FamilyName[0]": "Smith",             # Exact Match
    "form1[0].#subform[1].Pt3Line5b_GivenName[0]": "Jonathon",          # MISMATCH! (DB has Jonathan, PDF filled as Jonathon)
    "form1[0].#subform[1].Pt3Line5c_MiddleName[0]": "Alexander",        # Exact Match
    "form1[0].#subform[1].Line10_MobileTelephoneNumber[0]": "202-555-0144", # Exact Match
    "form1[0].#subform[1].Line12a_StreetNumberName[0]": "500 7th Street",
    "form1[0].#subform[1].Line12b_AptSteFlrNumber[0]": "",               # MISSING IN PDF! (DB has Apt 2B, left blank on PDF)
    "form1[0].#subform[1].Line12c_CityOrTown[0]": "Washington",
    "form1[0].#subform[1].Line12d_State[0]": "DC",
    "form1[0].#subform[1].Line12e_ZipCode[0]": "20001"
}

doc = fitz.open('forms/g-28.pdf')

fill_count = 0
for page in doc:
    for widget in page.widgets():
        fname = widget.field_name
        if fname in pdf_fill_values:
            widget.field_value = pdf_fill_values[fname]
            widget.update()
            fill_count += 1

output_pdf = 'forms/g-28_filled.pdf'
doc.save(output_pdf)
print(f"Successfully populated {fill_count} fields in {output_pdf}")
