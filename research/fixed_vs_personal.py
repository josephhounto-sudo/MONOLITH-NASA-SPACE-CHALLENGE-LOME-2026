"""Hypothesis H2: does the personal-baseline rule beat a fixed population-threshold rule?

SYNTHETIC only, and this is a SENSITIVITY ANALYSIS, not a proof. The answer depends on how much baselines differ
between people (spread factor f), and the generator ships with f = 0 (one Person for every crew). No source for a real f
is in this repository; the sweep shows how the result moves with it.

Fixed rule (thresholds from published texts, never tuned here):
  - sleep < 7 h        AASM and SRS consensus statement, Watson et al. 2015 (adults should sleep 7 h or more)
  - PVT-B lapses >= 11 Basner and Rubinstein 2011 (3-min PVT, 355 ms threshold; 11 and 20 lapses split simulated
                       luggage-screening performance; the context is airport screening, not spaceflight)
  Same persistence as the personal rule: flagged 2 days in a row; the procedure opens when both indicators are flagged
  (two dimensions out, as in csync.rules). Evaluated on days 6-10, the days the personal rule is allowed to fire.
Personal rules: (A) csync.rules.evaluate as shipped on all indicators; (B) the same function restricted to the same two
indicators (PH09, CO02) so the comparison is like for like. Fixed rules: (C) sleep and lapses together, (D) sleep alone.

Persons: sleep_h = 7.2 + f * 0.45 * z1, rt_ms = 265 + f * 10 * z2 (z standard normal, separate stream), f in 0, 1, 2, 3.
Seeds 65000-65149 (never used to tune the rule). Healthy crews = same seeds and persons with drift=False.
Limit that favours the fixed rule: the generator forces sleep to at most 5.9 h during the drift whatever the person's
baseline (absolute, not relative).

Run: python research/fixed_vs_personal.py
"""
from __future__ import annotations
import json, os, sys
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "research", "pilot"))
from csync.rules import Params, daily_values, evaluate
from pilot3 import wilson
from synthetic.generator import Person, generate

SEEDS = range(65000, 65150)
SPREADS = (0, 1, 2, 3)
SLEEP_MIN_H, LAPSES_MAX = 7.0, 11


def person(seed: int, f: float) -> Person:
    z = np.random.default_rng(seed + 1_000_003).normal(size=2)
    return Person(sleep_h=float(np.clip(7.2 + f * 0.45 * z[0], 5.0, 9.5)), rt_ms=float(np.clip(265 + f * 10 * z[1], 220, 330)))


def first_open(decisions: pd.DataFrame):
    d = decisions[decisions.action == "OPEN_PROCEDURE"]
    return int(d.day.min()) if len(d) else None


def personal(dv: pd.DataFrame, cols=None):
    x = dv if cols is None else dv[cols]
    return first_open(evaluate(x, Params())[3])


def fixed(dv: pd.DataFrame):
    body = (dv["PH09"] < SLEEP_MIN_H)
    attn = (dv["CO02"] >= LAPSES_MAX)
    for day in range(6, 11):
        if all(bool(s.get(d, False)) for s in (body, attn) for d in (day - 1, day)):
            return day
    return None


def fixed_sleep_only(dv: pd.DataFrame):
    """Single indicator, same persistence: sleep < 7 h on two consecutive days (days 6-10)."""
    low = dv["PH09"] < SLEEP_MIN_H
    for day in range(6, 11):
        if bool(low.get(day - 1, False)) and bool(low.get(day, False)):
            return day
    return None


def run():
    out = {}
    for f in SPREADS:
        RULES = ("A_personal_all", "B_personal_2ind", "C_fixed", "D_fixed_sleep_only")
        res = {}
        for kind, drift in (("drift", True), ("healthy", False)):
            r = {k: [] for k in RULES}
            for s in SEEDS:
                dv = daily_values(generate("histoire", seed=s, person=person(s, f), drift=drift, event=False, drift_amp=1.5, fast=True))
                r["A_personal_all"].append(personal(dv))
                r["B_personal_2ind"].append(personal(dv, ["PH09", "CO02"]))
                r["C_fixed"].append(fixed(dv))
                r["D_fixed_sleep_only"].append(fixed_sleep_only(dv))
            res[kind] = {}
            for k, v in r.items():
                hit = [x for x in v if x is not None]
                lo, hi = wilson(len(hit), len(v))
                res[kind][k] = {"n_open": len(hit), "n": len(v), "pct": round(100 * len(hit) / len(v), 1),
                                "wilson95": [round(float(lo), 1), round(float(hi), 1)], "median_first_day": float(np.median(hit)) if hit else None}
        out[f"f={f}"] = {"drift": res["drift"], "healthy": res["healthy"]}
    return out


if __name__ == "__main__":
    o = run()
    json.dump(o, open(os.path.join(ROOT, "research", "fixed_vs_personal_results.json"), "w"), indent=1)
    for f, v in o.items():
        print(f)
        for kind in ("drift", "healthy"):
            for k, m in v[kind].items():
                print(f"  {kind:8s} {k:16s} {m['n_open']:3d}/{m['n']} {m['pct']:5.1f}% {m['wilson95']} first-day median {m['median_first_day']}")
