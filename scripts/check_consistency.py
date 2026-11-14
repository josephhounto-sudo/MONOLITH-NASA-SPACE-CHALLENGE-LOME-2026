"""Anti-stale check (protocol P5). Exit code 0 only if every check passes. Run before sending any block, card or zip.
Usage: python scripts/check_consistency.py [--blocks path1 path2 ...]"""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
errs, notes = [], []
def err(m): errs.append(m)
R = lambda p: open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()

# 1 tests
r = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, capture_output=True, text=True)
if r.returncode: err("pytest fails:\n" + r.stdout[-400:])
else: notes.append("pytest: " + r.stdout.strip().splitlines()[-1])

# 2 task cards aligned with provisional values
T = json.load(open(os.path.join(ROOT, "docs/team/tasks.json"), encoding="utf-8"))["tasks"]
blob = json.dumps(T, ensure_ascii=False)
if "josephhounto-sudo/c-sync" in blob or "cd c-sync" in blob: err("tasks.json still points to the old repository name 'c-sync'")
m21 = [t for t in T if t["id"] == "M2-1"][0]["prompt"]
if "drift_amp=2.5" not in m21: err("M2-1 prompt lacks drift_amp=2.5")
if "FOCUS" not in m21: err("M2-1 prompt lacks the ui_hint mapping")
if "Delivered (once)" in blob: err("a card still hardcodes 'Delivered (once)' (single source = strings_en.json delivered_once)")

# 3 defaults used by scripts
for f in ("scripts/run_story.py",):   # the UI reads the capsules built by run_story.py (it no longer generates data itself)
    if "drift_amp" not in R(f) or "2.5" not in R(f): err(f"{f} does not pass drift_amp=2.5 explicitly")

# 4 the M3-1 criterion actually holds
from synthetic.generator import generate
from csync.rules import daily_values, evaluate, Params
_, _, states, _, _ = evaluate(daily_values(generate("histoire", seed=42, drift_amp=2.5, fast=True)), Params())
if states.loc[7, "Attention"] != "DEGRADED": err(f"M3-1 criterion broken: day 7 Attention = {states.loc[7, 'Attention']}")
else: notes.append("M3-1 criterion holds (day 7 Attention DEGRADED)")

# 5 honesty about EWMA: the decision text must match the code
code_has_ewma = "ewma" in R("csync/rules.py").lower()
dec = R("docs/OPEN_DECISIONS.md")
if (not code_has_ewma) and not re.search(r"pas cod|non cod", dec): err("OPEN_DECISIONS must say EWMA is not coded (rules.py has none)")
if code_has_ewma and re.search(r"pas cod|non cod", dec): err("OPEN_DECISIONS says EWMA is not coded but rules.py contains it")

# 6 banned wording in fixed UI strings
from csync.language import banned_hits
def walk(o):
    if isinstance(o, dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o, str): yield o
for s in walk(json.load(open(os.path.join(ROOT, "csync/config/strings_en.json"), encoding="utf-8"))):
    if banned_hits(s): err(f"banned word in UI string: {s}")

# 7 privacy: no email / phone in tracked text files
files = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).split()
pat = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\+\d[\d\s-]{7,}")
for f in files:
    if f.endswith((".md", ".py", ".json", ".txt")) and f != "LICENSE":
        for hit in pat.findall(R(f)):
            if "noreply@anthropic.com" in hit or "conduct@" in hit: continue
            err(f"possible personal data in {f}: {hit[:30]}")

# 8 every doc has the required header (P2): version/date/status in the first 6 lines, for the docs we own
for f in ("docs/PROTOCOLES.md", "docs/PROGRAMME_OFFICIEL.md"):
    if not re.search(r"(?i)version", "\n".join(R(f).splitlines()[:6])): err(f"{f} lacks a version header")

# 9 blocks freshness: embedded commit must equal HEAD
head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
if "--blocks" in sys.argv:
    for p in sys.argv[sys.argv.index("--blocks") + 1:]:
        m = re.search(r"commit ([0-9a-f]{7})", open(p, encoding="utf-8").read()[:600])
        if not m: err(f"{p}: no commit stamp (P3)")
        elif subprocess.run(["git", "diff", "--quiet", m.group(1), "HEAD", "--", "contracts", "csync", "synthetic", "docs/team/tasks.json", "docs/OPEN_DECISIONS.md", "docs/STORY.md"], cwd=ROOT).returncode:
            err(f"{p}: STALE — repository inputs changed since commit {m.group(1)} (HEAD is {head}); rebuild it")
        else: notes.append(f"{p}: up to date with the inputs (stamp {m.group(1)})")
for n in notes: print("OK  ", n)
for e in errs: print("ERR ", e)
print(f"{len(errs)} erreur(s)")
sys.exit(1 if errs else 0)
