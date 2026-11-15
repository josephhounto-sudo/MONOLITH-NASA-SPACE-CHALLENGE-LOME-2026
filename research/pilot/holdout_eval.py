"""Held-out check of the shipped rule (d >= 1.5, 2 consecutive days, SD floor).
The 1.5 threshold was chosen on seeds 1000-1299 / 5000-5149 / 7000-7149 (pilot 3). Here the SAME rule, with NO retuning,
is run on seeds never used for tuning: controls 30000-30299, gradual 35000-35149, abrupt 37000-37149.
ALL DATA ARE SYNTHETIC. Run from the repo root: python research/pilot/holdout_eval.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from pilot import ABS_FLOOR, zscores, run_flags, states_from_flags, procedure_days
from pilot2 import control, gradual, shifted
from pilot3 import wilson

THR = 1.5
SETS = {"control (false procedure)": (300, 30000, control),
        "gradual 1.5 SD": (150, 35000, gradual),
        "abrupt 2 SD": (150, 37000, lambda s: shifted(s, 2.0, 8, ["Attention", "Morale"]))}
out = {}
for name, (n, start, mk) in SETS.items():
    k = 0
    for s in range(start, start + n):
        dv = mk(s)
        if procedure_days(states_from_flags(run_flags(zscores(dv, ABS_FLOOR), THR), dv)):
            k += 1
    lo, hi = wilson(k, n)
    out[name] = {"n": n, "hits": k, "pct": round(100 * k / n, 1), "ci95": f"{lo:.1f}-{hi:.1f}"}
    print(f"{name}: {k}/{n} = {100*k/n:.1f} % (95 % CI {lo:.1f}-{hi:.1f})")
json.dump(out, open(os.path.join(HERE, "holdout_results.json"), "w"), indent=1)
