"""The dark proposal clears the thresholds on a flat fill. It is not the live theme."""
import os

from scripts.propose_dark_theme import below

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_flat_fill_meets_the_thresholds():
    assert below() == []


def test_proposal_does_not_touch_the_live_stylesheet():
    src = open(os.path.join(ROOT, "scripts", "propose_dark_theme.py"), encoding="utf8").read()
    assert "style.py" in src  # the file says it leaves the live stylesheet alone
    assert "inject" not in src
