# Rapport Cursor — tech-modules — 19/11/2026

Changepoint — quoi : CUSUM montant et BOCPD gaussien, séries SIMULATED, graine A 11011 (k=0.5, h=4) séparée de la graine B 22022 et de CO01 jours 1-10.
Changepoint — vérifié : `python -m pytest -q tests/test_changepoint.py` → 8 passed ; `python -m ruff check csync` → All checks passed.
Changepoint — non vérifié : suite complète rouge (verrou d'orphelin). Sur la capsule, le seuil 284.553 est franchi à l'indice 5 et CUSUM (h=4) alarme à l'indice 6 ; la pente lente testée est une rampe SIMULATED, pas ces 10 jours. `ruff check csync tests` reste rouge pour 62 erreurs déjà sur glass-navy.
Changepoint — ce qui peut casser : un appelant qui estime l'écart sur 5 jours plats obtient des z énormes ; BOCPD suppose des z de variance 1.
Changepoint — annuler : les fichiers ne sont pas commités ; les retirer du disque (`csync/analytics/`, `tests/test_changepoint.py`) ramène l'arbre de travail à glass-navy.

capsule_sign — non commencé. Arrêt après le jalon 1. Rien à annuler.
crdt_sim — non commencé. Arrêt après le jalon 1. Rien à annuler.
hrv — non commencé. Arrêt après le jalon 1. Rien à annuler.
Suite — le détail du blocage est dans research/tech/BLOCAGE.md. Branche tech-modules, pas de push de main.
