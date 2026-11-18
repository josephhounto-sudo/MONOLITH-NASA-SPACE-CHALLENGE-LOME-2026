"""Hybrid reference A+B: in-mission days 1-5 (A) cross-checked with a pre-mission Earth reference (B).

SYNTHETIC. Joseph's constraint (18/11): fit between A and B without reducing the margin of error, i.e. detection on a clean
reference must not drop and false alarms must not rise. Hybrid rule H(g): per indicator, if the pre-mission mean is more
favourable than the mission days 1-5 mean by more than g personal SD, the mission reference mean is moved to the
pre-mission mean (SD stays the mission one); else A is kept as is. g=inf is the shipped rule. The shipped evaluate() is
called unchanged on the adjusted frame.
Conditions: contamination b = days 1-5 pushed unfavourably by b SD (reference tired); adaptation o = the whole mission
sits o SD unfavourably from Earth for real (microgravity/confinement normal differs from Earth normal; o is NOT sourced).
Detection: crews with story drift. False alarm: crews without drift. Seeds 65000-65149. Run: python research/hybrid_baseline.py
"""
from __future__ import annotations
import json, os, sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "research")); sys.path.insert(0, os.path.join(ROOT, "research", "pilot"))
from csync.rules import DIRECTION, Params, daily_values, evaluate
from biased_baseline import INDS, SEEDS, detected, personal_sd, shift_baseline
from pilot3 import wilson
from synthetic.generator import generate

GATES = (None, 0.0, 0.5, 1.0)       # None = shipped rule A only
BIASES = (0.0, 0.5, 1.0, 1.5)
ADAPT = (0.0, 0.5, 1.0)


def frame(seed, drift):
    return daily_values(generate("histoire", seed=seed, drift=drift, event=False, drift_amp=1.5, fast=True))


def shift_all(dv, o, sd):
    out = dv.copy()
    for i in INDS:
        if pd.notna(sd[i]):
            out[i] = out[i] + DIRECTION[i] * o * float(sd[i])
    return out


def hybrid(mis, pre, g):
    if g is None:
        return mis
    out = mis.copy()
    sd = personal_sd(mis)
    for i in INDS:
        d = DIRECTION[i] * (float(mis.loc[1:5, i].mean()) - float(pre.loc[1:5, i].mean()))  # >0: pre more favourable
        s = float(sd[i]) if pd.notna(sd[i]) else 0.0
        if s > 0 and d > g * s:
            out.loc[out.index <= 5, i] = out.loc[out.index <= 5, i] - (float(mis.loc[1:5, i].mean()) - float(pre.loc[1:5, i].mean()))
    return out


def rate(k, n):
    lo, hi = wilson(k, n)
    return {"pct": round(100 * k / n, 1), "ci": [round(float(lo), 1), round(float(hi), 1)]}


def run():
    res = {}
    for o in ADAPT:
        for b in BIASES:
            row = {}
            for g in GATES:
                hit = fa = 0
                for s in SEEDS:
                    pre = frame(s + 7_000_000, False)
                    for drift in (True, False):
                        mis = frame(s, drift)
                        sd = personal_sd(mis)
                        mis = shift_all(mis, o, sd) if o else mis
                        mis = shift_baseline(mis, b, sd) if b else mis
                        r = detected(hybrid(mis, pre, g))
                        if drift: hit += r
                        else: fa += r
                row["shipped" if g is None else f"H(g={g})"] = {"detect": rate(hit, len(SEEDS)), "false_alarm": rate(fa, len(SEEDS))}
            res[f"adapt={o},bias={b}"] = row
    return res


if __name__ == "__main__":
    r = run()
    json.dump(r, open(os.path.join(ROOT, "research", "hybrid_baseline_results.json"), "w"), indent=1)
    for k, row in r.items():
        print(k, {n: f"det {v['detect']['pct']} / fa {v['false_alarm']['pct']}" for n, v in row.items()})
