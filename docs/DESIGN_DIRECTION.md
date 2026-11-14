# Direction artistique « Monolith Glass » — v1, samedi 14/11/2026 17:15 UTC
FAIT PAR L'IA À PARTIR DES RÉFÉRENCES DE M1 — À VALIDER PAR M1. Branche `m3-design` (pas encore dans `main`).

## 1. Ce que disent les références de M1 (10 images, Pinterest / Designspiration)
| Référence | Ce qu'on en retient | Où c'est dans l'app |
|---|---|---|
| Planches de formes géométriques (monolignes et pleines, crème sur anthracite) | un vocabulaire de formes simples : polyèdre, anneaux, points, lignes fines | fond animé : `.poly`, `.rings`, `.dots`, `.lines` |
| Cristal filaire autour d'un galet bleu nuit, sur dégradé feutré | le « monolithe » : une forme sombre protégée par une cage filaire (écho du logo MONOLITH) | polyèdre filaire + galet bleu, en haut à droite |
| Dégradés flous orange / rouge / cyan avec fines lignes blanches courbes (style Apple) | halos de lumière doux et traits très fins | halos `.blob` bleu, cyan et un chaud discret, lignes courbes |
| Affiche suisse rouge à formes franches | composition franche, aplats, grille nette | cartes d'état à bord net, grille de 5 |
Non repris : le rouge plein (réservé à l'alerte), les fonds blancs, les motifs chargés (le texte doit rester lisible).

## 2. Les règles (issues des sources, section 4)
1. **Trois couches** (règle Apple) : fond profond ; contenu sur matériau épais (≈ 82 % opaque, flou 10 px) ; couche fonctionnelle (barre du haut, bandeau, curseur, boutons) en verre dépoli plus léger (≈ 55 %, flou 14 à 16 px). Pas de verre sur le texte courant : le texte est lisible avant d'être joli.
2. **Couleurs** : bleu de confiance (`#2F7FD8`, `#6FB1F0`) uniquement pour le fond et le « chrome » ; cyan `#00E0F5` = interaction ; vert / ambre / corail = états seulement (inchangés) ; le chaud du fond reste à moins de 30 % d'opacité.
3. **Jamais la couleur seule** : chaque état garde son icône et son mot ; les cartes « contexte » sont en pointillés et atténuées.
4. **Mouvement lent** : boucles de 70 à 240 s, transformations et opacité seulement, rien ne bouge sous le texte à plus de 4 vw. Tout s'arrête avec `prefers-reduced-motion`.
5. **Repli** : sans `backdrop-filter` ou avec `prefers-reduced-transparency`, les panneaux deviennent opaques.
6. **Contrastes mesurés** (texte sur panneau `#0E161B`) : texte 16:1, texte secondaire 7,7:1, cyan 11,3:1, vert 9,9:1, ambre 8,8:1, corail 6,5:1, gris « inconnu » 6,2:1 (seuil visé 4,5:1).
7. **Hors ligne** : polices système uniquement, aucune image ni police chargée sur Internet ; les formes sont des SVG intégrés au CSS.

## 3. Ce qui a été construit (branche `m3-design`)
`.streamlit/config.toml` (thème sombre natif) · `csync/ui/style.py` (tout le CSS et les formes, couleurs lues dans `theme.json`) · `theme.json` (bloc `design`) · `app.py` (cartes, kicker, panneaux ; aucune couleur en dur) · 137 tests verts, dont les écrans des jours 7, 9 et 10.

## 4. Sources
- Apple Human Interface Guidelines, *Materials* : https://developer.apple.com/design/human-interface-guidelines/materials (verre pour la couche fonctionnelle, pas pour le contenu ; matériaux standards pour le contenu ; couche d'atténuation ; réglages de transparence réduite).
- Axess Lab, *Glassmorphism Meets Accessibility* : https://axesslab.com/?p=5111 (contraste 4,5:1 texte, 3:1 grands éléments ; calque semi-opaque derrière le texte ; éviter un flou ≥ 20 px ; respecter `prefers-reduced-transparency` et `prefers-reduced-motion`).
- Format DESIGN.md (9 sections : ambiance, palette, typographie, composants, mise en page, profondeur, faire / ne pas faire, responsive, guide pour agents) : https://github.com/VoltAgent/awesome-design-md et https://github.com/VoltAgent/awesome-claude-design (68 fichiers de marques, dont Apple, Linear, Vercel, SpaceX).
- Interface tactile de Crew Dragon (affinage des touches avec les astronautes ; mode manuel de secours) : https://www.space.com/spacex-crew-dragon-touchscreen-astronaut-thoughts.html . L'article ne parle ni de thème sombre ni de simplicité : ce sont nos choix, pas les siens.

## 5. Décisions pour M1
| # | Question | Recommandation |
|---|---|---|
| A1 | Fusionner `m3-design` dans `main` ? | Oui avant 18:00 si la direction te convient |
| A2 | Refaire les captures C1 à C5 du deck, PDF et pptx de secours (~20 min) ? | Oui : sinon la démo en direct ne ressemblera pas aux diapos 3 à 5 |
| A3 | Icône des cartes « contexte » : `?` (aujourd'hui, identique à « inconnu ») ou `○` ? | `○` : change 3 tests et `theme.json`, 10 min ; non fait sans ton accord |
| A4 | Garder le polyèdre filaire (monolithe) comme signature ? | Oui, c'est l'écho du logo ; il peut être masqué par `prefers-reduced-motion` |
| A5 | Page d'accueil hors démo (écran d'entrée) ? | Non avant le gel |
