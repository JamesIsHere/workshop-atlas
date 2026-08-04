"""Sheet-label audit (added 2026-08-04, walk-day session): every
"quoted label" in demo-walk-protocol.md's walk steps must appear in
the source that renders the screens (app_ui plus the client surface
in casework/app/server.py). Closes the drift class James hit on walk
day: the sheet was the program's only human-facing artifact with no
oracle, so button/heading names drifted from the screens and the
drift surfaced only in his browser.

Data values (SYNTH*, Vera*, demo*, dates, the token) are exempt.
Tab names computed via .capitalize() match case-insensitively.
Adjacent f-string literals are joined before matching (labels split
across source lines). Exit 0 = every label found.

Run: python verify/check_sheet_labels.py
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS = HERE.parent.parent
SHEET = HERE / "demo-walk-protocol.md"

SOURCES = (sorted((ATLAS / "casework-ui" / "app_ui").glob("*.py"))
           + [ATLAS / "casework" / "app" / "server.py"])

DATA_PREFIXES = ("SYNTH", "Vera", "demo", "2026", "SYNTHETIC", "done")
NOTATION = {"End:", "Go:", "Observe:", "Field"}  # sheet notation,
# quoted by the STEP RULE preamble -- not screen labels

text = SHEET.read_text(encoding="utf-8")
start = text.index("## Walk sheet")
end = text.index("## Timing marks")
# labels wrap across the sheet's 65-col lines: rejoin before extracting
steps = re.sub(r"\n\s+", " ", text[start:end])


# key by path (two files are named server.py); join adjacent
# f-string literals so labels split across source lines match
def _norm(src):
    return re.sub(r'"\s*\n\s*f?"', "", src)


corpus = {str(p.relative_to(ATLAS)): _norm(p.read_text(encoding="utf-8"))
          for p in SOURCES}
blob = "\n".join(corpus.values())

labels = sorted(set(re.findall(r'"([^"\n]+)"', steps)))
failures = []
checked = 0

# unmapped-value fence (papercut 7, 2026-08-04): a slash-separated
# value tuple ("Vera / Synthetic / ...") names no fields -- the
# driver must guess which value lands where. Every data value must
# be written against its field label ("Field" = value).
tuples = re.findall(r"\([^)]* / [^)]*\)", steps)
for t in tuples:
    failures.append(t)
    print(f"  FAIL unmapped value tuple {t!r} -- pin each value to"
          f" its field label")

# atomicity fence (STEP RULE, 2026-08-04): one step = one screen =
# at most one "End:" click. Two End: lines in one step means the
# step spans screens. Parse from the RAW text (before line-joins).
raw_steps = text[start:end]
chunks = re.split(r"(?m)^\s{0,4}(\d{1,2})\.\s", raw_steps)
for num, body in zip(chunks[1::2], chunks[2::2]):
    ends = body.count("End:")
    if ends > 1:
        failures.append(f"step {num}")
        print(f"  FAIL step {num} has {ends} 'End:' clicks --"
              f" a step is ONE screen")
for lab in labels:
    if lab.startswith(DATA_PREFIXES) or "<" in lab or lab in NOTATION:
        continue
    checked += 1
    if lab in blob:
        where = [n for n, t in corpus.items() if lab in t]
        print(f"  OK   {lab!r:45s} in {where[0]}")
    elif lab.lower() in blob:
        print(f"  OK   {lab!r:45s} (case-computed tab label)")
    else:
        failures.append(lab)
        print(f"  FAIL {lab!r} -- not in any rendering source")

print(f"\nsheet-label audit: {checked} labels checked,"
      f" {len(failures)} not found")
sys.exit(1 if failures else 0)
