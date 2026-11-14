# Catalogue de données — VÉRIFIÉ en ligne le 14/11/2026 (Chrome de M1)
Remplace G2 de Gemini (qui n'avait pas d'accès web). Rien ici n'est écrit de mémoire.

| Jeu | Source (page lue) | Contenu | Cadence | Licence / mention | Limite pour C-Sync |
|---|---|---|---|---|---|
| NASA OSDR Environmental Data App (EDA) | https://visualization.osdr.nasa.gov/eda/ ; API https://visualization.osdr.nasa.gov/eda/api/missions/ (24 missions listées) | Température (°C), humidité (%), CO2 (ppm) cabine ISS et sol ; rayonnement (mGy/jour) | 1, 5 ou 10 min | Mention : « Data and visualizations are courtesy of the Environmental Data App (EDA) » | Capteurs de cabine pendant expériences Rodent/plantes ; aucun humain suivi |
| EDA — missions avec télémétrie exploitable (20) | pages /eda/dashboard_<mission> | RR-1, 3, 5, 6, 7, 9, 10, 12, 18, 19, 20, 22, 23, 25, 28 ; APEX-03-1 et -03-2 (sans CO2) | — | idem | RR-22 : zéros de capteur et CO2 plafonné à 5000 ; APEX = culture de plantes |
| EDA — télémétrie vide | APEX-04, VEG-01A, VEG-01C (séries 100 % manquantes) ; VEG-01B (rien) | — | — | — | Inutilisable |
| EDA — rayonnement seul | RR-4, RR-8, RR-17 (19, 40, 58 jours) | Dose GCR/SAA quotidienne | jour | idem | Pas de télémétrie |
| PhysioNet Wearable Device Dataset v1.0.1 | https://physionet.org/content/wearable-device-dataset/1.0.1/ (DOI 10.13026/he0v-tf17) | Montre connectée, stress induit et exercice ; taille 247,4 Mo décompressé, ZIP 69,7 Mo | HR 1 Hz, TEMP 4 Hz, IBI | ODC-By 1.0 | Volontaires au sol, pas astronautes ; fichiers S02 dupliqués, f07 invalide, f14 scindé (data_constraints) |
| NASA Life Sciences Portal | https://nlsp.nasa.gov/explore | 2 676 expériences (catalogue) | — | — | NAG53952 : seulement le rapport final en accès ouvert ; pas de série individuelle |
| NASA HRP — Hazard: Distance From Earth | pages HRP | délai de communication « jusqu'à 20 minutes dans un sens » | — | — | texte, pas une donnée |

## Ce que ce catalogue ne prouve pas
- Qu'un jeu ouvert contienne PVT + sommeil + FC d'un même équipage : non trouvé.
- Que C-Sync fonctionne sur de vrais astronautes : non testé.
