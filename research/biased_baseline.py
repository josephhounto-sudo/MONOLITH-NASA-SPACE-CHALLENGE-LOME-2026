"""Bias when the personal baseline (days 1-5) is already shifted.

Question: if the reference window is tired, how many story drifts does the
shipped rule miss, compared with a clean reference?

SYNTHETIC only. Seeds 65000-65149 (150 crews), variant histoire,
drift_amp=1.5, no event, fast=True. The shipped rule is called as-is
(csync.rules.evaluate, Params()).

Shift: on days 1-5, each drift indicator moves by bias * personal SD
(ddof=1 of those five days) in the unfavourable direction. Days 6-10 stay
as generated. Bias levels: 0.5, 1.0, 1.5.

A detection is any OPEN_PROCEDURE. A missed drift is a crew detected on the
clean series and not detected after the shift.

Track tested and not adopted: a pre-mission reference. Five clean days are
placed before the tired window, and the rule (still baseline_days=5) reads
only those clean days. This is not wired into csync/rules.py.

Run: python research/biased_baseline.py
"""
from __future__ import annotations

import json
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "research", "pilot"))

from csync.rules import DIRECTION, DRIFT_INDICATORS, Params, daily_values, evaluate
from pilot3 import wilson
from synthetic.generator import generate

SEEDS = range(65000, 65150)
BIASES = (0.5, 1.0, 1.5)
INDS = [i for ids in DRIFT_INDICATORS.values() for i in ids]


def clean_frame(seed: int) -> pd.DataFrame:
    df = generate("histoire", seed=seed, drift=True, event=False, drift_amp=1.5, fast=True)
    return daily_values(df)


def personal_sd(dv: pd.DataFrame) -> pd.Series:
    return dv.loc[1:5, INDS].std(ddof=1)


def shift_baseline(dv: pd.DataFrame, bias: float, sd: pd.Series | None = None) -> pd.DataFrame:
    """Move days 1-5 in the unfavourable direction by `bias` personal SD."""
    out = dv.copy()
    sd = personal_sd(dv) if sd is None else sd
    for ind in INDS:
        step = sd[ind]
        if pd.notna(step) and step > 0:
            out.loc[out.index <= 5, ind] = out.loc[out.index <= 5, ind] + DIRECTION[ind] * bias * float(step)
    return out


def detected(dv: pd.DataFrame, prm: Params | None = None) -> bool:
    _, _, _, decisions, _ = evaluate(dv, prm or Params())
    return bool((decisions.action == "OPEN_PROCEDURE").any())


def pre_mission_frame(clean: pd.DataFrame, tired: pd.DataFrame) -> pd.DataFrame:
    """Days 1-5 clean, days 6-10 = tired days 1-5, days 11-15 = clean days 6-10.

    Tested only. Not adopted: evaluate() is still the shipped function,
    with baseline_days left at 5, so the reference is the prepended clean window.
    """
    head = clean.loc[1:5, INDS].copy()
    mid = tired.loc[1:5, INDS].copy()
    tail = clean.loc[6:10, INDS].copy()
    head.index = [1, 2, 3, 4, 5]
    mid.index = [6, 7, 8, 9, 10]
    tail.index = [11, 12, 13, 14, 15]
    return pd.concat([head, mid, tail])


def _rate(k: int, n: int) -> dict:
    lo, hi = wilson(k, n) if n else (float("nan"), float("nan"))
    return {"k": k, "n": n, "pct": round(100.0 * k / n, 1) if n else None,
            "ci_lo": round(float(lo), 1) if n else None, "ci_hi": round(float(hi), 1) if n else None}


def run() -> dict:
    cleans = [(s, clean_frame(s)) for s in SEEDS]
    clean_hits = {s: detected(dv) for s, dv in cleans}
    n = len(cleans)
    k_clean = sum(clean_hits.values())
    out = {
        "seeds": f"{SEEDS.start}-{SEEDS.stop - 1}",
        "n": n,
        "data": "SYNTHETIC",
        "clean": _rate(k_clean, n),
        "bias": {},
        "pre_mission_not_adopted": {},
    }
    for bias in BIASES:
        tired_hits = {}
        pre_drift = 0
        pre_early = 0
        for s, dv in cleans:
            sd = personal_sd(dv)
            tired = shift_baseline(dv, bias, sd)
            tired_hits[s] = detected(tired)
            pre = pre_mission_frame(dv, tired)
            _, _, _, decisions, _ = evaluate(pre, Params())
            opened = set(decisions.loc[decisions.action == "OPEN_PROCEDURE", "day"].tolist())
            if any(d <= 10 for d in opened):
                pre_early += 1
            if any(d >= 11 for d in opened):
                pre_drift += 1
        missed = sum(clean_hits[s] and not tired_hits[s] for s in clean_hits)
        out["bias"][f"{bias:.1f}"] = {
            "detected": _rate(sum(tired_hits.values()), n),
            "missed_among_clean_detections": _rate(missed, k_clean),
        }
        out["pre_mission_not_adopted"][f"{bias:.1f}"] = {
            "procedure_during_tired_window_days_6_to_10": _rate(pre_early, n),
            "procedure_during_injected_drift_days_11_to_15": _rate(pre_drift, n),
            "adopted": False,
        }
    return out


def main() -> None:
    result = run()
    path = os.path.join(ROOT, "research", "biased_baseline_results.json")
    with open(path, "w", encoding="utf8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
