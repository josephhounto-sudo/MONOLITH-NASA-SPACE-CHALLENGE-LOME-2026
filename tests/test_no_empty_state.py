"""Joseph (20/11/2026): no 'Unknown' and no empty box anywhere. Every gap says why, with the real information we hold.

The rule UNKNOWN != NORMAL is kept in the logic (rule v3 frozen); only the words change. Checked on every section, both roles,
on the story days that used to show 'Unknown' (baseline days and the sensor-fault habitat day)."""
import os

import pytest
from streamlit.testing.v1 import AppTest

APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csync", "ui", "app.py")


def _text(at):
    parts = [m.value for m in at.markdown] + [c.value for c in at.caption] + [w.value for w in at.warning]
    parts += [e.value for e in at.error] + [i.value for i in at.info] + [s.value for s in at.success]
    parts += [h.proto.body for h in at.get("html")]
    return "\n".join(parts)


@pytest.mark.parametrize("day", [1, 3, 7])
def test_no_unknown_word_on_any_section(day):
    at = AppTest.from_file(APP, default_timeout=90)
    at.session_state["cs-hook-done"] = True
    at.session_state["cs-bot-done"] = True
    at.session_state["cs-day"] = day
    at.run()
    for opt in list(at.sidebar.radio[0].options):
        at.sidebar.radio[0].set_value(opt).run()
        assert not at.exception, (opt, at.exception)
        assert "Unknown" not in _text(at), (day, opt)
