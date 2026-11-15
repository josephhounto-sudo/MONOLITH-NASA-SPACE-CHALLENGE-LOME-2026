# Essai sur un jeu ouvert — PMData

FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ. Ce n'est pas une validation. Personne ici n'est un astronaute, et le jeu n'est pas un analogue de mission.

Consultation le 15/11/2026.

## Jeu retenu

| | |
|---|---|
| Nom | PMData, journal sportif de 16 personnes, environ cinq mois |
| Fichiers | `data/real/raw/pmdata/p01` … `p16` : `pmsys/wellness.csv` (16 fichiers) et `fitbit/resting_heart_rate.json` (14 fichiers). p12 et p13 n'ont pas de fichier `resting_heart_rate.json` sur OSF (leur dossier Fitbit listé le 15/11/2026 contient `time_in_heart_rate_zones.json`, pas une fréquence de repos quotidienne). |
| Page des fichiers | https://osf.io/vx4bk/ (API OSF lue le 15/11/2026) |
| Article | Crossref, même jour : DOI `10.1145/3339825.3394926`, titre « PMData » (2020) ; prépublication DOI `10.31219/osf.io/k2apb`. Le PDF `MMSys_Dataset_2020_Sports_Logging.pdf` a été téléchargé depuis `https://osf.io/k2apb/download` et lu avec `pdftotext`. |
| Licence | Dans ce PDF : « free to use for research and teaching purposes » sous CC BY-NC 4.0 (`https://creativecommons.org/licenses/by-nc/4.0/`). L'enregistrement de licence du nœud OSF `vx4bk`, lu le même jour via l'API, dit CC BY 4.0. Les deux mentions sont rapportées ; les fichiers sont gardés pour cet essai de recherche, avec la citation Thambawita et al., MMSys 2020, et le lien OSF. |
| SHA-256 | `data/real/raw/SHA256SUMS.txt`, une ligne par fichier sous `pmdata/`. |

Ce que le PDF décrit, et que les fichiers confirment : `wellness.csv` a, chaque jour, fatigue, humeur, préparation, durée de sommeil en heures, qualité de sommeil, courbatures et stress. Humeur, stress, fatigue, qualité de sommeil et courbatures sont sur une échelle 1–5 : 3 est « normal », 1–2 en dessous, 4–5 au-dessus. La fréquence cardiaque de repos Fitbit est un nombre par jour.

Adaptateur : `csync.adapters.pmdata_measurements`. Même contrat que `eda_measurements` (enregistrement Measurement, `origin` = `REAL_OPEN`). Champs utilisés : sommeil → `PH09`, stress → `PS02`, humeur → `PS03`, fréquence de repos → `PH01`. Un jour Fitbit avec date vide et valeur 0 est `MISSING` (c'est ainsi que le fichier marque un jour vide, pas un seuil). Script : `python research/analog_pmdata.py`. Sortie : `research/analog_pmdata_results.json`.

`csync.rules.daily_values` ne lit que `source_id` `SYN` ou `WRIST`. Le script construit donc le tableau quotidien à partir des mesures, puis appelle `csync.rules.evaluate` avec `Params()` **sans modifier** `csync/rules.py`. Les indicateurs absents (temps de réaction `CO01` et `CO02`, somnolence `PS01`, charge `PS04`) sont laissés manquants, pour que la dimension reste `UNKNOWN` tant que la ligne « donnée manquante » de la règle s'applique.

## Ce que la règle a produit

16 personnes. 2 343 jours de calendrier au total (du premier au dernier jour daté de chaque personne, trous compris). 2 098 de ces jours ont au moins une valeur. 7 044 mesures. Après les 5 jours de référence de chaque personne : 2 263 jours notés.

| Dimension | NORMAL | WATCH | DEGRADED | UNKNOWN |
|---|---|---|---|---|
| Corps | 1 055 | 207 | 8 | 993 |
| Attention | 0 | 0 | 0 | 2 263 |
| Moral | 0 | 0 | 0 | 2 263 |

Jours avec `OPEN_PROCEDURE` : **0**.

La règle ne dit rien d'utile ici pour ouvrir une procédure. Une procédure demande deux dimensions hors de la normale. Attention n'est jamais notée : le jeu n'a pas de temps de réaction. Moral reste `UNKNOWN` tous les jours : somnolence et charge manquent, et le couple humeur + stress n'a jamais été marqué deux fois le même jour sur ces fichiers. Le Corps seul, même les 8 jours `DEGRADED`, n'ouvre rien.

Les 207 jours `WATCH` et les 8 jours `DEGRADED` du Corps sont un écart à la référence personnelle des cinq premiers jours de chaque fichier, sur le sommeil déclaré et la fréquence de repos Fitbit. Les échelles 1–5 ne sont pas celles du prototype (KSS, 0–10). Les planchers absolus livrés (`PS02` = 1, `PS03` = 0,5) s'appliquent quand même, parce que la règle n'a pas été modifiée. Rien de ceci n'est un résultat sur un équipage.

## Ce qui n'est pas mesuré

Temps de réaction, lapses, somnolence KSS, charge de travail, tension, température, glycémie, symptôme. Pas de contexte de mission. Pas d'isolement. Personnes au sol, journal d'entraînement, pas un vol.

## Autres jeux cherchés, non utilisés pour l'essai

- **MMASH** (PhysioNet), page `https://physionet.org/content/mmash/1.0.0/` lue le 15/11/2026. Licence Open Data Commons Open Database License v1.0. DOI v1.0.0 lu sur la page : `10.13026/cerq-fc86`. La page dit 24 heures de battements, d'actimétrie, de sommeil et de caractéristiques psychologiques pour 22 personnes. Une référence de 5 jours ne peut pas se construire. Fichier non téléchargé, donc pas de SHA-256.
- **NASA OSDR, Inspiration4.** Résultat de recherche du 15/11/2026 (page NASA « I4 Mission Datasets ») : sang, écouvillons, biopsies, données traitées ; pas de série quotidienne sommeil / fréquence cardiaque / temps de réaction. La FAQ OSDR, dans le même résultat de recherche, dit que les données de séquence issues d'astronautes sont en accès contrôlé. Non téléchargé.
- **Sommeil et PVT en vol ISS.** Article PMC8919197, déclaration de données lue : les données sont dans le Life Sciences Data Archive de la NASA et s'obtiennent sur demande. Pas un fichier ouvert. Non téléchargé.
- **Catalogue déjà dans le dépôt** (`docs/audit_gemini/NASA_DATA_CATALOG_VERIFIE.md`, 14/11/2026) : EDA est de la télémétrie de cabine, pas une personne ; PhysioNet Wearable Device Dataset est un stress induit de courte durée, pas plusieurs jours de sommeil et d'humeur. Non repris pour cet essai.
