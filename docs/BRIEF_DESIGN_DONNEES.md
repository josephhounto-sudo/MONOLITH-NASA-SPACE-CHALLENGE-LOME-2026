# À transmettre à la session de design — données NASA et crédibilité scientifique
FAIT PAR L'IA. Branche `nasa-data` (partie de `main`), **pas de CSS touché** : seul `habitat_panel()` a été ajouté à la fin de `csync/ui/app.py`, plus `csync/habitat.py`, `scripts/build_habitat.py`, `data/real/habitat_*.csv`, `tests/test_habitat.py`, et le thème sombre `.streamlit/config.toml` (identique à celui de `m3-design`).

## 1. Le constat de M1
« Cette interface ne ressemble pas à quelque chose que la NASA utiliserait ; ni le niveau médical ni le niveau scientifique ne sont prouvés. » Le jury cruel (`docs/JUGE_CRUEL.md`) note 2,6/5. La cause visuelle de départ : `main` n'avait pas de thème sombre.

## 2. Ce que l'écran doit montrer (ordre de lecture en 5 secondes)
1. **État du jour** : Body, Attention, Morale (formes distinctes par état, mot d'état en grand, jamais la couleur seule). Mission et Habitat : contexte, pointillés, jamais « normal ».
2. **Pourquoi** en une phrase, puis **action proposée**, puis « décision humaine : en attente ».
3. **Données réelles NASA**, à un endroit identifiable : le panneau Habitat (`habitat_panel`). C'est ce qui répond à « utiliser des données NASA ». Il doit être **visible sans défiler longuement** et lisible d'un coup d'œil :
   - la courbe CO2 réelle RR-1 en mmHg, la ligne de repère 3 mmHg (NASA-STD-3001), la zone de valeurs constantes marquée ARTIFACT (couleur d'état inconnu, pas couleur « normal ») ;
   - la phrase « CO2 constant à 2 646 ppm pendant 153 h : origine inconnue, jamais montré comme normal » ;
   - le tableau des 14 missions (12 ont des séries constantes), avec la mention d'origine EDA obligatoire.
4. Bandeau « DONNÉES SYNTHÉTIQUES » toujours visible pour tout ce qui concerne l'équipage.

## 3. Ce qu'il ne faut jamais écrire ou suggérer
- « validé par la NASA », « validé cliniquement », « diagnostic », « prouvé », « garanti » (le test refuse ces mots).
- « capteur gelé » pour le CO2 constant : **origine inconnue**.
- Que l'ISS dépasse sa limite de CO2 : le chiffre est une conversion approximative sur des capteurs d'installations rongeurs.
- Que les données NASA concernent un équipage : ce sont des télémétries de cabine.
- Tout chiffre non issu des fichiers du dépôt. Le panneau lit `data/real/habitat_*.csv`, reconstruits depuis le brut par `python scripts/build_habitat.py` et re-testés (`tests/test_habitat.py`).

## 4. Contraintes techniques à ne pas casser
- 162 tests verts (`python -m pytest -q`). `tests/test_ui.py` vérifie le balisage exact des cartes et que toute couleur vient de `csync/config/theme.json`.
- Aucune couleur en dur dans `app.py` ; textes dans `csync/config/strings_en.json` (clés `habitat_*`).
- axe-core : 0 violation (jours 7, 9, 10 ; mouvement normal et réduit) — vérifié sur cette branche.
- `st.html` retire le SVG en ligne ; `st.line_chart` accepte les couleurs du thème.
- Une zone riche à la fois : le panneau Habitat est une **section**, pas un fond animé.

## 5. Autres demandes de M1 pour le design
- Brief écrit prioritaire : futuriste, verre léger, formes, mot d'état en grand. Références : dossier Téléchargements de M1.
- Silhouette humaine : absente de l'application (voir `docs/HANDOFF_TOTAL.md` §6) ; à décider avec M1.
- Après le choix du design : captures du deck C1–C5 à refaire pour qu'elles ressemblent à l'écran réel.

## 6. À livrer par la session de design
Branche, fichiers modifiés, résultats `pytest` et axe, et trois captures (jours 7, 9, 10) **avec le panneau Habitat visible**.
