"""Try-it engine: the visitor types two days of check-in values, the SAME rule v3 (csync.rules.evaluate) answers.

Baseline = days 1-5 of the synthetic story crew member (data/out/measurements_histoire.csv). Typed values are days 6 and 7.
An empty value is missing: its dimension reads UNKNOWN, never NORMAL. Nothing here is a clinical threshold.
15/11/2026 · FAIT PAR L'IA (session design) — PAS ENCORE VÉRIFIÉ
"""
from __future__ import annotations

import math
import os

import pandas as pd

from csync.rules import DIMENSION_OF, DIRECTION, DRIFT_INDICATORS, Params, daily_values, evaluate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDICATORS = [i for lst in DRIFT_INDICATORS.values() for i in lst]


def baseline() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(ROOT, "data", "out", "measurements_histoire.csv"))
    dv = daily_values(df[df.variant == "histoire"])
    return dv.loc[[d for d in dv.index if d <= Params().baseline_days], INDICATORS]


def story_day(day: int) -> dict:
    """Story values of one day, to prefill the inputs."""
    df = pd.read_csv(os.path.join(ROOT, "data", "out", "measurements_histoire.csv"))
    dv = daily_values(df[df.variant == "histoire"])
    return {i: float(dv.at[day, i]) for i in INDICATORS if not math.isnan(dv.at[day, i])}


def try_it(day6: dict, day7: dict, prm: Params = Params()) -> dict:
    """day6 / day7: {indicator_id: float or None}. Returns states of day 7, d per indicator, flags, decision, reference."""
    b = baseline()
    rows = {6: day6, 7: day7}
    dv = pd.concat([b, pd.DataFrame({d: {i: (None if v.get(i) is None or (isinstance(v.get(i), float) and math.isnan(v.get(i))) else float(v[i]))
                                          for i in INDICATORS} for d, v in rows.items()}).T.astype(float)])
    z, flags, states, decisions, ref = evaluate(dv, prm)
    last = decisions[decisions.day == 7].iloc[0]
    return {"states": states.loc[7].to_dict(), "z": {i: (None if pd.isna(z.at[7, i]) else round(float(z.at[7, i]), 2)) for i in INDICATORS},
            "flagged": {i: bool(flags.at[7, i]) for i in INDICATORS}, "action": last.action, "procedure_id": last.procedure_id,
            "criticality": last.criticality, "mean": {i: round(float(ref["mu"][i]), 2) for i in INDICATORS},
            "direction": {i: DIRECTION[i] for i in INDICATORS}, "dimension": {i: DIMENSION_OF[i] for i in INDICATORS}}
