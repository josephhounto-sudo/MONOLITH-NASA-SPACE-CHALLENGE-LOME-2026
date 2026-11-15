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

---
## Décisions de M1 reçues le 14/11 21:30 (écrites par lui) et suite donnée

| # | Réponse de M1 | Suite |
|---|---|---|
| A1 | « glass un peu de quiet » | Profil `hybrid` construit sur `m3-design` (4035e4d) : glass gardé sur les cartes, sans mouvement, sans majuscules, sans flou sur les contrôles ; axe 0 violation (jours 7/9/10, avec et sans animations) ; 153 tests verts. Défaut `CSYNC_STYLE=hybrid`. **Pas de test humain fait** : l'effet visuel reste à juger par 3 personnes. |
| A2 | « oui comme tu l'as dit » | Fusion dans `main` seulement après : test 5 s (ou décision explicite de M1 de s'en passer), tests verts en clone neuf, tag de retour posé juste avant. Pas encore fusionné. |
| A3 | « oui avec Gemini puis on perfectionne » | **Non appliqué, désaccord noté.** Raison : le gel est passé, la règle v3 est mesurée (0,7 % de faux déclenchements) ; une autre règle la veille du dépôt n'a ni test ni relecture. Proposition : tester l'EWMA à part, dans `research/`, sans toucher `csync/rules.py`. |
| A4 (2e « A3 ») | « pour et contre, prends les plus optimisées » | Voir tableau ci-dessous. |
| A5 | Yves | Noté. Yves doit en être informé : il n'a pas encore confirmé (rien de lui visible). |
| A6 | « M2 vient de livrer, si joint » | **Rien de M2 visible sur GitHub** (origin : main, m3-design, cursor-heavy-1 ; aucun nouveau commit). À pousser par M2 ou à joindre via un ZIP. |

**M3 (Youssouf) : constat.** Son dossier est un clone de `main` (branche locale `m3-nominal`, aucun commit à lui). Seul changement : `csync/ui/app.py` modifié, non commité (polices agrandies, états forcés « UNKNOWN » les jours ≤ 5 même si l'état est calculé, journal de reprise retiré de l'encart technique). Copié sur une copie de `main` : **3 tests d'interface échouent** (cartes Body jours 7, 9, 10). Non intégré. Son objectif (cartes plus lisibles) est déjà couvert par `m3-design`.

**Pour / contre des points B (décidé sauf avis contraire)**
| # | Décision | Pour | Contre |
|---|---|---|---|
| B1 | Diapos (≤ 7), pas de vidéo | existent, relues, PDF + pptx de secours ; la vidéo n'existe pas et la musique n'a pas de licence | moins vivant ; la démo se fait en direct |
| B2 | Tag `v1.0-submission` + tag de retour avant fusion | retour en une commande ; preuve de ce qui est soumis | aucun |
| B3 | Pas de mode poignet complet | gel passé, risque de régression | démo moins riche |
| B4 | Icônes/formes d'état inchangées | tests et captures cohérents | si le test 5 s montre une confusion, trop tard (corrigeable seulement avant 09:30) |
| B5 | Masquer « Capsule file not found » : oui si 1 ligne testée | enlève un message qui ressemble à une panne | toucher l'interface après gel ; à faire dans m3-design seulement |
| B6 | Silhouette : maquette étiquetée gardée | honnête, déjà appliqué | non codée dans l'app |
| B7 | Plan B de déploiement tant que le lien public n'est pas prouvé | pas d'engagement non vérifié | pas d'app en ligne |
| B8 | Relecteur M4 (M2 occupé) pour SUBMISSION.md | regard neuf, 15 min | M4 n'a pas validé ses propres procédures encore |

## Avis sur les points « ouverts »
1. **Réattribuer les commits de `m3-design` : non.** Cela réécrit un historique publié sur la branche que M3 peut déjà avoir tirée ; gain purement cosmétique. L'AI_USAGE.md dit déjà que l'IA a écrit ces commits.
2. **DEV-03 relu par M2 : oui, avant la fusion.** C'est une correction de logique (ordre des arrivées) faite par moi et non relue ; 5 minutes pour M2 ou M4.
3. **Drapeau « bloqué » de M1-1 : le lever seulement si D9 (suppléant) est tranchée.** Avec Yves désigné, elle l'est : à toi de lever dans l'artefact.
4. **`TODO_M1` secondaires :** vérifier avec une recherche que « EDA version », la licence musique et les 4 affirmations non sourcées (délai Mars ~22 min, blackouts de semaines, capteur figé, « 23 tests ») n'apparaissent ni dans le README ni dans les diapos. Je lance la recherche ci-dessous.

**Résultat de la recherche TODO_M1 (14/11 21:45)**
- `pitch/deck/deck_final.html` ligne 109 et `pitch/deck/SCRIPT_EN.md` ligne 14 : « blackouts that can last weeks (NASA) » / « NASA also expects communication blackouts that can last weeks ». `SOURCES.md` cite le rapport NTRS 20220013418 (délai ~22 min) ; **la durée « semaines » n'y est pas confirmée, et je n'ai pas pu lire la page NTRS (accès non accordé). NON VÉRIFIÉ.** Recommandation : ouvrir l'abstract NTRS ; si « semaines » n'y est pas, remplacer par « Communication blackouts (NASA ASCEND study) » dans la diapo 2 et le script, puis refaire PDF/pptx.
- `deck.html` ligne 89 : `LOGO_À_FOURNIR` (deck.html seulement ; `deck_final.html` est propre d'après `test_deck.js final`).
- Aucune occurrence de « capteur figé », « 23 tests », « 22 min » dans README ni SUBMISSION.md. Version EDA et licence musique : hors livrable (fiches et vidéo non soumises).
