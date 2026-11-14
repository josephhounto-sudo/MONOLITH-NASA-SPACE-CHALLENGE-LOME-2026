"""Pilot 3 - methodological audit of pilot 2 (answers the review of 14/11).
Fixes the weaknesses of pilot 2:
  1. Fair calibration: every family is swept over its threshold, so methods are compared at comparable false-alarm levels,
     not at one arbitrary threshold each.
  2. Separate metrics: (a) % of crews with >=1 false procedure, (b) false procedure-days per astronaut-day,
     (c) detection rate, (d) detection delay in days after onset. They are NOT interchangeable.
  3. Uncertainty: Wilson 95 % intervals; paired exact McNemar test for the pairs we care about.
  4. Independence: seed ranges are disjoint between scenarios; controls 1000-1299, gradual 5000-5149, abrupt 7000-7149
     (built on control crews with those seeds), population reference 20000-20199. Within a scenario, every method sees
     the SAME crews (paired design).
ALL DATA ARE SYNTHETIC. Run: python research/pilot/pilot3.py  (about 4-6 min). Output: pilot3_sweep.csv, pilot3_paired.csv
"""
import os, sys, time
import numpy as np, pandas as pd
from scipy.stats import binomtest
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pilot2 as P2
from pilot import BASE, INDS, ABS_FLOOR, zscores, run_flags, ewma_flags, cusum_flags, states_from_flags, procedure_days
from pilot2 import zs_shrunk, kalman_flags, control, gradual, shifted

EVAL_DAYS = 10 - BASE   # days 6..10 are at risk
SCEN = {"control": (300, 1000, control, None),
        "gradual 1.5 SD (onset day 6)": (150, 5000, gradual, 6),
        "abrupt 2 SD (onset day 8)": (150, 7000, lambda s: shifted(s, 2.0, 8, ["Attention", "Morale"]), 8)}

FAMILIES = {   # name -> (thresholds, function(z, zsh, thr) -> flags)
    "Rule (d>=thr, 2 days, SD floor)": ([1.0, 1.25, 1.5, 1.75, 2.0, 2.5], lambda z, zsh, t: run_flags(z, t)),
    "EWMA (lambda 0.3, L=thr)": ([1.5, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5], lambda z, zsh, t: ewma_flags(z, 0.3, t)),
    "EWMA + shrunk SD (L=thr)": ([1.5, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5], lambda z, zsh, t: ewma_flags(zsh, 0.3, t)),
    "CUSUM (k 0.5, h=thr)": ([1.5, 2.0, 3.0, 4.0, 5.0], lambda z, zsh, t: cusum_flags(z, 0.5, t)),
    "Kalman level (q 0.05, L=thr)": ([0.5, 0.75, 1.0, 1.5, 2.0, 2.5], lambda z, zsh, t: kalman_flags(z, 0.05, 1.0, t)),
}

def wilson(k, n, zc=1.96):
    p = k / n; c = (p + zc * zc / (2 * n)) / (1 + zc * zc / n)
    h = zc * np.sqrt(p * (1 - p) / n + zc * zc / (4 * n * n)) / (1 + zc * zc / n)
    return 100 * (c - h), 100 * (c + h)

def main():
    data = {}
    for name, (n, start, mk, onset) in SCEN.items():
        data[name] = []
        for s in range(start, start + n):
            dv = mk(s); data[name].append((s, dv, zscores(dv, ABS_FLOOR), zs_shrunk(dv)))
    rows, hits = [], {}
    for fam, (ths, fn) in FAMILIES.items():
        for t in ths:
            rec = {"family": fam, "thr": t}
            for name, (n, start, mk, onset) in SCEN.items():
                pds = []
                for s, dv, z, zsh in data[name]:
                    pds.append(procedure_days(states_from_flags(fn(z, zsh, t), dv)))
                hit = [bool(p) for p in pds]; hits[(fam, t, name)] = hit
                k = sum(hit); lo, hi = wilson(k, n)
                rec[name + " | pct"] = round(100 * k / n, 1); rec[name + " | ci95"] = f"{lo:.1f}-{hi:.1f}"
                if onset is None:
                    rec["false procedure-days per astronaut-day (%)"] = round(100 * sum(len(p) for p in pds) / (n * EVAL_DAYS), 2)
                else:
                    delays = [min(p) - onset for p in pds if p]
                    rec[name + " | median delay (d)"] = float(np.median(delays)) if delays else None
                    rec[name + " | missed"] = n - k
            rows.append(rec)
    sw = pd.DataFrame(rows); sw.to_csv(os.path.join(HERE, "pilot3_sweep.csv"), index=False)
    pd.set_option("display.width", 250, "display.max_columns", 30); print(sw.to_string())
    # paired exact McNemar (discordant pairs) on abrupt and gradual, EWMA L=2.5 vs others
    ref = ("EWMA (lambda 0.3, L=thr)", 2.5); pairs = []
    for other in [("EWMA + shrunk SD (L=thr)", 2.5), ("Rule (d>=thr, 2 days, SD floor)", 1.5), ("CUSUM (k 0.5, h=thr)", 3.0), ("Kalman level (q 0.05, L=thr)", 1.0)]:
        for name in ("gradual 1.5 SD (onset day 6)", "abrupt 2 SD (onset day 8)", "control"):
            a, b = hits[ref + (name,)], hits[other + (name,)]
            n01 = sum((not x) and y for x, y in zip(a, b)); n10 = sum(x and (not y) for x, y in zip(a, b))
            p = binomtest(n01, n01 + n10, 0.5).pvalue if n01 + n10 else 1.0
            pairs.append({"reference": "EWMA L=2.5", "other": f"{other[0]} {other[1]}", "scenario": name, "only_other": n01, "only_ewma": n10, "mcnemar_p": round(p, 4)})
    pd.DataFrame(pairs).to_csv(os.path.join(HERE, "pilot3_paired.csv"), index=False); print(pd.DataFrame(pairs).to_string())
    # Kalman vs EWMA response to a step of 2 SD: why Kalman is slow
    from math import sqrt
    q, r = 0.05, 1.0; x = 0.0; p = 1.0; e = 0.0; lam = 0.3; out = []
    for day in range(1, 6):
        p += q; k = p / (p + r); x += k * (2.0 - x); p *= (1 - k)
        e = lam * 2.0 + (1 - lam) * e
        sig = sqrt(lam / (2 - lam) * (1 - (1 - lam) ** (2 * day)))
        out.append((day, round(x, 2), round(2.5 * sqrt(p), 2), round(e, 2), round(2.5 * sig, 2)))
    print("step response (day after step, Kalman level, Kalman limit L=2.5, EWMA, EWMA limit):", out)
if __name__ == "__main__":
    main()
