"""Regenerate the story data and every capsule the UI shows. Owner: M2 (task card M2-2).

Run: python scripts/run_story.py            (writes data/out/)
     python scripts/run_story.py --out DIR  (writes elsewhere, used by the tests)
Outputs per variant: measurements_<v>.csv, states_<v>.csv, decisions_<v>.csv, capsules_<v>.json.
capsules_histoire.json also holds the day-9 emergency capsule and the day-10 resume capsule.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import jsonschema  # noqa: E402

from csync import habitat  # noqa: E402
from csync.capsule import build_capsule, build_emergency_capsule, build_resume_capsule  # noqa: E402
from csync.gate import resume_gate  # noqa: E402
from csync.rules import daily_values, evaluate, event_rule  # noqa: E402
from csync.sendqueue import deliver, message_id  # noqa: E402
from synthetic.generator import generate, ts  # noqa: E402

SCHEMA = json.load(open(os.path.join(ROOT, "contracts", "decision_capsule.schema.json"), encoding="utf8"))
# Provisional values (MAJ n°1, M1 validates): story = drift_amp 2.5 + fast mode, rule v3 Params().
# The sensor variant needs fast=False: the generator applies the outage only in full wrist mode.
VARIANTS = (
    ("histoire", {"drift_amp": 2.5, "fast": True}),
    ("temoin", {"drift": False, "event": False, "fast": True}),
    ("capteur", {"drift": False, "event": False, "fast": False, "outage": (ts(7, 1), ts(7, 7))}),
)
LINK_DOWN, LINK_UP = ts(9, 13), ts(9, 19)          # story: link cut on day 9, 13:00-19:00
REPORT_TIME = ts(9, 14, 20)                         # story: report created 14:20
HEARTBEAT_MIN = 30                                  # demo parameter (same cadence as tests/test_sendqueue.py)
RESUME_REQUEST = ts(10, 9, 0)                       # story: resume requested day 10, 09:00


ALLOWED_PROCEDURES = {"PROC-FATIGUE-01", "PROC-EMERGENCY-01"}   # add an id only together with its data/procedures file


def load_procedure(pid):
    if pid not in ALLOWED_PROCEDURES:
        raise ValueError(f"unknown procedure_id: {pid!r}")
    with open(os.path.join(ROOT, "data", "procedures", f"{pid}.json"), encoding="utf8") as f:
        return json.load(f)


def send_status(report_payload):
    """Queue the report + heartbeats during the cut; 3 duplicates, queued batch reversed (story)."""
    report = {"created": REPORT_TIME, "payload_type": "report", "payload": report_payload}
    report["message_id"] = message_id({"created": REPORT_TIME, "payload": report_payload})
    msgs = [report]
    t = LINK_DOWN
    while t < LINK_UP:
        hb = {"created": t, "payload_type": "heartbeat", "payload": {}}
        hb["message_id"] = message_id({"created": t, "payload_type": "heartbeat"})
        msgs.append(hb)
        t += timedelta(minutes=HEARTBEAT_MIN)
    arrivals, ground = deliver(msgs, LINK_DOWN, LINK_UP, duplicates=(0, 4, 8), reverse_queued=True)
    rep_arrivals = [a for a in arrivals if a["message_id"] == report["message_id"]]
    rep_ground = [g for g in ground if g["message_id"] == report["message_id"]]
    iso = lambda x: x.isoformat(timespec="minutes")  # noqa: E731
    return {"link_down_utc": iso(LINK_DOWN), "link_up_utc": iso(LINK_UP),
            "report_message_id": report["message_id"], "report_created_utc": iso(REPORT_TIME),
            # first physical reception. NB: sendqueue.ground_view keeps the first copy in list order, which here is
            # the duplicate (19:25); reported to M1, sendqueue.py is not changed by this task.
            "report_received_utc": iso(min(a["received"] for a in rep_arrivals)),
            "ground_view_received_utc": iso(rep_ground[0]["received"]),
            "report_arrivals_including_duplicates": len(rep_arrivals), "report_deliveries_to_ground": len(rep_ground),
            "messages_queued": len(msgs), "arrivals_total": len(arrivals), "duplicates_dropped": len(arrivals) - len(ground),
            "ground_order_by_creation": [g["message_id"] for g in ground] ==
                                        [m["message_id"] for m in sorted(msgs, key=lambda m: m["created"])],
            "ground_delay_min": 20}


def story_events(df, states, episode_crit, hab):
    caps = []
    for ev in event_rule(df):
        t = datetime.fromisoformat(ev["timestamp_utc"])
        day = (t - ts(1, 0)).days + 1
        ev = {**ev, "day": day}
        guided = df[(df.source_id == "GUIDED") & (df.day == day)].to_dict("records")
        day_states = {**{k: str(v) for k, v in states.loc[day].items()}, "Mission": "UNKNOWN", "Habitat": hab[day]["state"]}
        report = {"day": day, "symptom": ev["trigger"],
                  "guided": [{k: g[k] for k in ("timestamp_utc", "indicator_id", "value", "value_text", "unit")} for g in guided]}
        caps.append(build_emergency_capsule(ev, guided, day_states, send_status(report)))
        # resume request on the next day (act 3)
        proc = load_procedure(ev["procedure_id"])
        rday = RESUME_REQUEST
        g10 = df[(df.source_id == "GUIDED") & (df.day == day + 1)]
        meas = [{"indicator_id": r.indicator_id, "timestamp": datetime.fromisoformat(r.timestamp_utc),
                 "quality": r.quality, "source": r.source_id} for r in g10.itertuples()]
        gate_proc = {k: proc.get(k) for k in ("prerequisites", "no_physical_prereq", "override_policy")}
        decision, reasons = resume_gate(rday, meas, gate_proc)
        d_ovr, reasons_ovr = resume_gate(rday, meas, gate_proc, override={"by": "Commander"})
        assert d_ovr == decision or decision == "RESUME_AUTHORIZED", "override must never change a refusal"
        gate_inputs = {"procedure_id": ev["procedure_id"], "request_time_utc": rday.isoformat(timespec="minutes"),
                       "measurements": [{**m, "timestamp": m["timestamp"].isoformat(timespec="minutes"),
                                         "age_min": round((rday - m["timestamp"]).total_seconds() / 60)} for m in meas],
                       "max_age_min": 10}
        r_states = {**{k: str(v) for k, v in states.loc[day + 1].items()}, "Mission": "UNKNOWN", "Habitat": hab[day + 1]["state"]}
        caps.append(build_resume_capsule(day + 1, gate_inputs["request_time_utc"], decision, reasons, gate_inputs,
                                         r_states, override_reasons=reasons_ovr, criticality=episode_crit))
    return caps


def write_trends(df, z, flags, ref, path):
    """Daily value, personal baseline and flag threshold per drift indicator, for the 'indicators over time' charts."""
    from csync.rules import DIRECTION, Params
    dv = daily_values(df)
    units = df.drop_duplicates("indicator_id").set_index("indicator_id")["unit"].to_dict()
    prm = Params()
    out = {"_header": "Generated by scripts/run_story.py. Synthetic crew (csync-synth-0.1, seed 42). Baseline = days 1-5. "
                      "The threshold is a design parameter, never a clinical limit.", "indicators": {}}
    for ind in z.columns:
        mu, sd = float(ref["mu"][ind]), float(ref["sd_eff"][ind])
        out["indicators"][ind] = {
            "unit": units.get(ind, ""), "direction": DIRECTION[ind], "baseline_mean": round(mu, 3),
            "threshold": round(mu + DIRECTION[ind] * prm.d_threshold * sd, 3),
            "days": [{"day": int(d), "value": None if dv.at[d, ind] != dv.at[d, ind] else round(float(dv.at[d, ind]), 2),
                      "flagged": bool(flags.at[d, ind])} for d in dv.index]}
    with open(path, "w", encoding="utf8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)


def main(out):
    os.makedirs(out, exist_ok=True)
    summary = {}
    hab = habitat.story_days()          # real NASA ISS cabin data, days 1-10 (same for every variant)
    for variant, kw in VARIANTS:
        df = generate(variant, seed=42, **kw)
        df.to_csv(os.path.join(out, f"measurements_{variant}.csv"), index=False)
        z, flags, states, dec, ref = evaluate(daily_values(df))
        states.to_csv(os.path.join(out, f"states_{variant}.csv"))
        dec.to_csv(os.path.join(out, f"decisions_{variant}.csv"), index=False)
        write_trends(df, z, flags, ref, os.path.join(out, f"trends_{variant}.json"))
        events = story_events(df, states, "CRITICAL", hab)
        em = [c for c in events if c["capsule_type"] == "emergency"]
        first = min((c["day"] for c in em), default=None)
        # the emergency episode stays open after its day until a human closes it (no closing event in the story)
        episode = {"procedure_id": em[0]["action"]["procedure_id"], "criticality": "CRITICAL",
                   "opened_utc": f"day {first}, {em[0]['time_utc']}"} if em else None
        caps = [build_capsule(d, states, dec, z, ref, flags=flags,
                              open_episode=episode if (first is not None and d > first) else None,
                              habitat=hab[int(d)]) for d in states.index]
        caps += events
        for c in caps:
            jsonschema.validate(c, SCHEMA)   # invalid capsule -> stop, never shown
        with open(os.path.join(out, f"capsules_{variant}.json"), "w", encoding="utf8") as f:
            json.dump(caps, f, indent=1, ensure_ascii=False)
        summary[variant] = caps
        print(variant, "->", int((dec.action == "OPEN_PROCEDURE").sum()), "procedure day(s) | events:", len(event_rule(df)),
              "| capsules:", len(caps))
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "out"))
    main(ap.parse_args().out)
