"""Baseline sanity check: can published fixed thresholds tell us the personal reference may be wrong?

SYNTHETIC only; sensitivity analysis. Question from Joseph (18/11): if the days used as 'normal' are already off, the
personal rule measures against a false reference. This tests a cheap second look that does not depend on the personal
baseline: on baseline days 1-5, flag 'reference to confirm' when mean sleep < 7 h (AASM and SRS consensus, Watson et al.
2015) or mean PVT-B lapses >= 11 (Basner and Rubinstein, severe-impairment cut). It is a note, never an alert.

Shifted references reuse research/biased_baseline.py (days 1-5 moved 0.5, 1.0, 1.5 personal SD in the unfavourable
direction). Persons come from research/fixed_vs_personal.py (spread f between people, not sourced). Seeds 65000-65149.
Healthy rows measure the cost: how often a clean reference is flagged only because the person naturally sleeps little.

Run: python research/baseline_check.py
"""
from __future__ import annotations
import json, os, sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "research"))
sys.path.insert(0, os.path.join(ROOT, "research", "pilot"))
from csync.rules import daily_values
from biased_baseline import shift_baseline
from fixed_vs_personal import LAPSES_MAX, SEEDS, SLEEP_MIN_H, person
from pilot3 import wilson
from synthetic.generator import generate

BIASES = (0.0, 0.5, 1.0, 1.5)
SPREADS = (0, 1, 2, 3)


def reference_to_confirm(dv: pd.DataFrame, baseline_days: int = 5) -> bool:
    b = dv.loc[1:baseline_days]
    return bool(b["PH09"].mean() < SLEEP_MIN_H or b["CO02"].mean() >= LAPSES_MAX)


def run():
    out = {}
    for f in SPREADS:
        row = {}
        for bias in BIASES:
            hit = 0
            for s in SEEDS:
                dv = daily_values(generate("histoire", seed=s, person=person(s, f), drift=True, event=False, drift_amp=1.5, fast=True))
                if bias:
                    dv = shift_baseline(dv, bias)
                hit += reference_to_confirm(dv)
            lo, hi = wilson(hit, len(SEEDS))
            row[f"bias={bias}"] = {"flagged": hit, "n": len(SEEDS), "pct": round(100 * hit / len(SEEDS), 1), "wilson95": [round(float(lo), 1), round(float(hi), 1)]}
        out[f"f={f}"] = row
    return out


if __name__ == "__main__":
    o = run()
    json.dump(o, open(os.path.join(ROOT, "research", "baseline_check_results.json"), "w"), indent=1)
    for f, row in o.items():
        print(f, {k: f"{v['pct']}% {v['wilson95']}" for k, v in row.items()})
