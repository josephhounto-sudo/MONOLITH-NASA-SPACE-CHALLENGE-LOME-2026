# Promesses de départ — taux de complétion (15/11/2026 08:00 UTC)
FAIT PAR L'IA. Liste fermée de 32 promesses extraites de `README.md`, `docs/SUBMISSION.md`, des scripts de pitch et du guide officiel de soumission. Une promesse est « faite » seulement si un test, une mesure ou un fichier la prouve. État de la branche `nasa-data` (174 tests verts, axe 0 violation à 1280 et 390 px).

**Taux : 23 faites sur 32 (72 %), 6 partielles, 3 non faites.** Sur `main` seul (sans la branche) : 21 sur 32 (66 %), car la silhouette et l'accessibilité n'y sont pas.

| # | Promesse | État | Preuve ou manque |
|---|---|---|---|
| 1 | Hors ligne, aucun appel réseau à l'exécution | Faite | aucun import réseau dans `csync/`, `synthetic/` ; seul `scripts/eda_load.py` lit un fichier local |
| 2 | Comparaison à la référence personnelle de 5 jours | Faite | `tests/test_rules.py` |
| 3 | Indique son degré de certitude | Faite | bloc `reliability` de la capsule, schéma |
| 4 | Donnée manquante jamais montrée comme normale | Faite | `test_rules.py` (dont le test de M2), `test_capsule.py` |
| 5 | Urgence guidée hors ligne, 6 étapes | Faite | `tests/test_ui.py` jour 9 |
| 6 | Rapport en file d'attente, livré une seule fois | Faite | `tests/test_sendqueue.py` |
| 7 | Reprise refusée si mesure trop ancienne, même avec ordre du commandant | Faite | `tests/test_gate.py`, `test_run_story.py` |
| 8 | Aucun traitement, médicament ni seuil clinique | Faite | contrôle de vocabulaire (`csync/language.py`), tests de textes |
| 9 | Cinq dimensions, quatre états | Faite (limite déclarée) | 3 dimensions évaluées, Mission et Habitat en contexte |
| 10 | Adaptateurs de sources vers le contrat Measurement | **Partielle** | adaptateur NASA EDA fait et testé (`csync/adapters.py`) ; la saisie d'équipage vient du générateur, pas d'un adaptateur |
| 11 | Contrôle qualité (manquant, artefact, valeur figée) avant les règles | **Partielle** | branché sur les données NASA ; les scénarios d'équipage ne contiennent aucun artefact (recette M4) |
| 12 | Mémoire locale | **Partielle** | `csync/memory.py` (une ligne par mesure, une seule fois, survit au redémarrage, testé) ; non branchée à l'écran |
| 13 | Capsule de décision à 8 blocs validée | Faite | `contracts/`, tests de schéma |
| 14 | Sol simulé à 20 min | Faite | `csync/sendqueue.py`, `run_story.py` |
| 15 | Utilise des données NASA réelles | Faite | panneau Habitat, `tests/test_habitat.py`, 14 missions recalculées depuis le brut |
| 16 | Carte du corps (exemple de l'énoncé) | Faite (branche) | `csync/silhouette.py`, `tests/test_silhouette.py` |
| 17 | Chiffres 0,7 % / 95,3 % / 59,3 % | Faite (avec réserve) | `tests/test_claims.py` ; seuil réglé sur les mêmes scénarios |
| 18 | Chaque mesure cite une source NASA ou dit « aucune référence » | Faite | fiches et procédures, tests d'écran |
| 19 | Données synthétiques étiquetées partout | Faite | bandeau, tableau de provenance |
| 20 | Délais NASA (0–22 min ; jours à mois) | Faite | NTRS 20220013418 lu, diapo 2, scripts |
| 21 | 7 diapos en anglais, PDF | Faite | `pitch/deck/`, `test_deck.js` |
| 22 | Noms des membres sur les diapos (guide officiel) | **Non faite** | noms non fournis |
| 23 | Titre du défi sur les diapos | Faite | diapo 1 |
| 24 | Image du projet, expérience utilisateur, donnée NASA sur les diapos | Faite | captures C1–C5 et figure NASA ; à recapturer après le design |
| 25 | Lien de démo public, sans connexion | **Partielle** | dépôt et PDF répondent en HTTP 200 ; test en navigation privée par un tiers non fait |
| 26 | Usage de l'IA déclaré (filigrane des images IA) | **Partielle** | déclaré ; logo IA sans filigrane, décision de M1 |
| 27 | Travail original relu par un tiers | **Partielle** | tests automatiques ; relecture humaine (V10) non faite |
| 28 | Pitch de 5 min répété au chronomètre | **Non faite** | M1 et M2, avant 11:00 |
| 29 | Soumission préparée (8 champs) | Faite | `docs/SUBMISSION.md` ; non soumise |
| 30 | Accessible (WCAG A+AA) | Faite (branche) | axe : 0 violation, jours 7, 9, 10, 1280 et 390 px, mouvement normal et réduit |
| 31 | Tests automatiques solides | Faite | 174 tests |
| 32 | Interface « futuriste, verre léger, formes » (brief de M1) | **Non faite** | en cours dans la session de design |

Reste hors de portée de l'IA : 22, 28, 32, la fin de 25, 26 et 27. Tout le reste de la liste est fait ou prouvé.
