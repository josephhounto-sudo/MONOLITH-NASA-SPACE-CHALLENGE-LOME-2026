"""M2-3: the real NASA EDA RR-1 hourly CO2 series contains exactly one frozen run: 37 h at 2646 ppm."""
import os

import pandas as pd

from csync.quality import flag_plateaus, mark_quality

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data", "real", "eda_rr1_iss_hourly_2014-09-26_to_10-05.csv")


def test_real_eda_single_37h_plateau():
    df = pd.read_csv(CSV)
    runs = flag_plateaus(df.co2_ppm.tolist(), min_len=6)
    assert len(runs) == 1
    r = runs[0]
    assert r["value"] == 2646 and r["length"] == 37
    assert df.hour_utc[r["start"]] == "2014-09-26 00:00" and df.hour_utc[r["end"]] == "2014-09-27 12:00"


def test_mark_quality_sets_artifact_only_on_plateau():
    q = mark_quality(pd.read_csv(CSV)).quality
    assert (q == "ARTIFACT").sum() == 37 and (q == "OK").sum() == len(q) - 37


def test_short_runs_and_missing_values():
    assert flag_plateaus([1, 1, 1, 1, 1, 2]) == []
    assert flag_plateaus([1] * 6) == [{"start": 0, "end": 5, "length": 6, "value": 1}]
    assert flag_plateaus([1, 1, 1, None, 1, 1, 1]) == []
    assert flag_plateaus([float("nan")] * 8) == []
