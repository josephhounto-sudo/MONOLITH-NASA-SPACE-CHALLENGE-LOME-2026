# Test deviations (expected written BEFORE running vs observed)

Rule: the expected files in `data/scenarios/` are never edited to match the output. Every gap is recorded here and sent to M1.

## DEV-01 — Control and sensor variants show Morale WATCH with no drift (14/11/2026)
- **Expected (written first, commit "M4-2: expected results written before any scenario run"):** `temoin` days 6-10 and `capteur` days 6, 8-10: Body, Attention, Morale all NORMAL (STORY.md: control = no drift).
- **Observed (rule v3, `Params()`, seed 42):** `temoin` day 8 and day 9: Morale WATCH. `capteur` day 9: Morale WATCH. Decision stays CONTINUE everywhere (only one dimension out of NORMAL), so the number of procedure days matches (0).
- **Mechanism:** PS01 (sleepiness, KSS, integer scale 1-9) goes from a baseline mean of 2.6 (temoin) / 3.0 (capteur) to 4 on two consecutive days. With a 5-day baseline, a one-point step gives d = 1.23 / 1.41, above the v3 threshold 1.0.
- **Link with the pilot:** same weakness as `research/pilot/RESULTS.md` point 1 (method A: 17 % false procedures; short baselines on integer scales).
- **Impact on the demo:** the control screen would show an amber Morale card on days 8-9 for an astronaut who is fine. It does not open a procedure.
- **Decision needed (M1):** decision n°1 (detector). Not fixed in code: EWMA is not coded without a MISE À JOUR.
- **Test status:** the 3 cases are marked `xfail(strict=True)` in `tests/test_scenarios.py`; they fail loudly (XPASS) if the rule changes.

### DEV-01 — CLOSED 14/11/2026 (06:35)
M1 chose the scientifically best-calibrated detector setting: `Params()` now uses threshold 1.5 + absolute SD floors. With it, the three xfail cases (temoin days 8–9, capteur day 9) match the expected files, which were not edited. The story amplitude is now `drift_amp=2.5` (was 2.0) so that day 7 Attention is DEGRADED again. The xfail markers were removed (they went XPASS).

## DEV-02 — Input parameter of `data/scenarios/histoire.json` changed, expected outputs untouched (14/11/2026)
`generate_kwargs.drift_amp` 2.0 → 2.5, following M1's calibration decision (see DEV-01). Only the scenario *input* changed; every expected state/decision is as written before the first run. Consequence to know: with the calibrated rule, the old amplitude 2.0 gives Attention WATCH on day 7 (DEGRADED on day 9).
