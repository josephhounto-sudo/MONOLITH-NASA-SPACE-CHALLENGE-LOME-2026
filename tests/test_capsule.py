"""M2-1: daily DecisionCapsule is valid against the contract and its wording passes banned_hits()."""
import json
import os

import jsonschema
import pytest

from csync.capsule import build_capsule, ui_hint
from csync.language import banned_hits
from csync.rules import daily_values, evaluate
from synthetic.generator import generate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, "contracts", "decision_capsule.schema.json"), encoding="utf8"))


@pytest.fixture(scope="module")
def story():
    df = generate("histoire", seed=42, drift_amp=2.5, fast=True)   # provisional values, MAJ n°1
    z, flags, states, dec, ref = evaluate(daily_values(df))
    return z, flags, states, dec, ref


def caps(story):
    z, flags, states, dec, ref = story
    return {d: build_capsule(d, states, dec, z, ref, flags=flags) for d in states.index}


def test_day7_capsule_valid_and_clean(story):
    z, flags, states, dec, ref = story
    cap = build_capsule(7, states, dec, z, ref, flags=flags)
    jsonschema.validate(cap, SCHEMA)
    assert banned_hits(cap["explanation"]) == [] and banned_hits(cap["situation"]) == []
    assert cap["human_decision"] == "pending"
    assert cap["states"]["Attention"] == "DEGRADED"
    assert cap["action"]["type"] == "OPEN_PROCEDURE" and cap["ui_hint"] == "FOCUS"   # IMPORTANT, not CRITICAL
    # the explanation cites each flagged indicator with its value, unit and personal baseline
    for s in cap["signals"]:
        if s["flagged"]:
            assert s["indicator_id"] in cap["explanation"] and s["unit"] in cap["explanation"]
            assert f"{s['baseline_mean']:g}" in cap["explanation"]


def test_one_valid_capsule_per_day(story):
    all_caps = caps(story)
    assert sorted(all_caps) == list(range(1, 11))
    for cap in all_caps.values():
        jsonschema.validate(cap, SCHEMA)
        assert cap["human_decision"] == "pending"
        assert banned_hits(cap["explanation"] + " " + cap["situation"] + " " + cap["action"]["text"]) == []
        assert "NORMAL" not in (cap["states"]["Mission"], cap["states"]["Habitat"])


def test_baseline_days_never_normal(story):
    for d, cap in caps(story).items():
        if d <= 5:
            assert set(cap["states"].values()) == {"UNKNOWN"}
            assert "baseline being built" in cap["situation"]


def test_flagged_values_match_daily_values(story):
    df = generate("histoire", seed=42, drift_amp=2.5, fast=True)
    dv = daily_values(df)
    z, flags, states, dec, ref = story
    cap = build_capsule(7, states, dec, z, ref, flags=flags)
    for s in cap["signals"]:
        assert s["value"] == pytest.approx(round(dv.at[7, s["indicator_id"]], 1), abs=0.051)


def test_ui_hint_mapping():
    assert ui_hint("CONTINUE", "ROUTINE") == "NOMINAL"
    assert ui_hint("OPEN_PROCEDURE", "CRITICAL") == "ACTION"
    for a, c in [("OPEN_PROCEDURE", "ROUTINE"), ("OPEN_PROCEDURE", "IMPORTANT"), ("PAUSE", "ROUTINE"), ("REFUSE_RESUME", "CRITICAL")]:
        assert ui_hint(a, c) == "FOCUS"
