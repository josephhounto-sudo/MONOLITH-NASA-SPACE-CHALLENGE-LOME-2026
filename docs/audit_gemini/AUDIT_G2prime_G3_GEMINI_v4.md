# Gemini v4 — G2' (catalogue) et G3 (cohérence des chiffres) — STATUT : revue par Claude, NON validée par un humain
Date/heure : sam. 14/11/2026 ~14:10 UTC.
**Verdict de Claude :**
- G2' : le contenu reprend le catalogue vérifié de Claude ; **toutes les « citations de ligne » indiquent « ligne 4 » — fausses** (les lignes du tableau sont distinctes) ; liens Markdown cassés dans des blocs de code. **Ne pas utiliser ce tableau** ; la référence reste `NASA_DATA_CATALOG_VERIFIE.md`.
- G3 : « 95,3 % vs 95 % » et « 59,3 % vs 59 % » sont des arrondis oraux, pas des écarts. Aucun vrai écart de chiffre trouvé entre section 7 et script : constat **plausible, recoupé par Claude** (630 mots = somme de la table ; 0,7 %, 300, jour 7 concordent). Gemini n'a pas vu (et ne pouvait pas voir) le vrai problème : « 37 h » de CO2 (PREMORTEM R1).
- Respect des règles dures : pas d'URL inventée (les URL viennent du texte collé), pas de nom propre, < 1 200 mots : OK. Citations de ligne : NON.
Texte ci-dessous = sortie brute de Gemini, non modifiée.

---
## TÂCHE G2' — Catalogue de données

| Jeu | Source (nom exact copié) | Ce qui est mesuré | Cadence | Licence | Limite pour C-Sync | Citable comme donnée ? |
| --- | --- | --- | --- | --- | --- | --- |
| NASA OSDR Environmental Data App (EDA) | `[https://visualization.osdr.nasa.gov/eda/](https://visualization.osdr.nasa.gov/eda/) ; API [https://visualization.osdr.nasa.gov/eda/api/missions/](https://visualization.osdr.nasa.gov/eda/api/missions/) (24 missions listées)` (TEXTE 1, ligne 4) | Température (°C), humidité (%), CO2 (ppm) cabine ISS et sol ; rayonnement (mGy/jour) (TEXTE 1, ligne 4) | 1, 5 ou 10 min (TEXTE 1, ligne 4) | Mention : « Data and visualizations are courtesy of the Environmental Data App (EDA) » (TEXTE 1, ligne 4) | EDA = capteurs de cabine pendant expériences Rodent/plantes (pas un humain suivi) (TEXTE 1, ligne 4) | Oui, comme contexte environnemental de cabine/sol uniquement (TEXTE 1, ligne 4) |
| EDA — missions avec télémétrie exploitable (20) | `pages /eda/dashboard_<mission>` (TEXTE 1, ligne 4) | RR-1, 3, 5, 6, 7, 9, 10, 12, 18, 19, 20, 22, 23, 25, 28 ; APEX-03-1 et -03-2 (sans CO2) (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | Mention : « Data and visualizations are courtesy of the Environmental Data App (EDA) » (TEXTE 1, ligne 4) | EDA = capteurs de cabine (pas un humain suivi) ; RR-22 : zéros de capteur et CO2 plafonné à 5000 ; APEX = culture de plantes (TEXTE 1, ligne 4) | Oui, comme contexte cabine avec réserves qualité (TEXTE 1, ligne 4) |
| EDA — télémétrie vide | `APEX-04, VEG-01A, VEG-01C (séries 100 % manquantes) ; VEG-01B (rien)` (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | EDA = capteurs de cabine (pas un humain suivi) ; inutilisable (séries 100 % manquantes ou rien) (TEXTE 1, ligne 4) | Non (inutilisable) (TEXTE 1, ligne 4) |
| EDA — rayonnement seul | `RR-4, RR-8, RR-17 (19, 40, 58 jours)` (TEXTE 1, ligne 4) | Dose GCR/SAA quotidienne (TEXTE 1, ligne 4) | jour (TEXTE 1, ligne 4) | Mention : « Data and visualizations are courtesy of the Environmental Data App (EDA) » (TEXTE 1, ligne 4) | EDA = capteurs de cabine (pas un humain suivi) ; pas de télémétrie (TEXTE 1, ligne 4) | Oui, pour la dose quotidienne GCR/SAA uniquement (TEXTE 1, ligne 4) |
| PhysioNet Wearable Device Dataset v1.0.1 | `[https://physionet.org/content/wearable-device-dataset/1.0.1/](https://physionet.org/content/wearable-device-dataset/1.0.1/) (DOI 10.13026/he0v-tf17)` (TEXTE 1, ligne 4) | Montre connectée, stress induit et exercice ; taille 247,4 Mo décompressé, ZIP 69,7 Mo (TEXTE 1, ligne 4) | HR 1 Hz, TEMP 4 Hz, IBI (TEXTE 1, ligne 4) | ODC-By 1.0 (TEXTE 1, ligne 4) | PhysioNet = volontaires au sol (pas astronautes) ; fichiers S02 dupliqués, f07 invalide, f14 scindé (`data_constraints`) (TEXTE 1, ligne 4) | Oui, comme signaux physiologiques de volontaires au sol (TEXTE 1, ligne 4) |
| NASA Life Sciences Portal | `[https://nlsp.nasa.gov/explore](https://nlsp.nasa.gov/explore)` (TEXTE 1, ligne 4) | 2 676 expériences (catalogue) (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | NAG53952 : seulement le rapport final en accès ouvert ; pas de série individuelle (TEXTE 1, ligne 4) | Non (catalogue et rapport final sans série individuelle) (TEXTE 1, ligne 4) |
| NASA HRP — Hazard: Distance From Earth | `pages HRP` (TEXTE 1, ligne 4) | délai de communication « jusqu'à 20 minutes dans un sens » (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | — (TEXTE 1, ligne 4) | texte, pas une donnée (TEXTE 1, ligne 4) | Non (texte de référence, pas une donnée) (TEXTE 1, ligne 4) |

**Ce que ce catalogue ne prouve pas :**

* Qu'un jeu ouvert contienne PVT + sommeil + FC d'un même équipage : non trouvé (TEXTE 1, ligne 5).
* Que C-Sync fonctionne sur de vrais astronautes : non testé (TEXTE 1, ligne 6).
* Qu'une série individuelle humaine en vol soit disponible dans les jeux ouverts listés : EDA mesure des capteurs de cabine (expériences Rodent/plantes), PhysioNet porte sur des volontaires au sol, le portail NLSP ne fournit pas de série individuelle et HRP est un document texte (TEXTE 1, ligne 4).

---

## TÂCHE G3 — Audit de cohérence des chiffres

* `95,3 % vs 95 %` | `METHODES_NASA_DOSSIER.md` section 7.3 (tableau, ligne Règle `d ≥ 1,5` : `95,3 %`), section 7.6 (`95,3 %`), section 7.10 (`détection graduelle 95,3 %`) | `SCRIPT_FR.md` Diapo 6 (`Sur des dérives progressives simulées, quatre-vingt-quinze pour cent sont repérées` = `95 %`)
* `59,3 % vs 59 %` | `METHODES_NASA_DOSSIER.md` section 7.3 (tableau, ligne Règle `d ≥ 1,5` : `59,3 %`), section 7.10 (`brutale 59,3 %`), section 7.11 (`59,3 % (règle 1,5)`) | `SCRIPT_FR.md` Diapo 6 (`Mais sur un saut brutal, seulement cinquante-neuf pour cent` = `59 %`)

**Aucun autre écart trouvé sur :**

* `300` équipages témoins / simulés en bonne santé : `300 équipages témoins` (`METHODES_NASA_DOSSIER.md`, sections 7.2 et 7.6) vs `trois cents équipages simulés en bonne santé` (`SCRIPT_FR.md`, Diapo 6).
* `0,7 %` de fausses alertes sur équipages témoins : `0,7 %` (`METHODES_NASA_DOSSIER.md`, sections 7.3, 7.6, 7.10 et 7.11) vs `zéro virgule sept pour cent` (`SCRIPT_FR.md`, Diapo 6).
* `Jour 7` (déclenchement dégradé sur le scénario « histoire ») : `Attention DEGRADED au jour 7` (`METHODES_NASA_DOSSIER.md`, section 7.10) vs `Au jour sept de notre histoire simulée... La carte Attention passe en dégradée` (`SCRIPT_FR.md`, Diapo 3).
* *Chiffres non comparables entre les deux textes* : le délai de communication de `20 minutes` (`SCRIPT_FR.md`, Diapos 1 et 2) figure dans `TEXTE 1` (ligne 4, `pages HRP`) mais pas dans `METHODES_NASA_DOSSIER.md` section 7 (`NON VÉRIFIÉ` dans TEXTE 2) ; le capteur de CO2 figé pendant `trente-sept heures` (`SCRIPT_FR.md`, Diapo 6) n'apparaît pas dans `METHODES_NASA_DOSSIER.md` section 7 (`NON VÉRIFIÉ` dans TEXTE 2).