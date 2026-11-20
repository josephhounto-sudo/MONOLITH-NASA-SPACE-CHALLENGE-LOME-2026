"""Open the Streamlit app past the opening hook (the hook has its own tests).

V3 (20/11/2026): the app opens on the live console; tests of the drift story open the "Demo story" section directly.
"""
import json
import os

from streamlit.testing.v1 import AppTest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_ROOT, "csync", "config", "strings_en.json"), encoding="utf8") as _fh:
    STORY_TAB = json.load(_fh)["ui"]["tab_home"]


def open_app(path, timeout=60, section=STORY_TAB):
    at = AppTest.from_file(path, default_timeout=timeout)
    at.session_state["cs-hook-done"] = True
    at.session_state["cs-bot-done"] = True
    if section:
        at.session_state["cs-nav"] = section
    return at.run()
