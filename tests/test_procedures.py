"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

M4-1: procedure files are valid, carry the fixed sentence and contain no banned wording."""
import json
import os

import jsonschema
import pytest

from csync.language import banned_hits

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
