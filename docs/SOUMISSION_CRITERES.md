# Critères T1–T8 et résultats — dimanche 15/11/2026 ~05:50 (Lomé)
FAIT PAR L'IA — À VALIDER PAR M1. Rien n'a été soumis ni déployé.

| # | Critère | Résultat | Preuve |
|---|---|---|---|
| T1 | Clone neuf de `main` : tests, cohérence, app | **OK** | `main` 8c165b5 : 153 tests, `check_consistency` 0 erreur, app HTTP 200 (port 8610) |
| T2 | Dépôt et PDF accessibles sans connexion | **OK** | `curl` anonyme : HTTP 200 sur le dépôt, la page du PDF et le PDF brut |
| T3 | Chaque champ du formulaire a un texte final en anglais | **Partiel** | 8 champs officiels lus sur le guide (nom, résumé, lien démo, lien projet, description, usage SI, données NASA, références) ; brouillons présents pour tous ; mots : résumé 104, détails 292, SI+NASA 131 ; aucun mot interdit ; **aucune limite de mots indiquée par le guide** ; trois points bloquants ci-dessous |
| T4 | Déclaration d'IA conforme aux règles officielles | **Non** | contradictions V1–V3 ci-dessous |
| T5 | Point de retour avant toute fusion de design | **OK (variante)** | le push d'un tag est refusé (HTTP 403) depuis cet environnement ; branche `checkpoint-before-design` = 8c165b5 sur GitHub ; tag local seulement |
| T6 | Accès page par page | voir tableau | |
| T7 | Liste de validation en 10 lignes oui/non | voir fin | |
| T8 | Rien soumis, rien déployé sans accord | **OK** | |

## Accès (T6)
| Page | Accès | Reste à faire par M1 |
|---|---|---|
| Guide de soumission (spaceappschallenge.org) | lu en entier dans ton Chrome | rien |
| Page projet de l'équipe (formulaire) | non ouverte : connexion personnelle, deux cases à cocher (conditions, travail original), bouton « Submit for Judging » | tout (connexion, cases, bouton) |
| Dépôt et PDF GitHub | ouverts sans connexion | rien |
| Streamlit Community Cloud | connecté (« My apps » vide) ; avertissement orange sur « Workspaces » non ouvert | accord pour « Deploy » |
| NTRS 20220013418 | lu | rien |

## Trois écarts trouvés entre nos documents et les règles officielles
**V1. Le logo de l'équipe est une image générée par IA, sans filigrane visible.** Le PNG intégré à `deck_final.html` contient des métadonnées de provenance : outil « gpt-image » d'OpenAI, type « trainedAlgorithmicMedia », daté du 22/10/2026 (avant l'événement). Règle officielle : les images générées par une IA doivent porter un filigrane visible. Le pied de page « AI use declared » n'en est pas un.
**V2. `AI_USAGE.md` affirme le contraire** : « no AI-generated image is used without a visible watermark » et « nothing generated before the event was reused as-is ». Les deux phrases sont fausses pour le logo tel qu'il est.
**V3. `AI_USAGE.md` : « Every change is reviewed by a team member before merge (checklist V10) »** : V10 est NON VÉRIFIÉ, et plusieurs commits (dont les miens) ont été poussés sans relecture par un membre. À reformuler selon l'état réel.

## Deux manques dans les 7 diapos (le guide : « ensure that the content of your slides address… »)
- **Noms des membres de l'équipe : absents** (« Team MONOLITH » seulement).
- **Titre du défi choisi : absent** (« NASA Space Apps Challenge 2026 · Lomé » seulement). Le titre utilisé par le README : « Create Health Monitoring Software for Astronauts on Space Missions ».
- Contrainte : 7 diapos au plus, anglais, aucune image de personne de moins de 18 ans.

## Autres points
- Diapo 2 : la ligne « Sources » cite deux pages nasa.gov que je n'ai pas ouvertes ; la source que j'ai lue est NTRS 20220013418.
- Règle SI du guide : l'IA « ne doit pas servir à trouver l'idée ». `AI_USAGE.md` déclare « research notes, idea review » (ChatGPT, Gemini). M1 doit confirmer l'origine de l'idée avant d'écrire la déclaration.
- Le guide demande de **tester le lien en navigation privée** : à faire par une autre personne que M1.
