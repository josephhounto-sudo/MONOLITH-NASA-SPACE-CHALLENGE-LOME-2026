"""Prototype: exposure ledger (registry id exposure_ledger, V3 20/11/2026). REAL NASA data (OSDR EDA, ISS missions).

One gauge per mission day: cumulative radiation dose received in the cabin (absorbed dose, mGy; NOT the 600 mSv career
limit, which is an effective dose) and the 7-day mean cabin CO2 against NASA's 2.5 mmHg level (OCHMO-TB-004)."""
from __future__ import annotations

import pandas as pd

from csync import habitat


def ledger() -> pd.DataFrame:
    """Columns: date, radiation_mgy_cum (from NASA's own 'accumulated' column), co2_7d_mmhg, co2_7d_above_2_5."""
    rad = habitat.rr1_radiation()[["date", "accumulated_mgy"]].rename(columns={"accumulated_mgy": "radiation_mgy_cum"})
    co2 = habitat.daily_means().rolling(7, min_periods=5).mean().rename("co2_7d_mmhg").reset_index()
    co2 = co2.rename(columns={co2.columns[0]: "date"})
    co2["date"] = pd.to_datetime(co2["date"]).dt.normalize()
    rad["date"] = pd.to_datetime(rad["date"]).dt.normalize()
    out = rad.merge(co2, on="date", how="left")
    out["co2_7d_above_2_5"] = out["co2_7d_mmhg"] > habitat.SEVEN_DAY_MMHG
    assert out["radiation_mgy_cum"].is_monotonic_increasing, "a cumulative dose never goes down"
    return out
