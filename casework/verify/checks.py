"""Supporting checks (goal.md): mechanical sweeps, not sampling.

Each check returns (name, ok, detail). Run against a live db connection
plus the app source tree. Deterministic output only -- no timestamps.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"

from app.schema.gen_schema import TABLES, APPEND_ONLY  # noqa: E402


def check_audit_coverage(conn):
    """Every audited record table carries all three audit triggers."""
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
        " AND name NOT LIKE 'sqlite_%'").fetchall()]
    triggers = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='trigger'").fetchall()}
    # unaudited-by-design: pure logs/datasets/queues (append-only or replay)
    exempt = {"audit_log", "matter_status_history", "esign_events",
              "receipt_status_history", "uscis_responses", "visa_bulletin",
              "notifications", "email_outbox", "sessions", "password_resets",
              "twofa_challenges", "record_access", "synthetic_marker"}
    missing = []
    for t in sorted(set(tables) - exempt):
        for suffix in ("ai", "au", "ad"):
            if f"trg_{t}_{suffix}" not in triggers:
                missing.append(f"{t}:{suffix}")
    return ("audit-coverage", not missing,
            "all audited tables carry insert/update/delete triggers"
            if not missing else f"missing triggers: {', '.join(missing)}")


def check_fact_store_integrity(conn):
    """Forms consume the fact store, never private copies: no form_answers
    question_key may duplicate a fact_definitions key."""
    dupes = [r[0] for r in conn.execute(
        "SELECT DISTINCT fa.question_key FROM form_answers fa"
        " JOIN fact_definitions fd ON fd.key = fa.question_key").fetchall()]
    return ("fact-store-lint", not dupes,
            "no form answers duplicate fact keys"
            if not dupes else f"fact keys stored as form answers: {', '.join(sorted(dupes))}")


def check_soft_delete_sweep():
    """DELETE FROM is legal only against non-tombstoned tables (facts,
    join/child rows -- gate ruling 9). Tombstoned tables are purge-only;
    append-only surface is never deleted. Rules derive from the
    generator's own declarations so sweep and schema cannot disagree.
    Unparseable or unknown targets fail loudly."""
    tombstoned = {name for name, _cols, soft, _aud in TABLES if soft}
    known = {name for name, *_ in TABLES}
    hits = []
    for py in sorted(APP.rglob("*.py")):
        if py.name == "purge.py":
            continue
        text = py.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            m = re.search(r"\bDELETE\s+FROM(?:\s+([A-Za-z_][A-Za-z0-9_]*))?",
                          line, re.IGNORECASE)
            if not m:
                continue
            table = m.group(1).lower() if m.group(1) else None
            loc = f"{py.relative_to(ROOT)}:{i}"
            if table is None or table not in known | APPEND_ONLY:
                hits.append(f"{loc} (unparseable or unknown target)")
            elif table in tombstoned:
                hits.append(f"{loc} ({table}: tombstoned, purge-only)")
            elif table in APPEND_ONLY:
                hits.append(f"{loc} ({table}: append-only)")
    return ("soft-delete-sweep", not hits,
            "DELETE targets only sanctioned non-tombstoned tables"
            if not hits else f"illegal DELETE: {', '.join(hits)}")


def check_fact_integrity_sweep(conn):
    """P5 gate ruling (2026-08-01): the P0-deferred fact-integrity sweep.
    Wholesale assertion of what facts.set_fact guards at the write path:
    (a) no orphan polymorphic subject_id -- every fact's subject row
    exists (tombstoned rows still exist; orphan = no row at all);
    (b) no fact whose subject_type disagrees with its definition."""
    problems = []
    for stype, table in (("contact", "contacts"), ("matter", "matters")):
        orphans = [str(r[0]) for r in conn.execute(
            f"SELECT DISTINCT f.subject_id FROM facts f"
            f" LEFT JOIN {table} t ON t.id = f.subject_id"
            f" WHERE f.subject_type = ? AND t.id IS NULL",
            (stype,)).fetchall()]
        if orphans:
            problems.append(f"orphan {stype} ids: {', '.join(sorted(orphans))}")
    mismatches = [f"{r[0]} ({r[1]} vs {r[2]})" for r in conn.execute(
        "SELECT DISTINCT f.key, f.subject_type, d.subject_type FROM facts f"
        " JOIN fact_definitions d ON d.key = f.key"
        " WHERE f.subject_type <> d.subject_type").fetchall()]
    if mismatches:
        problems.append(f"subject_type mismatch: {', '.join(sorted(mismatches))}")
    return ("fact-integrity-sweep", not problems,
            "no orphan subjects, no definition mismatches"
            if not problems else "; ".join(problems))


def check_synthetic_guard(conn):
    """The db must carry the SYNTHETIC marker before any seed data exists."""
    has_marker = conn.execute(
        "SELECT count(*) FROM synthetic_marker WHERE marker='SYNTHETIC'").fetchone()[0] > 0
    seeded = conn.execute("SELECT count(*) FROM contacts").fetchone()[0] > 0
    ok = has_marker or not seeded
    return ("synthetic-guard", ok,
            "SYNTHETIC marker present" if has_marker
            else ("empty db, marker not yet required" if ok
                  else "db holds contacts but no SYNTHETIC marker"))


def run_all(conn):
    return [
        check_audit_coverage(conn),
        check_fact_store_integrity(conn),
        check_fact_integrity_sweep(conn),
        check_soft_delete_sweep(),
        check_synthetic_guard(conn),
    ]
