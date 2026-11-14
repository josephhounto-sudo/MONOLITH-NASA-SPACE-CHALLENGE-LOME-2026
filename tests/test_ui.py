"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

M3-1..M3-3: headless checks of the Streamlit screens (streamlit.testing). A human still has to look at the screens."""
import os
import re

import pytest
from streamlit.testing.v1 import AppTest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "csync", "ui", "app.py")


def page(day):
    at = AppTest.from_file(APP, default_timeout=60).run()
    at.slider[0].set_value(day).run()
    assert not at.exception, at.exception
    return at


def html(at):
    return " ".join(m.value for m in at.markdown)


def test_banner_always_shown():
    at = page(7)
    assert any("SYNTHETIC DATA" in w.value for w in at.warning)


def test_day7_attention_degraded():
    h = html(page(7))
    assert re.search(r">Attention</div><div[^>]*>▲ Degraded<", h)


@pytest.mark.parametrize("day", [1, 3, 5])
def test_baseline_days_never_normal(day):
    h = html(page(day))
    for dim in ("Body", "Attention", "Morale"):
        assert re.search(rf">{dim}</div><div[^>]*>\? Personal baseline being built \(day {day} of 5\)<", h)
    assert "✓ Normal" not in h


def test_context_dimensions_never_normal():
    h = html(page(8))
    for dim in ("Mission", "Habitat"):
        assert re.search(rf">{dim}</div><div[^>]*>\? Context only", h)


def test_day9_six_steps_and_send_queue():
    at = page(9)
    seen = []
    for _ in range(6):
        seen.append(next(m.value for m in at.markdown if m.value.startswith("**Step ")))
        nxt = next(b for b in at.button if b.label == "Next")
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
        next(b for b in at.button if b.label == "Next").click().run()
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
