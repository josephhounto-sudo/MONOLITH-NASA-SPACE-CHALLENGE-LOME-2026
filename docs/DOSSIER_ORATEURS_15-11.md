---
title: "Dossier des orateurs — C-Sync (équipe MONOLITH)"
lang: fr
---
Dimanche 15/11/2026 · 5 minutes, sans questions du jury · diapos en anglais, pitch oral en français · orateur A = M1 (diapos 1, 2, 3, 6, 7), orateur B = M2 (diapos 4 et 5, démo en direct).

# 1. L'essentiel en une page

**C-Sync (Care Sync)** aide un équipage loin de la Terre, quand le sol met jusqu'à 22 minutes à répondre (NASA, NTRS 20220013418) et que les liaisons coupent des jours. Il fait trois choses : **repérer** une dérive par rapport à la référence de chaque astronaute, **guider** l'équipage pas à pas dans une urgence, **protéger la décision** de reprise (refus si la mesure est trop vieille). **L'humain décide toujours.**

| Chiffre | Valeur | D'où ça vient |
|---|---|---|
| Délai du sol | jusqu'à 22 min | NTRS 20220013418 |
| Règle | écart ≥ 1,5 écart-type, 2 jours de suite | `csync/rules.py` |
| Référence | les 5 premiers jours de chaque astronaute | idem |
| Limite de reprise | mesure de plus de 10 min = refus | `csync/gate.py` |
| Équipages sains testés | 0 sur 300 déclenchent une procédure | `research/pilot/holdout_results.json` |
| Dérives progressives repérées | 139 sur 150 (93 %) | idem |
| Changements brusques repérés | 86 sur 150 (57 %) : la limite connue | idem |
| Données NASA réelles | 759 525 points, 20 missions (cabine ISS) | onglet Evidence at scale |
| Tests automatiques | 205 | `python -m pytest -q` |

**Nouveautés du 15/11 à connaître (tout est dans l'app et les diapos) :**

1. **Diapo 2, objectif en quatre volets avec statut honnête** : guider l'urgence = fait ; aider le commandant = prototype (six équipiers simulés classés par urgence, il ne décide rien) ; données ouvertes NASA = fait, pour l'habitat seulement ; capteurs réels = prévu (l'app lit un format de données, aucun appareil n'est branché).
2. **Diapo 4, grande silhouette annotée** : thorax sélectionné, trois messages (douleur thoracique → procédure critique ; mesures guidées une à une ; rapport mis en file, livré une seule fois).
3. **Diapo 6, formes qui portent les vrais chiffres** : grille de 300 points (0 point allumé), deux anneaux (93 % et 57 %).
4. **Un seul code de formes partout** : cercle = normal, losange = surveillance, triangle = dégradé, carré tireté = inconnu. L'état n'est jamais dit par la couleur seule.
5. **Onglet « Commander board »** et **lecteur de flux d'appareil** (format seulement) dans l'app.
6. **Déclaration d'IA** : la diapo 1 nomme les images générées par IA (logo d'équipe, marque C-Sync).
7. **App en ligne** : elle se met à jour toute seule à chaque mise à jour du dépôt. C'est une version de test, pas le lien de soumission.

**À ne jamais dire :** « validé cliniquement » ; « connecté à la NASA en direct » ; « capteur réel branché » ; un montant de coût ; « il soigne » ou « il remplace le médecin ». **Phrase de repli :** « Nous ne l'avons pas encore vérifié, c'est notre prochaine étape. »

# 2. Lexique : tout ce qu'on peut vous demander d'expliquer

| Mot | Explication simple |
|---|---|
| Synthétique | Données inventées par notre générateur (version csync-synth-0.1), étiquetées partout. Aucun vrai astronaute. |
| Référence personnelle (baseline) | Le « normal » d'un astronaute, calculé sur ses 5 premiers jours. On compare chacun à lui-même. |
| Écart (d) | Distance entre aujourd'hui et la référence, mesurée en écarts-types. d ≥ 1,5 = signal. |
| NORMAL / WATCH / DEGRADED / UNKNOWN | Normal ; surveillance (1 indicateur sorti 2 jours de suite) ; dégradé (2 indicateurs ou plus) ; inconnu (donnée manquante, jamais affiché comme normal). |
| Procédure ouverte | Si 2 dimensions s'éloignent : fiche fixe (ex. PROC-FATIGUE-01) qui renvoie à la liste médicale de bord. Pas de traitement. |
| Dimensions | Corps, Attention, Moral (évalués) ; Mission et Habitat (contexte seulement). |
| Porte de reprise | Refuse la reprise du travail si la dernière mesure a plus de 10 min. |
| Override du commandant | Forçage enregistré dans le journal ; il ne suffit jamais seul à reprendre. |
| File d'envoi | Le rapport attend la liaison, puis part une seule fois (pas de doublon). |
| Commander board | Même règle sur six équipiers simulés, classés par urgence. Il ne décide rien. |
| Jeu tenu à l'écart (held-out) | Équipages simulés jamais utilisés pour régler la règle : le test honnête. |
| EDA / OSDR | Environmental Data App de la NASA : télémétrie de la cabine de l'ISS (CO2, température, humidité, radiation). |
| ARTIFACT | Valeur jugée suspecte par notre contrôle qualité (ex. CO2 constant pendant 153 h). Jamais affichée comme normale. |
| PH01, CO01… | Codes de nos indicateurs (ex. PH09 = sommeil, CO01 = temps de réaction). |

# 3. Texte complet du pitch (français, à dire)

Débit visé : 127 mots par minute en moyenne. La diapo 5 est volontairement lente (les deux clics de la démo). Si on est en retard, appliquer les lignes « coupe » : environ 14 secondes de gagnées.

### Diapo 1 · 0:00 → 0:25 (25 s) · orateur A
« À mi-chemin de Mars, un astronaute signale une douleur vive à la poitrine. Un message met jusqu'à vingt-deux minutes pour atteindre la Terre, et il n'y a pas de médecin à bord. Pendant ce délai, qui aide l'équipage à mesurer, à comprendre ce qui change, et à décider ? Nous sommes l'équipe MONOLITH, et notre réponse s'appelle C-Sync. »
**Transition :** clic sur « vingt-deux minutes ».

### Diapo 2 · 0:25 → 1:05 (40 s) · orateur A
« Un message met jusqu'à vingt-deux minutes pour atteindre la Terre, selon la NASA, et les coupures durent des jours. L'équipage est seul. Notre objectif a quatre volets. Guider l'urgence : fait. Aider le commandant : un prototype classe six équipiers simulés par urgence, et ne décide rien. Lire les données ouvertes de la NASA : fait, pour l'habitat seulement. Brancher de vrais capteurs : prévu ; l'application lit déjà un format de données, mais aucun appareil réel n'est branché. »
**Transition :** « Voici comment, en trois actes. »

### Diapo 3 · 1:05 → 1:55 (50 s) · orateur A
« Premier acte : une dérive lente. C-Sync compare chaque astronaute à lui-même, sur ses cinq premiers jours, et non à une norme universelle. Pendant ces cinq jours, aucune alerte de dérive n'est évaluée : la référence se construit, et l'écran le dit. Au jour sept de notre histoire simulée, le temps de réaction et les erreurs d'attention s'éloignent de sa référence deux jours de suite. La carte Attention passe en dégradée, et la carte Corps en surveillance : deux dimensions sortent de la normale. C-Sync affiche ce qui a changé, depuis quand, et avec quelle certitude. Il ouvre une procédure de fatigue et propose de revoir les signaux avec l'officier médical de bord. La décision reste humaine : elle est affichée en attente. »
**Transition :** passage de main à l'orateur B.

### Diapo 4 · 1:55 → 2:55 (60 s) · orateur B
« Deuxième acte, jour neuf : l'urgence de la vidéo du défi. L'astronaute signale une douleur vive à la poitrine. Une règle d'événement ouvre directement une procédure critique. L'écran guide les mesures, une par une : fréquence cardiaque, tension, température, glycémie. Pour chacune, il explique comment la prendre. La glycémie est marquée sans référence NASA en vol. C-Sync est conçu sans recommandation de médicament ni interprétation du symptôme : il enregistre les valeurs telles qu'elles sont mesurées, chacune avec son heure et son origine. Une phrase fixe rappelle de suivre la check-list médicale de bord et l'officier médical. Le compte rendu part dans une file d'envoi, et l'écran affiche l'état de la liaison. La liaison est coupée ; dès qu'elle revient, le rapport est envoyé une seule fois, sans doublon. À gauche, la silhouette de l'application : le thorax est sélectionné, l'habitat reste un simple contexte. »
**Transition :** « Le lendemain, l'équipage veut reprendre le travail. »
**Si on est en retard : coupe** la phrase « La glycémie est marquée sans référence NASA en vol. » (−9 mots, environ 4 s).

### Diapo 5 · 2:55 → 3:45 (50 s) · orateur B · DÉMO EN DIRECT
Manipulation : interface déjà ouverte au jour 10. Appui sur « Request resume », puis sur « Commander override ».
« Troisième acte, jour dix, en direct. Je demande la reprise. Refusée. [2 s de silence] Le commandant force la reprise. Le forçage est consigné dans le journal, mais la décision ne change pas : la dernière fréquence cardiaque date de quatorze minutes, la limite est de dix. Le système donne la raison en clair, sur l'écran. Une donnée périmée est signalée comme expirée, pas comme normale. Dans nos règles, un forçage seul ne suffit pas à reprendre. »
Démo en panne : si rien ne s'affiche en 10 secondes, passer à la capture C5 et dire le même texte.
**Transition :** retour au clavier de l'orateur A.

### Diapo 6 · 3:45 → 4:25 (40 s) · orateur A
« Nos preuves, dans l'esprit du défi méthodologique Artemis II : une référence individuelle. Nous avons réglé la règle sur un jeu d'équipages simulés, puis nous l'avons lancée, inchangée, sur trois cents nouveaux équipages en bonne santé : aucun n'a déclenché de procédure à tort. Dérives progressives : quatre-vingt-treize pour cent repérées. Saut brutal : seulement cinquante-sept pour cent, notre limite connue. Tout est simulé. Seule donnée réelle : la télémétrie de cabine de l'ISS, où notre contrôle qualité repère un CO2 constant pendant plus de six jours. »
**Si on est en retard : coupe** la dernière phrase (CO2 constant, −22 mots, environ 10 s).

### Diapo 7 · 4:25 → 5:00 (35 s) · orateur A
« Nos limites : l'équipage est simulé, rien n'est validé cliniquement. Les os, l'immunité et la dose de rayonnement reçue par l'équipage ne sont pas encore mesurés ; ils sont affichés comme inconnus. Nous avons choisi un moteur simple, testé et explicable, plutôt qu'une boîte noire. La suite : relecture des règles par des experts, essai sur des données de missions d'isolement simulé, puis de vrais capteurs. L'interface n'affiche que des écarts statistiques, sans qualification médicale. C-Sync : hors ligne, explicable, et c'est l'humain qui décide. Merci. »



# 4. Démo en direct (diapo 5)

1. L'interface est déjà ouverte au jour 10. 2. Clic sur **Request resume** : la décision est REFUSE_RESUME. 3. Silence de 2 secondes. 4. Clic sur **Commander override** : la ligne du journal dit que le forçage est enregistré et que la décision ne change pas. 5. **Si rien ne s'affiche en 10 secondes** : passer à la capture de la diapo et dire le même texte.

# 5. Questions possibles et réponses prêtes

(Le jury ne pose pas de questions pendant le pitch ; ces réponses servent après, aux organisateurs et aux visiteurs.)

###  Réponses validées (prêtes à dire)
1. Différence : « D'autres outils mesurent ou conseillent. Nous ajoutons la dérive par rapport à la référence personnelle, et le refus de reprise si la donnée est périmée. Nous complétons, nous ne remplaçons pas. »
2. Coût : « Logiciel sur ordinateur ou tablette. Nous n'avons pas chiffré, c'est la prochaine étape. » (aucun chiffre en euros)
3. Utilisateurs réels : « Pas encore. 205 tests automatiques et une histoire simulée de 10 jours. Aucune validation clinique. »
4. Données : « Équipage simulé, étiqueté synthétique partout, et télémétrie de cabine NASA pour le contrôle qualité. Aucune donnée de santé réelle. »
5. Impact : « Aujourd'hui : 0 faux déclenchement sur 300 équipages simulés tenus à l'écart, 93 % des dérives lentes repérées, 57 % des sauts brusques. Réglé sur des scénarios simulés : pas un résultat clinique. »
6. Hors ligne : « Le calcul est local, les comptes rendus attendent en file. Sans électricité, rien ne fonctionne ; procédures imprimées en suite. »
7. Si nous gagnons : relecture par des experts, vrais capteurs, essai sur données d'analogue (M1 confirme).
8. Règles plutôt qu'IA : chaque état renvoie à une règle lisible ; la décision reste humaine.
9. Seuils : paramètres de conception réglés sur des scénarios simulés, pas des seuils médicaux ; à valider par des experts.
10. Dérive ratée : limite assumée (57 % des sauts brusques seulement). Garde-fous : symptôme coché → procédure immédiate ; donnée manquante → UNKNOWN.
11. Capteur en panne : voir tableau C.
12. Fatigue dès le début : limite réelle, la référence serait faussée ; jours 1–5 sans alerte de dérive ; piste : mesures d'avant mission.
13. Responsabilité : l'humain. Compte rendu « en attente » ; override consigné, jamais suffisant seul.
Phrase de repli : « Nous ne l'avons pas encore vérifié, c'est notre prochaine étape. »
Ne jamais dire : « la NASA n'a rien » ; aucun coût, test réel ou résultat clinique.




###  Coût et ambition (réponses 2 et 7)
Coûts réels : **aucun chiffre dans le dépôt** (`TODO_M1`). Ce qui est établi : le logiciel tourne sur un ordinateur ou une tablette. Postes de coût à nommer sans montant : relecture par des experts, intégration, validation sur données d'analogue, capteurs (matériel de l'agence). Aucun montant à dire.
Les fiches du dépôt ne donnent que les rôles (M1 chef/PO et communication, M2 capsule de décision, M3 interface, M4 procédures et scénarios), pas les parcours personnels.
Ambition unique proposée (M1 confirme) : « Si nous gagnons, nous faisons relire les règles par des experts en médecine spatiale, puis nous les testons sur des données de missions d'isolement simulé. » Les capteurs réels et le reste viennent après.



# 6. Ce qui est fait, ce qui vient après

###  Ce qui est FAIT (preuve dans le dépôt)
| Élément | Preuve |
|---|---|
| Règle v3 : écart ≥ 1,5 ET sur la référence personnelle (jours 1–5), 2 jours consécutifs ; valeur manquante = UNKNOWN | `csync/rules.py`, `tests/` |
| Histoire de 10 jours en trois actes + variantes témoin et capteur en panne | `docs/STORY.md` |
| Urgence guidée (symptôme coché → CRITICAL immédiat) | `csync/rules.py` l.98 |
| Porte de reprise : refus si mesure > 10 min ; l'override du Commandant est consigné, jamais suffisant seul | `csync/gate.py` |
| Compte rendu « en attente de décision humaine », file d'envoi hors ligne sans doublon | `csync/capsule.py`, `csync/sendqueue.py` |
| Validation sur graines tenues à l'écart : 0/300 faux (0,0 %, IC 0,0–1,3 %), 92,7 % dérives lentes, 57,3 % sauts brusques | `docs/VALIDATION_HOLDOUT.md` |
| Données NASA réelles retraitées à l'ouverture : 759 525 points, 20 missions (télémétrie de cabine, pas de physiologie) | onglet « Evidence at scale », `csync/scale.py` |
| Valeur de CO2 constante ≈ 153 h (RR-1) signalée ARTIFACT | `docs/PREMORTEM_14-11.md` |
| App manipulable (saisie des jours 6–7, même règle, note SBAR) | onglet « Try it yourself », `csync/live.py` |
| 205 tests automatiques verts | `python -m pytest -q` |
| Silhouette cliquable en volume (SVG), verre v2, glyphes d'état | `csync/silhouette.py`, `csync/ui/style.py` |



**Après le pitch (rien de cela n'est affirmé comme fait) :**

###  Après le pitch (même liste que dans l'app et la diapo 7)
1. Relecture par des experts en médecine spatiale · 2. Essai sur données d'analogue · 3. Capteurs réels · 4. Référence avant mission · 5. Protection des données de santé · 6. Procédures imprimées · 7. Coût d'intégration à chiffrer.


