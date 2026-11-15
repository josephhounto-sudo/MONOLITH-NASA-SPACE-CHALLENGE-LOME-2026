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

## D. Écarts entre le script du pitch et l'app (à décider par M1, rien modifié)
- Diapo 4 dit « carte du corps … en maquette, non codée » : la silhouette est maintenant codée dans l'app. Soit garder la phrase (prudent), soit la corriger.
- Aucun script ne mentionne l'onglet « Try it yourself » ni « Evidence at scale » : la démo en direct ne les utilise pas. Ne pas les ajouter dans les 5 minutes sans répétition chronométrée.

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
