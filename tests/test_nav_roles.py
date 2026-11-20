"""Joseph (20/11): 'the commander board shows up at crew level'. The commander board is in the commander's navigation only;
switching back to crew from the board must not crash and lands on the live station."""
import json
import os

from tests.helpers_app import open_app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(ROOT + "/csync/config/strings_en.json", encoding="utf8") as _f:
    UI = json.load(_f)["ui"]
APP = ROOT + "/csync/ui/app.py"


def test_crew_navigation_has_no_commander_board_and_commander_has_it():
    crew = open_app(APP, 60, section=None)
    assert UI["tab_cmd"] not in crew.radio(key="cs-nav").options
    crew.radio(key="cs-role").set_value(UI["role_cmd"]).run()
    assert UI["tab_cmd"] in crew.radio(key="cs-nav").options and not crew.exception


def test_leaving_the_commander_role_from_the_board_lands_on_the_live_station():
    at = open_app(APP, 60, section=None)
    at.radio(key="cs-role").set_value(UI["role_cmd"]).run()
    at.radio(key="cs-nav").set_value(UI["tab_cmd"]).run()
    at.radio(key="cs-role").set_value(UI["role_crew"]).run()
    assert not at.exception and at.radio(key="cs-nav").value == UI["tab_live"]


def test_every_section_sits_in_exactly_one_group_for_both_roles():
    with open(APP, encoding="utf8") as fh:
        src = fh.read()
    body = src[src.index("def nav_groups"):src.index("def plain")]
    ns = {}
    exec(compile(body, "nav_groups", "exec"), ns)   # pure function, no Streamlit needed
    for cmd in (True, False):
        keys = [k for _g, ks in ns["nav_groups"](cmd) for k in ks]
        assert len(keys) == len(set(keys)) and all(k in UI for k in keys)
        assert ("tab_cmd" in keys) == cmd
