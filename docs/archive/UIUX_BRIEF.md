# Brief design UI/UX — samedi 14/11 15:50 UTC (gel des fonctionnalités : 18:00)
Qui : M1 (design), après la session Cursor. À ne pas faire en même temps que Cursor sur `csync/ui/app.py` (E1 y modifie des fichiers) : attendre sa pull request ou travailler sur une branche `m3-design` et rebaser.
Périmètre : apparence et lisibilité seulement. Pas de nouvelle fonction, pas de changement du moteur ni des textes qui portent un sens (états, raisons de refus, bandeau SYNTHETIC DATA). Couleurs : `csync/config/theme.json` ; textes : `csync/config/strings_en.json`. Pas de carte du corps dans l'app (D5).

## Constat sur la capture C1 (jour 7)
1. Fond de page **clair** (thème Streamlit par défaut) alors que `theme.json` définit un fond sombre `#05090B` : cartes sombres sur page blanche, deux identités visuelles. Le deck, lui, est sombre.
2. Curseur « Mission day » en rouge par défaut : le rouge est réservé à DEGRADED dans nos états ; un curseur rouge brouille le sens.
3. Cartes de hauteurs inégales : « Mission » et « Habitat » sont plus hautes (« Context only — not evaluated » passe sur 2 lignes). À égaliser.
4. « Context only — not evaluated » est précédé d'un « ? », le même symbole que UNKNOWN : confusion possible entre « non évalué » (contexte) et « inconnu » (donnée absente).
5. Le titre (« 2 dimension(s) away… ») est le message principal mais reste en taille proche des cartes ; la hiérarchie est plate.

## Corrections proposées (ordre de priorité, toutes dans le périmètre)
| # | Correction | Où | Effort |
|---|---|---|---|
| 1 | Thème sombre natif : `.streamlit/config.toml` avec `base="dark"`, `backgroundColor`, `secondaryBackgroundColor`, `textColor`, `primaryColor` repris de `theme.json` | nouveau fichier | 10 min |
| 2 | Curseur et boutons en `primaryColor` = cyan `#00E0F5` (couleur « interactive »), plus de rouge hors DEGRADED | même fichier | inclus |
| 3 | Hauteur minimale commune des cartes de dimension ; libellé court pour le contexte : « Context » avec icône « · » ou « ○ » (pas « ? ») | `app.py` carte | 15 min |
| 4 | Titre d'état plus grand que les cartes ; sous-titre en gris secondaire | `app.py` | 10 min |
| 5 | Écran Action : une seule action primaire visible par étape (« Next »), « Previous » en secondaire | `app.py` | 15 min |
| 6 | Écran Reprise : raison du refus en premier plan (carte DEGRADED), boutons dessous | `app.py` | 15 min |

## Règles de contrôle (accessibilité, simples)
- Jamais la couleur seule : chaque état garde son icône et son mot (déjà le cas).
- Contraste du texte secondaire `#9AABB1` sur `#0E161B` : à vérifier ≥ 4,5:1 avant de le garder pour du texte courant.
- Après chaque changement : relancer l'app, reprendre les captures C1 à C5 uniquement si le rendu change ; sinon ne pas toucher au deck (le deck embarque les captures actuelles).
- `python -m pytest -q` vert, y compris les tests d'interface et de mots interdits.

## Risque à connaître
Changer l'apparence après que les captures du deck sont figées crée un écart entre démo en direct et diapos 3 à 5. Soit on refait les captures (`pitch/deck/crop_captures.py`, `embed_captures.py`, exports PDF/pptx, ~15 min), soit on garde l'ancien rendu pour les diapos et on le dit. À décider avant 18:00.
