"""Pilot 2 - broader comparison, answering "can we do better than EWMA without losing reliability?"
New vs pilot.py: two scenarios (abrupt change, favourable-only change) and three new detectors:
  F  EWMA + shrunk SD   (partial pooling idea: the personal SD from 5 days is pulled toward a crew-population SD)
  G  Kalman local level (state-space idea: smoothed level of the unfavourable z, flag when level > 2.5 sd of the filter)
  I  hybrid: EWMA OR proposed rule B per indicator (trend + sudden change)
  H  Mahalanobis        (multivariate, per dimension, covariance shrunk toward the population correlation, two-sided)
Not tested (and why): PCA, Isolation Forest, HMM, hierarchical Bayes full model need many observations per person or a
fitted population model; with 5 baseline days per astronaut they cannot be fitted honestly. See docs/METHODES_NASA_DOSSIER.md.
ALL DATA ARE SYNTHETIC (generator csync-synth-0.1). Run: python research/pilot/pilot2.py (about 3-5 min).
"""
import os, sys, time
import numpy as np, pandas as pd
from scipy.stats import chi2
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synthetic.generator import generate
from csync.rules import daily_values, DIRECTION, DRIFT_INDICATORS
import pilot as P
from pilot import BASE, INDS, ABS_FLOOR, zscores, ewma_flags, run_flags, states_from_flags, procedure_days, METHODS

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- population reference, from separate seeds (no leakage into the test runs) ----
def population_reference(n=200, start=20000):
    sds, devs = [], []
    for s in range(start, start + n):
        dv = daily_values(generate("temoin", seed=s, drift=False, event=False, drift_amp=0, fast=True))
        b = dv.loc[1:BASE, INDS]
        sds.append(b.std(ddof=1)); devs.append((b - b.mean()))
    s0 = pd.concat(sds, axis=1).median(axis=1)
    corr = pd.concat(devs).corr().fillna(0)
    return s0, corr
S0, CORR = population_reference()

def zs_shrunk(dv, nu0=4):
    base = dv.loc[1:BASE, INDS]
    mu, s = base.mean(), base.std(ddof=1).fillna(0)
    sd = np.sqrt((nu0 * S0 ** 2 + (BASE - 1) * s ** 2) / (nu0 + BASE - 1))
    floor = mu.abs() * 0.05
    for k, v in ABS_FLOOR.items(): floor[k] = max(floor[k], v)
    sd = np.maximum(sd, floor)
    return pd.DataFrame({i: DIRECTION[i] * (dv[i] - mu[i]) / sd[i] for i in INDS}, index=dv.index)

def kalman_flags(z, q=0.05, r=1.0, L=2.5):
    f = pd.DataFrame(False, index=z.index, columns=z.columns)
    for i in z.columns:
        x, p, n = 0.0, 1.0, 0
        for d in z.index:
            if d <= BASE: continue
            p = p + q                                   # predict
            if not pd.isna(z.at[d, i]):
                k = p / (p + r); x = x + k * (z.at[d, i] - x); p = (1 - k) * p   # update
            n += 1
            f.at[d, i] = x > L * np.sqrt(p) if n > 1 else False
    return f

def mahalanobis_states(dv, alpha=0.5, p=0.99):
    z = zscores(dv, ABS_FLOOR)                           # signed, per-person standardised
    st = {}
    for d in z.index:
        row = {}
        for dim, lst in DRIFT_INDICATORS.items():
            if d <= BASE: row[dim] = "UNKNOWN"; continue
            ok = True; flags = []
            for dd in (d - 1, d):                        # two consecutive days, like rule v3
                v = z.loc[dd, lst].astype(float)
                if dd <= BASE or v.isna().any(): ok = False; break
                c = CORR.loc[lst, lst].values
                sig = (1 - alpha) * np.eye(len(lst)) + alpha * c
                flags.append(float(v.values @ np.linalg.solve(sig, v.values)) > chi2.ppf(p, len(lst)))
            row[dim] = "UNKNOWN" if not ok and d > BASE and z.loc[d, lst].isna().any() else ("WATCH" if ok and all(flags) else "NORMAL")
        st[d] = row
    return pd.DataFrame(st).T

NEW = {
    "F EWMA + shrunk SD": lambda dv: states_from_flags(ewma_flags(zs_shrunk(dv)), dv),
    "G Kalman local level": lambda dv: states_from_flags(kalman_flags(zscores(dv, ABS_FLOOR)), dv),
    "H Mahalanobis (shrunk cov.)": lambda dv: mahalanobis_states(dv),
}
def hybrid_states(dv):
    """I: an indicator is flagged if EWMA (trend) OR proposed rule B (d>=1.5 two days, sudden change) flags it."""
    z = zscores(dv, ABS_FLOOR)
    f = ewma_flags(z) | run_flags(z, 1.5)
    return states_from_flags(f, dv)
NEW["I hybrid EWMA OR rule B"] = hybrid_states
ALL = {k: METHODS[k] for k in ("A rule v3 (d>=1)", "B rule proposed (d>=1.5 + floor)", "C EWMA")}
ALL.update(NEW)

# ---- scenarios, all built on the same control crews ----
STEP_DAY = 8
def control(s): return daily_values(generate("temoin", seed=s, drift=False, event=False, drift_amp=0, fast=True))
def gradual(s): return daily_values(generate("histoire", seed=s, drift=True, event=False, drift_amp=1.5, fast=True))
def shifted(s, amp, day, dims, sign=+1):
    dv = control(s)
    for dim in dims:
        for i in DRIFT_INDICATORS[dim]:
            dv.loc[day:, i] = dv.loc[day:, i] + sign * DIRECTION[i] * amp * S0[i]
    return dv
SCEN = {
    "control (no change)": (300, 1000, control, False),
    "gradual drift 1.5 SD": (150, 5000, gradual, True),
    "abrupt change 2 SD, day 8, 2 dimensions": (150, 7000, lambda s: shifted(s, 2.0, STEP_DAY, ["Attention", "Morale"]), True),
    "favourable change 2 SD, 2 dimensions": (150, 9000, lambda s: shifted(s, 2.0, STEP_DAY, ["Attention", "Morale"], -1), False),
}

def run():
    rows = []
    for name, (n, start, mk, expect) in SCEN.items():
        for miss in ((0.0, 0.10) if name.startswith(("control", "gradual")) else (0.0,)):
            for s in range(start, start + n):
                dv = mk(s)
                if miss:
                    rng = np.random.default_rng(s + 99)
                    dv[INDS] = dv[INDS].mask(rng.random(dv[INDS].shape) < miss)
                for m, fn in ALL.items():
                    t0 = time.perf_counter(); st = fn(dv); ms = (time.perf_counter() - t0) * 1000
                    pd_ = procedure_days(st)
                    rows.append({"scenario": name, "missing": miss, "seed": s, "method": m, "procedure": bool(pd_),
                                 "first_day": min(pd_) if pd_ else None, "expected": expect, "ms": ms})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "pilot2_runs.csv"), index=False)
    summ = (df.groupby(["scenario", "missing", "method"])
              .agg(runs=("seed", "size"), pct_procedure=("procedure", lambda x: round(100 * x.mean(), 1)),
                   median_first_day=("first_day", "median"), ms=("ms", "median")).reset_index())
    summ.to_csv(os.path.join(OUT, "pilot2_summary.csv"), index=False)
    print(summ.to_string())

if __name__ == "__main__":
    run()
