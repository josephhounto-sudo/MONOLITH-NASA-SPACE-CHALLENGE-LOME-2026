# Rejeu rétrospectif sur des missions ISS réelles — pré-enregistrement

Écrit et commité AVANT tout calcul de résultat (le commit fait foi de l'heure). Rien ci-dessous ne sera modifié après le calcul; tout écart sera écrit dans RESULTS.md.

## Question
Sur la télémétrie CO2 réelle de cabine ISS (NASA OSDR Environmental Data App, 14 missions, fichier brut data/real/raw/eda_all_missions.json.gz, somme de contrôle vérifiée), qu'est-ce que la règle Habitat de C-Sync aurait montré à l'équipage, et qu'aurait-elle montré de plus qu'une lecture en moyenne journalière?

## Ce qu'on ne peut PAS mesurer (écrit avant)
- Aucun effet sur la santé: les symptômes de l'équipage (conférences médicales privées) ne sont pas publics.
- Aucune comparaison avec ce que voyaient les contrôleurs au sol: leurs écrans et décisions ne sont pas publics.
- Emplacement et étalonnage du capteur: non documentés dans le jeu de données.

## Règle gelée (code existant, non modifié)
- csync.habitat: moyenne d'une heure > 3,00 mmHg (NASA-STD-3001 Vol 2 V2 6004) = ATTENTION; heures ARTIFACT (plateau identique ≥ 1 h, csync.quality.flag_plateaus) exclues; conversion ppm→mmHg à 760 mmHg.
- Contexte publié, jamais une décision: moyenne glissante 7 jours comparée à 2,0 mmHg (Law et al. 2014, J Occup Environ Med: risque de céphalée < 1 % par semaine sous ce niveau) et à 1,5 mmHg (Cole et al., NTRS 20160012725: congestion < 1 %).

## Comparateur (pré-déclaré)
Lecture en moyenne journalière contre 3 mmHg. Mesure: heures au-dessus de 3 mmHg contenues dans des jours dont la moyenne est sous 3 mmHg (dépassements cachés par la moyenne).

## Mesures, par mission
heures valides; heures ARTIFACT; heures > 3 mmHg; épisodes (suites contiguës d'heures > 3); plus long épisode; jours avec moyenne > 3; heures cachées par la moyenne journalière; part des jours dont la moyenne 7 j dépasse 2,0 et 1,5 mmHg.

## Critères d'échec (écrits avant)
- Si les alertes tombent surtout pendant des heures ARTIFACT, la règle ne sert à rien telle quelle.
- Si plus de 50 % des heures déclenchent, c'est une alarme permanente (fatigue d'alarme): à dire.
- Si les dépassements cachés par la moyenne journalière sont nuls sur toutes les missions, l'argument « C-Sync montre ce que la moyenne cache » tombe.
