"""Body map: the 8 zones, honest status, preselected symptom zone, no banned words."""
import re

import pytest
from streamlit.testing.v1 import AppTest

from csync import silhouette
from csync.language import banned_hits

ROOT = silhouette.ROOT


def test_eight_zones_match_the_sheets():
    assert set(silhouette.fiches()) == set(silhouette.SHAPES) and len(silhouette.SHAPES) == 8


def test_unmeasured_zones_are_never_measured_status():
    f = silhouette.fiches()
    for rid in ("region-abdomen", "region-legs"):
        assert f[rid]["status"] == "unknown"
        assert 'stroke-dasharray' in silhouette.svg(None)   # unknown and context zones are dashed
    assert f["region-habitat"]["status"] == "context"


def test_svg_has_no_face_no_external_resource_and_marks_selection():
    s = silhouette.svg("region-chest")
    assert "http" not in s.replace("http://www.w3.org/2000/svg", "") and "<image" not in s
    assert "selected: Chest" in s and silhouette.THEME["interactive"] in s


def test_sheet_texts_have_no_banned_words():
    text = " ".join(str(v) for r in silhouette.fiches().values() for v in r.values() if isinstance(v, str))
    assert banned_hits(text) == []


def test_symptom_zone_mapping():
    assert silhouette.region_for_zone("thorax") == "region-chest" and silhouette.region_for_zone("x") is None


@pytest.mark.parametrize("day,preselected", [(7, None), (9, "region-chest")])
def test_app_shows_body_map_and_preselects_symptom_zone(day, preselected):
    at = AppTest.from_file(ROOT + "/csync/ui/app.py", default_timeout=30).run()
    at.slider[0].set_value(day).run()
    assert not at.exception
    assert any("Body map" in s.value for s in at.subheader)
    pills = [w for w in at.main if type(w).__name__ == "ButtonGroup"] or at.get("button_group")
    assert pills, "zone selector missing"
    value = pills[0].value
    assert (value == preselected) if preselected else (value in (None, []))


def test_selecting_a_zone_shows_how_why_when():
    at = AppTest.from_file(ROOT + "/csync/ui/app.py", default_timeout=30).run()
    at.get("button_group")[0].set_value("region-head").run()
    md = " ".join(m.value for m in at.markdown)
    assert "How it is measured" in md and "Why it matters" in md and "When C-Sync alerts" in md
