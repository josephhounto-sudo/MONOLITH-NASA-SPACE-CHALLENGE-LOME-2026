# Hypotheses and design parameters (none of them is a clinical threshold)

- Personal baseline: days 1-5 of the story (synthetic). Days 1-5 show UNKNOWN ("baseline being built").
- Drift rule: d = (value − personal mean) / SD in the unfavourable direction; flagged when d ≥ threshold two days in a row. threshold 1.5 with an absolute SD floor per indicator (calibrated on synthetic data, see `docs/METHODES_NASA_DOSSIER.md` section 7).
- Unfavourable direction: sleep ↓, resting HR ↑, reaction time ↑, lapses ↑, sleepiness ↑, stress ↑, perceived load ↑, mood ↓ (mood direction is our proposal). Blood pressure and body temperature are displayed only, not used in the drift rule.
- Glucose: keyboard entry, labelled "no NASA in-flight reference", no threshold, no alert of its own.
- Ground delay: 20 min one way. Maximum age of a resume prerequisite: 10 min.
- Synthetic astronaut: sleep 7.2 h, resting HR 62 bpm, PVT-B 265 ms, KSS 3, stress 3/10 (median of real baseline self-reports in PhysioNet S10), mood 3.8/5, load 4/10.
- What we do not measure: bone, immune system, gravity effects. Said openly.
