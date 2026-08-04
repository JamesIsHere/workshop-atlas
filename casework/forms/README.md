# forms/ -- starter-set form assets (U2.1)

Official agency AcroForm PDFs, imported as immutable data under P2
gate ruling 1 (official-AcroForm route). Never edited; a new agency
edition is a NEW file plus a new form_editions row via
app/forms.py new_edition(). schemas/ holds the authored per-edition
question schemas consumed by gen_seed.py; the db (form_editions.
schema_json) is the runtime authority, these files are its source.

## Provenance (verified 2026-08-01)

| File                             | Source                        | Edition   | sha256 (first 12) |
| -------------------------------- | ----------------------------- | --------- | ----------------- |
| g-28.pdf                         | spikes import; verified       | 09/17/18  | d73cd620d241      |
|                                  | field-identical to live       |           |                   |
|                                  | uscis.gov g-28.pdf same day   |           |                   |
| n-400.pdf                        | spikes import (uscis.gov)     | 01/20/25  | 8b33868ba071      |
| i-129.pdf                        | spikes import (uscis.gov)     | 02/27/26  | edc3cd0be3f7      |
| i-130.pdf                        | spikes import (uscis.gov)     | 04/01/24  | 7fc733d46399      |
| eta-9089.pdf                     | dol.gov one-time fetch        | 2023-FLAG | 5ced97733fb9      |
| eta-9089-appendix-a.pdf          | dol.gov one-time fetch        | 2023-FLAG | 74ac97c40c62      |
| eta-9089-appendix-b.pdf          | dol.gov one-time fetch        | 2023-FLAG | 5580d31dacd6      |
| eta-9089-appendix-d.pdf          | dol.gov one-time fetch        | 2023-FLAG | 93ec540316d7      |
| eta-9089-final-determination.pdf | dol.gov one-time fetch        | 2023-FLAG | e9cea9b761a0      |

DOL URLs: https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/
ETA-9089.pdf (+ -Appendix-A/-B/-D, -Final-Determination).

Edition note: uscis.gov serves G-28 edition 09/17/18 past its
printed OMB expiration (05/31/2021); the served edition is the
authority (live fetch beats the printed expiry and any prior).

## Schema format (schemas/*.json -> form_editions.schema_json)

- pdf: filename under pdfs/
- questions[]: key (q.<form>.<slug>), label, qtype, tab,
  repeating, pdf_fields[] (AcroForm fully-qualified names),
  source: one of
    {"fact": {"subject": "contact"|"matter", "key": <fact key>}}
    {"preparer": <field>}    -- preparer user / firm identity
    {"firm": <settings key>} -- firm_settings
    (absent)                 -- petition-specific -> form_answers
- attachments[]: {code, pdf, when: {question, equals}} --
  conditional parts (ETA-9089 appendices, final determination)

Invariant 1 is structural here: fact-sourced questions read/write
the fact store and never land in form_answers; only source-less
(petition-specific) questions do. The starter schemas are
REPRESENTATIVE subsets (content-class ruling): G-28 is the fullest;
each other form covers the mechanics it was chosen for. Library
growth is post-v1 content work.
