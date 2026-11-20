"""The guide bot: an original mascot (drawn here, no generated or third-party image) that runs the first-visit tutorial
and speaks the demo dialogue. Its lines live in the strings files (bot_steps, demo_dialogue) so the forbidden-word test
covers them. It never decides anything: it points, a human decides.
"""
from __future__ import annotations

import base64
import html

import streamlit as st

MASCOT = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'>
<defs><radialGradient id='h' cx='50%' cy='50%' r='50%'><stop offset='0' stop-color='#FF9A5C' stop-opacity='.75'/><stop offset='1' stop-color='#FF9A5C' stop-opacity='0'/></radialGradient>
<linearGradient id='b' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#FFFBF5'/><stop offset='1' stop-color='#E9D7C6'/></linearGradient>
<linearGradient id='v' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#4B4039'/><stop offset='1' stop-color='#1C1512'/></linearGradient></defs>
<circle cx='60' cy='64' r='54' fill='url(#h)'/>
<line x1='60' y1='22' x2='60' y2='10' stroke='#E9D7C6' stroke-width='3' stroke-linecap='round'/><circle cx='60' cy='9' r='5' fill='#FF8A4C'/>
<rect x='22' y='22' width='76' height='78' rx='36' fill='url(#b)'/>
<rect x='31' y='40' width='58' height='34' rx='17' fill='url(#v)'/>
<circle cx='49' cy='57' r='4.5' fill='#FFFDFD'/><circle cx='71' cy='57' r='4.5' fill='#FFFDFD'/>
<path d='M52 86 Q60 91 68 86' stroke='#CF783C' stroke-width='3' fill='none' stroke-linecap='round'/>
<circle cx='36' cy='92' r='3' fill='#E98F6D'/><circle cx='84' cy='92' r='3' fill='#E98F6D'/></svg>"""


def mascot_uri() -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(MASCOT.encode("utf-8")).decode("ascii")


def bubble(ui: dict, text: str, step: str = "") -> str:
    """One speech bubble with the mascot (st.html keeps <img>, not inline <svg>)."""
    assert text
    tag = f"<span class='cs-bot-step'>{html.escape(step)}</span>" if step else ""
    return (f"<div class='cs-bot'><img src='{mascot_uri()}' alt='{html.escape(ui['bot_name'])}, the C-Sync guide' width='72' height='72'>"
            f"<div class='cs-bot-say'><b>{html.escape(ui['bot_name'])}</b>{tag}<p>{html.escape(text)}</p></div></div>")


BOT_CSS = """<style>
.cs-bot{display:flex;gap:14px;align-items:flex-start;margin:4px 0 12px}
.cs-bot img{flex:none;filter:drop-shadow(0 10px 24px rgba(255,154,92,.45))}
.cs-bot-say{position:relative;border-radius:28px;padding:12px 18px;background:rgba(255,253,253,.96);color:#2E2621;max-width:640px;
 box-shadow:0 14px 34px rgba(0,0,0,.28)}
.cs-bot-say *{color:#2E2621!important}.cs-bot-say p{margin:.2em 0 0}
.cs-bot-step{margin-left:10px;font-size:.86rem;font-weight:600}
</style>"""


def tutorial(ui: dict) -> None:
    """First visit: steps one by one (Next / Skip). Afterwards: a small 'show the guide again' button."""
    steps = ui["bot_steps"]
    assert 1 <= len(steps) <= 6, "the tutorial keeps six steps at most"
    st.html(BOT_CSS)
    if st.session_state.get("cs-bot-done"):
        if st.button(ui["bot_replay"], key="cs-bot-replay"):
            st.session_state["cs-bot-done"], st.session_state["cs-bot-i"] = False, 0
            st.rerun()
        return
    i = min(int(st.session_state.get("cs-bot-i", 0)), len(steps) - 1)
    st.html(bubble(ui, steps[i], ui["bot_step_of"].format(i=i + 1, n=len(steps))))
    c1, c2 = st.columns([1, 1])
    last = i == len(steps) - 1
    if c1.button(ui["bot_done"] if last else ui["bot_next"], key="cs-bot-next", type="primary"):
        if last:
            st.session_state["cs-bot-done"] = True
        else:
            st.session_state["cs-bot-i"] = i + 1
        st.rerun()
    if not last and c2.button(ui["bot_skip"], key="cs-bot-skip"):
        st.session_state["cs-bot-done"] = True
        st.rerun()


def dialogue(ui: dict, lines: list) -> str:
    """Demo dialogue of one story beat: Pip speaks in its bubble, the astronaut and the commander in plain cards.
    Every line is at most 12 words (one breath, story-writer rule); the test enforces it."""
    assert lines and all(len(t.split()) <= 12 for _, t in lines)
    who = {"Pip": None, "Kora": ui["speaker_crew"], "Commander": ui["speaker_cmd"]}
    out = [BOT_CSS]
    for speaker, text in lines:
        if who.get(speaker) is None:
            out.append(bubble(ui, text))
        else:
            out.append(f"<div class='cs-bot'><div style='width:72px;flex:none'></div><div class='cs-say-h'><b>{html.escape(who[speaker])}</b>"
                       f"<p>{html.escape(text)}</p></div></div>")
    return "".join(out) + "<style>.cs-say-h{border-radius:28px;padding:10px 18px;background:rgba(34,27,23,.9);border:1px solid rgba(255,253,253,.22)}.cs-say-h p{margin:.2em 0 0}</style>"
