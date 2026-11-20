"""V3: live console, guide bot, Bookings look.

Pre-mortem (each line has a test below):
1. A frozen or stale feed is shown as a fresh value -> readingState says Unknown or Check, never Live.
2. Feed units change (psi instead of mmHg) and the values become absurd -> unitMode decides from cabin pressure, unknown hides values.
3. A live CO2 reading is presented as a decision -> the text says context only and cites the 1-hour limit.
4. The bot says a forbidden word or grows into a long lecture -> every UI string is checked; six steps at most.
5. A sidebar entry has no icon, or an icon file is missing on a cold start -> every nav key maps to a vendored Lucide file.
"""
import json
import os
import re
import shutil
import subprocess

import pytest

from csync.ui import bookings, bot, live

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(ROOT, "csync", "ui", "assets", "live.js")


def _ui(lang):
    with open(os.path.join(ROOT, "csync", "config", f"strings_{lang}.json"), encoding="utf8") as fh:
        return json.load(fh)["ui"]


UI_EN, UI_FR = _ui("en"), _ui("fr")
FORBIDDEN = re.compile(r"\bcause\b|diagnos|\bproves?\b|guarantee|disease", re.I)

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")


def _node(expr):
    code = f"const L=require({json.dumps(JS)});process.stdout.write(JSON.stringify({expr}));"
    return json.loads(subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True, timeout=30).stdout)


@needs_node
def test_reading_states_never_show_a_stale_or_frozen_value_as_live():
    now = 10_000_000
    # the feed only sends changes: a quiet value with the station clock ticking is Live, not stale
    live = _node(f"L.readingState(2.4, {now - 2000}, {now - 20 * 60000}, {now})")
    assert live["word"] == "Live" and live["show"]
    lost = _node(f"L.readingState(2.4, {now - 5 * 60000}, {now - 5000}, {now})")
    assert lost["word"] == "Unknown" and not lost["show"], "after signal loss the last value is hidden, never shown as fresh"
    assert _node(f"L.readingState(2.4, {now - 2000}, {now - 61 * 60000}, {now})")["word"] == "Check"
    assert _node(f"L.readingState(2.4, null, {now}, {now})")["word"] == "Unknown"
    assert _node(f"L.readingState(null, {now}, {now}, {now})")["word"] == "Unknown"


@needs_node
def test_units_are_decided_from_cabin_pressure():
    assert _node("L.unitMode(751.9)") == "mmhg"
    assert _node("L.unitMode(14.5)") == "psi"
    assert _node("L.unitMode(0)") == "unknown"
    assert _node("L.toMmhg(2.4, 'unknown')") is None
    assert abs(_node("L.toMmhg(1, 'psi')") - 51.7149) < 1e-6
    assert abs(_node("L.o2Percent(165.85, 751.89)") - 22.06) < 0.01


@needs_node
def test_live_co2_is_context_against_the_one_hour_limit():
    above, below = _node("L.co2Context(3.2)"), _node("L.co2Context(2.4)")
    assert "above" in above and "below" in below
    assert "context only" in above and "1-hour limit of 3 mmHg" in above
    assert _node("L.deltaText(2.44)") == "\u2193 0.56 under limit" and _node("L.deltaText(3.2)") == "\u2191 0.20 over limit"


@needs_node
def test_clocks_use_the_mission_time_zones():
    assert _node("L.ZONES.map(z => z[1])") == ["UTC", "America/Chicago", "Europe/Moscow", "Africa/Lome"]
    assert _node("L.clockText(new Date(Date.UTC(2026,10,20,6,0,0)), 'UTC')") == "06:00:00"
    assert _node("L.clockText(new Date(Date.UTC(2026,10,20,6,0,0)), 'Africa/Lome')") == "06:00:00"


def test_console_page_has_every_card_the_clocks_and_the_pinned_client():
    page = live.console_html(UI_EN)
    for key, *_ in live.CARDS:
        assert f"id='v-{key}'" in page and f"id='s-{key}'" in page
    assert page.count("id='clk") == 4
    assert "lightstreamer-client-web@9.2.3" in page
    assert UI_EN["live_source"].split(".")[0] in page


def test_physiology_channels_say_their_honest_status():
    h = live.physiology_html(UI_EN)
    assert UI_EN["live_simulated"] in h and UI_EN["live_in_dev"] in h
    assert "nothing recorded" in UI_EN["live_phys_blink_note"]


@pytest.mark.parametrize("ui", [UI_EN, UI_FR])
def test_no_forbidden_word_in_any_ui_string(ui):
    for k, v in ui.items():
        for text in (v if isinstance(v, list) else [v]):
            if isinstance(text, str):
                assert not FORBIDDEN.search(text), (k, text)


def test_bot_tutorial_is_short_and_speaks_in_one_breath():
    for ui in (UI_EN, UI_FR):
        assert 1 <= len(ui["bot_steps"]) <= 6
        assert all(len(s.split()) <= 22 for s in ui["bot_steps"])
    html = bot.bubble(UI_EN, UI_EN["bot_steps"][0], "Step 1 of 6")
    assert "<img" in html and "Pip" in html and "<svg" not in html   # st.html strips inline svg


def test_every_sidebar_entry_has_a_vendored_icon():
    keys = ["tab_live", "tab_home", "tab_cmd", "tab_body", "tab_env", "tab_trends", "tab_tech", "tab_scale", "tab_why", "tab_nasa", "tab_try", "tab_sources"]
    rules = bookings.nav_css(UI_EN, keys, ["role_crew", "role_cmd"])
    assert rules.count("--ico:url(") == len(keys) + 2
    with pytest.raises(FileNotFoundError):
        bookings.lucide("no-such-icon")


def test_bookings_css_keeps_text_on_dark_glass():
    css = bookings.css()
    assert "stMainBlockContainer" in css and bookings.CREAM in css
    assert "rgba(46,38,33,.93)" in css   # the panel under the text stays dark (luminance <= 0.07)


@pytest.mark.parametrize("ui", [UI_EN, UI_FR])
def test_demo_dialogue_lines_fit_one_breath_and_name_known_speakers(ui):
    for n in range(1, 7):
        lines = ui[f"beat{n}_dialogue"]
        assert lines and all(sp in ("Pip", "Kora", "Commander") for sp, _ in lines)
        html = bot.dialogue(ui, lines)
        assert "<svg" not in html and html.count("cs-bot'") >= len(lines)
