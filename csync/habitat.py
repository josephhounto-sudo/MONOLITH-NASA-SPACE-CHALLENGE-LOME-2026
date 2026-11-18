"""Habitat state from REAL NASA ISS cabin telemetry (OSDR Environmental Data App) against a NASA requirement. Not clinical.

V2 (decision P6, Joseph, 2026-11-18): this data ENTERS the calculation as the Habitat state (day_fact / story_days below).
It never opens a procedure by itself and never changes the crew-drift decision.

Reference: NASA-STD-3001 Vol. 2 Rev C requirement V2 6004 (average one-hour CO2 partial pressure in the habitable volume
must not exceed 3 mmHg), as stated in NASA OCHMO-TB-004 Rev B (11/10/2022). The same brief gives the current ISS
range as 1 to 9 mmHg. EDA reports CO2 in ppm: the conversion below assumes a total pressure of 760 mmHg (the brief's own
note: 0.5 % CO2 = 3.8 mmHg), so it is an approximation, not a compliance statement (sensor location and calibration
are not documented in the dataset).
"""
from __future__ import annotations

import functools
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL = os.path.join(ROOT, "data", "real")
P_TOTAL_MMHG = 760.0
LIMIT_MMHG = 3.0
ISS_RANGE_MMHG = (1.0, 9.0)
STORY_DAY1 = pd.Timestamp("2014-09-26")   # docs/STORY.md: 26/09 -> 05/10/2014 = story days 1 -> 10
MIN_VALID_HOURS = 12                      # DESIGN PARAMETER, not NASA: fewer valid hours in a day -> UNKNOWN
REQUIREMENT_ID = "NASA-STD-3001 Vol 2 V2 6004"
SOURCE_LIMIT = "https://nasa.gov/wp-content/uploads/2023/03/co2-technical-brief-ochmo.pdf"
SOURCE_DATA = "https://visualization.osdr.nasa.gov/eda/"


def ppm_to_mmhg(ppm: float) -> float:
    """Partial pressure of CO2 for a volume fraction in ppm at 760 mmHg total pressure."""
    return ppm * 1e-6 * P_TOTAL_MMHG


def rr1_hourly() -> pd.DataFrame:
    """RR-1 ISS CO2, hourly means (columns: hour_utc, co2_ppm, co2_mmhg, artifact)."""
    df = pd.read_csv(os.path.join(REAL, "habitat_rr1_hourly.csv"), parse_dates=["hour_utc"])
    df["co2_mmhg"] = df["co2_ppm"].map(ppm_to_mmhg)
    return df


@functools.lru_cache(maxsize=1)
def _rr1_measurements() -> tuple:
    from csync.adapters import eda_measurements
    df = pd.read_csv(os.path.join(REAL, "habitat_rr1_hourly.csv"))
    return tuple(eda_measurements(df["hour_utc"], df["co2_ppm"], "co2_ppm", "RR-1"))


def rr1_measurements() -> list[dict]:
    """RR-1 CO2 as validated Measurement records, quality control applied (csync.adapters)."""
    return [dict(m) for m in _rr1_measurements()]


def rr1_radiation() -> pd.DataFrame:
    return pd.read_csv(os.path.join(REAL, "eda_rr1_radiation_daily.csv"), parse_dates=["date"])


def missions() -> pd.DataFrame:
    """One row per mission with usable ISS CO2 telemetry (built by scripts/build_habitat.py from the raw EDA file)."""
    return pd.read_csv(os.path.join(REAL, "habitat_missions.csv"))


def day_fact(story_day: int, df: pd.DataFrame | None = None) -> dict:
    """Habitat state of one story day. Hours flagged ARTIFACT (sensor plateau) never count.

    UNKNOWN when fewer than MIN_VALID_HOURS valid hours (never NORMAL); WATCH when at least one valid one-hour mean is above
    the NASA requirement (3 mmHg, compared at the data's own 0.01 mmHg resolution); NORMAL otherwise.
    """
    df = rr1_hourly() if df is None else df
    start = STORY_DAY1 + pd.Timedelta(days=int(story_day) - 1)
    day = df[(df.hour_utc >= start) & (df.hour_utc < start + pd.Timedelta(days=1))]
    ok = day[~day["artifact"].astype(bool)]
    mm = ok["co2_mmhg"].round(2)
    valid, above = int(len(ok)), int((mm > LIMIT_MMHG).sum())
    state = "UNKNOWN" if valid < MIN_VALID_HOURS else "WATCH" if above else "NORMAL"
    return {"day": int(story_day), "state": state, "valid_hours": valid, "hours_above": above,
            "max_mmhg": float(mm.max()) if valid else None, "limit_mmhg": LIMIT_MMHG, "requirement": REQUIREMENT_ID}


def story_days(n: int = 10) -> dict:
    """{story day: day_fact} for days 1..n, read once."""
    df = rr1_hourly()
    return {d: day_fact(d, df) for d in range(1, n + 1)}
