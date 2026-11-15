"""Habitat context from real NASA data: recomputed from the raw file, never trusted from the CSV alone."""
import pandas as pd
import pytest

from csync import habitat
from csync.language import banned_hits
from scripts import build_habitat
from scripts.eda_load import load


def test_conversion_matches_nasa_brief_note():
    # NASA brief: 0.5 % CO2 = 3.8 mmHg ; our limit 3 mmHg is about 3,947 ppm at 760 mmHg
    assert habitat.ppm_to_mmhg(5000) == pytest.approx(3.8, abs=0.01)
    assert habitat.ppm_to_mmhg(3947.37) == pytest.approx(habitat.LIMIT_MMHG, abs=0.001)


def test_rebuild_matches_committed_files(tmp_path):
    build_habitat.main(str(tmp_path))
    for f in ("habitat_missions.csv", "habitat_rr1_hourly.csv"):
        pd.testing.assert_frame_equal(pd.read_csv(tmp_path / f), pd.read_csv(habitat.REAL + "/" + f))


def test_rr1_long_flat_run_is_flagged_never_normal():
    m = habitat.missions().set_index("mission")
    assert m.at["RR-1", "longest_run_h"] == pytest.approx(153.1, abs=0.1)
    assert m.at["RR-1", "longest_run_ppm"] == 2646
    df = habitat.rr1_hourly()
    flat = df[df["artifact"] & (df["co2_ppm"] == 2646)]
    assert len(flat) >= 150


def test_every_mission_row_traces_to_raw_data():
    raw = load()
    for name in habitat.missions()["mission"]:
        assert name in raw and raw[name]["telemetry"]["co2_iss"]


def test_twelve_of_fourteen_missions_have_constant_runs():
    m = habitat.missions()
    assert len(m) == 14 and int((m["artifact_runs_ge_1h"] > 0).sum()) == 12


def test_suspect_sensor_values_are_marked():
    m = habitat.missions().set_index("mission")
    assert bool(m.at["RR-22", "sensor_zero_or_cap"]) and bool(m.at["RR-3", "sensor_zero_or_cap"])


def test_texts_have_no_banned_words():
    import json
    ui = json.load(open(habitat.ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    text = " ".join(v for k, v in ui.items() if k.startswith("habitat") and isinstance(v, str))
    assert banned_hits(text) == []
