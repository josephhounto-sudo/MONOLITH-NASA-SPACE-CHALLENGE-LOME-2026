# Grille de critères et test des 5 secondes — écrans C-Sync (14/11/2026 21:00 UTC)
FAIT PAR L'IA. Les critères ci-dessous ont été écrits **après** les captures et après que l'IA a vu les écrans (elle ne les a pas notés) et **avant** tout avis humain. Ce n'est donc pas un protocole aveugle côté IA ; il l'est côté testeurs.

## Grille de 8 critères (notes 1 à 5, par un humain)
1. **État lu en 5 s** : le testeur dit quelles dimensions sont hors normal, sans aide.
2. **Hiérarchie** : il désigne la chose la plus importante de l'écran, et c'est la bonne (les états ou la décision).
3. **Inconnu ≠ normal** : il distingue les cartes « Context only » des cartes évaluées.
4. **Lisibilité à distance** : texte du « Why this view » lisible à 2 m (projecteur ou écran à bout de bras).
5. **Calme** : rien ne distrait de la lecture (mouvement, décor).
6. **Cohérence** : espacements, alignements, tailles égales pour les choses égales.
7. **Caractère** : le testeur décrit l'écran avec ses propres mots ; compter les mots utiles (« instrument », « fiable », « spatial »…) contre « générique », « template ».
8. **Confiance** : « confieriez-vous une décision médicale à cet outil ? » (1 non, 5 oui).

## Protocole (3 à 5 personnes qui n'ont jamais vu le projet ; pas M1)
Matériel : `docs/design_ab/blind_5s/` (6 images, noms neutres `jour7_X`, `jour7_Y`, …). **Ne pas ouvrir `blind_5s_KEY_ne_pas_montrer.json` avant la fin.**
1. Montrer `jour7_X` pendant 5 s, puis la cacher. Poser : « Que se passe-t-il ? Qu'est-ce qui vous a frappé ? » (critères 1, 2, 3, 7). Noter les mots exacts.
2. Montrer `jour7_Y` 5 s, mêmes questions. Alterner X/Y en premier d'un testeur à l'autre.
3. Remontrer chaque image sans limite : critères 4, 5, 6, 8 (notes 1 à 5).
4. Répéter avec les jours 9 et 10 si le temps le permet.
5. Question finale : « Laquelle donne le plus l'impression d'un outil sérieux pour un équipage ? Pourquoi ? »
Résultat : tableau testeur × image × critère, puis ouvrir la clé et attribuer X/Y aux profils. **Un écart de moins de 2 voix sur 5, ou des notes à moins de 0,5 point, ne départage pas.**

## Limites
3 à 5 personnes ne donnent pas de statistique. Les captures sont à 1280 px sur écran de bureau, pas sur le projecteur de Lomé. Les captures du deck ne correspondent à aucun des deux profils.

## v2 — 15/11/2026 ~07:40 : fusion contre signal (critères écrits AVANT tout avis humain)
Matériel : `docs/design_ab/blind_5s_v2/` (premier écran 1280×900, jours 7, 9 étape 3, 10 après « Request resume »), X/Y tirés au hasard (graine 20261115). **Clé : `blind_5s_v2_KEY_ne_pas_montrer.json`, à ouvrir seulement à la fin.** 3 à 5 personnes qui n'ont jamais vu le projet, pas M1 ni l'IA.
Questions, image montrée 5 s puis cachée : (a) « Que se passe-t-il ? » (b) « Qu'est-ce qui demande une action maintenant ? » (c) « Trois mots pour décrire l'écran. » Puis sans limite de temps : critères 4 à 8 de la grille ci-dessus (notes 1 à 5).
**Succès écrit d'avance pour la version retenue** : au jour 9, au moins 4 personnes sur 5 citent l'urgence (douleur thoracique / procédure guidée) en (b) ; au jour 10, au moins 4 sur 5 citent le refus de reprise ; au jour 7, au moins 4 sur 5 nomment Attention (ou « dégradé »). Un écart de moins de 2 voix sur 5 entre X et Y ne départage pas.
Biais connu : à 1280×900, la version « signal » cache l'urgence sous la ligne de flottaison ; la question (b) avantage donc la fusion par construction — c'est ce que l'on veut mesurer (la hiérarchie), pas l'esthétique. Pour l'esthétique seule, comparer les réponses (c) et le critère 7.
