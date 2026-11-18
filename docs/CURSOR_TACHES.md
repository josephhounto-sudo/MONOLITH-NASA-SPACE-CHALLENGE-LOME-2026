# Tâches Cursor — lot 3 « attaquer la règle » (19/11/2026, avant 12:00 UTC)

But falsifiable: un relecteur expert qui attaque la règle de dérive et la porte de reprise ne trouve aucune erreur que le dépôt n'ait déjà écrite et chiffrée.
Budget: ~18 $ au 18/11 à 22:40. Dépenser 14 $ au plus. Arrêter à 4 $ restants et rendre compte. Mode Agent local, branche `cursor-v4` (déjà créée depuis `v2`).
Propriété: Cursor = `tests/`, `scripts/`, `requirements-dev.txt`. INTOUCHABLES: `csync/rules.py`, `csync/gate.py`, `csync/ui/`, `csync/config/`, `contracts/`, `AGENTS.md`, histoire gelée, `requirements.txt` (l'app déployée en dépend). Règle v3 gelée: une divergence se RAPPORTE, elle ne se corrige pas.

## Ordre et budget (valeur par dollar; un commit par tâche; tests complets verts avant chaque commit)
T1 oracle (4 $) → T3 propriétés de la porte (2 $) → T4 faux positifs (1,5 $) → T5 contrôle à froid (1,5 $) → T2 mutations (4 $).
Si un test échoue et que tu ne vois pas pourquoi en 2 essais: arrête cette tâche, écris-le dans le rapport, passe à la suivante.

## T1 — Oracle indépendant de la règle de dérive (~4 $)
Matière brute: la docstring de `csync/rules.py` (texte de la règle P-06) et `docs/METHODES_NASA_DOSSIER.md`. NE PAS lire `evaluate()` avant d'avoir écrit l'oracle.
Livrable: `tests/oracle_rule.py` (≤ 60 lignes, listes Python et `statistics`, pas de pandas) + `tests/test_rule_oracle.py`: test différentiel avec Hypothesis (≥ 2000 équipages: valeurs manquantes, plateaux, écart-type nul, jours 1-5 identiques) qui compare drapeaux, états et décisions de `evaluate()` à l'oracle.
Hypothèse la plus risquée à tester d'abord: le compteur de jours consécutifs traverse la frontière jour 5/6 (un jour de référence compte dans la série). Dis si le texte de la règle l'autorise, avec le contre-exemple minimal réduit par Hypothesis.
Échec écrit d'avance: au moins une divergence = résultat valide. Zéro divergence sur 2000 cas = écris le nombre de cas et la graine.

## T3 — Propriétés de la porte de reprise (~2 $)
`tests/test_gate_properties.py`, Hypothesis. Propriétés: (a) jamais `RESUME_AUTHORIZED` si la dernière mesure d'un prérequis dépasse sa limite; (b) un override seul n'autorise jamais; (c) ajouter une mesure plus ancienne ne change pas la décision; (d) entrée mal formée (clé absente, horodatage None): REFUSE ou erreur explicite, JAMAIS autorisé. (d) a des chances d'échouer: ne pas corriger `gate.py`, rapporter le contre-exemple.

## T4 — Faux positifs sur des graines jamais utilisées (~1,5 $)
`scripts/null_crews.py`: 1000 équipages sains via `csync.scale.crews` avec `seed0 >= 900000` (le réglage a utilisé 50000). Taux de faux positifs avec intervalle de Wilson à 95 %, comparé au « 0,7 % » de `docs/METHODES_NASA_DOSSIER.md` §7. Ne rien régler. Échec écrit d'avance: borne haute > 3 % → écrire le vrai chiffre dans le rapport, sans l'adoucir.

## T5 — Contrôle de démarrage à froid scripté (~1,5 $)
`scripts/cold_check.py URL` (Playwright): charge l'URL, attend le premier rendu, imprime le temps et le tampon de version, sort en code 1 si l'accroche attendue est absente (lire la phrase dans `csync/config/strings_en.json`, ne pas la recopier) ou si la page contient « Run: python », « Traceback » ou « not found ». Test sur une app locale `streamlit run csync/ui/app.py`. Joseph l'exécutera sur l'URL publique après déploiement.

## T2 — Mutations sur la règle et la porte (~4 $)
`mutmut` ne tourne pas sous Windows: UN essai, puis `scripts/mutate.py` maison (≤ 80 lignes, module `ast`: `>=`→`>`, `1.5`→`1.4`/`1.6`, `and`→`or`, constantes ±1) appliqué à `rules.py` et `gate.py` en copie temporaire; relancer `tests/test_rules.py`, `tests/test_gate.py`, T1, T3. Critère: ≥ 90 % de mutants tués sur `gate.py`, ≥ 85 % sur `rules.py`; chaque survivant reçoit un test qui le tue ou une justification « équivalent ». Liste brute des survivants dans le rapport.

## Règles transverses
`hypothesis` va dans `requirements-dev.txt` seulement. `python -m pytest -q` et `python scripts/compare_strings.py` verts avant chaque commit. Aucun message technique côté utilisateur. Messages de commit: pourquoi, pas seulement quoi. Pas de push sur autre chose que `cursor-v4`.

## À rendre
`docs/RAPPORT_CURSOR.md` (20 lignes): par tâche, FAIT / VERIFIED (sortie brute collée) / UNVERIFIED / divergences trouvées / dollars dépensés / ce qui peut casser / comment annuler.
