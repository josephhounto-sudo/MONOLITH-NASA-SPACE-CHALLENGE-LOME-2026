# Prompts prêts à coller — 19/11/2026

## Cursor (modèle choisi à la main, pas Auto) — 1 requête par bloc, ordre: changepoint, signature, CRDT, HRV, audit
```
Lis AGENTS.md puis docs/CONTRACTS_TECH.md en entier. Branche: tech-modules (crée-la depuis glass-navy). 
Implémente UNIQUEMENT le module <NOM> décrit dans la section correspondante, avec ses tests, tests écrits d'abord.
Interdits: modifier csync/ui, csync/rules.py, csync/gate.py, contracts/, tout fichier hors de ceux listés pour Cursor.
Respecte les signatures exactes. Jeu de réglage et jeu de contrôle séparés, écrits dans le test.
Termine par: pytest -q, ruff check csync tests, puis un rapport de 5 lignes (quoi / vérifié comment / non vérifié / ce qui peut casser / comment annuler).
Ne commit pas sur main. Message: "TECH: <module>".
```
Requête d'audit (dernière): « Sur les trois premiers modules, écris des tests de propriétés et de mutations qui échouent si on change un seuil, un signe ou un ordre; ne modifie pas le code des modules, signale-le seulement. »

## ChatGPT (recherche sourcée, markdown, pas de code)
```
Contexte: app de démonstration NASA Space Apps (suivi de dérive de l'état d'un équipage, données SIMULÉES). 
Donne-moi, dans un fichier markdown, avec UNE URL cliquable à côté de CHAQUE affirmation:
1) Jeux de signaux cardiaques candidats (PhysioNet ou autres): nom exact, licence exacte, accès libre ou habilité, conditions de réutilisation, URL de la page officielle.
2) Références primaires: RFC 9171 (Bundle Protocol v7), Page 1954 (CUSUM), Task Force ESC/NASPE 1996 (variabilité cardiaque), un article de référence sur les CRDT.
3) Pour chaque référence: ce qu'elle établit, en une phrase, sans extrapoler.
Si tu ne trouves pas la page officielle, écris NON TROUVÉ. N'invente aucune licence, aucun chiffre, aucune URL.
```
Livrable à placer dans research/tech/licences.md. Claude vérifie chaque URL avant usage.

## Gemini (lecture longue, rapport uniquement, ne corrige pas)
```
Je te donne le dépôt (zip ou contenu). Produis un rapport markdown, sans modifier de code:
A) Fichiers morts, imports que aucun point d'entrée n'atteint, fonctions jamais appelées (chemin:ligne).
B) Phrases des textes affichés ou des docs qui promettent ce que le code ne fait pas (citation courte + fichier).
C) Contradictions entre docs (chiffres, états, dates).
D) Sur csync/analytics/changepoint.py (quand fourni): circularité entre jeu de réglage et jeu de contrôle.
Pour chaque point: fichier, ligne, gravité (bloquant / gênant / mineur). Si tu n'es pas sûr, écris INCERTAIN.
```
Livrable à placer dans research/review/. Lecture froide séparée: donner à Gemini le texte rendu extrait du DOM, avec les six questions fermées du protocole design-master; préciser que c'est un lecteur IA, pas un humain.
