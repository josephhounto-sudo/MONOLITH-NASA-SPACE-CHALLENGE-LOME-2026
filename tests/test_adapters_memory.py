"""Adapter (quality control before rules) and local memory (append-only, once per record)."""
import collections

import jsonschema
import pytest

from csync import habitat
from csync.adapters import SCHEMA, eda_measurements, pmdata_measurements
from csync.memory import LocalMemory


def test_adapter_flags_missing_and_constant_runs_and_validates_contract():
    vals = [400.0, 401.0] + [500.0] * 6 + [None, 402.0]
    ms = eda_measurements([f"2014-09-26T0{i}:00" if i < 10 else f"2014-09-26T{i}:00" for i in range(10)], vals, "co2_ppm", "RR-1")
    q = [m["quality"] for m in ms]
    assert q == ["OK", "OK"] + ["ARTIFACT"] * 6 + ["MISSING", "OK"]
    assert ms[8]["value"] is None
    for m in ms:
        jsonschema.validate(m, SCHEMA)
        assert m["origin"] == "REAL_OPEN" and m["evidence_kind"] == "MISSION_CONTEXT" and m["indicator_id"] == "HA01"


def test_rr1_measurements_keep_the_153h_run_as_artifact():
    ms = habitat.rr1_measurements()
    c = collections.Counter(m["quality"] for m in ms)
    assert len(ms) == 1009 and c["ARTIFACT"] >= 150 and c["MISSING"] == 0
    assert all(m["value"] == 2646.0 for m in ms if m["quality"] == "ARTIFACT" and m["timestamp_utc"] < "2014-09-27")


def test_pmdata_adapter_keeps_a_zero_resting_rate_missing():
    ms = pmdata_measurements("p00", [
        {"timestamp_utc": "2019-11-11T08:06:00+00:00", "field": "sleep_duration_h", "value": 8},
        {"timestamp_utc": "2019-11-11T00:00:00+00:00", "field": "resting_heart_rate", "value": 0},
        {"timestamp_utc": "2019-11-12T00:00:00+00:00", "field": "resting_heart_rate", "value": 52.2},
        {"timestamp_utc": "2019-11-11T08:06:00+00:00", "field": "mood", "value": 4},
    ])
    by = {(m["indicator_id"], m["timestamp_utc"][:10]): m for m in ms}
    assert by[("PH01", "2019-11-11")]["quality"] == "MISSING" and by[("PH01", "2019-11-11")]["value"] is None
    assert by[("PH01", "2019-11-12")]["quality"] == "OK" and by[("PH01", "2019-11-12")]["value"] == pytest.approx(52.2)
    assert by[("PH09", "2019-11-11")]["evidence_kind"] == "SELF_REPORTED"
    assert all(m["origin"] == "REAL_OPEN" and m["source_id"] == "PMDATA-p00" for m in ms)


def test_memory_stores_each_record_once_and_survives_restart(tmp_path):
    path = str(tmp_path / "mem.jsonl")
    ms = habitat.rr1_measurements()[:50]
    mem = LocalMemory(path)
    assert mem.add(ms) == 50 and mem.add(ms) == 0
    again = LocalMemory(path)                     # restart: the file is the only state
    assert again.add(ms) == 0 and len(again.records()) == 50
    assert again.add(habitat.rr1_measurements()[:60]) == 10


def test_memory_never_rewrites_existing_lines(tmp_path):
    path = tmp_path / "mem.jsonl"
    mem = LocalMemory(str(path))
    ms = habitat.rr1_measurements()[:5]
    mem.add(ms)
    before = path.read_text()
    mem.add(habitat.rr1_measurements()[3:8])
    assert path.read_text().startswith(before)
