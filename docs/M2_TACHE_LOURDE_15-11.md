# Tâche lourde M2 — après le pitch (15/11, 14:45 → 22:30) · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Pour M2, avec M1 en relecture. Branche `m2-heavy-1` (jamais `main`). Lis d'abord `AGENTS.md`, `docs/HANDOFF_TOTAL.md`, `docs/PITCH_FIGE_ET_REPONSES.md` (ce qui est fait, ce qui vient après). Modèle choisi à la main. `python -m pytest -q` (202 verts au départ) après chaque étape : aucun test ne disparaît. Un commit par étape, message `M2: ce que tu as fait`.

## Règles de fond
- Aucune affirmation sans source dans le dépôt. Un chiffre nouveau vient d'un script rejouable, jamais d'une mémoire. Un résultat défavorable est écrit tel quel.
- **Graines** : 1000–7149 = réglage, 30000–37149 = tenues à l'écart (déjà utilisées : ne plus s'en servir pour décider). Toute exploration nouvelle utilise **60000 et plus**. Le tableau du commandant utilise 61001–61006 ; les équipages « Evidence at scale » 50000+.
- Interdit : `csync/rules.py` et ses seuils (changer une valeur = décision M1 écrite dans `docs/OPEN_DECISIONS.md`), `contracts/`, `csync/ui/`, `csync/silhouette.py`, `pitch/` (réservés à la session design). Tu ajoutes des fichiers ; tu lis le reste.
- Mots interdits (`tests/test_banned_words.py`). Pas de nom ni de donnée personnelle. Données de démo = SYNTHÉTIQUES.

## Étapes (ordre conseillé ; arrêt et rapport si une étape échoue deux fois)
**H1 — Dossier de relecture pour experts (60 min, vient avant tout le reste).** `docs/REVIEW_PACKET.md` : une page par règle (dérive, urgence guidée, porte de reprise) en langage clair : ce que le code fait, chaque paramètre (valeur, d'où il vient : choix de conception ou source), ce qui est inconnu, les 5 questions précises à poser à un spécialiste de médecine spatiale. Matière brute : `csync/rules.py`, `csync/gate.py`, `csync/capsule.py`, `docs/procedures/` (ou équivalent), `pitch/silhouette/fiches.json`, `docs/OPEN_DECISIONS.md`. Chaque ligne citée est relue dans le fichier, pas de mémoire. Preuve extérieure : M4 relit et signe la ligne « relu par M4 » ; l'expert répond ensuite.

**H2 — Sensibilité des paramètres (90 min).** `research/sensitivity.py` : grille seuil d (1,0 à 2,5 par 0,25) × jours consécutifs (1, 2, 3) × longueur de référence (3, 5, 7 jours) sur les graines 60000+. Sorties : faux déclenchements, dérive 1,5 ET, saut 2 ET, avec intervalles de Wilson (`pilot3.wilson`). Figure `docs/figures/sensitivity.png` lisible sans couleur seule. Test : la case (1,5 ; 2 ; 5) redonne la règle livrée. Ne conclus pas « optimal » ; décris le compromis.

**H3 — Référence fatiguée (60 min).** Question 12 du jury : quantifier le biais. Scénario synthétique où la référence (jours 1–5) est décalée de 0,5, 1,0, 1,5 ET : part de dérives manquées vs référence propre. Fichier `research/biased_baseline.py` + `docs/BASELINE_BIAS.md` (le chiffre et sa limite). Piste testée, pas adoptée : référence avant mission.

**H4 — Essai sur données d'analogue (≥ 3 h, étape principale).** Trouver un jeu de données **ouvert** de plusieurs jours par personne avec au moins deux de : sommeil, fréquence cardiaque de repos, temps de réaction, humeur. Pistes à vérifier toi-même (aucune n'est confirmée ici) : jeux PhysioNet, NASA OSDR (études humaines), jeux d'isolement ou de simulation de mission publiés. Pour chaque jeu : licence, DOI ou URL, date de consultation, SHA-256 du fichier brut dans `data/real/raw/SHA256SUMS.txt`. Écrire un adaptateur (`csync/adapters.py`, même contrat que `eda_measurements`), faire tourner `csync.rules.evaluate` **sans la modifier**, rapporter : nombre de personnes, jours, états produits, ce qui n'est pas mesuré. Résultat dans `docs/ANALOG_TRIAL.md`, y compris « la règle ne dit rien d'utile ici ». Si aucun jeu n'est utilisable, écris-le et liste ce que tu as cherché. Ne jamais dire « validé ».

**H5 — Français de l'app (45 min).** `csync/config/strings_fr.json` : mêmes clés que `strings_en.json`, même ordre, vocabulaire de `pitch/deck/make_fr.py`. Test de parité des clés et des variables `{x}`. L'intégration dans `app.py` est faite par la session design : ne la touche pas.

**H6 — Chiffres du diaporama (30 min).** Étendre `tests/test_claims.py` : lire `pitch/deck/deck.html` et vérifier que 0/300, 93 %, 57 %, 759 525 points et 6 équipiers correspondent aux fichiers sources recalculés. Un écart = rapport, pas de modification du test.

**H7 — Rapport (20 min).** `docs/M2_RAPPORT_LOURD.md` : état des tests, écarts ouverts, ce qui n'a pas pu être fait, par étape. Commit, push de la branche, pull request.

## Jalons
14:45 début · 16:00 H1 livré à M4 · 18:00 gel des fonctionnalités (H2, H3, H5 finis) · 20:30 H4 livré ou déclaré infaisable · 22:30 rapport · 23:59 soumission (corrections de bugs seulement).

## Fin
`pytest` vert, aucun mot interdit, aucun fichier modifié hors de ceux cités, chaque chiffre rejouable. Preuve extérieure : relecture M4 (H1), graines neuves (H2, H3), SHA-256 des données (H4), tests de parité (H5, H6).
