# Rapport de recette M4 (données et tests)
Généré le 14/11/2026 16:57 UTC (= heure de Lomé) par `python scripts/recette_m4.py`, version `f725d0c-dirty`. Données de démonstration **SYNTHÉTIQUES** (générateur csync-synth-0.1, graine 42). Aucun seuil clinique.
Attendus : `data/scenarios/*.json`, écrits **avant** toute exécution et jamais modifiés après coup (écarts : `docs/TEST_DEVIATIONS.md`). Obtenus : paramètres de `scripts/run_story.py`, donc ce que montre l'écran.
Gravité : **BLOQUANT** = un acte de l'histoire ou un garde-fou tombe · **MAJEUR** = décision ou écran annoncé faux · **MINEUR** = écart sans effet sur l'écran · **INFO** = à savoir pour le pitch.

## Bilan
- Contrôles : 123 · écarts : 4 (BLOQUANT 0, MAJEUR 1, MINEUR 2, INFO 1).
- **MINEUR** · histoire jour 1-10 · jeu crédible : MISSING et ARTIFACT présents : attendu oui, obtenu MISSING 0, ARTIFACT 0.
- **MINEUR** · temoin jour 1-10 · jeu crédible : MISSING et ARTIFACT présents : attendu oui, obtenu MISSING 0, ARTIFACT 0.
- **MAJEUR** · histoire jour 1-10 · Habitat : vraies données NASA EDA RR-1 (STORY.md) : attendu état calculé, obtenu états affichés : UNKNOWN.
- **INFO** · histoire jour 6-9 · somnolence en hausse visible (STORY.md) : attendu Morale hors NORMAL un jour au moins, obtenu Morale : NORMAL.

## Actes 2 et 3, habitat
| Scénario | Jour | Contrôle | Attendu | Obtenu | Écart | Gravité |
|---|---|---|---|---|---|---|
| histoire | 9 | urgence guidée (T4) | jour 9 14:10 PROC-EMERGENCY-01 CRITICAL | jour 9 14:10 PROC-EMERGENCY-01 CRITICAL | non | — |
| histoire | 9 | compte rendu : remises au sol (T5) | 1 | 1 | non | — |
| histoire | 9 | compte rendu : réception affichée | 19:20 | 19:20 | non | — |
| histoire | 9 | compte rendu : réception gardée par le sol | 19:20 | 19:20 | non | — |
| histoire | 10 | reprise refusée (G3) | REFUSE_RESUME · PH01 is stale (14 min > 10 min) | REFUSE_RESUME · G3: PH01 is stale (14 min > 10 min) | non | — |
| histoire | 10 | même avec forçage (G6) | REFUSE_RESUME | G3: PH01 is stale (14 min > 10 min); G6: Commander override logged; it never authorises a resume on its own | non | — |
| histoire | 1-10 | Habitat : vraies données NASA EDA RR-1 (STORY.md) | état calculé | états affichés : UNKNOWN | **oui** | MAJEUR |
| histoire | 6-9 | somnolence en hausse visible (STORY.md) | Morale hors NORMAL un jour au moins | Morale : NORMAL | **oui** | INFO |

## États et décisions jour par jour
| Scénario | Jour | Contrôle | Attendu | Obtenu | Écart | Gravité |
|---|---|---|---|---|---|---|
| histoire | 1 | Body | UNKNOWN | UNKNOWN | non | — |
| histoire | 1 | Attention | UNKNOWN | UNKNOWN | non | — |
| histoire | 1 | Morale | UNKNOWN | UNKNOWN | non | — |
| histoire | 1 | decision | CONTINUE | CONTINUE | non | — |
| histoire | 2 | Body | UNKNOWN | UNKNOWN | non | — |
| histoire | 2 | Attention | UNKNOWN | UNKNOWN | non | — |
| histoire | 2 | Morale | UNKNOWN | UNKNOWN | non | — |
| histoire | 2 | decision | CONTINUE | CONTINUE | non | — |
| histoire | 3 | Body | UNKNOWN | UNKNOWN | non | — |
| histoire | 3 | Attention | UNKNOWN | UNKNOWN | non | — |
| histoire | 3 | Morale | UNKNOWN | UNKNOWN | non | — |
| histoire | 3 | decision | CONTINUE | CONTINUE | non | — |
| histoire | 4 | Body | UNKNOWN | UNKNOWN | non | — |
| histoire | 4 | Attention | UNKNOWN | UNKNOWN | non | — |
| histoire | 4 | Morale | UNKNOWN | UNKNOWN | non | — |
| histoire | 4 | decision | CONTINUE | CONTINUE | non | — |
| histoire | 5 | Body | UNKNOWN | UNKNOWN | non | — |
| histoire | 5 | Attention | UNKNOWN | UNKNOWN | non | — |
| histoire | 5 | Morale | UNKNOWN | UNKNOWN | non | — |
| histoire | 5 | decision | CONTINUE | CONTINUE | non | — |
| histoire | 6 | decision | CONTINUE | CONTINUE | non | — |
| histoire | 7 | Attention | DEGRADED | DEGRADED | non | — |
| histoire | 7 | decision | OPEN_PROCEDURE | OPEN_PROCEDURE | non | — |
| histoire | 8 | decision | OPEN_PROCEDURE | OPEN_PROCEDURE | non | — |
| histoire | 9 | decision | OPEN_PROCEDURE | OPEN_PROCEDURE | non | — |
| histoire | 10 | decision | CONTINUE | CONTINUE | non | — |
| histoire | 1-10 | jours de procédure | 3 | 3 | non | — |
| histoire | 1-10 | T1 donnée manquante jamais NORMAL | 0 cas | 0 cas | non | — |
| histoire | 1-10 | jeu crédible : MISSING et ARTIFACT présents | oui | MISSING 0, ARTIFACT 0 | **oui** | MINEUR |
| temoin | 1 | Body | UNKNOWN | UNKNOWN | non | — |
| temoin | 1 | Attention | UNKNOWN | UNKNOWN | non | — |
| temoin | 1 | Morale | UNKNOWN | UNKNOWN | non | — |
| temoin | 1 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 2 | Body | UNKNOWN | UNKNOWN | non | — |
| temoin | 2 | Attention | UNKNOWN | UNKNOWN | non | — |
| temoin | 2 | Morale | UNKNOWN | UNKNOWN | non | — |
| temoin | 2 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 3 | Body | UNKNOWN | UNKNOWN | non | — |
| temoin | 3 | Attention | UNKNOWN | UNKNOWN | non | — |
| temoin | 3 | Morale | UNKNOWN | UNKNOWN | non | — |
| temoin | 3 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 4 | Body | UNKNOWN | UNKNOWN | non | — |
| temoin | 4 | Attention | UNKNOWN | UNKNOWN | non | — |
| temoin | 4 | Morale | UNKNOWN | UNKNOWN | non | — |
| temoin | 4 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 5 | Body | UNKNOWN | UNKNOWN | non | — |
| temoin | 5 | Attention | UNKNOWN | UNKNOWN | non | — |
| temoin | 5 | Morale | UNKNOWN | UNKNOWN | non | — |
| temoin | 5 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 6 | Body | NORMAL | NORMAL | non | — |
| temoin | 6 | Attention | NORMAL | NORMAL | non | — |
| temoin | 6 | Morale | NORMAL | NORMAL | non | — |
| temoin | 6 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 7 | Body | NORMAL | NORMAL | non | — |
| temoin | 7 | Attention | NORMAL | NORMAL | non | — |
| temoin | 7 | Morale | NORMAL | NORMAL | non | — |
| temoin | 7 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 8 | Body | NORMAL | NORMAL | non | — |
| temoin | 8 | Attention | NORMAL | NORMAL | non | — |
| temoin | 8 | Morale | NORMAL | NORMAL | non | — |
| temoin | 8 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 9 | Body | NORMAL | NORMAL | non | — |
| temoin | 9 | Attention | NORMAL | NORMAL | non | — |
| temoin | 9 | Morale | NORMAL | NORMAL | non | — |
| temoin | 9 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 10 | Body | NORMAL | NORMAL | non | — |
| temoin | 10 | Attention | NORMAL | NORMAL | non | — |
| temoin | 10 | Morale | NORMAL | NORMAL | non | — |
| temoin | 10 | decision | CONTINUE | CONTINUE | non | — |
| temoin | 1-10 | jours de procédure | 0 | 0 | non | — |
| temoin | 1-10 | T1 donnée manquante jamais NORMAL | 0 cas | 0 cas | non | — |
| temoin | 1-10 | jeu crédible : MISSING et ARTIFACT présents | oui | MISSING 0, ARTIFACT 0 | **oui** | MINEUR |
| capteur | 1 | Body | UNKNOWN | UNKNOWN | non | — |
| capteur | 1 | Attention | UNKNOWN | UNKNOWN | non | — |
| capteur | 1 | Morale | UNKNOWN | UNKNOWN | non | — |
| capteur | 1 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 2 | Body | UNKNOWN | UNKNOWN | non | — |
| capteur | 2 | Attention | UNKNOWN | UNKNOWN | non | — |
| capteur | 2 | Morale | UNKNOWN | UNKNOWN | non | — |
| capteur | 2 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 3 | Body | UNKNOWN | UNKNOWN | non | — |
| capteur | 3 | Attention | UNKNOWN | UNKNOWN | non | — |
| capteur | 3 | Morale | UNKNOWN | UNKNOWN | non | — |
| capteur | 3 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 4 | Body | UNKNOWN | UNKNOWN | non | — |
| capteur | 4 | Attention | UNKNOWN | UNKNOWN | non | — |
| capteur | 4 | Morale | UNKNOWN | UNKNOWN | non | — |
| capteur | 4 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 5 | Body | UNKNOWN | UNKNOWN | non | — |
| capteur | 5 | Attention | UNKNOWN | UNKNOWN | non | — |
| capteur | 5 | Morale | UNKNOWN | UNKNOWN | non | — |
| capteur | 5 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 6 | Body | NORMAL | NORMAL | non | — |
| capteur | 6 | Attention | NORMAL | NORMAL | non | — |
| capteur | 6 | Morale | NORMAL | NORMAL | non | — |
| capteur | 6 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 7 | Body | UNKNOWN | UNKNOWN | non | — |
| capteur | 7 | Attention | NORMAL | NORMAL | non | — |
| capteur | 7 | Morale | NORMAL | NORMAL | non | — |
| capteur | 7 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 8 | Body | NORMAL | NORMAL | non | — |
| capteur | 8 | Attention | NORMAL | NORMAL | non | — |
| capteur | 8 | Morale | NORMAL | NORMAL | non | — |
| capteur | 8 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 9 | Body | NORMAL | NORMAL | non | — |
| capteur | 9 | Attention | NORMAL | NORMAL | non | — |
| capteur | 9 | Morale | NORMAL | NORMAL | non | — |
| capteur | 9 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 10 | Body | NORMAL | NORMAL | non | — |
| capteur | 10 | Attention | NORMAL | NORMAL | non | — |
| capteur | 10 | Morale | NORMAL | NORMAL | non | — |
| capteur | 10 | decision | CONTINUE | CONTINUE | non | — |
| capteur | 1-10 | jours de procédure | 0 | 0 | non | — |
| capteur | 1-10 | T1 donnée manquante jamais NORMAL | 0 cas | 0 cas | non | — |
| capteur | 1-10 | jeu crédible : MISSING et ARTIFACT présents | oui | MISSING 373, ARTIFACT 23 | non | — |

## Robustesse : l'histoire hors de la graine 42 (INFO)
Mêmes paramètres que la démo (amplitude 2,5, règle `Params()`), graines 1000 et suivantes.

| Mode du poignet | Graines | Procédure ouverte au jour 7 | Attention DEGRADED au jour 7 | Procédure dès le jour 6 |
|---|---|---|---|---|
| rapide (démo) | 200 | 89 % | 70 % | 0 % |
| complet | 100 | 91 % | 82 % | 0 % |

Lecture : l'écran du jour 7 (« Attention DEGRADED ») dépend de la graine 42. Ne pas dire au jury que cela arrive à chaque fois : c'est un scénario de démonstration, pas une mesure.

## Proposition à M1 (non appliquée) : histoire et témoin en mode complet du poignet
En mode rapide, l'histoire montrée au jury ne contient aucune valeur manquante ni aucun artefact (piège « jeu trop propre » de la fiche M4). Même graine 42, mêmes attendus, `fast=False` :

| Scénario | Écarts à l'attendu | MISSING | ARTIFACT |
|---|---|---|---|
| histoire | 0 | 302 | 22 |
| temoin | 0 | 304 | 23 |

À changer ensemble si M1 accepte : `VARIANTS` de `scripts/run_story.py` (M2) et `generate_kwargs.fast` des scénarios (M4, à noter comme DEV-02 : entrée modifiée, attendus intacts). Les valeurs affichées (FC de repos, explications) changent : à faire avant les captures de 22:30.

## Non couvert par cette recette
- Écrans Streamlit (M3) et deck : hors périmètre M4.
- G4 « hors plage » : aucune plage de plausibilité n'est définie, la porte ne lit jamais la valeur.
- T3 « confiance réduite 1 h après le retour du capteur » : le moteur ne produit pas de confiance par heure.
- G10 : la simultanéité est simulée par un indicateur (`pending_lock`), pas par un vrai verrou.
