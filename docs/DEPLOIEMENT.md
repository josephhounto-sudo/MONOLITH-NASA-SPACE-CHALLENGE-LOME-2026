# Parcours de mise en ligne et de livraison — samedi 14/11/2026 ~21:15 UTC
FAIT PAR L'IA — À VALIDER PAR M1. **Aucun parcours de déploiement n'existait dans le dépôt** (recherche de « deploy », « déploiement », « hébergement » : rien). Ce document le crée. Il ne déploie rien : chaque envoi, compte ou hébergement attend l'accord de M1.

## 1. Trois mises en ligne, trois risques
| Quoi | Où ça se passe | Risque | Statut |
|---|---|---|---|
| A. Soumission à la plateforme | formulaire du site officiel | clôture dimanche 23:59 ; connexion de M1 requise | brouillons prêts (`docs/SUBMISSION.md`), **rien soumis** |
| B. Démonstration en direct à midi | portable de démo, hors ligne | panne de démarrage, écran non répété | clone neuf testé à 20:55 (153 tests, app HTTP 200) ; **répétition chronométrée non faite** |
| C. Application en ligne (facultatif) | hébergement à créer | compte à créer, dépendances, contredit le récit « hors ligne » | **non prévu, non recommandé avant la soumission** |

## 2. Liens à fournir et leur état (testés sans connexion, 14/11 ~20:55 UTC)
| Champ du formulaire | Valeur proposée | Test | Remarque |
|---|---|---|---|
| Lien du projet | `https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026` | HTTP 200 sans connexion ; clone sans identifiant réussi | à rouvrir en navigation privée par un autre que M1 |
| Lien de démonstration (diapos) | `https://github.com/josephhounto-sudo/monolith-nasa-space-challenge-lome-2026/blob/main/pitch/deck/C-Sync_pitch_7_slides.pdf` | PDF de 7 pages, en anglais, 1,5 Mo | le lien « raw » se télécharge au lieu de s'afficher : prendre le lien `blob`. Les captures du PDF datent d'avant le choix de design |
| Lien de démonstration (vidéo) | aucun | **la vidéo n'existe pas** (seulement `pitch/video/SHOTLIST_30S.md`) | tâche R10 « héberger la vidéo » ouverte ; 30 s, sous-titres anglais, sans voix humaine |
| Déclaration d'IA | `docs/SUBMISSION.md` + `AI_USAGE.md` | | images et vidéos IA : filigrane visible ; code et données : mention dans le texte et les métadonnées |
Règle du formulaire (lue le 14/11) : diapos 7 au plus, titre compris ; vidéo 30 s au plus avec sous-titres anglais ; lien sans mot de passe ni inscription ; démonstration hébergée ailleurs que sur le site.

## 3. Étapes, dans l'ordre
| # | Étape | Qui | Quand | Preuve attendue |
|---|---|---|---|---|
| 1 | Choisir le profil de design (`glass` ou `quiet`) après le test des 5 secondes | M1 | ce soir | résultat du test (`docs/DESIGN_TEST_5S.md`) |
| 2 | Fusionner `m3-design` dans `main` si le profil est choisi, puis refaire les captures C1 à C5, le PDF et le pptx de secours | M1 décide, l'IA exécute (~20 min) | avant minuit | `pytest` vert ; PDF à 7 pages |
| 3 | Poser les marques Git `checkpoint-sat` puis `freeze` (**aucune n'existe**) | M5 | samedi soir / dimanche 10:30 | `git tag` |
| 4 | Répétition chronométrée sur le portable de démo, **depuis le tag** : A 190 s, B 110 s | M1, M2 | dimanche avant 11:00 | chrono, nombre de dépassements |
| 5 | Décider : vidéo de 30 s ou diapos seules | M1 | dimanche 09:00 au plus tard | décision écrite |
| 6 | Si vidéo : la produire, sous-titres anglais, l'héberger, tester le lien en navigation privée | M1 | dimanche avant 13:00 | lien ouvert par un tiers |
| 7 | Relire les brouillons de soumission (relecteur ≠ auteur) | M2 ou M4 | dimanche 12:30 | relecture notée |
| 8 | Remplir et envoyer la page de soumission | M1 (connexion personnelle) | dimanche 15:00 visé, 23:59 au plus tard | confirmation de la plateforme ; marque `submitted` |

## 4. Plan B
- Démo en direct impossible : dérouler les captures du PDF, annoncer « enregistrement de la démo » (ne pas mentir sur le direct).
- Vidéo impossible : soumettre les 7 diapos seules.
- Dépôt inaccessible le jour J : copie du dépôt en archive sur clé USB et sur le Drive.

## 5. La silhouette (maquette du corps), état au 14/11 ~21:10 UTC
- **Fait** : page autonome `pitch/silhouette/silhouette_demo.html`, 8 régions cliquables (clavier compris), 4 rubriques par région, liste de repli ; **45 contrôles passent** (relancés ce soir).
- **Non fait** : l'application ne l'utilise pas. L'étape 2 de l'urgence dit « select the body zone » mais `csync/ui/app.py` n'a aucune sélection de zone (décision E6 jamais tranchée). La diapo 4 l'annonce « Static mock-up · not in the app yet » (D5, appliquée).
- **Coût de l'intégration** : le SVG cliquable ne passe pas dans Streamlit (`st.html` retire le SVG, pas de composant bidirectionnel). Option réaliste : une liste de 8 zones à l'étape 2 (≈ 20 min, ajoute une valeur SY01 par la saisie guidée, change 2 à 3 tests). **Recommandation : ne pas le faire ce soir** (gel passé, aucun gain pour le jury à midi, risque de casser les 153 tests). Garder la maquette statique dite comme telle.
- **Reverse engineering** : `docs/pitch/REVERSE_ENGINEERING_REPORT.md` (v1, 06:00) a posé l'exigence « silhouette humaine cliquable » (A14, absente du code). Ce rapport est interne et cite des mots interdits.

## 6. Non vérifié
Le lien ouvert depuis un téléphone ou un autre réseau ; la page de soumission elle-même (connexion de M1) ; l'horaire exact du pitch sur le programme local ; la vidéo ; le portable de démo.
