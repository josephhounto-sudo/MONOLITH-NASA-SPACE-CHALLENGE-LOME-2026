# Held-out check of the rule (15/11/2026)
Question: is the rule (d ≥ 1.5, 2 consecutive days, SD floor) only good on the scenarios it was tuned on?
Method: same rule, no retuning, on synthetic crews whose seeds were never used for tuning (`research/pilot/holdout_eval.py`, results in `research/pilot/holdout_results.json`).

| Scenario | Tuning seeds (pilot 3) | Held-out seeds | 95 % interval (held-out) |
|---|---|---|---|
| Healthy crews with a false procedure | 0.7 % (300 runs) | **0.0 %** (0/300) | 0.0–1.3 % |
| Gradual drift 1.5 SD detected | 95.3 % | **92.7 %** (139/150) | 87.3–95.9 % |
| Abrupt shift 2 SD detected | 59.3 % | **57.3 %** (86/150) | 49.3–65.0 % |

Reading: the held-out figures fall inside or next to the tuning figures, so the rule is not obviously over-fitted to its tuning seeds. The weak point does not move: an abrupt shift is detected about once in two (57.3 %), because the rule waits for two consecutive days.
Limits: synthetic crews built by our own generator, so a held-out result here says nothing about real astronauts; no clinical meaning.
