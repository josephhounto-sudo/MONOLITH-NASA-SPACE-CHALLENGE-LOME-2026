# Rapport M2 — tâche lourde du 15/11/2026

FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ. Branche `m2-heavy-1`. `docs/PITCH_FIGE_ET_REPONSES.md` n'est pas dans le dépôt. `pitch/deck/make_fr.py` non plus. Rien n'a été poussé sur `main`. `csync/rules.py`, `contracts/`, `csync/ui/`, `csync/silhouette.py` et `pitch/` n'ont pas été modifiés.

## Tests

`python -m pytest -q` en fin de branche : **199 passed, 2 failed** (201 collectés, 38 s).

1. `tests/test_claims.py::test_deck_figures_match_recalculated_sources` — écart du diaporama, test laissé tel quel (H6).
2. `tests/test_habitat.py::test_rebuild_matches_committed_files` — le CSV horaire reconstruit diffère du fichier commité de 0,01 °C sur `temp_c` (23,13 contre 23,12, index 158). `scripts/build_habitat.py` ne lit pas les fichiers PMData. Le CSV commité n'a pas été réécrit.

Aucun test ancien n'a été retiré. Ajouts : sensibilité (3), référence décalée (1), adaptateur PMData (1), parité français (1), chiffres du diaporama (1).

## H1 — Dossier de relecture

`docs/REVIEW_PACKET.md`. Trois pages : dérive, urgence guidée, porte de reprise. Chaque paramètre est chiffré depuis le fichier relu, avec « choix de conception » ou la source du dépôt. Quinze questions (cinq par règle). Ligne `relu par M4` vide : M4 n'a pas signé dans cette session.

## H2 — Sensibilité

`research/sensitivity.py`, `research/sensitivity_grid.csv`, `research/sensitivity_note.txt`, `docs/figures/sensitivity.png`. Graines 60000–60199 (témoin, 200), 62000–62149 (dérive histoire 1,5 ET, 150), 63000–63149 (saut 2 ET personnels, 150). Intervalles de Wilson via `pilot3.wilson`. La case (1,5 ; 2 ; 5) redonne `Params()` : `tests/test_sensitivity.py`, 3 verts.

Réglage livré sur ces graines : faux déclenchements 2,0 % (4/200, Wilson 0,8–5,0) ; dérive 92,7 % (139/150, 87,3–95,9) ; saut 56,7 % (85/150, 48,7–64,3). Seuil 1,0 et 2 jours : faux 14,5 %, dérive 98,7 %, saut 86,7 %. Seuil 2,5 et 2 jours : faux 0,0 %, dérive 58,0 %, saut 6,7 %. Un seul jour au seuil 1,5 : faux 27,5 %. Trois jours : faux 0,0 %, dérive 70,7 %, saut 28,0 %. Référence de 7 jours sur la dérive de l'histoire : 56,0 %, parce que la rampe commence au jour 6 et entre dans la moyenne. Compromis, pas un optimum. Ces taux ne sont pas ceux du pilote 3 (autres graines ; le saut d'ici est en écart-type personnel).

## H3 — Référence fatiguée

`research/biased_baseline.py`, `docs/BASELINE_BIAS.md`. Graines 65000–65149, 150 équipages synthétiques. Référence propre : 146/150, 97,3 % (93,3–99,0). Part des détections propres qui disparaissent : 15,8 % à 0,5 ET (23/146), 37,0 % à 1,0 ET (54/146), 63,7 % à 1,5 ET (93/146). La piste « référence avant mission » retrouve 146/150 sur la dérive injectée, et ouvre une procédure pendant la fenêtre fatiguée chez 50,7 % des équipages quand le décalage est 1,5 ET. Non adoptée.

## H4 — Jeu ouvert

`docs/ANALOG_TRIAL.md`, `csync/adapters.py` (`pmdata_measurements`), `data/real/raw/pmdata/`, empreintes dans `data/real/raw/SHA256SUMS.txt`. PMData, OSF `https://osf.io/vx4bk/`, PDF lu le 15/11/2026 : CC BY-NC 4.0 pour la recherche et l'enseignement. L'API OSF du même nœud affiche CC BY 4.0. Les deux sont écrits. 16 personnes, 2 343 jours de calendrier, 7 044 mesures. Après la référence : Corps 1 055 NORMAL, 207 WATCH, 8 DEGRADED, 993 UNKNOWN ; Attention et Moral UNKNOWN sur les 2 263 jours notés. **0 jour de procédure.** La règle ne dit rien d'utile ici pour ouvrir une procédure. Pas de temps de réaction. p12 et p13 n'ont pas de fichier de fréquence de repos.

Aussi cherchés, non utilisés : MMASH (PhysioNet, 24 h, ODbL, DOI `10.13026/cerq-fc86`, pas de SHA-256 car non téléchargé), Inspiration4 sur OSDR (pas de série quotidienne sommeil / fréquence / temps de réaction dans le résultat de recherche), sommeil et PVT ISS (PMC8919197 : données sur demande au LSDA).

## H5 — Français

`csync/config/strings_fr.json`. Mêmes clés, même ordre, mêmes `{variables}` que `strings_en.json` (`tests/test_strings_fr.py`). Vocabulaire aligné sur `pitch/deck/SCRIPT_FR.md` (dérive, référence, surveillance, dégradé, reprise, forçage du commandant, officier médical de bord). `app.py` n'a pas été touché. `make_fr.py` est absent.

## H6 — Chiffres du diaporama

Sources recalculées : `research/pilot/holdout_results.json` donne 0/300, 139/150 (92,666… % , arrondi 93) et 86/150 (57,333… % , arrondi 57). `csync.scale.raw_inventory()` sur le fichier brut NASA donne **759 525** points (20 missions avec télémétrie). Le texte visible de `pitch/deck/deck.html` contient « 0.7% of 300 simulated healthy crews », pas `0/300`, pas 93 %, pas 57 %, pas 759 525, pas « 6 crew ». La diapo 1 porte quatre noms, pas six équipiers. Le test qui exige la correspondance échoue. Il n'a pas été modifié pour passer. `pitch/` n'a pas été édité.

## H7 — Ce qui n'a pas pu être fait

- Signature M4 du dossier de relecture.
- Intégration du français dans l'application (réservée à la session design).
- Correction du diaporama (dossier `pitch/` interdit ici).
- Un jeu ouvert avec temps de réaction et au moins cinq jours par personne : non trouvé en téléchargement direct. L'essai PMData est fait, et il ne débouche pas sur une procédure.
- Suite entièrement verte : deux échecs, décrits ci-dessus.
