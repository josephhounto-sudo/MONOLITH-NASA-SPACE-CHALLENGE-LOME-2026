# Vidéo V3 pour le local lead : script de 45 s (20/11/2026, remplace SHOTLIST_V3.md)

**Essence (19 mots) :** Quand l'aide est à vingt minutes, C-Sync compare chaque astronaute à lui-même et laisse une personne décider.

**Personnage :** Kora Mensah, astronaute **simulée** (le bandeau SYNTHETIC reste visible à chaque plan de l'histoire). Son geste ordinaire : le test de réaction du matin.
**Horloge :** délai aller de 20 minutes (barre d'opérations de l'histoire, paramètre de démo du contrat `ground_delay_min`). Elle est affichée à l'écran, pas seulement dite.
**Deux journées :** jour 7 (la valeur au quotidien), puis jour 9 (la valeur sous pression).
**Ce que le public sait et Kora ignore :** la courbe glisse depuis le jour 6, alors qu'elle se sent bien.

Enregistrement : voix de Joseph, écran de l'app publique en 1920×1080, sous-titres anglais incrustés (= texte de la voix). Aucune photo de personne, pas de logo NASA. Débit visé : 2,3 mots par seconde.

| # | Temps | Écran exact (clics) | Voix = sous-titre (≤ 1 souffle) | Donnée et statut | Émotion |
|---|---|---|---|---|---|
| 1 | 0–7 s | Arrivée : les trois lignes du bourdon apparaissent | A quick sum once said a bumblebee can't fly. It flew. Nobody had measured the bee. | Histoire vraie : mythe, vol expliqué par Dickinson et al., Science 1999 (source écrite sous le bouton) | Curiosité |
| 2 | 7–13 s | Clic « Enter the station » → console en direct, CO2 en gros chiffres | This is real air on the space station, live from NASA, right now. | **RÉEL** : flux public ISSLive (valeur du jour, non retouchée) | Surprise |
| 3 | 13–19 s | Habitat → rejeu des missions (barre des heures au-dessus de la limite) | On fourteen real missions, daily averages hid 370 hours above NASA's limit. | **RÉEL** : `research/retro/RESULTS.md` (OCHMO-TB-004, 3 mmHg sur 1 h) | Inquiétude |
| 4 | 19–27 s | Histoire, jour 7 : cartes d'état + courbe du temps de réaction | Kora feels fine. Her own reaction time has slipped for two days. | **SIMULÉ** : capsule du jour 7 (règle C-Sync, 2 jours de suite) | Suspense : on voit ce qu'elle ignore |
| 5 | 27–35 s | Barre d'opérations « 20 min » → Guide d'urgence, cas « Malaise », étape 1 sur 6 | Day nine, chest pain. Earth is twenty minutes away. The steps are on board. | **SIMULÉ** (l'histoire) ; chaque étape cite sa source NASA (`emergency_guide.json`) | Tension, puis appui |
| 6 | 35–40 s | Technologies → bouger le curseur « Transmissions lost » de la messagerie | Every piece can be touched, and says if it's proven or a promise. | **SIMULÉ** (liaison) ; statut lu dans le registre | Confiance |
| 7 | 40–45 s | Pip en bas à gauche, puis carton final | C-Sync points. A person decides. Measure the astronaut, not the average. | Carton : « Team MONOLITH, Lomé · Synthetic crew data · Real NASA cabin data » + URL | Phrase à répéter |

**Phrase à répéter (fin) :** *Measure the astronaut, not the average.* Elle ferme la boucle ouverte par le bourdon au plan 1.

## Version française de la voix (si le local lead préfère)
1. Un calcul rapide disait qu'un bourdon ne peut pas voler. Il a volé. Personne n'avait mesuré le bourdon.
2. Voici l'air réel de la station spatiale, en direct de la NASA.
3. Sur quatorze vraies missions, les moyennes du jour cachaient 370 heures au-dessus de la limite NASA.
4. Kora se sent bien. Son propre temps de réaction glisse depuis deux jours.
5. Jour neuf, douleur à la poitrine. La Terre est à vingt minutes. Les étapes sont à bord.
6. Chaque pièce se touche, et dit si elle est prouvée ou une promesse.
7. C-Sync montre. Une personne décide. Mesurer l'astronaute, pas la moyenne.

## Contrôles avant d'envoyer (aucun ne dépend de nous)
- **Lecture à voix haute chronométrée :** chaque ligne tient dans un souffle et dans sa case de temps. Si une ligne déborde, couper des mots, ne jamais accélérer.
- **Données :** 370 h et 14 missions viennent de `research/retro/RESULTS.md` ; 20 min du contrat ; « 6 étapes » du guide. Le CO2 en direct change à chaque prise : ne pas le citer à voix haute.
- **Mots interdits :** ni « cause », ni « diagnostic », ni « prouve », ni « garanti », ni « maladie » (vérifié sur ce texte : « proven » apparaît au plan 6 et désigne le statut d'une pièce logicielle, pas une affirmation médicale. Si le doute persiste, dire « tested » à la place).
- **Test de reformulation :** montrer la vidéo à 7 personnes qui ne connaissent pas le projet ; chacune raconte en 3 phrases. Cible : 5 sur 7 disent « il compare l'astronaute à lui-même » et « une personne décide ». Noter la première hésitation, mots exacts.
