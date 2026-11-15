"""Rebuild data/real/habitat_missions.csv and habitat_rr1_hourly.csv from the raw NASA EDA file (checksum verified).
Run: python scripts/build_habitat.py     Source: NASA OSDR Environmental Data App (courtesy of EDA)."""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from csync.habitat import LIMIT_MMHG, ppm_to_mmhg  # noqa: E402
from csync.quality import flag_plateaus  # noqa: E402
from scripts.eda_load import load  # noqa: E402

PLATEAU_MIN_H = 1.0  # a run of identical CO2 values lasting at least one hour is flagged ARTIFACT


def main(out=os.path.join(ROOT, "data", "real")):
    rows, rr1 = [], None
    for name, m in load().items():
        t = m.get("telemetry")
        if not t or not t.get("co2_iss"):
            continue
        s = pd.Series(pd.to_numeric(pd.Series(t["co2_iss"]), errors="coerce").values, index=pd.to_datetime(t["time"]))
        if s.notna().sum() == 0:
            continue
        step_min = float(s.index.to_series().diff().dt.total_seconds().median() / 60)
        runs = flag_plateaus(s.tolist(), min_len=max(2, int(PLATEAU_MIN_H * 60 / step_min)))
        longest = max(runs, key=lambda r: r["length"]) if runs else None
        hourly = s.resample("1h").mean().dropna()
        mm = hourly.map(ppm_to_mmhg)
        rows.append({
            "mission": name, "cadence_min": round(step_min), "points": len(s),
            "missing_pct": round(100 * float(s.isna().mean()), 1), "hours": len(hourly),
            "artifact_runs_ge_1h": len(runs),
            "longest_run_h": round(longest["length"] * step_min / 60, 1) if longest else 0.0,
            "longest_run_ppm": float(longest["value"]) if longest else "",
            "median_mmhg": round(float(mm.median()), 2), "max_1h_mmhg": round(float(mm.max()), 2),
            "min_1h_mmhg": round(float(mm.min()), 2),
            "pct_hours_above_3mmhg": round(100 * float((mm > LIMIT_MMHG).mean()), 1),
            "sensor_zero_or_cap": bool((s.dropna() == 0).any() or (s.dropna() >= 5000).any()),
        })
        if name == "RR-1":
            art = pd.Series(False, index=hourly.index)
            for r in runs:
                a, b = s.index[r["start"]], s.index[r["end"]]
                art[(art.index >= a.floor("1h")) & (art.index <= b)] = True
            rr1 = pd.DataFrame({"hour_utc": hourly.index, "co2_ppm": hourly.round(1).values, "artifact": art.values})
    pd.DataFrame(rows).to_csv(os.path.join(out, "habitat_missions.csv"), index=False)
    rr1.to_csv(os.path.join(out, "habitat_rr1_hourly.csv"), index=False)
    return rows


if __name__ == "__main__":
    for r in main():
        print(r["mission"], r["longest_run_h"], r["pct_hours_above_3mmhg"], r["min_1h_mmhg"], r["max_1h_mmhg"])
