"""Commander board: same rule as the story, never Normal by default, deterministic, sorted by urgency."""
import pandas as pd

from csync import crew


def test_baseline_days_all_unknown():
    for d in (1, 3, 5):
        b = crew.board(d)
        assert set(b.Body) | set(b.Attention) | set(b.Morale) == {"UNKNOWN"}


def test_sensor_gap_member_is_unknown_not_normal():
    b = crew.board(8).set_index("member")
    assert b.loc["Crew F", "Body"] == "UNKNOWN"


def test_sorted_most_urgent_first_and_procedure_waits_for_human():
    b = crew.board(9)
    assert list(b.action.map(crew.RANK)) == sorted(b.action.map(crew.RANK))
    opened = b[b.action == "OPEN_PROCEDURE"]
    assert len(opened) >= 1 and set(opened.human) == {"pending"} and set(opened.procedure) == {"PROC-FATIGUE-01"}


def test_deterministic_and_same_engine_as_single_member():
    assert crew.board(9).equals(crew.board(9))
    from csync.rules import Params, evaluate
    _z, _f, st, _d, _r = evaluate(crew.member_series("Crew C"), Params())
    assert crew.board(9).set_index("member").loc["Crew C", "Attention"] == st.loc[9, "Attention"]
