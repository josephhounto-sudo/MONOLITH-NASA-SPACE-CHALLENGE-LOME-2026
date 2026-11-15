# Brief — tous les changements de design (branches `design-v2` → `design-v3`), dimanche 15/11/2026 ~07:50 (Lomé = UTC)
FAIT PAR L'IA. **Validé par M1** : `design-v2` (07:20), `design-v3` (07:38, « v3 valide »). Rien n'est fusionné dans `main`, rien n'est déployé. Point de retour : `checkpoint-before-design` (= `main` 8c165b5).

## 1. Pour l'IA de la session principale : fusionner et refaire le deck (~25 min)
```
git fetch origin && git checkout main && git pull --rebase
git merge --no-ff origin/design-v3          # contient m3-design + design-v2 + nasa-data + ce passage
python scripts/run_story.py && python -m pytest -q        # attendu : 168 verts
python scripts/check_consistency.py                       # attendu : 0 erreur
python scripts/build_context.py && grep -rIl "^<<<<<<<" . --exclude-dir=.git   # attendu : rien
streamlit run csync/ui/app.py                             # profil par défaut : fusion (clair)
```
Puis captures C1–C5 **avec le panneau Habitat visible** (`pitch/deck/embed_captures.py`, `export_pdf_pptx.py`). Conflits probables avec `main` : `.streamlit/config.toml` (garder la base **claire** de `design-v3`), `docs/CONTEXTE_IA.md` (régénérer).

## 2. Ce qui a changé, fichier par fichier
| Fichier | Changement | Pourquoi |
|---|---|---|
| `csync/ui/style.py` | profil `fusion` (défaut) autonome : verre clair, plis blancs, champ chaud = criticité du jour, champ froid = liaison sol ; **pierre sombre** (+ ciel étoilé léger) seulement pour le CRITICAL ; une forme pleine par état ; bandeau de mission (métadonnées + trajectoire 10 jours, jours à venir vides) ; historique 10 jours par carte ; section Habitat « NASA DATA » ; logo C-Sync animé dans la barre du haut (statique en mouvement réduit) | brief M1 + 10 références ; voir `DESIGN_FUSION.md`, `RAPPORT_GRAPHIQUE_V3.md` |
| `csync/ui/app.py` | événement CRITICAL en premier (conteneur `cs-stone`), bandeau de mission après le curseur, historique dans les cartes, `habitat_panel()` dans `cs-habitat`, couleurs de graphique via `style.chart_colors` ; aucune couleur en dur | hiérarchie (le profil `signal` cachait l'urgence sous la ligne de flottaison à 1280×900) |
| `csync/config/theme.json` | bloc `fusion` : fond, encre, pierre, crème, champs, couleurs d'état **sur fond clair** (≥ 4,5:1), couleurs de graphique (≥ 3:1) | le cyan `#00E0F5` faisait 1,6:1 sur blanc |
| `csync/config/strings_en.json` | clés `brand_*`, `habitat_*` (de `nasa-data`), bandeau de mission, historique | aucun texte en dur |
| `.streamlit/config.toml` | base **claire** | les contrôles natifs suivent le verre clair ; remettre `dark` pour les anciens profils |
| `csync/ui/fonts/` | Clash Display, Satoshi (woff2) + licence Fontshare | typographie hors ligne, usage web autorisé |
| `csync/ui/assets/` | logo C-Sync animé et statique (générés par `brand/make_mark.py`) | barre du haut, demandé par M1 à 07:38 |
| `brand/` | marque C-Sync (SVG ink, cream, dégradé, petite taille), lockups, `csync_motion.*`, **`csync_care_sync_to_csync_{dark,light}.{html,mp4}`** (+ GIF sombre) | identité et ouverture de pitch |
| `tests/test_design_fusion.py` | 6 tests : contrastes des jetons, pierre = CRITICAL seulement, inconnu jamais comme normal, polices présentes, **la trajectoire ne montre jamais l'avenir** | garde-fous |
| `docs/` | `DESIGN_FUSION.md`, `RAPPORT_GRAPHIQUE_V3.md`, ce brief, `DESIGN_TEST_5S.md` v2 (+ images `design_ab/blind_5s_v2`, clé à ne pas ouvrir) | traçabilité |
| `AI_USAGE.md` | ligne : logo C-Sync et animations dessinés par une IA (géométrie générée par code) | règles de l'événement |

## 3. Taux d'achèvement du design (liste fermée, chaque point vaut 1)
| # | Point | État |
|---|---|---|
| 1 | Brief M1 : clair, verre léger, formes par état, grand mot d'état | ✔ validé par M1 |
| 2 | Inconnu ≠ normal ; jamais la couleur seule | ✔ testé |
| 3 | Données synthétiques étiquetées en permanence | ✔ testé |
| 4 | Événement critique en tête | ✔ |
| 5 | Données NASA réelles visibles et lisibles (panneau Habitat) | ✔ (mais sous la ligne de flottaison à 1280×900 : partiel côté « sans défiler longuement ») |
| 6 | Mouvement réduit respecté (logo et motion inclus) | ✔ |
| 7 | axe-core 0 violation (j3, 7, 9, 10 ; normal et réduit) | ✔ |
| 8 | Contraste mesuré sur pixels : 0 échec réel | ✔ |
| 9 | Tests verts (168) | ✔ |
| 10 | Logo C-Sync + motion | ✔ (proposition intégrée à la barre du haut ; déclaration IA faite ; filigrane : décision M1) |
| 11 | Test des 5 secondes, 3 à 5 personnes | ✘ |
| 12 | Photo du projecteur de la salle | ✘ |
| 13 | Fusion dans `main` | ✘ |
| 14 | Captures du deck C1–C5, PDF, pptx refaits | ✘ |
| 15 | App en ligne sur le design retenu | ✘ (suit `m3-design` + `signal`) |
| 16 | Silhouette humaine (décision M1) | ✘ |
**10 sur 16 = 62,5 % fait.** Le code et la mesure par outils sont finis ; ce qui manque dépend de personnes (test, photo, décisions) ou de la fusion. Ce taux ne dit rien de la qualité perçue : seul le test des 5 secondes le dira.

## 4. Ce qu'il ne faut pas faire
- Ne pas mettre l'insigne NASA (« meatball ») dans l'app ou les diapos : son usage est réservé et soumis à autorisation de la NASA (14 CFR 1221). Les mentions « NASA OSDR EDA », « NASA-STD-3001 » comme sources restent correctes.
- Ne pas écrire « capteur gelé », « validé », « diagnostic », « prouvé », « garanti ».
- Ne réécrire aucun commit publié ; `git pull --rebase` avant tout push.

## 5. Limites connues
- Les étoiles de la pierre sont très discrètes (opacité 0,1 à 0,55) : peut-être invisibles au projecteur ; c'est voulu (texte d'abord).
- Le logo animé rejoue peut-être à chaque interaction si Streamlit recrée la barre du haut : non vérifié dans un navigateur réel par une personne.
- « Planète + anneau » est un motif courant : le logo est une proposition, à confirmer par M1 et par le test.
