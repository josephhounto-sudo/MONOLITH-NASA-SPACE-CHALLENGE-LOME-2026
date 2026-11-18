Branche `cursor-v2` depuis `v2`. Quatre commits, dans l'ordre. Le plafond maestro de 3 tâches est dépassé : le brief en nomme 4. `contracts/` et `AGENTS.md` intacts. Heures, valeurs et graines de l'histoire intactes.
Fait 1. Vulture ≥ 80 ne signalait que `direction` (passé par `trends_panel`, jamais lu) et `dashed` (jamais passé à `_orbit`). Les deux sont retirés. `csync.memory`, `glyphs` et `sendqueue` sont gardés.
Fait 2. `python scripts/compare_strings.py` ne sort aucune ligne. Français corrigé : « porte », « utile », « charge », « une fausse », le passé de la personne, la mesure qui ne disait pas qu'elle était ancienne. Anglais non modifié.
Fait 3. `scripts/measure_contrast.py` ouvre la page avec Playwright à 1400, 1000 et 390 px. Aucune couleur changée.
Fait 4. Verdict court (« Day 7: Body Watch, Attention Degraded. »), une ligne par indicateur signalé, règle dans le repliable. La phrase longue du jour est repliée avec la règle.
Thème sombre : branche `cursor-v2-dark`, fichier `scripts/propose_dark_theme.py` seulement. `csync/ui/style.py` n'y est pas modifié. Non branché, car le gel des fonctions (AGENTS.md) n'autorise plus que des bugs.
Vérifié. `python -m pytest -q` : 288 passed sur `cursor-v2` avant ce rapport ; 290 passed sur `cursor-v2-dark`.
Vérifié. Pixels du jour 7, avant le découpage : corps au-dessus de 4,5 (bannière 13,26 à 1400). Légendes mesurées à 14,0 px, donc seuil 4,5 et non 7 : décision humaine 4,40 et ligne de version 4,11 à 1400, sous le seuil. Mots d'état sous 4,5 à 1400 : Attention 3,64, Mission 3,87, Habitat 3,87. Body Watch 5,43 et Morale 4,61 passent.
Vérifié. Après le découpage, Playwright à 1400 et 390 : aucun bloc visible de plus de 3 lignes (verdict 2 puis 3 lignes, lignes d'indicateur de 1 à 3).
Vérifié. Aplats proposés, `contrast_ratio` sur fond #14181F : corps 15,77, légende 11,38, normal 9,96, surveillance 8,14, dégradé 7,77, inconnu 9,80. Tous au-dessus du seuil écrit. Ce n'est pas une capture.
Non vérifié. Attention à 390 px vaut 1,59 dans le script, et 3,64 à 1400 : le recadrage de la carte empilée n'est pas stable, le 1,59 n'est pas une couleur.
Non vérifié. Le contraste des nouvelles lignes d'indicateur n'a pas été remesuré après le découpage. Le thème sombre n'a pas été rendu.
Non vérifié. Aucun lecteur extérieur n'a fait le test des 60 secondes. Playwright n'est pas dans `requirements.txt`.
Peut casser. Une unité très longue peut dépasser 110 caractères. Le repliable montre encore la phrase longue du jour. Le sampler mélange glyphe et contour : un ratio proche de 4,5 peut être un peu bas.
Annuler. Rien n'est poussé. `git checkout v2` revient au commit `5723423`. `git branch -D cursor-v2 cursor-v2-dark` retire les deux branches locales.
