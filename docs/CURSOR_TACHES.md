# Tâches pour Cursor (à coller une par une dans le chat de l'agent)

Préparé le 18/11/2026. Ouvre le dépôt sur la branche `v2`, mode Agent. Les règles de `.cursor/rules/csync.mdc` s'appliquent. Chaque tâche finit par `python -m pytest -q` vert.

## 1. Code mort (le plus utile pour réduire l'erreur)
« Installe vulture (`pip install vulture`) et lance-le sur `csync/` avec `--min-confidence 80`. Pour chaque fonction ou module signalé, dis qui l'appelle. Supprime seulement ce qu'aucun point d'entrée n'atteint (app, scripts, tests de recherche) et montre-moi la liste avant de supprimer. Cas connus: `csync.memory`, `glyphs`, `sendqueue`: ne pas supprimer sans me demander. »
Réussite: liste signalée + justification par élément; tests verts après suppression.

## 2. Parité EN/FR des textes
« Compare `csync/config/strings_en.json` et `strings_fr.json`: clés manquantes d'un côté, valeurs identiques (non traduites), phrases qui disent autre chose en français qu'en anglais. Corrige le français, pas l'anglais. Pas de nouvelle clé sans sa jumelle. »
Réussite: script de comparaison qui sort 0 écart; aucune phrase médicale modifiée.

## 3. Contraste mesuré sur pixels (thème sombre)
« Écris `scripts/measure_contrast.py` qui ouvre l'app avec Playwright (1400, 1000, 390 px de large), capture, et calcule le rapport de contraste WCAG du texte contre le fond réel pour: corps, légendes, mots d'état. Seuils: 4,5:1 le corps, 7:1 les légendes de moins de 14 px. Sortie: tableau par largeur. Ne change aucune couleur: mesure seulement. »
Réussite: tableau reproductible; liste des éléments sous le seuil.

## 4. Mur de texte « Why this view »
« Dans `csync/ui/app.py`, la fonction `nominal` affiche toute l'explication en un paragraphe. Sépare-la en: une phrase de verdict, une ligne par indicateur signalé (valeur, normale de la personne, fois la variation habituelle), et la règle repliée dans un expander. Ne change pas `csync/capsule.py` ni le contrat. Les tests existants doivent rester verts. »
Réussite: capture à 1400 et 390 px: pas de paragraphe de plus de 3 lignes.
