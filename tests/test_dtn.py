"""DTN prototype: the promise's own test, plus the failure it must survive (losses and duplicates)."""
from csync.proto import dtn


def test_promise_1000_reports_through_a_6_hour_outage_and_a_20_minute_delay():
    r = dtn.simulate(1000, 1, (120, 120 + 360), 20, 0.0, seed=1)
    assert r["all_once_in_order"]


def test_lossy_link_still_delivers_every_report_once_in_order():
    r = dtn.simulate(1000, 1, (120, 480), 20, 0.15, seed=2)
    assert r["all_once_in_order"] and r["transmissions"] > 1000   # losses were really resent


def test_nothing_crosses_a_cut_link():
    r = dtn.simulate(10, 1, (0, 600), 0, 0.0, seed=3)
    assert r["last_arrival_min"] >= 600
