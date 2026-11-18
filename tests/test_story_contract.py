"""V2 story contract: the story is FROZEN (decision of 2026-11-18). Design may change; these facts may not.

If one of these tests fails, the code drifted from docs/STORY.md or someone changed a beat.
A changed beat needs a new paper test with 7 strangers (60 s, 3 questions; threshold 5 of 7), not just a new constant here.
"""
import importlib.util
import os
import re

import pytest

from csync.rules import Params

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORY = open(os.path.join(ROOT, "docs", "STORY.md"), encoding="utf8").read()


@pytest.fixture(scope="module")
def story(tmp_path_factory):
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = mod.main(str(tmp_path_factory.mktemp("story")))
    return mod, out["histoire"]


def by(caps, kind, day):
    return next(c for c in caps if c.get("capsule_type", "daily") == kind and c["day"] == day)


def test_story_document_still_says_what_this_contract_checks():
    # the contract is only meaningful while the reference text keeps the same facts
    for fragment in ("13:00-19:00", "14:10", "14:20", "19:20", "une seule fois", "08:46", "09:00", "14 min > 10 min"):
        assert fragment in STORY, f"docs/STORY.md no longer contains {fragment!r}"


def test_clock_constants_match_story(story):
    mod, _ = story
    assert mod.LINK_DOWN.strftime("%H:%M") == "13:00"
    assert mod.LINK_UP.strftime("%H:%M") == "19:00"
    assert mod.REPORT_TIME.strftime("%H:%M") == "14:20"
    assert mod.RESUME_REQUEST.strftime("%H:%M") == "09:00"
    # same calendar day for the cut, the report and the link restoration
    assert mod.LINK_DOWN.date() == mod.LINK_UP.date() == mod.REPORT_TIME.date()
    assert (mod.RESUME_REQUEST.date() - mod.REPORT_TIME.date()).days == 1


def test_freshness_limit_is_ten_minutes():
    assert Params().max_age_min == 10


def test_beat2_two_dimensions_away_opens_fatigue_procedure(story):
    _, caps = story
    d7 = by(caps, "daily", 7)
    assert d7["states"]["Body"] == "WATCH" and d7["states"]["Attention"] == "DEGRADED"
    assert d7["action"]["procedure_id"] == "PROC-FATIGUE-01"


def test_baseline_days_one_to_five_are_unknown(story):
    _, caps = story
    for day in (1, 3, 5):
        st = by(caps, "daily", day)["states"]
        assert {st["Body"], st["Attention"], st["Morale"]} == {"UNKNOWN"}


def test_beat3_chest_pain_is_critical_at_1410(story):
    _, caps = story
    em = by(caps, "emergency", 9)
    assert em["time_utc"] == "14:10"
    assert em["action"]["procedure_id"] == "PROC-EMERGENCY-01"
    assert em["action"]["criticality"] == "CRITICAL"


def test_beat4_report_created_1420_received_1920_exactly_once(story):
    _, caps = story
    q = by(caps, "emergency", 9)["send_queue"]
    assert q["report_created_utc"].endswith("14:20")
    assert q["report_received_utc"].endswith("19:20")
    assert q["ground_view_received_utc"].endswith("19:20")
    assert q["report_deliveries_to_ground"] == 1
    assert q["duplicates_dropped"] == 3
    assert q["ground_order_by_creation"] is True


def test_beat5_resume_refused_14_over_10_even_with_commander_override(story):
    _, caps = story
    r = by(caps, "resume", 10)
    assert r["action"]["type"] == "REFUSE_RESUME"
    assert r["gate_inputs"]["max_age_min"] == 10
    ages = {m["indicator_id"]: m["age_min"] for m in r["gate_inputs"]["measurements"]}
    assert ages["PH01"] == 14 and ages["PH01"] > r["gate_inputs"]["max_age_min"]
    # the gate itself refuses with an override present: the override never authorises a resume alone
    from csync.gate import resume_gate
    from datetime import datetime
    now = datetime.fromisoformat(r["gate_inputs"]["request_time_utc"])
    meas = [{"indicator_id": m["indicator_id"], "timestamp": datetime.fromisoformat(m["timestamp"]),
             "quality": m["quality"], "source": m["source"]} for m in r["gate_inputs"]["measurements"]]
    proc = {"prerequisites": [{"indicator_id": "PH01", "max_age_min": 10, "sources": ["GUIDED"]}],
            "override_policy": {"allowed": True}}
    decision, reasons = resume_gate(now, meas, proc, override={"by": "commander"})
    assert decision == "REFUSE_RESUME"
    assert any(re.match(r"G3: PH01 is stale \(14 min > 10 min\)", x) for x in reasons)


def test_fixed_medical_sentence_is_on_every_action():
    import json
    strings = json.load(open(os.path.join(ROOT, "csync", "config", "strings_en.json"), encoding="utf8"))
    assert strings["fixed_medical_sentence"] == "Follow the onboard medical checklist and the crew medical officer."
