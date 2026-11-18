import os, sys
import pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "research"))
from fixed_vs_personal import fixed, fixed_sleep_only, person, SLEEP_MIN_H, LAPSES_MAX


def frame(sleep, lapses):
    return pd.DataFrame({"PH09": sleep, "CO02": lapses}, index=range(1, 11))


def test_spread_zero_is_the_shipped_person():
    p = person(65000, 0)
    assert p.sleep_h == 7.2 and p.rt_ms == 265.0


def test_published_thresholds_are_the_ones_named():
    assert SLEEP_MIN_H == 7.0 and LAPSES_MAX == 11


def test_fixed_rules_fire_on_two_consecutive_days_only():
    s = [7.2] * 5 + [6.5, 7.5, 6.5, 6.5, 7.5]
    assert fixed_sleep_only(frame(s, [0] * 10)) == 9
    assert fixed_sleep_only(frame([7.2] * 10, [0] * 10)) is None
    both = frame([7.2] * 5 + [6.0] * 5, [0] * 5 + [12] * 5)
    assert fixed(both) == 7
    assert fixed(frame([6.0] * 10, [0] * 10)) is None      # sleep alone never opens the two-indicator rule
