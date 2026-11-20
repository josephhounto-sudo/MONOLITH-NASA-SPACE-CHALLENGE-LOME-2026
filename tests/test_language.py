"""French for the local lead and the testers: same keys in both files, and switching language keeps the visitor's place."""
import json
import os

from tests.helpers_app import open_app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = ROOT + "/csync/ui/app.py"


def _ui(lang):
    with open(f"{ROOT}/csync/config/strings_{lang}.json", encoding="utf8") as fh:
        return json.load(fh)["ui"]


def test_switching_to_french_keeps_the_section_and_shows_french():
    en, fr = _ui("en"), _ui("fr")
    at = open_app(APP, 60, section=en["tab_tech"])
    at.radio(key="cs-lang").set_value("Français").run()
    assert not at.exception, at.exception
    assert at.radio(key="cs-nav").value == fr["tab_tech"]
    assert fr["tech_title"] in [s.value for s in at.subheader]


def test_every_section_opens_in_french():
    fr = _ui("fr")
    at = open_app(APP, 90, section=None)
    at.radio(key="cs-lang").set_value("Français").run()
    for opt in at.radio(key="cs-nav").options:
        at.radio(key="cs-nav").set_value(opt).run()
        assert not at.exception, (opt, at.exception)
    assert fr["tab_live"] in at.radio(key="cs-nav").options
