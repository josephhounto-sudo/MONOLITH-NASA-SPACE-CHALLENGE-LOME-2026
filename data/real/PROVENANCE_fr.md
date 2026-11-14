# Provenance — S10 PhysioNet Wearable Device Dataset v1.0.1
Hongn, A., Bosch, F., Prado, L., & Bonomini, P. (2025). Wearable Device Dataset from Induced Stress and Structured Exercise Sessions (version 1.0.1). PhysioNet. https://doi.org/10.13026/he0v-tf17
Licence: Open Data Commons Attribution License v1.0.
Accès le 14/11/2026 vers 04:20 (Lomé) via le navigateur de M1, pages de prévisualisation PhysioNet
(/content/.../<fichier>). LIMITE : la prévisualisation n'affiche que les 500 premières lignes de chaque fichier :
HR = 498 s (~8,3 min à 1 Hz), TEMP = 498 échantillons (~2 min à 4 Hz), IBI = 499 battements.
Les statistiques sont donc celles du DÉBUT de séance (ligne de base de 3 min + début du protocole), pas de la séance entière.
Statistiques calculées dans le navigateur (JavaScript), puis copiées ici.
hr_base_* = HR échantillons 10 à 190 (on saute les 10 premières secondes de démarrage du capteur).
rmssd5_ms = RMSSD sur les IBI des 300 premières secondes, seulement entre battements consécutifs détectés (écart < 0,05 s).
ibi_cov_5min = somme des IBI détectés / 300 s (part du temps couvert par des battements détectés).
Contraintes officielles (data_constraints.txt) : S02 données dupliquées ; f07 cache de protection non retiré (PPG et TEMP invalides) ; f14 fichier scindé (f14_a, f14_b).
Stress_level_v1/v2 : niveaux de stress auto-déclarés de 0 à 10 (l'article dit 1 à 10 ; des valeurs 0 et 0,5 existent), copiés intégralement.

# Provenance — S03 NASA OSDR Environmental Data App (EDA)
Mention obligatoire : « Data and visualizations are courtesy of the Environmental Data App (EDA) (https://visualization.osdr.nasa.gov/eda/), Version # » (numéro de version à relever sur la page).
Accès le 14/11/2026 vers 04:25 (Lomé) via le navigateur de M1 : données JSON intégrées aux pages /eda/dashboard_<mission> (les mêmes que les graphiques).
UNITÉS VÉRIFIÉES sur la page (libellés d'axes) : température en °C, humidité relative en %, CO2 en ppm, rayonnement en mGy/jour (dose cumulée en mGy).
CADENCE VÉRIFIÉE : 5 minutes (RR-1 à RR-19) ou 1 minute (RR-10, RR-18, RR-20, RR-23, RR-25, RR-28).
Missions lues : 17 listées, 14 avec télémétrie exploitable (RR-4, RR-8, RR-17 : format différent, non lues).
eda_mission_stats.csv : statistiques sur la série complète de chaque mission (calcul dans le navigateur).
eda_quality_flags.csv : comptage de valeurs suspectes (CO2 ≤ 500 ppm, RH > 100 %, etc.) et de « plateaux » (même valeur CO2 plus de 60 min).
eda_rr1_iss_hourly_*.csv : moyennes horaires ISS de RR-1 sur 10 jours (26/09 au 05/10/2014), 12 points de 5 min par heure.
eda_rr1_radiation_daily.csv : doses quotidiennes RR-1 complètes.
LIMITE : ces données viennent de missions Rodent Research (capteurs de cabine ISS pendant des expériences sur rongeurs), pas d'un équipage suivi individuellement.

# NLSP (NASA Life Sciences Portal) — recherche de données humaines ouvertes
Accès le 14/11/2026 vers 04:35 via le navigateur de M1 : catalogue complet des 2 676 expériences (API publique du portail).
Filtre : humain + mention « publicly available » + variables proches de C-Sync (PVT, sommeil, FC, tension, température, glycémie, humeur, stress, fatigue) : 93 expériences.
Les plus proches : NAG53952 (lumière intermittente, Czeisler ; PVT, KSS, journal de sommeil, température centrale) et NAG91161 (vulnérabilité au manque de sommeil ; PVT, KSS).
Vérifié sur la fiche NAG53952 : les « Open-Access Data » se limitent au RAPPORT FINAL (niveau « Summarized »), pas aux mesures individuelles.
Conclusion : NLSP confirme qu'il n'existe pas de série individuelle ouverte et téléchargeable PVT + sommeil + FC ; les études sont citables comme travaux antérieurs, pas comme données.

# Complément EDA — vérification par Chrome le 14/11/2026 (≈ 13:00 Lomé)
Contrôle croisé avec le site (API /eda/api/missions/ : 24 missions listées, pas 17).
RR-1 : identique au site (39 jours de rayonnement, somme GCR 5,11484, SAA 2,84822, total 7,96306 mGy ; 12 087 points ; moyennes et écarts-types identiques).
Ajouts à eda_mission_stats.csv (même méthode, écart-type de population) : APEX-03-1, APEX-03-2 (pas de CO2 : 100 % manquant), RR-22 (1 min).
Ajouts à eda_radiation_summary.csv : RR-4, RR-8, RR-17 (rayonnement seul, pas de télémétrie).
Sans valeur exploitable (toutes les séries à 100 % manquant) : APEX-04, VEG-01A, VEG-01C ; VEG-01B : aucune télémétrie ni rayonnement.
ATTENTION RR-22 : p05 et minimum = 0,0 pour température, humidité et CO2 (zéros de capteur, non filtrés) et CO2 plafonné à 5000 ppm ; 9,91 % de valeurs sol manquantes. À traiter comme données suspectes, ne pas citer sans filtrage.
ATTENTION APEX : matériel de culture de plantes (température 1,5 à 24,7 °C), pas la cabine équipage.
Colonne daily_mean_sd des lignes ajoutées : écart-type de population sur moyennes par jour UTC ; sur RR-1 cette méthode donne 0,58 / 5,51 / 520,04 contre 0,59 / 5,64 / 532,57 dans les lignes d'origine (écart ≤ 2,5 %, méthode d'origine non retrouvée). Les autres colonnes sont identiques à RR-1.
Les séries brutes complètes ne sont pas copiées ici (≈ 700 Ko par mission, intégrées aux pages du site) : elles restent lisibles en ligne.

# Complément PhysioNet S10 — ZIP complet analysé le 14/11/2026 (≈ 12:00 Lomé)
Téléchargé par M1 (accord donné) : wearable-device-dataset-1.0.1.zip, 73 121 143 octets (69,7 Mo), source https://physionet.org/content/wearable-device-dataset/get-zip/1.0.1/ . Le ZIP lui-même n'est pas dans le dépôt (259 Mo décompressé, 709 fichiers).
Intégrité : 708 fichiers sur 708 conformes à SHA256SUMS.txt (0 écart, 0 manquant).
Nouveau fichier : s10_stress_full_session_stats.csv = statistiques de la SÉANCE ENTIÈRE pour les 37 participants du protocole STRESS (HR 1 Hz, TEMP 4 Hz) ; durées 11,6 à 80,0 min (médiane 36,9). Remplace la limite « 500 premières lignes » des extraits d'origine.
Contrôle : hr_base_mean est identique pour les 37 participants entre ce fichier et s10_stress_first_window_stats.csv (0 écart) : les extraits du 14/11 matin sont confirmés.
Dossier physionet_s10_docs/ : README, Data_Dictionary, data_constraints, LICENSE (ODC-By 1.0) et SHA256SUMS copiés tels quels.
Non intégrés (volume) : séries brutes ACC/BVP/EDA/HR/IBI/TEMP des dossiers AEROBIC et ANAEROBIC, et séries brutes STRESS ; elles restent dans le ZIP de M1 (Téléchargements) et sur PhysioNet.
Rappel des contraintes officielles : S02 données dupliquées ; f07 PPG et TEMP invalides ; f14 fichier scindé. Les statistiques de ces trois participants sont à ne pas citer sans précaution.

# Séries brutes EDA — 24 missions (14/11/2026, 12:31 UTC)
data/real/raw/eda_all_missions.json.gz (4,05 Mo ; 35,4 Mo décompressé ; sha256 dans data/real/raw/SHA256SUMS.txt) : télémétrie et rayonnement bruts des 24 missions listées par l'API, tels que fournis par les pages /eda/dashboard_<mission>. Téléchargé par M1 (accord donné). Lecture : python scripts/eda_load.py.
Contrôle : les 94 lignes de eda_mission_stats.csv (nombre de valeurs valides et moyenne) sont retrouvées à l'identique à partir de ce fichier (0 écart).
Brut PhysioNet : trop lourd pour git (69,7 Mo). Pour le récupérer : https://physionet.org/content/wearable-device-dataset/1.0.1/ (bouton « Download the ZIP file »), puis vérifier avec SHA256SUMS.txt du ZIP.
