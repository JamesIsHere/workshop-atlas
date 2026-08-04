"""Clock gauntlet (P3 U3.1): the verifiers must be GREEN under any
single consistent clock.

Two clock bugs surfaced on 2026-08-03 -- the walk's fire-time rode
wall-clock now instead of the posted event time, and casework's
esign spine test asserted a date literal that expired the day
after it was written. Both were violations of one property: a
verifier's expectations must derive from the same clock the app
uses, whatever that clock says. This gauntlet makes the calendar
adversarial instead of lucky.

Mechanism: each run is a subprocess whose first act is replacing
datetime.datetime with an offset subclass -- BEFORE any app or
verifier import -- so app and verifier share one consistent fake
clock, exactly the invariant of a cold user's machine. Stdlib
only; zero app-code edits; casework runs read-only (a red there
under a fake clock is a FLAG for the gate, never a fix from this
project).

Each gauntlet ends with real-clock closing runs (walk x2, spine,
anchor) so every report on disk reflects the real clock, and the
walk-x2 completion-proof receipt rides along.

Run: python verify/run_clock_gauntlet.py
Writes verify/clock-gauntlet-report.txt; exit 0 iff every run of
every verifier is green under every clock.
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
UI_ROOT = HERE.parent
CASEWORK = UI_ROOT.parent / "casework"
REPORT = HERE / "clock-gauntlet-report.txt"

SHIM = (
    "import datetime as _dt, os, runpy, sys\n"
    "_real = _dt.datetime\n"
    "_off = _dt.timedelta(seconds=float(os.environ['CG_OFFSET_S']))\n"
    "class _Fake(_real):\n"
    "    @classmethod\n"
    "    def now(cls, tz=None):\n"
    "        return _real.now(tz) + _off\n"
    "    @classmethod\n"
    "    def today(cls):\n"
    "        return _real.today() + _off\n"
    "    @classmethod\n"
    "    def utcnow(cls):\n"
    "        return _real.utcnow() + _off\n"
    "_dt.datetime = _Fake\n"
    "runpy.run_path(os.environ['CG_TARGET'], run_name='__main__')\n"
)

VERIFIERS = [
    ("ui-walk", UI_ROOT, HERE / "run_ui_walk.py"),
    ("spine", CASEWORK, CASEWORK / "verify" / "run_spine.py"),
    ("anchor", CASEWORK, CASEWORK / "verify" / "run_anchor.py"),
]


def _now():
    return datetime.now(timezone.utc)


def clocks():
    """(label, offset_fn, hunts). offset_fn is evaluated at BLOCK
    START, not gauntlet start -- straddle arms must place the fake
    clock seconds before the flip relative to when their runs
    actually begin, or elapsed prior blocks push them past it."""
    def at(**repl):
        def fn():
            now = _now()
            return (now.replace(microsecond=0, **repl)
                    - now).total_seconds()
        return fn

    return [
        ("pre-09Z", at(hour=4, minute=30, second=0),
         "time-of-day assumptions (fire-time class)"),
        ("post-09Z", at(hour=14, minute=30, second=0),
         "control arm: date effects isolated from time-of-day"),
        ("plus-400d", lambda: timedelta(days=400).total_seconds(),
         "expiring literals; year rollover (esign class)"),
        ("midnight-straddle", at(hour=23, minute=59, second=59),
         "date captured before the flip, compared after"),
        ("new-years-eve", at(month=12, day=31, hour=23, minute=59,
                             second=59),
         "year+month+day all roll mid-run"),
    ]


def run_one(name, cwd, target, offset_s):
    env = dict(os.environ, CG_OFFSET_S=str(offset_s),
               CG_TARGET=str(target))
    p = subprocess.run([sys.executable, "-c", SHIM], cwd=str(cwd),
                       env=env, capture_output=True, text=True,
                       timeout=900)
    out = (p.stdout or "").strip().splitlines()
    tail = out[0] if out else (p.stderr or "").strip().splitlines()[-1:] \
        and (p.stderr.strip().splitlines()[-1]) or "(no output)"
    return p.returncode, tail


def main():
    lines = ["# clock-gauntlet-report -- P3 U3.1 (verifier hardening)",
             "",
             f"run started: {_now().strftime('%Y-%m-%dT%H:%M:%SZ')}",
             "property: every verifier green under any single"
             " consistent clock", ""]
    failures = 0
    for label, offset_fn, hunts in clocks():
        lines.append(f"clock {label}  (hunts: {hunts})")
        for name, cwd, target in VERIFIERS:
            # offset per RUN: every verifier must START on its
            # arm's target clock (straddle arms sit seconds before
            # the flip; elapsed siblings must not push them past)
            offset_s = offset_fn()
            fake = _now() + timedelta(seconds=offset_s)
            code, tail = run_one(name, cwd, target, offset_s)
            status = "PASS" if code == 0 else "FAIL"
            failures += 0 if code == 0 else 1
            lines.append(f"  {status} {name:8s} exit {code}  start"
                         f" {fake.strftime('%Y-%m-%dT%H:%M:%SZ')}"
                         f"  {tail}")
        lines.append("")

    lines.append("real-clock closing runs (reports on disk stay"
                 " truthful; walk x2 = completion-proof receipt)")
    closing = [("ui-walk", UI_ROOT, HERE / "run_ui_walk.py"),
               ("ui-walk", UI_ROOT, HERE / "run_ui_walk.py"),
               ("spine", CASEWORK, CASEWORK / "verify" / "run_spine.py"),
               ("anchor", CASEWORK, CASEWORK / "verify" / "run_anchor.py")]
    for name, cwd, target in closing:
        code, tail = run_one(name, cwd, target, 0.0)
        status = "PASS" if code == 0 else "FAIL"
        failures += 0 if code == 0 else 1
        lines.append(f"  {status} {name:8s} exit {code}  {tail}")

    verdict = "GREEN" if failures == 0 else f"FAIL ({failures} red runs)"
    lines += ["", f"verdict: {verdict}"]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8",
                      newline="\n")
    print(f"clock-gauntlet: {verdict}")
    print(f"report: {REPORT}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
