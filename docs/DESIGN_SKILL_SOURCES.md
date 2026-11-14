# Skill de design C-Sync — sources, principes, preuves (14/11/2026 20:50 UTC)
FAIT PAR L'IA — À VALIDER PAR M1. Branche `m3-design`, rien dans `main`. Aucun jugement visuel de l'IA : le test final est humain (`docs/DESIGN_TEST_5S.md`).

## 1. Sources lues (fichiers réels)
| Source | Ce que c'est, vérifié dans les fichiers | Licence |
|---|---|---|
| `github.com/heydamir/unslop`, commit `97daa3e` (09/11/2026), cloné | Skill pour Claude Code / Codex (`skills/unslop/SKILL.md`, 31,6 ko ; `references/signs.md`, `tokens.md`, `visuals.md`, `effects.md` ; scripts `snapshot.mjs`, `story.mjs` ; tests Node). Méthode : écrire une « direction » en 5 lignes, auditer les « signes de slop », corriger en 9 passes (espacement, couleur, icônes, texte, typo, mise en page, détails, visuels, mouvement), vérifier avec une liste. | CC BY 4.0 (`LICENSE`, `CITATION.cff`, en-tête du SKILL.md). Adaptation permise avec mention de l'auteur : **Damir Sokolovsky (@heydamir)**, https://heydamir.design/unslop. Aucun code copié ici : seulement des principes reformulés. |
| Portfolio de M1, https://portfolio.josephhounto.workers.dev/ — lu dans le navigateur (`/style.css` 47,9 ko, `/script.js` 20,8 ko) | Jetons dans `:root` (couleurs `--ink`, `--primary`, espacement `--sp-xxs…huge` de 2 à 64 px, rayons `--r-xs…xl`, durées `--dur-fast 140ms`, `--dur-med 220ms`) ; l'en-tête du CSS dit « derived from VoltAgent/awesome-design-md (design-md/stripe/DESIGN.md) » et « emil-design-eng » pour le mouvement ; 13 blocs `prefers-reduced-motion` ; introductions jouées une fois par session (`sessionStorage`) et supprimées si mouvement réduit ; apparition au défilement par `IntersectionObserver` ; flou de verre limité à 8–18 px. | Aucune licence trouvée : c'est le travail de M1. **Dépôt GitHub du portfolio : introuvable** (la page ne lie que `github.com/josephhounto-sudo`, que je ne peux pas lister). |
| Non lus : `emil-design-eng`, `VoltAgent/awesome-design-md` (fichier Stripe) | cités par le CSS du portfolio ; je n'ai ouvert ni l'un ni l'autre dans cette passe. | non vérifiée |

## 2. Huit principes retenus (chacun relié à une règle de `docs/DESIGN_DIRECTION.md` §2)
| # | Principe | Source | Règle DD |
|---|---|---|---|
| P1 | Écrire la direction en 5 lignes avant de toucher (produit, caractère, monde, moments, signature) ; mots interdits : propre, moderne, premium | unslop « Direction » | §1 (références) |
| P2 | Une seule zone riche (les cartes d'état et la décision) ; tout le reste est calme | unslop « What good looks like » | R1 (trois couches) |
| P3 | Une rampe de neutres, trois rôles de texte, un accent (cyan) ; couleurs d'état réservées aux états | unslop « Color » ; portfolio (`--ink`, `-secondary`, `-mute`) | R2, R6 |
| P4 | Espacement sur grille de 4 px ; choses égales = tailles égales ; l'espace intérieur d'un groupe < espace entre groupes | unslop « Spacing » ; portfolio (`--sp-*`) | non couverte → à ajouter |
| P5 | Texte : casse normale, deux graisses, chiffres tabulaires, pas d'interlettrage négatif en petit | unslop « Type » | non couverte ; **contredit** le kicker en majuscules |
| P6 | Une seule source de valeurs : `theme.json` / variables CSS, aucune couleur en dur | portfolio (`:root`) ; test `test_no_hardcoded_colours_in_app` | R7 |
| P7 | Le mouvement explique, il ne décore : propriétés nommées, une courbe, repli `prefers-reduced-motion` partout | unslop « Motion » ; portfolio | R4, R5 |
| P8 | Jamais la couleur seule ; l'inconnu ne ressemble jamais au normal (carte pointillée, icône + mot) | propre à C-Sync, pas des sources | R3 |
**Écartés** : vidéo d'histoire (`story.mjs`), génération d'image pour le hero, règles de page d'accueil, Tailwind, bouton blanc cassé, ressorts à dépassement du portfolio (unslop les interdit ; ils n'existent pas dans C-Sync).

## 3. Conflit à trancher (honnête)
unslop interdit : halos flous, formes décoratives (« orbs, nebulas, floating cubes, glowing grids »), verre (« do not swap one trend for another like glass »), étiquettes en majuscules espacées, mouvement en boucle. **Monolith Glass, tel que construit, fait exactement ces choses** (halos, polyèdre, anneaux, points, lignes, verre, kickers en majuscules, 7 animations de fond). Le skill ne peut donc pas être « Monolith Glass + unslop » sans choisir. Deux profils existent, même markup, CSS seul : `CSYNC_STYLE=glass` (défaut, inchangé) et `CSYNC_STYLE=quiet` (principes P2, P3, P5, P7 appliqués : fond plat, un seul signe gardé — le polyèdre, fixe —, cartes pleines à filet fin, étiquettes en casse normale). Choisir = décision de M1, avec le test des 5 secondes.

## 4. Preuves mesurées (outils, pas jugement)
| Mesure | A · glass | B · quiet |
|---|---|---|
| axe-core 4.x (WCAG 2.0/2.1/2.2 A+AA), jours 7, 9, 10, mouvement normal et réduit | 0 violation | 0 violation (après correction) |
| Lighthouse accessibilité | 100 | 100 |
| Lighthouse bonnes pratiques | 100 | 100 |
| Animations de fond actives, mouvement normal → réduit | 7 → 0 | 0 → 0 |
| Contrastes sur le panneau `#0E161B` | texte 16,0 · secondaire 7,7 · cyan 11,3 · normal 9,9 · watch 8,8 · degraded 6,5 · unknown 6,2 (inchangés) | idem |
| Tests | 153 passent | 153 passent |
Défaut réel trouvé et corrigé (les deux profils) : les légendes Streamlit (« Human decision: pending », « Capsule file not found… ») étaient rendues à 3,58:1 (couleur correcte mais `opacity` du conteneur). Corrigé dans `csync/ui/style.py`. Axe ne pouvait pas mesurer ce cas sur le fond dégradé du profil A (résultat « incomplet »), donc « 0 violation » en A est moins fort qu'en B.
**Lighthouse performance : 30 (A) et 31 (B)**, LCP ≈ 16 s, CLS ≈ 0,27. Ces chiffres viennent de Streamlit lui-même sous la limitation mobile simulée de Lighthouse sur ce serveur ; ils ne départagent pas les deux profils et ne disent rien du portable de démo. Non utilisé comme preuve.

## 5. Ce que je n'ai pas pu vérifier
- L'effet sur de vraies personnes (test des 5 secondes à faire passer).
- Le rendu sur le projecteur et le portable de démo (coût du flou, luminosité).
- Le dépôt GitHub du portfolio, `emil-design-eng`, le fichier Stripe de `awesome-design-md`.
- Le skill n'a pas été testé sur un autre projet que C-Sync.
- Les captures C1–C5 du deck ne correspondent à aucun des deux profils.
