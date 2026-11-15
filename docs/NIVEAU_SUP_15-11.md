# Relever le niveau — grille jury, défense médicale, test des 5 secondes (15/11, 13:00 UTC)
FAIT PAR L'IA — À VALIDER PAR M1. Critères annoncés : Impact, Créativité, Validité, Pertinence, Présentation (`docs/PROGRAMME_OFFICIEL.md`, mise à jour à venir).

## 1. Ce que chaque diapo apporte à chaque critère (preuve vérifiable, pas un slogan)
| Critère | Diapo | Preuve dans le dépôt |
|---|---|---|
| Impact | 1, 2 | Délai jusqu'à 22 min (NTRS 20220013418) ; quatre volets avec statut honnête (fait / prototype / prévu) |
| Créativité | 2, 3, 4 | Un seul code de formes dans l'app et le deck (`csync/glyphs.py` : cercle normal, losange surveillance, triangle dégradé, carré tireté inconnu) ; l'inconnu n'est jamais affiché comme normal |
| Validité | 5, 6 | 0/300 sains déclenchent, 139/150 dérives progressives, 86/150 brusques sur graines jamais utilisées pour régler (`research/pilot/holdout_results.json`) ; test `tests/test_deck_shapes.py` |
| Pertinence | 3, 4, 5 | Hors ligne, ligne de base personnelle, porte de reprise : exactement « décider loin du sol » |
| Présentation | toutes | Fond sombre unique, une idée par diapo, captures réelles de l'app, 7 diapos, ≤ 25 mots |

## 2. Ce qu'un médecin du jury peut attaquer, et la réponse exacte (sans promesse hors preuve)
| Attaque | Réponse |
|---|---|
| « Données synthétiques : donc rien de prouvé » | Oui, et c'est écrit sur chaque capture. Le chiffre mesure le comportement de la règle, pas une validité clinique. Suite : revue d'experts, puis essai sur données d'isolement simulé. |
| « 1,5 écart-type, pourquoi ? » | Seuil réglé sur graines 1000–7149, puis vérifié sans réglage sur 30000–37149 : 0/300 faux, 92,7 % et 57,3 %. Choix arbitraire assumé, borne d'incertitude publiée (`docs/VALIDATION_HOLDOUT.md`). |
| « Zéro faux déclenchement ? » | 0/300 sur un jeu, 4/200 (2,0 %) sur un autre : « de 0 à 2 % selon les équipages simulés ». |
| « Votre point faible ? » | Les changements brusques : 57,3 %, parce que la règle attend deux jours. C'est dit sur la diapo 6 et dans le dépôt. |
| « Que fait-il pour une douleur thoracique ? » | Il ouvre une procédure fixe, guide les mesures une à une avec leur source, met le rapport en file. Il ne propose ni traitement ni dose ; il renvoie à la liste de contrôle médicale de bord et à l'officier médical. |
| « Les fiches sont validées ? » | Non : non validées par un médecin (relecture M4 en attente). Ne jamais dire « validé cliniquement ». |

## 3. Test des 5 secondes (la seule preuve qui ne vient ni de toi ni de moi)
À faire avec **deux personnes hors équipe**, dont une du milieu médical, avant de soumettre :
1. Montrer chaque diapo 5 secondes, puis la cacher. Demander : « Qu'est-ce que ça fait ? Qu'est-ce que ça ne fait pas ? »
2. Noter mot pour mot. Attendu : « surveille la santé loin de la Terre », « l'humain décide », « données simulées ».
3. Si une personne dit « il soigne » ou « il remplace le médecin », corriger la diapo (pas la personne).
4. Noter les réponses ici : `docs/NIVEAU_SUP_15-11.md`, section 4.

## 4. Résultats du test des 5 secondes
(à remplir par M1 : date, personne, réponses.)

## 5. Contrôles faits par l'IA
Deck EN/FR : tests verts ; captures régénérées depuis l'app courante (C1–C6) ; glyphes identiques app/deck ; 211 tests ; axe 0 violation (à relancer après ce commit : `/tmp/axe_tabs.py` n'est pas dans le dépôt).
