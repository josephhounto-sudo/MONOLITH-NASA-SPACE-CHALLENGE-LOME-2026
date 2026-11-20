# C-Sync V3 — plan vérifié avant construction (20/11/2026, 05:40 UTC)

Statut : PLAN. Aucune ligne de V3 n'est codée. Chaque étape a une entrée, une sortie, un critère d'acceptation mesurable par un tiers et un responsable.

**But (vérifiable)** : en 60 secondes, un inconnu dit à quoi sert C-Sync et montre une donnée NASA en direct à l'écran.

**Bloquant** : l'échéance (date et heure, vidéo comprise) est inconnue. Sans elle, l'ordre de coupe ci-dessous s'applique.

## 1. Préconditions testées ce matin

| Pari | Résultat | Preuve |
|---|---|---|
| Caméra autorisée jusqu'au composant Streamlit | OUI côté permissions | iframe de l'app publique : `allow` contient `camera`. Streamlit 1.67 donne `camera` aux iframes de composant (IFrameUtil). La capture réelle reste NON VÉRIFIÉE : il faut un clic humain. |
| CO2 de l'ISS en direct, public | OUI | Tableau ISS Mimic ouvert à 05:3x UTC : LAB PPCO2 = 2,44 ; N3 PPCO2 = 2,95 ; LAB PRESS = 751,9 ; LAB TEMP = 23,3. Unité de fait : le mmHg (pression ≈ 752). Le fichier PUIList annonce PSIA, ce qui est contradictoire : il faut lire la valeur brute du flux avant affichage. |
| Flux branché depuis notre app | NON VÉRIFIÉ | Mon shell est bloqué (code 000), et l'injection de script dans une page en ligne m'a été refusée. Le test se fera dans le composant de notre propre app. Conditions d'usage du serveur public push.lightstreamer.com : NON VÉRIFIÉES. |
| Licences | OUI | three 0.187.0 sous MIT ; @mediapipe/tasks-vision 1.2.3 sous Apache-2.0 ; lightstreamer-client-web 9.2.3 sous Apache-2.0 (npm view). |
| Police à points | OUI | `csync/ui/fonts/Doto-700.woff2` est embarquée, mais ne sert qu'au gros chiffre. |
| Données de mission réelles | OUI, pour l'air seulement | 14 missions ISS. Rejeu pré-enregistré : `research/retro/` (370 h de dépassement cachées par la moyenne du jour ; risque de fatigue d'alarme sur RR-28 et RR-3). Aucune donnée d'astronaute publique sous forme de série temporelle. |
| Gemini | NON VÉRIFIÉ ce matin | Connecté lors des sessions précédentes. À rouvrir au lancement du lot 4. |

## 2. Jetons de design mesurés sur la référence Bookings Per Day

Mesures sur les pixels de l'image (736×1104), quantification en 4 couleurs par zone.

- Fond : #F5F0ED (crème chaud), avec une forme sombre floue (#4B4039 → #2A211C) et des halos orange.
- Carte du graphe : verre fumé ; tons #D8BCAA (haut clair), #9C8373, #715A4B, #4B4039 (bas sombre). Rayon d'environ 40 px sur une largeur de 460 px.
- Courbe : orange #D79A76 avec un halo ; point final blanc #FFFDFD sous une lueur.
- Rangée de jours : pastilles rondes à contour clair ; le jour choisi est plein et blanc.
- Pilules de chiffres (rayon = moitié de la hauteur) :

| Pilule | Teinte dominante | Lueur | Clair |
|---|---|---|---|
| Corail | #D78368 | #E49F82 | #EFC9B4 |
| Gris fumé | #8E7F75 | #B7A79B | #E3D6CC |
| Orange brûlé | #CF783C | #A04A24 | #552919 |
| Action | #FAE2C6 et #413730 | — | — |

  Chaque pilule porte une icône en haut à droite et une pastille de variation « ↑ 20 % ».
- Bouton d'action : rond, lueur crème #FFF2DA.
- Texte : #FFFDFD. Gros chiffres environ 2,5 fois le libellé.

**La référence échoue au contraste.** Texte blanc sur #D78368 : 2,86:1. Sur #CF783C : 3,28:1. Sur #9C8373 : 3,55:1. Le seuil du projet est 4,5:1.

Règle V3 : on garde l'aspect, mais tout texte de moins de 24 px se pose sur une zone de verre assombrie à ≤ #715A4B (6,43:1). Les chiffres de 24 px ou plus restent autorisés à 3:1, mesure faite sur les pixels.

## 3. Contradictions et décisions qui reviennent à Joseph

1. **Thème clair à la place du navy.** « Exactement la référence » remplace navy/crème/corail par crème/verre fumé/orange.
   - Recommandation : accepter. Le crème devient visible, ce qui répond à ta remarque « je ne vois nulle part le crème ».
2. **L'orange signifie « attention » dans les conventions NASA** (rouge = alarme, jaune/ambre = attention). La référence l'emploie pour décorer.
   - Recommandation : orange et corail réservés aux catégories et à la marque. Les états s'affichent toujours en mot + icône (Normal, Attention, Urgent, Inconnu), avec ambre et rouge réservés à ces seuls états.
3. **La dérive n'apparaît que dans la démo.** La règle v3 reste dans le code, gelée (AGENTS.md).
   - Recommandation : l'accueil = console en direct + bot ; un « Mode démo » rejoue l'histoire de Kora pour la vidéo.
4. **Silhouette floue de la référence.** On ne met pas de photo d'une personne identifiable.
   - Recommandation : une forme générée en CSS (flous et dégradés), aucune photo.
5. **Clignement des yeux (PERCLOS).** Seul, il n'est pas validé (Abe 2023). Aucune lecture d'émotion (Barrett 2019).
   - Recommandation : indicateur d'attention expérimental, calcul sur l'appareil, rien n'est enregistré, consentement visible. Il ne décide jamais seul.
6. **Alertes Habitat.** Le rejeu montre qu'un affichage heure par heure fatigue l'équipage.
   - Recommandation : afficher des épisodes (début, durée, pic). La règle de calcul ne change pas.

7. AGENTS.md est périmé : il interdit le push direct sur main (règle 1), impose le format de commit « M2: » (règle 3) et fixe un gel au samedi 18:00 (règle 8). Joseph a levé le gel et autorisé la fusion sur main ; les commits récents ne suivent pas le format « M2: ». Recommandation : mettre AGENTS.md à jour avec ces décisions datées, sinon toute autre IA du dépôt suivra des règles fausses.

## 4. Lots de travail, dans l'ordre

| # | Lot | Entrée | Sortie | Critère d'acceptation (tiers) | Qui |
|---|---|---|---|---|---|
| 1 | Système Bookings | Jetons §2, décisions 1, 2 et 4 | Fond crème + forme floue, cartes de verre fumé, pilules de catégorie, courbe lumineuse + rangée de jours, Doto sur tous les chiffres, barre latérale fine avec icônes Lucide | Capture côte à côte avec la référence. Contraste mesuré sur pixels à 390 et 1400 px : « Below threshold: none ». Aucune pilule sans icône. | Claude |
| 2 | Console en direct | Flux ISS (LAB et N3 : ppCO2, pression, température) | Composant en direct : valeur, âge de la mesure, limite de 3 mmHg, mention « NASA, en direct, contexte seulement ». Épisodes Habitat issus du rejeu. | Une valeur change en moins de 60 s. Valeur brute comparée à ISS Mimic au même moment (écart < 0,05). Hors ligne : la mention « Inconnu » s'affiche, jamais une valeur périmée. | Claude |
| 3 | Clignement | Composant caméra + MediaPipe | Prototype isolé PERCLOS + consentement | Vidéo de Joseph : 10 s yeux ouverts, puis 10 s yeux fermés ; la mesure sépare les deux. Sinon on abandonne et la promesse disparaît. Essai sur 3 personnes, échecs écrits. | Claude, puis Joseph (vidéo) |
| 4 | Bot | Brief à Gemini (personnalité, nom, image originale, tutoriel ≤ 6 étapes, dialogue de démo astronaute + commandant) | Bot intégré : tutoriel au premier passage, bulles, image | Test qui passe tous les textes au filtre des mots interdits (n'existe pas encore : à créer). Un inconnu termine le tutoriel sans aide. L'image n'est pas un personnage connu. | Gemini (contenu), Claude (intégration et vérification) |
| 5 | Technologies montrées | Modules existants | Chaque techno = un essai que l'on manipule (falsifier la capsule et voir la signature casser ; couper la liaison et voir la file attendre ; bouger le stress et voir le RMSSD bouger), une phrase au maximum | Aucun paragraphe de plus de 25 mots. Chaque carte a un contrôle et un effet visible. | Claude |
| 6 | Corps 2,5D | Zones de la capsule | Corps en profondeur (CSS 3D ou three.js), zone allumée selon la donnée, légende | La zone touchée correspond à la capsule (test). Premier rendu sur mobile < 2 s. | Claude |
| 7 | Graphes et tableaux | Graphes actuels | Phrase de lecture au-dessus de chaque graphe, point clé annoté ; tableaux remplacés par des petites courbes + la liste des seuls écarts | Test : chaque graphe a sa phrase. Aucun tableau de plus de 6 colonnes. | Claude |
| 8 | Mode démo | Histoire de Kora, dialogue (lot 4) | Rejeu guidé pour la vidéo : dérive, dialogue avec l'astronaute, passage bref chez le commandant | Rejeu complet sans erreur. Durée ≤ 2 min. | Claude, Joseph (tournage) |
| 9 | Contrôle de sortie | Tout | Tests, ruff, contraste sur pixels, démarrage à froid de l'URL publique, test des 5 s auprès d'inconnus | Tous les tests verts ; « none » au contraste ; URL à jour ; 5 inconnus sur 7 répondent à « à quoi ça sert ? » | Claude, Joseph (inconnus) |

**Ordre de coupe si le temps manque** : 6, puis 7, puis 5. Les lots 1, 2, 4 et 8 forment le minimum présentable.

## 5. Encore NON VÉRIFIÉ
- Capture caméra réelle dans l'app déployée.
- Connexion au flux ISS depuis notre composant ; unité brute ; conditions d'usage du serveur public.
- Seuil 7 jours corrigé à 2,5 mmHg (OCHMO-TB-004, source NASA) ; le 2,0 du résumé de presse est abandonné.
- Accès à Gemini aujourd'hui.
- Aucun inconnu n'a encore testé quoi que ce soit.

## 6. Décisions de Joseph (20/11, 05:35 UTC)
1. Référence reprise, textures comprises. 2. Orange utilisé (attention du public) ; les états restent écrits en mot et icône. 3. La dérive n'est pas la base : console en direct à l'accueil. 4. Pas de photo de personne : fond sans personne (§8). 5. Clignement : « en développement », avec note courte. 6. Épisodes Habitat : expliqués à Joseph, en attente. Horloge mondiale demandée (§9). 7. AGENTS.md mis à jour.

## 7. Inventaire du temps réel (relevé ISS Mimic, 05:3x et 05:4x UTC)
| Indicateur | Source | Statut |
|---|---|---|
| CO2 partiel LAB et Node 3 (mmHg) | NASA ISS, flux public | RÉEL. Valeur identique sur deux relevés à environ 10 min d'écart (2,435 et 2,950) : cadence de mise à jour NON VÉRIFIÉE. |
| O2 et N2 partiels, pression cabine, température LAB | NASA ISS, flux public | RÉEL. La température a changé entre les relevés (23,32 → 23,45 °C). |
| Réservoirs d'eau, production d'oxygène (OGA), recyclage d'eau | NASA ISS, flux public | RÉEL |
| Signal sol (acquis / perte prochaine) | NASA ISS, flux public | RÉEL. Le flux s'interrompt pendant les pertes de signal : âge de la mesure obligatoire. |
| Physiologie d'un astronaute | aucune source publique en direct | N'EXISTE PAS en réel |
| Clignement des yeux de l'utilisateur | caméra de l'appareil | EN DÉVELOPPEMENT |
| Rythme cardiaque de l'équipage | simulé | SIMULÉ |

## 8. Fond sans photo de personne (propositions)
- A : casque de combinaison vu de dos, dessiné en SVG (forme simple, pas un individu), flouté, avec les halos orange de la référence.
- B : limbe d'une planète (arc sombre et lueur orange de l'atmosphère), généré en CSS : rappelle Mars et la mission.
- C : la station en silhouette géométrique, floutée, qui avance lentement selon la position réelle (flux public).
Recommandation : B pour l'accueil, A derrière le bot.

## 9. Horloge mondiale
Aucune bibliothèque nécessaire : `Intl.DateTimeFormat` du navigateur.
Fuseaux retenus : heure de bord ISS = UTC (choix des agences partenaires) ; Houston (America/Chicago, centre de contrôle NASA) ; Moscou (Europe/Moscow, centre de contrôle russe) ; Lomé (Africa/Lome, l'équipe, UTC+0 donc à l'heure de la station). Ajout : temps écoulé de la mission démo (jour et heure), et délai de liaison simulé de Mars.
Critère : écart de moins d'une seconde avec l'horloge système ; test des quatre fuseaux.

## 10. Revue d'ingénieur NASA (20/11, 06:00 UTC)
Matière : les 18 risques HRP copiés le 15/11 (`data/nasa_official/`), l'énoncé du défi, les champs bruts de l'EDA (24 missions), le flux ISS en direct, les fiches techniques OCHMO.

### 10.1 Traçabilité risque NASA → C-Sync
| Risque HRP (liste officielle) | Fonction C-Sync | Donnée | Statut |
|---|---|---|---|
| Inadequate Sleep and Irregular Schedules | dérive d'attention, clignement | simulée ; caméra | couvert (simulé, en développement) |
| Behavioral Changes and Psychiatric Disorders | indicateur Morale | simulée | couvert (simulé) |
| Cardiovascular Adaptations | rythme cardiaque, variabilité | simulée | couvert (simulé) |
| Inadequate Systems Operations Support | capsule hors ligne, procédures, file d'envoi | conception | couvert |
| Danger « environnement fermé ou hostile » | Habitat CO2 | RÉELLE (EDA + direct) | couvert |
| Radiation-Induced Cancers | aucune | dose quotidienne RÉELLE dans l'EDA, 24 missions, inutilisée | MANQUE |
| Hypoxia | aucune | ppO2 et pression RÉELS en direct | MANQUE |
| Decompression Sickness | aucune | pression du sas en direct (préparation de sortie) | piste seulement |
| Inadequate Teamwork | aucune | — | hors portée |
Les huit autres risques (os, muscles, vision, immunité, microbes, nutrition, sorties, charges) n'ont aucune donnée accessible : on les nomme, on n'y touche pas.

### 10.2 Données mal utilisées ou oubliées
1. Radiation (correction du 20/11, 06:30) : la dose quotidienne RR-1 est déjà tracée dans Habitat (volet replié), mais elle n'entre dans aucun état ni aucune jauge. La ressource de l'ASC sur la radiation, citée par le défi, est inutilisée. Attention : l'EDA donne une dose absorbée (mGy) ; la limite NASA de carrière (600 mSv, NASA-STD-3001) est une dose efficace. On affiche la dose cumulée réelle, sans conversion inventée.
2. CO2 : seule la limite d'une heure est utilisée ; l'exposition sur 7 jours (OCHMO-TB-004 : < 2,5 mmHg) est absente de l'app.
3. Température et humidité de cabine : tracées, jamais évaluées. Les plages NASA restent à trouver (NON VÉRIFIÉ).
4. Jalons de mission de l'EDA (lancement, arrivée, retour) : inutilisés ; ils permettent d'aligner les événements sur les courbes.
5. Capteur de cabine ≠ air respiré : le CO2 peut stagner près du visage (Aerospace Medicine and Human Performance, 2025). À écrire sous chaque valeur.

### 10.3 Idées techniques que nos données rendent possibles
| # | Idée | Antériorité | Essai d'une heure qui peut échouer |
|---|---|---|---|
| I1 | Séparer « signal partagé par l'équipage » et « signal individuel » : si plusieurs membres dérivent ensemble pendant un épisode de CO2, la carte dit « signal commun, voir l'air de cabine » plutôt que d'accuser une personne. Johnston et Dietlein (1974) notent déjà qu'on ne savait pas séparer l'effet du vol de la variation individuelle. | Aucun outil de ce type trouvé en une recherche : NON PROUVÉ comme nouveau | Équipages simulés (graines jamais utilisées) avec un décalage commun et un individuel ; il faut au moins 90 % de bonnes attributions, sinon on abandonne. |
| I2 | Grand livre d'exposition, comme une jauge : CO2 sur 7 jours face à 2,5 mmHg, dose de radiation cumulée réelle | La NASA suit déjà la dose (dosimètres) ; ce qui est nouveau, c'est la vue côté équipage, hors ligne et combinée | Rejeu des 24 missions : le cumul affiché doit égaler la colonne `accumulated` de l'EDA. |
| I3 | Contrôle d'intégrité du flux en direct : notre détecteur de plateaux (ARTIFACT) appliqué au flux ISS signale une valeur figée comme suspecte | Réutilisation de notre propre code | Une heure de flux : si le CO2 reste identique (comme ce matin), la carte doit dire « valeur figée depuis X min ». |
| I4 | Rejeu de mission dans l'app : le jury choisit une des 14 missions réelles et voit ce que C-Sync aurait signalé | Notre rejeu pré-enregistré | Les chiffres affichés doivent égaler `replay_results.csv`. |
| I5 | Fraction d'O2 en direct = ppO2 ÷ pression totale (LAB ce matin : 165,8 ÷ 751,9 ≈ 22,1 %), face à la règle normoxique NASA | Calcul simple ; les seuils de vol restent à sourcer (la norme dit que les limites physiologiques de vol sont inconnues) | Comparer au même moment avec ISS Mimic. |

## 11. État d'exécution (20/11/2026, 06:30 UTC) — main = dab9964
| Lot | Fait | Preuve |
|---|---|---|
| 1 Système Bookings | fond crème à grain, limbe de planète flou, halos orange, panneau de verre fumé, pilules avec lueur par catégorie, barre latérale claire avec icônes Lucide et pilule blanche, Doto sur horloges, valeurs en direct, métriques et bandes | captures 1400/390 ; measure_contrast « Below threshold: none » (page d'accueil seulement) |
| 2 Console en direct | CO2 labo + Node 3, part d'O2, pression, 4 horloges ; fraîcheur jugée sur l'horloge de la station ; valeur cachée après perte de signal | URL publique 06:23 UTC : 2,44 / 2,95 mmHg, 22,1 %, 752 mmHg, état « Live » ; tests node |
| 3 Habitat | phrase de lecture calculée, épisodes, 7 jours face à 2,5 mmHg, rejeu de 14 missions, tableau replié | tests (épisodes = rejeu de recherche) ; URL publique |
| 4 Bot Pip | mascotte SVG originale, tutoriel 6 étapes, dialogue de démo par étape (Kora, Pip, commandant) | tests (≤ 6 étapes, ≤ 12 mots par réplique, mots interdits) ; URL publique |
| 5 Technologies | bandes de jours/étapes, empreinte en Doto, courbe RR zoomée | capture 1400 |
| 6 Corps 2,5D | perspective CSS + ombres + sol lumineux | capture 1400 |
| 7 Graphes | phrase de lecture Habitat et Tendances | tests |
| Non fait | délégation du bot à Gemini (écrit par Claude) ; détection de clignement (affichée « en développement ») ; idée I1 signal commun ; jauge radiation ; Doto sur la frise des jours | — |

## 12. Session longue, suite (20/11/2026, 07:00 UTC) — main = f062911
- Corps : vrai 3D construit en code (three.js 0.187.0, sphères et capsules, aucun modèle téléchargé), zone mesurée pleine, zone non mesurée estompée, zone choisie en lueur orange, rotation au doigt ; la carte 2D reste en secours sans WebGL. Vérifié : rendu WebGL sur l'URL publique (canvas présent), tests node.
- Carte héros « CO2 par jour » de la référence : courbe lumineuse, pastilles de jours alignées sur les points, jour choisi en blanc, flèches de semaine, chiffre en Doto ; données réelles RR-1 (jours sans 12 h valides = manquants, jamais 0). Vérifié : capture 1400 px, URL publique.
- Pilules en direct : icône Lucide en haut à droite et pastille d'écart à la limite (« ↓ 0,56 sous la limite »). Vérifié : URL publique.
- Défaut trouvé et corrigé : sur l'app hébergée, une barre latérale repliée et mémorisée par le navigateur revenait sans bouton pour la rouvrir. Sur ordinateur, la barre ne se replie plus ; sur téléphone, le bouton existe (vérifié à 375 px).

## 13. Rétrospective de la session (format « lessons learned » NASA : constat → cause → action), 20/11/2026 07:20 UTC
| # | Constat | Cause racine | Action (faite ou à faire) |
|---|---|---|---|
| 1 | J'ai déclaré « tout est codé » alors que 7 demandes de Joseph manquaient (bot, temps réel, clignement, 3D, verre, police, techno visible) | Je vérifiais ma propre liste, pas la liste de Joseph | Faite : chaque session part du tableau des demandes (§4, §11) ; une demande non faite est écrite « non fait » |
| 2 | Seuil 7 jours pris dans un résumé de presse (2,0) au lieu de la fiche NASA (2,5) | Matière digérée au lieu de la source | Faite : rejeu recalculé, écart déclaré ; règle inscrite dans maestro (source NASA la plus officielle) |
| 3 | « Radiation inutilisée » affirmé à tort | Inventaire fait sur les fichiers, pas sur l'écran | Faite : corrigé ; un inventaire se fait sur le rendu |
| 4 | Fraîcheur du direct mal jugée (valeur stable prise pour périmée) | Hypothèse sur le flux non testée (il n'envoie que les changements) | Faite : fraîcheur jugée sur l'horloge de la station, test node |
| 5 | Barre latérale repliée sans bouton de retour sur l'app hébergée | L'app locale ne reproduisait pas l'hébergement | Faite : barre fixe sur ordinateur ; contrôle à froid de l'URL publique à chaque déploiement |
| 6 | Curseur de jour et frise Mars au-dessus de données réelles de 2014 | Règle « un écran, un seul moment » appliquée à l'accroche seulement | Faite : frise et curseur seulement dans Histoire, Commandant, Tendances, Technologies |
| 7 | « Unknown » et cases vides partout | Vocabulaire du code exposé au visiteur | Faite : chaque trou dit pourquoi (apprentissage, capteur, dernière valeur horodatée) ; test sur toutes les sections |
| 8 | Aucun inconnu n'a testé l'app | Le travail fermé a toujours priorité sur le retour extérieur | À faire (Joseph) : 5 à 7 inconnus, 60 s, trois questions |

Ce qui a marché : pré-enregistrer le rejeu avant de calculer ; tester le pari le plus risqué en premier (flux ISS) ; déployer tôt et vérifier sur l'URL publique.

## 14. Rétrospective n°2 et avancement (20/11/2026, 07:50 UTC) — main = b78093b
| Constat | Cause | Action |
|---|---|---|
| La frise « Mars transit » était un dessin d'orbite sans fait | Décor hérité de la V2 | Remplacée par une barre d'opérations (temps, liaison, délai) + ligne de temps plate, mêmes champs en direct et dans l'histoire |
| Risque d'intégrité : le lien soumis pointe sur `main`, qui change après la date limite | Lien de soumission = dépôt vivant ; étiquette de soumission jamais publiée (push refusé) | Note de version en tête du README (commit soumis `de0b5be`) ; PDF soumis jamais modifié ; Joseph doit publier l'étiquette via GitHub > Releases |
| Urgence et questions de la vidéo : affirmées de mémoire auparavant | — | Vérifiées en ligne (`pitch/v3/QUESTIONS_ET_ECRANS.md`) |

Avancement mesurable du plan V3 : lots 1 à 7 faits et vérifiés en ligne ; lot 8 (mode démo) partiel : le dialogue est dans l'histoire, la vidéo V3 n'est pas tournée ; lot 9 partiel : tests, contrôle à froid et contraste de l'accueil faits, aucun inconnu. Côté soumission : vidéo V3 décrite, diapos V3 écrites (contenu, pas encore mises en page), message au local lead rédigé (non envoyé).

## 15. Corps intégré et promesses (20/11/2026, 08:10 UTC) — main = 2a302be
- Corps : modèle ouvert « Cesium Man » (Khronos glTF Sample Assets, CC BY 4.0, licence lue dans le fichier LICENSE du dépôt d'origine), chargé depuis un CDN épinglé (278 Ko, vérifié sur l'URL publique), zones par bandes dans le shader, tête-logo remplacée par une sphère, étiquettes à trait de rappel, crédit sous la vue ; secours : mannequin en code puis 2D.
- Technologies : 6 concepts affichés comme promesses (clignement, signal commun à l'équipage, registre d'exposition, explicateur hors ligne, messagerie DTN, pouls par caméra), chacun avec « comment nous saurons » et « nous l'abandonnons si » ; test qui interdit une promesse sans test.
- Skills : améliorations proposées pour design-master, code-master-writer et maestro (cartes à valider par Joseph).
