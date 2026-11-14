# C-Sync — Care Sync: taking care of the crew

**NASA Space Apps Challenge 2026 · Lomé · Team MONOLITH**
Challenge: *Create Health Monitoring Software for Astronauts on Space Missions*

> When the ground is 20 minutes away, who protects the decision?

C-Sync is an offline-first assistant that helps a crew notice unusual changes against each astronaut's **own baseline**, guides the crew step by step in an emergency, and keeps the decision with a human. Crew data in our demo is **synthetic and labelled as such**.

**Status: work in progress (hackathon, 14–15 Nov 2026).** This commit publishes the base structure only; content is added during the event.

## Repository structure
| Folder | Purpose |
|---|---|
| `contracts/` | data contracts (JSON schemas) |
| `csync/` | engine, decision capsule, UI |
| `synthetic/` | labelled synthetic scenario generator |
| `data/` | real-data extracts (with provenance), procedures, scenarios |
| `research/pilot/` | reproducible analysis pilots |
| `tests/` | automated tests |
| `scripts/` | helper scripts |
| `docs/` | documentation |
| `pitch/` | pitch material |

See [`SOURCES.md`](SOURCES.md), [`HYPOTHESES.md`](HYPOTHESES.md) and [`AI_USAGE.md`](AI_USAGE.md). C-Sync has not been validated by NASA or clinically. License: [MIT](LICENSE).
