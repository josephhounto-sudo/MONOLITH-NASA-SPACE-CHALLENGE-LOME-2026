# Journal des mises à jour envoyées aux IA (P4)
| N° | Date/heure (Lomé) | Pour | Ce qui change | Commit |
|---|---|---|---|---|
| bloc v1 | 14/11 05:45 | assistant code M2–M4 | première version | e9e4973 |
| MAJ 1 | 14/11 06:00 | assistant code M2–M4 | fichiers manquants fournis ; valeurs provisoires (drift_amp 2.5, ui_hint, délai, texte de livraison) | f5b3836 |
| bloc maquette v1 | 14/11 06:15 | assistant maquette/pitch | première version | 3246539+ |
| MAJ 2 | 14/11 06:30 | assistant code M2–M4 | rôle TRANSVERSAL et protocoles P1–P12 | voir git log |

- 14/11 MAJ 2 : dossier méthodes section 7 (pilote 3, calibration équitable, IC, délais). Moteur inchangé. Constat : Params() par défaut = 17 % de fausses procédures sur équipages témoins (décision seuil → M1).
- 14/11 MAJ 3 : validation phase 1 maquette/pitch + ordres phase 2 (VALIDATION_PHASE_1_MAQUETTE_PITCH.md). Diapo 6 sans pourcentage tant que M1 n'a pas fixé le seuil ; silhouette = décision ouverte M1.
- 14/11 MAJ 4 : décision M1 seuil → Params() = seuil 1,5 + planchers ; démo histoire drift_amp 2.5 (jour 7 Attention DEGRADED). Silhouette : construite par le chat maquette avant le départ, testée sur place. Transcription vidéo : résumé jugé suffisant par M1 (citations restent NON VÉRIFIÉES).
- 14/11 MAJ 5 : intégration du travail du chat M2–M4 (capsule.py, quality.py, scénarios attendus, procédures, UI capsules, 91 tests). Réalignement sur le seuil calibré : drift_amp 2.5, DEV-01 clos (xfail retirés), DEV-02 (entrée de scénario modifiée, sorties attendues intactes).
- 14/11 MAJ 6 : tâche lourde chat M2–M4 (TACHE_LOURDE_chat_M2M4.md : captures, sources UI, raisons de refus lisibles, tests de calibration, mots interdits). GitHub : structure de base poussée (c57e63c), rien d'interne.
- 14/11 MAJ 7 : validation phase 2 pitch + phase 3 (silhouette, deck, script FR, vidéo 30 s, fiches). Sources NASA délai/blackouts vérifiées en lecture complète.
- 14/11 MAJ 8 : bloc Gemini Pro v2 (G1 audit des pilotes, G2 catalogue de données NASA, G3 ré-implémentation contre vecteurs). Parcours v10 : avancement principal/accessoire, comptes à rebours, états des tâches.
- 14/11 11:45 MAJ 9 : intégration des 3 rendus (code MAJ5 : 127 tests ; pitch phase 3 : deck, silhouette, script FR, vidéo ; audit indépendant). Captures C1–C6 insérées, C6 refaite en anglais, sources NASA dans la silhouette (cœur, tension, sommeil). OUTLINE.md obsolète, RESULTS.md marqué partiellement obsolète.
- 14/11 14:50 MAJ 10 : passation Cursor (AGENTS.md, docs/CURSOR_HANDOFF.md) ; pré-mortem de l'artefact Parcours (PREMORTEM_ARTEFACT_14-11.md) ; artefact simplifié 8→4 onglets.
- 14/11 15:05 MAJ 11 : D6, D9, D10, D11 tranchées par M1 ; logo intégré ; SCRIPT_FR v3 (formulations absolues adoucies), SCRIPT_EN v1 ; diapo 5 « Stale data is flagged as expired » ; bloc lourd Cursor.
- 14/11 17:35 MAJ 12 : travail M4 (Jean) intégré : branches m4-procedures (5 tests, en-têtes « validation humaine M4 : à faire ») et m4-expected (tests de scénarios, `scripts/recette_m4.py`, `docs/RECETTE_M4.md`, DEV-03). DEV-03 corrigé dans `sendqueue.ground_view` et clos ; README/STORY : Habitat = contexte, non évalué. 153 tests. Non repris : modification non commitée de HELP_CARD_SOURCES.md (en-tête « VÉRIFIÉ PAR M4 » sans preuve, tableau reformaté).
- 14/11 21:00 MAJ 13 : registre des décisions ouvertes créé (docs/A_TRANCHER.md) ; état vérifié : main 8e03e59, 153 tests, check_consistency 0 erreur ; aucun commit M2/M3 visible sur origin. Rien appliqué sans réponse de M1.
- 14/11 21:45 MAJ 14 : décisions M1 reçues (A1 hybride construit sur m3-design 4035e4d ; A3 EWMA non appliqué, motif écrit) ; M3 : changement local non commité, 3 tests rouges, non intégré ; M2 : rien visible sur origin ; « blackouts of weeks » non vérifié.
- 15/11 04:55 MAJ 15 : diapo 2 et scripts EN/FR alignés sur l'abstract NTRS 20220013418 lu dans le navigateur (délai 0–22 min ; coupures de plusieurs jours à plusieurs mois) ; remplace « up to ~20 min (HRP) » et « weeks ». PDF et pptx de secours régénérés ; 153 tests, test_deck OK.
