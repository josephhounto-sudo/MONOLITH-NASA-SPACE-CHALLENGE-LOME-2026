# Rapport graphique — design-v3, dimanche 15/11/2026 ~08:25 (Lomé = UTC)
FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ PAR DES PERSONNES. Branche `design-v3` = `design-v2` (validée par M1 à 07:20) + `nasa-data` (panneau Habitat) + ce passage. Point de retour : `checkpoint-before-design`.

## 1. Ce que les 4 nouvelles références apportent (et ce que je n'en prends pas)
| Référence | Ce qu'elle fait | Ce que l'interface en tire — **une information, pas un décor** |
|---|---|---|
| Logo planète + trajectoire, blanc sur noir | forme en négatif, une trajectoire qui traverse | le logo C-Sync (§3) : une orbite qui traverse le croissant en défonce |
| Affiche « 21 Grams » | sphère sombre, lignes fines, petits blocs de dates encadrés, chiffres fins | les **métadonnées de coin** : mission, jour, liaison sol, délai (bandeau de mission) |
| Affiche « LUNAR » | ellipses orbitales fines ponctuées de points, panache chaud, textes minuscules aux coins | la **trajectoire de mission** : 10 jours = 10 nœuds sur un arc, chacun a la forme de l'état le plus haut du jour, l'urgence et le refus sont marqués |
| Plaques translucides empilées sur crème | des couches qui montrent le temps | l'**historique** dans chaque carte : une petite forme par jour (la dérive devient visible : ◇ puis ▲) |
Non repris : le fond noir (M1 a validé le clair à 07:20), le panneau rouge de l'affiche, les textures. Les références de M1 sont des images de tiers : non versionnées.

## 2. Ce qui a changé dans l'interface (et pourquoi)
1. **Panneau Habitat (données NASA réelles)** intégré depuis `nasa-data`, dans une section en verre marquée « NASA DATA ». Défaut corrigé : sur fond clair, le graphique traçait le CO2 en cyan `#00E0F5` (**1,6:1 sur blanc**) et la ligne de l'exigence en `#9AABB1` (**2,4:1**), sous le seuil de 3:1 des éléments graphiques. Couleurs propres au profil : série `#1F2A3D` (14,4:1), exigence `#0B6E85` (5,9:1), ARTIFACT `#56636A` (6,2:1, couleur « inconnu »).
2. **Bandeau de mission** : métadonnées de coin (Mars transit · jour 09/10 ; liaison sol coupée 13:00–19:00 le jour 9 ; délai 20 min, valeur de démonstration du contrat) et **trajectoire**. Les jours à venir sont des points vides : **l'écran ne montre jamais l'avenir** (défaut trouvé sur la première version : le jour 7 affichait l'urgence du jour 9 ; test ajouté).
3. **Historique par carte** (10 cases) : la dérive Body/Attention se lit sans ouvrir « Signals ».
4. **Passe « 1 % »** : rayons emboîtés (extérieur 30 → intérieur 18 = extérieur − marge) ; une seule échelle de texte ; chiffres tabulaires ; les petites métadonnées en capitales espacées à un seul endroit (le bandeau) ; texte « Delay 20 min (demo) » raccourci pour tenir sur une ligne.

## 3. Logo C-Sync (proposition, non intégré)
- **Idée** : un « C » en croissant (l'équipage, la pierre du design) et un petit corps logé dans sa bouche (le sol), sur **la même orbite** : deux corps synchronisés. L'orbite passe **derrière** le croissant sur sa moitié arrière et **devant** sur sa moitié avant, en défonce. La première version la faisait passer devant aux deux croisements, ce qui est impossible ; corrigé.
- **Fichiers** (`brand/`) : `csync_mark_ink.svg`, `csync_mark_cream.svg`, `csync_mark_gradient.svg`, `csync_mark_small_ink.svg` (sans orbite : elle disparaît sous 32 px), `csync_lockup_light.png`, `csync_lockup_dark.png`, `csync_lockup_gradient.png`, `csync_mark_sizes.png` (16 à 128 px), générateur `make_mark.py` (géométrie pure, grille 100×100).
- **Motion façon Gemini** : `csync_motion.html` (CSS, 3,2 s, se joue une fois ; `prefers-reduced-motion` montre l'image finale), `csync_motion.mp4` (H.264, 4 s, 30 i/s) et `csync_motion.gif` (320 px). Le dégradé tourne dans le croissant (bleu canard → pierre → corail → orange, les couleurs des références), l'orbite se trace, le point fait un tour et se loge dans le C avec une légère pulsation (le « sync »).
- **Risques honnêtes** : (1) « planète + anneau » est un motif très courant dans l'imagerie spatiale ; ce qui le distingue ici est le croissant en C avec le point dans sa bouche, c'est mince ; (2) c'est une image produite par une IA : règles de l'événement (déclaration, filigrane) à trancher par M1, ligne ajoutée à `AI_USAGE.md` ; (3) le logo de l'équipe (MONOLITH) n'a pas été modifié, rien n'est intégré dans l'app ni les diapos sans accord écrit de M1.

## 4. Mesures (outils, pas jugement)
| Mesure | Résultat |
|---|---|
| `python -m pytest -q` | **168 verts** (162 de `nasa-data` + 5 de `design-v2` + 1 « jamais l'avenir ») |
| axe-core 4, jours 3, 7, 9 (étape 3), 10 (refus), mouvement normal et réduit | **0 violation** ; 21 à 36 nœuds « contraste incomplet » par jour (verre, dégradés) |
| Contraste sur pixels rendus (5e centile du fond) | 0 échec réel ; min 5,10:1 au jour 9. Un « échec » à 1,83:1 aux jours 3/7/10 est un **faux positif** vérifié : la légende « Data origin » est dans l'expandeur fermé ; ouvert, elle est sur blanc (≈ 7:1) |
| Logo à 16, 24, 32, 64, 128 px | l'orbite se perd sous 32 px → variante `small` |
Ce que ces mesures ne disent pas : si c'est beau, si un jury le trouve « NASA ». Réponse : test des 5 secondes (`DESIGN_TEST_5S.md` v2, images mises à jour) et photo du projecteur.

## 5. Ce qui reste (et qui le fait)
1. M1 : valider `design-v3` ; dire si le logo C-Sync remplace quelque chose (barre du haut, diapo 1) ou reste une proposition.
2. 3 à 5 personnes : test des 5 secondes (`docs/design_ab/blind_5s_v2/`).
3. IA de la session principale, après fusion : captures du deck C1–C5 (avec le panneau Habitat visible), PDF, pptx.
4. Arrêt : si rien n'est validé à 09:45, présenter `signal` tel quel.
