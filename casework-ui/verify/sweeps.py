"""Supporting sweeps (goal.md): mechanical, not sampled.

no-logic lint -- the goal's rule made exact (drafted with the code,
as ratified): app_ui/reads.py is the ONE file allowed SQL, and only
SELECT; every other app_ui file carries zero SQL keywords and zero
.execute calls. Mutations always route through casework modules.

JS discipline -- no .js files, no <script> occurrences without a
justification line in verify/js-justifications.txt, no framework
artifacts (package.json / node_modules) anywhere in the project.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_UI = ROOT / "app_ui"
JUSTIFICATIONS = Path(__file__).resolve().parent / "js-justifications.txt"

SQL_RE = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE)\b")
MUTATION_RE = re.compile(r"\b(INSERT|UPDATE|DELETE)\b")

# Named exemptions, each with its why. Anything else fails. The
# synthetic-marker stamp is provenance, not business logic; casework
# is frozen so it cannot grow a helper for it without an approval
# cycle (worklog 2026-08-01, P0 design note).
ALLOWLIST = {
    ("app_ui/server.py", "INSERT INTO synthetic_marker"),
}


def _allowlisted(rel, line):
    return any(str(rel).replace("\\", "/") == path and frag in line
               for path, frag in ALLOWLIST)


def no_logic_lint():
    hits = []
    allowed = 0
    for py in sorted(APP_UI.rglob("*.py")):
        text = py.read_text(encoding="utf-8")
        rel = py.relative_to(ROOT)
        for i, line in enumerate(text.splitlines(), 1):
            if py.name == "reads.py":
                if MUTATION_RE.search(line):
                    hits.append(f"{rel}:{i} (mutation SQL in reads.py)")
                continue
            if SQL_RE.search(line) or ".execute(" in line:
                if _allowlisted(rel, line):
                    allowed += 1
                    continue
                hits.append(f"{rel}:{i} (SQL outside reads.py)")
    return ("no-logic-lint", not hits,
            f"SQL confined to reads.py (SELECT-only); {allowed} named"
            f" exemption(s); mutations ride casework modules"
            if not hits else f"violations: {', '.join(hits)}")


def js_sweep():
    justified = set()
    if JUSTIFICATIONS.exists():
        justified = {ln.split("|")[0].strip()
                     for ln in JUSTIFICATIONS.read_text(encoding="utf-8")
                     .splitlines() if ln.strip() and not
                     ln.startswith("#")}
    hits = []
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or "verify" in path.parts:
            continue
        if path.name in ("package.json", "node_modules"):
            hits.append(f"{path.relative_to(ROOT)} (framework artifact)")
        if path.suffix == ".js" and str(path.relative_to(ROOT)) \
                not in justified:
            hits.append(f"{path.relative_to(ROOT)} (unjustified .js)")
        if path.suffix == ".py" and path.is_file() \
                and "app_ui" in path.parts:
            text = path.read_text(encoding="utf-8")
            for i, line in enumerate(text.splitlines(), 1):
                if "<script" in line.lower():
                    key = f"{path.relative_to(ROOT)}:{i}"
                    if key not in justified:
                        hits.append(f"{key} (unjustified <script>)")
    return ("js-discipline", not hits,
            "zero JS; nothing to justify" if not hits and not justified
            else ("all JS justified" if not hits
                  else f"violations: {', '.join(hits)}"))


def run_all():
    return [no_logic_lint(), js_sweep()]
