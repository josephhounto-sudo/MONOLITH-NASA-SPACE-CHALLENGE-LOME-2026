# Design « fusion » (Pleats + Monolith) — dimanche 15/11/2026 ~07:40 (Lomé = UTC)
FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ PAR DES PERSONNES. Branche `design-v2` (issue de `m3-design`). Choix de M1 à 06:55 : « une fusion entre le 1 et 3 ». Point de retour : `checkpoint-before-design`.

## 1. Ce que disent les 6 références de M1 (mesuré sur les pixels, k-means 6 couleurs, image réduite à 200 px)
| Référence | Pixels clairs (L>0,8) | Pixels sombres (L<0,2) | Couleurs dominantes |
|---|---|---|---|
| Halo orange flou | 92 % | 0 % | blanc #FEFEFE, orange #FE8423 |
| Plis lumineux (×2) | 77 % | 0 % | blanc lilas #F4ECF3, cyan #64DAF4, corail #F77256 |
| Affiche suisse rouge | 41 % | 0 % | rouge #A02921, blanc |
| Diagonales rouge-orangé | 67 % | 0 % | gris clair #E7E7E9, rouge-orangé #EA5A44 |
| Cage filaire + galet | 0 % | 3 % | sauge #626E71–#8C8E7F, bleu nuit #28344C |
**Constat** : 5 références sur 6 sont claires, sans aucun pixel sombre. Les 5 profils précédents (glass, quiet, hybrid, calm, signal) sont tous sur fond quasi noir `#05090B`, et `DESIGN_DIRECTION.md` §1 avait écarté « les fonds blancs ». C'est l'explication la plus probable du jugement « débutant » de M1. Les images ne sont pas versionnées ici (images de tiers) ; elles sont dans les Téléchargements de M1.

## 2. La fusion : un rôle par parent, pas une moyenne
| Parent | Apporte | Règle |
|---|---|---|
| 1 · Pleats (plis, halos) | le matériau : verre clair, plis blancs, champ chaud et champ froid | le **champ chaud** suit la criticité la plus haute du jour (calme 0,06 / surveillance 0,22 / critique 0,62) ; le **champ froid** = la liaison avec le sol |
| 3 · Monolith (cage, galet) | la signature : la cage filaire autour du galet (dans la barre du haut, statique) et la **pierre sombre** | la pierre n'enveloppe que ce qui exige d'agir maintenant (CRITICAL : urgence du jour 9, demande de reprise du jour 10). Test : `test_stone_surface_only_wraps_critical_screens` |
Autres choix : l'événement CRITICAL passe **avant** l'état de l'équipage ; une forme pleine par état (cercle, losange, triangle, carré pointillé) ; mot d'état en Clash Display ; texte en Satoshi (polices locales, licence Fontshare jointe dans `csync/ui/fonts/`, hors ligne) ; l'état inconnu (y compris « référence en construction ») est pointillé et en texte courant, jamais en grand.

## 3. Mesures (outils, pas jugement)
| Mesure | Résultat |
|---|---|
| `python -m pytest -q` | **158 verts** (153 + 5 nouveaux dans `tests/test_design_fusion.py`) ; `tests/test_ui.py` inchangé |
| axe-core 4 (WCAG 2.0/2.1/2.2 A+AA), jours 3, 7, 9 (étape 3), 10 (refus), mouvement normal et réduit | **0 violation** ; mais 5 à 24 nœuds « contraste incomplet » par jour (axe ne sait pas calculer sur dégradé/verre) |
| Contraste mesuré sur les pixels rendus (fond capturé sans texte, 5e centile, seuil 4,5 ou 3 pour le grand texte) | 0 échec ; minimum 6,55 (j3), 5,04 (j7), 5,10 (j9), 4,42 sur un grand titre (j10, seuil 3) |
| Jetons (`test_design_fusion.py`) | couleurs d'état sur verre clair ≥ 4,5:1 ; crème sur pierre ≥ 7:1 ; ambre, corail et cyan sur pierre ≥ 4,5:1 |
| Hiérarchie, premier écran 1280×900 (fait mesurable, pas goût) | profil `signal` : l'urgence (j9) et le refus de reprise (j10) **ne sont pas visibles** au premier écran ; fusion : visibles en premier. En contrepartie, au j9 les cartes d'état passent sous la ligne de flottaison |
Ce que ces mesures ne disent pas : si c'est beau, si c'est « futuriste », si ça passe au projecteur. Réponse : test des 5 secondes (`DESIGN_TEST_5S.md` §v2) et photo du projecteur de la salle.

## 4. Limites connues
- `.streamlit/config.toml` passe en base **claire** : les anciens profils sombres restent sélectionnables (`CSYNC_STYLE=signal`…) mais leurs contrôles natifs seront clairs ; remettre `base = "dark"` pour eux.
- L'application de test en ligne suit `m3-design` avec `CSYNC_STYLE=signal` : elle ne montre pas cette branche.
- Le bandeau « SYNTHETIC DATA » est neutre (plus d'ambre) : il reste affiché en permanence (testé).
- Captures du deck C1–C5, PDF, pptx : à refaire après fusion (IA de la session principale).
