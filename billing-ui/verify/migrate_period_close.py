"""One-shot migration: add the period_closes table (+ its audit
triggers) to a pre-close database (period-close.md, ratified
2026-08-09; program amendment same date).

Pre-close dbs cannot serve the close page or accept ledger writes:
period.assert_open runs inside ledger._post and fails loud on the
missing table (deliberate -- no unlockable ledger exists silently).
This migration brings a retained walk db forward. The DDL is LIFTED
FROM THE GENERATED schema.sql at run time, never duplicated here, so
it cannot drift from gen_schema.py's output.

Fail-loud by design: refuses a db that already has the table.
Fresh-schema dbs need nothing.

Run: python verify/migrate_period_close.py <db-path> [<db-path>...]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "casework"))
from app import db as appdb  # noqa: E402

SCHEMA = (Path(__file__).resolve().parents[2] / "casework" / "app"
          / "schema" / "schema.sql")


def _ddl():
    text = SCHEMA.read_text(encoding="utf-8")
    start = text.index("CREATE TABLE period_closes")
    end = text.index("CREATE TABLE", start + 1)
    block = text[start:end].rstrip()
    assert "trg_period_closes_ad" in block, \
        "audit triggers missing from the extracted block"
    return block


def migrate(path):
    conn = appdb.connect(path)
    have = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
        " AND name='period_closes'").fetchone()[0]
    if have:
        print(f"{path}: period_closes already present -- refusing")
        return 1
    conn.actor.set("system", None)
    conn.executescript(_ddl())
    conn.commit()
    n = conn.execute("SELECT COUNT(*) FROM period_closes").fetchone()[0]
    trg = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
        " AND name LIKE 'trg_period_closes_%'").fetchone()[0]
    assert n == 0 and trg == 3, f"post-migration state wrong: {n}, {trg}"
    print(f"{path}: period_closes added (0 rows, 3 audit triggers)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(max(migrate(p) for p in sys.argv[1:]))
