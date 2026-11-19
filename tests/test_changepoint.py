"""CUSUM and BOCPD. Every series here is SIMULATED. Seed A freezes k and h; seed B and the capsule do not."""
import statistics

import pytest

from synthetic.generator import generate
from csync.analytics.changepoint import bocpd, cusum

# Seed A (11011) froze these. This file does not score seed A.
TUNE_SEED = 11011
CONTROL_SEED = 22022
FROZEN_K = 0.5
FROZEN_H = 4.0
# Capsule days 1-10, indicator CO01, from data/out/trends_histoire.json. SIMULATED story.
CAPSULE_CO01 = [258.3, 279.4, 254.0, 261.4, 270.4, 296.2, 303.5, 317.1, 330.3, 254.1]
CAPSULE_MEAN = 264.7
FIXED_THRESHOLD = 284.553


def _sd(values):
    return statistics.stdev(values)


def _daily_co01(seed, variant):
    frame = generate(variant, seed=seed, fast=True, drift=(variant == "histoire"), event=False)
    rows = frame[frame.indicator_id == "CO01"].sort_values("day")
    return [float(v) for v in rows.value.tolist()]


def test_flat_series_has_no_alarm():
    flat = [10.0] * 8
    out = cusum(flat, baseline_mean=10.0, baseline_sd=1.0)
    assert out["alarm_index"] is None
    assert out["scores"] == [0.0] * 8


def test_sharp_jump_alarms_within_one_sample():
    # Hand scores with k=0.5, h=4: five zeros, then 4.5, 9.0, 13.5. Alarm at index 5.
    series = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 5.0, 5.0]
    out = cusum(series, baseline_mean=0.0, baseline_sd=1.0, k=0.5, h=4.0)
    assert out["scores"] == [0.0, 0.0, 0.0, 0.0, 0.0, 4.5, 9.0, 13.5]
    assert out["alarm_index"] == 5


def test_slow_slope_before_fixed_co01_threshold():
    """SIMULATED ramp from the capsule mean. The fixed cut is 284.553. Alarm must land earlier."""
    sd = _sd(CAPSULE_CO01[:5])
    ramp = [CAPSULE_MEAN + i for i in range(30)]
    cross = next(i for i, value in enumerate(ramp) if value >= FIXED_THRESHOLD)
    out = cusum(ramp, baseline_mean=CAPSULE_MEAN, baseline_sd=sd, k=FROZEN_K, h=FROZEN_H)
    assert out["alarm_index"] is not None
    assert out["alarm_index"] < cross
    assert ramp[out["alarm_index"]] < FIXED_THRESHOLD


def test_capsule_control_is_separate_from_tuning():
    assert TUNE_SEED != CONTROL_SEED
    sd = _sd(CAPSULE_CO01[:5])
    first = cusum(CAPSULE_CO01, CAPSULE_MEAN, sd, k=FROZEN_K, h=FROZEN_H)
    second = cusum(CAPSULE_CO01, CAPSULE_MEAN, sd, k=FROZEN_K, h=FROZEN_H)
    assert first == second
    cross = next(i for i, value in enumerate(CAPSULE_CO01) if value >= FIXED_THRESHOLD)
    assert cross == 5
    assert first["alarm_index"] is not None


def test_control_seed_temoin_stays_quiet_and_histoire_alarms():
    # Person.rt_day_sd in the generator. Not estimated on seed A or seed B.
    design_sd = 10.0
    for variant, expect_alarm in (("temoin", False), ("histoire", True)):
        series = _daily_co01(CONTROL_SEED, variant)
        out = cusum(series, statistics.fmean(series[:5]), design_sd, k=FROZEN_K, h=FROZEN_H)
        assert (out["alarm_index"] is not None) is expect_alarm


def test_empty_and_non_positive_sd_raise():
    with pytest.raises(ValueError):
        cusum([], baseline_mean=0.0, baseline_sd=1.0)
    with pytest.raises(ValueError):
        cusum([1.0, 2.0], baseline_mean=0.0, baseline_sd=0.0)
    with pytest.raises(ValueError):
        cusum([1.0, 2.0], baseline_mean=0.0, baseline_sd=-1.0)


def test_cusum_and_bocpd_are_deterministic():
    series = [0.0, 0.1, -0.2, 3.0, 3.2, 2.8]
    assert cusum(series, 0.0, 1.0) == cusum(series, 0.0, 1.0)
    assert bocpd(series) == bocpd(series, hazard=1 / 20)


def test_bocpd_flat_has_no_standout_and_jump_is_near_the_step():
    flat = bocpd([0.0] * 12)
    assert flat["most_likely_index"] is None
    assert len(flat["change_prob"]) == 12
    jump = bocpd([0.0] * 5 + [4.0] * 5)
    assert jump["most_likely_index"] is not None
    assert abs(jump["most_likely_index"] - 5) <= 1
