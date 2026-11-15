# Dossier de soumission finale — C-Sync, équipe MONOLITH · 15/11/2026
FAIT PAR L'IA — À VALIDER PAR M1. Rien n'a été soumis. Règles : `docs/PROGRAMME_OFFICIEL.md` (clôture dimanche 23:59, seule la dernière soumission est jugée) et le guide officiel lu le 14/11.

## Contenu du dossier
| Pièce | Fichier | Exigence officielle | État |
|---|---|---|---|
| 8 champs du formulaire, textes finaux en anglais | `submission/FORM_FIELDS_EN.md` | nom, résumé, lien démo, lien projet, détails, usage de l'IA, données NASA, références | prêt, chiffres alignés sur le jeu tenu à l'écart (0/300, 92,7 %, 57,3 %) et 205 tests |
| Démo : 7 diapos en anglais (ou vidéo ≤ 30 s) | `submission/C-Sync_pitch_7_slides.pdf` (copie de `pitch/deck/`) | 7 diapos au plus, titre compris, anglais, lien ouvert sans compte | prêt, 7 diapos, test du deck vert |
| Secours PowerPoint | `submission/C-Sync_pitch_SECOURS_images.pptx` | — | images seulement |
| Dépôt public | https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026 | public, sans mot de passe | public, `main` à jour |
| Déclaration d'IA | `AI_USAGE.md` | nommer outils et usage ; images IA avec filigrane visible | mise à jour 15/11 ; ligne visible sur la diapo 1 |
| Sources | `SOURCES.md`, `README.md` | références, données NASA citées | à jour |
| Données NASA | diapo 6 + champ 7 | requises pour les prix mondiaux | OSDR EDA, contexte habitat seulement |
| Équipe | diapo 1 : 4 noms | tous inscrits sur la page équipe | à vérifier par M1 sur la plateforme |

## Ce que seul M1 peut faire (connexion personnelle)
1. Ouvrir la page projet de l'équipe sur spaceappschallenge.org, coller les 8 champs depuis `FORM_FIELDS_EN.md`.
2. Cocher les deux cases (conditions ; travail original produit pendant l'événement) : à lire avant de cocher, voir les points ci-dessous.
3. Cliquer « Submit for Judging », noter l'heure et garder la confirmation.
4. Faire tester le lien démo en navigation privée par quelqu'un d'autre (guide officiel).

## Points à décider ou vérifier avant de cliquer
- **Logo d'équipe généré par IA, créé le 22/10 (avant l'événement)** : déclaré dans `AI_USAGE.md` et nommé sur la diapo 1, mais la case « travail produit pendant l'événement » ne dit pas la même chose pour un élément antérieur. Option sûre : le dire tel quel (déjà fait) ; option plus sûre : retirer le logo de la diapo 1 si un organisateur le demande.
- **Début du travail** : autorisation orale « commencer samedi soir » sans trace écrite ; la FAQ dit aucun travail avant samedi 09:00 (`docs/PROGRAMME_OFFICIEL.md`). À confirmer auprès des organisateurs, par écrit si possible.
- **Origine de l'idée** : l'IA ne doit pas servir à trouver l'idée ; `AI_USAGE.md` dit que l'idée vient de l'équipe. M1 confirme que c'est exact.
- **Relecture** : le champ IA dit « relecture partielle ». Ne pas écrire « tout est relu » tant que V10 (relu par quelqu'un d'autre que l'auteur) n'est pas fait.
- **Application en ligne** : l'app Streamlit de test n'est pas le lien de soumission ; ne pas la mettre dans le formulaire. Les promesses du champ 5 portent sur le dépôt.
- **Aucune limite de mots** n'est indiquée par le guide ; les champs font 103 mots (résumé) et 352 mots (détails).
- **Images de personnes de moins de 18 ans** : aucune dans le deck ni le dépôt.

## Contrôles faits le 15/11 (reproductibles)
`python -m pytest -q` : 205 passés · `python scripts/check_consistency.py` : 0 erreur · deck : `NODE_PATH=/tmp/node_modules node pitch/tests/test_deck.js pitch/deck/deck_final.html /tmp/d.txt` : tous passent · axe : 0 violation sur les 8 onglets de l'app · liens démo et dépôt : HTTP 200 sans connexion (vérifier de nouveau après le dernier push).

## Après le clic
Marquer `submitted` avec l'heure dans `docs/MAJ_LOG.md`. Plusieurs soumissions sont possibles jusqu'à 23:59 : si on corrige quelque chose, soumettre de nouveau, seule la dernière compte.
