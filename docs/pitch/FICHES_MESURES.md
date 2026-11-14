# FICHIER: FICHES_MESURES.md
Date/heure : sam. 14/11/2026 08:45 Lomé (UTC) · Commit de référence : dc61786 · Version v2 (remplace la v1 de la phase 2)
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

## Sources lues pour cette version (zip rev4)
- `data/procedures/PROC-EMERGENCY-01.json` et `PROC-FATIGUE-01.json` : textes « how_to », champs « why » et « hrp_source_url ».
- `synthetic/generator.py` : unités, heure de mesure, origine.
- `csync/rules.py` : règle v3, seuil 1,5, 2 jours, planchers.
- `csync/gate.py`, `csync/capsule.py`, `contracts/decision.schema.json`, `docs/OPEN_DECISIONS.md`.
- `docs/HELP_CARD_SOURCES.md`, `SOURCES.md`, `csync/config/strings_en.json`.

## Règles
- **« SOURCE À AJOUTER »** : aucune source NASA lue n'existe dans le dépôt pour cette rubrique. Dans le dépôt, tous les champs « why » valent `TODO_M1`. Rien n'est inventé.
- **« Comment la prendre »** reprend le texte du dépôt. C'est un texte de C-Sync, pas une citation de la NASA.
- **« Quand alerter »** décrit uniquement la logique codée de C-Sync :
  - écart à la référence personnelle (jours 1–5) d'au moins 1,5 écart-type, 2 jours de suite → indicateur signalé ;
  - 1 indicateur signalé → WATCH ; 2 ou plus → DEGRADED ;
  - 2 dimensions hors NORMAL → procédure IMPORTANT (officier médical de bord) ;
  - symptôme déclaré → procédure CRITICAL (chirurgien de vol, d'après `contracts/decision.schema.json`).

  **Aucun seuil clinique.**
- **« Ce que nous ne faisons pas »**, pour toutes les mesures : aucun seuil clinique, aucun conseil de traitement ni de médicament, aucune étiquette posée sur la personne. Phrase fixe affichée : « Follow the onboard medical checklist and the crew medical officer. »
- Toutes les valeurs de la démo sont SYNTHÉTIQUES (générateur csync-synth-0.1, seed 42, drift_amp 2.5), sauf Habitat.

---
## BODY (corps)
| Id | Mesure (unité) | Comment la prendre (texte du dépôt) | Pourquoi elle compte | Quand alerter (logique C-Sync) | Codé dans la démo ? |
|---|---|---|---|---|---|
| PH01 | Fréquence cardiaque (bpm) | Au repos : moyenne du capteur au poignet entre 06:00 et 07:00 (au moins 3 points valides, sinon donnée manquante). En procédure : « Use the onboard device for heart rate and confirm the value shown on screen. » | SOURCE À AJOUTER (`why` = TODO_M1, `hrp_source_url` = TODO_M1) | Règle de dérive (plancher d'écart-type 3 bpm). **Porte de reprise : doit dater de moins de 10 min** (démo, jour 10 : 14 min → reprise refusée). | Oui (règle + porte + urgence) |
| PH09 | Sommeil déclaré (h) | « Enter the number of hours slept, as estimated by the crew member. » (PROC-FATIGUE-01, étape 2) | Page NASA citée par le dépôt : https://www.nasa.gov/hrp/risks/ (risque « Inadequate Sleep and Irregular Schedules », `docs/HELP_CARD_SOURCES.md`). **Phrase « why » : SOURCE À AJOUTER** | Règle de dérive ; une baisse est défavorable (plancher 0,5 h) | Oui (règle) |
| PH10 | Tension artérielle (mmHg, SYS et DIA) | « Use the onboard device for blood pressure and confirm both values (SYS and DIA). » | SOURCE À AJOUTER | Aucune alerte automatique : affichée et jointe au compte rendu (choix par défaut de la décision ouverte n°5, à confirmer par M1) | Enregistrée (urgence + routine), hors règle |
| PH11 | Température corporelle (°C) | « Use the onboard device for body temperature and confirm the value shown on screen. » | SOURCE À AJOUTER | Aucune alerte automatique : affichée et jointe au compte rendu (même décision n°5) | Enregistrée (urgence + routine), hors règle |
| PH12 | Glycémie (mg/dL) | « Use the onboard device for blood glucose and confirm the value shown on screen. » | **« no NASA in-flight reference »** (étiquette du dépôt) | Aucune alerte, aucun seuil | Enregistrée (urgence seulement) |
| SY01 | Symptôme déclaré + zone du corps | L'astronaute le déclare et choisit la zone du corps (PROC-EMERGENCY-01, étape 2) | SOURCE À AJOUTER (`docs/HELP_CARD_SOURCES.md`, ligne « Chest pain / symptoms checklist » vide) | Règle d'événement : OPEN_PROCEDURE, **CRITICAL**, immédiatement ; compte rendu en file d'envoi, livré une fois | Oui. **Le choix de la zone n'est pas codé dans l'interface** (la silhouette est une maquette) |

## ATTENTION
| Id | Mesure (unité) | Comment la prendre | Pourquoi elle compte | Quand alerter | Codé ? |
|---|---|---|---|---|---|
| CO01 | Temps de réaction (ms) | « Run the 3-minute reaction-time test on the onboard tablet. » (PROC-FATIGUE-01) ; test de 3 min chaque matin à 08:00 (générateur) | SOURCE À AJOUTER pour la NASA. Référence de méthode dans `SOURCES.md` : Basner et al. 2011, PVT-B, *Acta Astronautica* (article scientifique, pas une page NASA) | Règle de dérive (une hausse est défavorable). Aussi prérequis de la procédure d'urgence : moins de 10 min | Oui |
| CO02 | Erreurs d'attention (nombre de réponses ≥ 355 ms) | Même test de 3 min | Même cas que CO01 | Règle de dérive (une hausse est défavorable, plancher 1) | Oui |

## MORALE
| Id | Mesure (unité) | Comment la prendre | Pourquoi elle compte | Quand alerter | Codé ? |
|---|---|---|---|---|---|
| PS01 | **Somnolence**, échelle KSS 1–9 (attention : c'est la somnolence, pas la durée du sommeil, qui est PH09) | Check-in au clavier à 07:30 (générateur) ; pas de texte « how_to » dans les procédures → **SOURCE À AJOUTER** | SOURCE À AJOUTER | Règle de dérive (une hausse est défavorable, plancher 1) | Oui |
| PS02 | Stress (0–10) | Check-in au clavier | SOURCE À AJOUTER | Règle de dérive (hausse défavorable) | Oui |
| PS03 | Humeur (1–5, moyenne de 2 réponses) | Check-in au clavier | SOURCE À AJOUTER | Règle de dérive (baisse défavorable ; sens proposé, décision n°5) | Oui |
| PS04 | Charge de travail (0–10) | Check-in au clavier | SOURCE À AJOUTER | Règle de dérive (hausse défavorable) | Oui |

## MISSION — HORS PÉRIMÈTRE DÉMO
MI03 (indicateur opérationnel 0–10) et MI05 (délai sol, paramètre de 20 min) existent dans le générateur, mais la dimension est **« Context only — not evaluated »** (carte grise). Elle ne déclenche aucun état dans la démo.

## HABITAT — données réelles, contexte seulement
| Id | Mesure (unité) | Origine | Rôle dans C-Sync |
|---|---|---|---|
| HA01 | CO2 cabine (ppm) | **Réelle** : NASA OSDR Environmental Data App, mission RR-1 (ISS, 26/09–05/10/2014), moyennes horaires (`data/real/`) | Contrôle qualité : une valeur figée sur 6 points ou plus est marquée ARTIFACT, jamais normale. Résultat exécuté : une série figée de 37 h à 2 646 ppm (`tests/test_quality.py`) |
| HA02 | Température cabine (°C) | Réelle, idem | Contexte, non évalué |
| HA03 | Humidité relative (%) | Réelle, idem | Contexte, non évalué |
| HA05 | Rayonnement (mGy/jour) | Réelle, idem | Contexte, non évalué |

Limite (`data/real/PROVENANCE_fr.md`) : ce sont des capteurs de cabine de l'ISS pendant des missions Rodent Research, pas un équipage suivi individuellement. Dans l'histoire de démo, `scripts/run_story.py` ne charge pas ces données : la carte Habitat reste grise.
Mention obligatoire : « Data and visualizations are courtesy of the Environmental Data App (EDA) », numéro de version `TODO_M1`.

## Non mesuré (affiché UNKNOWN, jamais NORMAL)
Os, système immunitaire, dose de rayonnement personnelle, abdomen, échographie.
