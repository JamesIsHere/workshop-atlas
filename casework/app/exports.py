"""CSV export (contacts-and-matters.csv-export, fx-0090/0155): the
Export button on the Contacts and Matters dashboards -- the full
record list as a CSV for local backup or offline use."""

import csv
import io

from app import facts

CONTACT_FACT_COLS = [("email", "contact.email"), ("phone", "contact.phone"),
                     ("a_number", "imm.a_number")]


def export_contacts_csv(conn):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "kind", "display_name"]
               + [c for c, _ in CONTACT_FACT_COLS] + ["archived", "created_at"])
    for r in conn.execute("SELECT * FROM contacts WHERE deleted_at IS NULL"
                          " ORDER BY id"):
        w.writerow([r["id"], r["kind"], r["display_name"]]
                   + [facts.get_fact(conn, "contact", r["id"], key) or ""
                      for _, key in CONTACT_FACT_COLS]
                   + ["yes" if r["archived_at"] else "no", r["created_at"]])
    return buf.getvalue()


def export_matters_csv(conn):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "name", "primary_contact", "matter_type", "status",
                "assignee", "archived", "created_at"])
    q = ("SELECT m.*, c.display_name AS primary_contact,"
         " mt.name AS type_name, ms.name AS status_name,"
         " u.name AS assignee_name"
         " FROM matters m JOIN contacts c ON c.id=m.primary_contact_id"
         " LEFT JOIN matter_types mt ON mt.id=m.matter_type_id"
         " LEFT JOIN matter_statuses ms ON ms.id=m.matter_status_id"
         " LEFT JOIN users u ON u.id=m.assignee_id"
         " WHERE m.deleted_at IS NULL ORDER BY m.id")
    for r in conn.execute(q):
        w.writerow([r["id"], r["name"], r["primary_contact"],
                    r["type_name"] or "", r["status_name"] or "",
                    r["assignee_name"] or "",
                    "yes" if r["archived_at"] else "no", r["created_at"]])
    return buf.getvalue()
