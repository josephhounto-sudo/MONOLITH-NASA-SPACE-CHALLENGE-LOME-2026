# FICHIER: pitch/deck/SCRIPT_FR.md
Date/heure : sam. 14/11/2026 ~15:00 UTC · Version v4 (15/11 : diapo 6 sur les graines tenues à l'écart, VALIDATION_HOLDOUT.md) · v3 (D6 orateurs ; formulations absolues adoucies : « jamais » remplacé par ce que le code fait réellement)
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

Pitch oral en français, 5:00 exactes, **sans questions du jury** (`docs/PROGRAMME_OFFICIEL.md`). Diapositives : `deck.html`. Démo en direct : Acte 3 (diapo 5).
Débit visé : 130 à 145 mots par minute. Les comptes de mots ont été faits par script sur le texte entre guillemets ; voir le tableau à la fin.
Rôles (décision D6, 14/11) : orateur A = M1 (diapos 1, 2, 3, 6, 7 = 190 s) ; orateur B = M2 (diapos 4 et 5 = 110 s, dont la démo). Aucun nom dans ce fichier.

---
## Diapo 1 · 0:00 → 0:25 (25 s) · orateur A
« À mi-chemin de Mars, un astronaute signale une douleur vive à la poitrine. Un message met jusqu'à vingt-deux minutes pour atteindre la Terre, et il n'y a pas de médecin à bord. Pendant ce délai, qui aide l'équipage à mesurer, à comprendre ce qui change, et à décider ? Nous sommes l'équipe MONOLITH, et notre réponse s'appelle C-Sync. »
**Transition :** clic sur « vingt-deux minutes ».

## Diapo 2 · 0:25 → 1:05 (40 s) · orateur A
« Selon une analyse de la NASA présentée à ASCEND 2022, un message entre Mars et la Terre met jusqu'à vingt-deux minutes dans un sens, et les coupures de communication peuvent durer de plusieurs jours à plusieurs mois. Pour toute mission habitée vers Mars, ces retards sont inévitables. L'équipage est donc seul pour mesurer et agir. Or les astronautes ne sont pas médecins. Il leur faut un outil qui fonctionne hors ligne, qui guide chaque mesure, et qui signale toute donnée absente au lieu de la faire passer pour normale. »
**Transition :** « Voici comment, en trois actes. »

## Diapo 3 · 1:05 → 1:55 (50 s) · orateur A
« Premier acte : une dérive lente. C-Sync compare chaque astronaute à lui-même, sur ses cinq premiers jours, et non à une norme universelle. Pendant ces cinq jours, aucune alerte de dérive n'est évaluée : la référence se construit, et l'écran le dit. Au jour sept de notre histoire simulée, le temps de réaction et les erreurs d'attention s'éloignent de sa référence deux jours de suite. La carte Attention passe en dégradée, et la carte Corps en surveillance : deux dimensions sortent de la normale. C-Sync affiche ce qui a changé, depuis quand, et avec quelle certitude. Il ouvre une procédure de fatigue et propose de revoir les signaux avec l'officier médical de bord. La décision reste humaine : elle est affichée en attente. »
**Transition :** passage de main à l'orateur B.

## Diapo 4 · 1:55 → 2:55 (60 s) · orateur B
« Deuxième acte, jour neuf : l'urgence de la vidéo du défi. L'astronaute signale une douleur vive à la poitrine. Une règle d'événement ouvre directement une procédure critique. L'écran guide les mesures, une par une : fréquence cardiaque, tension, température, glycémie. Pour chacune, il explique comment la prendre. La glycémie est marquée sans référence NASA en vol. C-Sync est conçu sans recommandation de médicament ni interprétation du symptôme : il enregistre les valeurs telles qu'elles sont mesurées, chacune avec son heure et son origine. Une phrase fixe rappelle de suivre la check-list médicale de bord et l'officier médical. Le compte rendu part dans une file d'envoi, et l'écran affiche l'état de la liaison. La liaison est coupée ; dès qu'elle revient, le rapport est envoyé une seule fois, sans doublon. Ici, une carte du corps à cliquer, encore en maquette, non codée. »
**Transition :** « Le lendemain, l'équipage veut reprendre le travail. »
**Si on est en retard : coupe** la phrase « La glycémie est marquée sans référence NASA en vol. » (−9 mots, environ 4 s).

## Diapo 5 · 2:55 → 3:45 (50 s) · orateur B · DÉMO EN DIRECT
Manipulation : interface déjà ouverte au jour 10. Appui sur « Request resume », puis sur « Commander override ».
« Troisième acte, jour dix, en direct. Je demande la reprise. Refusée. [2 s de silence] Le commandant force la reprise. Le forçage est consigné dans le journal, mais la décision ne change pas : la dernière fréquence cardiaque date de quatorze minutes, la limite est de dix. Le système donne la raison en clair, sur l'écran. Une donnée périmée est signalée comme expirée, pas comme normale. Dans nos règles, un forçage seul ne suffit pas à reprendre. »
Démo en panne : si rien ne s'affiche en 10 secondes, passer à la capture C5 et dire le même texte.
**Transition :** retour au clavier de l'orateur A.

## Diapo 6 · 3:45 → 4:25 (40 s) · orateur A
« Nos preuves, dans l'esprit du défi méthodologique Artemis II : une référence individuelle. Nous avons réglé la règle sur un jeu d'équipages simulés, puis nous l'avons lancée, inchangée, sur trois cents nouveaux équipages en bonne santé : aucun n'a déclenché de procédure à tort. Dérives progressives : quatre-vingt-treize pour cent repérées. Saut brutal : seulement cinquante-sept pour cent, notre limite connue. Tout est simulé. Seule donnée réelle : la télémétrie de cabine de l'ISS, où notre contrôle qualité repère un CO2 constant pendant plus de six jours. »
**Si on est en retard : coupe** la dernière phrase (CO2 constant, −22 mots, environ 10 s).

## Diapo 7 · 4:25 → 5:00 (35 s) · orateur A
« Nos limites : l'équipage est simulé, rien n'est validé cliniquement. Les os, l'immunité et la dose de rayonnement reçue par l'équipage ne sont pas encore mesurés ; ils sont affichés comme inconnus. Nous avons choisi un moteur simple, testé et explicable, plutôt qu'une boîte noire. La suite : de vraies données si elles s'ouvrent, et des adaptateurs pour de vrais capteurs. L'interface n'affiche que des écarts statistiques, sans qualification médicale. C-Sync : hors ligne, explicable, et c'est l'humain qui décide. Merci. »

---
## Comptes et minutage (calculés par script)
| Diapo | Début → fin | Durée | Mots dits | Mots/min |
|---|---|---|---|---|
| 1 | 0:00 → 0:25 | 25 s | 59 | 142 |
| 2 | 0:25 → 1:05 | 40 s | 88 | 132 |
| 3 | 1:05 → 1:55 | 50 s | 122 | 146 |
| 4 | 1:55 → 2:55 | 60 s | 139 | 139 |
| 5 | 2:55 → 3:45 | 50 s | 72 | 86 |
| 6 | 3:45 → 4:25 | 40 s | 82 | 123 |
| 7 | 4:25 → 5:00 | 35 s | 78 | 134 |
| **Total** | **0:00 → 5:00** | **300 s** | **633** | **127** |

Lecture : les diapos parlées (1–4, 6, 7) vont de 126 à 146 mots/min (cible 130–145 ; la diapo 3 est un peu au-dessus, la diapo 6, chargée en chiffres, un peu en dessous). La moyenne sur 5:00 (128) est plus basse parce que la diapo 5 est volontairement lente (environ 85 mots/min) : elle laisse le temps des deux clics de la démo et de 2 s de silence après « Refusée ».
Répétition : chronométrer une lecture complète à voix haute ; si elle dépasse 5:00, appliquer les deux lignes « coupe » (environ −14 s au total).
Méthode de comptage : mots entre guillemets, un mot = suite de lettres ou de chiffres, apostrophes incluses (« l'équipage » = 1) ; un mot composé avec trait d'union compte pour un (« quatre-vingt-quinze » = 1).
