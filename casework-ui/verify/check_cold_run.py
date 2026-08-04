"""Cold-run artifact check (U3.4): the db receipts a passing run
MUST leave behind. Born from the 2026-08-03 rehearsal, which
produced a filled G-28 while skipping the invitation and client
intake leg entirely and never saving the deadline -- none of which
the eyeball-only pass criteria caught.

Read-only assertions against the run's db. The proctor runs this
untimed, after "done":

    python verify/check_cold_run.py data/cold-run-<date>.db

Exit 0 iff every artifact check passes. The PDF check (opens,
family name present) stays manual -- downloads leave no db trace.
"""

import sqlite3
import sys
from pathlib import Path

FIRM_EMAIL = "casey.op@synthetic.test"
CLIENT = {"bio.family_name": "Sharma",
          "bio.given_name": "Priya",
          "contact.email": "priya.client@synthetic.test"}


def checks(conn):
    one = lambda q, *p: conn.execute(q, p).fetchone()[0]  # noqa: E731

    yield ("synthetic marker present",
           one("SELECT count(*) FROM synthetic_marker") > 0, "")

    n = one("SELECT count(*) FROM users WHERE deleted_at IS NULL")
    admin = conn.execute(
        "SELECT email FROM users ORDER BY id LIMIT 1").fetchone()
    yield ("firm card followed (account is Casey)",
           n == 1 and admin is not None and admin[0] == FIRM_EMAIL,
           f"users={n}, email={admin[0] if admin else None!r}")

    bad = []
    for key, want in CLIENT.items():
        got = conn.execute(
            "SELECT value FROM facts WHERE subject_type='contact'"
            " AND key=?", (key,)).fetchone()
        if got is None or got[0] != want:
            bad.append(f"{key}={got[0] if got else None!r}")
    yield ("client card followed (Priya's facts match)",
           not bad, "; ".join(bad))

    yield ("matter exists with Priya as primary contact",
           one("SELECT count(*) FROM matters WHERE deleted_at IS NULL"
               " AND primary_contact_id IS NOT NULL") > 0, "")

    yield ("intake invitation sent (step 4 happened)",
           one("SELECT count(*) FROM intake_invitations") > 0, "")

    n = one("SELECT count(*) FROM audit_log WHERE entity_type='facts'"
            " AND actor_type='contact'")
    yield ("client leg happened (fact writes by actor 'contact')",
           n > 0, f"contact-actor fact writes: {n}")

    yield ("invitation returned (client submitted)",
           one("SELECT count(*) FROM intake_invitations WHERE"
               " status='returned'") > 0, "")

    yield ("deadline on calendar, tied to the matter",
           one("SELECT count(*) FROM events WHERE deleted_at IS NULL"
               " AND matter_id IS NOT NULL") > 0, "")

    yield ("email reminder attached to the deadline",
           one("SELECT count(*) FROM event_reminders") > 0, "")


def main():
    if len(sys.argv) != 2 or not Path(sys.argv[1]).exists():
        print("usage: python verify/check_cold_run.py <run-db-path>")
        return 2
    conn = sqlite3.connect(sys.argv[1])
    conn.row_factory = sqlite3.Row
    failures = 0
    for name, ok, detail in checks(conn):
        status = "PASS" if ok else "FAIL"
        failures += 0 if ok else 1
        suffix = f"  ({detail})" if detail and not ok else ""
        print(f"{status}  {name}{suffix}")
    verdict = "ARTIFACTS COMPLETE" if failures == 0 \
        else f"INCOMPLETE ({failures} missing)"
    print(f"cold-run artifacts: {verdict}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
