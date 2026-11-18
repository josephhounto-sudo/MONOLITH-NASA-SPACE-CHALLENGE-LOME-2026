"""EN/FR string parity.

Acceptance: `python scripts/compare_strings.py` prints nothing and exits 0.
English sentences are not rewritten. No medical sentence is edited here.

Five ways the check fails:
1. a string file is missing or empty (cold start).
2. a key exists on only one side.
3. a prose value is copied from English and is not a shared word.
4. a placeholder differs ({n} vs {m}), so format() would break one language.
5. a reviewed false friend is still in the French file (Gate rendered as a door).
"""
import json
import os
import subprocess
import sys

import pytest

from scripts.compare_strings import gaps, load_pair

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = os.path.join(ROOT, "csync", "config", "strings_en.json")
FR = os.path.join(ROOT, "csync", "config", "strings_fr.json")


def test_missing_or_empty_file_says_what_to_do(tmp_path):
    """Failure 1: a cold tree with no string file."""
    empty = tmp_path / "empty.json"
    empty.write_text("", encoding="utf8")
    missing = tmp_path / "nope.json"
    with pytest.raises(ValueError) as err:
        load_pair(str(missing), str(empty))
    text = str(err.value)
    assert "restore it from git" in text
    assert "empty" in text


def test_a_key_on_only_one_side_is_a_gap():
    """Failure 2: French lost a key, or gained one English does not have."""
    assert any("missing in French" in g for g in gaps({"a": "Yes"}, {}))
    assert any("missing in English" in g for g in gaps({}, {"b": "Oui"}))


def test_identical_prose_is_a_gap():
    """Failure 3: an untranslated sentence."""
    found = gaps({"a": "The report is waiting."}, {"a": "The report is waiting."})
    assert any("identical" in g for g in found)
    assert gaps({"a": "C-Sync"}, {"a": "C-Sync"}) == []


def test_placeholder_mismatch_is_a_gap():
    """Failure 4: the two languages do not format the same fields."""
    found = gaps({"a": "Day {n}"}, {"a": "Jour {m}"})
    assert any("placeholders" in g for g in found)


def test_gate_rendered_as_a_door_is_a_gap():
    """Failure 5: a reviewed false friend. 'Porte' is a door, not the resume check."""
    found = gaps({"ui": {"decision": "Gate decision"}}, {"ui": {"decision": "Décision de la porte"}})
    assert any("door" in g for g in found)
    assert gaps({"ui": {"decision": "Gate decision"}}, {"ui": {"decision": "Décision du contrôle"}}) == []


def test_english_medical_sentence_is_unchanged():
    en = json.load(open(EN, encoding="utf8"))
    assert en["fixed_medical_sentence"] == "Follow the onboard medical checklist and the crew medical officer."


def test_catalog_has_zero_gaps():
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "compare_strings.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stdout
    assert proc.stdout.strip() == ""
