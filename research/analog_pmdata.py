"""Run the shipped rule on PMData wellness + resting heart rate.

Open files under data/real/raw/pmdata/ (OSF vx4bk). Not astronauts.
csync.rules.evaluate is called unchanged. daily_values() only reads
source_id SYN, so this script builds the daily table from the Measurement
records itself, then calls evaluate.

Unmeasured drift indicators are left as missing days, so a dimension that
was not fully recorded stays UNKNOWN unless two of its present indicators
are flagged (the shipped missing-data line).

Run: python research/analog_pmdata.py
"""
from __future__ import annotations

import csv
import json
import os
from collections import Counter
from datetime import datetime, timedelta

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, ROOT)

from csync.adapters import pmdata_measurements
from csync.rules import DRIFT_INDICATORS, Params, evaluate

RAW = os.path.join(ROOT, "data", "real", "raw", "pmdata")
INDS = [i for ids in DRIFT_INDICATORS.values() for i in ids]


def _stamp(text: str) -> str:
    # Keep the UTC date written in the file. Do not shift it to a local zone.
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return text


def rows_for(participant: str) -> list[dict]:
    base = os.path.join(RAW, participant)
    rows = []
    well = os.path.join(base, "pmsys", "wellness.csv")
    with open(well, newline="", encoding="utf8") as f:
        for rec in csv.DictReader(f):
            ts = _stamp(rec["effective_time_frame"])
            for field in ("sleep_duration_h", "stress", "mood"):
                raw = rec[field].strip()
                rows.append({"timestamp_utc": ts, "field": field, "value": None if raw == "" else float(raw)})
    rhr_path = os.path.join(base, "fitbit", "resting_heart_rate.json")
    if os.path.exists(rhr_path):
        blob = json.load(open(rhr_path, encoding="utf8"))
        for rec in blob:
            inner = rec.get("value") or {}
            day = rec["dateTime"][:10]
            empty = inner.get("date") in (None, "") or inner.get("value") in (None, 0, 0.0)
            rows.append({"timestamp_utc": day + "T00:00:00+00:00", "field": "resting_heart_rate",
                         "value": None if empty else float(inner["value"])})
    return rows


def daily_table(measurements: list[dict]) -> pd.DataFrame:
    by = {}
    for m in measurements:
        day = m["timestamp_utc"][:10]
        by.setdefault((day, m["indicator_id"]), m["value"])
    if not by:
        return pd.DataFrame(columns=INDS)
    dates = sorted({d for d, _ in by})
    start = datetime.fromisoformat(dates[0])
    end = datetime.fromisoformat(dates[-1])
    idx, cursor = [], start
    while cursor <= end:
        idx.append(cursor.date().isoformat())
        cursor += timedelta(days=1)
    frame = pd.DataFrame(index=range(1, len(idx) + 1), columns=INDS, dtype=float)
    pos = {day: i + 1 for i, day in enumerate(idx)}
    for (day, ind), value in by.items():
        if value is not None:
            frame.at[pos[day], ind] = value
    return frame


def one(participant: str) -> dict:
    ms = pmdata_measurements(participant, rows_for(participant))
    dv = daily_table(ms)
    _, _, states, decisions, _ = evaluate(dv, Params())
    scored = states.loc[states.index > Params().baseline_days]
    counts = {dim: dict(Counter(scored[dim].astype(str))) for dim in states.columns}
    return {
        "participant": participant,
        "measurements": len(ms),
        "calendar_days": int(len(dv)),
        "days_with_any_value": int(dv[INDS].notna().any(axis=1).sum()),
        "procedures": int((decisions.action == "OPEN_PROCEDURE").sum()),
        "states_after_baseline": counts,
        "has_resting_heart_rate_file": os.path.exists(os.path.join(RAW, participant, "fitbit", "resting_heart_rate.json")),
    }


def main() -> None:
    people = sorted(p for p in os.listdir(RAW) if p.startswith("p"))
    rows = [one(p) for p in people]
    out = {"people": len(rows), "rows": rows,
           "not_measured": ["CO01", "CO02", "PS01", "PS04", "PH10", "PH11", "PH12", "SY01"]}
    path = os.path.join(ROOT, "research", "analog_pmdata_results.json")
    with open(path, "w", encoding="utf8") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    procs = sum(r["procedures"] for r in rows)
    days = sum(r["calendar_days"] for r in rows)
    print(f"people {len(rows)} calendar_days {days} procedure_days {procs}")
    for r in rows:
        print(r["participant"], "days", r["calendar_days"], "proc", r["procedures"], r["states_after_baseline"])


if __name__ == "__main__":
    main()
