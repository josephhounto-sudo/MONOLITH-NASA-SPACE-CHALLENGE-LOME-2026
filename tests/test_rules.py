"""Drift rule behaviour on the reference story (seed 42) and on the control."""
from synthetic.generator import generate
from csync.rules import daily_values, evaluate, event_rule, Params, PROPOSED

def run(variant, prm=Params(), **kw):
    df = generate(variant, seed=42, fast=True, event=(variant == "histoire"), drift=(variant == "histoire"), **kw)
    return df, evaluate(daily_values(df), prm)

def test_baseline_days_are_unknown_never_normal():
    _, (_, _, states, _, _) = run("histoire")
    assert (states.loc[1:5] == "UNKNOWN").all().all()

def test_drift_detected_on_day_7():
    _, (_, _, states, dec, _) = run("histoire", drift_amp=2.5)
    assert dec.set_index("day").at[7, "action"] == "OPEN_PROCEDURE"
    assert dec.set_index("day").at[6, "action"] == "CONTINUE"     # two consecutive days are required

def test_control_has_no_alert_seed42():
    _, (_, _, states, dec, _) = run("temoin")
    assert not (states == "DEGRADED").any().any()
    assert (dec.action == "CONTINUE").all()

def test_proposed_rules_still_detect_amplitude_2():
    _, (_, _, states, dec, _) = run("histoire", prm=PROPOSED, drift_amp=2.5)
    assert (dec.action == "OPEN_PROCEDURE").any()
    assert (states.loc[6:] == "DEGRADED").any().any()

def test_episode_criticality_never_decreases():
    _, (_, _, _, dec, _) = run("histoire")
    crit = list(dec[dec.action == "OPEN_PROCEDURE"].criticality)
    order = {"ROUTINE": 0, "IMPORTANT": 1}
    assert all(order[a] <= order[b] for a, b in zip(crit, crit[1:]))

def test_emergency_opens_immediately():
    df, _ = run("histoire")
    ev = event_rule(df)
    assert len(ev) == 1 and ev[0]["criticality"] == "CRITICAL"


def test_missing_value_after_baseline_is_unknown_and_never_an_alert():
    import pandas as pd
    from csync.rules import evaluate
    cols = ["PH01", "PH09", "CO01", "CO02", "PS01", "PS02", "PS03", "PS04"]
    dv = pd.DataFrame({c: [50.0] * 8 for c in cols}, index=range(1, 9))
    dv.loc[7, "PH01"] = float("nan")          # sensor outage on day 7
    _, _, states, decisions, _ = evaluate(dv)
    assert states.at[7, "Body"] == "UNKNOWN"          # missing data: never NORMAL
    assert states.at[7, "Attention"] == "NORMAL"      # complete data, no drift
    assert decisions.set_index("day").at[7, "action"] == "CONTINUE"   # UNKNOWN is not an alert
