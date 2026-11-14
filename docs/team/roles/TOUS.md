# Fiches TOUS

> Dans Cursor : choisis le modèle à la main (Claude, GPT ou Gemini). Jamais le mode automatique, jamais un modèle d'origine chinoise. Ouvre le dossier du dépôt (MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026), colle le prompt tel quel dans le chat de Cursor, puis lis ce que l'IA propose avant d'accepter.

## S0 · Installer et lancer le projet sur ton ordinateur
**Rôle :** Tous · **Quand :** Sam 09:30

**Pourquoi :** Tout le monde travaille sur la même copie du code ; si les tests passent chez toi, ton poste est prêt.

1. Installe Python 3.11 (python.org), Git (git-scm.com) et Cursor (cursor.com). Redémarre le terminal après.
2. Envoie ton nom d'utilisateur GitHub à M1 dans le groupe, pour être ajouté au dépôt. Attends sa confirmation.
3. Ouvre un terminal et tape : git clone https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026.git
4. Puis : cd MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026
5. Puis : python -m venv .venv
6. Active l'environnement. Windows : .venv\Scripts\activate — Mac/Linux : source .venv/bin/activate
7. Puis : pip install -r requirements.txt
8. Puis : python -m pytest -q  → tu dois lire « 23 passed » (ou plus). Sinon, copie le message d'erreur dans le groupe.
9. Ouvre le dossier du dépôt (MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026) dans Cursor (File > Open Folder).

**Fini quand :** « passed » sans « failed » dans le terminal.

**Prompt à coller dans Cursor :**
```text
Je débute. Dans ce dépôt C-Sync, explique-moi en 10 lignes maximum, en français simple, à quoi sert chaque dossier (contracts, csync, synthetic, data, research, tests, docs, pitch). Ne modifie aucun fichier.
```

## S1 · Envoyer ton travail (Git, sans casser celui des autres)
**Rôle :** Tous · **Quand :** À chaque tâche

**Pourquoi :** Chacun travaille sur sa branche ; seul M5 réunit les branches aux assemblages.

1. Avant de commencer une tâche : git checkout main puis git pull
2. Crée ta branche : git checkout -b m2-capsule (remplace par ton rôle et un mot sur la tâche)
3. Travaille, puis lance python -m pytest -q : tout doit passer.
4. git add -A
5. git commit -m "M2: capsule builder + tests" (ton rôle, deux-points, ce que tu as fait)
6. git push -u origin m2-capsule
7. Sur github.com, ouvre le dépôt : un bandeau jaune propose « Compare & pull request ». Clique, puis « Create pull request ».
8. Préviens M5 dans le groupe : « PR prête : m2-capsule ».

**Fini quand :** La pull request est ouverte et M5 est prévenu.

**Prompt à coller dans Cursor :**
```text
J'ai fini ma tâche. Vérifie mes changements avec git diff : y a-t-il un nom de personne, un numéro de téléphone, une clé secrète, un mot interdit (cause, diagnostic, maladie, prouve, garanti) ou un seuil clinique sans source ? Lance python -m pytest -q et dis-moi si tout passe. Ne pousse rien toi-même.
```
