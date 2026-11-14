"""M4-2: compare the expected results (written BEFORE running, data/scenarios/*.json) with the drift rule output.

If a case fails, do NOT edit the expected file: record the gap in docs/TEST_DEVIATIONS.md and tell M1.
A null expected value means the story documents do not state it; it is not checked.
"""
import json
import os

import pytest

from csync.rules import daily_values, evaluate, event_rule
from synthetic.generator import generate, ts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIMS = ("Body", "Attention", "Morale")


def load(sid):
    with open(os.path.join(ROOT, "data", "scenarios", f"{sid}.json"), encoding="utf8") as f:
        return json.load(f)


def run(sid):
    kw = dict(load(sid)["expected"]["generate_kwargs"])
    seed = kw.pop("seed")
    if "outage" in kw:  # stored as text in the scenario file; the outage window is day 7, 01:00-07:00
        kw["outage"] = (ts(7, 1), ts(7, 7))
    df = generate(sid, seed=seed, **kw)
    _, _, states, dec, _ = evaluate(daily_values(df))
    return df, states, dec.set_index("day")


# DEV-01 (Morale WATCH without drift) was closed on 14/11 by the calibrated Params() (threshold 1.5 + absolute floors);
# the expected files were never edited. See docs/TEST_DEVIATIONS.md.
KNOWN_DEVIATIONS = {}


def cases():
    for sid in ("histoire", "temoin", "capteur"):
        for d, exp in load(sid)["expected"]["days"].items():
            reason = KNOWN_DEVIATIONS.get((sid, int(d)))
            marks = [pytest.mark.xfail(strict=True, reason=reason)] if reason else []
            yield pytest.param(sid, int(d), exp, id=f"{sid}-day{d}", marks=marks)


@pytest.mark.parametrize("sid,day,exp", list(cases()))
def test_day_matches_expected(sid, day, exp):
    _, states, dec = run(sid)
    got = {k: states.at[day, k] for k in DIMS}
    got["decision"] = dec.at[day, "action"]
    gaps = {k: (v, got[k]) for k, v in exp.items() if v is not None and got[k] != v}
    assert not gaps, f"{sid} day {day}: expected vs observed {gaps}"


@pytest.mark.parametrize("sid", ["histoire", "temoin", "capteur"])
def test_number_of_procedure_days(sid):
    _, _, dec = run(sid)
    assert int((dec.action == "OPEN_PROCEDURE").sum()) == load(sid)["expected"]["procedure_days"]


@pytest.mark.parametrize("sid", ["histoire", "temoin", "capteur"])
def test_emergency_events(sid):
    df, _, _ = run(sid)
    expected = [e for e in load(sid)["events"] if e["type"] == "SY01"]
    got = event_rule(df)
    assert len(got) == len(expected)
    for e, g in zip(expected, got):
        assert g["procedure_id"] == e["procedure_id"] and g["criticality"] == e["criticality"]
