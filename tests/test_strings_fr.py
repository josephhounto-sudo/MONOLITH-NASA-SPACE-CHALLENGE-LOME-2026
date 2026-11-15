"""French string file: same keys, same order, same {placeholders} as the English file.

Vocabulary follows pitch/deck/SCRIPT_FR.md. pitch/deck/make_fr.py is not in this repository.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PH = re.compile(r"\{[^{}]+\}")


def _load(name):
    with open(os.path.join(ROOT, "csync", "config", name), encoding="utf8") as f:
        return json.load(f)


def _same(en, fr, path):
    assert type(en) is type(fr), path
    if isinstance(en, dict):
        assert list(en) == list(fr), path
        for key in en:
            _same(en[key], fr[key], f"{path}.{key}")
    elif isinstance(en, list):
        assert len(en) == len(fr), path
        for i, (a, b) in enumerate(zip(en, fr)):
            _same(a, b, f"{path}[{i}]")
    elif isinstance(en, str):
        assert PH.findall(en) == PH.findall(fr), path


def test_french_strings_match_english_keys_order_and_placeholders():
    _same(_load("strings_en.json"), _load("strings_fr.json"), "strings")
