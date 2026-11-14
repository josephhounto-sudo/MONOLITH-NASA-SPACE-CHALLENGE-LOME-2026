"""Analysis pilot — which detector should C-Sync use with only 5 baseline days?

Experiments (same simulated astronauts for every method, fixed seeds):
  E1 control: no drift at all            -> false procedures (lower is better)
  E2 drift of 1.0 / 1.5 / 2.0 personal SD -> detection rate and day of first procedure
  E3 robustness: 10 % of daily values missing at random
Methods (per-indicator detectors, same aggregation: 1 flagged indicator = WATCH, 2+ = DEGRADED,
2 dimensions out of NORMAL = procedure):
  A  rule v3          d >= 1.0 two days in a row, SD floor 5 %
  B  rule proposed    d >= 1.5 two days in a row, absolute SD floor per indicator
  C  EWMA             lambda 0.3, limit 2.5 sigma of the EWMA
  D  CUSUM            one-sided, k = 0.5, h = 3.0
  E  combined score   per dimension: sum of squared unfavourable z > chi-square 99 % (diagonal: a full
                      covariance cannot be estimated from 5 days and 8 indicators)
Run: python research/pilot/pilot.py   (about 2 minutes)
All data are SYNTHETIC (generator csync-synth-0.1). Results describe the rules on our noise model, not real astronauts.
"""
import os, sys, time, json
import numpy as np, pandas as pd
from scipy.stats import chi2
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from synthetic.generator import generate
from csync.rules import daily_values, DIRECTION, DRIFT_INDICATORS

OUT = os.path.dirname(os.path.abspath(__file__))
BASE = 5
ABS_FLOOR = {"PS01": 1.0, "PS02": 1.0, "PS03": 0.5, "PS04": 1.0, "CO02": 1.0, "PH09": 0.5, "PH01": 3.0}
INDS = [i for v in DRIFT_INDICATORS.values() for i in v]

def zscores(dv, abs_floor=None):
    base = dv.loc[1:BASE, INDS]
    mu, sd = base.mean(), base.std(ddof=1).fillna(0)
    floor = mu.abs() * 0.05
    for k, v in (abs_floor or {}).items():
        floor[k] = max(floor[k], v)
    sd = np.maximum(sd, floor)
    return pd.DataFrame({i: DIRECTION[i] * (dv[i] - mu[i]) / sd[i] for i in INDS}, index=dv.index)

def run_flags(z, thr):
    f = pd.DataFrame(False, index=z.index, columns=z.columns)
    for i in z.columns:
        run = 0
        for d in z.index:
            if pd.isna(z.at[d, i]): run = 0; continue
            run = run + 1 if z.at[d, i] >= thr else 0
            f.at[d, i] = d > BASE and run >= 2
    return f

def ewma_flags(z, lam=0.3, L=2.5):
    f = pd.DataFrame(False, index=z.index, columns=z.columns)
    for i in z.columns:
        e, n = 0.0, 0
        for d in z.index:
            if d <= BASE or pd.isna(z.at[d, i]): continue
            n += 1
            e = lam * z.at[d, i] + (1 - lam) * e
            sigma = np.sqrt(lam / (2 - lam) * (1 - (1 - lam) ** (2 * n)))
            f.at[d, i] = e > L * sigma
    return f

def cusum_flags(z, k=0.5, h=3.0):
    f = pd.DataFrame(False, index=z.index, columns=z.columns)
    for i in z.columns:
        s = 0.0
        for d in z.index:
            if d <= BASE or pd.isna(z.at[d, i]): continue
            s = max(0.0, s + z.at[d, i] - k)
            f.at[d, i] = s > h
    return f

def combined_dim_states(z, p=0.99):
    st = {}
    for d in z.index:
        row = {}
        for dim, lst in DRIFT_INDICATORS.items():
            if d <= BASE: row[dim] = "UNKNOWN"; continue
            v = z.loc[d, lst]
            if v.isna().any(): row[dim] = "UNKNOWN"; continue
            stat = float((np.clip(v, 0, None) ** 2).sum())
            row[dim] = "WATCH" if stat > chi2.ppf(p, len(lst)) else "NORMAL"
        st[d] = row
    return pd.DataFrame(st).T

def states_from_flags(f, dv):
    st = {}
    for d in f.index:
        row = {}
        for dim, lst in DRIFT_INDICATORS.items():
            if d <= BASE: row[dim] = "UNKNOWN"; continue
            n = int(f.loc[d, lst].sum())
            missing = dv.loc[d, lst].isna().any()
            row[dim] = "DEGRADED" if n >= 2 else "UNKNOWN" if missing else "WATCH" if n == 1 else "NORMAL"
        st[d] = row
    return pd.DataFrame(st).T

def procedure_days(st):
    out = (st.isin(["WATCH", "DEGRADED"])).sum(axis=1)
    return [d for d in st.index if d > BASE and out[d] >= 2]

METHODS = {
    "A rule v3 (d>=1)": lambda dv: states_from_flags(run_flags(zscores(dv), 1.0), dv),
    "B rule proposed (d>=1.5 + floor)": lambda dv: states_from_flags(run_flags(zscores(dv, ABS_FLOOR), 1.5), dv),
    "C EWMA": lambda dv: states_from_flags(ewma_flags(zscores(dv, ABS_FLOOR)), dv),
    "D CUSUM": lambda dv: states_from_flags(cusum_flags(zscores(dv, ABS_FLOOR)), dv),
    "E combined score (diagonal)": lambda dv: combined_dim_states(zscores(dv, ABS_FLOOR)),
}

def simulate(n, drift_amp, start, missing=0.0):
    rows = []
    for s in range(start, start + n):
        df = generate("histoire" if drift_amp else "temoin", seed=s, drift=bool(drift_amp), event=False,
                      drift_amp=drift_amp or 0, fast=True)
        dv = daily_values(df)
        if missing:
            rng = np.random.default_rng(s + 99)
            mask = rng.random(dv[INDS].shape) < missing
            dv[INDS] = dv[INDS].mask(mask)
        for name, fn in METHODS.items():
            t0 = time.perf_counter()
            st = fn(dv)
            ms = (time.perf_counter() - t0) * 1000
            pdays = procedure_days(st)
            rows.append({"seed": s, "method": name, "drift": drift_amp or 0.0, "missing": missing,
                         "procedure": bool(pdays), "first_day": min(pdays) if pdays else None,
                         "unknown_dim_days": int((st.loc[BASE + 1:] == "UNKNOWN").sum().sum()), "ms": ms})
    return rows

if __name__ == "__main__":
    rows = []
    rows += simulate(300, 0.0, 1000)
    for amp in (1.0, 1.5, 2.0):
        rows += simulate(150, amp, 5000)
    rows += simulate(300, 0.0, 1000, missing=0.10)
    rows += simulate(150, 1.5, 5000, missing=0.10)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "pilot_runs.csv"), index=False)
    summ = (df.groupby(["method", "missing", "drift"])
              .agg(runs=("seed", "size"), pct_procedure=("procedure", lambda x: round(100 * x.mean(), 1)),
                   median_first_day=("first_day", "median"), unknown_dim_days=("unknown_dim_days", "mean"), ms=("ms", "median"))
              .reset_index())
    summ.to_csv(os.path.join(OUT, "pilot_summary.csv"), index=False)
    print(summ.to_string())
