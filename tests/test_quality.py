"""M2-3: the real NASA EDA RR-1 hourly extract (26/09-05/10/2014) contains exactly one constant run: 37 h at 2646 ppm.
The RAW 5-min series holds the whole run: 1837 points = 153 h (21/09 04:24 to 27/09 13:25); see test_raw_series_plateau_is_153h."""
import os

import pandas as pd

from csync.quality import flag_plateaus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data", "real", "eda_rr1_iss_hourly_2014-09-26_to_10-05.csv")


def test_real_eda_single_37h_plateau():
    df = pd.read_csv(CSV)
    runs = flag_plateaus(df.co2_ppm.tolist(), min_len=6)
    assert len(runs) == 1
    r = runs[0]
    assert r["value"] == 2646 and r["length"] == 37
    assert df.hour_utc[r["start"]] == "2014-09-26 00:00" and df.hour_utc[r["end"]] == "2014-09-27 12:00"


def test_short_runs_and_missing_values():
    assert flag_plateaus([1, 1, 1, 1, 1, 2]) == []
    assert flag_plateaus([1] * 6) == [{"start": 0, "end": 5, "length": 6, "value": 1}]
    assert flag_plateaus([1, 1, 1, None, 1, 1, 1]) == []
    assert flag_plateaus([float("nan")] * 8) == []


def test_raw_series_plateau_is_153h():
    """The 37 h of the hourly extract is the part of a longer constant run (>= 12 h) in the raw series of RR-1."""
    import gzip, json
    raw = os.path.join(ROOT, "data", "real", "raw", "eda_all_missions.json.gz")
    t = json.load(gzip.open(raw))["missions"]["RR-1"]["telemetry"]
    runs = flag_plateaus(t["co2_iss"], min_len=144)  # 144 points of 5 min = 12 h
    assert len(runs) == 1
    r = runs[0]
    assert r["value"] == 2646 and r["length"] == 1837
    assert t["time"][r["start"]] == "2014-09-21 04:24:00" and t["time"][r["end"]] == "2014-09-27 13:25:00"
