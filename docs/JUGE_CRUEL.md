# Jury cruel — C-Sync, dimanche 15/11/2026 07:30 UTC
FAIT PAR L'IA. Écrit contre nous, à partir de ce qui est dans le dépôt et mesuré aujourd'hui. Les cinq critères sont ceux que le dépôt retient pour le jugement (impact, créativité, validité, pertinence, présentation). Notes sur 5, à discuter, pas des vérités.

## Verdict en une ligne
Moteur honnête et bien testé, **interface nue et données NASA presque invisibles**. Un juge de la NASA verrait un tableau de bord Streamlit standard avec un graphique de plus tard, pas un outil qu'un centre de contrôle utiliserait.

## Note par critère
| Critère | Note | Raison la plus dure |
|---|---|---|
| Validité (science, données) | **2,5** | Tout le résultat chiffré est sur des équipages **simulés**, avec un seuil **réglé sur ces mêmes scénarios** (0,7 % de fausses alertes, 95,3 % de dérives lentes, 59,3 % de changements brusques : 41 % des changements brusques ne sont pas vus). Aucune validation sur des données humaines. La partie « NASA » est une télémétrie de cabine de missions rongeurs, pas un équipage. |
| Pertinence au défi | **3** | Le défi parle de surveillance de la santé des astronautes ; nous évaluons 3 dimensions sur 5, Mission et Habitat restent « contexte seulement ». Les 4 mesures guidées de l'urgence existent mais la silhouette citée comme exemple par l'énoncé (selon notre rapport interne) n'était pas dans l'application ; elle l'est maintenant sur la branche `nasa-data` (sélection par boutons, pas encore cliquable sur le corps). |
| Impact | **2,5** | Aucune preuve qu'un équipage ou un médecin de vol en tirerait quoi que ce soit. Aucun avis d'un professionnel. |
| Créativité | **3** | L'idée « un refus qui protège l'équipage » (porte de reprise) et « UNKNOWN n'est jamais normal » sont de vraies idées. L'écran ne les met pas en valeur. |
| Présentation | **2** | `main` s'affichait sur fond blanc avec des cartes de hauteurs inégales et 1 à 2 violations de contraste. Diapos et captures datent d'un état antérieur. Pas de noms d'équipe sur la diapo 1, contrairement au guide. Le logo est une image IA sans filigrane (risque accepté par M1). |
| **Moyenne** | **2,6 / 5** | |

## Les cinq failles qu'un juge sévère trouve en 10 minutes
1. **La NASA n'était pas à l'écran.** Les données réelles ne servaient qu'à un test et à une figure de diapo. Corrigé en partie par le panneau Habitat (branche `nasa-data`) : CO2 réel RR-1 contre la exigence NASA-STD-3001, plateaux signalés, 14 missions.
2. **Aucune preuve médicale.** Le dépôt le dit lui-même (« paramètres de conception, pas de valeurs cliniques »). C'est honnête, mais cela signifie : pas de sensibilité réelle, pas de médecin de vol consulté. **Ne rien revendiquer de plus.**
3. **Seuil réglé sur les données d'évaluation.** Les 95,3 % sont donc optimistes. Phrase obligatoire à l'oral : « réglé sur les mêmes scénarios ».
4. **Le changement brusque est mal vu** (59,3 %). La méthode qui le couvre mieux (hybride EWMA ou règle B, 81 %) n'a pas été adoptée, gain non concluant à 300 équipages.
5. **Fatigue du juge** : 8 champs de soumission, 7 diapos, pitch de 5 minutes sans questions. Tout ce qui n'est pas visible en 5 secondes n'existe pas.

## Ce que la donnée NASA montre vraiment (calculé aujourd'hui depuis le brut, vérifié par test)
- Sur **14 missions** avec CO2 exploitable, **12** contiennent au moins une série de valeurs **strictement identiques de 1 h ou plus**. La plus longue : **222 h** (RR-5, 3000 ppm). RR-1 : 153,1 h à 2646 ppm.
- Plusieurs valeurs constantes sont **improbables comme mesures de CO2** (200, 250, 500 ppm : RR-7, RR-3, RR-6) : plus probablement un remplissage de données. **Origine inconnue : ne jamais écrire « capteur gelé ».**
- Zéros ou plafond à 5000 ppm de capteur : RR-3, RR-7, RR-20, RR-22, RR-25, RR-28 marqués (6 missions sur 14).
- Repère NASA : **moyenne horaire de la pression partielle de CO2 dans le volume habitable ≤ 3 mmHg** (NASA-STD-3001 Vol. 2 Rev C, note OCHMO-TB-004 Rev B du 11/10/2022). Conversion ppm vers mmHg à 760 mmHg : **approximative**. La même note donne l'intervalle actuel de l'ISS à 1–9 mmHg ; nos maxima horaires (2,2 à 6,8 mmHg) sont dedans, **sans que ce soit une preuve** (capteurs d'installations rongeurs).
- RR-1 : **8,9 % des heures** au-dessus de 3 mmHg-équivalent ; RR-28 : 46,9 % ; RR-3 : 36,8 %. À présenter comme un contexte, **jamais** comme une non-conformité de l'ISS.

## Ce qui prouverait que nous avons raison (et que ni toi ni moi ne pouvons fournir)
- Un médecin de vol ou un chercheur du domaine qui lit l'écran et la règle (aucun contact).
- Un jeu de données humain avec étiquettes (inexistant en accès ouvert d'après la recherche NLSP).
- Le test des 5 secondes avec 3 à 5 personnes.

## Seconde passe, même grille (15/11/2026 08:05 UTC, branche `nasa-data`)
| Critère | Avant | Après | Ce qui a changé | Ce qui plafonne la note |
|---|---|---|---|---|
| Validité | 2,5 | **3,0** | données NASA réelles à l'écran avec repère officiel, contrôle qualité branché, 14 missions recalculées depuis le brut, tableau de provenance, README et AI_USAGE exacts | résultats toujours sur équipage simulé, seuil réglé sur les mêmes scénarios |
| Pertinence | 3,0 | **3,5** | carte du corps dans l'application, action d'abord quand une procédure est ouverte | 3 dimensions sur 5 évaluées ; pas d'avis de professionnel |
| Impact | 2,5 | **2,5** | rien | aucune preuve d'usage réel |
| Créativité | 3,0 | **3,0** | rien | l'écran ne met pas les idées en valeur |
| Présentation | 2,0 | **2,5** | thème sombre, 0 violation d'accessibilité | pas de design abouti, pas de noms, diapos à recapturer |
| **Moyenne** | **2,6** | **2,9** | | |

Le jury ne « choisit » pas une équipe à 2,9 sur 5 : il le fait pour l'équipe dont l'écran se comprend en 5 secondes et dont une preuve extérieure existe. Les deux leviers restants ne sont pas du code : le **design** (en cours ailleurs) et **une voix extérieure** (médecin de vol, chercheur, ou 3 à 5 personnes au test des 5 secondes). Je ne peux pas simuler l'une ni l'autre honnêtement.
