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
| ISS cabin CO2, temperature, humidity, radiation — NASA OSDR **Environmental Data App**, mission RR-1 (2014) | **Real, NASA** | Habitat **context** and data-quality checks only: the screen shows Habitat as "Context only", it is not scored (a real run of constant CO2 values, 2,646 ppm for 153 h in the raw 5-minute series, is flagged ARTIFACT; origin unknown: sensor or data fill) |
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
streamlit run csync/ui/app.py       # the interface
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
| Rules engine, resume gate, send queue | implemented; 153 automated tests (software stability, not clinical validation) |
| Generator + story data | implemented |
| Decision capsule, UI screens, procedure files | implemented; the three screens (days 7, 9, 10) are covered by automated screen tests (body map: static mock-up, not in the app) |

## Team & AI use
Team MONOLITH, five members (M1-M5). AI tools were used and are declared in [`AI_USAGE.md`](AI_USAGE.md). License: [MIT](LICENSE).
