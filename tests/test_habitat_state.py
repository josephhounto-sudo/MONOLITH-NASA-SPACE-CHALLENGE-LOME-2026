"""Decision P6 (Joseph, 2026-11-18): real NASA data ENTER the calculation.

Habitat state = real ISS cabin CO2 (NASA OSDR EDA, mission RR-1, 26/09 -> 05/10/2014 = story days 1-10) against the NASA
design requirement (NASA-STD-3001 Vol 2 V2 6004: average one-hour ppCO2 <= 3 mmHg, as stated in NASA OCHMO-TB-004 Rev B).
Rules: hours flagged ARTIFACT (sensor plateau) never count; fewer than MIN_VALID_HOURS valid hours -> UNKNOWN, never NORMAL;
any valid hour above the requirement -> WATCH. The environment NEVER opens a procedure by itself and never changes the
crew-drift decision (that would need a new hold-out evaluation and an expert opinion).
"""
import importlib.util
import json
import os
import re

import pandas as pd
import pytest

from csync import habitat
from csync.language import banned_hits

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Derived from data/real/habitat_rr1_hourly.csv on 2026-11-18 (story day -> state); the real series is fixed, so this is stable.
EXPECTED = {1: "UNKNOWN", 2: "UNKNOWN", 3: "NORMAL", 4: "NORMAL", 5: "NORMAL", 6: "NORMAL", 7: "NORMAL", 8: "NORMAL",
            9: "WATCH", 10: "WATCH"}


def fake(co2_ppm, artifact=None, start="2014-09-26"):
    n = len(co2_ppm)
    return pd.DataFrame({"hour_utc": pd.date_range(start, periods=n, freq="h"), "co2_ppm": co2_ppm,
                         "artifact": artifact or [False] * n, "temp_c": [23.0] * n, "rh_pct": [40.0] * n,
                         "co2_mmhg": [habitat.ppm_to_mmhg(v) for v in co2_ppm]})


def test_nasa_conversion_note():
    # NASA brief: "0.5% CO2 = 3.8 mmHg"
    assert habitat.ppm_to_mmhg(5000) == pytest.approx(3.8, abs=0.01)


def test_story_days_match_the_real_series():
    assert {d: habitat.day_fact(d)["state"] for d in range(1, 11)} == EXPECTED


def test_unusable_sensor_is_unknown_never_normal():
    f1 = habitat.day_fact(1)
    assert f1["valid_hours"] == 0 and f1["state"] == "UNKNOWN" and f1["max_mmhg"] is None


def test_artifact_hours_never_count_even_when_above_the_limit():
    ppm = [2000.0] * 23 + [5000.0]          # last hour is above 3 mmHg but flagged as a sensor plateau
    art = [False] * 23 + [True]
    f = habitat.day_fact(1, df=fake(ppm, art))
    assert f["valid_hours"] == 23 and f["hours_above"] == 0 and f["state"] == "NORMAL"


def test_one_valid_hour_above_is_watch():
    ppm = [2000.0] * 23 + [4500.0]
    f = habitat.day_fact(1, df=fake(ppm))
    assert f["hours_above"] == 1 and f["state"] == "WATCH" and f["max_mmhg"] == pytest.approx(3.42, abs=0.01)


def test_too_few_valid_hours_is_unknown_even_if_all_above():
    ppm = [6000.0] * 11
    f = habitat.day_fact(1, df=fake(ppm))
    assert f["state"] == "UNKNOWN"


def test_exactly_the_limit_is_not_above():
    ppm = [3.0 / (760.0 * 1e-6)] * 24        # exactly 3.0 mmHg
    assert habitat.day_fact(1, df=fake(ppm))["hours_above"] == 0


@pytest.fixture(scope="module")
def story(tmp_path_factory):
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main(str(tmp_path_factory.mktemp("hab")))


def daily(caps, day):
    return next(c for c in caps if c.get("capsule_type", "daily") == "daily" and c["day"] == day)


@pytest.mark.parametrize("variant", ["histoire", "temoin", "capteur"])
def test_capsules_carry_the_computed_habitat_state(story, variant):
    for day in range(1, 11):
        cap = daily(story[variant], day)
        assert cap["states"]["Habitat"] == EXPECTED[day], (variant, day)
        assert cap["states"]["Mission"] == "UNKNOWN"
        assert cap["reliability"]["context_only"] == ["Mission"]
        assert cap["reliability"]["habitat_in_calculation"] is True
        sig = next(s for s in cap["signals"] if s["dimension"] == "Habitat")
        assert sig["indicator_id"] == "HA01" and sig["unit"] == "mmHg"


def test_watch_days_explain_with_real_numbers_and_the_nasa_requirement(story):
    cap = daily(story["histoire"], 9)
    f = habitat.day_fact(9)
    text = cap["explanation"]
    assert f"{f['hours_above']} h" in text and "3 mmHg" in text and "NASA-STD-3001" in text
    assert banned_hits(text) == []
    assert not re.search(r"\bcaus", text, re.I)          # co-occurrence only, never a stated cause


def test_environment_never_changes_the_crew_decision(story):
    # same actions as before habitat entered the calculation (rule v3 hold-out numbers stay valid)
    hist = {c["day"]: c["action"]["type"] for c in story["histoire"] if c.get("capsule_type", "daily") == "daily"}
    assert hist[7] == "OPEN_PROCEDURE" and hist[9] == "OPEN_PROCEDURE"
    assert all(c["action"]["type"] == "CONTINUE" for c in story["temoin"] if c.get("capsule_type", "daily") == "daily")
    # a habitat WATCH on days 9-10 of the control crew opens nothing
    assert daily(story["temoin"], 9)["states"]["Habitat"] == "WATCH"


def test_emergency_and_resume_capsules_show_the_same_habitat_state(story):
    em = next(c for c in story["histoire"] if c.get("capsule_type") == "emergency")
    rs = next(c for c in story["histoire"] if c.get("capsule_type") == "resume")
    assert em["states"]["Habitat"] == EXPECTED[9] and rs["states"]["Habitat"] == EXPECTED[10]


def test_capsules_still_validate_against_the_unchanged_contract(story):
    import jsonschema
    schema = json.load(open(os.path.join(ROOT, "contracts", "decision_capsule.schema.json"), encoding="utf8"))
    for caps in story.values():
        for c in caps:
            jsonschema.validate(c, schema)
