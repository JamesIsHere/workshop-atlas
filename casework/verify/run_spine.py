"""Spine suite runner (verifier 1). Oracle-first: exists before features.

Loads ../spine-map.json, discovers test functions in ../tests/spine/,
runs each against a fresh seeded db, writes spine-report.txt beside this
file. Exit 0 iff every spine entry is green AND all supporting checks
pass. Entries with no implemented test stay 'pending' (reported, exit 1).

DETERMINISM CONTRACT: the report carries no timestamps or machine facts;
two consecutive runs on the same tree must be byte-identical (goal.md
completion proof). Do not add wall-clock output.

Run: python run_spine.py [--db PATH]   (default: fresh in-memory db,
seeded from seeds/seed.sql when it exists)
"""

import importlib.util
import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from app import db as appdb  # noqa: E402
from verify import checks  # noqa: E402

MAP_PATH = ROOT / "spine-map.json"
TESTS_DIR = ROOT / "tests" / "spine"
SEED_SQL = ROOT / "seeds" / "seed.sql"
REPORT = HERE / "spine-report.txt"


def discover_tests():
    """Import every tests/spine/test_*.py; return {func_name: callable}."""
    found = {}
    if not TESTS_DIR.exists():
        return found
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
    spine = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    tests = discover_tests()
    results = []
    failures = []
    for entry in spine["entries"]:
        if entry["class"] == "parked":
            results.append((entry["id"], entry["class"], "parked"))
            continue
        fn = tests.get(entry["test"])
        if fn is None:
            results.append((entry["id"], entry["class"], "pending"))
            continue
        conn = fresh_db()
        try:
            fn(conn)
            results.append((entry["id"], entry["class"], "green"))
        except Exception:
            results.append((entry["id"], entry["class"], "red"))
            failures.append((entry["id"], traceback.format_exc(limit=4)))
        finally:
            conn.close()

    conn = fresh_db()
    check_results = checks.run_all(conn)
    conn.close()

    counts = {"green": 0, "red": 0, "pending": 0, "parked": 0}
    for _, _, status in results:
        counts[status] += 1

    lines = ["# spine-report -- verifier 1", ""]
    lines.append(f"entries: {len(results)}  green: {counts['green']}"
                 f"  red: {counts['red']}  pending: {counts['pending']}"
                 f"  parked: {counts['parked']}")
    lines.append("")
    for eid, cls, status in results:
        lines.append(f"{status.upper():7s} [{cls:7s}] {eid}")
    lines.append("")
    lines.append("# supporting checks")
    checks_ok = True
    for name, ok, detail in check_results:
        checks_ok = checks_ok and ok
        lines.append(f"{'PASS' if ok else 'FAIL':4s} {name}: {detail}")
    lines.append("")
    all_green = counts["red"] == 0 and counts["pending"] == 0
    verdict = "GREEN" if (all_green and checks_ok) else "NOT GREEN"
    lines.append(f"verdict: {verdict}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"spine: {counts['green']} green, {counts['red']} red,"
          f" {counts['pending']} pending; checks {'pass' if checks_ok else 'FAIL'}")
    for eid, tb in failures:
        print(f"--- {eid}\n{tb}")
    print(f"report: {REPORT}")
    return 0 if (all_green and checks_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
