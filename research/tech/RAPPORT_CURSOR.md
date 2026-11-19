# Rapport Cursor — tech-modules — 19/11/2026

Changepoint — quoi : CUSUM montant et BOCPD gaussien. Séries SIMULATED. Graine A 11011 gèle k=0.5 et h=4. Graine B 22022 et CO01 jours 1-10 sont le contrôle.
Changepoint — vérifié : `python -m pytest -q tests/test_changepoint.py` → 8 passed. `python -m ruff check csync` → All checks passed.
Changepoint — non vérifié : le câblage dans l'interface (Claude). Sur la capsule, 284.553 est franchi à l'indice 5 et CUSUM alarme à l'indice 6. La pente qui alarme avant 284.553 est une rampe SIMULATED.
Changepoint — ce qui peut casser : un écart estimé sur cinq jours plats gonfle les z. BOCPD suppose des z de variance 1.
Changepoint — annuler : `git revert 1b8a439`.

capsule_sign — quoi : enveloppe Ed25519. Empreinte JSON canonique. Le texte public est « detects modification ».
capsule_sign — vérifié : `python -m pytest -q tests/test_capsule_sign.py` → 6 passed. Licence lue dans les métadonnées du paquet 50.0.2 : Apache-2.0 OR BSD-3-Clause, ligne ajoutée à requirements.txt et THIRD_PARTY_NOTICES.md.
capsule_sign — non vérifié : une installation neuve sans `pip install -r requirements.txt`.
capsule_sign — ce qui peut casser : une clé qui n'est pas 32 octets bruts renvoie une entrée mal formée.
capsule_sign — annuler : `git revert 3999726`.

crdt_sim — quoi : registres last-writer-wins. Objet étiqueté simulation. Égalité d'horloge : le replica_id le plus grand l'emporte.
crdt_sim — vérifié : `python -m pytest -q tests/test_crdt_sim.py` → 5 passed. 25 graines fixes pour la commutativité et l'associativité. Coupure aux pas 4-8, délai 2, convergence au dernier pas.
crdt_sim — non vérifié : hypothesis n'est pas utilisé (boucles à graine fixe). Pas de réseau réel.
crdt_sim — ce qui peut casser : un délai plus long que le nombre de pas laisse le dernier message non livré.
crdt_sim — annuler : `git revert c6350b7`.

hrv — quoi : RMSSD, SDNN (écart échantillon, diviseur n-1), série SIMULATED, nettoyage hors de 300-2000 ms. Aucun fichier PhysioNet chargé.
hrv — vérifié : `python -m pytest -q tests/test_hrv.py` → 5 passed. Quatre intervalles calculés à la main. Stress plus haut, RMSSD plus bas, sur 20 graines.
hrv — non vérifié : l'écart clinique du papier de 1996 (diviseur n ou n-1) n'a pas été rejoué sur un extrait. licences.md interdit le chargement réel.
hrv — ce qui peut casser : une fréquence moyenne très haute peut rapprocher les intervalles de zéro si le stress est bas. Le générateur refuse stress hors de 0 à 1.
hrv — annuler : `git revert 8c5747c`.

Suite — `python -m pytest -q` → 2 failed, 328 passed. Les deux échecs sont dans tests/test_reachability.py (module orphelin et noms publics). test_reachability.py n'a pas été modifié. `csync.tech.registry` était déjà dans cet échec avant ces jalons. Pas de push de main.
