# Passation totale — dimanche 15/11/2026 ~06:15 (Lomé = UTC)
FAIT PAR L'IA — À LIRE EN PREMIER par toute IA ou personne qui reprend le travail. Remplace `docs/CURSOR_HANDOFF.md` (état du 14/11 14:40, périmé). Rien n'est soumis. Rien n'est déployé en production.

## 0. Contexte en 6 lignes
- Projet **C-Sync (Care Sync)**, équipe MONOLITH, NASA Space Apps 2026 Lomé. Défi : « Create Health Monitoring Software for Astronauts on Space Missions ». Assistant hors ligne pour un équipage loin du sol ; la décision reste humaine.
- Équipe : **M1/M5** (chef, soumet), **M2** (capsule, livraison attendue, rien de visible), **M3** (design/écrans, rien de commité), **M4** (procédures et recette, validation humaine à faire).
- Calendrier : pitch **dimanche 12:00** (5 min, sans questions) ; soumission visée **15:00**, limite **23:59** ; gel des fonctions passé (sam. 18:00) : corrections seulement.
- Préférences de M1 : **vérité directe même si elle déplaît**, précis sans divaguer, réponses en français, texte affiché et pitch en anglais. Il demande souvent « une version plus profonde, pas plus grosse » : (1) ce qu'un pro ferait en plus, (2) la matière la plus brute, (3) méthodes et outils, (4) preuve extérieure ; puis réécrire sa demande et l'exécuter.
- M1 est limité en usage sur cette session : la suite (design) se fait ailleurs, avec un autre Claude.
- **Ne jamais soumettre, déployer en production, créer un compte ou accepter des conditions à sa place.**

## 1. État technique vérifié (commandes en §9)
| Quoi | Valeur |
|---|---|
| `main` | tests : **153 verts** ; `scripts/check_consistency.py` : 0 erreur ; clone neuf : app HTTP 200 |
| Branches utiles | `main`, `m3-design` (design, **non fusionnée**), `checkpoint-before-design` (= point de retour sur `main` 8c165b5), `cursor-heavy-1` (déjà fusionnée) |
| Tags | aucun sur GitHub (le push d'un tag est refusé : HTTP 403 depuis l'environnement IA) ; M1 peut en pousser depuis sa machine |
| Dépôt public | https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026 (HTTP 200 sans connexion) |
| PDF des 7 diapos | `pitch/deck/C-Sync_pitch_7_slides.pdf` (+ pptx de secours en images) ; lien : voir `docs/DEPLOIEMENT.md` |
| App de test en ligne | https://monolith-nasa-space-challenge-lome-kwtv79qy52ihwgezt8byuy.streamlit.app/ (Streamlit Community Cloud, branche `m3-design`, Python 3.13, secret `CSYNC_STYLE="signal"`). **Test seulement**, pas le lien de soumission. Se met à jour à chaque push de `m3-design`. Non testée en accès anonyme (domaine bloqué pour l'IA) |
| Artefact de suivi « Parcours » | https://claude.ai/artifact/1xzdf1Dt413knUJMc6gY5F (collections `tasks`, `annonces`, etc. ; une écriture exige `if_version`) |
| Artefact d'aperçu design | https://claude.ai/artifact/UKY4gYxA1k2cCP1Gv5tqFy (captures glass / hybrid / calm / signal) |
| Registres | `docs/A_TRANCHER.md` (décisions), `docs/SOUMISSION_CRITERES.md` (critères T1–T8), `docs/MAJ_LOG.md` (journal), `docs/PREMORTEM_14-11.md` §7 (D1–D12) |

## 2. Décisions écrites par M1 (ses mots font foi, pas les miens)
- 14/11 14:16 : « mes recommandations sont acceptées » → D1–D12 (voir PREMORTEM §7) ; orateurs : A = M1, B = M2, M4 pas d'oral ; jury bilingue, oral en anglais.
- 14/11 21:30 : style « glass un peu de quiet » (ensuite il a **rejeté** les rendus calm/hybrid/signal comme « débutants »), fusion de `m3-design` « oui comme tu l'as dit » (après choix du design), suppléant de soumission = Yves, EWMA : « oui avec Gemini puis on perfectionne » (**non appliqué** par moi : règle v3 mesurée, gel passé ; à tester à part dans `research/` si voulu).
- 15/11 05:35 : logo IA **gardé sans filigrane** (décision de M1 ; risque expliqué) ; `AI_USAGE.md` corrigé pour le décrire ; idée du projet = équipe (IA = recherche, relecture, construction) ; **relecture totale à faire après le design** ; pas de noms sur la diapo 1 « vu le temps serré » ; branche `checkpoint-before-design` acceptée comme point de retour.
- 15/11 05:52 : noms des membres : « oui si le guide le demande » → le guide dit « ensure that the content of your slides address… names of team members » ; **il me faut les noms exacts à publier** (non fournis, jamais inventés) ; ils iraient sur la diapo 1 et donc dans le PDF **présenté et soumis** (c'est le même fichier). NTRS sur la diapo 2 : « oui tant que les jurés le comprennent » → **appliqué** (§3).

## 3. Fait cette nuit (preuves dans le dépôt)
- Diapo 2 et scripts EN/FR alignés sur la fiche NASA NTRS 20220013418 (lue dans le navigateur) : délai 0–22 min, coupures « de plusieurs jours à plusieurs mois » ; ligne « Source » = article ASCEND 2022 + lien NTRS. PDF et pptx régénérés. `SOURCES.md` à jour.
- Diapo 1 : titre du défi ajouté en pied de page (petit ; à placer mieux dans le nouveau design).
- `AI_USAGE.md` : logo = image générée par IA (métadonnées OpenAI « gpt-image », 22/10/2026, avant l'événement), utilisé tel quel sans filigrane ; idée = équipe.
- Contrôles de la page de soumission : `docs/SOUMISSION_CRITERES.md`.
- Profils de design sur `m3-design` (voir §5).

## 4. Reste à faire, par qui
| # | Tâche | Qui | Note |
|---|---|---|---|
| 1 | Design complet (refonte) | M1 + autre Claude | §5 |
| 2 | Fusionner `m3-design` dans `main`, refaire captures C1–C5, PDF, pptx (~20 min) | IA après choix de M1 | `python pitch/deck/embed_captures.py`, `export_pdf_pptx.py` ; tests verts ; point de retour `checkpoint-before-design` |
| 3 | Noms des membres sur la diapo 1 | M1 donne les noms | sinon non fait |
| 4 | Relecture totale (AI_USAGE, SUBMISSION, diapos, README) | quelqu'un d'autre que l'auteur | phrase « relu avant fusion » dans `AI_USAGE.md` inexacte jusque-là ; V10 non vérifié |
| 5 | Validation humaine des procédures et de la recette | M4 | message WhatsApp envoyé par M1 : 4 tâches (clone neuf, procédures, test 5 s, relecture) ; réponse attendue avant 08:30 |
| 6 | Test des 5 secondes (3 à 5 personnes) | M4 / M1 | `docs/DESIGN_TEST_5S.md`, `docs/design_ab/blind_5s/` ; l'IA ne juge jamais l'effet visuel |
| 7 | Répétition chronométrée (A 190 s, B 110 s) | M1, M2 | avant 11:00 |
| 8 | Livraison de M2 et de M3 | M2, M3 | rien de visible sur GitHub à 05:40 ; M3 : dossier local = clone de `main` + un `app.py` modifié non commité qui rend **3 tests rouges** (non intégré) ; M2 : introuvable (un ZIP de ~490 Mo existe dans Téléchargements de M1, trop gros à lire ; demander un ZIP sans `.venv` ou un `git push`) |
| 9 | Silhouette humaine | décision M1 | §6 |
| 10 | Page de soumission : connexion, 2 cases, « Submit for Judging » | M1 seul | 8 champs : nom, résumé, lien démo, lien projet, description, usage SI, données NASA, références ; textes prêts dans `docs/SUBMISSION.md` ; aucune limite de mots indiquée par le guide |
| 11 | Test du lien en navigation privée par un tiers | quelqu'un d'autre que M1 | le guide l'exige |

## 5. Design — état et leçons
- **Profils CSS** dans `csync/ui/style.py`, choisis par `CSYNC_STYLE` : `glass` (défaut de `main`, fond animé, verre), `quiet`, `hybrid` (défaut de `m3-design`), `calm`, `signal`. Même balisage ; seul `app.py` a reçu `data-state` sur les cartes et `.cs-action` autour de l'action proposée.
- **M1 n'est satisfait d'aucun** : mes passes ont surtout *retiré* des choses (le skill unslop retire ; il contredit le brief de départ « futuriste, verre léger façon Apple, formes »). Son brief écrit prime sur le skill. Deux idées Pinterest n'avaient jamais été appliquées avant « signal » : une forme distincte par état (losange / triangle / cercle / carré pointillé) et le mot d'état en grand sur grille. Références de M1 : images dans `Téléchargements` de son ordinateur (planche « Beyond the Grid… 120 shapes », « Search Minimal and Graphics… Designspiration », « Search Projects… logos », « Iphone ios 7 », trois « téléchargement*.jpg »). Sources lues : `emil-design-eng` (courbe `cubic-bezier(.23,1,.32,1)`, propriétés nommées, :active scale .97), CSS du portfolio de M1 (jetons 4 px, durées 140/220 ms). **Non lus** : fichier Stripe/SpaceX de awesome-design-md (site bloqué pour l'IA).
- **Contraintes à ne pas casser** : 153 tests (`tests/test_ui.py` vérifie le balisage des cartes par expressions régulières : `>Attention</div><div[^>]*>▲ Degraded<`, couleur et icône issues de `csync/config/theme.json`) ; aucune couleur en dur dans `app.py` ; **inconnu ne ressemble jamais à normal** (carte contexte = pointillée et atténuée) ; jamais la couleur seule ; axe-core 0 violation (jours 7, 9, 10, mouvement normal et réduit) ; `st.html` retire le SVG en ligne ; Streamlit applique une `opacity` aux légendes (déjà corrigée) ; données synthétiques toujours étiquetées à l'écran.
- Mesures déjà faites : `docs/design_ab/` (axe, Lighthouse accessibilité 100 ; performance Lighthouse ~30 = Streamlit, ne départage rien).
- Skill `csync-design` : `docs/skills/csync-design/SKILL.md` (8 principes). À utiliser comme **liste de contrôle**, pas comme direction créative.
- À faire après la refonte : captures du deck (C1–C5) = celles du design retenu, sinon la démo en direct ne ressemblera pas aux diapos 3 à 5.

## 6. Silhouette humaine
Existe seulement dans la page autonome `pitch/silhouette/silhouette_demo.html` (8 zones cliquables, clavier, 45 contrôles qui passent) et sur la diapo 4 comme « Static mock-up · not in the app yet ». **Absente de l'application** (`csync/ui/app.py` n'a aucune sélection de zone). Streamlit retire le SVG cliquable ; option réaliste ≈ 20 min : une liste de 8 zones à l'étape 2 de l'urgence (change des tests, une valeur de saisie guidée SY01). Recommandation de l'IA : ne pas l'ajouter ; à M1 de trancher.

## 7. Règles d'outillage (pièges déjà rencontrés)
- Commits : identité `Team MONOLITH (adresse noreply : voir AGENTS.md)` ; messages terminés par les lignes `Co-Authored-By: Claude …` et `Claude-Session: …`. **Ne jamais réécrire un commit déjà publié.**
- Un hook de fin de session réclame un `--amend --reset-author` sur les commits de `m3-design` (« Unverified ») : **refusé** à chaque fois (réécriture d'historique publié, étiquette cosmétique). À ne faire que sur demande de M1 et après confirmation de M3.
- `git pull --rebase origin <branche>` avant tout push ; pousser avec `git -c push.negotiate=true push origin HEAD:<branche>` ; vérifier avec `git ls-remote --heads origin` (le clone de travail ne suit que `main`, les alertes « commits non poussés » sont de fausses alertes). Après une fusion avec conflit : `git status`, puis `python scripts/build_context.py` et vérifier **0** marqueur `<<<<<<<`.
- `AGENTS.md` dit « jamais de push direct sur `main` » : les documents de nuit y ont été poussés directement, à la demande de M1 (délégation). À rappeler.
- Réseau de l'IA : pas de push de tags (403), pas de `gh pr`, pas d'écriture REST de références, domaine `streamlit.app` et `getdesign.md` bloqués ; GitHub `raw` et `api` en lecture fonctionnent.
- Mots interdits dans README, chaînes et procédures : cause, prove, guarantee, diagnos…, disease. Aucune affirmation chiffrée sans source du dépôt ; si pas de source : « NON VÉRIFIÉ ».
- Outils d'audit disponibles dans l'environnement IA (peuvent avoir disparu) : Playwright, axe-core, Lighthouse, jsdom ; scripts de captures dans `/tmp` (non versionnés).

## 8. Intégrité de la déclaration d'IA (à ne pas oublier)
- Le logo est une image générée par IA, sans filigrane (décision de M1). Le guide officiel exige un filigrane visible sur les images générées par IA ; M1 a lu la règle comme visant le contenu du projet. **Risque connu et accepté par lui.**
- « To our knowledge » : les autres images des diapos sont des captures du logiciel et des figures produites par les scripts du projet ; **à revérifier par M1**.
- Les 3 mentions de relecture du dépôt sont partielles ; la relecture totale est reportée.

## 9. Vérifier soi-même (rien de ceci ne dépend de moi)
```
git clone https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026 && cd MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026
pip install -r requirements.txt && python -m pytest -q          # 153 passed attendu
python scripts/check_consistency.py                              # 0 erreur
CSYNC_STYLE=signal python -m streamlit run csync/ui/app.py       # après git checkout m3-design
git ls-remote --heads origin                                     # branches réelles
```

## 10. Prompt de démarrage à coller dans la nouvelle session
> Tu reprends le projet C-Sync (équipe MONOLITH, NASA Space Apps 2026 Lomé). Lis d'abord `docs/HANDOFF_TOTAL.md` puis `AGENTS.md`. Réponds en français, dis la vérité sans flatter, sois précis et bref. Mission : refaire entièrement le design de l'interface Streamlit (branche `m3-design`) à partir du brief de M1 (futuriste, verre léger, formes) et de ses images de référence, sans casser les 153 tests ni les règles de §5. Propose d'abord 3 directions très différentes en maquettes haute fidélité sur l'écran du jour 9, fais choisir M1, puis implémente, puis mesure (axe, contraste, tests). Ne juge pas toi-même l'effet visuel : prépare le test des 5 secondes. Ne soumets rien, ne déploie rien en production, ne réécris aucun commit publié.
