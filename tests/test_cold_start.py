"""Cold clone: data/out/ is generated, not committed, so the hosted app starts without it (audit 2026-11-18: a visitor saw
"Capsule file not found ... Run: python scripts/run_story.py", and the trends panel silently vanished).

conftest.py builds data/out for the other tests, so this test points the app at an EMPTY folder instead.
"""
import json
import os
import re
import time

import pytest
from streamlit.testing.v1 import AppTest
from tests.helpers_app import open_app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "csync", "ui", "app.py")
UI = json.load(open(os.path.join(ROOT, "csync", "config", "strings_en.json"), encoding="utf8"))["ui"]
DEV_TEXT = re.compile(r"Run:|python scripts|scripts/run_story|not found|Traceback|FileNotFound|data/out", re.I)


@pytest.fixture(scope="module")
def cold_page(tmp_path_factory):
    empty = tmp_path_factory.mktemp("empty_out")
    os.environ["CSYNC_OUT_DIR"] = str(empty)
    try:
        t0 = time.time()
        at = open_app(APP, 120)
        at.first_render_seconds = time.time() - t0
        yield at, empty
    finally:
        os.environ.pop("CSYNC_OUT_DIR", None)


def all_visible_text(at):
    parts = [m.value for m in at.markdown] + [c.value for c in at.caption] + [w.value for w in at.warning]
    parts += [e.value for e in at.error] + [i.value for i in at.info] + [s.value for s in at.success]
    return "\n".join(parts)


def test_cold_start_renders_without_exception(cold_page):
    at, _ = cold_page
    assert not at.exception, at.exception
    assert any("SYNTHETIC DATA" in w.value for w in at.warning)


def test_no_developer_text_for_a_visitor(cold_page):
    at, _ = cold_page
    assert DEV_TEXT.search(all_visible_text(at)) is None, DEV_TEXT.search(all_visible_text(at))


def test_cold_start_does_not_write_into_the_repo_or_the_empty_folder(cold_page):
    _, empty = cold_page
    assert list(empty.iterdir()) == []          # the build goes to a temp folder, never into the configured folder


def test_trends_panel_present_on_cold_start(cold_page):
    at, _ = cold_page
    at.sidebar.radio[0].set_value(UI["tab_trends"]).run()
    assert UI["trend_title"] in [s.value for s in at.subheader], "the indicators-over-time panel vanished on a cold clone"


def test_cold_first_render_time_is_recorded_and_bounded(cold_page):
    at, _ = cold_page
    print(f"cold first render: {at.first_render_seconds:.1f} s")
    assert at.first_render_seconds < 60          # hosted app measured ~10 s of blank page on 2026-11-18; target < 5 s later


def test_navigation_opens_every_section_without_error(cold_page):
    at, _ = cold_page
    nav = at.sidebar.radio[0]
    assert nav.options[0] == UI["tab_home"], "the overall crew state must be the first entry"
    assert len(nav.options) == 11
    for opt in list(nav.options):
        at.sidebar.radio[0].set_value(opt).run()
        assert not at.exception, (opt, at.exception)
        assert DEV_TEXT.search(all_visible_text(at)) is None, opt


def test_cold_first_screen_is_the_hook_without_developer_text(cold_page):
    _, _ = cold_page
    at = AppTest.from_file(APP, default_timeout=120).run()
    assert not at.exception, at.exception
    assert UI["hook_title"] in [s.value for s in at.subheader]
    assert DEV_TEXT.search(all_visible_text(at)) is None
