# FICHIER : REVERSE_ENGINEERING_REPORT.md
Version : v1 · Date/heure : samedi 14/11/2026, 06:00 (Lomé, UTC+0)
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Base : uniquement « BLOC MAQUETTE & PITCH C-SYNC v1 ». Vidéo officielle NON vue, transcription NON disponible.
TODO_M1 restants : voir section F (questions bloquantes) et les mentions `TODO_M1` du texte.

Note : ce rapport est interne. Il cite des mots interdits (« diagnosis », « cause »…) uniquement pour signaler où ils apparaissent. Ils ne doivent figurer dans aucun texte affiché ni parlé.

---

## Verdict en 6 lignes
1. **Le plus gros trou de pertinence** : la vidéo demande que l'outil explique *comment prendre chaque mesure, pourquoi elle compte, quoi faire si elle sort de l'ordinaire*. C'est le cœur de la demande, et **aucune diapositive actuelle ne le montre**. La silhouette (l'exemple donné par l'énoncé) n'est dans aucune diapositive et dans aucune fiche de tâche.
2. **Le plus gros risque de validité** : la diapositive 6 présente l'EWMA (2,7 %), alors que rien ne dit que le logiciel démontré utilise l'EWMA. Si l'application tourne encore avec la règle A (17 %), le chiffre affiché décrit un détecteur qu'on ne montre pas.
3. **Des mots interdits sont déjà présents** dans les textes existants (« no cause, no diagnosis », « No diagnosis. »), alors que la règle les interdit même à la forme négative.
4. **Le storyboard v3 est obsolète sur 6 points** : durée, questions, maquette, ordre des actes, jour de la capsule, « collapses ».
5. Plusieurs chiffres affichés **n'ont pas de source dans le bloc** : environ 22 min, « blackouts of weeks », « frozen sensor caught », « 23 tests ».
6. **La tension entre « traitement » et « diagnostic » doit être assumée à l'écran.** Si on ne l'explique pas, le jury verra une exigence absente. Expliquée, elle devient un argument (« quand alerter qui »).

---

## A. Ce que le défi exige (énoncé officiel, d'après le résumé de M1 du 13/11)
Toutes les citations sont le « résumé de M1 » en français. La seule citation anglaise est le titre du défi. Couverture : C = couverte, P = partielle, A = absente, A* = absente par choix (règle non négociable).

| # | Exigence | Source | Réponse C-Sync actuelle | État |
|---|---|---|---|---|
| A1 | Outil **visuel** qui rassemble des indicateurs de santé | « Create Health Monitoring Software for Astronauts on Space Missions » + résumé M1 | 5 dimensions et 4 états | C |
| A2 | Permettre à l'astronaute **d'évaluer son état et d'agir** | résumé M1 | Capsule de décision (ce qui a changé, quand, à quel point on est sûr, action) + « Human decision: pending » | C |
| A3 | **Conseils de traitement** et d'amélioration de la santé | résumé M1 | Aucun traitement ni médicament. On le remplace par des actions de prévention et la règle « quand alerter qui » | A* (à expliquer à l'écran) |
| A4 | Indicateurs cités : FC, sommeil, humeur | résumé M1 | Présents (Acte 1) | C |
| A5 | Indicateurs cités : tension, température, glycémie | résumé M1 | Décidés « dans le MVP » (saisie clavier, urgence guidée). État réel dans le code inconnu | P · `TODO_M1` |
| A6 | Données type images (échographie) | résumé M1 | Rien | A (à citer comme limite, pas à promettre) |
| A7 | Saisie clavier / clics / caméra | résumé M1 | Clavier : check-in quotidien. Clics : dépendent de la silhouette. Caméra : rien | P |
| A8 | Quelles mesures sont **faisables dans l'espace** ? | résumé M1 | Fiches « comment mesurer, pourquoi » décidées, contenu non vu | P · `TODO_M1` |
| A9 | **Pourquoi** un examen est nécessaire ? | résumé M1 | Même fiches | P |
| A10 | Comment les **5 dangers** affectent les indicateurs | résumé M1 | Distance → délai de 20 min ; isolement → humeur, attention ; environnement fermé → Habitat (télémétrie ISS). Rayonnement et gravité (os, immunité) : non mesurés | P |
| A11 | **Quand** un résultat mérite l'attention de l'équipage ou des chirurgiens de vol | résumé M1 (en capitales dans l'énoncé) | IMPORTANT → officier médical de bord ; CRITICAL → chirurgien de vol | C (décidé) · à montrer à l'écran |
| A12 | Actions qui **préviennent un état critique** | résumé M1 | Conseils d'action explicites décidés, contenu non vu | P · `TODO_M1` |
| A13 | Présenter clairement les mesures (l'énoncé dit aussi « diagnosis ») | résumé M1 | Présentation claire : C. Partie « diagnosis » : A* | C / A* |
| A14 | Exemple d'interface : **silhouette humaine cliquable** | résumé M1 | Décidée dans le MVP, attribuée à personne | A dans le code |
| A15 | Animations, interactivité | résumé M1 | Inconnu | P |
| A16 | Facultatif : environnements variés (vaisseau, station, rover, base) | résumé M1 | Seulement « vol vers Mars » + télémétrie ISS | P |
| A17 | Facultatif : rappels de mesure | résumé M1 | Décidé | P |
| A18 | Facultatif : gamification | résumé M1 | Rien. À ne pas ajouter, c'est hors priorité | A |
| A19 | Facultatif : graphiques dynamiques dans le temps | résumé M1 | Décidé | P |
| A20 | Facultatif : code couleur lisible d'un coup d'œil | résumé M1 | Couleur + icône + mot | C |
| A21 | Facultatif : instructions simples (mesures, indicateurs, risques) | résumé M1 | = A8/A9 | P |
| A22 | Citer les ressources HRP (Hazards, Risks, Ongoing Research) | section 3.1 | « Chaque fiche cite sa page HRP » décidé, pages précises non attribuées | P · `TODO_M1` |
| A23 | Règle d'événement : au moins une source NASA dans les ressources | section 3.7 | NASA OSDR Environmental Data App | C |
| A24 | Règle d'événement : décrire l'usage de l'IA | section 3.7 | AI_USAGE.md + ce journal | C |

---

## B. Ce que la vidéo exige (d'après la section 3.1 seulement)
**Ce que l'on sait** :
- B1. Le scénario : à mi-chemin de Mars, un coéquipier ressent une **douleur vive à la poitrine**.
- B2. La demande : un logiciel qui aide à **évaluer** la santé **et** **guide quoi faire**.
- B3. « Les astronautes ne sont pas des médecins », donc pour chaque mesure : **comment la prendre, pourquoi elle compte, quoi faire si elle ne paraît pas normale**.

**Couverture actuelle** : B1 → Acte 2 (C). B2 → Acte 2, étapes guidées (C pour « guide », P pour « évaluer »). B3 → **aucune diapositive** ; la diapo 4 dit « measurements one by one » sans le « comment / pourquoi / quoi faire ».

**Ce que je ne peux pas savoir sans la transcription** :
1. Le coéquipier reste-t-il conscient ? (Le storyboard dit « collapses ». S'il s'effondre, il ne peut plus faire ses propres mesures et le scénario change.)
2. La vidéo cite-t-elle des mesures précises (ECG, tension, saturation…) ?
3. Cite-t-elle un délai de communication chiffré ?
4. Parle-t-elle du chirurgien de vol ou de l'officier médical ?
5. Parle-t-elle de traitement, de médicaments, de trousse médicale ?
6. Attend-elle un livrable précis (application, maquette, prototype) ?
7. Durée, auteur, phrases exactes reprenables en citation de moins de 15 mots ?
8. Montre-t-elle une interface de référence (et donc un style à éviter de copier) ?

---

## C. Modèle humain / silhouette cliquable, décomposé
Règles appliquées : aucun seuil clinique, aucun traitement. « Quand alerter » repose **uniquement** sur la logique C-Sync : écart à la référence personnelle → WATCH/DEGRADED ; symptôme déclaré par règle d'événement → CRITICAL ; donnée absente → UNKNOWN.

| Région (id proposé) | Mesure faisable à bord | Pourquoi elle compte (danger HRP) | Comment la prendre | Quand alerter | Page HRP | Procédure liée |
|---|---|---|---|---|---|---|
| Tête `region-head` | Heures de sommeil, humeur, vigilance (auto-évaluation au clavier) ; température corporelle | Isolement et confinement → santé comportementale ; distance de la Terre | Check-in quotidien ; thermomètre (saisie de la valeur) | Dérive par rapport à la référence sur plusieurs signaux → capsule, puis officier médical de bord (IMPORTANT) si 2 dimensions hors NORMAL | `TODO_M1` (risque santé comportementale / sommeil) | Acte 1, capsule de dérive |
| Poitrine `region-chest` | Fréquence cardiaque ; symptôme « douleur thoracique » (saisie) | Événements cardiovasculaires | Capteur ou prise manuelle ; déclaration du symptôme | Symptôme déclaré → CRITICAL immédiat → chirurgien de vol (compte rendu en file, 20 min) | `TODO_M1` (risque cardiovasculaire) | Acte 2, procédure d'urgence |
| Bras `region-arm` | Tension artérielle | Événements cardiovasculaires | Brassard, saisie au clavier, étapes guidées | Dans l'urgence : valeur jointe au compte rendu. Hors urgence : écart à la référence. Aucun seuil absolu | `TODO_M1` | Acte 2 |
| Main / doigt `region-hand` | Glycémie | Nutrition insuffisante | Glucomètre, saisie en mg/dL | **Aucun seuil.** Étiquette « sans référence NASA en vol ». Affichage seulement | `TODO_M1` (risque nutrition) | Aucune |
| Abdomen `region-abdomen` | Aucune mesure dans le MVP | Nutrition | — | État UNKNOWN affiché | `TODO_M1` | Aucune |
| Jambes / os `region-legs` | **Non mesuré** | Champs de gravité → perte osseuse | — | UNKNOWN permanent, signalé comme limite | `TODO_M1` | Aucune |
| Corps entier `region-body` | **Non mesuré** : immunité, dose de rayonnement | Rayonnement ; changements immunitaires | (Dosimétrie : ressource CSA citée par l'énoncé, non intégrée) | UNKNOWN permanent, signalé comme limite | https://www.nasa.gov/hrp/hazards/ (générique) | Aucune |
| Hors corps `region-habitat` | Télémétrie cabine ISS **réelle** | Environnement fermé et hostile | Données OSDR | Capteur figé ou valeur absente → UNKNOWN (« frozen sensor », source `TODO_M1`) | https://www.nasa.gov/hrp/hazards/ | Aucune |

**Faisable en 2 jours** :
- Silhouette SVG originale (de face, neutre, sans visage) avec 7 régions + une zone Habitat. Chaque région a un `id`, un état (couleur + icône + mot) et un lien vers une fiche « comment / pourquoi / quand alerter ».
- Liste de repli au clavier (mêmes ids, même ordre, lisible par un lecteur d'écran).
- Régions non mesurées affichées en UNKNOWN : c'est notre règle « UNKNOWN jamais présenté comme normal » rendue visible. C'est un argument, pas une faiblesse.

**Pas faisable** : 3D, plusieurs postures, saisie par caméra, échographie, seuils cliniques, contenu médical validé.

**Risque principal** : si M3 n'intègre pas la silhouette avant la capture des écrans, on ne pourra la montrer qu'en **WIREFRAME déclaré**. Dans une démo jugée sur la « Validité », un wireframe à côté de captures réelles affaiblit le tout. Il faut décider maintenant : on l'implémente, ou on la sort du pitch.

---

## D. Correspondance critères ↔ diapositives (plan actuel, section 3.3)

| Critère | Diapo(s) qui le démontrent | Preuve disponible | Faiblesse |
|---|---|---|---|
| Impact | 2 (problème), 4 (urgence) | Délai de 20 min (démo) ; scénario de la vidéo officielle | « ~22 min » et « blackouts of weeks » sans source dans le bloc |
| Créativité | 3 (référence personnelle), 5 (reprise refusée même avec un override) | Porte de reprise 13/13 (simulé) | Acte 3 = l'idée la plus originale, mais 30 s seulement |
| Validité | 6 (méthode), 7 (limites) | Tableau du pilote (A–E), IC 1,4–5,2 %, 300 témoins ; télémétrie ISS réelle | Détecteur montré ≠ détecteur démontré ? 76 % sur changements brutaux non dit ; « 23 tests » sans source |
| Pertinence | 2, 4 | Scénario de la vidéo repris | **Pas de silhouette, pas de « comment mesurer / pourquoi », pas d'explication du refus de traiter** : les trois points que l'énoncé et la vidéo nomment explicitement |
| Présentation | Ensemble ; démo en direct | — | Diapo 6 surchargée (bien plus de 25 mots) ; durée de démo en direct non planifiée |

---

## E. Incohérences et trous (listés, non corrigés)
**Format et programme**
1. Storyboard v3 : pitch de 3 minutes avec deux réponses préparées. Programme officiel : **5 minutes, sans questions**.
2. Storyboard : « Jamais de maquette ». Bloc, règle 5 : wireframes étiquetés autorisés tant que le logiciel n'existe pas. Il reste à décider si un wireframe peut figurer dans la **version finale**.
3. Moment des captures : plan du pitch « samedi 22:30 », storyboard « dimanche 10:30–11:30 ».
4. « 7 diapositives OU vidéo de 30 s » (format de démo pour la soumission) et « pitch oral de 5 min » sont deux livrables différents. Lequel est soumis : l'un, l'autre, les deux ? Guides 2026 « à reconfirmer ».
5. Démo en direct : le storyboard prévoit l'ancien SC-10 en direct. Rien n'est prévu dans le minutage de 5:00 ni comme repli si la démo plante.
6. « M1 + un second membre » à l'oral : qui ? M5 est déjà tenu par M1, donc la charge de M1 est critique dimanche matin.

**Récit**
7. **Ordre des actes** : le storyboard met l'urgence (SC-12) avant la dérive (SC-02) ; le pitch met Dérive → Urgence → Reprise.
8. Storyboard plan 4 : « capsule du **jour 10** » pour la dérive. Or la dérive couvre les jours 6–9, la première procédure arrive au jour 7, et le jour 10 est celui de l'Acte 3.
9. « Human decision **required** » (storyboard) vs « Human decision: **pending** » (projet).
10. « a crewmate **collapses** » (storyboard) vs « douleur vive à la poitrine » (vidéo, résumé M1). C'est une dramatisation non sourcée, qui contredit en plus l'idée qu'il fait lui-même ses mesures guidées.
11. Codes SC-02 / SC-12 / SC-10 encore utilisés comme titres de plans.
12. Silhouette décidée « dans le MVP », absente de toutes les fiches de tâche, et pourtant montrée en capture dans le plan 3 du storyboard.

**Mots interdits déjà présents**
13. Storyboard plan 4 : « No **diagnosis**. »
14. Pitch diapo 3 : « no **cause**, no **diagnosis** ».
15. Storyboard : réponse préparée « Est-ce un **diagnostic** ? » (devient sans objet puisqu'il n'y a plus de questions).
16. Soumission : « helps a deep-space crew notice unusual changes in their health ». C'est proche de l'interdit « détecte les problèmes de santé » ; à relire.
17. Diapo 7 : « CDSS integration » (Clinical Decision Support System). Le terme évoque le diagnostic ; à reformuler ou à justifier.
18. Diapo 6 : « Same principle as the winners of NASA HRP's Artemis II… ». C'est plus proche d'un appui que la phrase autorisée. Utiliser la formule autorisée de la règle 3.

**Chiffres**
19. « Mars delay up to ~22 min one way » : pas de source dans le bloc → `TODO_M1`.
20. « blackouts of weeks » : pas de source → `TODO_M1`.
21. « frozen sensor caught » : pas de source dans le bloc → `TODO_M1`.
22. « 23 tests passent » : pas de fichier source dans la section 3 → `TODO_M1`.
23. « EWMA 99 % » : le tableau dit 99,3 %, et pour une dérive de **1,5 écart-type** seulement. La diapo 6 doit le préciser, sinon le chiffre est trompeur.
24. Section 3.6 : l'EWMA détecte seulement **76 %** des changements brutaux en 3 jours. Ce chiffre n'apparaît nulle part dans le pitch. L'omettre est un risque de validité.
25. **Le détecteur du logiciel démontré** (A ou C ?) n'est dit nulle part. La recommandation EWMA reste « décision pour M1 ».
26. Section 1 : « 150 à 300 équipages simulés par scénario ». Les chiffres de la section 3.5 viennent de 300 témoins et 150 dérives : cohérent, mais à afficher tel quel.

**Énoncé non traité**
27. « Conseils de traitement » : le refus est décidé mais n'est expliqué dans aucune diapositive.
28. Les fiches « comment mesurer / pourquoi » et les « conseils d'action » : décidés, contenu non fourni.
29. Pages HRP précises par risque : non attribuées.
30. Échographie, caméra, os, immunité, rayonnement : à lister en limites (la diapo 7 cite seulement « os et immunité » dans le repli du storyboard).
31. Logo `LOGO_ACTUEL` : non fourni. Licence de la musique : non choisie.

---

## F. Questions bloquantes pour M1
1. **Transcription ou sous-titres de la vidéo officielle** : peux-tu les coller ? Sans eux, la section B reste incomplète, en particulier la question 1 (conscient ou effondré).
2. **Silhouette** : qui l'implémente, et sera-t-elle dans le vrai logiciel au moment des captures ? Si non : (a) wireframe déclaré dans le pitch, ou (b) retirée du pitch ?
3. **Détecteur dans le logiciel démontré** : règle A ou EWMA ? Cela décide ce que la diapo 6 a le droit d'afficher.
4. **Livrable de démo pour la soumission** : 7 diapositives, vidéo de 30 s, ou les deux ? Et que montre-t-on dimanche à 12:00 : diapositives + démo en direct de quel acte ?
5. **Ordre des actes** : Dérive → Urgence → Reprise (pitch) ou Urgence d'abord (storyboard, plus proche de la vidéo) ?
6. **Sources** pour : ~22 min, « blackouts of weeks », « frozen sensor caught », « 23 tests ».
7. **Captures** : samedi 22:30 ou dimanche 10:30 ?
8. **Logo et couleurs** : peux-tu fournir `LOGO_ACTUEL` et la palette, ou je propose une palette neutre en variables CSS ?

---

## G. Plan de la phase 2 (après « VALIDATION PHASE 1 »)
Un livrable par réponse, dans cet ordre (« SUITE » pour passer au suivant). Chaque réponse met aussi à jour `CHANGELOG.md` et `AI_USAGE_LOG.md`.

| Ordre | Fichier | Contenu | Espaces réservés |
|---|---|---|---|
| 1 | `pitch/deck/slides.md` | 7 diapositives (≤ 25 mots chacune), visuel, source de chaque chiffre, notes d'oral en français, total 5:00. Proposition : la silhouette + « how to measure / why / when to alert » entrent dans la diapo 4 ; l'explication du refus de traiter va en diapo 4 ou 7 ; 76 % et l'IC vont en diapo 6 | `[CAPTURE RÉELLE à insérer : écran X]` pour chaque écran |
| 2 | `pitch/video/storyboard.md` | v4 : 30,0 s, sous-titres EN sans mots interdits, ordre et jours corrigés | Captures |
| 3 | `pitch/assets/*.svg` + `pitch/assets/README.md` | Silhouette (ids de la section C), schéma Terre ↔ Mars 20:00, schéma 5 dimensions, schéma porte de reprise. Couleurs et textes en variables CSS | Logo |
| 4 | `pitch/build_deck.py` | Python 3 standard → `pitch/deck.html` (clair/sombre, téléphone, clavier) + commande et résultat attendu | — |
| 5 | `pitch/CHECKLIST_PRESENTATION.md` | Mots interdits EN/FR, filigrane IA, SYNTHETIC DATA, aucun nom ni numéro, licence musique, chiffres sourcés, critères | — |
| 6 | `pitch/SPEC_SILHOUETTE.md` | Régions, ids, états, liens vers mesures et procédures, liste de repli, accessibilité, pour M3 | Pages HRP `TODO_M1` |

Restent en espace réservé jusqu'à fourniture : toutes les captures réelles, le logo, la musique, les pages HRP précises, les sources des chiffres listés en E19–E22.

---

PHASE 1 TERMINÉE — j'attends VALIDATION PHASE 1
