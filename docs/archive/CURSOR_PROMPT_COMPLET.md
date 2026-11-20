# Prompt Cursor — C-Sync (équipe MONOLITH) — à coller tel quel

## Comment le lancer (guide pour Joseph)

1. Ouvre Cursor, dossier du dépôt C-Sync. `git fetch && git checkout -b cursor-1 origin/main`.
2. Ouvre le chat de l'agent (Cmd/Ctrl+I), mode **Agent**. Colle tout le bloc « PROMPT » ci-dessous.
3. Crédits : choisis le modèle À LA MAIN en bas du chat (Claude, GPT ou Gemini). Pas le mode Auto : `AGENTS.md` règle 9 l'interdit. Évite le mode **Max** sauf besoin réel (plus cher).
4. Suivi de la consommation : cursor.com/dashboard, onglet usage. Tu peux y fixer une limite de dépense.
5. Les tarifs et quotas affichés dans la documentation Cursor ne sont pas cohérents d'une page à l'autre : ne te fie qu'à ton tableau de bord.
6. Les agents cloud demandent un compte Premium (indiqué par Cursor). Sans cela, utilise l'agent local.
7. Quand il a fini : lance `python -m pytest -q`, puis pousse la branche `cursor-1` (jamais `main`). Un humain fusionne.

## PROMPT

Contexte. Projet C-Sync (Care Sync), équipe MONOLITH, NASA Space Apps Challenge 2026 Lomé. Pitch dimanche 15/11 à 12:00. App Streamlit : `csync/ui/app.py`. Règle v3 dans `csync/rules.py` : écart ≥ 1,5 écart-type par rapport à la ligne de base personnelle des jours 1–5, deux jours consécutifs ; une valeur manquante donne UNKNOWN, jamais NORMAL. Les données de l'équipage sont synthétiques (`synthetic/generator.py`, graine 42). Les données NASA réelles sont dans `data/real/raw/eda_all_missions.json.gz` (télémétrie d'habitat, pas de physiologie d'équipage réelle). Validation : graines de réglage 1000–7149, graines de test 30000–37149 (`docs/VALIDATION_HOLDOUT.md`).

Lis d'abord : `docs/ECART_DEFI_ET_PLAN.md`, `docs/CURSOR_TACHE_LOURDE.md`, `docs/CURSOR_HANDOFF.md`, `docs/RELAIS_15-11_0850.md`.

Règles non négociables :
- Aucun mot de la liste interdite (`tests/test_banned_words.py`). Ne rien inventer qui ne soit pas dans le dépôt : si une donnée manque, écris `TODO_M1`.
- Ne pas modifier `contracts/`.
- Fichiers INTERDITS : `csync/ui/app.py`, `docs/`, `pitch/`, `AI_USAGE.md`. Ne pas toucher aux fichiers d'une autre tâche.
- Lis `AGENTS.md` (règles 1–9 ; message de commit `M2: ce que tu as fait`). Texte affiché au jury en anglais.
- Branche `cursor-1` uniquement, jamais `main`. Les tests passent avant tout push.
- Ne jamais affirmer que le projet a été codé par un étudiant en médecine : le dépôt ne le dit pas, et l'usage de l'IA est déclaré.

Tâches (fichiers disjoints) :
1. `research/ewma_compare.py` + test : comparer la règle v3 à une EWMA sur les graines de test 30000–37149, mêmes métriques que `research/pilot/holdout_results.json`. Rapporter les chiffres tels quels, y compris défavorables.
2. `csync/quality.py` + tests : contrôles de qualité des données (valeurs hors plage, trous, séries constantes). Un trou produit UNKNOWN.
3. `csync/memory.py` + `tests/test_adapters_memory.py` : mémoire de l'état par membre, déterministe.
4. `csync/config/strings_fr.json` : traduction française de toutes les clés de `strings_en.json`, mêmes clés, même ordre. Test de parité des clés.
5. `tests/test_claims.py` : un test par chiffre affiché sur le site ou le diaporama (92,7 % ; 57,3 % ; 0/300 ; 759 525 points ; 195 tests), calculé depuis les fichiers sources, pas copié.

Livrable : un commit par tâche, message court, puis un résumé de 10 lignes avec ce qui n'a pas pu être fait.
