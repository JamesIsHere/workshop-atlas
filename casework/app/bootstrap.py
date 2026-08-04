"""Fresh-install bootstrap (U5.1): the app-owned install path.

A fresh database (schema.sql just applied) has no fact definitions and
no forms library; until P5 the synthetic seed was the only thing that
loaded them, which meant no cold-deployment path existed at all.
install() is the one place a fresh database gets its baseline
vocabulary. gen_seed.py imports BASELINE_FACT_DEFS from here so the
seed and a live install can never drift apart.
"""

from app import forms

BASELINE_FACT_DEFS = [
    # key, subject_type, value_type, label, repeating
    ("bio.given_name", "contact", "text", "Given name", 0),
    ("bio.family_name", "contact", "text", "Family name", 0),
    ("bio.middle_name", "contact", "text", "Middle name", 0),
    ("bio.date_of_birth", "contact", "date", "Date of birth", 0),
    ("bio.country_of_birth", "contact", "text", "Country of birth", 0),
    ("bio.marital_status", "contact", "list", "Marital status", 0),
    ("addr.street", "contact", "text", "Street address", 1),
    ("addr.city", "contact", "text", "City", 1),
    ("addr.state", "contact", "text", "State", 1),
    ("addr.zip", "contact", "text", "ZIP code", 1),
    ("addr.country", "contact", "text", "Country", 1),
    ("contact.email", "contact", "text", "Email address", 0),
    ("contact.phone", "contact", "text", "Phone number", 0),
    ("imm.a_number", "contact", "text", "A-Number", 0),
    ("imm.us_status", "contact", "text", "US immigration status", 0),
    ("imm.vmax_date", "contact", "date", "VMAX date", 0),
    # the eight built-in expiry-date types (fx-0147, U3.2)
    ("imm.us_status_expiry", "contact", "expiry", "US Status expiry", 0),
    ("imm.niv_expiry", "contact", "expiry", "Non-Immigrant Visa expiry", 0),
    ("imm.ap_expiry", "contact", "expiry", "Advanced Parole expiry", 0),
    ("imm.status_expiry", "contact", "expiry", "Current authorized stay expiry", 0),
    ("imm.ead_expiry", "contact", "expiry", "EAD expiry", 0),
    ("imm.petition_expiry", "contact", "expiry", "Petition expiration", 0),
    ("imm.passport_expiry", "contact", "expiry", "Passport or travel document expiry", 0),
    ("imm.lca_expiry", "contact", "expiry", "LCA expiration", 0),
    ("emp.employer_name", "contact", "text", "Employer name", 0),
    ("emp.job_title", "contact", "text", "Job title", 0),
    ("meta.unique_identifier", "contact", "text", "Firm unique identifier", 0),
    ("meta.synthetic", "contact", "boolean", "Synthetic record marker", 0),
    ("bio.prior_family_name", "contact", "text", "Other family names used", 1),
    ("bio.prior_given_name", "contact", "text", "Other given names used", 1),
]


def install(conn, now):
    """Load baseline vocabulary into a fresh schema: fact definitions
    plus the forms library. Call once, on a just-created database."""
    conn.executemany(
        "INSERT INTO fact_definitions (key, subject_type, value_type,"
        " label, repeating) VALUES (?,?,?,?,?)", BASELINE_FACT_DEFS)
    forms.load_library(conn, now)
