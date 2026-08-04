"""Submission-ready packages (U2.7). E-filing family, adapted by
map ratification: government submission is out; v1 proves the
validated questionnaire -> submission-ready artifact chain (form
PDF + structured field payload, G-28 attached)."""

import json

from app import facts, forms, intake, render


class EfilingBlocked(Exception):
    """Raised when export is attempted with a failing validation.
    Carries the per-question error list."""

    def __init__(self, errors):
        super().__init__(f"{len(errors)} validation errors")
        self.errors = errors


def _efilable_sffs(conn, smart_form_id):
    out = []
    for sff in forms.forms_of(conn, smart_form_id):
        efilable = conn.execute(
            "SELECT efilable FROM form_definitions WHERE code=?",
            (sff["form_code"],)).fetchone()["efilable"]
        if efilable and sff["form_code"] != "g-28":
            out.append(sff)
    return out


def validate(conn, smart_form_id):
    """Per-question validation of the efilable forms' questionnaire:
    every client-side, non-boolean, non-repeating question needs a
    value. Returns the error list -- one entry per question with a
    Go-to-question link and explanation (fx-0016/0017/0022)."""
    errors = []
    seen = set()
    for sff in _efilable_sffs(conn, smart_form_id):
        schema = forms.schema_of(conn, sff["form_edition_id"])
        for q in schema["questions"]:
            source = q.get("source") or {}
            if "preparer" in source or "firm" in source or \
                    "registry" in source:
                continue  # firm-side data, not questionnaire completeness
            if q["qtype"] in ("boolean", "document_request"):
                continue
            if q.get("repeating"):
                continue
            if q["key"] in seen:
                continue
            seen.add(q["key"])
            vals = render.resolve_question(conn, smart_form_id, q)
            if not any(v not in (None, "") for v in vals):
                errors.append({
                    "question": q["key"], "label": q["label"],
                    "tab": q["tab"],
                    "link": f"/intake/{smart_form_id}/question/{q['key']}",
                    "reason": "This question has no answer."})
    return errors


def export_package(conn, smart_form_id, out_dir, workdir):
    """Validated questionnaire -> submission-ready package: each
    efilable form in efile_package mode becomes a rendered artifact
    plus a structured field payload, with the attached G-28 rendered
    alongside (fx-0017). Blocked while validation fails."""
    errors = validate(conn, smart_form_id)
    if errors:
        raise EfilingBlocked(errors)
    targets = [sff for sff in _efilable_sffs(conn, smart_form_id)
               if sff["mode"] == "efile_package"]
    if not targets:
        raise ValueError("no included form is in efile_package mode")
    g28 = next((sff for sff in forms.forms_of(conn, smart_form_id)
                if sff["form_code"] == "g-28"), None)
    if g28 is None:
        raise ValueError("an e-file package carries an attached G-28"
                         " (fx-0017); include one")
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"smart_form_id": smart_form_id, "forms": []}
    for sff in targets:
        pdf_path = out_dir / f"{sff['form_code']}.pdf"
        render.render_form(conn, sff["id"], pdf_path)
        payload = {"form_code": sff["form_code"],
                   "edition": sff["edition"],
                   "fields": render.db_values(conn, sff["id"])}
        payload_path = out_dir / f"{sff['form_code']}.json"
        payload_path.write_text(json.dumps(payload, indent=2),
                                encoding="utf-8")
        manifest["forms"].append(sff["form_code"])
    render.render_form(conn, g28["id"], out_dir / "g-28.pdf")
    manifest["attached_g28"] = True
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2),
                                           encoding="utf-8")
    return manifest


def toggle_paper(conn, smart_form_id, mode):
    """Switch the N-400 between e-file-package and paper without
    recreating the intake (fx-0017: currently N-400 + G-28 only)."""
    if mode not in ("paper", "efile_package"):
        raise ValueError("mode is paper or efile_package")
    row = next((sff for sff in forms.forms_of(conn, smart_form_id)
                if sff["form_code"] == "n-400"), None)
    if row is None:
        raise ValueError("the electronic/paper toggle is supported for"
                         " the N-400 (fx-0017)")
    conn.execute("UPDATE smart_form_forms SET mode=? WHERE id=?",
                 (mode, row["id"]))
    return row["id"]


# --- H-1B electronic registration (adapted) ---

MAX_BENEFICIARIES = 20


def create_h1b_registration(conn, employer_contact_id,
                            beneficiary_contact_ids, title, now,
                            created_by):
    """Bulk registration instance: the employer plus up to 20
    selected prospective employees on ONE registration Smart Form
    (fx-0013). E-filing itself is out by adaptation."""
    ids = list(beneficiary_contact_ids)
    if not ids:
        raise ValueError("select at least one prospective employee")
    if len(ids) > MAX_BENEFICIARIES:
        raise ValueError(f"bulk preparation is limited to"
                         f" {MAX_BENEFICIARIES} beneficiaries (fx-0013)")
    sfid = forms.create_smart_form(conn, title, now, created_by,
                                   contact_id=employer_contact_id,
                                   kind="h1b_registration")
    forms.assign_role(conn, sfid, "employer", employer_contact_id)
    for i, cid in enumerate(ids, 1):
        forms.assign_role(conn, sfid, f"beneficiary_{i}", cid)
    return sfid


def registration_payload(conn, smart_form_id):
    """Structured registration data for the instance: employer +
    every selected beneficiary, from the fact store."""
    kind = conn.execute("SELECT kind FROM smart_forms WHERE id=?",
                        (smart_form_id,)).fetchone()["kind"]
    if kind != "h1b_registration":
        raise ValueError("not an H-1B registration instance")
    employer_id = forms.role_contact(conn, smart_form_id, "employer")
    employer = conn.execute("SELECT display_name FROM contacts WHERE id=?",
                            (employer_id,)).fetchone()["display_name"]
    beneficiaries = []
    for r in conn.execute(
            "SELECT role, contact_id FROM smart_form_contacts WHERE"
            " smart_form_id=? AND role LIKE 'beneficiary_%'"
            " ORDER BY CAST(substr(role, 13) AS INTEGER)",
            (smart_form_id,)):
        cid = r["contact_id"]
        beneficiaries.append({
            "contact_id": cid,
            "given_name": facts.get_fact(conn, "contact", cid,
                                         "bio.given_name"),
            "family_name": facts.get_fact(conn, "contact", cid,
                                          "bio.family_name")})
    return {"employer": employer, "beneficiaries": beneficiaries}
