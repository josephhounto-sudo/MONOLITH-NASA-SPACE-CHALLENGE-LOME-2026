"""Indicator charts: values, baseline and threshold come from the rule engine, not from the UI."""
import json
import os

import pytest
from streamlit.testing.v1 import AppTest
from tests.helpers_app import open_app

from csync.language import banned_hits
from csync.rules import DIRECTION, Params, daily_values, evaluate
from synthetic.generator import generate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def trends():
    return json.load(open(ROOT + "/data/out/trends_histoire.json", encoding="utf8"))["indicators"]


def test_trends_match_the_engine(trends):
    df = generate("histoire", seed=42, drift_amp=2.5, fast=True)
    dv = daily_values(df)
    z, flags, _, _, ref = evaluate(dv)
    for ind, t in trends.items():
        assert t["baseline_mean"] == pytest.approx(float(ref["mu"][ind]), abs=1e-3)
        want = float(ref["mu"][ind]) + DIRECTION[ind] * Params().d_threshold * float(ref["sd_eff"][ind])
        assert t["threshold"] == pytest.approx(want, abs=1e-3)
        assert [r["flagged"] for r in t["days"]] == [bool(x) for x in flags[ind]]
        assert [r["value"] for r in t["days"] if r["value"] is not None] == [round(float(v), 2) for v in dv[ind].dropna()]


def test_sleep_drift_is_visible_from_day_7(trends):
    days = {r["day"]: r for r in trends["PH09"]["days"]}
    assert not any(days[d]["flagged"] for d in range(1, 7)) and all(days[d]["flagged"] for d in (7, 8, 9))


def test_strings_have_no_banned_words():
    ui = json.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    text = json.dumps({k: v for k, v in ui.items() if k.startswith(("trend", "hazard"))}, ensure_ascii=False)
    assert banned_hits(text) == []


def test_hazard_table_names_the_five_nasa_hazards():
    ui = json.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    names = [r["hazard"].lower() for r in ui["hazard_rows"]]
    assert names == ["space radiation", "isolation and confinement", "distance from earth", "gravity fields",
                     "hostile closed environments"]
    assert any("not measured" in r["status"].lower() for r in ui["hazard_rows"])   # never shown as fine


def test_app_shows_chart_up_to_the_chosen_day_only():
    at = open_app(ROOT + "/csync/ui/app.py", 40)
    at.sidebar.radio[0].set_value("Trends").run()
    at.slider[0].set_value(7).run()
    assert not at.exception
    md = " ".join(m.value for m in at.markdown)
    assert "Flagged days up to day 7: 7." in md
    at.slider[0].set_value(4).run()
    assert "No flagged day up to day 4." in " ".join(m.value for m in at.markdown)


def test_countermeasures_panel_cites_sources_and_gives_no_advice():
    at = open_app(ROOT + "/csync/ui/app.py", 30)
    at.sidebar.radio[0].set_value("NASA hazards and countermeasures").run()
    assert not at.exception
    assert any("countermeasures" in s.value for s in at.subheader)
    rows = json.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]["cm_rows"]
    assert all(r["source"] and "NASA" in r["source"] or "NTRS" in r["source"] for r in rows)
    text = " ".join(" ".join(r.values()) for r in rows)
    assert "does not" in rows[0]["csync"].lower() or "no recommendation" in rows[0]["csync"].lower()
    assert banned_hits(text) == []
