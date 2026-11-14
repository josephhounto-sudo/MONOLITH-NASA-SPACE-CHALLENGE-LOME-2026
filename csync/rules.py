"""Personal-baseline drift rules (deterministic, explainable).

Every number here is a DESIGN PARAMETER, never a clinical threshold.
Rule (PARAMETRES v3, P-06): d = (value - personal mean) / SD in the unfavourable direction;
an indicator is flagged when d >= threshold on N consecutive days; a dimension is WATCH with
1 flagged indicator, DEGRADED with 2 or more, UNKNOWN when today's data are missing or the
personal baseline is still being built. Two dimensions in WATCH/DEGRADED -> OPEN_PROCEDURE.
UNKNOWN never counts as NORMAL and never counts as an alert (it raises a data-quality message).
"""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
import pandas as pd

@dataclass
class Params:
    baseline_days: int = 5
    d_threshold: float = 1.5          # calibrated 14/11 (M1 decision 1): 0.7 % of healthy synthetic crews trigger, see docs/METHODES_NASA_DOSSIER.md s.7
    consecutive_days: int = 2
    sd_floor_rel: float = 0.05        # 5 % of the baseline mean
    sd_floor_abs: dict = field(default_factory=lambda: {"PS01": 1.0, "PS02": 1.0, "PS03": 0.5, "PS04": 1.0,
                                                         "CO02": 1.0, "PH09": 0.5, "PH01": 3.0})  # absolute SD floor per indicator
    max_age_min: int = 10
    ground_delay_min: int = 20

PROPOSED = Params()   # kept as alias: the calibrated values are now the default

# +1 = an increase is unfavourable, -1 = a decrease is unfavourable (P-07; PS03 direction is a proposal)
DIRECTION = {"PH09": -1, "PH01": +1, "CO01": +1, "CO02": +1, "PS01": +1, "PS02": +1, "PS04": +1, "PS03": -1}
DRIFT_INDICATORS = {"Body": ["PH01", "PH09"], "Attention": ["CO01", "CO02"], "Morale": ["PS01", "PS02", "PS03", "PS04"]}
DIMENSION_OF = {"PH01": "Body", "PH09": "Body", "PH10": "Body", "PH11": "Body", "PH12": "Body", "SY01": "Body",
                "CO01": "Attention", "CO02": "Attention", "PS01": "Morale", "PS02": "Morale", "PS03": "Morale",
                "PS04": "Morale", "MI03": "Mission", "MI05": "Mission", "HA01": "Habitat", "HA02": "Habitat",
                "HA03": "Habitat", "HA05": "Habitat"}

def daily_values(df: pd.DataFrame) -> pd.DataFrame:
    """One value per day and drift indicator. PH01 = wrist mean 06:00-07:00 (>= 3 OK points) else missing."""
    out = {}
    base = df[(df.source_id == "SYN") & df.indicator_id.isin(["PH09", "CO01", "CO02", "PS01", "PS02", "PS03", "PS04"])]
    for r in base.itertuples():
        out[(r.day, r.indicator_id)] = r.value
    for r in df[df.source_id == "WRIST-DAILY"].itertuples():
        out[(r.day, "PH01")] = r.value
    w = df[(df.source_id == "WRIST") & (df.indicator_id == "PH01")].copy()
    if len(w):
        w["t"] = pd.to_datetime(w.timestamp_utc)
        for day, g in w.groupby("day"):
            win = g[(g.t.dt.hour == 6) & (g.quality == "OK")]
            out[(day, "PH01")] = round(win.value.mean(), 1) if len(win) >= 3 else None
    dv = pd.Series(out, dtype="object").rename("value").reset_index()
    dv.columns = ["day", "indicator_id", "value"]
    return dv.pivot(index="day", columns="indicator_id", values="value").sort_index().astype(float)

def evaluate(dv: pd.DataFrame, prm: Params = Params()):
    """Apply the drift rule day by day. Returns (z, flags, states, decisions, reference)."""
    days = list(dv.index)
    inds = [i for v in DRIFT_INDICATORS.values() for i in v if i in dv.columns]
    base = dv.loc[[d for d in days if d <= prm.baseline_days], inds]
    mu, sd = base.mean(skipna=True), base.std(ddof=1, skipna=True)
    floor = mu.abs() * prm.sd_floor_rel
    for k, v in prm.sd_floor_abs.items():
        if k in floor.index:
            floor[k] = max(floor[k], v)
    sd_eff = np.maximum(sd.fillna(0), floor)
    z = pd.DataFrame({i: DIRECTION[i] * (dv[i] - mu[i]) / sd_eff[i] for i in inds}, index=days)
    flags = pd.DataFrame(False, index=days, columns=inds)
    for i in inds:
        run = 0
        for d in days:
            if pd.isna(z.at[d, i]):
                run = 0
                continue
            run = run + 1 if z.at[d, i] >= prm.d_threshold else 0
            flags.at[d, i] = d > prm.baseline_days and run >= prm.consecutive_days
    states = pd.DataFrame(index=days, columns=list(DRIFT_INDICATORS), dtype=object)
    for d in days:
        for dim, lst in DRIFT_INDICATORS.items():
            lst = [i for i in lst if i in inds]
            if d <= prm.baseline_days:
                states.at[d, dim] = "UNKNOWN"          # personal baseline under construction
                continue
            n = int(flags.loc[d, lst].sum())
            missing = any(pd.isna(dv.at[d, i]) for i in lst)
            states.at[d, dim] = "DEGRADED" if n >= 2 else "UNKNOWN" if missing else "WATCH" if n == 1 else "NORMAL"
    decisions, episode = [], None
    for d in days:
        out = [k for k, v in states.loc[d].items() if v in ("WATCH", "DEGRADED")]
        if len(out) >= 2:
            crit = "IMPORTANT" if (states.loc[d] == "DEGRADED").any() else "ROUTINE"
            # an open episode keeps its highest criticality until a human closes it
            episode = crit if episode is None else ("IMPORTANT" if "IMPORTANT" in (episode, crit) else "ROUTINE")
            decisions.append({"day": d, "action": "OPEN_PROCEDURE", "procedure_id": "PROC-FATIGUE-01", "criticality": episode, "dims_out": out})
        else:
            decisions.append({"day": d, "action": "CONTINUE", "procedure_id": "", "criticality": "ROUTINE", "dims_out": out})
    return z, flags, states, pd.DataFrame(decisions), {"mu": mu, "sd": sd, "sd_eff": sd_eff}

def event_rule(df: pd.DataFrame):
    """A ticked symptom opens the guided emergency procedure immediately (CRITICAL)."""
    return [{"timestamp_utc": r.timestamp_utc, "action": "OPEN_PROCEDURE", "procedure_id": "PROC-EMERGENCY-01",
             "criticality": "CRITICAL", "trigger": r.value_text} for r in df[df.indicator_id == "SY01"].itertuples()]
