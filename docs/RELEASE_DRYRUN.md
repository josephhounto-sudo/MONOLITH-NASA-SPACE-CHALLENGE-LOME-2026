# Répétition de livraison — branche cursor-heavy-1

## E3 — `scripts/check_consistency.py`

Fichier fautif : `data/real/physionet_s10_docs/data_constraints.txt` (octet 0x95, 10 occurrences). Lecture passée en `encoding="utf-8", errors="replace"` dans `R()`.

Sortie du script (14/11/2026) :

```
OK   pytest: 137 passed in 120.92s (0:02:00)
OK   M3-1 criterion holds (day 7 Attention DEGRADED)
0 erreur(s)
```
