# AGENTS.md — lire en premier (Cursor et toute IA du dépôt)

> **Reprise de session : lire d'abord `docs/HANDOFF_TOTAL.md` (état au 15/11/2026 06:15, remplace `docs/CURSOR_HANDOFF.md`).**
Projet : C-Sync, NASA Space Apps 2026 Lomé, équipe MONOLITH. Réponds en français. Texte produit/affiché : anglais (jury), sauf docs d'équipe.

**Lis d'abord** : `docs/CURSOR_HANDOFF.md` (état, tâches, décisions), puis `docs/CONTEXTE_IA.md` (contexte complet à jour).

## Règles non négociables
1. Une branche par tâche (`m2-capsule`, `m3-nominal`…). Jamais de push direct sur `main`. `git pull --rebase` avant tout push.
2. `python -m pytest -q` doit passer (128 tests au 14/11 14:40) avant tout commit.
3. Message de commit : `M2: ce que tu as fait`.
4. Jamais de nom, téléphone, clé, donnée personnelle. Mots interdits dans README/chaînes/procédures : cause, diagnos*, prove/proves, guarantee, disease.
5. Contrats (`contracts/`) : changement seulement avec l'accord de M1.
6. Aucune affirmation chiffrée sans source dans le dépôt. Données de démo = SYNTHÉTIQUES ; ne jamais dire « validé sur de vrais équipages ».
7. Ne pas inventer de référence, de chiffre NASA, ni de ligne de README. Écrire « NON VÉRIFIÉ » si pas de source.
8. Gel des fonctionnalités : samedi 18:00. Ensuite : bugs uniquement.
9. Choisir le modèle à la main (Claude, GPT ou Gemini), jamais le mode automatique.
