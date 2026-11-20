"""Prototypes of V3 promises. Each one runs the test its promise states (registry 'test' field)."""
from csync.proto import common_signal as cs
from csync.proto import exposure_ledger as el


def test_common_signal_meets_its_promise_on_seeds_never_used():
    # promise: at least 90 % correct attribution on seeds never used for tuning (rule chosen on 0-199 only, see module doc)
    assert cs.accuracy(range(5000, 6000)) >= 0.90
    assert cs.accuracy_all_days(range(5000, 6000)) >= 0.95   # quiet days count too: a false alarm is an error


def test_common_signal_rule_on_a_hand_made_crew():
    z = {"A": [0, 2, 0], "B": [0, 2, 0], "C": [0, 0, 2], "D": [0, 0, 0]}
    kinds = [r["kind"] for r in cs.attribute(z)]
    assert kinds == ["none", "shared", "individual"]


def test_exposure_ledger_equals_the_nasa_column_day_by_day():
    from csync import habitat
    led = el.ledger()
    nasa = habitat.rr1_radiation()["accumulated_mgy"].tolist()
    assert led["radiation_mgy_cum"].tolist() == nasa   # promise: the cumulative dose equals NASA's own column
    assert led["co2_7d_above_2_5"].dtype == bool
