# Pré-mortem C-Sync — sam. 14/11/2026 ~14:15 UTC
Statut : FAIT PAR L'IA (Claude) — **chaque solution marquée « D# » attend la confirmation de M1** ; rien de ce qui change un chiffre, une phrase du script ou une diapo n'a été appliqué.
Question posée : « Dimanche 14:00, le pitch a échoué. Pourquoi ? » Reste ≈ 22 h avant le créneau (dim. 12:00–14:00), 5 min, sans questions du jury ; dépôt avant dim. 23:59.

## 1. Vérifié aujourd'hui (faits, pas avis)
- Série brute EDA RR-1, CO2 ISS (5 min) : valeur **2646 ppm constante du 21/09/2014 04:24 au 27/09/2014 13:25 = 1 837 points ≈ 153 h**. Le « 37 h » du script/README/test vient de l'extrait horaire du 26/09 au 05/10, qui coupe ce plateau. Des séries constantes ≥ 60 points existent dans 14 missions : pas un cas isolé.
- README : 73 lignes. Les numéros de ligne de ChatGPT (112–172) sont inventés ; ses citations existent.
- Page NASA « gagnants du défi Artemis II » : existe (annonce 11/09/2026, méthodes individuelles bayésiennes à petit effectif pour la plupart).
- `tests/test_sendqueue.py` couvre « exactly once » (doublons simulés dédupliqués). Aucune clé/secret trouvé dans le dépôt.
- Premier commit du dépôt : 14/11 04:47 UTC ; `AI_USAGE.md` dit « après confirmation des organisateurs, dès 04:15 ».
- `deck_final.html` contient encore : cadre `LOGO_À_FOURNIR`, libellé visible « À CONFIRMER M1 — non codée » (diapo 4), note `TODO_M1`.

## 2. Scénarios d'échec (classés par gravité × probabilité)
| # | Scénario | Proba | Impact | Solution proposée | Décision |
|---|---|---|---|---|---|
| R1 | Un juré ouvre EDA/RR-1 : le plateau fait 6 jours, pas 37 h → crédibilité du seul résultat « donnée réelle » entamée | Élevée | Élevé | Dire « plus de six jours de valeur constante » (153 h, série brute RR-1) ; ne pas affirmer « capteur figé » (cause inconnue : capteur ou remplissage) mais « valeur constante signalée ARTIFACT par notre contrôle » ; corriger script diapo 6, README, commentaire du test | D1 |
| R2 | Départ avant l'ouverture officielle (1er commit 04:47, début équipe 09:30, permission **orale**) → contestation ou disqualification | Moyenne | **Critique** | Obtenir une trace écrite (message/mail des organisateurs, capture) et la mettre dans `docs/` ; laisser `AI_USAGE.md` factuel ; ne rien cacher | D10 |
| R3 | Démo live en panne (clic, navigateur, projecteur, polices Google bloquées hors ligne) | Moyenne | Élevé | Copie locale hors ligne (le deck est autonome, polices système, aucune ressource externe : test automatique), capture C5 en secours, état « jour 10 » préchargé, 3 répétitions avec le vrai matériel, 2e appareil | — |
| R4 | Dépassement de 5:00 coupé net (630 mots = 4:51 à 130 mots/min, + 2 clics + 2 s de silence ; zéro marge) | Élevée | Moyen-élevé | Viser 4:45 : appliquer les deux coupes déjà écrites + 1 phrase en diapo 3 ; 3 lectures chronométrées (une avec la démo) ; orateur A parle 190 s, B 110 s : à rééquilibrer ? | D6 |
| R5 | Question de fond sur le seuil : « réglé sur les mêmes scénarios que l'évaluation » (section 7.10) absent des diapos → paraît du sur-ajustement caché | Moyenne | Moyen-élevé | Ajouter en diapo 6 : « seuil réglé sur les mêmes scénarios simulés » (≤ 8 mots) ; une phrase de réponse prête | D2 |
| R6 | « Données NASA » (diapo 6) lu comme « santé d'équipage réelle de la NASA » | Moyenne | Élevé | Dire : « Équipage simulé. Seule donnée réelle : la télémétrie de cabine de l'ISS, pour le contrôle qualité » | D3 |
| R7 | Soumission ratée : format inconnu, dernier jour, un seul compte | Moyenne | Critique | Brouillon de la page de soumission prêt samedi soir (`docs/SUBMISSION.md`), soumission cible **dim. 15:00** (pas 23:59), 2 personnes connaissent la procédure, test de lien public depuis un autre compte | D7, D9 |
| R8 | Point de défaillance unique : M1 cumule M1+M5 + toute ma délégation ; si M1 est absent, personne ne peut soumettre/pousser | Moyenne | Élevé | Désigner un suppléant (accès dépôt Yves/Youssouf déjà invité), `docs/RELEASE_CHECKLIST.md` à jour, sauvegarde finale remise à 2 personnes | D9 |
| R9 | Écrasement de commits d'équipe : ma synchro par copie de fichiers remplace le contenu ; dès que d'autres poussent, je perds leurs changements | Moyenne (dès qu'ils poussent) | Moyen | Règle : `git pull --rebase` avant tout push, je ne synchronise plus par copie ; chacun pousse sur une branche, M1/moi fusionnons | D9 |
| R10 | Deck hors format : le projecteur/soumission attend PDF ou PowerPoint, le deck est un HTML | Moyenne | Moyen-élevé | PDF 16:9 exporté du deck (impression déjà prévue) + .pptx de secours généré à partir du deck ; vidéo de 30 s seulement si exigée (`SUBMISSION.md`) | D7 |
| R11 | Diapos illisibles à la projection : captures C1–C6 petites, logo manquant, mention « À CONFIRMER » visible | Élevée | Moyen | Je fais : une capture par diapo, texte réduit, logo, retrait des marqueurs internes ; test du rendu 1280×720 | D5 |
| R12 | Un texte écrit par IA est dit comme fait : le script porte « PAS ENCORE VÉRIFIÉ » ; ChatGPT et Gemini ont déjà inventé (lignes, IDs, EWMA) | Moyenne | Élevé | M1 relit le script **à voix haute** et signe chaque diapo ; toute sortie d'IA externe passe par moi avant d'entrer dans le dépôt (fait aujourd'hui : 2 erreurs de citation attrapées) | — |
| R13 | Langue : oral français, diapos anglaises, jury inconnu | Faible-moyenne | Moyen | Confirmer la langue du jury ; garder diapos EN (NASA) et oral FR si le jury est francophone | D11 |
| R14 | Fatigue : 26 h d'effort, décisions bâclées dimanche matin | Élevée | Moyen | Gel des fonctions samedi 18:00, plus de modification de code après ; 6 h de sommeil minimum ; dimanche seulement relecture, répétition, soumission | D8 |
| R15 | Jean absent/injoignable (autre hackathon, pseudo GitHub manquant) → rôle M4 non tenu | Moyenne | Moyen | Pas d'oral pour lui ; ses livrables M4-1/2 sont faits ; accès GitHub dès qu'il donne son pseudo ; ne rien lui rendre critique | D6 |
| R16 | Sauvegarde périmée ou introuvable (ZIP FINAL3 = commit ancien ; ZIP non sur Drive) | Moyenne | Moyen | GitHub = sauvegarde de référence ; ZIP final après gel, copie locale chez M1 + suppléant ; Drive : parties ≤ 3 Mo seulement si utile | D8 |
| R17 | Fuite de données privées : Drive public = dossier public trié seulement ; dépôt public = pseudo GitHub de M1 visible | Faible | Faible-moyen | Rien à faire de plus ; ne jamais élargir le partage du Drive complet sans me le demander | — |
| R18 | Sources/licences : EDA (mention présente diapo 6), PhysioNet (ODC-By, DOI) cité une seule fois dans `SOURCES.md` | Faible | Faible-moyen | Vérifier que tout jeu cité à l'oral figure dans `SOURCES.md` avec sa mention ; je le fais | — |
| R19 | Ma continuité : ma session peut se couper, perdre le lien avec ton PC (le pont est déjà tombé une fois, logo non récupéré) | Moyenne | Moyen | `CONTEXTE_IA.md` public toujours à jour ; je pousse après chaque lot ; envoie le logo en pièce jointe | — |

## 3. Anglais des diapos — tri des 26 corrections de ChatGPT
Retenues (5) : « compared with their own baseline » (diapo 1) ; « first five days » (3) ; **« limit: 10 minutes » (5, unité manquante)** ; « 0.7% » et autres pourcentages sans espace (6) ; « Not yet measured » (7).
Rejetées : « Care and synchronization » (c'est le nom du produit « Care Sync ») ; « The human makes the decision » et « Human decisions remain in human hands » (affaiblissent la devise, le script finit par « c'est l'humain qui décide ») ; « independently » (le sens voulu est « seul ») ; « Resumption » (« Resume » = bouton de l'interface) ; « each way/lasting weeks/Critical procedure initiated/how certain/Step-by-step…perform each one/ Fallback plan » (équivalents ou moins naturels : « take a measurement » est la bonne locution).
À trancher : la légende « English figure » (diapo 6) est ambiguë : la retirer ? (D4)

## 4. README — assouplissements retenus / refusés
Retenus : « never hides missing data » → « never shows missing data as normal » (c'est ce que les tests vérifient) ; « opens instantly » → « opens offline, in the demo » (non mesuré) ; « no team or personal data is ever collected » → « the demo uses only synthetic crew data » ; « implemented, tested » → « implemented; 128 automated tests (software stability, not clinical validation) ».
Refusés : « exactly once » (couvert par `test_sendqueue.py`) ; attribution Artemis II (sourcée, formule « inspiration, not endorsement » déjà dans RESULTS.md). À corriger : « 37-hour » (R1).

## 5. Questions prévisibles (pas de Q&A officiel, mais utiles en couloir) — réponses honnêtes
1. Données de vrais astronautes ? Non : équipage simulé (csync-synth-0.1, graine 42). 2. Validé en vol/clinique ? Non. 3. Pourquoi 1,5 écart-type sur 2 jours ? Compromis mesuré : 0,7 % de fausses alertes, 95,3 % de dérives lentes, 59,3 % de sauts brusques ; réglé sur les mêmes familles de scénarios, donc à confirmer sur d'autres données. 4. Pourquoi pas un modèle bayésien/EWMA ? Mesuré à fausses alertes égales : pas de gagnant net ; la règle est la plus explicable. 5. Pas de données PVT ouvertes trouvées avec sommeil et FC du même équipage. 6. Délai : « jusqu'à 20 minutes dans un sens » (NASA HRP) ; coupures de plusieurs semaines. 7. Que fait-il en cas de panne capteur ? Une donnée absente ou périmée n'est jamais présentée comme normale (porte de reprise, 10 min). 8. Risque de fausse alerte ? 0,7 % d'équipages sains simulés. 9. Pas de diagnostic ? Aucun médicament proposé, aucune interprétation du symptôme. 10. Données réelles utilisées ? Télémétrie de cabine ISS (EDA) pour le contrôle qualité seulement ; PhysioNet : volontaires au sol, statistiques seulement.

## 6. Décisions à confirmer par M1 (réponse « D1 oui/non », etc.)
- **D1** CO2 : « plus de six jours (153 h) de valeur constante » au lieu de « 37 heures », sans dire « capteur figé » (R1) — recommandé : oui.
- **D2** Ajouter « seuil réglé sur les mêmes scénarios simulés » en diapo 6 (R5) — recommandé : oui.
- **D3** Reformuler « Données NASA » en diapo 6 / script (R6) — recommandé : oui.
- **D4** Appliquer les 5 corrections d'anglais ; retirer ou garder « English figure » — recommandé : appliquer, retirer.
- **D5** Diapo 4 : garder la maquette de la carte du corps avec le libellé « Static mock-up · not in the app yet » et supprimer « À CONFIRMER M1 — non codée » ; ou retirer la maquette du pitch — recommandé : garder, libellé honnête.
- **D6** Qui est orateur A et B ? Rééquilibrer (A 190 s / B 110 s) ? Jean : pas d'oral ?
- **D7** Livrable de soumission : PDF des 7 diapos + lien dépôt (+ .pptx de secours) ; vidéo de 30 s seulement si exigée — recommandé : oui.
- **D8** Calendrier : gel des fonctions sam. 18:00 ; répétition 1 sam. 19:00 ; sommeil ; dim. 08:00 répétition chronométrée ; 09:30 gel dépôt + ZIP final ; 11:00 test matériel ; soumission dim. 15:00 au plus tard.
- **D9** Suppléant de soumission (Yves ou Youssouf ?) ; règle git : branches + `pull --rebase`, plus de synchro par copie.
- **D10** Trace écrite de l'autorisation de démarrer avant 09:00 : la retrouver/obtenir ce soir.
- **D11** Langue du jury : à confirmer.
- **D12** Appliquer les 4 assouplissements README (section 4).

## 7. Décisions prises le 14/11 à 14:16 (M1 : « mes recommandations sont acceptées ») et leur état à 15:20 UTC
| Décision | État | Où |
|---|---|---|
| D1 CO2 « plus de six jours (153 h) », sans « capteur figé » | **Appliquée** | script diapo 6 (v2), README, nouvelle figure C6 (série brute, EN/FR), test `test_raw_series_plateau_is_153h` ; temp. et humidité sont aussi plates sur la même période → origine inconnue (capteur ou remplissage) |
| D2 « seuil réglé sur les mêmes scénarios simulés » | **Appliquée** | diapo 6, script diapo 6, README |
| D3 « Données NASA » reformulé | **Appliquée** | diapo 6 (« Real data: ISS cabin telemetry, quality checks only »), script diapo 6 |
| D4 anglais (5 corrections), légende « English figure » retirée | **Appliquée** | deck v3 ; « 0.7% », « five days », « limit 10 minutes », « compared with », « Not yet measured … crew radiation dose » |
| D5 diapo 4 : maquette gardée, libellé honnête | **Appliquée** | « Static mock-up · not in the app yet » ; « À CONFIRMER M1 » retiré |
| D7 PDF + .pptx de secours | **Faits** | `pitch/deck/C-Sync_pitch_7_slides.pdf` ; `C-Sync_pitch_SECOURS_images.pptx` (images des diapos, texte non éditable) |
| D8 calendrier (gel sam. 18:00 …) | Accepté | à tenir ; je ne modifie plus le code après le gel sauf bug |
| D12 assouplissements README | **Appliquée** | README (+ pilote 3 avec chiffres et réserve, « 128 tests ») |
| D6 orateurs A/B | **En attente de M1** | noms + rééquilibrage 190 s / 110 s |
| D9 suppléant de soumission | **En attente de M1** | règle git (branches + pull --rebase) acceptée de mon côté |
| D10 trace écrite de l'autorisation de démarrer | **En attente de M1** | à retrouver/obtenir |
| D11 langue du jury | **En attente de M1** | |
Reste ouvert : logo (fichier non reçu), `scripts/check_consistency.py` plante (octet 0x95 dans un fichier lu en UTF-8, ancien problème, non lié à ces changements).
