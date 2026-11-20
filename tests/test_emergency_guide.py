"""Emergency guide. Pre-mortem: (1) a step with no source; (2) a treatment or drug slips in; (3) the time-to-490 mmHg
arithmetic is wrong or alarms on a rising pressure; (4) a case is unreachable in the app; (5) the fixed sentence is missing."""
import os
import re

import pytest

from csync import emergency_guide as eg

APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csync", "ui", "app.py")
FORBIDDEN = re.compile(r"\bcause\b|diagnos|\bproves?\b|guarantee|disease|\bdose\b|\bmg\b|tablet|inject|aspirin|nitro", re.I)


def test_every_step_has_a_known_source_and_no_treatment_word():
    g = eg.load()
    assert {c["id"] for c in g["cases"]} >= {"medical", "depress", "fire", "toxic", "co2"}
    for c in g["cases"]:
        for s in c["steps"]:
            assert s["src"] in g["sources"]
            assert not FORBIDDEN.search(s["text"]), (c["id"], s["text"])


def test_time_to_reserve_matches_hand_arithmetic():
    assert eg.time_to_reserve(752, 748, 1) == pytest.approx(64.5)   # (748 - 490) / 4
    assert eg.time_to_reserve(500, 495, 1) == pytest.approx(1.0)
    assert eg.time_to_reserve(748, 752, 1) is None                    # rising pressure: no leak
    assert eg.time_to_reserve(495, 480, 1) == 0.0
    with pytest.raises(ValueError):
        eg.time_to_reserve(750, 748, 0)


def test_every_case_opens_in_the_app_with_the_fixed_sentence():
    import json
    with open(os.path.join(os.path.dirname(APP), "..", "config", "strings_en.json"), encoding="utf8") as fh:
        S = json.load(fh)
    from streamlit.testing.v1 import AppTest
    for cid in ("medical", "depress", "fire", "toxic", "co2"):
        at = AppTest.from_file(APP, default_timeout=60)
        at.session_state["cs-bot-done"] = True
        at.session_state["cs-nav"] = S["ui"]["tab_emergency"]
        at.session_state["cs-em-case"] = cid
        at.run()
        assert not at.exception, (cid, at.exception)
        case = next(c for c in eg.load()["cases"] if c["id"] == cid)
        md = " ".join(m.value for m in at.markdown)
        assert case["steps"][0]["text"] in md and case["trigger"] in md, cid
        assert any(S["fixed_medical_sentence"] in i.value for i in at.info)
