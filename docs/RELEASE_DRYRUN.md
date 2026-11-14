# Répétition de livraison — branche cursor-heavy-1

## E3 — `scripts/check_consistency.py`

Fichier fautif : `data/real/physionet_s10_docs/data_constraints.txt` (octet 0x95, 10 occurrences). Lecture passée en `encoding="utf-8", errors="replace"` dans `R()`.

Sortie du script (14/11/2026) :

```
OK   pytest: 137 passed in 120.92s (0:02:00)
OK   M3-1 criterion holds (day 7 Attention DEGRADED)
0 erreur(s)
```

## E4 — points de `docs/RELEASE_CHECKLIST.md`

La checklist n'a pas été cochée (réservé à M5).

| Point | Résultat |
|---|---|
| `python -m pytest -q` | OK — 137 passed in 74.62s, exit 0 |
| `python scripts/validate_contracts.py` | OK — 7 schémas valides, 0 fichier en échec, exit 0 |
| `python scripts/run_story.py` deux fois (`--out` distincts) | OK — mêmes empreintes SHA-256 ; histoire 3 jours de procédure, 1 événement, 12 capsules |
| `node pitch/tests/test_deck.js pitch/deck/deck_final.html` | ÉCART — toutes les assertions PASS, puis exit 1 : le script écrit `process.argv[3]` (fichier de sortie, voir l'en-tête de `pitch/tests/test_deck.js` ligne 2) et cet argument est absent. Avec ce fichier de sortie : `TOUS LES TESTS PASSENT`, exit 0 |
| V1 Produit à partir du 14/11 | NON VÉRIFIÉ — confirmation des organisateurs hors dépôt |
| V2 Pas de code préexistant sans accord écrit | NON VÉRIFIÉ — le dépôt dit une autorisation orale (D10), pas un écrit |
| V3 Toute source citée dans SOURCES.md | NON VÉRIFIÉ — pas de relecture exhaustive de SOURCES.md dans cette session |
| V4 Données synthétiques étiquetées | OK — bandeau `SYNTHETIC DATA` à l'écran ; générateur `csync-synth-0.1`, graine 42 (`README.md` ligne 36) |
| V5 Pas de seuil clinique sans citation | NON VÉRIFIÉ au-delà de `csync/rules.py` : le fichier dit que ses nombres sont des paramètres de conception |
| V6 Pas de nom, numéro, clé, donnée personnelle | OK pour le scan de `scripts/check_consistency.py` (0 erreur, courriel / téléphone). Images non revues une par une |
| V7 Le changement dit quel test il couvre | OK sur cette branche (commits E1 et E2) |
| V8 Message de commit `Mx:` | OK sur cette branche (`M2:`) |
| V9 Licence MIT | OK — `README.md` ligne 73 et fichier `LICENSE` |
| V10 Relu par quelqu'un d'autre que l'auteur | NON VÉRIFIÉ |
| V11 `AI_USAGE.md` à jour | ÉCART — cette session n'y est pas ajoutée (fichier hors de la liste autorisée par la tâche) |
| V12 Liste du code, textes et images à jour | NON VÉRIFIÉ |

## E5 — cohérence des textes

Chiffres recalculés par `tests/test_claims.py` : 2/300 = 0,666… % (affiché 0,7 %), 143/150 = 95,333… % (95,3 %), 89/150 = 59,333… % (59,3 %). Plateau CO2 brut : (1837 − 1) × 5 min = 153 h. Porte de reprise 10 min. Délai sol de la démo 20 min.

Concordances vérifiées dans le dépôt : jours 7 / 9 / 10 (`pitch/deck/deck.html` lignes 130, 149, 181 ; `pitch/deck/SCRIPT_EN.md` lignes 17, 19, 25 ; `pitch/deck/SCRIPT_FR.md` lignes 19, 23, 29). Jour 7 : Attention DEGRADED et Body WATCH (`SCRIPT_EN.md` ligne 17, `SCRIPT_FR.md` ligne 19), comme les capsules de l'histoire. États NORMAL, WATCH, DEGRADED, UNKNOWN : `README.md` ligne 29. Délai de démo 20 min : `README.md` ligne 27. 0,7 % sur 300 équipages : `README.md` ligne 41 et `deck.html` ligne 203.

Écarts (scripts et deck non modifiés) :

- `pitch/deck/SCRIPT_EN.md` ligne 29 et `pitch/deck/SCRIPT_FR.md` ligne 34 disent 95 % et 59 %. Le calcul donne 95,3 % et 59,3 %, déjà écrits dans `README.md` ligne 41. Arrondi oral à l'entier.
- `SCRIPT_EN.md` ligne 29 et `SCRIPT_FR.md` ligne 34 disent « plus de six jours » de CO2 constant. La série brute mesure 153 h (`README.md` ligne 34), soit 6,375 jours.
- `pitch/deck/deck.html` ligne 203 ne donne que 0,7 % sur 300 équipages. Les 95,3 % et 59,3 % n'y sont pas.
- `pitch/deck/deck.html` ligne 134 ne cite que « Attention Degraded » au jour 7. Les capsules et les deux scripts citent aussi Body WATCH.
- `README.md` ligne 6 dit « 20 minutes away ». `deck.html` ligne 108 et `SCRIPT_EN.md` ligne 11 disent « up to ~20 minutes » / « up to twenty minutes ». Le paramètre de démo est 20 min exactement. Phrase du README laissée telle quelle : elle correspond au délai simulé, pas au plafond NASA.
- `README.md` ligne 49 (« work in progress ») et ligne 70 (« in progress ») : les trois écrans ont des tests AppTest verts. Statut d'équipe, non modifié.

Correction README : ligne 68, « 128 automated tests » remplacé par « 137 automated tests » (comptage `pytest` de cette branche).
