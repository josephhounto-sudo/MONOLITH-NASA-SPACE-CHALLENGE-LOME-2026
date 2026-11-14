"""Rebuild the code-assistant block from the repository (protocol P3). Never edit the output by hand.
Usage: python scripts/build_blocks.py [out_dir]   (default: ./out_blocks). Writes BLOC_CODE_<commit>.md
The static part (rules, project summary, provisional values) lives in docs/blocks/code_header.md; everything else is
read from the repository at build time and stamped with the commit."""
import datetime, glob, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
R = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()
sh = lambda *a: subprocess.check_output(a, cwd=ROOT, text=True).strip()
commit = sh("git", "rev-parse", "--short", "HEAD")
dirty = bool(sh("git", "status", "--porcelain"))
now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
URL = "https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026"

# facts measured now
from synthetic.generator import generate
from csync.rules import daily_values, evaluate, Params
st = evaluate(daily_values(generate("histoire", seed=42, drift_amp=2.5, fast=True)), Params())[2]
pt = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, capture_output=True, text=True)
tests = pt.stdout.strip().splitlines()[-1] if pt.stdout.strip() else "pytest not run"
facts = (f"## FAITS MESURÉS À LA GÉNÉRATION DE CE BLOC\n- pytest : {tests}\n- Histoire graine 42, drift_amp 2.5, Params() par défaut, jour 7 : "
         f"{json.dumps(dict(st.loc[7]))}\n- Dépôt : {URL} (le dépôt GitHub peut être vide : le code utile est dans ce bloc)\n")
tree = [t for t in sh("git", "ls-files").splitlines() if not t.endswith(".png") and "__pycache__" not in t]
def code(p):
    lang = {"json": "json", "csv": "csv", "md": "markdown", "txt": "text", "py": "python"}.get(p.rsplit(".", 1)[-1], "text")
    return f"### {p}\n```{lang}\n{R(p).strip()}\n```\n"
tasks = json.load(open(os.path.join(ROOT, "docs/team/tasks.json"), encoding="utf-8"))["tasks"]
cards = "## Annexe F — Fiches de tâches par rôle (fais UNIQUEMENT celles de ton rôle)\n"
for role in ("M2", "M3", "M4"):
    cards += f"### ROLE {role}\n"
    for t in [x for x in tasks if x["role"] == role]:
        cards += (f"**{t['id']} · {t['titre']}** — quand : {t['quand']}\n- Pourquoi : {t['pourquoi']}\n- Étapes : " + " / ".join(t["etapes"]) +
                  f"\n- Fini quand : {t['fini_quand']}\n- Instruction détaillée : {t['prompt']}\n\n")
out = [f"<!-- commit {commit}{' (working tree modified)' if dirty else ''} · généré le {now} · NE PAS MODIFIER À LA MAIN (scripts/build_blocks.py) -->\n",
       R("docs/blocks/code_header.md"), facts,
       "# ANNEXES (référence technique exacte)\n",
       "## Annexe A — Arborescence du dépôt (fichiers suivis par git)\n```\n" + "\n".join(tree) + "\n```\n",
       "## Annexe B — Contrats (NE PAS MODIFIER)\n" + "".join(code(p) for p in sorted(glob.glob("contracts/*.json", root_dir=ROOT))),
       "## Annexe C — Code existant\n" + "".join(code(p) for p in ["csync/__init__.py", "csync/rules.py", "csync/gate.py", "csync/sendqueue.py", "csync/language.py", "csync/config/theme.json", "csync/config/strings_en.json", "requirements.txt"]),
       "## Annexe D — Décisions ouvertes, histoire et protocoles\n" + R("docs/OPEN_DECISIONS.md") + "\n" + R("docs/STORY.md") + "\n" + R("docs/PROTOCOLES.md") + "\n" + R("docs/PROGRAMME_OFFICIEL.md") + "\n",
       "## Annexe E — Règles Git\nUne branche par tâche, jamais de travail direct sur main, une pull request par tâche, pytest vert avant la PR. M1 fusionne.\n",
       cards,
       "## Annexe G — Fichiers complets\n" + "".join(code(p) for p in ["synthetic/generator.py", "csync/ui/app.py", "scripts/run_story.py", "docs/HELP_CARD_SOURCES.md", "research/pilot/RESULTS.md", "data/real/eda_rr1_iss_hourly_2014-09-26_to_10-05.csv", "data/real/PROVENANCE_fr.md"] + sorted(glob.glob("tests/test_*.py", root_dir=ROOT))),
       "\n---\n# FIN DU BLOC. Attends la ligne « MON RÔLE : ... » de l'utilisateur (section 2).\n"]
od = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out_blocks"); os.makedirs(od, exist_ok=True)
path = os.path.join(od, f"BLOC_CODE_{commit}.md"); open(path, "w", encoding="utf-8").write("\n".join(out))
print(path, len(open(path, encoding="utf-8").read()) // 1024, "Ko")
