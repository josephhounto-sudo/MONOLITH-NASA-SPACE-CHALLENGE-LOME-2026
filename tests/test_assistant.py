"""Scripted assistant (csync/assistant.py): validated by Joseph on 2026-11-18 as scripted, not a free-text model.

Properties that must hold for EVERY capsule of EVERY variant, in EN and FR:
short lines, no banned wording, every number traceable to the capsule, UNKNOWN never worded as normal,
fail-closed on missing provenance, deterministic, no network or model import.
"""
import ast
import importlib.util
import json
import os
import re

import pytest

from csync import assistant
from csync.language import banned_hits
from csync.rules import Params

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRA = [r"\bdiagnos", r"\bcaus(e|es|ed|ing|al)\b", r"\bprov(e|es|ed|ing)\b", r"\bguarantee", r"\bmaladie",
         r"\bpathologi", r"\bprouv", r"\bgaranti"]
MAX_WORDS = 20
STR = {lang: json.load(open(os.path.join(ROOT, "csync", "config", f"strings_{lang}.json"), encoding="utf8")) for lang in ("en", "fr")}


@pytest.fixture(scope="module")
def all_capsules(tmp_path_factory):
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = mod.main(str(tmp_path_factory.mktemp("caps")))
    return [(v, c) for v, caps in out.items() for c in caps]


def allowed_numbers(cap):
    ok = {str(cap["day"])}
    ok |= set(re.findall(r"\d+", cap.get("time_utc", "")))
    for s in cap.get("signals", []):
        for k in ("value", "baseline_mean"):
            if s.get(k) is not None:        # baseline days and sensor outages carry no value or no mean
                ok.add(f"{round(float(s[k]), 1):g}")
    gi = cap.get("gate_inputs")
    if gi:
        ok.add(str(gi["max_age_min"]))
        ok |= {str(m["age_min"]) for m in gi["measurements"]}
    prm = Params()
    ok |= {f"{round(prm.d_threshold, 1):g}", str(prm.consecutive_days), str(cap["reliability"].get("baseline_days", 5))}
    return ok


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_every_capsule_every_question(all_capsules, lang):
    for variant, cap in all_capsules:
        for q in assistant.QUESTIONS:
            lines = assistant.answer(cap, q, STR[lang])
            assert lines, (variant, cap["day"], q)
            for line in lines:
                assert len(line.split()) <= MAX_WORDS, line
                assert banned_hits(line) == [] and not any(re.search(p, line, re.I) for p in EXTRA), line
                assert "{" not in line and "}" not in line, f"unfilled placeholder: {line}"


def test_every_number_in_why_is_traceable_to_the_capsule(all_capsules):
    for variant, cap in all_capsules:
        text = " ".join(assistant.answer(cap, "why", STR["en"]))
        for n in re.findall(r"\d+(?:\.\d+)?", text):
            assert n in allowed_numbers(cap), (variant, cap["day"], cap.get("capsule_type"), n, text)


def test_baseline_days_say_learning_never_normal(all_capsules):
    for variant, cap in all_capsules:
        if cap.get("capsule_type", "daily") == "daily" and cap["day"] <= 5:
            text = " ".join(assistant.answer(cap, "why", STR["en"]))
            assert "learning" in text
            assert "Nothing is outside" not in text


def test_story_beats_say_what_the_story_says(all_capsules):
    caps = {(v, c.get("capsule_type", "daily"), c["day"]): c for v, c in all_capsules}
    d7 = " ".join(assistant.answer(caps[("histoire", "daily", 7)], "why", STR["en"]))
    assert "sleep: 5.5 h, usual 7.2 h" in d7 and "Reaction time: 303.5 ms, usual 264.7 ms" in d7
    em = assistant.answer(caps[("histoire", "emergency", 9)], "why", STR["en"])
    assert em[0] == "Nia reported chest pain at 14:10 UTC. Guided steps are open."
    assert em[1] == STR["en"]["fixed_medical_sentence"]
    rs = assistant.answer(caps[("histoire", "resume", 10)], "why", STR["en"])
    assert rs[0] == "The heart-rate reading is 14 min old. The limit is 10 min."
    assert rs[-1] == "Resume refused. New measurements are needed."


def test_control_variant_has_nothing_to_report(all_capsules):
    for variant, cap in all_capsules:
        if variant == "temoin" and cap.get("capsule_type", "daily") == "daily" and cap["day"] > 5:
            assert "Nothing is outside" in " ".join(assistant.answer(cap, "why", STR["en"]))


def test_missing_provenance_fails_closed(all_capsules):
    _, cap = all_capsules[0]
    cap = json.loads(json.dumps(cap))
    cap["reliability"]["data_origin"] = "UNSPECIFIED"
    lines = assistant.answer(cap, "data", STR["en"])
    assert lines[0] == STR["en"]["assistant"]["data_origin_unstated"]
    assert not any("simulated" in line for line in lines[:1])


def test_data_answer_never_claims_nasa_data_enters_the_calculation(all_capsules):
    _, cap = next(x for x in all_capsules if x[1].get("capsule_type", "daily") == "daily" and x[1]["day"] == 7)
    text = " ".join(assistant.answer(cap, "data", STR["en"]))
    assert "not in my calculation" in text and "context only" in text.lower()


def test_unknown_question_is_refused(all_capsules):
    with pytest.raises(ValueError):
        assistant.answer(all_capsules[0][1], "free text please", STR["en"])


def test_deterministic(all_capsules):
    _, cap = all_capsules[8]
    assert assistant.answer(cap, "why", STR["en"]) == assistant.answer(cap, "why", STR["en"])


def test_no_network_or_model_imports():
    tree = ast.parse(open(os.path.join(ROOT, "csync", "assistant.py"), encoding="utf8").read())
    mods = {n.names[0].name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import)}
    mods |= {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
    assert mods <= {"__future__", "re", "csync"}, mods
