"""Blind replay of the frozen C-Sync Habitat rule over every ISS mission in the raw NASA EDA file.
Pre-registration: research/retro/PREREGISTRATION.md (committed before this script). Run: python research/retro/replay.py"""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from csync.habitat import LIMIT_MMHG, ppm_to_mmhg  # noqa: E402
from csync.quality import flag_plateaus  # noqa: E402
from scripts.eda_load import load  # noqa: E402

LAW_HEADACHE, COLE_CONGESTION = 2.0, 1.5


def mission_rows():
    for name, m in load().items():
        t = m.get("telemetry")
        if not t or not t.get("co2_iss"):
            continue
        s = pd.Series(pd.to_numeric(pd.Series(t["co2_iss"]), errors="coerce").values, index=pd.to_datetime(t["time"])).dropna()
        if s.empty:
            continue
        step = float(s.index.to_series().diff().dt.total_seconds().median() / 60)
        art = pd.Series(False, index=s.index)
        vals = s.tolist()
        for r in flag_plateaus(vals, min_len=max(2, int(60 / step))):
            art.iloc[r["start"]:r["start"] + r["length"]] = True
        h = pd.DataFrame({"mm": s.map(ppm_to_mmhg), "art": art}).resample("1h").agg({"mm": "mean", "art": "mean"}).dropna()
        h["art"] = h["art"] >= 0.5
        ok = h[~h["art"]].copy()
        ok["above"] = ok["mm"].round(2) > LIMIT_MMHG
        runs = (ok["above"] != ok["above"].shift()).cumsum()
        ep = ok[ok["above"]].groupby(runs[ok["above"]]).size()
        day = ok["mm"].resample("1D").mean().dropna()
        hidden = sum(int(g["above"].sum()) for d, g in ok.groupby(ok.index.floor("D")) if d in day.index and day[d] <= LIMIT_MMHG)
        r7 = day.rolling(7, min_periods=5).mean().dropna()
        yield {"mission": name, "hours_valid": len(ok), "hours_artifact": int(h["art"].sum()),
               "hours_above_3": int(ok["above"].sum()), "pct_above": round(100 * ok["above"].mean(), 1),
               "episodes": len(ep), "longest_ep_h": int(ep.max()) if len(ep) else 0,
               "days_mean_above_3": int((day > LIMIT_MMHG).sum()), "days": len(day),
               "hours_hidden_by_daily_mean": hidden,
               "pct_days_7d_above_2.0": round(100 * (r7 > LAW_HEADACHE).mean(), 1) if len(r7) else None,
               "pct_days_7d_above_1.5": round(100 * (r7 > COLE_CONGESTION).mean(), 1) if len(r7) else None,
               "max_7d_mmhg": round(float(r7.max()), 2) if len(r7) else None}


if __name__ == "__main__":
    df = pd.DataFrame(list(mission_rows()))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "replay_results.csv")
    df.to_csv(out, index=False)
    print(df.to_string(index=False))
