# FICHIER: pitch/deck/captures_map.md
Date/heure : sam. 14/11/2026 08:10 Lomé (UTC) · Commit de référence : dc61786 · Version v1
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Remplace : `CAPTURES_A_FAIRE.md` (phase 2), dont les options de commande étaient supposées.

## Préparer (commandes lues dans le dépôt, exécutées le 14/11 sur le zip rev4)
```bash
python scripts/run_story.py          # écrit data/out/ ; histoire = seed 42, drift_amp 2.5, fast (VARIANTS dans le script)
streamlit run csync/ui/app.py        # interface ; le curseur « Mission day » ouvre au jour 7
```
Résultat obtenu à l'exécution :
- `histoire -> 3 procedure day(s) | events: 1 | capsules: 12`, puis les lignes `temoin` et `capteur` à 0 jour de procédure.
- `states_histoire.csv`, jour 7 : Body WATCH, **Attention DEGRADED**, Morale NORMAL ; décision OPEN_PROCEDURE PROC-FATIGUE-01 (IMPORTANT).
- Capsule de reprise du jour 10 : `G3: PH01 is stale (14 min > 10 min)` ; avec l'override : `G6: Commander override logged; it never authorises a resume on its own`.

**Pas d'option `--seed` ni `--drift-amp`** : les paramètres sont fixés dans `scripts/run_story.py` (VARIANTS). Ne pas les changer pour les captures.

## Correspondance diapo → capture
Mettre les PNG dans `pitch/deck/captures/` avec ces noms exacts, puis lancer `python pitch/deck/embed_captures.py`, qui produit `deck_final.html`.

| Diapo | Capture | Écran de l'application et manipulation | Doit être visible | Nom de fichier attendu |
|---|---|---|---|---|
| 3 | C1 | Vue principale, curseur sur le jour 7 | 5 cartes : Body Watch, Attention Degraded, Morale Normal, Mission et Habitat gris « Context only — not evaluated » ; bandeau SYNTHETIC DATA | `C1_dimensions_j7_seed42_amp25.png` |
| 3 | C2 | Jour 7, explication + action + volet « Signals » ouvert | Ce qui a changé (valeur, unité), action PROC-FATIGUE-01, « Human decision: pending » | `C2_capsule_j7_seed42_amp25.png` |
| 4 | C3 | Jour 9, écran « Guided emergency », bouton « Next » jusqu'à « Step 3 of 6 » | Mesures guidées avec « How to measure », « Why: Source to be added (M1) » (à laisser visible, c'est honnête), valeurs « Recorded » ; phrase fixe « Follow the onboard medical checklist and the crew medical officer. » ; aucun médicament | `C3_procedure_j9_seed42_amp25.png` |
| 4 | C4 | Jour 9, choix « Link down », puis « Link restored » (capturer le second) | « Waiting for link — report queued », puis « Delivered to ground (once) » | `C4_file_envoi_j9_seed42_amp25.png` |
| 5 | C5 | Jour 10, « Request resume », puis « Commander override » | `Gate decision: REFUSE_RESUME`, raison PH01 14 min > 10 min, ligne de journal de l'override | `C5_reprise_j10_seed42_amp25.png` |
| 6 | C6 | **Pas un écran de l'application.** Version anglaise de `pitch/figures/nasa_eda_habitat_fr.png` (CO2, température, rayonnement, RR-1) | Titres en anglais ; annotation « value frozen 37 h (2,646 ppm) → ARTIFACT, never “normal” » ; crédit EDA | `C6_habitat_eda_rr1_en.png` |

## Points d'attention
- **C6** : aucun script du zip ne produit `nasa_eda_habitat_fr.png` (recherche faite dans tout le dépôt). La version anglaise doit être refaite par le chat qui produit les captures. Sinon, garder le cadre vide.
- **C4** : l'interface coche « Delivered to ground (once) ». `run_story.py` signale aussi que la vue sol garde la première copie reçue (19:25, un doublon). C'est un écart connu, déjà notifié à M1 dans le code. La diapo dit seulement « delivered once », ce qui est exact.
- **C5** : chaque appui sur « Commander override » ajoute **une** ligne de journal, et non deux comme le disait le storyboard v3.
- Format : 1920×1080 PNG, même thème pour toutes les captures, aucune notification, aucun nom.

## Mise à jour 14/11 ~15:20 UTC (deck v3)
- C1–C5 : le deck utilise des **recadrages sans retouche** (`captures/crops/Cn_crop.png`, script `crop_captures.py`) ; les originaux restent dans `captures/`.
- **C6 remplacée** : figure tirée de la série brute 5 min de RR-1 (`pitch/figures/make_eda_habitat_fig.py`) ; plateau de CO2 de 153 h (21/09 04:24 → 27/09 13:25), et non plus 37 h (extrait horaire du 26/09 au 05/10).
- Logo : déposer `captures/LOGO_ACTUEL_horizontal.png` puis `python pitch/deck/embed_captures.py` ; exports : `python pitch/deck/export_pdf_pptx.py`.
