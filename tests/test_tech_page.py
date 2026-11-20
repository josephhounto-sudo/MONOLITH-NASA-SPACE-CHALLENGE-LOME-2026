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


def _tech(group=None):
    at = open_app(APP, 60, section=UI["tab_tech"])
    if group:
        at.segmented_control(key="tech_group").set_value(UI[group]).run()
    assert not at.exception, at.exception
    return at


def test_tech_page_shows_every_registry_status_and_data_label():
    reg = registry.load()
    txt = " ".join(_text(_tech(g)) for g in ("tech_g_measure", "tech_g_decide", "tech_g_deliver"))
    for it in reg["items"]:
        assert it["name"] in txt and registry.label(reg, it) in txt
    assert "SIMULATED" in txt and "REAL" in txt


def test_tech_page_demos_run_and_tamper_is_detected():
    at = _tech("tech_g_deliver")
    assert UI["tech_sig_ok"] in _text(at)
    at.button(key="tech_tamper").click().run()
    assert "detected" in _text(at) and not at.exception


def test_changepoint_card_reports_both_alarms_honestly():
    at = _tech()
    txt = _text(at)
    assert "Fixed threshold first crossed on day 6." in txt
    assert "Cumulative-sum alarm on day 7." in txt   # later than the fixed threshold: the page must not claim otherwise


def test_both_roles_show_the_same_capsule_state_and_differ_only_in_order():
    crew = open_app(APP, 40)
    cmd = open_app(APP, 40)
    cmd.radio(key="cs-role").set_value(UI["role_cmd"]).run()
    assert not cmd.exception
    assert set(cmd.radio(key="cs-nav").options) - set(crew.radio(key="cs-nav").options) == {UI["tab_cmd"]}   # board: commander only
    for w in ("Watch", "Degraded"):
        assert w in _text(crew) and w in _text(cmd)


def test_body_map_box_zones_carry_their_names():
    from csync import silhouette
    svg = silhouette.svg(None)
    assert ">Habitat</text>" in svg and ">Whole body</text>" in svg   # no unlabeled box on the figure


def test_every_technology_can_be_touched_and_the_explainer_blocks_an_invented_number():
    at = _tech()
    assert UI["tech_ex_block"].split("{")[0] in _text(at)          # the default sentence carries an invented number
    at.text_input(key="tech_ex_mine").set_value("Day 9.").run()
    assert UI["tech_ex_pass"] in _text(at)
    at = _tech("tech_g_deliver")
    at.slider(key="tech_dtn_loss").set_value(30).run()
    assert not at.exception and "Data: NONE" not in _text(at)
