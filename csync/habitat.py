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


SEVEN_DAY_MMHG = 2.5   # NASA OCHMO-TB-004: 7-day average below 2.5 mmHg keeps the headache risk under 1 % (context only)
REPLAY = os.path.join(ROOT, "research", "retro", "replay_results.csv")


def episodes(df: pd.DataFrame | None = None, limit: float = LIMIT_MMHG) -> list[dict]:
    """Runs of consecutive valid hours above the limit (an episode = one alert, not one per hour; replay of 20/11/2026).
    ARTIFACT hours never count and break a run."""
    df = rr1_hourly() if df is None else df
    assert {"hour_utc", "co2_mmhg", "artifact"} <= set(df.columns)
    out, cur = [], None
    for h, v, art in zip(df["hour_utc"], df["co2_mmhg"].round(2), df["artifact"].astype(bool), strict=True):
        above = (not art) and v > limit
        if above and cur and h - cur["end"] <= pd.Timedelta(hours=1):
            cur["end"], cur["hours"], cur["peak"] = h, cur["hours"] + 1, max(cur["peak"], float(v))
        elif above:
            cur = {"start": h, "end": h, "hours": 1, "peak": float(v)}
            out.append(cur)
        else:
            cur = None
    return out


def summary(df: pd.DataFrame | None = None) -> dict:
    """Numbers for the one-sentence reading of the Habitat chart (all computed, none typed)."""
    df = rr1_hourly() if df is None else df
    ok = df[~df["artifact"].astype(bool)]
    assert len(ok) > 0
    ep = episodes(df)
    day = ok.set_index("hour_utc")["co2_mmhg"].resample("1D").mean().dropna()
    r7 = day.rolling(7, min_periods=5).mean().dropna()
    return {"days": int(len(day)), "pct_under": round(100 * float((ok["co2_mmhg"].round(2) <= LIMIT_MMHG).mean()), 1),
            "episodes": len(ep), "longest_h": max((e["hours"] for e in ep), default=0),
            "pct_7d_above": round(100 * float((r7 > SEVEN_DAY_MMHG).mean()), 1) if len(r7) else None}


def replay() -> pd.DataFrame:
    """Pre-registered replay of the frozen rule on every ISS mission (research/retro, commit 9c4994b)."""
    return pd.read_csv(REPLAY)
