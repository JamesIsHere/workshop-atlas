#!/usr/bin/env python
"""run_billing.py -- verifier 1: billing parity suite over billing-map.json.

Mirrors casework's spine runner convention: discovers test FUNCTIONS
named per the map's test ids from ../tests/test_*.py, runs each against
a fresh seeded in-memory db (casework schema + seed), reports.
Entries with no implemented test stay 'pending'. Exit 0 iff every
in-scope entry is green.

DETERMINISM CONTRACT: no timestamps or machine facts in the report;
two consecutive runs must be byte-identical (goal.md).
"""
import importlib.util
import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CASEWORK = ROOT.parent / "casework"
sys.path.insert(0, str(CASEWORK))

from app import db as appdb  # noqa: E402

MAP = ROOT / "billing-map.json"
TESTS_DIR = ROOT / "tests"
SEED_SQL = CASEWORK / "seeds" / "seed.sql"
REPORT = HERE / "billing-report.txt"


def discover_tests():
    found = {}
    for py in sorted(TESTS_DIR.glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(py.stem, py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name in dir(mod):
            if name.startswith("test_") and callable(getattr(mod, name)):
                found[name] = getattr(mod, name)
    return found


def fresh_db():
    conn = appdb.create_db(":memory:")
    if SEED_SQL.exists():
        conn.actor.set("system", None)
        conn.executescript(SEED_SQL.read_text(encoding="utf-8"))
    return conn


def main():
    m = json.loads(MAP.read_text(encoding="utf-8"))
    tests = discover_tests()
    lines, failures = [], []
    green = red = pending = parked = 0
    for e in m["entries"]:
        if e["class"] == "parked":
            parked += 1
            lines.append("PARKED  %s" % e["id"])
            continue
        fn = tests.get(e["test"])
        if fn is None:
            pending += 1
            lines.append("PENDING %s" % e["id"])
            continue
        conn = fresh_db()
        try:
            fn(conn)
            green += 1
            lines.append("GREEN   %s" % e["id"])
        except Exception:
            red += 1
            lines.append("RED     %s" % e["id"])
            failures.append((e["id"], traceback.format_exc(limit=4)))
        finally:
            conn.close()
    checks_ok = run_supporting_checks(lines)
    lines.append("billing: %d green, %d red, %d pending, %d parked; "
                 "checks %s; verdict: %s"
                 % (green, red, pending, parked,
                    "pass" if checks_ok else "FAIL",
                    "GREEN" if red == 0 and pending == 0 and checks_ok
                    else "NOT GREEN"))
    REPORT.write_text("\n".join(lines) + "\n")
    print(lines[-1])
    print("report: %s" % REPORT)
    for eid, tb in failures:
        print("--- %s\n%s" % (eid, tb))
    sys.exit(0 if red == 0 and pending == 0 and checks_ok else 1)


BILLING_TABLES = ("ledger_accounts", "journal_entries", "journal_postings",
                  "external_events", "invoices", "invoice_charges",
                  "saved_charges", "invoice_payments", "payment_plans",
                  "plan_installments", "invoice_shares", "time_entries",
                  "processor_transactions", "settlement_batches")

BILLING_MODULES = ("ledger.py", "billing.py", "processor.py",
                   "timekeeping.py")


def run_supporting_checks(lines):
    """Goal.md supporting checks owned by this runner: CSV round-trip
    (anti-lock-in) and the float sweep (integer cents everywhere)."""
    import csv
    import io
    from app import billing
    ok = True
    conn = fresh_db()
    try:
        exports = {
            "invoices": (billing.export_invoices_csv, "invoices"),
            "payments": (billing.export_payments_csv, "invoice_payments"),
            "time_entries": (billing.export_time_entries_csv,
                             "time_entries"),
            "trust_ledger": (billing.export_trust_ledger_csv,
                             "journal_postings"),
        }
        for name, (fn, table) in exports.items():
            rows = list(csv.reader(io.StringIO(fn(conn))))
            cols = len(rows[0])
            bad_width = [r for r in rows[1:] if len(r) != cols]
            expected = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
                + ("" if table == "journal_postings"
                   else " WHERE deleted_at IS NULL")).fetchone()[0]
            passed = not bad_width and len(rows) - 1 == expected
            ok = ok and passed
            lines.append("CHECK   csv-export %s: %d cols x %d rows"
                         " (table %d) %s"
                         % (name, cols, len(rows) - 1, expected,
                            "pass" if passed else "FAIL"))
        # float sweep: no REAL columns in billing tables, no float() in
        # billing modules' monetary code
        real_cols = []
        for t in BILLING_TABLES:
            for r in conn.execute(f"PRAGMA table_info({t})"):
                if "REAL" in (r[2] or "").upper() \
                        or "FLOA" in (r[2] or "").upper() \
                        or "DOUB" in (r[2] or "").upper():
                    real_cols.append(f"{t}.{r[1]}")
        float_calls = []
        for mod in BILLING_MODULES:
            src = (CASEWORK / "app" / mod).read_text(encoding="utf-8")
            for i, line in enumerate(src.splitlines(), 1):
                if "float(" in line and "cent" in line.lower():
                    float_calls.append(f"{mod}:{i}")
        passed = not real_cols and not float_calls
        ok = ok and passed
        lines.append("CHECK   float-sweep: %d REAL columns, %d float()"
                     " on cents %s"
                     % (len(real_cols), len(float_calls),
                        "pass" if passed else "FAIL"))
    finally:
        conn.close()
    return ok


if __name__ == "__main__":
    main()
