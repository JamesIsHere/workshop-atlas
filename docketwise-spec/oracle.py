"""oracle.py -- docketwise-spec corpus verifier (goal.md verifier 1).

Seven checks, all mechanical. Exit 0 iff every check passes.
--seed relaxes ONLY the inventory-count minimum (check 3) for the
Phase 0 micro-corpus; every other check runs at full strictness.
Output is deterministic (no timestamps): check 7 (determinism) is
executed by the runner -- run twice, byte-compare the reports.
"""
import sys, os, re, json, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
SEED = "--seed" in sys.argv
# --extraction: phases 1-3, inventories exist but closure is not yet
# due -- unmapped items are COUNTED (progress metric), not failures.
# Default (no flag) is FULL mode, the Phase 4 bar: unmapped = FAIL.
EXTRACTION = "--extraction" in sys.argv
REQUIRED = ["name", "named-by-us", "description", "criterion",
            "sources", "tier"]
OPTIONAL = ["detail", "gap", "superseded-by"]
TIERS = {"confirmed", "provisional"}
FAMILIES = {"marketing", "help", "youtube", "release-notes", "reviews"}
MIN_FAMILIES = 3

failures = []
report = []

def fail(check, msg):
    failures.append(check)
    report.append("  FAIL [%s] %s" % (check, msg))

def note(msg):
    report.append("  " + msg)

# ---- load manifest ----
man_path = os.path.join(ROOT, "fixtures", "manifest.json")
manifest = {}
if os.path.exists(man_path):
    for row in json.load(open(man_path)):
        manifest[row["id"]] = row
else:
    fail("2", "fixtures/manifest.json missing")

# ---- parse corpus ----
entries = {}
parse_errors = []
corpus_dir = os.path.join(ROOT, "corpus")
for fn in sorted(os.listdir(corpus_dir)):
    if not fn.endswith(".md"):
        continue
    text = open(os.path.join(corpus_dir, fn), encoding="utf-8").read()
    m = re.search(r"^# module: (\S+)", text, re.M)
    if not m:
        parse_errors.append("%s: no '# module:' header" % fn)
        continue
    module = m.group(1)
    if fn != module + ".md":
        parse_errors.append("%s: filename != module '%s'" % (fn, module))
    blocks = re.split(r"^## entry: ", text, flags=re.M)[1:]
    for b in blocks:
        lines = b.splitlines()
        eid = lines[0].strip()
        fields = {}
        key = None
        for ln in lines[1:]:
            fm = re.match(r"^- ([a-z-]+): ?(.*)$", ln)
            if fm:
                key = fm.group(1)
                fields[key] = fm.group(2).strip()
            elif key and (ln.startswith("  ") and ln.strip()):
                fields[key] += " " + ln.strip()
            elif ln.strip() == "":
                key = None
        if eid in entries:
            parse_errors.append("duplicate entry id: " + eid)
        entries[eid] = {"module": module, "file": fn, "fields": fields}

live = {k: v for k, v in entries.items()
        if "superseded-by" not in v["fields"]}

# ---- check 1: schema ----
report.append("CHECK 1 SCHEMA")
for e in parse_errors:
    fail("1", e)
for eid, e in sorted(entries.items()):
    f = e["fields"]
    for r in REQUIRED:
        if r not in f or not f[r]:
            fail("1", "%s: missing field '%s'" % (eid, r))
    for k in f:
        if k not in REQUIRED + OPTIONAL:
            fail("1", "%s: unknown field '%s'" % (eid, k))
    if f.get("tier") not in TIERS:
        fail("1", "%s: bad tier '%s'" % (eid, f.get("tier")))
    if not eid.startswith(e["module"] + "."):
        fail("1", "%s: id not prefixed by module '%s'" % (eid, e["module"]))
    if f.get("named-by-us") not in ("yes", "no"):
        fail("1", "%s: named-by-us must be yes/no" % eid)
note("%d entries (%d live) across %d modules" % (
    len(entries), len(live),
    len(set(e["module"] for e in entries.values()))))

# ---- check 2: citation closure + fixture integrity ----
report.append("CHECK 2 CITATION CLOSURE")
cited = set()
for eid, e in sorted(live.items()):
    srcs = [s.strip() for s in e["fields"].get("sources", "").split(",")
            if s.strip()]
    if not srcs:
        fail("2", eid + ": no sources")
    for s in srcs:
        cited.add(s)
        if s not in manifest:
            fail("2", "%s cites %s: not in manifest" % (eid, s))
for fid, row in sorted(manifest.items()):
    p = os.path.join(ROOT, "fixtures", row.get("file", fid + ".html"))
    if not os.path.exists(p):
        fail("2", fid + ": manifest row but file missing")
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != row["sha256"]:
        fail("2", fid + ": sha256 mismatch (fixture edited?)")
    if row.get("family") not in FAMILIES:
        fail("2", fid + ": unknown family '%s'" % row.get("family"))
excl_path = os.path.join(ROOT, "exclusion-log.md")
excl_text = open(excl_path, encoding="utf-8").read() \
    if os.path.exists(excl_path) else ""
for fid in sorted(manifest):
    if fid not in cited and fid not in excl_text:
        fail("2", fid + ": orphan fixture (uncited, not excluded)")

# ---- superseded pointer validity (goal.md round-6 clause) ----
for eid, e in sorted(entries.items()):
    sup = e["fields"].get("superseded-by")
    if sup and sup not in entries:
        fail("1", "%s: dangling superseded-by -> %s" % (eid, sup))

# ---- check 3: coverage closure ----
report.append("CHECK 3 COVERAGE CLOSURE")
inv_dir = os.path.join(ROOT, "inventories")
inv_files = sorted(f for f in os.listdir(inv_dir)) \
    if os.path.exists(inv_dir) else []
if len(inv_files) == 0 and SEED:
    note("SEED MODE: 0 inventories -- coverage undefined, not judged")
elif len(inv_files) < MIN_FAMILIES:
    fail("3", "only %d inventories; %d source families required "
         "(blocker floor)" % (len(inv_files), MIN_FAMILIES))
else:
    unmapped = 0
    items = 0
    for fn in inv_files:
        for ln in open(os.path.join(inv_dir, fn),
                       encoding="utf-8").read().splitlines():
            if not ln.startswith("- "):
                continue
            items += 1
            im = re.match(r"^- (.+?) :: (entries|excluded): (.+)$", ln)
            if not im:
                unmapped += 1
                if not EXTRACTION:
                    fail("3", "%s: unmapped item: %s"
                         % (fn, ln[2:60].strip()))
                continue
            if im.group(2) == "entries":
                for ref in im.group(3).split(","):
                    if ref.strip() not in live:
                        fail("3", "%s: maps to unknown entry %s"
                             % (fn, ref.strip()))
            # excluded: rationale text is the ruling; presence suffices
    note("%d inventory files, %d items, %d unmapped%s"
         % (len(inv_files), items, unmapped,
            " (extraction mode: progress metric, not failure)"
            if EXTRACTION else ""))

# ---- check 4: attestation tiers ----
report.append("CHECK 4 ATTESTATION TIERS")
tiercount = {"confirmed": 0, "provisional": 0}
for eid, e in sorted(live.items()):
    srcs = [s.strip() for s in e["fields"].get("sources", "").split(",")
            if s.strip()]
    fams = set(manifest[s]["family"] for s in srcs if s in manifest)
    tier = e["fields"].get("tier")
    if tier == "confirmed" and len(fams) < 2:
        fail("4", eid + ": confirmed but <2 source families")
    if tier == "provisional" and len(fams) >= 2:
        fail("4", eid + ": provisional but has %d families "
             "(promote to confirmed)" % len(fams))
    if tier in tiercount:
        tiercount[tier] += 1
note("confirmed=%d provisional=%d"
     % (tiercount["confirmed"], tiercount["provisional"]))

# ---- check 5: criterion lint ----
report.append("CHECK 5 CRITERION LINT")
for eid, e in sorted(live.items()):
    c = e["fields"].get("criterion", "")
    if "->" not in c:
        fail("5", eid + ": criterion lacks 'ACTION -> RESULT' form")
    else:
        a, _, b = c.partition("->")
        if not a.strip() or not b.strip():
            fail("5", eid + ": empty side of '->'")

# ---- check 6: source-gap integrity ----
report.append("CHECK 6 SOURCE-GAP INTEGRITY")
gaps = 0
for eid, e in sorted(live.items()):
    g = e["fields"].get("gap")
    if g:
        gaps += 1
        if "what:" not in g or "source:" not in g:
            fail("6", eid + ": gap needs 'what:' and 'source:' parts")
note("%d SOURCE-GAP entries (trial-account decision inventory)" % gaps)

# ---- emit ----
print("oracle.py report -- docketwise-spec%s"
      % (" [SEED MODE]" if SEED else ""))
for ln in report:
    print(ln)
status = "GREEN (exit 0)" if not failures else \
    "RED: %d failures in checks %s" % (
        len([r for r in report if "FAIL" in r]),
        ",".join(sorted(set(failures))))
print("RESULT: " + status)
print("(check 7 determinism is runner-executed: run twice, "
      "byte-compare reports)")
sys.exit(0 if not failures else 1)
