# Tâches Cursor — lot 2 (19/11/2026, avant midi UTC)

Budget: 24 $ restants au 18/11 à 21:20 (dashboard cursor.com). Arrêter dès 14 $ restants et rendre compte. Mode Agent local, branche `cursor-v3` depuis `v2` (pas `v2` directement).
Propriété: Cursor = nouveaux fichiers `csync/ui/theme_dark.py`, `scripts/`, tests de ces fichiers. Claude = `csync/ui/style.py`, textes, histoire. `AGENTS.md`, `contracts/`, histoire gelée: intouchables. Le gel du 14/11 ne s'applique pas à v2 (décision Joseph, 18/11).

## K1 — Thème sombre rendu et mesuré (la plus grosse, ~8 $ max)
Critère: `?theme=dark` dans l'URL affiche l'app en sombre sans modifier le thème clair par défaut; `python scripts/measure_contrast.py` à 1400, 1000 et 390 px sur le jour 7 donne zéro ligne sous le seuil écrit; trois captures PNG commitées dans `docs/captures/`.
5 échecs à tester d'abord: paramètre absent (clair par défaut); valeur inconnue; mot d'état sur dégradé; page mobile; recharge Streamlit qui perd le paramètre.
Couleurs de départ: `scripts/propose_dark_theme.py` (fond #14181F). Style: règles « unslop » ci-dessous.

## K2 — Artefact de mesure à 390 px (~3 $)
Au jour 7 mobile, « Attention ▲ Degraded » sort à 1,71:1 alors que le même mot est à 4,3+ à 1000 px. Trouver si c'est le script (cadrage) ou la page; corriger le script ou signaler le vrai défaut avec la capture.

## K3 — Contrôle de non-régression (~1 $)
`python -m pytest -q` + `python scripts/compare_strings.py` + `tests/test_section_use.py` verts; rendre la sortie brute.

## Règles de design à appliquer (d'après heydamir/unslop, CC BY 4.0, © Damir Sokolovsky, github.com/heydamir/unslop)
Neuf passes dans l'ordre: espacement (grille 4 px, éléments égaux = tailles égales), couleur (neutres d'une seule rampe, un seul accent, pas de dégradé/lueur/ombre colorée), icônes (un seul jeu), texte (faits de la page seulement, pas de ton publicitaire), typo (poids 400–500, casse normale), mise en page, détails (rayons emboîtés, cartes de chiffres sans mini-graphe), visuels (pas d'orbes décoratifs), mouvement (pas de boucle ni de pulsation).

## À rendre
`docs/RAPPORT_CURSOR.md` (15 lignes): fait / VERIFIED avec sortie brute / UNVERIFIED / ce qui peut casser / comment annuler.
