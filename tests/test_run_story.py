"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

M2-2: one command produces every capsule the UI shows; all capsules are valid."""
import json
import os
import subprocess
import sys

import jsonschema
import pytest

from csync.language import banned_hits

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, "contracts", "decision_capsule.schema.json"), encoding="utf8"))


@pytest.fixture(scope="module")
def out(tmp_path_factory):
    d = tmp_path_factory.mktemp("out")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run_story.py"), "--out", str(d)],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr
    return d


def load(out, v):
    return json.load(open(out / f"capsules_{v}.json", encoding="utf8"))


@pytest.mark.parametrize("variant", ["histoire", "temoin", "capteur"])
def test_three_files_valid(out, variant):
    caps = load(out, variant)
    assert sorted(c["day"] for c in caps if c["capsule_type"] == "daily") == list(range(1, 11))
    for c in caps:
        jsonschema.validate(c, SCHEMA)
        assert c["human_decision"] == "pending"
        assert banned_hits(" ".join([c["situation"], c["explanation"], c["action"]["text"]])) == []


def test_story_emergency_day9(out):
    em = [c for c in load(out, "histoire") if c["capsule_type"] == "emergency"]
    assert len(em) == 1
    e = em[0]
    assert e["day"] == 9 and e["time_utc"] == "14:10" and e["ui_hint"] == "ACTION"
    assert e["action"]["procedure_id"] == "PROC-EMERGENCY-01" and e["action"]["criticality"] == "CRITICAL"
    q = e["send_queue"]
    assert q["report_created_utc"].endswith("14:20") and q["report_received_utc"].endswith("19:20")
    assert q["report_deliveries_to_ground"] == 1 and q["duplicates_dropped"] == 3 and q["ground_order_by_creation"]


def test_story_resume_day10_refused_even_with_override(out):
    rs = [c for c in load(out, "histoire") if c["capsule_type"] == "resume"]
    assert len(rs) == 1
    r = rs[0]
    assert r["day"] == 10 and r["action"]["type"] == "REFUSE_RESUME" and r["ui_hint"] == "FOCUS"
    assert r["reliability"]["gate_reasons"] == ["G3: PH01 is stale (14 min > 10 min)"]
    assert any(x.startswith("G6") for x in r["reliability"]["gate_reasons_with_override"])
    assert r["reliability"]["gate_reasons_text"] == ["The heart-rate reading is 14 min old; the limit is 10 min."]
    assert "G3" not in r["explanation"] and "14 min old" in r["explanation"]


def test_controls_have_no_story_events(out):
    for v in ("temoin", "capteur"):
        assert {c["capsule_type"] for c in load(out, v)} == {"daily"}


def test_sensor_outage_day7_body_unknown(out):
    day7 = next(c for c in load(out, "capteur") if c["day"] == 7)
    assert day7["states"]["Body"] == "UNKNOWN" and "PH01" in day7["reliability"]["missing_indicators"]


def test_day10_daily_does_not_say_continue_while_emergency_open(out):
    day10 = next(c for c in load(out, "histoire") if c["capsule_type"] == "daily" and c["day"] == 10)
    assert "Continue" not in day10["action"]["text"]
    assert day10["open_episode"]["procedure_id"] == "PROC-EMERGENCY-01"


def _load_run_story():
    import importlib.util
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_load_procedure_accepts_known_ids_and_refuses_others():
    rs = _load_run_story()
    assert isinstance(rs.load_procedure("PROC-EMERGENCY-01"), dict)
    assert isinstance(rs.load_procedure("PROC-FATIGUE-01"), dict)
    for bad in ("../README", "PROC-UNKNOWN-99", ""):
        with pytest.raises(ValueError):
            rs.load_procedure(bad)
