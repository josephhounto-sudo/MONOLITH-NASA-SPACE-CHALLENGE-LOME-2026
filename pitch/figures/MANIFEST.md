<!-- 2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ -->
# Screenshots of the C-Sync interface (demo story, SYNTHETIC data)

| File | Screen | sha256 (12) |
|---|---|---|
| demo_day7_nominal.png | Day 7: Body WATCH, Attention DEGRADED, procedure PROC-FATIGUE-01 proposed | 3365695b35f1 |
| demo_day9_emergency_step3.png | Day 9: guided emergency, step 3 of 6 (4 guided measurements), link restored, "Delivered to ground (once)" | 1e1eb3534d4e |
| demo_day10_resume_refused.png | Day 10: Request resume then Commander override, REFUSE_RESUME, plain-language reasons | 9d5ed71abc8c |

- **Taken:** 2026-11-14 ~06:45 UTC (Lomé), by the AI code assistant, with headless Chrome on the running app (real renders, not mock-ups).
- **Code base:** zip SAUVEGARDE_COMPLETE_C-Sync_14-11_rev4 (reference commit dc61786; the zip has no .git, so the commit id was not checked) + the changes T2, T3, T5 of this delivery.
- **Commands:** `python scripts/run_story.py` then `streamlit run csync/ui/app.py` (viewport 1400 px wide, scale 1.5, bottom whitespace trimmed).
- **Story settings:** variant histoire, seed 42, drift_amp 2.5, fast=True, rule v3 `Params()` (threshold 1.5 + absolute SD floors). EWMA is not used by the engine.
- **Clicks:** day 7 = slider only; day 9 = Next twice (step 3), then "19:20 — Link restored"; day 10 = Request resume, then Commander override.
- Older screenshots (threshold 1.0, drift_amp 2.0) are obsolete: do not use them.
