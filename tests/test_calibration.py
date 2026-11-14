"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

T4: guard-rails for the calibrated rule (Params(): threshold 1.5 + absolute SD floors). SYNTHETIC crews only.
If (a) or (b) fails, do NOT move the engine threshold: report the numbers to M1.
Measured 14/11/2026 on this code: (a) 1/100 control crews open a procedure; (b) 95/100 drift crews do.
"""
import json
import os

import numpy as np
import pandas as pd
import pytest

from csync.rules import Params, daily_values, evaluate
from synthetic.generator import generate
from tests.helpers_detectors import cusum_flags, ewma_flags

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORS = json.load(open(os.path.join(ROOT, "docs", "blocks", "test_vectors_detectors.json"), encoding="utf8"))


def opens_procedure(df):
    _, _, _, dec, _ = evaluate(daily_values(df))
    return bool((dec.action == "OPEN_PROCEDURE").any())


def test_a_control_crews_false_procedures_at_most_3_percent():
    n = sum(opens_procedure(generate("temoin", seed=s, drift=False, event=False, drift_amp=0, fast=True))
            for s in range(1000, 1100))
    assert n <= 3, f"{n}/100 control crews open a procedure (limit 3)"


def test_b_drift_crews_detected_at_least_90_percent():
    n = sum(opens_procedure(generate("histoire", seed=s, drift_amp=1.5, fast=True)) for s in range(5000, 5100))
    assert n >= 90, f"{n}/100 drift crews open a procedure (limit 90)"


def engine_flags(z):
    """Feed a series of d values through the real engine (csync.rules.evaluate) on one indicator.

    CO01 (increase unfavourable, no absolute floor): baseline days are all 100 -> SD 0 -> SD floor 5 % = 5,
    so value = 100 + 5 * d gives exactly d. Missing d -> missing value.
    """
    days = list(range(1, len(z) + 1))
    dv = pd.DataFrame({"CO01": [np.nan if v is None else 100 + 5 * v for v in z]}, index=days)
    zz, flags, _, _, _ = evaluate(dv, Params())
    got = zz["CO01"].tolist()
    for g, v in zip(got, z):
        assert (v is None and np.isnan(g)) or g == pytest.approx(v)
    return [bool(x) for x in flags["CO01"]]


@pytest.mark.parametrize("case", sorted(VECTORS))
def test_c_rule_d15_matches_vectors(case):
    v = VECTORS[case]
    assert engine_flags(v["z_days_1_to_10"]) == v["rule_d1.5_two_consecutive_flags"]


@pytest.mark.parametrize("case", sorted(VECTORS))
def test_c_reference_ewma_matches_vectors(case):
    v = VECTORS[case]
    assert ewma_flags(v["z_days_1_to_10"]) == v["ewma_lambda0.3_L2.5_flags_days_1_to_10"]


@pytest.mark.parametrize("case", sorted(VECTORS))
def test_c_reference_cusum_matches_vectors(case):
    v = VECTORS[case]
    assert cusum_flags(v["z_days_1_to_10"]) == v["cusum_k0.5_h3_flags"]


def test_engine_has_no_ewma_or_cusum():
    src = open(os.path.join(ROOT, "csync", "rules.py"), encoding="utf8").read().lower()
    assert "ewma" not in src and "cusum" not in src
