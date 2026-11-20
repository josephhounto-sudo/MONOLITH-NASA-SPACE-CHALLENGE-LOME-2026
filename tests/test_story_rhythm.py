"""Simulated heart rhythm tied to the story, and the two role views."""
import json
import os

import pytest
from tests.helpers_app import open_app

from csync.physio import hrv
from csync.ui import widgets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(ROOT + "/csync/config/strings_en.json", encoding="utf8") as _f:
    UI = json.load(_f)["ui"]
APP = ROOT + "/csync/ui/app.py"


def _md(at):
    return " ".join([m.value for m in at.markdown] + [c.value for c in at.caption] + [t.value for t in at.text])


def test_story_rhythm_is_simulated_and_falls_as_distance_rises():
    vals = [hrv.story_rhythm(7, d)["rmssd"] for d in (0.0, 1.0, 2.0, 3.0, 4.0)]
    assert all(a > b for a, b in zip(vals, vals[1:], strict=False)), vals
    r = hrv.story_rhythm(7, 2.93)
    assert r["simulated"] is True and 0 < r["stress"] <= 1


def test_story_rhythm_rejects_bad_day_and_clips_distance():
    with pytest.raises(ValueError):
        hrv.story_rhythm(0, 1.0)
    assert hrv.story_rhythm(3, -5)["stress"] == 0.0 and hrv.story_rhythm(3, 99)["stress"] == 0.5


def test_curve_without_threshold_has_text_alternative_and_no_threshold_line():
    ch = {"threshold": "#fff", "value": "#fff", "flagged": "#f00", "ink": "#fff", "baseline": "#fff", "flag_line": "#f00", "ring": "#000"}
    rows = [{"day": d, "value": 40 - d, "flagged": False} for d in range(1, 6)]
    md = widgets.curve_image(rows, 38.0, None, "RMSSD", ch, "Mission day")
    assert "no threshold" in md and "nan" not in md.lower()


def test_rhythm_panel_is_labelled_simulated_context_and_changes_no_state():
    at = open_app(APP, 40)
    at.slider[0].set_value(7).run()
    assert not at.exception
    txt = _md(at)
    assert UI["rhythm_title"] in txt and UI["rhythm_note"] in txt
    states_before = [m.value for m in at.markdown if "Degraded" in m.value][:1]
    at.slider[0].set_value(7).run()
    assert [m.value for m in at.markdown if "Degraded" in m.value][:1] == states_before


def test_commander_sees_decision_before_state_cards_and_crew_the_reverse():
    crew, cmd = open_app(APP, 40), open_app(APP, 40)
    for at in (crew, cmd):
        at.slider[0].set_value(7).run()
    cmd.sidebar.radio[1].set_value(UI["role_cmd"]).run()
    assert not cmd.exception

    def order(at):
        items = [m.value for m in at.markdown]
        pos = lambda key: next(i for i, v in enumerate(items) if key in v)
        return pos("cs-card"), pos(UI["action_label"])

    # commander: the proposed action comes before the first state card; crew: after
    c_card, c_act = order(cmd)
    k_card, k_act = order(crew)
    assert c_act < c_card and k_act > k_card
    assert UI["crew_own"] in _md(crew) and UI["crew_own"] not in _md(cmd)


def test_rhythm_drop_is_moderate_on_day_7():
    base = hrv.story_rhythm(1, 0.0)["rmssd"]
    assert 0.5 * base < hrv.story_rhythm(7, 2.93)["rmssd"] < base   # illustrative, not a collapse
