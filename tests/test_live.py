"""Try-it engine: it must give the same answer as the story run, and a missing value must never read NORMAL. 15/11/2026 · FAIT PAR L'IA."""
import math
import os

import pandas as pd
import pytest

from csync.live import INDICATORS, baseline, story_day, try_it
from csync.rules import Params


def test_story_values_reproduce_the_story_states():
    out = try_it(story_day(6), story_day(7))
    st = pd.read_csv(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/out/states_histoire.csv", index_col=0)
    row = st.loc[7]
    assert out["states"] == {"Body": row["Body"], "Attention": row["Attention"], "Morale": row["Morale"]}


def test_baseline_values_stay_normal():
    mean = {i: float(baseline()[i].mean()) for i in INDICATORS}
    out = try_it(mean, mean)
    assert set(out["states"].values()) == {"NORMAL"}
    assert out["action"] == "CONTINUE"


def test_missing_value_never_reads_normal():
    mean = {i: float(baseline()[i].mean()) for i in INDICATORS}
    day7 = {**mean, "PH09": None}
    out = try_it(mean, day7)
    assert out["states"]["Body"] == "UNKNOWN"


def test_one_bad_day_is_not_enough():
    mean = {i: float(baseline()[i].mean()) for i in INDICATORS}
    bad = {**mean, "PH09": 4.0}
    assert try_it(mean, bad)["states"]["Body"] == "NORMAL"           # rule v3 needs 2 days in a row
    assert try_it(bad, bad)["states"]["Body"] == "WATCH"


def test_two_dimensions_open_the_procedure():
    mean = {i: float(baseline()[i].mean()) for i in INDICATORS}
    bad = {**mean, "PH09": 4.0, "CO01": 400.0}
    out = try_it(bad, bad)
    assert out["action"] == "OPEN_PROCEDURE" and out["procedure_id"] == "PROC-FATIGUE-01"
