# Prompt Cursor — bloc unique (19/11/2026)
Modèle: choisi à la main (Claude, GPT ou Gemini), jamais Auto.

```
Lis AGENTS.md, puis docs/CONTRACTS_TECH.md en entier. Ignore la mention de gel des fonctions de AGENTS.md: décision de Joseph du 19/11, le gel ne s'applique plus.
Branche: tech-modules, créée depuis glass-navy (git fetch; git checkout -b tech-modules origin/glass-navy).

Travail en 4 jalons, dans cet ordre. Après CHAQUE jalon: python -m pytest -q vert, ruff check csync tests propre, un commit "TECH: <module>", puis passe au suivant. Si un jalon échoue après 2 essais, arrête-toi et écris le blocage dans research/tech/BLOCAGE.md au lieu de contourner.
1. csync/analytics/changepoint.py (+ tests/test_changepoint.py)
2. csync/crypto/capsule_sign.py (+ tests/test_capsule_sign.py)
3. csync/sync/crdt_sim.py (+ tests/test_crdt_sim.py)
4. csync/physio/hrv.py (+ tests/test_hrv.py)

Règles: signatures EXACTES du contrat; tests écrits avant le code; jeu de réglage et jeu de contrôle séparés et écrits dans le test; aucune donnée réelle chargée; tout objet non réel étiqueté SIMULATED; mots interdits dans chaînes et docs: cause, diagnos*, prove/proves, guarantee, disease.
Interdits: modifier csync/ui, csync/rules.py, csync/gate.py, contracts/, tout autre fichier hors liste du contrat. Pas de push sur main.
À la fin: rapport de 5 lignes par module (quoi / vérifié comment / non vérifié / ce qui peut casser / comment annuler), dans research/tech/RAPPORT_CURSOR.md, puis push de la branche tech-modules.
```

Requête 2 (audit, séparée): « Sur les trois modules changepoint, capsule_sign, crdt_sim: écris des tests de propriétés et de mutations qui échouent si on change un seuil, un signe ou un ordre. Ne modifie pas le code des modules; signale ce qui survit aux mutations dans research/tech/MUTATIONS.md. »
