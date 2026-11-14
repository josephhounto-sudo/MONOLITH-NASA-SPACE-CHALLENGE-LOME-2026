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
