"""Evidence-at-scale module: counts come from the raw file, the live crew run is deterministic. 15/11/2026 · FAIT PAR L'IA."""
import pandas as pd
from csync import scale
from csync.habitat import missions


def test_inventory_matches_the_raw_file_and_the_committed_summary():
    inv = scale.raw_inventory()
    assert inv["missions"] >= 14 and inv["points"] > 500_000
    assert inv["hours"] == round(inv["points"] * 5 / 60)
    assert inv["per_mission"]["RR-1"] == 12087


def test_reprocess_equals_the_committed_mission_table():
    r = scale.reprocess_nasa()
    got = pd.DataFrame(r["rows"]).set_index("mission")
    ref = missions().set_index("mission")
    assert list(got.index) == list(ref.index)
    for col in ("points", "hours", "artifact_runs_ge_1h", "longest_run_h"):
        assert (got[col] == ref[col]).all(), col


def test_crew_run_is_deterministic_and_bounded():
    a, b = scale.crews(12, 6, seed0=50000), scale.crews(12, 6, seed0=50000)
    assert a["control"]["hits"] == b["control"]["hits"] and a["gradual"]["hits"] == b["gradual"]["hits"]
    assert 0 <= a["control"]["hits"] <= 12 and 0 <= a["gradual"]["hits"] <= 6
