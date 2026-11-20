"""Habitat V3: episodes, one-sentence reading, mission replay.

Pre-mortem: (1) an artifact hour counted as an alert; (2) a gap between two runs merged into one episode;
(3) the reading sentence typed by hand drifts from the data; (4) the app replay disagrees with the research replay;
(5) the 7-day level differs from NASA's 2.5 mmHg."""
import pandas as pd

from csync import habitat


def _df(vals, art=None):
    h = pd.date_range("2014-09-26", periods=len(vals), freq="1h")
    return pd.DataFrame({"hour_utc": h, "co2_mmhg": vals, "artifact": art or [False] * len(vals)})


def test_artifact_hours_never_count_and_break_a_run():
    ep = habitat.episodes(_df([3.2, 3.3, 3.4, 3.2], [False, False, True, False]))
    assert [e["hours"] for e in ep] == [2, 1]


def test_one_episode_per_continuous_run():
    ep = habitat.episodes(_df([2.0, 3.1, 3.5, 3.2, 2.0, 3.4]))
    assert [(e["hours"], e["peak"]) for e in ep] == [(3, 3.5), (1, 3.4)]
    assert habitat.episodes(_df([2.0, 2.9, 3.0])) == []   # 3.00 is at the limit, not above


def test_reading_numbers_come_from_the_data_and_match_the_research_replay():
    sm = habitat.summary()
    rr1 = habitat.replay().set_index("mission").loc["RR-1"]
    assert sm["episodes"] == int(rr1["episodes"]) and sm["longest_h"] == int(rr1["longest_ep_h"])
    assert abs(sm["pct_7d_above"] - float(rr1["pct_days_7d_above_2.5"])) < 0.05


def test_seven_day_level_is_nasa_s_and_replay_covers_fourteen_missions():
    assert habitat.SEVEN_DAY_MMHG == 2.5
    assert len(habitat.replay()) == 14
