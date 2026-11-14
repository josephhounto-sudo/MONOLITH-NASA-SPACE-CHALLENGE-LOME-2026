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
