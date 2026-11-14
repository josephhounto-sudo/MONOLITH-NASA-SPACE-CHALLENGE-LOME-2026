Version 1 · 14/11/2026 ~07h10 Lomé · Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ · Remplace : création initiale

## Avertissement d'accès web (Règles 2 et G2)

- **Accès web direct indisponible dans cet environnement :** aucune page externe (NASA OSDR, NASA Task Book, NASA HRP, PhysioNet) n'a pu être ouverte ni consultée en ligne lors de la rédaction de ce fichier.
- **Application stricte de la règle anti-fabrication :** aucun identifiant d'étude externe non lu sur une page ouverte (`OSD-xxx`, `LSDA`, `NSBRI`) ni aucune URL non ouverte n'est inscrit dans ce document. Toute information non présente directement dans les fichiers du dépôt (`commit dc61786`) est marquée **`NON VÉRIFIÉ`**.

---

## 1. Sources réelles déjà référencées dans le dépôt (`commit dc61786`)

Les deux entrées ci-dessous proviennent uniquement de l'inspection directe de `synthetic/generator.py` (lignes 4–6, 37, 94–101) et de la note de contexte du projet. Leurs pages sources web n'ont pas été ouvertes ici.

### Entrée 1 — Télémétrie environnementale cabine ISS (déjà intégrée dans `generator.py`)
- **Titre exact :** `NON VÉRIFIÉ` (désigné dans `generator.py` sous `NASA OSDR EDA RR-1 (ISS cabin CO2 / temperature / humidity / radiation)`).
- **Identifiant tel qu'affiché dans le code :** `S03-EDA-RR1` / `NASA OSDR EDA RR-1` (`NON VÉRIFIÉ` sur le portail OSDR en ligne).
- **URL ouverte :** `NON VÉRIFIÉ` (aucune page ouverte).
- **Date d'accès :** `NON VÉRIFIÉ`.
- **Contenu du jeu (variables lues dans `generator.py` L.96–101) :** `co2_ppm` (mappé vers `HA01`), `temp_c` (mappé vers `HA02`), `rh_pct` (mappé vers `HA03`), `total_mgy_day` (mappé vers `HA05`), échantillonnage horaire (`story_day`, `hour`) pour les trois premiers et quotidien pour le rayonnement.
- **Nombre de sujets :** Sans objet (télémétrie d'habitat cabine, pas de sujet humain individuel).
- **Licence / accès :** `NON VÉRIFIÉ` (marqué `origin="REAL_OPEN"` dans `generator.py`, licence exacte non lue sur le portail).
- **Limites :** Mesures environnementales de cabine uniquement ; aucune donnée physiologique humaine (sommeil, fréquence cardiaque, tension) ni cognitive (PVT).
- **Verdict — utilisable pour une référence personnelle :** **non** (utile uniquement pour la dimension `Habitat`, pas pour étalonner une référence physiologique ou cognitive individuelle).

### Entrée 2 — Jeu portable poignet (utilisé comme modèle de bruit dans `generator.py`)
- **Titre exact :** `NON VÉRIFIÉ` (désigné dans le dossier sous `PhysioNet (Wearable Device Dataset)` et dans `generator.py` L.6, 37 sous `PhysioNet S10`).
- **Identifiant tel qu'affiché dans le code :** `PhysioNet S10` (`NON VÉRIFIÉ` sur le portail PhysioNet en ligne).
- **URL ouverte :** `NON VÉRIFIÉ` (aucune page ouverte).
- **Date d'accès :** `NON VÉRIFIÉ`.
- **Contenu du jeu (éléments cités dans `generator.py` L.6, 37, 89) :** Fréquence cardiaque au poignet (bruit intra-fenêtre médian cité à `5,1 bpm`, couverture moyenne citée à `~55 %`), niveau déclaré `Baseline` (`stress` médian cité à `3` sur `n=36`).
- **Nombre de sujets :** `n=36` cité en commentaire de `generator.py` L.37 (`NON VÉRIFIÉ` sur la page source).
- **Licence / accès :** `NON VÉRIFIÉ`.
- **Limites :** Cohorte terrestre en protocole de laboratoire/ambulatoire (non spatiale) ; utilisé dans `generator.py` uniquement pour calibrer le bruit du capteur poignet et le niveau initial, sans vérification directe de la structure longitudinale multi-jours ici.
- **Verdict — utilisable pour une référence personnelle :** **à vérifier** (ouvrir la fiche PhysioNet officielle pour contrôler la durée longitudinale par sujet, la disponibilité sommeil/PVT/tension et les conditions de licence).

---

## 2. Jeux de données NASA OSDR / HRP candidates (sommeil, FC, tension, PVT)

- **Catalogue de nouvelles études OSDR / HRP :** **`NON VÉRIFIÉ`** (accès web requis pour interroger le portail NASA Open Science Data Repository et ouvrir chaque fiche d'étude avant inscription).
- **Page des défis méthodologiques Artemis II de la NASA HRP :** **`NON VÉRIFIÉ`** (page non ouverte dans cet environnement). Seule la mention interne du dossier (`section 12`) est disponible : la NASA y expose le problème des petits effectifs, des données longitudinales et des valeurs manquantes, et a récompensé des propositions bayésiennes individuelles de concours (non opérationnelles). La liste exacte des jeux de données fournis aux participants du défi Artemis II reste **`NON VÉRIFIÉ`** tant que la page officielle n'est pas ouverte.

---

## 3. Protocole de vérification en ligne à exécuter par M1–M5 (sans invention)

Pour compléter ce catalogue dès qu'un accès web est disponible, chaque entrée ajoutée devra respecter le gabarit strict ci-dessous après ouverture effective de sa page :

1. **Requête sur le portail NASA OSDR** (`osdr.nasa.gov`, non ouvert ici) filtrée sur les études humaines (vol spatial, analogues d'isolement type HERA/bed-rest) comportant des séries temporelles longitudinales (`sleep`, `heart rate`, `blood pressure`, `PVT` / `Psychomotor Vigilance Test`).
2. **Ouverture de la page des défis méthodologiques NASA HRP / Artemis II** pour relever les identifiants exacts des jeux mis à disposition, leur format et leurs restrictions d'accès.
3. **Fiche de contrôle obligatoire par jeu candidat :**
   - Titre exact copié depuis la page ouverte
   - Identifiant exact tel qu'affiché
   - URL complète effectivement ouverte
   - Date d'accès (AAAA-MM-JJ)
   - Variables longitudinales présentes (sommeil, FC, tension, PVT) et fréquence d'échantillonnage
   - Nombre de sujets (`N`) et durée de suivi en jours
   - Licence et conditions d'accès (accès ouvert immédiat vs demande d'accès contrôlé)
   - Limites (ex. données omiques uniquement, absence de série temporelle individuelle, données agrégées)
   - Verdict : `oui` / `non` / `à vérifier`
