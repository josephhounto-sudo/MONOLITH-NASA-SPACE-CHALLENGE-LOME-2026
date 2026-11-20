"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

M3-1..M3-3: headless checks of the Streamlit screens (streamlit.testing). A human still has to look at the screens."""
import json
import os
import re

import pytest
from streamlit.testing.v1 import AppTest
from tests.helpers_app import open_app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "csync", "ui", "app.py")
CFG = os.path.join(ROOT, "csync", "config")
STRINGS = json.load(open(os.path.join(CFG, "strings_en.json"), encoding="utf8"))
THEME = json.load(open(os.path.join(CFG, "theme.json"), encoding="utf8"))
UI = STRINGS["ui"]
CONTEXT = ("Mission",)      # Habitat is computed from real NASA data since V2 (decision P6)
# Daily capsules of the story (seed 42, drift_amp 2.5): evaluated states; Mission stays UNKNOWN (context only);
# Habitat is computed from real NASA ISS cabin CO2 against the NASA 3 mmHg requirement (story days 9-10 are above it).
DAY7 = {"Body": "WATCH", "Attention": "DEGRADED", "Morale": "NORMAL", "Mission": "UNKNOWN", "Habitat": "NORMAL"}
DAY9 = {**DAY7, "Habitat": "WATCH"}
DAY10 = {"Body": "NORMAL", "Attention": "NORMAL", "Morale": "NORMAL", "Mission": "UNKNOWN", "Habitat": "WATCH"}


def page(day):
    at = open_app(APP, 60)
    at.slider[0].set_value(day).run()
    assert not at.exception, at.exception
    return at


ICO = "(?:<svg class='cs-ico'(?:(?!</div>).)*?</svg>)?"   # state icons are inline SVG, followed by the state word; never spans two cards


def html(at):
    return " ".join(m.value for m in at.markdown)


def test_banner_always_shown():
    at = page(7)
    assert any("SYNTHETIC DATA" in w.value for w in at.warning)


def test_day7_attention_degraded():
    h = html(page(7))
    assert re.search(r">Attention</div><div[^>]*>"+ICO+r" Degraded<", h)


@pytest.mark.parametrize("day", [1, 3, 5])
def test_baseline_days_never_normal(day):
    h = html(page(day))
    for dim in ("Body", "Attention", "Morale"):
        assert re.search(rf">{dim}</div><div[^>]*>"+ICO+rf" Personal baseline being built \(day {day} of 5\)<", h)
        assert not re.search(rf">{dim}</div><div[^>]*>"+ICO+r" Normal", h)      # crew dimensions only; Habitat has its own data


def test_mission_is_context_only_and_never_normal():
    h = html(page(8))
    assert re.search(r">Mission</div><div[^>]*>"+ICO+r" Context only", h)


@pytest.mark.parametrize("day,word", [(1, "Unknown"), (3, "Normal"), (9, "Watch")])
def test_habitat_card_shows_the_computed_state_not_the_personal_baseline_message(day, word):
    h = html(page(day))
    assert re.search(rf">Habitat</div><div[^>]*>"+ICO+rf"[^<]*{word}<", h), (day, word)
    assert not re.search(r">Habitat</div><div[^>]*>"+ICO+r"[^<]*baseline being built", h)


def test_day9_six_steps_and_send_queue():
    at = page(9)
    seen = []
    for _ in range(6):
        seen.append(next(m.value for m in at.markdown if m.value.startswith("**Step ")))
        nxt = next(b for b in at.button if b.label == "Next" and b.key != "beat-next")
        if nxt.disabled:
            break
        nxt.click().run()
    assert [s.split("**")[1] for s in seen] == [f"Step {n} of 6" for n in range(1, 7)]
    assert any("Follow the onboard medical checklist" in i.value for i in at.info)
    assert any("Waiting for link" in w.value for w in at.warning)
    at.radio[0].set_value(at.radio[0].options[1]).run()
    assert any(s.value == "Delivered to ground (once)" for s in at.success)


def test_day9_guided_values_shown_without_threshold():
    at = page(9)
    for _ in range(2):
        next(b for b in at.button if b.label == "Next" and b.key != "beat-next").click().run()
    h = html(at)
    assert "104" in h and "142 / 91" in h and "36.9" in h and "112" in h
    assert h.count("No NASA in-flight reference") == 2         # body temperature, blood glucose
    assert "risk-of-cardiovascular-adaptations" in h
    assert "Source to be added" not in h and "TODO" not in h


def test_day10_resume_refused_even_with_override():
    at = page(10)
    assert "REFUSE_RESUME" not in html(at)            # the decision is revealed only by the button (pitch moment)
    next(b for b in at.button if b.label == "Request resume").click().run()
    h = html(at)
    assert "Gate decision: REFUSE_RESUME" in h
    assert "The heart-rate reading is 14 min old; the limit is 10 min." in h
    assert "G3" not in h                                      # the code stays in the technical log
    assert any(t.value == "G3: PH01 is stale (14 min > 10 min)" for t in at.text)
    next(b for b in at.button if b.label == "Commander override").click().run()
    h = html(at)
    assert "Gate decision: REFUSE_RESUME" in h
    assert any("Commander override logged. Decision unchanged: REFUSE_RESUME" in t.value for t in at.text)
    assert "A Commander override was logged. It cannot authorise a resume on its own." in html(at)


def test_no_hardcoded_colours_in_app():
    src = open(APP, encoding="utf8").read()
    assert not re.search(r"#[0-9A-Fa-f]{6}\b", src)


def dimension_label(dim, state):
    if dim in CONTEXT:
        return UI["context_only"]
    return STRINGS["states"][state]


def assert_dimensions(h, states):
    """Each card uses the icon, word and colour stored in theme.json / strings_en.json."""
    allowed = {THEME["surface"], THEME["panel"], THEME["text"], THEME["text_secondary"], THEME["interactive"]}
    allowed.update(s["color"] for s in THEME["state"].values())
    for colour in re.findall(r"#[0-9A-Fa-f]{6}", h):
        assert colour in allowed, colour
    for dim, state in states.items():
        look = THEME["state"][state]
        label = dimension_label(dim, state)
        assert re.search(
            rf">{dim}</div><div style='color:{look['color']};font-size:1.1em'><svg class='cs-ico'[^>]*aria-hidden='true'[^>]*>.*?</svg> {re.escape(label)}<",
            h,
        ), dim


def assert_synthetic(at):
    assert any(STRINGS["synthetic_banner"] in w.value for w in at.warning)


def test_screen_nominal_day7():
    at = page(7)
    h = html(at)
    assert_synthetic(at)
    assert any(s.value.startswith("Day 7:") for s in at.subheader)
    assert_dimensions(h, DAY7)


def test_screen_action_day9():
    at = page(9)
    h = html(at)
    assert_synthetic(at)
    assert UI["emergency_title"] in h
    assert_dimensions(h, DAY9)
    assert any(m.value.startswith(f"**{UI['step_counter'].format(n=1, total=6)}**") for m in at.markdown)


def test_screen_resume_refused_day10():
    at = page(10)
    assert_synthetic(at)
    assert UI["resume_title"] in html(at)
    assert_dimensions(html(at), DAY10)
    next(b for b in at.button if b.label == UI["request_resume"]).click().run()
    h = html(at)
    reason = STRINGS["gate_reasons"]["G3"].format(name=STRINGS["indicator_names"]["PH01"], age=14, limit=10)
    assert reason in h
    assert "heart-rate" in h and "14 min old" in h and "limit is 10 min" in h


def test_daily_proposal_can_be_accepted_or_declined_by_a_human():
    import json as _j
    ui = _j.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    at = open_app(APP, 60)
    at.slider[0].set_value(7).run()
    labels = [b.label for b in at.button]
    assert ui["btn_accept"] in labels and ui["btn_decline"] in labels
    next(b for b in at.button if b.label == ui["btn_decline"]).click().run()
    assert any("Declined on day 7" in s.value for s in at.success)
    assert ui["btn_accept"] not in [b.label for b in at.button], "buttons must disappear once a human has decided"


def _story_cold():
    """V3: the app opens on the live console; the drift story (with its hook) is the Demo story section."""
    from tests.helpers_app import STORY_TAB
    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["cs-nav"] = STORY_TAB
    at.session_state["cs-bot-done"] = True
    return at.run()


def test_opening_hook_shows_the_day_9_problem_once_then_moves_to_day_7():
    import json as _j
    ui = _j.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    at = _story_cold()
    assert ui["hook_title"] in [s.value for s in at.subheader]
    assert "14:10" in ui["hook_text"] and "13:00 to 19:00" in ui["hook_text"] and "19:20" in ui["hook_text"]
    assert not at.slider, "the first screen is the problem and one button: no day-7 panel under a day-9 hook"
    assert any("SYNTHETIC DATA" in w.value for w in at.warning), "the synthetic notice stays on the first screen"
    next(b for b in at.button if b.label == ui["hook_button"]).click().run()
    assert ui["hook_title"] not in [s.value for s in at.subheader]
    assert at.slider[0].value == 3          # the story restarts at beat 1, day 3


def test_story_beats_walk_the_frozen_days_in_order():
    import json as _j
    ui = _j.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    at = _story_cold()
    next(b for b in at.button if b.label == ui["hook_button"]).click().run()
    seen = [(at.slider[0].value)]
    for _ in range(5):
        nxt = next(b for b in at.button if b.label == ui["story_next"])
        if nxt.disabled:
            break
        nxt.click().run()
        assert not at.exception, at.exception
        seen.append(at.slider[0].value)
    assert seen == [3, 7, 9, 9, 10, 10]
    assert next(b for b in at.button if b.label == ui["story_next"]).disabled, "no step after the last beat"
    assert any(ui["beat6_title"] in m.value for m in at.markdown)


def test_why_panel_reads_the_committed_research_numbers():
    import json as _j
    ui = _j.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    at = open_app(APP, 60)
    at.sidebar.radio[0].set_value(ui["tab_why"]).run()
    assert not at.exception, at.exception
    md = " ".join(m.value for m in at.markdown)
    fp = _j.load(open(ROOT + "/research/fixed_vs_personal_results.json", encoding="utf8"))
    assert f"{fp['f=2']['drift']['B_personal_2ind']['pct']:.1f} %" in md      # shown number = file number
    assert f"{fp['f=2']['drift']['C_fixed']['pct']:.1f} %" in md
    assert "SIMULATED" in " ".join(c.value for c in at.caption)


def test_step5_shows_the_refusal_without_pressing_the_button():
    import json as _j
    ui = _j.load(open(ROOT + "/csync/config/strings_en.json", encoding="utf8"))["ui"]
    at = _story_cold()
    next(b for b in at.button if b.label == ui["hook_button"]).click().run()
    for _ in range(4):
        next(b for b in at.button if b.label == ui["story_next"]).click().run()
    assert not at.exception, at.exception
    assert any("REFUSE_RESUME" in m.value for m in at.markdown), "step 5 must show the gate answer"
    # before step 5 nothing was decided for the visitor
    at2 = _story_cold()
    next(b for b in at2.button if b.label == ui["hook_button"]).click().run()
    assert "resume_result" not in at2.session_state


def test_hook_draws_the_clock_from_the_capsule_not_from_typed_numbers():
    ui = json.load(open(os.path.join(CFG, "strings_en.json"), encoding="utf8"))["ui"]
    at = _story_cold()
    h = html(at)
    assert "cs-hooktl" in h and "5 h 10 min" in h and "14:10" in h and "19:20" in h and ui["hook_tl_ground"] in h
    assert "role='img'" in h, "the drawing has a text alternative"


def test_indicator_card_day7_is_real_markup_with_text_alternative():
    """The watch-style card (reaction time, day 7) shows the capsule's state, an <img> with alt text, and never raw markdown or base64 as visible text."""
    at = page(7)
    cards = [m.value for m in at.markdown if "class='cs-ind'" in m.value]
    assert len(cards) == 1, "exactly one indicator card on day 7"
    h = cards[0]
    assert "data-state='DEGRADED'" in h, "reaction time belongs to Attention, DEGRADED on day 7"
    assert "Reaction time" in h and "Degraded" in h, "name and state word are written"
    assert re.search(r"<img src='data:image/svg\+xml;base64,[A-Za-z0-9+/=]+' alt='[^']{20,}'>", h), "history drawing is an <img> with an alt text"
    assert "![" not in h, "markdown image syntax would show as raw text inside an HTML block"
    assert "304" in h and "ms" in h, "last value and unit"


def test_no_indicator_card_while_baseline_builds():
    """Days 1 to 5: nothing is flagged and the baseline is still being built, so no card and no empty frame."""
    at = page(3)
    assert not [m for m in at.markdown if "class='cs-ind'" in m.value]
