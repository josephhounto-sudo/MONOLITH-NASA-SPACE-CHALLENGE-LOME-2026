<!-- Sortie de Gemini Pro (bloc v3), relue par Claude le 14/11/2026 : G2' conforme (reprend le catalogue vérifié), G3 = aucun écart réel (seulement arrondis oraux 95,3→95 et 59,3→59). NON VÉRIFIÉ par un humain. -->
# Audit G2' & G3 — Projet C-Sync (Équipe MONOLITH)

## TÂCHE G2' — Catalogue de données

| Jeu | Source (nom exact copié) | Ce qui est mesuré | Cadence | Licence | Limite pour C-Sync | Citable comme donnée ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| NASA OSDR Environmental Data App (EDA) | `https://visualization.osdr.nasa.gov/eda/ ; API https://visualization.osdr.nasa.gov/eda/api/missions/ (24 missions listées)` (Texte 1, l. 4) | Température (°C), humidité (%), CO2 (ppm) cabine ISS et sol ; rayonnement (mGy/jour) (Texte 1, l. 4) | 1, 5 ou 10 min (Texte 1, l. 4) | Mention : « Data and visualizations are courtesy of the Environmental Data App (EDA) » (Texte 1, l. 4) | EDA = capteurs de cabine pendant expériences Rodent/plantes (pas un humain suivi) (Texte 1, l. 4) | Oui, comme contexte environnemental de cabine/sol uniquement (Texte 1, l. 4) |
| EDA — missions avec télémétrie exploitable (20) | `pages /eda/dashboard_<mission>` (Texte 1, l. 5) | RR-1, 3, 5, 6, 7, 9, 10, 12, 18, 19, 20, 22, 23, 25, 28 ; APEX-03-1 et -03-2 (sans CO2) (Texte 1, l. 5) | — (Texte 1, l. 5) | Mention : « Data and visualizations are courtesy of the Environmental Data App (EDA) » (Texte 1, l. 4-5) | EDA = capteurs de cabine (pas un humain suivi) ; RR-22 : zéros de capteur et CO2 plafonné à 5000 ; APEX = culture de plantes (Texte 1, l. 4-5) | Oui, comme contexte cabine avec réserves qualité (Texte 1, l. 5) |
| EDA — télémétrie vide | `APEX-04, VEG-01A, VEG-01C (séries 100 % manquantes) ; VEG-01B (rien)` (Texte 1, l. 6) | — (Texte 1, l. 6) | — (Texte 1, l. 6) | — (Texte 1, l. 6) | EDA = capteurs de cabine (pas un humain suivi) ; inutilisable (séries 100 % manquantes ou rien) (Texte 1, l. 4, 6) | Non (inutilisable) (Texte 1, l. 6) |
| EDA — rayonnement seul | `RR-4, RR-8, RR-17 (19, 40, 58 jours)` (Texte 1, l. 7) | Dose GCR/SAA quotidienne (Texte 1, l. 7) | jour (Texte 1, l. 7) | Mention : « Data and visualizations are courtesy of the Environmental Data App (EDA) » (Texte 1, l. 4, 7) | EDA = capteurs de cabine (pas un humain suivi) ; pas de télémétrie (Texte 1, l. 4, 7) | Oui, pour la dose quotidienne GCR/SAA uniquement (Texte 1, l. 7) |
| PhysioNet Wearable Device Dataset v1.0.1 | `https://physionet.org/content/wearable-device-dataset/1.0.1/ (DOI 10.13026/he0v-tf17)` (Texte 1, l. 8) | Montre connectée, stress induit et exercice ; taille 247,4 Mo décompressé, ZIP 69,7 Mo (Texte 1, l. 8) | HR 1 Hz, TEMP 4 Hz, IBI (Texte 1, l. 8) | ODC-By 1.0 (Texte 1, l. 8) | PhysioNet = volontaires au sol (pas astronautes) ; fichiers S02 dupliqués, f07 invalide, f14 scindé (`data_constraints`) (Texte 1, l. 8) | Oui, comme signaux physiologiques de volontaires au sol (Texte 1, l. 8) |
| NASA Life Sciences Portal | `https://nlsp.nasa.gov/explore` (Texte 1, l. 9) | 2 676 expériences (catalogue) (Texte 1, l. 9) | — (Texte 1, l. 9) | — (Texte 1, l. 9) | NAG53952 : seulement le rapport final en accès ouvert ; pas de série individuelle (Texte 1, l. 9) | Non (catalogue et rapport final sans série individuelle) (Texte 1, l. 9) |
| NASA HRP — Hazard: Distance From Earth | `pages HRP` (Texte 1, l. 10) | délai de communication « jusqu'à 20 minutes dans un sens » (Texte 1, l. 10) | — (Texte 1, l. 10) | — (Texte 1, l. 10) | texte, pas une donnée (Texte 1, l. 10) | Non (texte de référence, pas une donnée) (Texte 1, l. 10) |

**Ce que ce catalogue ne prouve pas :**
- Qu'un jeu ouvert contienne PVT + sommeil + FC d'un même équipage : non trouvé (Texte 1, l. 12).
- Que C-Sync fonctionne sur de vrais astronautes : non testé (Texte 1, l. 13).
- Qu'une série individuelle humaine en vol soit disponible dans les jeux ouverts listés : EDA porte uniquement sur des capteurs de cabine/expériences Rodent/plantes, PhysioNet sur des volontaires au sol, NLSP ne fournit pas de série individuelle et HRP est du texte (Texte 1, l. 4-10).

---

## TÂCHE G3 — Audit de cohérence des chiffres

* **Écarts numériques relevés (arrondis oraux dans le script par rapport aux valeurs décimales du dossier méthodologique) :**
  * `95,3 % vs 95 %` | `METHODES_NASA_DOSSIER.md` section 7.3 (tableau, ligne Règle `d ≥ 1,5` : `95,3 %`), section 7.6 (`95,3 %`), section 7.10 (`détection graduelle 95,3 %`) | `SCRIPT_FR.md` Diapo 6 (`Sur des dérives progressives simulées, quatre-vingt-quinze pour cent sont repérées` = `95 %`, arrondi oral à l'entier)
  * `59,3 % vs 59 %` | `METHODES_NASA_DOSSIER.md` section 7.3 (tableau, ligne Règle `d ≥ 1,5` : `59,3 %`), section 7.10 (`brutale 59,3 %`), section 7.11 (`59,3 % (règle 1,5)`) | `SCRIPT_FR.md` Diapo 6 (`Mais sur un saut brutal, seulement cinquante-neuf pour cent` = `59 %`, arrondi oral à l'entier)

* **Aucun autre écart trouvé sur les nombres communs aux deux textes :**
  * `300` équipages témoins / simulés en bonne santé : `300 équipages témoins` (`METHODES_NASA_DOSSIER.md`, sections 7.2 et 7.6) vs `trois cents équipages simulés en bonne santé` (`SCRIPT_FR.md`, Diapo 6).
  * `0,7 %` de fausses alertes (équipages témoins déclenchant à tort) : `0,7 %` (`METHODES_NASA_DOSSIER.md`, sections 7.3, 7.6, 7.10, 7.11) vs `zéro virgule sept pour cent` (`SCRIPT_FR.md`, Diapo 6).
  * `Jour 7` (déclenchement dégradé sur le scénario « histoire ») : `Attention DEGRADED au jour 7` (`METHODES_NASA_DOSSIER.md`, section 7.10) vs `Au jour sept de notre histoire simulée... La carte Attention passe en dégradée` (`SCRIPT_FR.md`, Diapo 3).
  * *Note sur les chiffres propres à un seul texte (non comparables entre A et B)* : le délai de communication de `20 minutes` (`SCRIPT_FR.md`, Diapos 1 et 2) concorde avec `TEXTE 1` (`pages HRP`, l. 10) ; le chiffre de `trente-sept heures` pour le capteur de CO2 figé (`SCRIPT_FR.md`, Diapo 6) n'apparaît pas dans `METHODES_NASA_DOSSIER.md` section 7 (`NON VÉRIFIÉ` dans Texte 2).