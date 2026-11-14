"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA
14/11 ~15:25 : relu et complété pour M4 par l'assistant (Claude Code) | VALIDATION HUMAINE M4 : À FAIRE

M4-1: procedure files are valid, carry the fixed sentence and contain no banned wording.
Added for M4 (14/11): step order of the task card, units consistent with the measurement data, no number
in the guided measures (no threshold), and the real procedure files driven through the resume gate."""
import json
import os
from datetime import datetime, timedelta

import jsonschema
import pytest

from csync.gate import resume_gate
from csync.language import banned_hits
from synthetic.generator import UNITS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, "contracts", "procedure_file.schema.json"), encoding="utf8"))
IDS = ["PROC-EMERGENCY-01", "PROC-FATIGUE-01"]
TREATMENT_WORDS = ["medication", "medicine", "drug", "dose", "treatment", "aspirin", "nitroglycerin"]


def load(pid):
    with open(os.path.join(ROOT, "data", "procedures", f"{pid}.json"), encoding="utf8") as f:
        return json.load(f)


def all_text(obj):
    if isinstance(obj, dict):
        return " ".join(all_text(v) for v in obj.values())
    if isinstance(obj, list):
        return " ".join(all_text(v) for v in obj)
    return obj if isinstance(obj, str) else ""


@pytest.mark.parametrize("pid", IDS)
def test_valid_against_contract(pid):
    jsonschema.validate(load(pid), SCHEMA)


@pytest.mark.parametrize("pid", IDS)
def test_fixed_sentence_and_wording(pid):
    p = load(pid)
    assert p["fixed_sentence"] == "Follow the onboard medical checklist and the crew medical officer."
    text = all_text(p).lower()
    assert banned_hits(text) == []
    assert not [w for w in TREATMENT_WORDS if w in text]


def test_emergency_has_six_steps_and_four_guided_measures():
    p = load("PROC-EMERGENCY-01")
    assert [s["n"] for s in p["steps"]] == [1, 2, 3, 4, 5, 6]
    measures = p["steps"][2]["measures"]
    assert [m["indicator_id"] for m in measures] == ["PH01", "PH10", "PH11", "PH12"]
    for m in measures:
        assert m["how_to"]
    assert measures[3]["nasa_reference"] is False          # blood glucose: no NASA in-flight reference


def measure_items():
    for pid in IDS:
        for s in load(pid)["steps"]:
            for item in [s, *s.get("measures", [])]:
                if "how_to" in item:
                    yield pid, item


def test_every_measure_has_a_nasa_source_or_says_there_is_none():
    for pid, m in measure_items():
        if m.get("nasa_reference") is False:
            assert "why" not in m and "hrp_source_url" not in m, (pid, m["measure"])
        else:
            assert m["why"] and m["hrp_source_url"].startswith("https://www.nasa.gov/"), (pid, m["measure"])


def test_no_placeholder_left():
    for pid in IDS:
        assert "TODO" not in json.dumps(load(pid))


def test_sources_are_listed_in_help_card_file():
    cards = open(os.path.join(ROOT, "docs", "HELP_CARD_SOURCES.md"), encoding="utf8").read()
    for pid, m in measure_items():
        if m.get("nasa_reference") is not False:
            assert m["hrp_source_url"] in cards and m["why"] in cards, (pid, m["measure"])


def test_emergency_steps_follow_the_task_card_order():
    """Task card M4-1: 1 safety, 2 where, 3 guided measurements, 4 report, 5 send with link status, 6 log."""
    texts = [s["text"] for s in load("PROC-EMERGENCY-01")["steps"]]
    prefixes = ["Safety:", "Where:", "Guided measurements", "Report:", "Send:", "Log:"]
    assert all(t.startswith(p) for t, p in zip(texts, prefixes)), texts
    assert "link status" in texts[4].lower()


def test_temperature_and_glucose_say_no_nasa_reference():
    measures = {m["indicator_id"]: m for m in load("PROC-EMERGENCY-01")["steps"][2]["measures"]}
    assert measures["PH11"]["nasa_reference"] is False and measures["PH12"]["nasa_reference"] is False


def test_guided_measures_carry_no_number_so_no_threshold():
    """V5: no clinical threshold in a procedure file. A guided measure is recorded, never compared."""
    for m in load("PROC-EMERGENCY-01")["steps"][2]["measures"]:
        text = " ".join(m.get(k, "") for k in ("how_to", "why"))
        assert not any(c.isdigit() for c in text), (m["measure"], text)


def test_units_match_the_measurement_data():
    for pid, m in measure_items():
        if "unit" in m:
            assert m["unit"] == UNITS[m["indicator_id"]], (pid, m["measure"])


REQ = datetime(2031, 3, 10, 9, 0)   # story day 10, 09:00 (synthetic.generator.ts(10, 9))


def guided(ind, minutes_ago, source="GUIDED", quality="OK"):
    return {"indicator_id": ind, "timestamp": REQ - timedelta(minutes=minutes_ago), "quality": quality, "source": source}


def gate_view(pid):
    p = load(pid)
    return {k: p.get(k) for k in ("prerequisites", "no_physical_prereq", "override_policy")}


def test_emergency_file_drives_the_resume_gate():
    """G1, G3, G6 with the real file, not a test fixture: the 2 prerequisites are read from PROC-EMERGENCY-01."""
    proc = gate_view("PROC-EMERGENCY-01")
    assert resume_gate(REQ, [guided("PH01", 3), guided("CO01", 5)], proc)[0] == "RESUME_AUTHORIZED"
    # story act 3: heart rate taken at 08:46 (14 min), control PVT at 08:55 (5 min), Commander override
    d, reasons = resume_gate(REQ, [guided("PH01", 14), guided("CO01", 5)], proc, override={"by": "Commander"})
    assert d == "REFUSE_RESUME"
    assert reasons[0] == "G3: PH01 is stale (14 min > 10 min)" and reasons[-1].startswith("G6")
    # a wrist reading is not a guided measurement
    assert resume_gate(REQ, [guided("PH01", 3, source="WRIST"), guided("CO01", 5)], proc)[0] == "REFUSE_RESUME"
