<!-- 2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ (line 'What C-Sync does' only) -->
# C-Sync (Care Sync: taking care of the crew) — offline-first crew health operations assistant

**NASA Space Apps Challenge 2026 · Challenge: _Create Health Monitoring Software for Astronauts on Space Missions_ · Team MONOLITH (Lomé)**

> When the ground is 20 minutes away, who protects the decision?

> **Version note (for judges).** The version submitted to Space Apps is commit `de0b5be` (15 Nov 2026, 17:42 UTC, before the 23:59 deadline): browse it at <https://github.com/josephhounto-sudo/MONOLITH-NASA-SPACE-CHALLENGE-LOME-2026/tree/de0b5be>. Everything below the line "After the deadline" was built later (V3, 16–20 Nov) and is shown for transparency; if the rules judge the submitted version only, please use that commit.
>
> **After the deadline (V3, 16–20 Nov, branch `main`):** the live app (<https://monolith-nasa-space-challenge-lome-kwtv79qy52ihwgezt8byuy.streamlit.app/>) opens on **real ISS cabin air, live from NASA's public ISSLive feed** (CO2, oxygen share, cabin pressure, ground-link status, four clocks). Pick a role first (crew member or commander); the navigation follows the visitor's path: *Now* (live station, commander board), *What C-Sync does* (demo story, emergency guide with five NASA-sourced cases, body map, technologies) and *Where it comes from* (real NASA habitat data, evidence, sources). Pip, a guide (not an AI), stays bottom-left and leads to the next step. Every technology card can be touched; each says whether it is built and tested, a prototype (DTN messaging, camera pulse, eye blink, crew-wide signal, exposure ledger, offline explainer) or a promise, with the test that decides it. Live NASA data is context only: it never opens a procedure. Process documents moved to `docs/archive/`; the current plan and retrospective are in `docs/PLAN_V3.md`.

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
| ISS cabin CO2, temperature, humidity, radiation — NASA OSDR **Environmental Data App**, mission RR-1 (2014) | **Real, NASA** | Habitat **state, computed**: the Habitat dimension compares the real CO2 series with the NASA-STD-3001 requirement (3 mmHg one-hour average, converted from ppm at 760 mmHg, approximate) with quality flags; hours flagged ARTIFACT never count and fewer than 12 valid hours gives Unknown; the habitat never opens a procedure by itself and does not change the crew-drift decision; the panel also compares 14 missions (a real run of constant CO2 values, 2,646 ppm for 153 h in the raw 5-minute series, is flagged ARTIFACT; origin unknown: sensor or data fill) |
| PhysioNet Wearable Device Dataset v1.0.1 (Empatica E4, 33 valid sessions) | Real, open (ODC-By) | Wrist-sensor noise model (5.1 bpm) and beat coverage (~55 %) |
| Crew physiology, sleep, PVT-B, check-ins | **Synthetic**, labelled, generator `csync-synth-0.1`, seed 42 | The story; the demo uses only synthetic crew data |

Details and limits: [`data/real/`](data/real), [`SOURCES.md`](SOURCES.md), [`HYPOTHESES.md`](HYPOTHESES.md).

## Analysis pilot
Detection methods are compared at equal false-alarm rates in pilot 3 (300 healthy crews, 150 gradual-drift and 150 abrupt-change crews, synthetic; [`docs/METHODES_NASA_DOSSIER.md`](docs/METHODES_NASA_DOSSIER.md) section 7). The engine is the rule v3 (threshold 1.5, two consecutive days): 0.7 % of healthy simulated crews trigger, 95.3 % of gradual drifts and 59.3 % of abrupt changes are detected; the threshold was tuned on the same scenario families, so these figures are not validation. A held-out run on seeds never used for tuning gives 0.0 % false procedures, 92.7 % gradual and 57.3 % abrupt detection, still synthetic ([`docs/VALIDATION_HOLDOUT.md`](docs/VALIDATION_HOLDOUT.md)). [`research/pilot/`](research/pilot) keeps the earlier pilots, reproducibly. Inspired by NASA HRP's Artemis II Data Methodology Challenge, which favoured individual-level, small-sample methods; C-Sync keeps a simplified, deterministic version that can run offline. **Held-out check (15/11/2026, seeds never used for tuning, no retuning):** 0/300 healthy crews triggered a procedure, 139/150 (92.7 %) gradual drifts and 86/150 (57.3 %) abrupt shifts were detected ([`docs/VALIDATION_HOLDOUT.md`](docs/VALIDATION_HOLDOUT.md)). Synthetic crews only; nothing is clinically validated.

## Prototypes added on 15/11/2026
- **Commander board** (app tab): the same rule on six synthetic crew members, sorted by urgency; it decides nothing, every open procedure waits for a human.
- **Device-feed reader** (`csync/devicefeed.py`): reads a text format of daily measurements (format check only); no real device is connected.
- **Real NASA data** stays limited to ISS cabin telemetry (habitat context); no real crew physiology.

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
| Rules engine, resume gate, send queue | implemented; 211 automated tests (software stability, not clinical validation) |
| Generator + story data | implemented |
| Decision capsule, UI screens, procedure files | implemented; the three screens (days 7, 9, 10) are covered by automated screen tests (the body map has eight selectable zones in the app; the Habitat panel shows real NASA ISS data with quality control) |

## Team & AI use
Team MONOLITH, five members (M1-M5). AI tools were used and are declared in [`AI_USAGE.md`](AI_USAGE.md). License: [MIT](LICENSE).
