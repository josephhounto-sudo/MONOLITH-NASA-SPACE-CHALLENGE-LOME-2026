"""Hand-checked intervals. The series from simulated_rr is SIMULATED, not a recorded rhythm."""
import math

import pytest

from csync.physio.hrv import clean_rr, rmssd, sdnn, simulated_rr

# Four intervals. Successive gaps: 10, -20, 30. Sample deviation divisor is n-1.
RR = [800.0, 810.0, 790.0, 820.0]


def test_hand_values_on_four_intervals():
    assert rmssd(RR) == math.sqrt((100 + 400 + 900) / 3)
    assert sdnn(RR) == math.sqrt(500 / 3)


def test_too_few_or_non_positive_intervals_raise():
    for bad in ([], [800.0, 810.0], [800.0, 0.0, 790.0], [800.0, -1.0, 790.0]):
        with pytest.raises(ValueError):
            rmssd(bad)
        with pytest.raises(ValueError):
            sdnn(bad)


def test_simulated_series_is_deterministic():
    first = simulated_rr(60, 60.0, seed=7, stress=0.2)
    second = simulated_rr(60, 60.0, seed=7, stress=0.2)
    assert first == second
    assert len(first) >= 3
    assert all(value > 0 for value in first)


def test_higher_stress_lowers_rmssd_on_twenty_seeds():
    for seed in range(20):
        calm = rmssd(simulated_rr(30, 70.0, seed=seed, stress=0.0))
        tense = rmssd(simulated_rr(30, 70.0, seed=seed, stress=0.8))
        assert tense < calm


def test_clean_rr_drops_out_of_range_and_counts_them():
    kept, dropped = clean_rr([250.0, 300.0, 800.0, 2000.0, 2001.0])
    assert kept == [300.0, 800.0, 2000.0]
    assert dropped == 2
