# Sources

## NASA data and resources
- **NASA OSDR Environmental Data App (EDA)** — https://visualization.osdr.nasa.gov/eda/ — ISS cabin telemetry and radiation, missions RR-1 to RR-28; accessed 14/11/2026. *Data and visualizations are courtesy of the Environmental Data App (EDA).* Units read on the page: °C, %, ppm, mGy/day; cadence 5 min or 1 min.
- **NASA Human Research Program — Risks of Human Spaceflight** — https://www.nasa.gov/hrp/risks/ (sleep, behavioral health, cardiovascular).
- **NASA HRP — 5 Hazards of Human Spaceflight** — https://www.nasa.gov/hrp/hazards/
- **NASA HRP — Ongoing HRP Research in Space** — https://www.nasa.gov/hrp/ongoing-hrp-research/ — listed as an official resource on the challenge page; added 15/11/2026; text snapshot in `data/nasa_official/nasa_hrp_ongoing_research.txt`.
- **CSA (Canadian Space Agency) — Monitoring Radiation for Astronaut Health** — https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp — official challenge resource, read-only reference, not used, text not copied.
- **CSA — Why Do We Conduct Science Experiments in Space?** — https://www.asc-csa.gc.ca/eng/iss/science/why-do-we-conduct-science-experiments-in-space.asp — official challenge resource, read-only reference, not used, text not copied.
- Snapshots of the NASA HRP hazards and risks pages (read 15/11/2026): `data/nasa_official/`. Full inventory: `docs/NASA_RESSOURCES_OFFICIELLES.md`.
- **NASA Life Sciences Portal** — https://nlsp.nasa.gov/explore — catalogue searched 14/11/2026; experiment NAG53952 (PVT, KSS, sleep) cited as prior work (open access = final report only).
- **Winners of NASA HRP's Artemis II Data Methodology Challenge** (11/09/2026) — https://www.nasa.gov/hrp/winners-of-nasa-hrps-artemis-ii-data-methodology-challenge/ — methodological inspiration (individual-level, small-sample methods). Not a validation of C-Sync.
- NASA ASCEND, *Communication Delays, Disruptions, and Blackouts for Crewed Mars Missions*, NTRS 20220013418 (abstract read on ntrs.nasa.gov, 15/11/2026: delay 0 to 22 min one way; disruptions "several days up to several months").

## Other data
- Hongn A., Bosch F., Prado L., Bonomini P. (2025). *Wearable Device Dataset from Induced Stress and Structured Exercise Sessions* (v1.0.1). PhysioNet. https://doi.org/10.13026/he0v-tf17 — ODC-By 1.0. Also: Hongn et al. (2025), *Scientific Data* 12(1). And Pollard T. et al. (2026), PhysioNet, *Nature Health*.

- Thambawita V. et al. (2020). *PMData: a sports logging dataset* (OSF, https://osf.io/vx4bk/), 16 people, read 15/11/2026. Licence: the paper states CC BY-NC 4.0 (research and teaching), the OSF API shows CC BY 4.0; both are recorded. Used only for the analog-data format trial (`docs/ANALOG_TRIAL.md`), file fingerprints in `data/real/raw/SHA256SUMS.txt`; not used in the demo.

## Methods
- Basner M., Mollicone D., Dinges D. F. (2011). Validity and sensitivity of a brief psychomotor vigilance test (PVT-B). *Acta Astronautica* 69, 949-959 — 3-minute PVT, lapse ≥ 355 ms.

## Software
Python, NumPy, pandas, Matplotlib, Streamlit, Plotly, jsonschema, pytest (open source licenses).
