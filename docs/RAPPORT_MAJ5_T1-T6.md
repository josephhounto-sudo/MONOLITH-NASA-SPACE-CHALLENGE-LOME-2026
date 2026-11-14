<!-- 2026-11-14 ~07:00 Lomé (UTC) | commit de référence dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ -->
# Rapport — MAJ 5, tâche lourde T1–T6 (chat M2/M3/M4)

## Base de travail
- Zip `SAUVEGARDE_COMPLETE_C-Sync_14-11_rev4.zip` reçu ; 91 tests verts avant modification (vérifié par exécution).
- Le zip ne contient pas de `.git` : le commit dc61786 est repris comme référence, **non vérifié**.
- Les fichiers JSON n'acceptent pas de commentaires : leur en-tête est une clé `_header`.
- **Écart à l'ordre demandé :** T1 (captures) a été fait en dernier. T2, T3 et T5 modifiaient les écrans ; des captures faites avant auraient été périmées tout de suite.

## Récapitulatif

| Tâche | État | Détail | Preuve |
|---|---|---|---|
| T1 Captures | **Fait** | 3 rendus réels (Chrome sans écran sur l'application en marche) + `pitch/figures/MANIFEST.md`. | Vérifié par exécution ; captures regardées |
| T2 Sources NASA | **Fait, 3 manques** | Sourcés : fréquence cardiaque, tension, sommeil, temps de réaction. **Aucune page NASA lue ne couvre la température corporelle ni la glycémie** → l'écran affiche « No NASA in-flight reference ». **Pas de liste de symptômes « chest pain » sourcée.** Pour le temps de réaction, la page parle seulement de « performance decrements », pas de PVT. | Pages ouvertes et lues le 14/11 vers 06:45 (vérifié). Phrases « why » en nos mots : **relecture humaine nécessaire** |
| T3 Raisons du refus | **Fait** | L'écran dit « The heart-rate reading is 14 min old; the limit is 10 min. ». G3/G6 restent dans « Technical log ». `gate.py` inchangé, tests G1–G10 intacts. | Vérifié par exécution |
| T4 Calibration | **Fait, seuils passés** | (a) 1/100 équipages témoins ouvrent une procédure (plafond 3). (b) 95/100 équipages en dérive en ouvrent une (minimum 90). (c) Les 8 vecteurs passent : règle (moteur réel), EWMA et CUSUM (référence, dans `tests/` uniquement, rien dans `csync/`). | Vérifié par exécution |
| T5 Mots interdits | **Fait** | Un seul cas trouvé, dans `README.md` (« does not diagnose… name causes »), reformulé en phrase positive. `tests/test_banned_words.py` couvre aussi les formes niées. | Vérifié par exécution |
| T6 Cohérence | **Fait** | **127 tests verts, dont 36 nouveaux** (91 avant) : calibration 27, mots interdits 7, procédures +2. `scripts/validate_contracts.py` : 0 fichier en échec. Le zip appliqué sur une copie propre de rev4 donne aussi 127 verts. | Vérifié par exécution |

## Fichiers changés (17)
- **Modifiés :** `README.md`, `csync/capsule.py`, `csync/config/strings_en.json`, `csync/ui/app.py`, `data/procedures/PROC-EMERGENCY-01.json`, `data/procedures/PROC-FATIGUE-01.json`, `docs/HELP_CARD_SOURCES.md`, `tests/test_procedures.py`, `tests/test_run_story.py`, `tests/test_ui.py`.
- **Créés :** `tests/helpers_detectors.py`, `tests/test_calibration.py`, `tests/test_banned_words.py`, `pitch/figures/MANIFEST.md`, `pitch/figures/demo_day7_nominal.png`, `pitch/figures/demo_day9_emergency_step3.png`, `pitch/figures/demo_day10_resume_refused.png`.
- **Pas touché :** `csync/rules.py`, `csync/gate.py`, `docs/team/`, `docs/PROTOCOLES.md`, `docs/blocks/`.

## Commandes (depuis la racine `c-sync/`, après avoir dézippé)
```
python scripts/run_story.py          → histoire 3 procédures, témoin 0, capteur 0
python -m pytest -q                  → 127 passed
python scripts/validate_contracts.py → 7 schemas valid; 0 file(s) failing
streamlit run csync/ui/app.py
```

## À trancher par M1
1. **Délai de communication.** La page NASA « Distance from Earth » (lue) dit « up to 20 minutes one way » ; l'équipe annonce ~22 min (ASCEND). Il faut aligner les deux formulations avant le pitch.
2. **Vecteur EWMA fragile.** Le cas `step_2_at_day8` passe de justesse (1,020 contre une limite de 1,0196). Un changement d'arrondi le fera basculer.
3. **`docs/blocks/code_header.md` se contredit.** Il contient tout le bloc v2 : la ligne « valeurs provisoires n° 1 » dit encore « seuil 1,0 », la section Vérifié dit 1,5. Non modifié (dossier interdit).
4. **Le texte « (IMPORTANT) » est toujours à l'écran au jour 7.** Il vient de la criticité calculée par la règle. Si c'est ce que la MAJ reprochait aux anciennes captures, il faut une décision, pas une retouche.
5. **README, non corrigé (hors tâche).** Il dit « measurements one by one » alors que l'étape 3 affiche les 4 mesures ensemble ; « three detection methods » alors que le pilote en compare 5 ; tableau de statut périmé.
6. **Clé inutilisée.** `no_reference` n'est plus utilisée dans `strings_en.json` ; laissée en place.

TÂCHE LOURDE TERMINÉE — j'attends VALIDATION
