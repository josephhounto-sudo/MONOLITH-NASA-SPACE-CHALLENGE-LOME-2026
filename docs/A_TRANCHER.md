# À trancher — registre des décisions ouvertes (sam. 14/11, ~21:00 locale)

Sources : `docs/OPEN_DECISIONS.md`, `docs/PREMORTEM_14-11.md` §6–7, `docs/DEPLOIEMENT.md`, `docs/DESIGN_DIRECTION.md`, `docs/RELEASE_DRYRUN.md`, recherche automatique « À CONFIRMER / TODO_M1 / NON VÉRIFIÉ ».
Règle : rien de ce qui suit n'est appliqué tant que M1 n'a pas répondu par écrit. « Défaut » = ce qui se passe si M1 ne répond pas.

## État vérifié à 20:58 locale
- `main` = `8e03e59` ; 153 tests verts ; `check_consistency.py` : 0 erreur (le plantage 0x95 n'existe plus).
- Aucun nouveau commit de M2 ni de M3 sur origin (branches : main, m3-design, cursor-heavy-1). Leur état n'est donc PAS vérifié.
- Non vérifié : vidéo (absente), répétition chronométrée, test humain des 5 secondes, relecture de SUBMISSION.md par un tiers, V1 V2 V3 V5 V10 V12.

## A. À trancher ce soir (avant 22:30, GO/NO-GO)
| # | Question | Options | Recommandation | Défaut si silence | Réversible |
|---|---|---|---|---|---|
| A1 | Style : glass (défaut actuel) ou quiet ? | glass / quiet / test humain 5 s d'abord | Faire le test 5 s avec 3 humains (grille `DESIGN_TEST_5S.md`), puis choisir ; la mesure automatique ne tranche pas l'effet visuel | glass reste, m3-design non fusionnée | oui |
| A2 | Fusionner `m3-design` dans `main` ? | oui ce soir / dim. avant 09:30 / non | Oui, mais seulement après A1 et après `pytest` vert ; puis recapturer C1–C5, PDF, pptx (~20 min) | non fusionnée | oui (revert) |
| A3 | Règle de dérive (OPEN_DECISIONS n°1) : coder l'EWMA ? | non / oui | Non. Le gel est passé, la règle v3 est mesurée (0,7 % faux déclenchements) | v3 seule | non après gel |
| A4 | OPEN_DECISIONS n°2–8 : valider les défauts déjà codés ? | valider en bloc / ligne par ligne | Valider en bloc (réponse « 2–8 défaut ») : ils sont codés et testés ; ça ferme la colonne vide | colonne reste vide, défauts appliqués de fait | oui |
| A5 | D9 suppléant de soumission (Yves ou Youssouf) | Yves / Youssouf / aucun | Yves (a un compte GitHub actif) ; à fixer à 22:30 | pas de suppléant : risque R en cas d'indisponibilité de M1 | oui |
| A6 | Que faire de M3 et M2 s'ils ne livrent rien d'ici 22:30 ? | geler sans eux / attendre | Geler sans eux ; ne pas fusionner de travail non relu après 22:30 | gel sans eux | oui |

## B. À trancher dimanche matin (avant 09:30, gel du dépôt)
| # | Question | Recommandation | Défaut |
|---|---|---|---|
| B1 | Livrable : diapos (≤ 7, anglais, hébergées) ou vidéo ≤ 30 s | Diapos (D7 déjà accepté). Pas de vidéo : aucune n'existe et aucune musique n'a de licence notée | diapos |
| B2 | Tag Git de soumission (aucun tag n'existe) | Poser `v1.0-submission` sur le commit soumis | pas de tag |
| B3 | Mode démo « poignet » complet | Non : le gel est passé | non |
| B4 | Icônes d'état (? vs ○), formes d'état | Non, sauf si le test 5 s montre une confusion | inchangé |
| B5 | Masquer la ligne « Capsule file not found » | Oui, si c'est un correctif d'une ligne et testé ; sinon laisser | laisser |
| B6 | Silhouette : maquette statique étiquetée (déjà D5) ou retrait du pitch | Garder, étiquette honnête (déjà appliquée) | gardée |
| B7 | Déploiement en ligne de l'app (docs/DEPLOIEMENT.md, étapes 1–8) | Seulement si l'étape 1 prouve un lien public sans mot de passe ; sinon plan B du document | plan B |
| B8 | Relecteur indépendant de SUBMISSION.md et des textes du formulaire | M2 ou M4, 15 min | pas de relecture |

## C. Choses que seul un humain peut faire (pas des décisions)
- M4 : validation humaine des procédures (en-têtes « VALIDATION HUMAINE M4 : À FAIRE ») et V10.
- Répétition chronométrée (A 190 s, B 110 s), sans écran puis avec.
- Test 5 secondes (grille prête, captures `docs/design_ab/blind_5s/`).
- Confirmer par écrit (ou accepter le risque) V1/V2 : autorisation de démarrer avant 09:00 = orale seulement (D10, déjà accepté).

## D. Points que j'ai laissés ouverts et qui te concernent
- D1. Ré-attribution des commits de m3-design (auteur Team MONOLITH) : non fait, car cela réécrit un historique publié. À faire seulement si tu le demandes, sur m3-design uniquement.
- D2. DEV-03 (ordre des arrivées dans `ground_view`) : corrigé à ta demande, non relu par M2. À faire relire.
- D3. `TODO_M1` restants hors livrable principal : numéro de version EDA (`docs/pitch/FICHES_MESURES.md`), licence musique (`pitch/video/SHOTLIST_30S.md`), sources de 4 affirmations du rapport de rétro-ingénierie (délai Mars ~22 min, blackouts, capteur figé, 23 tests). À vérifier qu'aucune n'apparaît dans README ni dans les diapos ; je ne l'ai pas contrôlé exhaustivement.
- D4. Drapeau « bloqué » de la tâche M1-1 dans l'artefact : à confirmer ou lever.

## Format de réponse (une ligne)
`A1 glass|quiet|test · A2 oui|non|dim · A3 non · A4 oui · A5 Yves|Youssouf|aucun · A6 geler · B1 diapos · B2 oui|non · B3 non · B4 non · B5 oui|non · B6 garder · B7 plan B|ligne · B8 M2|M4 · D1 oui|non`
