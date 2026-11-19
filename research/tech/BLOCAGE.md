# Blocage — jalon 1, 19/11/2026

Décision de Joseph le 19/11 : le verrou rouge est attendu. Les quatre modules sont commités sans modifier tests/test_reachability.py. Le rapport à jour est RAPPORT_CURSOR.md.

## Blocage initial (dépassé)

Le module `csync/analytics/changepoint.py` et `tests/test_changepoint.py` sont écrits. Les 8 tests du module passent. La suite complète ne passe pas, et les deux essais autorisés sont épuisés. Jalons 2, 3 et 4 non commencés. Les fichiers du module ne sont pas commités : un commit exige une suite verte.

## Essai 1
`python -m pytest -q` : 3 failed, 306 passed.
- `tests/test_lint.py` : `ruff` absent. Corrigé par `pip install -r requirements-dev.txt` (aucun fichier du dépôt modifié).
- `tests/test_reachability.py::test_no_new_orphan_module` : orphelin nouveau `csync.analytics.changepoint`. Autorisés : `csync.assistant`, `csync.memory`.
- `tests/test_reachability.py::test_no_new_dead_function` : noms publics sans appelant produit : `bocpd`, `cusum`.

## Essai 2
Correction interne seulement : la masse utile de BOCPD est le régime le plus probable (avec un aléa constant, P(longueur 0) vaut toujours l'aléa) ; l'écart de la graine de contrôle est `Person.rt_day_sd = 10`, pas l'écart des 5 premiers jours. `k=0.5` et `h=4` restent ceux gelés sur la graine A `11011`.
`python -m pytest -q tests/test_changepoint.py` : 8 passed.
`python -m ruff check csync` : All checks passed.
Le verrou reste rouge :
`unreachable csync modules: ['csync.analytics.changepoint', ...]`
`public names no product code uses: [..., 'bocpd', 'cusum', ...]`

## Pourquoi je n'ai pas contourné
`tests/test_reachability.py` n'atteint un module que depuis `csync/ui/app.py` ou `scripts/run_story.py`. Le contrat interdit d'éditer `csync/ui`. `scripts/run_story.py` et `tests/test_reachability.py` sont hors de la liste de Cursor. Le fichier dit que `KNOWN_ORPHANS` ne peut que rétrécir : y ajouter ce module rendrait le test vert en violant sa propre règle.

## Lint demandé
`ruff check csync tests` : 62 erreurs déjà présentes sur `glass-navy` (SIM115, F401, B007, B905, F541), aucune dans `csync/analytics` ni `tests/test_changepoint.py`. Je ne les corrige pas : ces fichiers sont hors liste.
