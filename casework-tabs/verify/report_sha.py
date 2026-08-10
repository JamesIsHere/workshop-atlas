"""Canonical timing-strip sha for tabs-walk-report.txt.

Same recipe as billing-ui's report_sha.py (added there 2026-08-07
after recipe drift produced incomparable shas): this script IS the
recipe; a sha quoted in any receipt must come from running it, never
from an inline reimplementation.

Recipe: drop the "run started:" line, drop each per-step elapsed
column (" N.NNNs"), drop the "; total N.NNNs" figure; sha256 of
the result, first 8 hex chars.

Run: python verify/report_sha.py
"""

import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(__file__).resolve().parent / "tabs-walk-report.txt"


def stripped_sha(text):
    t = "\n".join(l for l in text.splitlines()
                  if not l.startswith("run started:"))
    t = re.sub(r" +\d+\.\d{3}s", "", t)
    t = re.sub(r"; total \d+\.\d{3}s", "", t)
    return hashlib.sha256(t.encode("utf-8")).hexdigest()[:8]


if __name__ == "__main__":
    if not REPORT.exists():
        print(f"no report at {REPORT}")
        sys.exit(1)
    print(stripped_sha(REPORT.read_text(encoding="utf-8")))
