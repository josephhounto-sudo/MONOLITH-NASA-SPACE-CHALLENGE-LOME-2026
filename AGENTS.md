# AGENTS.md — lire en premier (Cursor et toute IA du dépôt)

> **Reprise de session : lire d'abord `docs/HANDOFF_TOTAL.md` (état au 15/11/2026 06:15, remplace `docs/CURSOR_HANDOFF.md`).**
Projet : C-Sync, NASA Space Apps 2026 Lomé, équipe MONOLITH. Réponds en français. Texte produit/affiché : anglais (jury), sauf docs d'équipe.

**Lis d'abord** : `docs/CURSOR_HANDOFF.md` (état, tâches, décisions), puis `docs/CONTEXTE_IA.md` (contexte complet à jour).

## Règles non négociables
1. Une branche par tâche. `git pull --rebase` avant tout push. Depuis le 19/11/2026 (décision de Joseph), une branche aux tests verts peut être avancée sur `main` en avance rapide.
2. `python -m pytest -q` doit passer avant tout commit (342 tests au 20/11).
3. Message de commit : `M<n>: ce que tu as fait`, puis une ligne qui dit pourquoi.
4. Jamais de nom, téléphone, clé, donnée personnelle. Mots interdits dans README/chaînes/procédures : cause, diagnos*, prove/proves, guarantee, disease.
5. Contrats (`contracts/`) : changement seulement avec l'accord de M1.
6. Aucune affirmation chiffrée sans source dans le dépôt. Données de démo = SYNTHÉTIQUES ; ne jamais dire « validé sur de vrais équipages ».
7. Ne pas inventer de référence, de chiffre NASA, ni de ligne de README. Écrire « NON VÉRIFIÉ » si pas de source.
8. Gel des fonctionnalités levé par Joseph le 19/11/2026. Plan en cours : `docs/PLAN_V3.md`.
9. Choisir le modèle à la main (Claude, GPT ou Gemini), jamais le mode automatique.

## Décisions de Joseph du 20/11/2026 (V3)
- Design : reprendre la référence « Bookings Per Day » (couleurs, verre fumé, textures, pilules, courbe lumineuse). Jetons mesurés : `docs/PLAN_V3.md` §2. Tout texte de moins de 24 px reste à 4,5:1 mesuré sur pixels.
- L'orange de la référence est utilisé (capter l'attention). Les états restent toujours écrits en mot et icône.
- La dérive n'est pas la base du produit. L'accueil est une console en direct ; la dérive est un moteur parmi d'autres, montré surtout en mode démo.
- Aucune photo de personne identifiable.
- Clignement des yeux (PERCLOS) : affiché « en développement », avec une note courte qui dit pourquoi.
- Données NASA en direct : contexte seulement, jamais une décision ; âge de la mesure toujours affiché.
