# Règle personnelle contre seuils fixes (hypothèse H2) — sensibilité, pas validation

FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ PAR UN TIERS. Équipages SYNTHÉTIQUES (générateur csync-synth-0.1, variante histoire, drift_amp=1.5, graines 65000–65149, jamais utilisées pour régler la règle).

Script: `research/fixed_vs_personal.py`. Sortie brute: `research/fixed_vs_personal_results.json`. Tests: `tests/test_fixed_vs_personal.py`.

## Question
Une règle à seuils fixes de population voit-elle aussi tôt la dérive qu'une référence personnelle, sans fausses alertes ?

## Seuils fixes (tirés de textes publiés, jamais réglés ici)
- Sommeil < 7 h: consensus AASM et SRS, Watson et al. 2015 (les adultes devraient dormir 7 h ou plus).
- Lapses du PVT-B ≥ 11: Basner et Rubinstein (PVT de 3 min, seuil 355 ms; 11 et 20 lapses séparent des niveaux de performance en dépistage de bagages). Contexte aéroportuaire, pas spatial: c'est un seuil d'altération marquée, pas de dérive précoce.
- Même persistance que la règle personnelle (2 jours de suite); la procédure s'ouvre quand deux indicateurs sont dehors (règle C), ou sur le sommeil seul (règle D). Jours 6 à 10.
- Aucun seuil de population sourcé n'existe dans le dépôt pour la fréquence cardiaque, le temps de réaction moyen ou le moral: ces indicateurs ne sont pas comparés.

## Facteur d'écart entre personnes (f)
Le générateur livré donne la même personne à tous les équipages (f = 0). Aucune valeur réelle de f n'est sourcée ici. Le balayage fait varier la référence de sommeil de f × 0,45 h et le temps de réaction de f × 10 ms (écarts-types).

## Résultats (150 équipages dérivants, 150 sains par ligne)
| f | A personnelle (tout) | B personnelle (2 indicateurs) | C fixe (sommeil + lapses) | D fixe (sommeil seul) |
|---|---|---|---|---|
| 0, détection | 97,3 % | 86,7 % | 22,0 % | 100 % |
| 1 | 97,3 % | 84,0 % | 30,0 % | 100 % |
| 2 | 87,3 % | 65,3 % | 29,3 % | 100 % |
| 3 | 84,7 % | 56,7 % | 35,3 % | 100 % |
Fausses alertes sur équipages sains: A 0,7 / 0 / 0 / 0,7 % ; B 0 % partout ; C 0 / 0 / 0 / 4,7 % ; D 18,0 / 32,7 / 40,0 / 44,7 %.
Jour médian de première ouverture (équipages détectés): A 7–8; B 8; C 8–9; D 7 (6 à 7 chez les sains).

## Lecture honnête
- À comparaison égale (B contre C, mêmes indicateurs et même persistance), la règle personnelle détecte plus, à tous les écarts testés, sans fausse alerte notable. L'écart se réduit quand f augmente (56,7 % contre 35,3 % à f = 3).
- Le sommeil seul sous 7 h (D) voit aussi vite (jour 7) mais déclenche chez 18 à 45 % des équipages sains: il ne distingue pas une nuit courte d'une dérive.
- Le seuil de lapses de C est un seuil d'altération marquée: il arrive tard par construction. Le comparer à une règle de dérive précoce n'est pas équitable pour lui.
- Le générateur impose au sommeil de passer sous 5,9 h pendant la dérive quelle que soit la personne (valeur absolue): cela favorise les règles fixes, pas la règle personnelle.
- Circularité: le générateur et la règle personnelle ont été conçus ensemble (écarts-types intra-personne). Ce test mesure la règle sur son propre monde simulé, plus un écart entre personnes inventé. Seules des données réelles d'équipage ou d'analogue trancheraient.

## Ce qui ferait abandonner l'argument
Des données réelles où l'écart entre personnes est faible et où un seuil fixe voit aussi tôt sans fausses alertes. Ou un relecteur expert qui conteste le choix des seuils fixes.
