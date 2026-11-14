# C-Sync — contexte pour IA (généré le 14/11/2026 14:24 UTC, base commit dca82da)
Source unique : ce dépôt public. Si ce fichier date de plus de 6 h, demande à M1 de le régénérer (P5/P8).
Règles pour l'IA qui lit ceci : ne lis que ce qui est ici ; si une page est inaccessible, dis-le ; n'invente rien ; réponds en français ; écris « NON VÉRIFIÉ » pour toute affirmation sans source ici.
Rôles : M1 chef/PO, M5 communication/soumission ; M2 capsule de décision ; M3 interface ; M4 procédures/scénarios. Pitch dim. 12:00-14:00 (5 min, sans questions) ; soumission dim. 23:59. Démo sur données SYNTHÉTIQUES, non validée sur de vrais équipages.


---
# README

<!-- 2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ (line 'What C-Sync does' only) -->
# C-Sync (Care Sync: taking care of the crew) — offline-first crew health operations assistant

**NASA Space Apps Challenge 2026 · Challenge: _Create Health Monitoring Software for Astronauts on Space Missions_ · Team MONOLITH (Lomé)**

> When the ground is 20 minutes away, who protects the decision?

C-Sync helps a crew on a deep-space mission notice unusual changes in health and performance, guides them step by step in an emergency, and protects the decision to resume work — **without needing the ground**. It compares each astronaut to **their own personal baseline**, shows how sure it is, and never shows missing data as normal. The decision stays human by design.

**What C-Sync does, and where it stops:** C-Sync flags what changed against the astronaut's own baseline and proposes the next step. It points to fixed procedure files, shows how sure it is, and leaves every decision to the crew and the crew medical officer. It proposes no treatment or drug and uses no clinical threshold. NASA has not reviewed C-Sync, and it has no clinical validation.

## The demo story — "Mars transit, days 1 to 10"
| Act | Days | What happens |
|---|---|---|
| Baseline | 1-5 | C-Sync learns this astronaut's normal (screen says *baseline being built*, never "normal") |
| 1 · Drift | 6-9 | Sleep drops below 6 h; reaction time and sleepiness rise; dimensions go WATCH then DEGRADED; a fatigue procedure is proposed |
| 2 · Emergency | 9 | A crewmate ticks *chest pain*. The guided procedure opens offline: safety, where, measurements one by one, report. The link is down for 6 h: the report waits in the send queue and arrives **exactly once** (deduplicated by message ID, covered by `tests/test_sendqueue.py`) |
| 3 · Return | 10 | Resume requested with a heart-rate reading that is 14 min old → **REFUSE_RESUME**, even with a Commander override |

## Architecture
```
sources (NASA EDA telemetry · crew check-ins · synthetic scenario)
  → adapters → Measurement (one contract)
  → quality control (missing / artifact / frozen value) → local memory
  → rules engine (personal baseline, deviation d, state per dimension)
  → Decision + resume gate → DecisionCapsule (8 blocks) → UI (Nominal / Action)
                                              └→ send queue (store-and-forward, message_id) → simulated ground (+20 min)
```
Five dimensions: **Body, Attention, Morale, Mission, Habitat**. Four states: **NORMAL, WATCH, DEGRADED, UNKNOWN** (UNKNOWN is never shown as NORMAL).

## Data
| Data | Origin | Use |
|---|---|---|
| ISS cabin CO2, temperature, humidity, radiation — NASA OSDR **Environmental Data App**, mission RR-1 (2014) | **Real, NASA** | Habitat dimension of the story; data-quality checks (a real run of constant CO2 values, 2,646 ppm for 153 h in the raw 5-minute series, is flagged ARTIFACT; origin unknown: sensor or data fill) |
| PhysioNet Wearable Device Dataset v1.0.1 (Empatica E4, 33 valid sessions) | Real, open (ODC-By) | Wrist-sensor noise model (5.1 bpm) and beat coverage (~55 %) |
| Crew physiology, sleep, PVT-B, check-ins | **Synthetic**, labelled, generator `csync-synth-0.1`, seed 42 | The story; the demo uses only synthetic crew data |

Details and limits: [`data/real/`](data/real), [`SOURCES.md`](SOURCES.md), [`HYPOTHESES.md`](HYPOTHESES.md).

## Analysis pilot
Detection methods are compared at equal false-alarm rates in pilot 3 (300 healthy crews, 150 gradual-drift and 150 abrupt-change crews, synthetic; [`docs/METHODES_NASA_DOSSIER.md`](docs/METHODES_NASA_DOSSIER.md) section 7). The engine is the rule v3 (threshold 1.5, two consecutive days): 0.7 % of healthy simulated crews trigger, 95.3 % of gradual drifts and 59.3 % of abrupt changes are detected; the threshold was tuned on the same scenario families, so these figures are not validation. [`research/pilot/`](research/pilot) keeps the earlier pilots, reproducibly. Inspired by NASA HRP's Artemis II Data Methodology Challenge, which favoured individual-level, small-sample methods; C-Sync keeps a simplified, deterministic version that can run offline.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q                 # resume gate G1-G10, rules, send queue, wording
python scripts/run_story.py         # regenerate the story and its outputs
streamlit run csync/ui/app.py       # the interface (work in progress)
```

## Repository map
| Folder | Content |
|---|---|
| `contracts/` | JSON schemas: Measurement, DimensionState, Decision, DecisionCapsule, scenario file, send envelope, procedure file |
| `csync/` | rules engine, resume gate, send queue, wording check, settings, UI |
| `synthetic/` | scenario generator (labelled SYNTHETIC) |
| `data/` | real-data extracts with provenance; procedures; scenarios |
| `research/pilot/` | reproducible analysis pilot (methods comparison) |
| `tests/` | acceptance tests |
| `docs/` | architecture, open decisions, team task cards (French) |
| `pitch/` | 7-slide outline and figures |

## Status (updated at each team checkpoint)
| Part | Status |
|---|---|
| Contracts v0 | drafted, to be validated |
| Rules engine, resume gate, send queue | implemented; 128 automated tests (software stability, not clinical validation) |
| Generator + story data | implemented |
| Decision capsule, UI screens, procedure files | in progress (body map: static mock-up, not in the app) |

## Team & AI use
Team MONOLITH, five members (M1-M5). AI tools were used and are declared in [`AI_USAGE.md`](AI_USAGE.md). License: [MIT](LICENSE).


---
# ARCHITECTURE

# Architecture (résumé)
Monolithe modulaire, hors ligne. Un seul format d'entrée (Measurement), un seul format pour l'écran (DecisionCapsule). Modules : `synthetic/generator.py` (sources simulées), `csync/rules.py` (référence personnelle, écarts, états, décisions), `csync/gate.py` (porte de reprise), `csync/sendqueue.py` (file d'envoi, message_id), `csync/language.py` (mots interdits), `csync/ui/app.py` (Streamlit). À venir : `csync/capsule.py` (M2), `csync/quality.py` (M2), fichiers procédure (M4).


---
# HYPOTHÈSES

# Hypotheses and design parameters (none of them is a clinical threshold)

- Personal baseline: days 1-5 of the story (synthetic). Days 1-5 show UNKNOWN ("baseline being built").
- Drift rule: d = (value − personal mean) / SD in the unfavourable direction; flagged when d ≥ threshold two days in a row. threshold 1.5 with an absolute SD floor per indicator (calibrated on synthetic data, see `docs/METHODES_NASA_DOSSIER.md` section 7).
- Unfavourable direction: sleep ↓, resting HR ↑, reaction time ↑, lapses ↑, sleepiness ↑, stress ↑, perceived load ↑, mood ↓ (mood direction is our proposal). Blood pressure and body temperature are displayed only, not used in the drift rule.
- Glucose: keyboard entry, labelled "no NASA in-flight reference", no threshold, no alert of its own.
- Ground delay: 20 min one way. Maximum age of a resume prerequisite: 10 min.
- Synthetic astronaut: sleep 7.2 h, resting HR 62 bpm, PVT-B 265 ms, KSS 3, stress 3/10 (median of real baseline self-reports in PhysioNet S10), mood 3.8/5, load 4/10.
- What we do not measure: bone, immune system, gravity effects. Said openly.


---
# DÉCISIONS OUVERTES

# Décisions ouvertes — M1, samedi 09:30-10:30
| N° | Question | Défaut proposé | Chiffres du pilote | Décision M1 |
|---|---|---|---|---|
| 1 | Détecteur de dérive | Recommandé : EWMA + plancher d'écart-type (repli : d ≥ 1,5 + plancher). **Codé aujourd'hui : règle v3 seule, seuil 1,5 + planchers absolus (csync/rules.py, Params(), calibré le 14/11). EWMA n'est pas codée ; ne la coder que si M1 le décide.** | fausses procédures 17 % → 2,7 % ; détection 1,5 ET 99,3 % ; 94,7 % avec 10 % de données manquantes (research/pilot/RESULTS.md) | |
| 2 | Amplitude de la dérive de l'histoire | 2,5 ET (provisoire, passé explicitement : drift_amp=2.5 ; le défaut du générateur reste 1,5) | DEGRADED atteint dans 99 % des tirages (200 graines, amplitude 2,5, Params() calibré ; 94 % à 2,0). Vérifié graine 42, jour 7, Attention : Params() calibré (seuil 1,5 + planchers) : amplitude 2,5 → DEGRADED (jours 7–9) ; 2,0 → WATCH le jour 7, DEGRADED le jour 9 ; 1,5 → NORMAL | |
| 3 | Référence de 5 ou 7 jours | 5 jours | 7 jours : aucune amélioration (12 % de fausses procédures) | |
| 4 | UNKNOWN compte-t-il comme « hors NORMAL » ? | Non | sinon 8 procédures au lieu de 3 dans l'histoire | |
| 5 | Sens de l'humeur ; tension et température dans la règle ? | humeur ↓ défavorable ; TA et T affichées seulement | — | |
| 6 | Mission et Habitat dans le décompte des dimensions ? | Non (contexte) | — | |
| 7 | Criticité d'un épisode ouvert | garder le niveau le plus haut (déjà codé) | — | |
| 8 | Tension : une mesure par valeur ou value_text ? | une mesure par valeur, value_text SYS/DIA (déjà codé) | — | |

**Valeurs provisoires ajoutées le 14/11 (M1 valide) :** `ui_hint` : CONTINUE → NOMINAL ; OPEN_PROCEDURE CRITICAL → ACTION ; OPEN_PROCEDURE ROUTINE/IMPORTANT, PAUSE, REFUSE_RESUME → FOCUS. `ground_delay_min` = 20 est la valeur de démonstration figée par le contrat (le délai réel vers Mars va jusqu'à ~22 min). Texte de livraison : seule source = `delivered_once` dans `csync/config/strings_en.json`.


---
# CHECKLIST DE LIVRAISON

# Liste « avant de publier » (V1 à V12) — M5
V1 Produit à partir du 14/11 (début confirmé par les organisateurs) · V2 Aucun code préexistant sans accord écrit de M1 · V3 Toute source citée dans SOURCES.md · V4 Données synthétiques étiquetées (version + graine) · V5 Aucun seuil clinique sans citation · V6 Aucun nom, numéro, clé, donnée personnelle, image de mineur · V7 Le changement dit quel test il couvre · V8 Message de commit « Mx: … » · V9 Licence MIT, dépendances compatibles · V10 Relu par quelqu'un d'autre que l'auteur · V11 AI_USAGE.md à jour · V12 Liste du code, textes, images à jour (images IA filigranées)


---
# JOURNAL DES MISES À JOUR

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


---
# PROGRAMME OFFICIEL

# Programme officiel — source unique des horaires (Lomé = UTC)
Version 1 · 14/11/2026 06h15 · Statut : VÉRIFIÉ sur le communiqué et le programme des deux jours reçus par M1 · Remplace : tout horaire cité ailleurs
- Samedi 14/11 : début du travail 09:30 ; travail libre 17:00–00:00.
- Dimanche 15/11 : pitch et jury 12:00–14:00 (5 minutes par équipe, SANS questions du jury, démonstration en direct si possible) ; délibération et prix locaux 14:00–14:45.
- Soumission : jusqu'au dimanche 15/11 à 23:59 heure locale. Plusieurs soumissions possibles, seule la dernière est jugée.
- Format de démonstration : 7 diapositives ou vidéo de 30 secondes, en anglais. Données NASA requises pour les prix mondiaux.
- Équipe : 6 membres au plus, ajouts tardifs possibles. Crédits Cursor donnés sur place.
- Critères de jugement annoncés : Impact, Créativité, Validité, Pertinence, Présentation (mise à jour à venir, à reporter ici avec date).
- À confirmer par M1 : heure exacte du pitch ; trace écrite de l'autorisation orale de commencer ce soir (la FAQ officielle dit aucun travail avant samedi 09:00).


---
# CONSIGNES POUR TOUS

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
