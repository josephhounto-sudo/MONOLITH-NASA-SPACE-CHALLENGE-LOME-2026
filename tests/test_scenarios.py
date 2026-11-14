"""M4-2: compare the expected results (written BEFORE running, data/scenarios/*.json) with the drift rule output.

If a case fails, do NOT edit the expected file: record the gap in docs/TEST_DEVIATIONS.md and tell M1.
A null expected value means the story documents do not state it; it is not checked.
Added for M4 (14/11 ~15:30, assistant, M4 human review to do): the events already written in the scenario files
(emergency time, report at the ground, resume request), T1 on every variant, data labels, sensor outage rows.
"""
import importlib.util
import json
import os
from datetime import datetime

import pytest

from csync.gate import resume_gate
from csync.rules import DRIFT_INDICATORS, daily_values, evaluate, event_rule
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


# ---------------------------------------------------------------- events written in the scenario files (M4)
def event(sid, etype):
    return next(e for e in load(sid)["events"] if e["type"] == etype)


def clock(day, hhmm):
    h, m = map(int, hhmm.split(":"))
    return ts(day, h, m)


def run_story_module():
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_emergency_opens_at_the_symptom_time():
    """T4: the ticked symptom opens the procedure at once (same minute), not days later."""
    e = event("histoire", "SY01")
    df, _, _ = run("histoire")
    g = event_rule(df)[0]
    assert datetime.fromisoformat(g["timestamp_utc"]) == clock(e["day"], e["time_utc"])
    assert g["trigger"] == e["value_text"]


def test_report_reaches_the_ground_exactly_once():
    """T5: 3 duplicates injected and the queued batch reversed; the ground keeps one copy."""
    e = event("histoire", "REPORT")
    q = run_story_module().send_status({"day": e["day"]})
    assert q["report_created_utc"] == clock(e["day"], e["created_utc"]).isoformat(timespec="minutes")
    assert q["report_deliveries_to_ground"] == e["deliveries"]
    assert q["ground_order_by_creation"]


def test_report_reception_time_recorded_by_the_ground():
    e = event("histoire", "REPORT")
    q = run_story_module().send_status({"day": e["day"]})
    assert q["ground_view_received_utc"] == clock(e["day"], e["received_utc"]).isoformat(timespec="minutes")


def test_resume_request_refused_even_with_override():
    """Act 3 (G3, G6): guided measurements of day 10 from the generator, prerequisites from PROC-EMERGENCY-01."""
    e = event("histoire", "RESUME_REQUEST")
    df, _, _ = run("histoire")
    with open(os.path.join(ROOT, "data", "procedures", "PROC-EMERGENCY-01.json"), encoding="utf8") as f:
        proc = json.load(f)
    gate_proc = {k: proc.get(k) for k in ("prerequisites", "no_physical_prereq", "override_policy")}
    meas = [{"indicator_id": r.indicator_id, "timestamp": datetime.fromisoformat(r.timestamp_utc),
             "quality": r.quality, "source": r.source_id}
            for r in df[(df.source_id == "GUIDED") & (df.day == e["day"])].itertuples()]
    request = clock(e["day"], e["time_utc"])
    decision, reasons = resume_gate(request, meas, gate_proc)
    decision_ovr, reasons_ovr = resume_gate(request, meas, gate_proc, override={"by": "Commander"})
    assert decision == e["expected"] and any(e["expected_reason"] in r for r in reasons)
    assert decision_ovr == e["with_override"] and any(r.startswith("G6") for r in reasons_ovr)


# ---------------------------------------------------------------- data checks (T1, labels, outage)
@pytest.mark.parametrize("sid", ["histoire", "temoin", "capteur"])
def test_missing_data_is_never_normal(sid):
    """T1 on every day and dimension: a missing drift indicator never gives NORMAL."""
    df, states, _ = run(sid)
    dv = daily_values(df)
    bad = [(d, dim) for d in states.index for dim, inds in DRIFT_INDICATORS.items()
           if states.at[d, dim] == "NORMAL" and dv.loc[d, [i for i in inds if i in dv.columns]].isna().any()]
    assert not bad, f"{sid}: NORMAL with missing data on {bad}"


@pytest.mark.parametrize("sid", ["histoire", "temoin", "capteur"])
def test_every_row_is_labelled_synthetic_with_generator_and_seed(sid):
    """M4 card: each data set carries origin SYNTHETIC, the generator version and its seed; quality OK/MISSING/ARTIFACT."""
    s = load(sid)
    df, _, _ = run(sid)
    assert set(df.origin) == {"SYNTHETIC"}
    assert set(df.generator_version) == {s["generator_version"]}
    assert {int(x) for x in df.seed} == {s["seed"]}
    assert set(df.quality) <= {"OK", "MISSING", "ARTIFACT"}


def test_sensor_outage_rows_are_missing_not_zero():
    """T3: every wrist reading inside the outage window is MISSING with no value (never a made-up number)."""
    e = event("capteur", "SENSOR_OUTAGE")
    df, _, _ = run("capteur")
    t = df.timestamp_utc.map(datetime.fromisoformat)
    inside = df[(df.source_id == "WRIST") & (df.indicator_id == e["indicator_id"]) &
                (t >= clock(e["day"], e["from_utc"])) & (t < clock(e["day"], e["to_utc"]))]
    assert len(inside) == 6 * 12                     # 6 h of 5-minute readings
    assert set(inside.quality) == {"MISSING"} and inside.value.isna().all()
