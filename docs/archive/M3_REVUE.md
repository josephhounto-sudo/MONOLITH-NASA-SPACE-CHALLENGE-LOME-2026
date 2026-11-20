# Revue du travail de M3 (dimanche 15/11/2026 07:20 UTC)
FAIT PAR L'IA. Source : `csync/ui/app.py` de M3 lu sur son ordinateur (dossier de son clone, fichier non commité, 8 705 octets), comparé ligne à ligne à `main`. Ni sa branche ni ses commits n'existent sur GitHub.

| Changement de M3 | Verdict | Preuve |
|---|---|---|
| Journal de reprise affiché deux fois (dans « technical log » et en dessous) : suppression de la répétition | **Repris** | Les 13 tests d'écran passent après le retrait |
| `elif day <= 5:` au lieu de `state == "UNKNOWN" and day <= 5` : « baseline en construction » pour tout état aux jours 1 à 5 | **Refusé** | Masquerait un état réel (ex. symptôme déclaré) aux jours 1 à 5 : contraire à la règle « inconnu n'est jamais normal / rien n'est caché ». Le comportement actuel est déjà correct (états UNKNOWN pendant la référence) |
| Cartes plus grandes (rembourrage 16, nom 1,3 em, état 1,6 em) | **Non repris ici, transmis au design** | Casse 3 tests (`test_screen_nominal_day7`, `_action_day9`, `_resume_refused_day10`) : ils exigent `font-size:1.1em`. L'idée (mot d'état en grand) est celle du brief de M1 ; la session de design la reprend avec les tests mis à jour |
| Fichiers de M3 : aucun autre | — | Seul `app.py` a changé dans son dossier |

Conclusion : le travail de M3 se réduit à une retouche de style et une correction mineure. Les trois écrans (Nominal, Action, Reprise) existaient déjà sur `main`. Rien d'autre n'est à récupérer chez M3.
