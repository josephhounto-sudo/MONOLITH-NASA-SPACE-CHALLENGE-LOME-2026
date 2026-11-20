# AGENTS.md — lire en premier (Cursor et toute IA du dépôt)

> **Reprise de session (20/11/2026) : lire d'abord `docs/PLAN_V3.md` (§16 = dernier état et rétrospective). `main` porte la V3 ; l'app hébergée lit `m3-design`, synchronisée automatiquement par `.github/workflows/sync-hosted-app.yml` à chaque push sur `main` (pas sur `v3` : avancer `main` en avance rapide après des tests verts). Les documents de processus anciens sont dans `docs/archive/`.**
Projet : C-Sync, NASA Space Apps 2026 Lomé, équipe MONOLITH. Réponds en français. Texte produit/affiché : anglais (jury), sauf docs d'équipe.

**Historique** : `docs/HANDOFF_TOTAL.md` et `docs/CONTEXTE_IA.md` décrivent l'état au 15/11 (version soumise de0b5be).

## Règles non négociables
1. Une branche par tâche. `git pull --rebase` avant tout push. Depuis le 19/11/2026 (décision de Joseph), une branche aux tests verts peut être avancée sur `main` en avance rapide.
2. `python -m pytest -q` doit passer avant tout commit (392 tests au 20/11, 13:40).
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
- Clignement des yeux : premier prototype sur la caméra du visiteur (Technologies, Mesurer), toujours dit « en développement » sur la console, avec la raison (non validé).
- Données NASA en direct : contexte seulement, jamais une décision ; âge de la mesure toujours affiché.
