"""The nominal screen must not show the whole explanation as one paragraph.

Acceptance: a verdict sentence, one short line per flagged indicator
(value, this person's normal, times the usual variation), and the rule
only inside the folded detail. No line is longer than 110 characters.

Five ways it fails:
1. no signals (empty day): still a verdict, and no crash.
2. a flagged reading with no value: no made-up number.
3. two flagged indicators: two lines, not one paragraph.
4. a capsule that is not a dict (cold / wrong file): a clear error.
5. the rule sentence is missing: the visible lines stay short.
"""
import os

import pytest

from csync.ui.why import short_verdict, why_parts

UI = {
    "why_line": "{name}: {value} {unit}. This person's normal: {normal}. {times}× usual variation.",
    "why_missing": "{name} is missing today, so this view does not treat it as normal.",
    "why_context": "{name}: {value} {unit}.",
}


def _sig(name, value=5.5, normal=7.0, d=1.8, flagged=True):
    return {"name": name, "value": value, "unit": "h", "baseline_mean": normal, "d": d, "flagged": flagged}


def test_empty_signals_still_have_a_verdict():
    """Failure 1: nothing was flagged."""
    out = why_parts({"situation": "Day 3: no evaluated dimension is away from this person's own normal.",
                     "signals": [], "explanation": "No indicator is flagged today. Rule v3: an indicator is flagged when it is at least 1.5 times."}, UI)
    assert out["verdict"].startswith("Day 3:")
    assert out["lines"] == []
    assert "Rule v3" in out["rule"]
    assert "Rule v3" not in out["verdict"]


def test_missing_value_is_not_invented():
    """Failure 2: the reading is missing."""
    cap = {"situation": "Day 4: not evaluated.", "signals": [_sig("Sleep", value=None, d=None)],
           "explanation": "Sleep is missing today. Rule v3: kept."}
    out = why_parts(cap, UI)
    assert len(out["lines"]) == 1
    assert "times" not in out["lines"][0].lower()
    assert "None" not in out["lines"][0]


def test_two_flagged_indicators_are_two_lines():
    """Failure 3: several indicators must not collapse into one paragraph."""
    cap = {"situation": "Day 7: two dimensions away.",
           "signals": [_sig("Sleep", 5.5, 7.1, 1.8), _sig("Heart rate", 70, 60, 2.0, flagged=True),
                       _sig("Mood", 4, 4, 0.1, flagged=False)],
           "explanation": "Sleep ... Heart rate ... Rule v3: two days."}
    out = why_parts(cap, UI)
    assert len(out["lines"]) == 2
    assert "Sleep" in out["lines"][0] and "Heart rate" not in out["lines"][0]
    assert "5.5" in out["lines"][0] and "7.1" in out["lines"][0] and "1.8" in out["lines"][0]
    for line in out["lines"]:
        assert len(line) <= 110
        assert "Rule v3" not in line


def test_bad_capsule_says_what_to_do():
    """Failure 4: the file is not a capsule."""
    with pytest.raises(ValueError) as err:
        why_parts([], UI)
    assert "capsule" in str(err.value).lower()


def test_missing_rule_does_not_dump_the_paragraph():
    """Failure 5: the stored explanation has no rule sentence."""
    wall = " ".join(["Reported sleep is 5.5 h against a long personal sentence."] * 8)
    cap = {"situation": "Day 7: away.", "signals": [_sig("Sleep")], "explanation": wall}
    out = why_parts(cap, UI)
    assert out["rule"] == ""
    assert wall not in out["verdict"]
    assert all(wall not in line for line in out["lines"])
    assert all(len(line) <= 110 for line in out["lines"])


def test_short_verdict_stays_one_sentence():
    cap = {"day": 7, "states": {"Body": "WATCH", "Attention": "DEGRADED", "Morale": "NORMAL", "Habitat": "NORMAL"},
           "situation": "Day 7: 2 dimension(s) away from this person's own normal: Body (WATCH), Attention (DEGRADED)."}
    text = short_verdict(cap, {"WATCH": "Watch", "DEGRADED": "Degraded", "NORMAL": "Normal"})
    assert text == "Day 7: Body Watch, Attention Degraded."
    assert len(text) <= 90
    early = short_verdict({"day": 3, "states": {"Body": "UNKNOWN", "Attention": "UNKNOWN", "Morale": "UNKNOWN"}}, {})
    assert "baseline" in early
    assert "nothing is away" not in early


def test_nominal_no_longer_prints_the_explanation_as_one_paragraph():
    app = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "csync", "ui", "app.py"), encoding="utf8").read()
    assert "why_parts(" in app
    assert "cap['explanation']}" not in app
    assert "why_rule_label" in app
