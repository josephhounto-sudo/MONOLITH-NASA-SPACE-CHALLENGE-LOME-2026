"""Every section except the home carries a one-line 'use' caption (rule: the interface works without the story)."""
from streamlit.testing.v1 import AppTest
from tests.helpers_app import open_app

import os
APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csync", "ui", "app.py")


def _sections():
    at = open_app(APP, 60)
    return list(at.radio(key="cs-nav").options)


def test_each_section_has_use_line_and_home_does_not_need_one():
    for name in [n for n in _sections() if n not in ("Live station", "Demo story")]:   # V3: those two carry their own intro
        at = open_app(APP, 60)
        at.radio(key="cs-nav").set_value(name).run()
        assert not at.exception, name
        captions = [c.value for c in at.caption]
        assert any(c.startswith(("Use:", "Usage :")) for c in captions), name
