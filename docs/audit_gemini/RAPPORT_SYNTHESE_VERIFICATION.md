Version 1 · 14/11/2026 ~07h10 Lomé · Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ · Remplace : création initiale

# Rapport de vérification indépendante — C-Sync (`commit dc61786`)

## 1. Périmètre et nature des preuves

- **G1 (`AUDIT_PILOTS.md`) — Raisonné et calculé analytiquement (non exécuté sur le banc complet) :** inspection des scripts `pilot.py`, `pilot2.py`, `pilot3.py`, `generator.py`, `rules.py` et des fichiers `pilot3_sweep.csv`, `pilot3_paired.csv`.
- **G2 (`NASA_DATA_CATALOG.md`) — `NON VÉRIFIÉ` (absence d'accès web) :** recensement strictement limité aux références présentes dans `generator.py` (`S03-EDA-RR1` et `PhysioNet S10`), sans aucun identifiant externe deviné ni URL non ouverte.
- **G3 (`detectors_reference.py` + `RAPPORT_VECTEURS.md`) — Calculé et exécuté en Python (stdlib uniquement) :** ré-implémentation indépendante des trois détecteurs (`Règle 1.5`, `EWMA`, `CUSUM`) et exécution sur les 8 cas de `test_vectors_detectors.json` (`24 / 24` concordances exactes).

## 2. Points clés à retenir pour l'équipe MONOLITH (M1–M5)

1. **Validation des détecteurs unitaires (G3 — exécuté) :** la spécification mathématique des trois détecteurs (`Règle d>=1.5 sur 2 jours`, `EWMA λ=0.3 L=2.5`, `CUSUM k=0.5 h=3.0`) est cohérente et sans ambiguïté sur l'ensemble des 8 vecteurs de test, y compris aux bornes strictes (`s = 3.0` vs `s > 3.0`) et en présence d'un jour manquant (`missing_day8`).
2. **Justification du réglage retenu le 14/11 par M1 (G1 — raisonné) :** sur le générateur simulé `csync-synth-0.1`, la règle déterministe `d >= 1,5` sur 2 jours consécutifs produit **`0,7 %`** de fausses procédures sur équipages sains simulés (`0,13 %` par astronaute-jour) et détecte **`95,3 %`** des dérives graduelles de `1,5 SD` avec un délai médian de **`1,0` jour**. À taux de fausses alertes égal (`0,7 %`), EWMA (`L=3.0`) et CUSUM (`h=4.0`) ne font pas mieux (`délai médian 2,0 jours`).
3. **Corrections requises avant toute communication chiffrée (G1 — raisonné) :**
   - Ne pas citer les p-values de `pilot3_paired.csv` opposant `EWMA L=2.5` (`2,7 %` de fausses alertes) à `Rule 1.5` (`0,7 %`), car les taux de fausses alertes ne sont pas égaux.
   - Ne pas citer les délais du scénario `abrupt 2 SD (onset day 8)` de `pilot3_sweep.csv` sans filtrer les déclenchements survenus aux jours 6 et 7 avant l'injection de l'événement.
   - Préciser que l'évaluation longitudinale codée dans `csync/rules.py` porte sur 3 dimensions (`Body`, `Attention`, `Morale`), tandis que `Habitat` et `Mission` relèvent de règles distinctes.
4. **Traçabilité des données (G2 — `NON VÉRIFIÉ` en ligne) :** toutes les trajectoires d'équipage évaluées proviennent du générateur **SIMULÉ** `csync-synth-0.1`. Aucune affirmation d'usage opérationnel par la NASA ni d'étalonnage clinique réel n'est étayée dans le dépôt.

## 3. Contenu de l'archive ZIP (`csync_verification_complete.zip`)

- `RAPPORT_SYNTHESE_VERIFICATION.md` — Synthèse générale des trois tâches G1, G2, G3.
- `AUDIT_PILOTS.md` — Livrable G1 (audit technique et statistique des pilotes).
- `NASA_DATA_CATALOG.md` — Livrable G2 (état vérifié des sources réelles et protocole OSDR/HRP).
- `detectors_reference.py` — Livrable G3 (ré-implémentation indépendante en bibliothèque standard Python).
- `RAPPORT_VECTEURS.md` — Livrable G3 (tableau de résultats exécutés sur `test_vectors_detectors.json`).
