"""Data-quality checks on real habitat telemetry. Owner: M2 (task card M2-3).

A long run of identical values is flagged as ARTIFACT: it is never taken as normal. This is a data-quality rule,
not a clinical or environmental threshold; min_len is a design parameter (6 consecutive points by default).
"""
from __future__ import annotations

import math

import pandas as pd


def flag_plateaus(values, min_len: int = 6) -> list[dict]:
    """Return the runs where the value stays identical for at least min_len consecutive points.

    Each run: {"start": first index, "end": last index (inclusive), "length": n points, "value": v}.
    Missing values (None/NaN) break a run and are never part of one.
    """
    vals = list(values)
    runs, i = [], 0
    while i < len(vals):
        v = vals[i]
        if v is None or (isinstance(v, float) and math.isnan(v)):
            i += 1
            continue
        j = i
        while j + 1 < len(vals) and vals[j + 1] == v:
            j += 1
        if j - i + 1 >= min_len:
            runs.append({"start": i, "end": j, "length": j - i + 1, "value": v})
        i = j + 1
    return runs


def mark_quality(df: pd.DataFrame, column: str = "co2_ppm", min_len: int = 6) -> pd.DataFrame:
    """Copy of df with a 'quality' column: ARTIFACT on plateau points of `column`, OK elsewhere (MISSING if empty)."""
    out = df.copy()
    q = ["MISSING" if pd.isna(v) else "OK" for v in out[column]]
    for r in flag_plateaus(out[column].tolist(), min_len):
        for k in range(r["start"], r["end"] + 1):
            q[k] = "ARTIFACT"
    out["quality"] = q
    return out
