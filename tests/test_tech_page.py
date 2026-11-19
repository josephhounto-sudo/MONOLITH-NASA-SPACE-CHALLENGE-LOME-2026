"""Technologies page and role entries: the page says only what the registry allows; both roles read the same capsule."""
import json
import os

from tests.helpers_app import open_app

from csync.tech import registry

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(ROOT + "/csync/config/strings_en.json", encoding="utf8") as _f:
    UI = json.load(_f)["ui"]
APP = ROOT + "/csync/ui/app.py"


def _text(at):
    return " ".join([m.value for m in at.markdown] + [c.value for c in at.caption] + [w.value for w in at.text] + [s.value for s in at.subheader])


def test_tech_page_shows_every_registry_status_and_data_label():
    at = open_app(APP, 40)
    at.sidebar.radio[0].set_value(UI["tab_tech"]).run()
    assert not at.exception
    txt = _text(at)
    reg = registry.load()
    for it in reg["items"]:
        assert it["name"] in txt and registry.label(reg, it) in txt
    assert "SIMULATED" in txt and UI["tech_building"] in txt


def test_tech_page_demos_run_and_tamper_is_detected():
    at = open_app(APP, 40)
    at.sidebar.radio[0].set_value(UI["tab_tech"]).run()
    assert UI["tech_sig_ok"] in _text(at)
    at.button(key="tech_tamper").click().run()
    assert "detected" in _text(at) and not at.exception


def test_changepoint_card_reports_both_alarms_honestly():
    at = open_app(APP, 40)
    at.sidebar.radio[0].set_value(UI["tab_tech"]).run()
    at.slider[0].set_value(9).run()
    txt = _text(at)
    assert "Fixed threshold first crossed on day 6." in txt
    assert "Cumulative-sum alarm on day 7." in txt   # later than the fixed threshold: the page must not claim otherwise


def test_both_roles_show_the_same_capsule_state_and_differ_only_in_order():
    crew = open_app(APP, 40)
    cmd = open_app(APP, 40)
    cmd.sidebar.radio[1].set_value(UI["role_cmd"]).run()
    assert not cmd.exception
    assert set(crew.sidebar.radio[0].options) == set(cmd.sidebar.radio[0].options)
    assert crew.sidebar.radio[0].options != cmd.sidebar.radio[0].options
    for w in ("Watch", "Degraded"):
        assert w in _text(crew) and w in _text(cmd)
