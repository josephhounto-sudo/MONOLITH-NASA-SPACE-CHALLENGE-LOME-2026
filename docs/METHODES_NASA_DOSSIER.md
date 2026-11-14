# Dossier technique — méthodes d'analyse pour C-Sync (14/11/2026)

> Statut : version de travail rédigée samedi 14/11 tôt le matin, avant le hackathon. Les résultats chiffrés viennent de **données simulées** (générateur csync-synth-0.1), jamais de vrais astronautes. Aucune méthode ici n'est « validée par la NASA ».

## 1. Ce que la NASA publie vraiment (sources lues le 14/11/2026)

| Source | Ce qu'elle dit réellement | Ce qu'on peut en tirer | Ce qu'on ne peut PAS dire |
|---|---|---|---|
| [Human Research Laboratories (JSC)](https://www.nasa.gov/reference/jsc-human-research-laboratories/) | Équipe Statistics & Data Science : petits échantillons (« limited astronaut population »), données longitudinales, déséquilibrées, imbriquées, observationnelles ; valeurs manquantes ; pipelines ETL, apprentissage automatique, prévision, évaluation quantitative du risque ; développement de nouvelles méthodes statistiques pour l'aérospatial | Le **problème** que résout C-Sync (petit effectif, suivi dans le temps, données manquantes) est exactement celui que la NASA décrit | La page ne nomme **aucune** méthode précise (ni EWMA, ni CUSUM, ni bayésien) |
| [Artemis II Data Methodology Challenge — gagnants](https://www.nasa.gov/hrp/winners-of-nasa-hrps-artemis-ii-data-methodology-challenge/) | 10 propositions primées ; 1re : empirical-Bayes + permutation + notation multivariée avec rétrécissement ; 3e : cadre bayésien hiérarchique unifié, un modèle par astronaute, alertes précoces, blackout de communication ; 4e : N-of-1 bayésien ; 6e : espace d'état bayésien hiérarchique | La communauté primée par la NASA converge sur : **modèle individuel + partage prudent d'information entre individus + incertitude explicite** | Ce sont des **propositions de concours**, pas des systèmes opérationnels NASA |
| [Diagnostics & Prognostics Group (Ames)](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/diagnostics-and-prognostics-group/) | Méthodes physiques, pilotées par les données, hybrides ; réseaux bayésiens ; quantification et propagation de l'incertitude ; estimation d'état et de paramètres ; bancs d'essai avec injection de pannes | Principe reprenable : **tester un détecteur en injectant des changements connus** (c'est ce que fait notre pilote) | Concerne la santé des **systèmes techniques**, pas la santé humaine ; aucun Kalman nommé sur la page |
| [OSDR — accès aux données Inspiration4 (npj Microgravity 2024)](https://www.nature.com/articles/s41526-024-00393-5) | 4 astronautes civils, 10 études OSDR, mesures avant/pendant/après le vol, métadonnées, API (GLOpenAPI), données humaines brutes en accès contrôlé | OSDR est la source des **vraies données** (omiques, cliniques) ; l'API permet l'accès programmé | Ce sont surtout des données omiques et cliniques, pas des séries quotidiennes sommeil/vigilance comparables à nos 5 dimensions |

**Conclusion honnête :** la NASA décrit le problème et récompense des méthodes individuelles à petit effectif ; elle ne publie pas « la » méthode à reprendre. Nos méthodes (EWMA, CUSUM) sont de la statistique classique de suivi de procédé, **non attribuées à la NASA**.

## 2. Catalogue des méthodes étudiées

Légende « faisable avec 5 jours de référence par astronaute » : oui = ajustable honnêtement ; non = demande beaucoup plus d'observations par personne ou un modèle de population ajusté.

| Famille | Méthode | Principe en une phrase | Données nécessaires | Faisable (5 j) | Hors ligne | Testée ici |
|---|---|---|---|---|---|---|
| Individuel | Référence personnelle + écart d (z) | On compare chaque valeur à la moyenne et à l'écart-type de l'astronaute lui-même | 5 j par indicateur | oui | oui (calcul trivial) | oui (A, B) |
| Suivi de procédé | EWMA | Moyenne glissante pondérée qui amplifie les petites dérives persistantes | idem | oui | oui | oui (C) |
| Suivi de procédé | CUSUM | Somme cumulée des écarts, alarme quand elle dépasse un seuil | idem | oui | oui | oui (pilote 1, D) |
| Hiérarchique (partage) | Rétrécissement de l'écart-type vers celui de l'équipage (version simple, empirical-Bayes) | Avec 5 jours l'écart-type perso est très bruité : on le tire vers une valeur de population | 5 j + une référence de population | oui | oui | oui (F) |
| Espace d'état | Filtre de Kalman niveau local | Estime un niveau caché qui varie lentement malgré le bruit de mesure | idem | oui | oui | oui (G) |
| Multivarié | Distance de Mahalanobis | Distance tenant compte des corrélations entre indicateurs d'une dimension | idem + corrélations de population | oui avec covariance rétrécie | oui | oui (H) |
| Multivarié | PCA | Résume des dizaines de variables en quelques axes | beaucoup de variables et d'observations | non (1 personne, 5 jours) | oui | non |
| Détection d'anomalies | Isolation Forest | Isole les points rares dans un échantillon | un échantillon de population assez grand | non en individuel | oui | non |
| Espace d'état | HMM / états cachés | Modèle à états discrets (ex. « normal / dégradé ») appris sur des séquences | longues séquences ou population étiquetée | non | oui mais ajustement lourd | non |
| Hiérarchique complet | Modèle bayésien hiérarchique (MCMC) | Estimations personnelles + niveau population, avec intervalles crédibles | cohortes comparables, historique | non en 2 jours ; **piste après le hackathon** | lourd (calcul) | non |
| Qualité | Données manquantes, provenance, propagation d'incertitude | Ne jamais confondre « pas de mesure » et « normal » | — | oui | oui | oui (UNKNOWN, scénario 10 % manquant) |

## 3. Protocole d'expérimentation (reproductible)

- **Code :** `research/pilot/pilot.py` (pilote 1) et `research/pilot/pilot2.py` (pilote 2). Commande : `python research/pilot/pilot2.py` (≈ 2,5 min). Graines fixes, résultats bruts dans `pilot2_runs.csv`, résumé dans `pilot2_summary.csv`.
- **Données :** équipages **simulés** (générateur csync-synth-0.1), 10 jours, 5 jours de référence. Références de population (écart-type typique, corrélations) estimées sur 200 autres équipages simulés (graines 20000+), jamais sur les équipages testés.
- **Règle de décision commune :** 1 indicateur signalé = WATCH, 2 ou plus = DEGRADED ; une « fausse procédure » ou une « détection » = au moins 2 dimensions sorties de NORMAL.
- **Scénarios :**
  1. *Contrôle* : aucun changement (300 équipages) → on veut 0 % de procédure.
  2. *Amélioration* : décalage favorable de 2 écarts-types sur 2 dimensions (150) → on veut 0 %.
  3. *Dérive progressive* de 1,5 écart-type (150) → on veut 100 %.
  4. *Changement brutal* de 2 écarts-types au jour 8 sur 2 dimensions (150) → on veut 100 % (seulement 3 jours pour le voir).
  5. *Données manquantes* : 10 % des valeurs quotidiennes retirées au hasard (contrôle et dérive).
- **Non couvert :** « signaux contradictoires » au sens fin (deux indicateurs d'une même dimension en sens opposé) et « variations individuelles normales » plus larges que celles du générateur. Pas de vrais labels, donc pas de sensibilité/spécificité cliniques.

## 4. Résultats (pourcentage d'équipages avec procédure déclenchée)

Pour « contrôle » et « amélioration », **plus bas = mieux**. Pour « dérive » et « brutal », **plus haut = mieux**.

| Méthode | Contrôle | Amélioration | Dérive 1,5 ET | Brutal 2 ET | Contrôle, 10 % manquant | Dérive, 10 % manquant |
|---|---|---|---|---|---|---|
| A règle actuelle (d ≥ 1) | 17.0 | 6.0 | 100.0 | 91.3 | 9.0 | 93.3 |
| B règle stricte (d ≥ 1,5 + plancher) | 0.7 | 0.0 | 95.3 | 59.3 | 0.0 | 80.7 |
| C EWMA | 2.7 | 0.7 | 99.3 | 76.0 | 1.0 | 94.7 |
| F EWMA + écart-type rétréci | 2.0 | 0.7 | 99.3 | 76.7 | 0.3 | 96.7 |
| G Kalman niveau local | 0.7 | 0.0 | 95.3 | 38.0 | 0.3 | 92.0 |
| H Mahalanobis | 0.0 | 7.3 | 40.7 | 4.0 | 0.0 | 18.7 |
| I hybride EWMA ou règle B | 4.0 | 0.7 | 99.3 | 81.3 | 1.0 | 95.3 |

Temps de calcul médian par équipage de 10 jours : 11 à 13 ms pour A à G et I, 23 à 27 ms pour H. Tout tient hors ligne sur un ordinateur de bord ordinaire.

**Lecture, sans en rajouter :**
- Avec 150 à 300 équipages, un écart inférieur à environ 3 points n'est **pas** distinguable du hasard. Les différences entre C, F et I sont de cet ordre : on ne peut pas dire laquelle est « meilleure ».
- **La règle actuelle (A)** détecte le plus, y compris le changement brutal (91 %), mais déclenche une fausse procédure chez 17 % des équipages sans aucun changement et 6 % lors d'une simple amélioration. Elle n'est pas utilisable telle quelle.
- **EWMA (C)** garde 2,7 % de fausses procédures, 99 % de détection sur dérive progressive, mais **ne voit que 76 % des changements brutaux** dans une fenêtre de 3 jours. C'est sa faiblesse connue.
- **Hybride (I : EWMA ou règle B)** : 81 % sur changement brutal pour 4 % de fausses procédures. Gain apparent de 5 points sur le brutal, perte de 1,3 point sur les fausses procédures : non concluant à cette taille d'échantillon.
- **Écart-type rétréci (F)** : résultats très proches de C, légèrement meilleurs avec données manquantes (0,3 % contre 1,0 % de fausses procédures, 96,7 % contre 94,7 % de détection). Cohérent avec l'idée « partager prudemment l'information entre astronautes », mais l'effet est petit et non confirmé.
- **Kalman niveau local (G)** : peu de fausses alertes mais détecte seulement 38 % des changements brutaux. Pas d'avantage ici.
- **Mahalanobis (H)** : détecte 41 % de la dérive et 4 % du changement brutal, et déclenche 7,3 % sur une simple amélioration (test bilatéral). **Dans cette implémentation non réglée**, il n'est pas compétitif. Cela ne prouve pas que la méthode est mauvaise : son seuil n'a pas été optimisé.

## 5. Recommandations d'intégration

| Décision | Méthodes | Justification |
|---|---|---|
| **Moteur du hackathon** | Référence personnelle + EWMA, avec plancher d'écart-type et statut UNKNOWN | Meilleur compromis mesuré, simple, explicable, hors ligne, déjà testé |
| **Ajout possible si M1 le décide** | Hybride I (EWMA ou règle B) | Couvre mieux le changement brutal ; mais gain non concluant ; à ne retenir que si M2 a du temps et que les tests restent verts |
| **À répéter avant d'adopter** | Écart-type rétréci (F) | Gain petit ; relancer avec 1 000 équipages et variantes de nu0 |
| **Piste expérimentale (après hackathon)** | Mahalanobis réglé, PCA, Isolation Forest, HMM, modèle bayésien hiérarchique complet | Demandent beaucoup plus d'observations par personne ou une population ajustée, que nous n'avons pas |
| **Écartées pour l'instant** | Kalman niveau local | Pas d'avantage mesuré sur nos scénarios |

**Notre architecture est-elle assez ambitieuse ?** Pour 2 jours, oui : elle est testée, expliquée et tient hors ligne. Elle n'est pas « de pointe » au sens bayésien hiérarchique. Le dire clairement au jury est plus crédible que de prétendre l'inverse. Le test principal manquant, et le plus utile après le hackathon, est une validation sur de vraies séries longitudinales d'astronautes ou d'analogues.

## 6. Limites et affirmations interdites dans la présentation

- **Interdit :** « la NASA utilise EWMA / nos méthodes » ; « validé par la NASA » ; « détecte les problèmes de santé » ; tout chiffre de ce dossier présenté comme un résultat sur de vrais astronautes ; « Mahalanobis / Kalman ne fonctionnent pas » (seule notre implémentation non réglée est testée).
- **Permis :** « données NASA » (OSDR, télémétrie ISS) pour la partie réelle ; « dans l'esprit du défi méthodologique Artemis II : suivi individuel, petit effectif, incertitude explicite » ; « comparaison reproductible de 7 détecteurs sur équipages simulés ».
- **Limites techniques :** un seul générateur de bruit ; mêmes dérives pour toutes les personnes ; pas de rythme circadien complexe ; 10 jours seulement ; seuils non optimisés par méthode (sauf choix documentés).
- **Sources :** voir section 1 (liens) et `docs/HELP_CARD_SOURCES.md`.

---

## 7. Révision méthodologique (pilote 3) — 14/11/2026

Suite à la relecture externe (ChatGPT) du dossier. Tout est **synthétique** (générateur csync-synth-0.1), rien n'est validé sur données réelles.

### 7.1 Ce qui était faux ou non comparable dans les sections 4–5

- **Comparaison non calibrée.** Au pilote 2, chaque méthode avait un seuil « de bon sens » différent ; un seuil plus haut déclenche moins, donc paraît « meilleur ». Les comparaisons de la section 4 ne prouvent **pas** qu'une méthode est supérieure.
- **Métriques mélangées.** Le pourcentage d'équipages avec au moins une procédure ≠ taux de fausses alertes par astronaute-jour. Le pilote 3 les sépare.
- **Pas d'incertitude ni de délai.** Ajoutés : intervalles de Wilson à 95 %, délai médian de détection, tests de McNemar exacts appariés.

### 7.2 Protocole du pilote 3 (`research/pilot/pilot3.py`)

- Balayage de seuil par famille : règle (1.0–2.5), EWMA λ=0,3 (L 1,5–3,5), EWMA à écart-type rétréci, CUSUM k=0,5 (h 1,5–5), Kalman niveau local q=0,05 (L 0,5–2,5).
- Scénarios : témoin (300 équipages, graines 1000+), dérive graduelle 1,5 SD (150, graines 5000+, début jour 6), changement brutal 2 SD (150, graines 7000+, début jour 8, Attention + Morale).
- **Indépendance** : chaque équipage a sa propre graine, jeux de graines disjoints entre scénarios ; ils sont indépendants *au sein du modèle de bruit unique du générateur* (voir limites). Les tests appariés comparent les méthodes sur les mêmes équipages.
- Paramètres complets : voir `pilot3.py` (FAMILIES) ; sorties `pilot3_sweep.csv`, `pilot3_paired.csv`.

### 7.3 Résultat à fausses alertes égales (≈ 0,7 % d'équipages témoins déclenchant)

| Méthode (réglage) | Témoin | Dérive graduelle | Brutal 2 SD | Délai médian (grad./brutal) |
|---|---|---|---|---|
| Règle (d ≥ 1,5) | 0,7 % | 95,3 % | 59,3 % | 1 j / 1 j |
| EWMA (L = 3,0) | 0,7 % | 96,0 % | 51,3 % | 2 j / 2 j |
| EWMA rétréci (L = 3,0) | 0,7 % | 98,7 % | 52,0 % | 1 j / 2 j |
| CUSUM (h = 4) | 0,7 % | 95,3 % | 61,3 % | 2 j / 2 j |
| Kalman (L = 2,5) | 0,7 % | 95,3 % | 38,0 % | 2 j / 2 j |

À ≈ 2,5 % (règle 1,25 ; EWMA 2,5 ; CUSUM 3 ; Kalman 2,0) : 99–100 % en graduel pour tous, brutal 70–81 % (Kalman le plus bas, CUSUM le plus haut). Intervalles de confiance dans `pilot3_sweep.csv` : les écarts graduels sont dans le bruit ; les écarts brutaux entre Kalman et les autres dépassent l'IC.

Tests appariés (EWMA L=2,5 vs autre, seuils non égalisés) : voir `pilot3_paired.csv`. À lire avec prudence, car les taux de fausses alertes diffèrent entre les lignes comparées.

### 7.4 Réponses aux six points de la relecture

1. **Calibration équitable** : faite par balayage (7.3). Conclusion : à fausses alertes égales, règle stricte, EWMA, CUSUM sont **proches**. Aucun gagnant démontré.
2. **Délai et IC** : ajoutés (7.3 et CSV).
3. **Métriques séparées** : taux témoin (équipages), fausses procédures par astronaute-jour, détection, délai : colonnes distinctes.
4. **Indépendance / paramètres** : voir 7.2 ; limite : un seul modèle de bruit.
5. **Kalman** : son faible déclenchement (0,7 %) et ses 38 % de détection brutale sont **le même phénomène** : un seuil réglé trop haut (L=2,5). À L=2,0 : 2,7 % / 70 %. Ce n'est pas une « propriété » de Kalman. De plus, la réponse à l'échelon montre un lissage lent : niveau estimé 1,02 → 1,75 sur 5 jours pour un saut de 2 SD, avec une limite qui baisse ; il rattrape donc tard un changement brutal.
6. **Échecs d'EWMA** : changement brutal (délai +1 j vs règle, détection plus faible à L élevé) et fausses alertes très sensibles à L (32,7 % à L=1,5 contre 0,7 % à L=3,0). **Signaux contradictoires** (ex. une dimension monte, une autre baisse) : **non testés** comme scénario étiqueté ; limite ouverte.

### 7.5 Corrections de deux affirmations de la relecture

- « Conserver EWMA dans le moteur actuel » : **EWMA n'est pas dans le moteur** (`csync/rules.py` = règle v3 uniquement). C'est une recommandation en attente de la décision 1 de M1.
- Kalman « intéressant sur les changements brutaux » : c'est l'inverse dans nos données (le plus faible en brutal, 38 % à L=2,5).

### 7.6 Constat sur le moteur actuel (à décider par M1)

Mesuré sur 300 équipages témoins : `Params()` par défaut (seuil 1,0, sans plancher absolu) déclenche une procédure chez **17 %** des équipages sains ; avec planchers absolus, seuil 1,25 → 2,3 % (détection graduelle 100 %), seuil 1,5 → 0,7 % (95,3 %). Le réglage par défaut est donc trop sensible pour une démo « sans fausse alerte ». **Je n'ai rien modifié** : à valider par M1 (décision sur le seuil).

### 7.7 Décision technique retenue

- Moteur de production **inchangé** (règle v3, `Params()`).
- EWMA reste une **recommandation documentée**, non codée ; l'hybride et le rétrécissement ne sont **pas adoptés** (pas d'avantage mesuré).
- Aucune méthode ajoutée « pour faire sophistiqué ».

### 7.8 Limites restantes

Modèle de bruit unique ; pas d'étiquettes réelles ; pas de scénario de signaux contradictoires ni de données manquantes dans le pilote 3 ; seuils choisis sur les mêmes familles de scénarios que l'évaluation (risque de sur-ajustement léger) ; 23 tests = stabilité logicielle, pas validité scientifique.

### 7.9 Pistes après le hackathon

Calibration sur séries réelles (OSDR/HRP, accès à vérifier) ; modèle bayésien hiérarchique par astronaute ; scénarios contradictoires et capteurs manquants ; validation croisée des seuils ; relecture indépendante du code des pilotes (tâche Gemini G1).

### 7.10 Décision M1 appliquée (14/11, 06:30)

M1 a demandé le réglage « le plus juste scientifiquement ». Retenu : **seuil 1,5 + planchers absolus** (0,7 % d'équipages sains déclenchent ; détection graduelle 95,3 %, brutale 59,3 % — compromis assumé : un seuil plus bas détecte plus mais fausse-alerte plus). `Params()` porte désormais ces valeurs (`PROPOSED` en est un alias). Le moteur reste la règle v3 ; EWMA toujours non codée. Conséquence sur la démo : l'amplitude de dérive injectée dans le scénario « histoire » passe de 2,0 à **2,5** pour retrouver Attention DEGRADED au jour 7 (graine 42) ; c'est un paramètre du scénario synthétique, pas un résultat. Réserve : le seuil a été choisi sur les mêmes familles de scénarios que l'évaluation.

### 7.11 Relecture indépendante (autre IA, 14/11, sur commit dc61786) — ce qui est retenu

Livrables : audit des pilotes (raisonné, **non exécuté sur le banc complet**), ré-implémentation de la règle, d'EWMA et de CUSUM contre `docs/blocks/test_vectors_detectors.json` (**exécutée : 24/24 concordances**), catalogue de données NASA (**non vérifié : pas d'accès web**).
- **Retenu :** les trois détecteurs sont bien spécifiés ; à fausses alertes égales (0,7 %), EWMA (L = 3,0) et CUSUM (h = 4) ne font pas mieux que la règle (délai médian 2 j contre 1 j).
- **Ne pas citer :** les p-values de `pilot3_paired.csv` opposant EWMA L = 2,5 (2,7 % de fausses alertes) à la règle 1,5 (0,7 %) : les taux de fausses alertes ne sont pas égaux.
- **Vérifié par moi (Claude) le 14/11 :** la critique sur le scénario brutal (déclenchements avant l'injection, jours 6–7) est fondée mais sans effet sur les chiffres : 1 équipage sur 150 déclenche avant le jour 8, et la détection à partir du jour 8 reste 59,3 % (règle 1,5), 51,3 % (EWMA 3,0), 61,3 % (CUSUM 4) ; délais médians 1 / 2 / 2 jours.
- **Précision à garder :** `csync/rules.py` évalue 3 dimensions (Body, Attention, Morale) ; Mission et Habitat sont en contexte seulement.
- **Catalogue G2 :** à refaire avec accès web ; rien n'est utilisable tel quel.
