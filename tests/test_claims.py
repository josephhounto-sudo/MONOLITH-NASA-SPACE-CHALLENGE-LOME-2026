"""Recalculate the figures quoted for the oral, from the code. Seeds and scenario sizes: docs/METHODES_NASA_DOSSIER.md §7.2.

SYNTHETIC crews only. If a figure falls outside the stated tolerance, leave this test as it is and report the gap to M1.
"""
import gzip
import json
import os
from datetime import datetime, timedelta

import pandas as pd
import pytest

from csync.gate import resume_gate
from csync.quality import flag_plateaus
from csync.rules import DRIFT_INDICATORS, DIRECTION, Params, daily_values, evaluate
from csync.sendqueue import deliver
from synthetic.generator import generate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDS = [i for ids in DRIFT_INDICATORS.values() for i in ids]
BASE = 5


def _daily(seed, variant, drift_amp):
    return daily_values(generate(variant, seed=seed, drift=variant == "histoire", event=False,
                                 drift_amp=drift_amp, fast=True))


def _population_sd():
    """Median baseline SD on seeds 20000-20199 (population reference, disjoint from the test crews)."""
    sds = []
    for seed in range(20000, 20200):
        dv = _daily(seed, "temoin", 0)
        sds.append(dv.loc[1:BASE, INDS].std(ddof=1))
    return pd.concat(sds, axis=1).median(axis=1)


def _abrupt(seed, s0):
    """2 SD step on day 8, Attention and Morale, same construction as research/pilot/pilot2.py."""
    dv = _daily(seed, "temoin", 0)
    for dim in ("Attention", "Morale"):
        for ind in DRIFT_INDICATORS[dim]:
            dv.loc[8:, ind] = dv.loc[8:, ind] + DIRECTION[ind] * 2.0 * s0[ind]
    return dv


def _opens(dv):
    _, _, _, decisions, _ = evaluate(dv, Params())
    return bool((decisions.action == "OPEN_PROCEDURE").any())


def _percent(hits, n):
    return 100.0 * hits / n


@pytest.fixture(scope="module")
def quoted_rates():
    s0 = _population_sd()
    control = sum(_opens(_daily(s, "temoin", 0)) for s in range(1000, 1300))
    gradual = sum(_opens(_daily(s, "histoire", 1.5)) for s in range(5000, 5150))
    abrupt = sum(_opens(_abrupt(s, s0)) for s in range(7000, 7150))
    return {
        "control": _percent(control, 300),
        "gradual": _percent(gradual, 150),
        "abrupt": _percent(abrupt, 150),
        "counts": (control, gradual, abrupt),
    }


def test_false_triggers_300_healthy_crews(quoted_rates):
    got = quoted_rates["control"]
    assert abs(got - 0.7) <= 0.3, f"false triggers {got:.2f}% (counts {quoted_rates['counts']})"


def test_gradual_drift_detection(quoted_rates):
    got = quoted_rates["gradual"]
    assert abs(got - 95.3) <= 1.5, f"gradual detection {got:.2f}% (counts {quoted_rates['counts']})"


def test_abrupt_jump_detection(quoted_rates):
    got = quoted_rates["abrupt"]
    assert abs(got - 59.3) <= 3.0, f"abrupt detection {got:.2f}% (counts {quoted_rates['counts']})"


def test_co2_raw_plateau_is_153h():
    raw = os.path.join(ROOT, "data", "real", "raw", "eda_all_missions.json.gz")
    telemetry = json.load(gzip.open(raw))["missions"]["RR-1"]["telemetry"]
    runs = flag_plateaus(telemetry["co2_iss"], min_len=144)
    assert len(runs) == 1
    run = runs[0]
    assert run["value"] == 2646
    span_h = (run["length"] - 1) * 5 / 60
    start = datetime.strptime(telemetry["time"][run["start"]], "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(telemetry["time"][run["end"]], "%Y-%m-%d %H:%M:%S")
    clock_h = (end - start).total_seconds() / 3600
    assert span_h == pytest.approx(153)
    assert clock_h == pytest.approx(153, abs=2 / 60)


def test_resume_gate_is_10_min():
    assert Params().max_age_min == 10
    request = datetime(2031, 3, 10, 9, 0)
    procedure = {
        "prerequisites": [{"indicator_id": "PH01", "max_age_min": Params().max_age_min, "sources": ["GUIDED"]}],
        "no_physical_prereq": False,
        "override_policy": {"logged_not_sufficient": True},
    }
    stale = [{"indicator_id": "PH01", "timestamp": request - timedelta(minutes=14), "quality": "OK", "source": "GUIDED"}]
    decision, reasons = resume_gate(request, stale, procedure)
    assert decision == "REFUSE_RESUME"
    assert any("14 min > 10 min" in r for r in reasons)
    fresh = [{**stale[0], "timestamp": request - timedelta(minutes=10)}]
    decision, _ = resume_gate(request, fresh, procedure)
    assert decision == "RESUME_AUTHORIZED"


def test_ground_delay_is_20_min():
    assert Params().ground_delay_min == 20
    link_down = datetime(2031, 3, 9, 13, 0)
    link_up = datetime(2031, 3, 9, 19, 0)
    created = datetime(2031, 3, 9, 14, 20)
    arrivals, _ = deliver([{"message_id": "report", "created": created}], link_down, link_up)
    assert arrivals[0]["received"] - arrivals[0]["sent"] == timedelta(minutes=Params().ground_delay_min)
    assert arrivals[0]["received"] == link_up + timedelta(minutes=20)
