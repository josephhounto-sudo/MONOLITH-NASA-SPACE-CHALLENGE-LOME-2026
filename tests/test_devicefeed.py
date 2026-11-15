"""Device-feed adapter: same engine, bad lines rejected with a reason, a missing indicator never reads Normal."""
import json

from csync import devicefeed as adapters, live


def lines(day, vals):
    inv = {v: k for k, v in adapters.METRICS.items()}
    return "\n".join(json.dumps({"device": "d", "mission_day": day, "metric": inv[i], "value": v}) for i, v in vals.items())


def test_story_values_through_adapter_equal_typed_values():
    d6, d7 = live.story_day(6), live.story_day(7)
    p = adapters.parse(lines(6, d6) + "\n" + lines(7, d7))
    assert not p["rejected"] and p["accepted"] == len(d6) + len(d7)
    assert live.try_it(p["days"][6], p["days"][7]) == live.try_it(d6, d7)


def test_rejects_bad_lines_with_reason_and_keeps_indicator_missing():
    txt = 'nonsense\n{"mission_day":7,"metric":"resting_hr_bpm","value":900}\n{"mission_day":7,"metric":"foo","value":1}\n{"mission_day":3,"metric":"kss","value":4}'
    p = adapters.parse(txt)
    assert p["accepted"] == 0 and len(p["rejected"]) == 4
    assert p["days"][7]["PH01"] is None
    out = live.try_it(live.story_day(6), p["days"][7])
    assert out["states"]["Body"] == "UNKNOWN" and out["states"]["Attention"] == "UNKNOWN"


def test_same_day_readings_are_averaged():
    p = adapters.parse('{"mission_day":6,"metric":"kss","value":4}\n{"mission_day":6,"metric":"kss","value":6}')
    assert p["days"][6]["PS01"] == 5.0
