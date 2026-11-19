"""Rebuild docs/CONTEXTE_IA.md: one public, always-current file any member's AI can read by URL.
Run after every important change:  python scripts/build_context.py  then  git add -A && git commit && git push
Stable URL (once pushed): https://raw.githubusercontent.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026/main/docs/CONTEXTE_IA.md"""
import datetime, pathlib, subprocess
R = pathlib.Path(__file__).resolve().parent.parent
def rd(p): return (R / p).read_text(encoding="utf8")
try: sha = subprocess.check_output(["git", "-C", str(R), "rev-parse", "--short", "HEAD"], text=True).strip()
except (OSError, subprocess.CalledProcessError): sha = "inconnu"
now = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
head = f"""# C-Sync — contexte pour IA (généré le {now}, base commit {sha})
Source unique : ce dépôt public. Si ce fichier date de plus de 6 h, demande à M1 de le régénérer (P5/P8).
Règles pour l'IA qui lit ceci : ne lis que ce qui est ici ; si une page est inaccessible, dis-le ; n'invente rien ; réponds en français ; écris « NON VÉRIFIÉ » pour toute affirmation sans source ici.
Rôles : M1 chef/PO, M5 communication/soumission ; M2 capsule de décision ; M3 interface ; M4 procédures/scénarios. Pitch dim. 12:00-14:00 (5 min, sans questions) ; soumission dim. 23:59. Démo sur données SYNTHÉTIQUES, non validée sur de vrais équipages.
"""
parts = [("AGENTS.md", "RÈGLES POUR L'IA (AGENTS)"), ("docs/CURSOR_HANDOFF.md", "PASSATION : ÉTAT ET TÂCHES"), ("docs/CURSOR_TACHE_LOURDE.md", "TÂCHE LOURDE CURSOR"), ("README.md", "README"), ("docs/ARCHITECTURE.md", "ARCHITECTURE"), ("HYPOTHESES.md", "HYPOTHÈSES"),
         ("docs/OPEN_DECISIONS.md", "DÉCISIONS OUVERTES"), ("docs/RELEASE_CHECKLIST.md", "CHECKLIST DE LIVRAISON"),
         ("docs/MAJ_LOG.md", "JOURNAL DES MISES À JOUR"), ("docs/PROGRAMME_OFFICIEL.md", "PROGRAMME OFFICIEL"),
         ("docs/team/roles/TOUS.md", "CONSIGNES POUR TOUS")]
out = head + "".join(f"\n\n---\n# {t}\n\n" + rd(p) for p, t in parts if (R / p).exists())
(R / "docs" / "CONTEXTE_IA.md").write_text(out, encoding="utf8")
print(f"docs/CONTEXTE_IA.md : {len(out.split())} mots")
