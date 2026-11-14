"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

T5: banned wording must never come back in what the screen or the README shows, including negated forms
("no diagnosis", "does not diagnose"). "emergency" and "chest pain" are allowed: they are events declared by the crew.
"""
import glob
import os
import re

import pytest

from csync.language import banned_hits

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["csync/config/strings_en.json", "csync/ui/app.py", "README.md",
         *sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "data", "procedures", "*.json")))]
# word stems that csync.language does not list in every inflected form
EXTRA = [r"\bdiagnos", r"\bcaus(e|es|ed|ing|al)\b", r"\bprov(e|es|ed|ing)\b", r"\bguarantee", r"\bmaladie",
         r"\bpathologi", r"\bprouv", r"\bgaranti"]


@pytest.mark.parametrize("rel", FILES)
def test_no_banned_wording(rel):
    text = open(os.path.join(ROOT, rel), encoding="utf8").read()
    if rel == "README.md":
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    hits = banned_hits(text) + [p for p in EXTRA if re.search(p, text, re.I)]
    assert hits == [], f"{rel}: {hits}"


def test_detector_catches_negated_forms():
    for s in ("This report contains no diagnosis.", "C-Sync does not diagnose.", "It does not name causes."):
        t = s.lower()
        assert banned_hits(t) or any(re.search(p, t) for p in EXTRA), s


def test_emergency_words_are_allowed():
    assert banned_hits("Guided emergency: chest pain reported by the crew member.") == []
