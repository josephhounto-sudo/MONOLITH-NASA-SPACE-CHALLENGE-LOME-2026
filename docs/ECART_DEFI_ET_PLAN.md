# Écart défi ↔ C-Sync, pack Cursor, plan du diapo (15/11/2026)

## 1. C-Sync règle-t-il les problèmes nommés dans le défi ? Réponse honnête : en partie

| Exigence de l'énoncé | Ce que fait C-Sync (branche nasa-data) | Écart |
|---|---|---|
| Suivre la santé d'un astronaute en autonomie, hors ligne | Règle v3 vs ligne de base personnelle, capsule de décision, mémoire locale, reprise après coupure (G1–G10) | Mesuré sur données **synthétiques** seulement ; pas de données équipage réelles |
| Silhouette / zones du corps | 8 zones, présélection par symptôme, fiche comment/pourquoi/quand | Fiches non validées par un médecin (M4 en attente) |
| Graphiques dynamiques | Courbes par indicateur jusqu'au jour choisi, base, seuil, jours signalés | Données synthétiques ; 8 indicateurs seulement |
| Les 5 dangers NASA | Tableau des 5 dangers avec statut | Seuls CO2/température/humidité/radiation (habitat) sont mesurés ; les autres affichés « non mesuré » |
| Données NASA réelles | 14 missions habitat, CO2 en mmHg vs exigence 3 mmHg, qualité, provenance | Contexte habitat uniquement, pas de physiologie équipage |
| **Conseils de traitement / amélioration de la santé** | **Aucun, volontairement** : procédures NASA existantes + décision humaine | **Trou principal.** À assumer ou à combler par des procédures citées HRP/NASA, jamais inventées |
| Gamification, variantes d'environnement | Non faits | Hors périmètre avant 15:00 ; à dire en « suite » |

Verdict : C-Sync répond bien à « détecter tôt, hors ligne, avec décision humaine » ; il ne répond pas à « guider un traitement ». Le dire dans le pitch évite que le jury le découvre.

## 2. Pack Cursor (tâches à fichiers disjoints, à coller une par session)
Je n'ai pas pu piloter Cursor depuis ici (pas d'accès à ton écran). Chaque tâche : branche `cursor-<n>` depuis `nasa-data`, ne toucher que les fichiers listés, lancer `python scripts/build_context.py`, `python scripts/check_consistency.py`, `pytest -q`, pousser sur la branche, jamais sur main.
1. **EWMA vs règle v3** : seulement `research/ewma_compare.py` + `tests/test_ewma_compare.py`. Comparer sur les mêmes scénarios synthétiques, rapporter faux déclenchements et délai ; ne pas changer le moteur.
2. **Contrôle qualité** : seulement `csync/quality.py` + tests. Plateaux, valeurs manquantes, doublons ; cas limites.
3. **Mémoire locale branchée** : seulement `csync/memory.py` + `tests/test_adapters_memory.py`. Redémarrage, fichier corrompu, concurrence.
4. **Textes FR** : seulement `csync/config/strings_fr.json` (traduction fidèle, mêmes clés, mots interdits respectés).
Interdits : modifier `csync/ui/app.py`, `docs/`, `pitch/`, `AI_USAGE.md` (conflits avec le design du frère).

## 3. Plan du diapo (après choix du design)
Pas de PDF final avant la fusion. Ordre : (1) problème + équipe (noms à fournir) ; (2) pourquoi les astronautes ne peuvent pas attendre le sol (délai 0–22 min, source NTRS) ; (3) règle v3 en une image ; (4) capture réelle de l'app jour 9 (remplacer « Static mock-up ») ; (5) silhouette + données NASA réelles (CO2 vs 3 mmHg) ; (6) limites annoncées : synthétique, pas de traitement, validation M4 ; (7) suite. Rôle B de M2 : diapos 4–5, 110 s.
Après fusion (~20 min) : recapturer C1–C5, régénérer PDF et pptx, relancer les tests.
