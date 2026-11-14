Version 1 · 14/11/2026 ~07h10 Lomé · Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ · Remplace : création initiale

## Statut d'exécution et méthode

- **Statut :** **Calculé et exécuté par moi** en Python (bibliothèque standard uniquement : `math`, `json`, `typing`) via `detectors_reference.py`, ré-implémenté indépendamment à partir de la spécification G3 seule, avant toute comparaison avec `pilot.py`.
- **Commande d'exécution locale :**
  ```bash
  python detectors_reference.py docs/blocks/test_vectors_detectors.json
  ```
- **Résultat global :** **`24 / 24` paires (8 cas × 3 détecteurs) concordent exactement** (`0` écart sur les `240` drapeaux journaliers évalués).

---

## Tableau de confrontation : cas × détecteur (jours 1 à 10, `0 = False`, `1 = True`)

| Cas de test (`test_vectors_detectors.json`) | Détecteur | Drapeaux obtenus (`J1..J10`) | Drapeaux attendus (`J1..J10`) | Écart | Qui a tort et pourquoi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `flat_zero` | Règle (`d>=1.5`, 2 j) | `0000000000` | `0000000000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `flat_zero` | EWMA (`λ=0.3, L=2.5`) | `0000000000` | `0000000000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `flat_zero` | CUSUM (`k=0.5, h=3`) | `0000000000` | `0000000000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `gradual_ramp` | Règle (`d>=1.5`, 2 j) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `gradual_ramp` | EWMA (`λ=0.3, L=2.5`) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `gradual_ramp` | CUSUM (`k=0.5, h=3`) | `0000000001` | `0000000001` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `step_2_at_day8` | Règle (`d>=1.5`, 2 j) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `step_2_at_day8` | EWMA (`λ=0.3, L=2.5`) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `step_2_at_day8` | CUSUM (`k=0.5, h=3`) | `0000000001` | `0000000001` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `single_spike_4_day7` | Règle (`d>=1.5`, 2 j) | `0000000000` | `0000000000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `single_spike_4_day7` | EWMA (`λ=0.3, L=2.5`) | `0000001000` | `0000001000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `single_spike_4_day7` | CUSUM (`k=0.5, h=3`) | `0000001000` | `0000001000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `persistent_1_5` | Règle (`d>=1.5`, 2 j) | `0000001111` | `0000001111` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `persistent_1_5` | EWMA (`λ=0.3, L=2.5`) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `persistent_1_5` | CUSUM (`k=0.5, h=3`) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `missing_day8` | Règle (`d>=1.5`, 2 j) | `0000000001` | `0000000001` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `missing_day8` | EWMA (`λ=0.3, L=2.5`) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `missing_day8` | CUSUM (`k=0.5, h=3`) | `0000000011` | `0000000011` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `favourable_negative` | Règle (`d>=1.5`, 2 j) | `0000000000` | `0000000000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `favourable_negative` | EWMA (`λ=0.3, L=2.5`) | `0000000000` | `0000000000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `favourable_negative` | CUSUM (`k=0.5, h=3`) | `0000000000` | `0000000000` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `late_step_3_at_day9` | Règle (`d>=1.5`, 2 j) | `0000000001` | `0000000001` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `late_step_3_at_day9` | EWMA (`λ=0.3, L=2.5`) | `0000000001` | `0000000001` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |
| `late_step_3_at_day9` | CUSUM (`k=0.5, h=3`) | `0000000001` | `0000000001` | Aucun écart (`10/10` jours identiques) | Sans objet (concordance totale) |

---

## Vérification des cas limites critiques (calculés/exécutés)

1. **Période de référence (`J1..J5`) :** aucun déclenchement sur les 5 premiers jours dans l'ensemble des 8 cas (`00000...`).
2. **Frontière stricte `>` vs `>=` sur `single_spike_4_day7` (`z_7 = 4`, `z_8 = 0`) :**
   - **CUSUM (`k=0.5, h=3.0`) :** au jour 7, `s = 3.5 > 3.0` (`True`). Au jour 8 (`z_8 = 0`), `s = max(0, 3.5 + 0 - 0.5) = 3.0`. Comme la condition est strictement `s > 3.0`, le jour 8 repasse à `False`, en accord exact avec le vecteur attendu.
   - **EWMA (`λ=0.3, L=2.5`) :** au jour 7 (`n=2`), `e_2 = 1.2 > 2.5 * sigma_2 = 0.9155` (`True`). Au jour 8 (`n=3, z_8 = 0`), `e_3 = 0.7 * 1.2 = 0.84 <= 2.5 * sigma_3 = 0.9865` (`False`), en accord exact avec le vecteur attendu.
3. **Effet de la valeur manquante sur `missing_day8` (`z = [..., 1.0, 2.0, null, 2.0, 2.0]`) :**
   - **Règle (`d >= 1.5`, 2 jours consécutifs) :** au jour 7 (`z_7 = 2.0`), `run = 1` (`False`). Au jour 8 (`null`), `run` est remis à `0` (`False`). Au jour 9 (`z_9 = 2.0`), `run = 1` (`False`). Le signalement n'apparaît qu'au jour 10 (`run = 2`, `True`), en accord exact avec le vecteur attendu.
   - **EWMA et CUSUM :** le jour 8 (`null`) n'incrémente pas `n` et ne réinitialise pas l'accumulateur ; dès le jour 9 (`z_9 = 2.0`), `e_3 = 1.167 > 0.9865` et `s = 3.5 > 3.0` déclenchent (`True`), en accord exact avec le vecteur attendu.
4. **Seuil exact `persistent_1_5` (`z = 1.5` aux jours 6–10) :**
   - **EWMA :** au jour 8 (`n=3`), `e_3 = 0.9855 <= 2.5 * sigma_3 = 0.9864995` (`False` à `0,001` près), puis `True` aux jours 9 et 10 (`e_4 = 1.13985 > 1.0195`). Concordance totale avec le vecteur attendu.
   - **CUSUM :** au jour 8, `s = 3.0` (`False`), puis `s = 4.0 > 3.0` au jour 9 (`True`). Concordance totale avec le vecteur attendu.
5. **Variations favorables (`favourable_negative`, `z = -2` aux jours 6–10) :** aucun déclenchement sur les 3 détecteurs (`0000000000`), car CUSUM est borné à `0` par `max(0, ...)` et EWMA/Règle testent uniquement les dépassements positifs (`> L * sigma_n` et `>= 1.5`).

---

## Comparaison secondaire avec `research/pilot/pilot.py` (après exécution des vecteurs)

- Après vérification contre `test_vectors_detectors.json`, les fonctions `run_flags`, `ewma_flags` et `cusum_flags` de `research/pilot/pilot.py` implémentent exactement les mêmes équations et conventions de gestion des valeurs manquantes que `detectors_reference.py`.
