"""Every section except the home carries a one-line 'use' caption (rule: the interface works without the story)."""
from streamlit.testing.v1 import AppTest

import os
APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csync", "ui", "app.py")


def _sections():
    at = AppTest.from_file(APP, default_timeout=60).run()
    return list(at.sidebar.radio[0].options)


def test_each_section_has_use_line_and_home_does_not_need_one():
    for name in _sections()[1:]:
        at = AppTest.from_file(APP, default_timeout=60).run()
        at.sidebar.radio[0].set_value(name).run()
        assert not at.exception, name
        captions = [c.value for c in at.caption]
        assert any(c.startswith(("Use:", "Usage :")) for c in captions), name
