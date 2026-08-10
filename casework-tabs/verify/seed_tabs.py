"""Demo seed for the per-tab hands-on gates (plan.md P0): realistic
synthetic volume across all six tab domains so gate screens are
judged at n>1, not against near-empty tables.

Casework/app modules ONLY -- this file writes zero SQL. The db is
created through app_ui's own make_server path (install + synthetic
marker included), then populated by module calls, exactly the way
the UI itself writes. The WALK never uses this db; the rail runs on
fresh empty databases by contract.

Deterministic by design: fixed dates, fixed content -- regenerating
yields the same records (e-sign request tokens are the one random
element, generated inside the frozen core). Regenerated, never
hand-edited.

Run (from casework-tabs/): python verify/seed_tabs.py
Writes data/demo-tabs.db and prints the summary. Login for gate
reviews: demo.tabs@synthetic.test / demo-tabs-pass (MFA code shown
in the mailbox panel).
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS = HERE.parent.parent
CASEWORK_UI = ATLAS / "casework-ui"
sys.path.insert(0, str(CASEWORK_UI))

import app_ui  # noqa: F401, E402  (wires casework onto sys.path)
from app_ui import server as ui_server  # noqa: E402
from app import auth, billing, contacts, esign, events  # noqa: E402
from app import expiry, facts, files, matters, notes  # noqa: E402
from app import search, tasks, trash, users  # noqa: E402

DB = HERE.parent / "data" / "demo-tabs.db"

ADMIN_EMAIL = "demo.tabs@synthetic.test"
ADMIN_PASS = "demo-tabs-pass"

NOW = "2026-08-10T00:00:00Z"
AUG = ["2026-08-%02d" % d for d in range(1, 32)]
SEP = ["2026-09-%02d" % d for d in range(1, 31)]


# Minimal valid single-page PDF for e-sign candidates (mirrors the
# rail's helper; duplicated so the seed stays runnable stand-alone).
def tiny_pdf(text):
    objs = ["<</Type /Catalog /Pages 2 0 R>>",
            "<</Type /Pages /Kids [3 0 R] /Count 1>>",
            "<</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]"
            " /Contents 4 0 R /Resources <</Font <</F1 5 0 R>>>>>>",
            None,
            "<</Type /Font /Subtype /Type1 /BaseFont /Helvetica>>"]
    stream = (f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET").encode()
    objs[3] = (f"<</Length {len(stream)}>>\nstream\n".encode()
               + stream + b"\nendstream")
    out = b"%PDF-1.4\n"
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        body = o if isinstance(o, bytes) else o.encode()
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<</Size {len(objs) + 1} /Root 1 0 R>>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    return out


def main():
    if DB.exists():
        DB.unlink()  # generated artifact; regenerated every run
    httpd = ui_server.make_server(DB)
    conn = httpd.app_conn
    storage = DB.parent / "storage"
    try:
        # --- firm: admin + two staff (one deactivated for browse) ---
        admin = users.create_user(conn, ADMIN_EMAIL, "Demo Reviewer",
                                  NOW, role_label="Managing Attorney")
        users.update_user(conn, admin, is_admin=1, is_owner=1)
        auth.set_password(conn, admin, ADMIN_PASS)
        status, token = auth.login(conn, ADMIN_EMAIL, ADMIN_PASS, NOW)
        assert status == "enrollment_required", status
        auth.enroll_twofa(conn, admin, "email", token, NOW)
        conn.actor.set("user", admin)
        para = users.create_user(conn, "sasha.para@synthetic.test",
                                 "Sasha Paralegal", NOW,
                                 role_label="Paralegal")
        gone = users.create_user(conn, "former.staff@synthetic.test",
                                 "Former Staff", NOW,
                                 role_label="Associate")
        users.deactivate_user(conn, gone, NOW)

        # --- clients and matters ---
        c = {}
        for given in ("Anya", "Boris", "Chloe", "Dmitri"):
            c[given] = contacts.create_contact(
                conn, "person", NOW, admin, given_name=given,
                family_name="Synthetic",
                email=f"{given.lower()}.client@synthetic.test")
        m = {
            "anya": matters.create_matter(
                conn, "Anya Synthetic I-130", c["Anya"], NOW, admin),
            "boris": matters.create_matter(
                conn, "Boris Synthetic H-1B", c["Boris"], NOW, admin),
            "chloe": matters.create_matter(
                conn, "Chloe Synthetic N-400", c["Chloe"], NOW, admin),
            "dmitri": matters.create_matter(
                conn, "Dmitri Synthetic I-485", c["Dmitri"], NOW,
                admin),
        }

        # --- calendar: default reminders, appointments, expiry
        # rules -> auto events, vmax dates ---
        events.set_default_reminders(
            conn, [{"value": 1, "unit": "days"}])
        appts = [
            ("SYNTH USCIS interview prep", AUG[11], "15:00", "16:00",
             "Anya", "anya"),
            ("SYNTH H-1B strategy call", AUG[13], "10:00", "10:30",
             "Boris", "boris"),
            ("SYNTH N-400 biometrics", AUG[17], "09:00", "09:30",
             "Chloe", "chloe"),
            ("SYNTH RFE working session", AUG[20], "14:00", "15:30",
             "Dmitri", "dmitri"),
            ("SYNTH firm case review", SEP[1], "13:00", "14:00",
             None, None),
        ]
        n_events = 0
        for title, day, t0, t1, given, mk in appts:
            eid = events.create_event(
                conn, title, f"{day}T{t0}:00Z", NOW, admin,
                description=f"{title} (synthetic)",
                ends_at=f"{day}T{t1}:00Z",
                contact_id=c[given] if given else None,
                matter_id=m[mk] if mk else None)
            events.add_attendee(conn, eid, user_id=admin)
            if given:
                events.add_attendee(conn, eid, contact_id=c[given])
            n_events += 1
        expiry.configure_reminder(conn, "imm.ead_expiry", 30, "admin")
        expiry.configure_reminder(conn, "imm.passport_expiry", 60,
                                  "admin")
        expiry.set_expiry_date(conn, c["Anya"], "imm.ead_expiry",
                               SEP[24], NOW)
        expiry.set_expiry_date(conn, c["Boris"], "imm.passport_expiry",
                               "2026-10-15", NOW)
        expiry.set_expiry_date(conn, c["Chloe"], "imm.ead_expiry",
                               "2026-11-30", NOW)
        facts.set_fact(conn, "contact", c["Boris"], "imm.vmax_date",
                       "2027-03-01", NOW)
        facts.set_fact(conn, "contact", c["Dmitri"], "imm.vmax_date",
                       "2026-12-20", NOW)

        # --- invoices with due dates (calendar invoice kind +
        # search coverage of display codes) ---
        op = billing.create_bank_account(conn, "operating_bank",
                                         "SYNTH Operating", admin)
        assert op is not None
        inv_a = billing.create_invoice(conn, "bill", c["Anya"], admin,
                                       AUG[0], matter_id=m["anya"])
        billing.add_charge(conn, inv_a, "service",
                           "SYNTH I-130 preparation", 250000, admin,
                           charge_date=AUG[0])
        billing.update_invoice_settings(conn, inv_a,
                                        due_date=AUG[29])
        inv_b = billing.create_invoice(conn, "bill", c["Boris"], admin,
                                       AUG[2], matter_id=m["boris"])
        billing.add_charge(conn, inv_b, "service",
                           "SYNTH H-1B preparation", 350000, admin,
                           charge_date=AUG[2])
        billing.update_invoice_settings(conn, inv_b,
                                        due_date=SEP[14])

        # --- tasks: open mine, others', completed, dued ---
        t1 = tasks.create_task(conn, "SYNTH draft I-130 cover letter",
                               NOW, admin, matter_id=m["anya"],
                               due_date=AUG[24])
        tasks.create_task(conn, "SYNTH assemble H-1B exhibits", NOW,
                          admin, matter_id=m["boris"],
                          due_date=AUG[27])
        tasks.create_task(conn, "SYNTH request tax transcripts", NOW,
                          admin, contact_id=c["Chloe"],
                          assignee_id=para)
        done = tasks.create_task(conn, "SYNTH open the client file",
                                 NOW, admin, matter_id=m["anya"])
        tasks.complete_task(conn, done, NOW)
        # a completed task that STAYS visible (the one above rides
        # into trash below) -- the gate's Reopen target
        done2 = tasks.create_task(
            conn, "SYNTH confirm biometrics attendance", NOW, admin,
            matter_id=m["chloe"])
        tasks.complete_task(conn, done2, NOW)
        tl = tasks.create_task_list(conn, "SYNTH I-130 checklist")
        tasks.add_list_item(conn, tl, "SYNTH gather civil documents",
                            1, duration_days=7)
        tasks.add_list_item(conn, tl, "SYNTH prepare G-28", 2,
                            duration_days=3)
        tasks.add_list_item(conn, tl, "SYNTH file before EAD expiry",
                            3, ref_fact_key="imm.ead_expiry",
                            ref_direction="before", ref_days=30)
        tasks.import_task_list(conn, tl, NOW, admin,
                               matter_id=m["anya"])
        # workflow automation (P2 gate: the builder's Automations
        # column renders this linkage; no UI creates workflows --
        # config-depth kill, so it exists only on seeded dbs).
        # Evgenia's matter enters "SYNTH Opened" at creation, the
        # status auto-imports the checklist: her tasks arrive
        # UNASSIGNED (firm scope shows them, my-open does not) and
        # the EAD reference item computes its due date from her
        # fact.
        c["Evgenia"] = contacts.create_contact(
            conn, "person", NOW, admin, given_name="Evgenia",
            family_name="Synthetic",
            email="evgenia.client@synthetic.test")
        expiry.set_expiry_date(conn, c["Evgenia"], "imm.ead_expiry",
                               SEP[29], NOW)
        mt_i130 = matters.create_matter_type(conn, "SYNTH I-130"
                                             " Family")
        st_open = matters.add_status(conn, mt_i130, "SYNTH Opened",
                                     1, auto_task_list_id=tl)
        m["evgenia"] = matters.create_matter(
            conn, "Evgenia Synthetic I-130", c["Evgenia"], NOW,
            admin, matter_type_id=mt_i130, matter_status_id=st_open)

        # --- notes: categories, pins, notify-all ---
        cat_strategy = notes.create_category(conn, "SYNTH Strategy")
        cat_call = notes.create_category(conn, "SYNTH Client call")
        n1 = notes.create_note(
            conn, "SYNTH consular processing is the faster route"
            " here; adjustment adds nine months.", NOW, admin,
            title="SYNTH strategy memo", matter_id=m["anya"],
            category_id=cat_strategy)
        notes.pin(conn, n1)
        notes.create_note(
            conn, "SYNTH client called about the biometrics"
            " appointment; rescheduled to the 17th.", NOW, admin,
            title="SYNTH call log", contact_id=c["Chloe"],
            category_id=cat_call)
        notes.create_note(
            conn, "SYNTH premium processing fee increase takes"
            " effect in October -- flag on all open H-1Bs.", NOW,
            admin, title="SYNTH firm-wide flag",
            matter_id=m["boris"], notify_all=1)
        trash_note = notes.create_note(
            conn, "SYNTH obsolete draft note (trash browse).", NOW,
            admin, title="SYNTH obsolete draft",
            contact_id=c["Dmitri"])

        # --- files: folders, uploads, rename, e-sign states ---
        folder = files.create_folder(conn, "SYNTH Civil documents",
                                     NOW, matter_id=m["anya"],
                                     user_id=admin)
        f1 = files.upload_file(
            conn, "SYNTH-birth-certificate.txt",
            b"SYNTH scanned birth certificate.\n", NOW, storage,
            matter_id=m["anya"], folder_id=folder, user_id=admin)
        files.upload_file(
            conn, "SYNTH-passport-scan.txt",
            b"SYNTH scanned passport bio page.\n", NOW, storage,
            contact_id=c["Boris"], user_id=admin)
        files.rename(conn, "file", f1,
                     "SYNTH-birth-certificate-certified.txt")
        g28 = files.upload_file(
            conn, "SYNTH-g28-anya.pdf", tiny_pdf("SYNTH G-28 Anya"),
            NOW, storage, matter_id=m["anya"], user_id=admin)
        retainer = files.upload_file(
            conn, "SYNTH-retainer-boris.pdf",
            tiny_pdf("SYNTH Retainer Boris"), NOW, storage,
            matter_id=m["boris"], user_id=admin)
        # a produced-custody artifact so the index's source filter
        # has all live arms at the gate (client source needs the
        # intake flow; out of a seed's reach by design)
        files.save_produced(
            conn, "SYNTH-g28-anya-filled.pdf",
            tiny_pdf("SYNTH filled G-28"), NOW, storage,
            contact_id=c["Anya"], matter_id=m["anya"])
        es_draft = esign.prepare(conn, g28, NOW, admin)
        s1 = esign.add_signer(conn, es_draft, contact_id=c["Anya"])
        esign.add_field(conn, es_draft, s1, "signature", 1, 100, 600)
        es_req = esign.prepare(conn, retainer, NOW, admin)
        s2 = esign.add_signer(conn, es_req, contact_id=c["Boris"])
        esign.add_field(conn, es_req, s2, "signature", 1, 100, 600)
        esign.request_signatures(conn, es_req, NOW)

        # --- search recents ---
        search.open_record(conn, admin, "contact", c["Anya"], NOW)
        search.open_record(conn, admin, "matter", m["boris"], NOW)
        search.open_record(conn, admin, "contact", c["Chloe"], NOW)

        # --- trash browse content ---
        trash.soft_delete(conn, "notes", trash_note, admin, NOW)
        trash.soft_delete(conn, "tasks", done, admin, NOW)
        conn.commit()

        counts = {}
        for label, table in (("users", "users"),
                             ("contacts", "contacts"),
                             ("matters", "matters"),
                             ("events", "events"),
                             ("tasks", "tasks"),
                             ("notes", "notes"),
                             ("files", "files"),
                             ("invoices", "invoices")):
            counts[label] = conn.execute(
                "SELECT count(*) FROM " + table).fetchone()[0]
        assert t1 is not None
    finally:
        httpd.client_httpd.server_close()
        httpd.server_close()
        conn.close()

    print("seed_tabs: " + "; ".join(
        f"{v} {k}" for k, v in counts.items()))
    print(f"db: {DB}")
    print(f"login: {ADMIN_EMAIL} / {ADMIN_PASS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
