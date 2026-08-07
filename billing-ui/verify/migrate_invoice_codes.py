"""One-shot migration: add stored invoice display codes to a
pre-item-10 database (invoice-codes.md; build authorized by James
2026-08-07, billing-ui s8).

Adds invoices.display_code + invoices.code_scope and backfills in
creation (id) order, replaying _next_code's semantics: one gapless
series per type per scope, scope taken from each row's own
number_scope (number and code are born under the same mode in the
new creation path). If global numbering is ON, the per-type global
counters are seeded to the per-type totals so the next code
continues correctly (fx-0076 mirror).

Fail-loud by design: refuses a db that already has the column;
asserts every row ends with a valid code and every series is
gapless. Never run on a fresh-schema db -- those get codes at
creation.

Run: python verify/migrate_invoice_codes.py <db-path> [<db-path>...]
"""

import re
import sys
from pathlib import Path

# open via casework's connect() -- the audit triggers need its actor
# functions, and dbs are only ever opened through it (casework rule)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "casework"))
from app import db as appdb  # noqa: E402

CODE_RE = re.compile(r"^[BT]\d{4,}$")
LETTER = {"bill": "B", "trust_request": "T"}


def migrate(path):
    conn = appdb.connect(path)
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(invoices)")]
    if "display_code" in cols:
        nulls = conn.execute("SELECT COUNT(*) FROM invoices WHERE"
                             " display_code IS NULL").fetchone()[0]
        if nulls == 0:
            print(f"{path}: display_code already present and fully"
                  f" backfilled -- refusing")
            return 1
        # a torn earlier run: DDL auto-committed, backfill rolled
        # back. Resume -- the replay below asserts any row already
        # coded matches what it would assign.
        print(f"{path}: resuming torn migration ({nulls} rows uncoded)")
    else:
        conn.execute("ALTER TABLE invoices ADD COLUMN display_code TEXT")
        conn.execute("ALTER TABLE invoices ADD COLUMN code_scope TEXT")

    counters = {}  # (letter, scope-key) -> last n
    rows = conn.execute("SELECT id, invoice_type, contact_id,"
                        " number_scope, display_code FROM invoices"
                        " ORDER BY id").fetchall()
    for r in rows:
        letter = LETTER[r["invoice_type"]]
        key = ((letter, "client", r["contact_id"])
               if r["number_scope"] == "client" else (letter, "global"))
        n = counters.get(key, 0) + 1
        counters[key] = n
        code = f"{letter}{n:04d}"
        if r["display_code"] is not None:
            assert r["display_code"] == code, \
                (f"row {r['id']} already coded {r['display_code']},"
                 f" replay says {code} -- refusing to overwrite")
            continue
        conn.execute("UPDATE invoices SET display_code=?, code_scope=?"
                     " WHERE id=?", (code, r["number_scope"], r["id"]))

    # continuation for global mode (fx-0076 mirror): next code picks
    # up from the per-type firm totals
    mode = conn.execute("SELECT value FROM firm_settings WHERE"
                        " key='billing.global_numbering'").fetchone()
    if mode and mode["value"] == "1":
        for itype, letter in LETTER.items():
            total = conn.execute("SELECT COUNT(*) FROM invoices WHERE"
                                 " invoice_type=?", (itype,)).fetchone()[0]
            conn.execute(
                "INSERT INTO firm_settings (key, value) VALUES (?,?)"
                " ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (f"billing.code_global_next.{letter}", str(total + 1)))

    # fail-loud verification: valid codes everywhere, gapless series
    bad = conn.execute("SELECT COUNT(*) FROM invoices WHERE"
                       " display_code IS NULL OR code_scope IS NULL"
                       ).fetchone()[0]
    assert bad == 0, f"{bad} rows left without a code"
    for r in conn.execute("SELECT display_code FROM invoices"):
        assert CODE_RE.match(r["display_code"]), r["display_code"]
    for key, last in counters.items():
        letter = key[0]
        where = ("code_scope='client' AND contact_id=? AND"
                 " display_code LIKE ?" if key[1] == "client"
                 else "code_scope='global' AND display_code LIKE ?")
        args = ((key[2], f"{letter}%") if key[1] == "client"
                else (f"{letter}%",))
        got = sorted(int(r["display_code"][1:]) for r in conn.execute(
            f"SELECT display_code FROM invoices WHERE {where}", args))
        assert got == list(range(1, last + 1)), \
            f"series {key} not gapless: {got}"
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM invoices").fetchone()[0]
    print(f"{path}: {total} invoices coded across"
          f" {len(counters)} series -- verified gapless")
    conn.close()
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(max(migrate(p) for p in sys.argv[1:]))
