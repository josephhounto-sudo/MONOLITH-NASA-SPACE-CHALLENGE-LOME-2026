# Consignes pour M2 — pitch et soumission (dimanche 15/11/2026)
FAIT PAR L'IA — décisions de M1 révocables. Aucun nom dans ce fichier (règle du dépôt).

## 1. Ton audit est intégré
Ton rapport a été lu ; les 3 fichiers de code (`scripts/run_story.py`, `tests/test_rules.py`, `tests/test_run_story.py`) ont été repris tels quels (liste fixe de `procedure_id`, test « valeur manquante = UNKNOWN »). `AI_USAGE.md` : seule ta ligne Grok a été ajoutée (ta version du fichier effaçait la déclaration du logo IA, elle n'a pas été reprise). Résultat : **155 tests verts**. Les 4 points A–D sont tranchés plus bas.

## 2. Liens (à ouvrir en fenêtre privée, sans te connecter)
| Quoi | Lien |
|---|---|
| Dépôt public | https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026 |
| Les 7 diapos (PDF, = lien de démo de la soumission) | https://github.com/josephhounto-sudo/monolith-nasa-space-challenge-lome-2026/blob/main/pitch/deck/C-Sync_pitch_7_slides.pdf |
| Ton texte (orateur B) | `pitch/deck/SCRIPT_EN.md`, diapos 4 et 5 ; version française : `pitch/deck/SCRIPT_FR.md` |
| Textes de soumission prêts à copier | `docs/SUBMISSION.md` |
| App de test (test seulement, pas le lien de soumission) | https://monolith-nasa-space-challenge-lome-kwtv79qy52ihwgezt8byuy.streamlit.app/ |
| État complet du projet | `docs/HANDOFF_TOTAL.md` |

## 3. Pitch : tu es l'orateur B (diapos 4 et 5, 110 s, démo comprise)
À faire avant **11:00** :
1. Lis `SCRIPT_EN.md` diapos 4 et 5. Dis le texte à voix haute **3 fois au chronomètre** : diapo 4 ≤ 60 s, diapo 5 ≤ 50 s. Pas de lecture : apprends les repères, pas les phrases.
2. Lance la démo à l'avance (jour 10, bouton « Request resume », puis « Commander override »). Ouvre l'app avant de monter sur scène. Si rien ne s'affiche en 10 s : passe à la capture C5 de la diapo et dis le même texte.
3. Phrase à ne pas dire autrement : « un override seul ne suffit pas pour reprendre ». Dis **« données simulées »** quand tu parles des chiffres.
4. Coupures si tu es en retard : la phrase sur la glycémie (diapo 4).
5. Dis à M1 le résultat de ton chrono.

Ne dis jamais : « diagnostic », « prouvé », « cliniquement validé », « garanti ». Pas de questions à la fin (règle de l'épreuve).

## 4. Soumission : tu es suppléant (D9)
- À **11:00** : confirme à M1 que tu es disponible jusqu'à 23:59. Seul M1 remplit et soumet le formulaire avec son compte ; tu ne soumets rien sans accord écrit de M1 dans le groupe.
- Vérifie en **fenêtre privée** : le lien du dépôt et le lien du PDF s'ouvrent sans connexion. Écris à M1 « OK » ou le lien qui échoue.
- Compare chaque champ de `docs/SUBMISSION.md` au guide officiel (8 champs) et note les écarts, sans modifier le fichier.

## 5. Tes points A–D : réponse (valable jusqu'à désaccord de M1)
| Point | Décision |
|---|---|
| A. Mesure postérieure à la demande de reprise | **Limite connue, non corrigée** : `gate.py` est figé (gel passé). À écrire dans `docs/TEST_DEVIATIONS.md` ; tu peux proposer un test qui échoue sur une branche à part, sans l'intégrer. |
| B. La porte ne vérifie pas la valeur | **Voulu** : aucun seuil clinique. À dire en une phrase si on te le demande ; pas de diapo. |
| C. Tout UNKNOWN = CONTINUE / NOMINAL | **Pas de nouvel indice** avant la soumission (changement d'écran). À noter comme limite. |
| D. Indicateur manquant : WATCH devient UNKNOWN | **Voulu**, conforme à la règle écrite. |
| `ui_hint` : REFUSE_RESUME et PAUSE vers FOCUS | **Provisoire gardé** ; l'écran « Reprise refusée » est piloté par le type de capsule. Ne pas toucher. |

## 6. Ce que tu ne fais pas
Pas de push sur `main`, pas de fusion, pas de changement de `gate.py`, des contrats ou de l'interface. Une branche par tâche, message de commit « M2: … ». Retire la mention « FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ » d'un fichier seulement après l'avoir relu entièrement.

## 7. Chiffre du CO2 (à citer comme M2 l'a écrit)
« Au moins 37 h dans l'extrait horaire, environ 153 h dans la série brute de 5 minutes. » Origine inconnue : ne dis pas « capteur gelé ».
