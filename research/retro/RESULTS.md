# Rejeu rétrospectif ISS — résultats (20/11/2026)

Pré-enregistrement: PREREGISTRATION.md, commit 9c4994b (05:21 UTC), avant tout calcul. Script: replay.py. Chiffres: replay_results.csv. Un écart au plan, déclaré : le seuil de contexte 7 jours passe de 2,0 mmHg (résumé de presse de Law 2014) à 2,5 mmHg, valeur écrite par la NASA elle-même (OCHMO-TB-004 : moyenne 7 jours < 2,5 mmHg pour un risque de céphalée < 1 %). Changement fait après le premier calcul, parce que la source officielle contredit le résumé ; il ne touche pas la règle d'alerte.

## Résultats (14 missions, télémétrie CO2 réelle de cabine ISS, NASA OSDR EDA)
- Dépassements cachés par une lecture journalière: 370 heures au-dessus de 3 mmHg tombaient dans des jours dont la moyenne restait sous 3 mmHg, sur 8 missions sur 14 (RR-28: 215 h; RR-3: 57 h; RR-1: 31 h). Critère d'échec 3 non atteint: l'argument « l'heure montre ce que la journée cache » tient.
- Fatigue d'alarme: aucune mission au-delà de 50 % d'heures en alerte, mais deux s'en approchent (RR-28: 46,5 %, 57 épisodes en 44 jours; RR-3: 41,9 %, dont un épisode continu de 364 h sur une mission où le capteur touche zéro ou plafonne). Une alerte par heure serait inutilisable pour l'équipage: l'unité à afficher est l'épisode, pas l'heure. Critère d'échec 2 non atteint, mais de peu.
- Heures ARTIFACT (plateaux identiques ≥ 1 h): 1 755 heures exclues au total; elles n'ont jamais compté comme normales.
- Contexte publié (jamais une décision): la moyenne 7 jours dépasse 2,5 mmHg (OCHMO-TB-004) sur plus de la moitié des jours de 5 missions (RR-3 88 %, RR-28 88 %, RR-7 65 %, RR-1 56 %, RR-9 56 %).

## Ce que ce rejeu ne montre pas
- Aucun effet sur la santé: les symptômes de l'équipage ne sont pas publics.
- Pas une comparaison avec la NASA: les contrôleurs au sol suivent le CO2 bien plus finement qu'une moyenne journalière; le comparateur est une lecture simple choisie par nous.
- Capteur: emplacement et étalonnage non documentés; conversion ppm→mmHg à 760 mmHg = approximation.
- Capteur de cabine, pas zone de respiration: le CO2 peut rester plus élevé près du visage (Aerospace Medicine and Human Performance, 2025, vol. 96 n° 11); la valeur affichée sous-estime peut-être l'air respiré.

## Conséquence pour le produit (proposition, pas un résultat)
Afficher les épisodes (début, durée, valeur max) plutôt que chaque heure; afficher la moyenne 7 jours face aux niveaux publiés comme contexte.
