# Protocoles anti-périmé (valables pour tous : humains et IA) — version 1, 14/11/2026 06h15
Problème à ne plus revivre : un bloc ou une fiche qui cite un fichier absent, une valeur dépassée, un planning remplacé.
**Règle d'or : on ne recopie jamais à la main ce qui peut se générer ou se vérifier par un script.**

| N° | Protocole | Comment |
|---|---|---|
| P1 | **Source unique** | Le dépôt Git est la vérité pour le code, les contrats, les fiches (`docs/team/tasks.json`) et les décisions (`docs/OPEN_DECISIONS.md`). Le Drive, le Parcours et les blocs sont des COPIES. En cas de doute : le dépôt, puis le programme officiel (`docs/PROGRAMME_OFFICIEL.md`). |
| P2 | **En-tête obligatoire** | Tout document partagé commence par : `Version · date/heure (Lomé) · Statut : BROUILLON / VÉRIFIÉ / OBSOLÈTE · Remplace : …`. Sans en-tête, il est considéré périmé. |
| P3 | **Les blocs d'IA se génèrent** | `python scripts/build_blocks.py` régénère le bloc de code depuis le dépôt et inscrit le numéro de commit en tête. Jamais de bloc rédigé à la main après le premier envoi. |
| P4 | **Mises à jour numérotées** | Toute correction envoyée à une IA commence par `MISE À JOUR n°X` et est inscrite dans `docs/MAJ_LOG.md` (date/heure, ce qui change, commit). L'IA confirme en une phrase. |
| P5 | **Contrôle avant envoi** | `python scripts/check_consistency.py` doit afficher `0 erreur` avant d'envoyer un bloc, une fiche ou un zip. Il vérifie les tests, l'alignement des valeurs provisoires, les liens, les mots interdits, la vie privée et l'âge des blocs. |
| P6 | **Âge visible** | L'annonce en haut du Parcours affiche son âge. Plus de 6 h sans mise à jour : elle passe en « à revérifier » et personne ne s'y fie sans demander à M1. |
| P7 | **Deux statuts de preuve** | « Vérifié » = exécuté et résultat observé. « Non vérifié » = produit par une IA ou une personne, pas relu ni testé. Tout livrable d'IA est « non vérifié » jusqu'à `pytest` vert chez un humain ET relecture M1. |
| P8 | **Obsolète = marqué** | Un document remplacé reçoit en première ligne « OBSOLÈTE — remplacé par X » et part dans `PRIVATE/ARCHIVE` du Drive. On ne supprime rien sans confirmation de M1. |
| P9 | **Une décision, un horodatage** | Quand M1 change une décision (`OPEN_DECISIONS.md`), il la date ; tout bloc dépendant est régénéré (P3) et une MAJ (P4) part. |
| P10 | **Les heures viennent d'un seul fichier** | `docs/PROGRAMME_OFFICIEL.md`. Aucune autre page ne redonne un horaire sans le citer. |
| P11 | **L'IA dit ce qu'elle ne voit pas** | Une IA qui découvre un fichier cité mais absent, une incohérence ou une valeur douteuse le signale AVANT de travailler (comme l'a fait le Claude de M2–M4 ; c'est la bonne pratique). |
| P12 | **Revue indépendante** | Un résultat chiffré important est relu par une autre IA ou un autre humain avec le code (pas seulement le compte rendu). |
