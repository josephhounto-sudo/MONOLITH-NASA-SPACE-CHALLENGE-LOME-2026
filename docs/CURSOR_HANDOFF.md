# Passation à Cursor — état au samedi 14/11/2026 14:40 (Lomé = UTC)
Équipe : M1/M5 Joseph, M2 Yves, M3 Youssouf, M4 Jean. Pitch dim. 12:00 (5 min, sans questions). Soumission dim. 23:59, cible 15:00.

## 1. Ce qui existe et marche (128 tests verts)
- Moteur : `csync/rules.py` (règle v3 : seuil 1,5 écart-type vs référence individuelle jours 1–5, 2 jours de suite ; 1 dimension = WATCH, 2+ = DEGRADED ; Corps/Attention/Moral évalués, Mission/Habitat = contexte).
- `csync/capsule.py` (DecisionCapsule, 8 blocs), `gate.py` (reprise : 10 min), `quality.py` (plateaux, `flag_plateaus`), `sendqueue.py` (envoi une fois, dédup par id), `language.py`, `csync/ui/app.py` (Streamlit, en cours), `csync/config/*.json`.
- Données synthétiques `csync-synth-0.1` (graine 42, drift_amp 2.5). Mesuré sur synthétique, seuil réglé sur les mêmes scénarios : 0,7 % de faux déclenchements (300 équipages sains), 95,3 % dérive progressive, 59,3 % saut brutal.
- Données réelles NASA EDA : `data/real/raw/`, chargeur `scripts/eda_load.py`. CO2 ISS constant à 2646 ppm sur 153 h (origine inconnue : capteur ou remplissage) ; ne jamais écrire « capteur figé ».
- Pitch : `pitch/deck/` (deck.html → embed_captures.py → deck_final.html ; PDF + pptx de secours), script `SCRIPT_FR.md` v2.

## 2. Tâches restantes (ordre de priorité)
| Id | Qui | Tâche | Fait quand | Fiche |
|---|---|---|---|---|
| M3-1 | M3 | Écran Nominal : 5 dimensions, état par dimension, tout en anglais | capture propre + test d'affichage | `docs/team/tasks.json` M3-1 |
| M3-2 | M3 | Écran Action : urgence guidée (capsule → étapes) | idem | M3-2 |
| M3-3 | M3 | Écran Reprise refusée (raison lisible, forçage insuffisant sans mesure récente) | idem | M3-3 |
| M2-1/2 | M2 | Capsule finalisée + script qui rejoue l'histoire de bout en bout | `pytest` + sortie rejouable identique | M2-1, M2-2 |
| M2-3 | M2 | Contrôle qualité habitat : plateau **153 h** (pas 37 h) | test `test_raw_series_plateau_is_153h` vert | M2-3 |
| M4-1/2 | M4 | Fichiers procédure + résultat attendu écrit AVANT de lancer | `tests/` verts, mots interdits OK | M4-1, M4-2 |
| M1-3 | M1 | Une page NASA HRP citée par fiche d'aide | `docs/HELP_CARD_SOURCES.md` complet | M1-3 |
| M5-1/2 | M5 | Assemblage GO/NO-GO 13:30, 17:30, 22:30, dim. 10:30, 12:00 ; page de soumission | `docs/RELEASE_CHECKLIST.md` coché | M5-1, M5-2 |

Étapes détaillées et prompts : `docs/team/tasks.json`, `docs/team/roles/`. Suivi en direct : artefact Parcours (onglet « Maintenant »).

## 3. Décisions (voir `docs/PREMORTEM_14-11.md` §7)
Appliquées : D1 CO2 153 h, D2 « seuil réglé sur les mêmes scénarios », D3 « Données NASA » reformulé, D4 anglais du deck, D5 maquette corps = statique (non intégrée à l'app, à dire), D7 PDF/pptx de secours, D8 calendrier, D12 README.
En attente de M1 : D6 orateurs A/B (A 190 s, B 110 s ; Jean pas d'oral), D9 suppléant de soumission, D10 trace écrite de l'autorisation de démarrer, D11 langue du jury. Ne pas trancher à sa place.
`docs/OPEN_DECISIONS.md` : tableau d'origine, chiffres antérieurs au 14/11 ; fait foi : `rules.py` + PREMORTEM §7.

## 4. Pièges connus
- `scripts/check_consistency.py` plante (UnicodeDecodeError octet 0x95) : ancien bug, hors périmètre sauf demande.
- Le test des mots interdits scanne README, chaînes et procédures : relancer `pytest` après toute phrase ajoutée.
- Ne pas régénérer à la main `deck_final.html` : passer par `embed_captures.py` ; tests du deck : `pitch/tests/test_deck.js`.
- Logo : intégré (Drive, LOGO_ACTUEL_horizontal.png, fond blanc affiché en plaque sur la diapo 1).
- Un rapport d'IA externe n'est jamais une preuve : vérifier ligne par ligne contre le dépôt avant de corriger (un audit a cité des lignes de README inexistantes).

## 5. Après chaque changement important
`python scripts/build_context.py` puis commit/push : régénère `docs/CONTEXTE_IA.md` (URL brute stable lue par les IA des membres).
