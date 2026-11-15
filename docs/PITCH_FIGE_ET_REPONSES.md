# Pitch figé + réponses aux questions — 15/11/2026 ~10:30 UTC
Statut : FAIT PAR L'IA — chaque chiffre ci-dessous a été recontrôlé dans le dépôt (fichier source indiqué). « NON VÉRIFIÉ » = absent du dépôt, ne pas affirmer.

## A. Ce qui est FAIT (preuve dans le dépôt)
| Élément | Preuve |
|---|---|
| Règle v3 : écart ≥ 1,5 ET sur la référence personnelle (jours 1–5), 2 jours consécutifs ; valeur manquante = UNKNOWN | `csync/rules.py`, `tests/` |
| Histoire de 10 jours en trois actes + variantes témoin et capteur en panne | `docs/STORY.md` |
| Urgence guidée (symptôme coché → CRITICAL immédiat) | `csync/rules.py` l.98 |
| Porte de reprise : refus si mesure > 10 min ; l'override du Commandant est consigné, jamais suffisant seul | `csync/gate.py` |
| Compte rendu « en attente de décision humaine », file d'envoi hors ligne sans doublon | `csync/capsule.py`, `csync/sendqueue.py` |
| Validation sur graines tenues à l'écart : 0/300 faux (0,0 %, IC 0,0–1,3 %), 92,7 % dérives lentes, 57,3 % sauts brusques | `docs/VALIDATION_HOLDOUT.md` |
| Données NASA réelles retraitées à l'ouverture : 759 525 points, 20 missions (télémétrie de cabine, pas de physiologie) | onglet « Evidence at scale », `csync/scale.py` |
| Valeur de CO2 constante ≈ 153 h (RR-1) signalée ARTIFACT | `docs/PREMORTEM_14-11.md` |
| App manipulable (saisie des jours 6–7, même règle, note SBAR) | onglet « Try it yourself », `csync/live.py` |
| 195 tests automatiques verts | `python -m pytest -q` |
| Silhouette cliquable en volume (SVG), verre v2, glyphes d'état | `csync/silhouette.py`, `csync/ui/style.py` |

## B. Ce qui sera fait APRÈS le pitch (rien de cela n'est affirmé comme fait)
1. Relecture des règles par des experts en médecine spatiale (relecture M4 = en attente).
2. Essai sur des données de missions d'isolement simulé (analogues).
3. Branchement de vrais capteurs (adaptateurs).
4. Référence avant mission pour éviter la référence faussée des jours 1–5.
5. Chiffrement et contrôle d'accès des données de santé (absents aujourd'hui).
6. Plan de secours en procédures imprimées.
7. Chiffrage du coût d'intégration.
8. Diaporama bilingue EN/FR ; lancement des tâches Cursor (`docs/CURSOR_PROMPT_COMPLET.md`) : comparaison EWMA, contrôles qualité, mémoire, chaînes FR, tests de chaque chiffre affiché.
9. Re-mesure axe et contraste après les derniers onglets.

## C. Corrections à faire dans la fiche de réponses (avant de la lire)
| Dans la fiche | Problème | Remplacer par |
|---|---|---|
| « 155 tests automatiques » | périmé | **195** tests |
| « 0,7 % sur 300 équipages » | c'est le chiffre de réglage | « **0 sur 300** équipages tenus à l'écart » ; ajouter « 93 % des dérives lentes, 57 % des sauts brusques » |
| « capteur figé pendant 153 heures » | la cause (capteur ou remplissage) est inconnue (`PREMORTEM_14-11.md` R1) | « une valeur de CO2 **constante pendant plus de six jours**, signalée ARTIFACT » |
| Q4 « données de l'ISS pour les contrôles qualité » | exact, mais JUGE_CRUEL précise : télémétrie de cabine, pas un équipage | garder « télémétrie de cabine, aucune donnée de santé d'astronaute » |
| Q11 « vu sur les données de l'ISS : capteur en panne → UNKNOWN » | mélange deux cas | « Capteur en panne (variante simulée) : UNKNOWN et refus de reprise. Série constante réelle de l'ISS : ARTIFACT. » |
| Q1 Bio-Monitor, Reaction Self Test, CMO-DA | **NON VÉRIFIÉ** : aucune source dans le dépôt | M2 donne la source, sinon dire : « D'autres outils mesurent ou conseillent ; nous n'avons pas trouvé, dans les sources publiques que nous avons lues, de dérive personnelle + refus de reprise. Nous ne l'avons pas encore vérifié de façon exhaustive. » |
| Q5 « quatre indicateurs » | **NON VÉRIFIÉ** dans le dépôt | présenter comme « ce que nous mesurerions », pas comme existant |
| Q2, Q7 | engagements d'équipe | M1 confirme avant le pitch (déjà noté dans la fiche) |
| Sécurité des données | rien en place (seule une empreinte SHA-256 sert d'identifiant de message) | « Pas encore : chiffrement et accès sont une prochaine étape. Les données de la démo sont synthétiques. » |

## D. Synchronisation faite à 10:55 UTC (remplace la version de 10:35)
- **Diapo 2 = problème + objectif** (l'ancienne diapo « Far from help » est fusionnée). Quatre lignes avec étiquette : Guider l'urgence = Fait ; Aider le commandant = Prototype ; Lire les données NASA = Habitat seulement ; Brancher de vrais capteurs = Prévu. Source ASCEND conservée en pied.
- **Diapo 4** : vraie carte du corps de l'app. **Diapo 7** : « Next: expert review, analog data, sensors ».
- **Deck FR** généré depuis le deck EN (`pitch/deck/make_fr.py`, tout texte manquant arrête le script) : `deck_fr_final.html`, `C-Sync_pitch_7_slides_FR.pdf`, PowerPoint de secours FR. Plafond de mots : 25 en anglais, 32 en français (le français est plus long ; tests verts). Les captures restent en anglais (l'app n'a pas de chaînes françaises).
- **L'app a maintenant de quoi prouver la diapo 2** : onglet « Commander board » (6 équipiers simulés, même règle, triés par urgence, « human decision pending », aucune décision automatique) ; onglet « Try it yourself » accepte un flux de capteur au format JSON lines (lignes invalides rejetées avec la raison, valeur manquante = UNKNOWN). Aucun appareil réel n'est branché : c'est un format, pas une intégration.
- Scripts FR et EN : diapo 2 réécrite, tableaux de minutage recalculés (diapo 2 lente : 111 mots/min FR, 106 EN, à chronométrer).
- axe-core : 0 violation sur les 8 onglets. 202 tests verts. Contraste en pixels non relancé.

## D2. Coût et ambition (réponses 2 et 7)
Coûts réels : **aucun chiffre dans le dépôt** (`TODO_M1`). Ce qui est établi : le logiciel tourne sur un ordinateur ou une tablette. Postes de coût à nommer sans montant : relecture par des experts, intégration, validation sur données d'analogue, capteurs (matériel de l'agence). Aucun montant à dire.
Les fiches du dépôt ne donnent que les rôles (M1 chef/PO et communication, M2 capsule de décision, M3 interface, M4 procédures et scénarios), pas les parcours personnels.
Ambition unique proposée (M1 confirme) : « Si nous gagnons, nous faisons relire les règles par des experts en médecine spatiale, puis nous les testons sur des données de missions d'isolement simulé. » Les capteurs réels et le reste viennent après.

## D3. Après le pitch (même liste que dans l'app et la diapo 7)
1. Relecture par des experts en médecine spatiale · 2. Essai sur données d'analogue · 3. Capteurs réels · 4. Référence avant mission · 5. Protection des données de santé · 6. Procédures imprimées · 7. Coût d'intégration à chiffrer.

## D4. Les 13 questions : où en est chaque réponse
| Questions | État |
|---|---|
| 3, 4, 6, 8, 9, 10, 12, 13 | Répondues, appuyées sur le dépôt |
| 5, 11 | Répondues après correction (voir C) |
| 1 | Réponse prudente : Bio-Monitor, Reaction Self Test et CMO-DA sont NON VÉRIFIÉS, M2 doit sourcer |
| 2, 7 | Réponse prête, engagement à confirmer par M1 |
| Sécurité des données | Réponse honnête : rien en place, prochaine étape |

## E. Réponses validées (prêtes à dire)
1. Différence : « D'autres outils mesurent ou conseillent. Nous ajoutons la dérive par rapport à la référence personnelle, et le refus de reprise si la donnée est périmée. Nous complétons, nous ne remplaçons pas. »
2. Coût : « Logiciel sur ordinateur ou tablette. Nous n'avons pas chiffré, c'est la prochaine étape. » (aucun chiffre en euros)
3. Utilisateurs réels : « Pas encore. 195 tests automatiques et une histoire simulée de 10 jours. Aucune validation clinique. »
4. Données : « Équipage simulé, étiqueté synthétique partout, et télémétrie de cabine NASA pour le contrôle qualité. Aucune donnée de santé réelle. »
5. Impact : « Aujourd'hui : 0 faux déclenchement sur 300 équipages simulés tenus à l'écart, 93 % des dérives lentes repérées, 57 % des sauts brusques. Réglé sur des scénarios simulés : pas un résultat clinique. »
6. Hors ligne : « Le calcul est local, les comptes rendus attendent en file. Sans électricité, rien ne fonctionne ; procédures imprimées en suite. »
7. Si nous gagnons : relecture par des experts, vrais capteurs, essai sur données d'analogue (M1 confirme).
8. Règles plutôt qu'IA : chaque état renvoie à une règle lisible ; la décision reste humaine.
9. Seuils : paramètres de conception réglés sur des scénarios simulés, pas des seuils médicaux ; à valider par des experts.
10. Dérive ratée : limite assumée (57 % des sauts brusques seulement). Garde-fous : symptôme coché → procédure immédiate ; donnée manquante → UNKNOWN.
11. Capteur en panne : voir tableau C.
12. Fatigue dès le début : limite réelle, la référence serait faussée ; jours 1–5 sans alerte de dérive ; piste : mesures d'avant mission.
13. Responsabilité : l'humain. Compte rendu « en attente » ; override consigné, jamais suffisant seul.
Phrase de repli : « Nous ne l'avons pas encore vérifié, c'est notre prochaine étape. »
Ne jamais dire : « la NASA n'a rien » ; aucun coût, test réel ou résultat clinique.
