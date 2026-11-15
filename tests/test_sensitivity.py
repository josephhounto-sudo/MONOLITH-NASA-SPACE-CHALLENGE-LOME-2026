"""The shipped cell of the sensitivity grid is the shipped rule.

SYNTHETIC crews, seeds 60000+. Does not run the full grid.
"""
from research.sensitivity import shipped_cell_matches


def test_cell_1_5_2_5_matches_shipped_rule_on_control():
    assert shipped_cell_matches(60000, "false")


def test_cell_1_5_2_5_matches_shipped_rule_on_drift():
    assert shipped_cell_matches(62000, "drift15")


def test_cell_1_5_2_5_matches_shipped_rule_on_jump():
    assert shipped_cell_matches(63000, "jump2")
