"""Pip stays on screen and leads the visitor: a line for every section, a Next button that really moves, fixed beta answers."""
import json
import os

from tests.helpers_app import open_app

from csync.language import banned_hits

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = ROOT + "/csync/ui/app.py"
with open(ROOT + "/csync/config/strings_en.json", encoding="utf8") as _f:
    UI = json.load(_f)["ui"]


def test_pip_has_one_short_clean_line_for_every_section_in_both_languages():
    for lang in ("en", "fr"):
        with open(f"{ROOT}/csync/config/strings_{lang}.json", encoding="utf8") as fh:
            ui = json.load(fh)["ui"]
        for k in [k for k in ui if k.startswith("tab_")]:
            line = ui["pip_say_" + k]
            assert len(line.split()) <= 18 and not banned_hits(line), (lang, k)
        for q, a in ui["pip_questions"]:
            assert not banned_hits(q + " " + a) and len(a.split()) <= 30


def test_next_button_moves_the_visitor_along_the_path():
    at = open_app(APP, 60)                       # demo story, Pip in its corner
    assert at.button(key="cs-pip-next")
    at.button(key="cs-pip-next").click().run()
    assert not at.exception and at.radio(key="cs-nav").value != UI["tab_home"]


def test_pip_can_be_made_small_and_comes_back():
    at = open_app(APP, 60)
    at.button(key="cs-pip-min-btn").click().run()
    assert at.button(key="cs-pip-open") and not at.exception
    at.button(key="cs-pip-open").click().run()
    assert at.button(key="cs-pip-next")
