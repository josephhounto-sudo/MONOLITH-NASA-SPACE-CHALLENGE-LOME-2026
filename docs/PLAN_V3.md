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
- Seuil de 2,0 mmHg de Law 2014 : lu dans le résumé de presse seulement.
- Accès à Gemini aujourd'hui.
- Aucun inconnu n'a encore testé quoi que ce soit.
