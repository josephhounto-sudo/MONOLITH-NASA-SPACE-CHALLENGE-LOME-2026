"""3D body. Pre-mortem: (1) an unknown zone drawn like a measured one; (2) an unexpected status drawn as measured;
(3) WebGL missing leaves a blank frame; (4) a selected zone id that does not exist; (5) the zone map drifts from the sheets."""
import json
import os
import shutil
import subprocess

import pytest

from csync import silhouette
from csync.ui import body3d

JS = os.path.join(os.path.dirname(body3d.__file__), "assets", "body3d.js")
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")


def _node(expr):
    code = f"const B=require({json.dumps(JS)});process.stdout.write(JSON.stringify({expr}));"
    return json.loads(subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True, timeout=30).stdout)


@needs_node
def test_unknown_zones_are_faded_and_never_look_measured():
    m, u = _node("B.zoneLook('measured', false)"), _node("B.zoneLook('unknown', false)")
    assert m["opacity"] == 1 and u["opacity"] < 0.5 and u["color"] != m["color"]
    assert _node("B.zoneLook('surprise', false)") == u
    assert _node("B.zoneLook('unknown', true)")["emissive"] == _node("B.SELECTED_GLOW")


@needs_node
def test_every_body_region_of_the_sheets_has_parts_in_3d():
    drawn = set(_node("Object.keys(B.PARTS)"))
    regions = set(silhouette.fiches()) - {"region-body", "region-habitat"}   # those two are drawn on the floor
    assert regions == drawn


def test_viewer_page_carries_the_fallback_and_the_pinned_engine():
    page = body3d.viewer_html("region-chest", "Selected zone: Chest", "Drag to turn")
    assert "three@0.187.0" in page and "<svg" in page and "region-chest" in page
    assert "importmap" in page and "CesiumMan.glb" in page and "CC BY 4.0" in page   # licence credit shown with the model
    with pytest.raises(AssertionError):
        body3d.viewer_html("region-tail", "x", "y")


@needs_node
def test_model_zones_cover_every_band_and_match_the_sheets():
    z = lambda ax, y: _node(f"B.zoneOf({ax},{y})")   # noqa: E731
    assert [z(0, .9), z(.05, .7), z(.2, .6), z(.35, .55), z(.05, .5), z(.07, .2)] == [
        "region-head", "region-chest", "region-arm", "region-hand", "region-abdomen", "region-legs"]
    assert set(_node("B.ZONE_IDS")) == set(silhouette.fiches()) - {"region-body", "region-habitat"}
