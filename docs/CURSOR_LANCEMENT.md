# Lancement de Cursor — répartition du travail (18/11/2026)

Branches: Claude travaille sur `v2`. Cursor travaille sur `cursor-v2` (créée depuis `v2`), jamais sur `v2` directement. Fusion par Joseph après lecture des tests.
Fichiers à lui seul (évite les conflits):
| Qui | Possède |
|---|---|
| Cursor | `scripts/`, `tests/` des scripts qu'il crée, `csync/config/strings_fr.json` (parité), la fonction `nominal()` de `csync/ui/app.py` (mur de texte), suppressions de code mort validées |
| Claude | histoire (`docs/STORY.md`, ordre des beats), `csync/ui/style.py` (thème), écrans de référence croisée |
| Partagé | `csync/config/strings_en.json`: ajouter des clés en fin de bloc, tirer `v2` avant chaque commit |
Relecteurs externes (Claude les pilote dans le navigateur): ChatGPT et Gemini lisent chaque écran à froid après chaque fusion.

## Prompt à coller dans l'agent Cursor
```
Tu travailles sur le dépôt C-Sync (Streamlit/Python), branche `cursor-v2` créée depuis `v2`. Lis d'abord `AGENTS.md`, `docs/CURSOR_TACHES.md` et les règles de `.cursor/rules/` (maestro, design-master, story-writer, code-master-writer): elles s'appliquent à tout ce que tu fais.

But en une phrase: un inconnu comprend à quoi sert C-Sync et qui décide, en 60 secondes, sur un écran lisible et sans erreur visible.

Fais les tâches 1 à 4 de `docs/CURSOR_TACHES.md`, dans cet ordre, une par commit. Pour chaque tâche: (1) écris d'abord le critère d'acceptation et 5 façons dont elle peut échouer, avec un test avant le code; (2) montre-moi la liste avant toute suppression; (3) lance `python -m pytest -q` et colle la fin de la sortie; (4) termine par VERIFIED (comment) ou UNVERIFIED pour chaque affirmation.

Ensuite, section longue: construis `scripts/measure_contrast.py` puis, avec ses résultats, propose un thème sombre dans une branche à part (`cursor-v2-dark`) sans toucher `csync/ui/style.py` de `v2`. Ne change jamais l'histoire gelée (heures, valeurs, graines), ni `contracts/`, ni `AGENTS.md`. N'ajoute aucune affirmation médicale. Si une règle t'empêche de faire quelque chose, dis laquelle: ne la contourne pas.

À la fin, écris `docs/RAPPORT_CURSOR.md` en 15 lignes: fait, vérifié, non vérifié, ce qui peut casser, comment annuler.
```
