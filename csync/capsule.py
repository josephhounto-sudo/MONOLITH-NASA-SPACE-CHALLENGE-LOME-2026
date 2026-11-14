"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

DecisionCapsule builders (contract: contracts/decision_capsule.schema.json). Owner: M2 (task cards M2-1, M2-2).

The capsule is the ONLY object the UI reads. Every text here is generated from data and checked with
csync.language.banned_hits(). human_decision is always "pending" on the machine side.
ui_hint mapping (provisional, MAJ n°1, M1 validates): CONTINUE -> NOMINAL; OPEN_PROCEDURE + CRITICAL -> ACTION;
OPEN_PROCEDURE ROUTINE/IMPORTANT, PAUSE, REFUSE_RESUME -> FOCUS.
"""
from __future__ import annotations

import json
import math
import os
import re

import pandas as pd

from csync.language import banned_hits
from csync.rules import DIRECTION, DRIFT_INDICATORS, Params

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIMENSIONS = ["Body", "Attention", "Morale", "Mission", "Habitat"]
CONTEXT_DIMENSIONS = ["Mission", "Habitat"]   # decision n°6 (provisional): context only, not evaluated
NAMES = {"PH01": "Resting heart rate", "PH09": "Reported sleep", "CO01": "Reaction time", "CO02": "Reaction-time lapses",
         "PS01": "Sleepiness (KSS)", "PS02": "Stress", "PS03": "Mood", "PS04": "Workload",
         "PH10": "Blood pressure", "PH11": "Body temperature", "PH12": "Blood glucose", "SY01": "Symptom"}
UNITS = {"PH01": "bpm", "PH09": "h", "CO01": "ms", "CO02": "count (>=355 ms)", "PS01": "KSS 1-9", "PS02": "0-10",
         "PS03": "1-5", "PS04": "0-10", "PH10": "mmHg", "PH11": "degC", "PH12": "mg/dL"}
DEFAULT_EVIDENCE = ("SYNTHETIC data (demo story, not a real astronaut): generator csync-synth-0.1, seed 42. "
                    "Detector: drift rule v3 in csync/rules.py, compared with this crew member's own baseline.")


def _strings():
    with open(os.path.join(ROOT, "csync", "config", "strings_en.json"), encoding="utf8") as f:
        return json.load(f)


FIXED_SENTENCE = _strings()["fixed_medical_sentence"]
_REASON_PATTERNS = [
    ("G3", re.compile(r"^G3: (?P<ind>\w+) is stale \((?P<age>\d+) min > (?P<limit>\d+) min\)$")),
    ("G2", re.compile(r"^G2: (?P<ind>\w+) missing$")),
    ("G4", re.compile(r"^G4: (?P<ind>\w+) quality is (?P<quality>\w+)$")),
    ("G8", re.compile(r"^G8: (?P<ind>\w+) timestamped in the future$")),
    ("G9", re.compile(r"^G9: session is (?P<state>\w+), not SUSPENDED$")),
]


def human_reason(reason: str) -> str:
    """Plain-language version of a resume-gate reason. The coded reason (G1-G10) stays in the technical log.

    csync/gate.py is unchanged; unknown formats are returned as they are (never hidden).
    """
    s = _strings()
    templates, names = s["gate_reasons"], s["indicator_names"]
    for code, pat in _REASON_PATTERNS:
        m = pat.match(reason)
        if m:
            g = m.groupdict()
            if "ind" in g:
                g["name"] = names.get(g["ind"], g["ind"])
            if "state" in g:
                g["state"] = g["state"].lower()
            return templates[code].format(**g)
    code = reason.split(":", 1)[0]
    return templates.get(code, reason) if code in ("G1", "G5", "G6", "G7", "G10") else reason


def ui_hint(action: str, criticality: str) -> str:
    if action == "CONTINUE":
        return "NOMINAL"
    if action == "OPEN_PROCEDURE" and criticality == "CRITICAL":
        return "ACTION"
    return "FOCUS"


def _num(x, nd=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    return round(float(x), nd)


SCALE_UNITS = {"KSS 1-9", "0-10", "1-5"}


def _fmt(x, unit=""):
    if x is None:
        return "missing"
    return f"{x:g} (scale {unit})" if unit in SCALE_UNITS else f"{x:g} {unit}"


def _check(text: str) -> str:
    hits = banned_hits(text)
    if hits:
        raise ValueError(f"banned wording in generated text: {hits}")
    return text


def _run_lengths(z: pd.DataFrame, prm: Params) -> pd.DataFrame:
    """Number of consecutive days (ending on each day) with d >= threshold; reset on missing data."""
    runs = pd.DataFrame(0, index=z.index, columns=z.columns)
    for i in z.columns:
        r = 0
        for d in z.index:
            v = z.at[d, i]
            r = 0 if pd.isna(v) else (r + 1 if v >= prm.d_threshold else 0)
            runs.at[d, i] = r
    return runs


def build_capsule(day, states, decisions, z, reference, *, flags=None, prm: Params = Params(),
                  evidence: str = DEFAULT_EVIDENCE, data_origin: str = "SYNTHETIC", open_episode: dict | None = None) -> dict:
    """Daily DecisionCapsule for one day, from the outputs of csync.rules.evaluate().

    open_episode: an event episode still open on this day (e.g. the emergency, until a human closes it). The drift
    decision is unchanged, but the action text no longer says "continue" while that episode is open.
    """
    day = int(day)
    dec = decisions.set_index("day").loc[day] if "day" in decisions.columns else decisions.loc[day]
    action, crit, pid = dec["action"], dec["criticality"], dec.get("procedure_id", "") or ""
    mu, sd, sd_eff = reference["mu"], reference["sd"], reference["sd_eff"]
    runs = _run_lengths(z, prm)
    if flags is None:
        flags = runs >= prm.consecutive_days
        flags.loc[[d for d in flags.index if d <= prm.baseline_days]] = False
    building = day <= prm.baseline_days

    day_states = {dim: str(states.at[day, dim]) for dim in DRIFT_INDICATORS}
    for dim in CONTEXT_DIMENSIONS:
        day_states[dim] = "UNKNOWN"   # never NORMAL: not evaluated in this prototype

    signals, flagged, missing = [], [], []
    for dim, inds in DRIFT_INDICATORS.items():
        for i in inds:
            if i not in z.columns:
                continue
            zi = z.at[day, i]
            value = None if pd.isna(zi) else _num(mu[i] + DIRECTION[i] * zi * sd_eff[i], 1)
            if value is None:
                missing.append(i)
            is_flag = bool(flags.at[day, i])
            sig = {"indicator_id": i, "name": NAMES[i], "dimension": dim, "value": value, "unit": UNITS[i],
                   "baseline_mean": _num(mu[i], 2), "baseline_sd_used": _num(sd_eff[i], 3),
                   "d": None if building else _num(zi, 2), "flagged": is_flag}
            signals.append(sig)
            if is_flag:
                flagged.append((sig, int(runs.at[day, i])))

    out = [k for k, v in day_states.items() if v in ("WATCH", "DEGRADED")]
    unknown = [k for k in DRIFT_INDICATORS if day_states[k] == "UNKNOWN"]
    if building:
        situation = f"Day {day}: personal baseline being built (day {day} of {prm.baseline_days})."
    elif out:
        situation = f"Day {day}: {len(out)} dimension(s) away from the personal baseline: " + \
                    ", ".join(f"{k} ({day_states[k]})" for k in out) + "."
    else:
        situation = f"Day {day}: no evaluated dimension is away from the personal baseline."
    if not building and unknown:
        situation += " Not evaluated today (missing data): " + ", ".join(unknown) + "."

    parts = []
    if building:
        parts.append(f"Days 1 to {prm.baseline_days} build this crew member's personal baseline; no comparison is made yet.")
    else:
        for sig, run in flagged:
            parts.append(f"{sig['name']} ({sig['indicator_id']}) is {_fmt(sig['value'], sig['unit'])} against a personal "
                         f"baseline of {_fmt(sig['baseline_mean'], sig['unit'])} (d = {sig['d']:.1f}, unfavourable side) "
                         f"for {run} days in a row.")
        if not flagged:
            parts.append("No indicator is flagged today.")
        for i in missing:
            parts.append(f"{NAMES[i]} ({i}) is missing today, so its dimension is shown as UNKNOWN, never as NORMAL.")
        parts.append(f"Rule v3: an indicator is flagged when d >= {prm.d_threshold:g} on {prm.consecutive_days} consecutive days; "
                     "1 flagged indicator = WATCH, 2 or more = DEGRADED; 2 dimensions away from baseline open a procedure.")
    explanation = " ".join(parts)

    if action == "OPEN_PROCEDURE":
        text = f"Open procedure {pid} ({crit}). {FIXED_SENTENCE}"
    elif open_episode:
        text = (f"No procedure from the drift rule today. Episode {open_episode['procedure_id']} "
                f"({open_episode['criticality']}) is still open until a human closes it.")
    else:
        text = "Continue the mission plan."
    present = len(signals) - len(missing)
    capsule = {
        "capsule_type": "daily",
        "day": day,
        "states": day_states,
        "situation": _check(situation),
        "signals": signals,
        "evidence": evidence,
        "explanation": _check(explanation),
        "reliability": {"data_completeness": _num(present / len(signals), 2) if signals else None,
                        "missing_indicators": missing,
                        "baseline_status": "building" if building else "ready",
                        "baseline_days": prm.baseline_days,
                        "sd_floor_applied": [i for i in sd_eff.index if not pd.isna(sd_eff[i]) and (pd.isna(sd[i]) or sd_eff[i] > sd[i])],
                        "detector": f"rule v3 (d >= {prm.d_threshold:g}, {prm.consecutive_days} consecutive days)",
                        "context_only": CONTEXT_DIMENSIONS,
                        "data_origin": data_origin},
        "action": {"type": action, "procedure_id": pid, "criticality": crit, "text": _check(text)},
        "human_decision": "pending",
        "reevaluation": f"Next evaluation: day {day + 1} daily check-in.",
        "ui_hint": ui_hint(action, crit),
    }
    if open_episode:
        capsule["open_episode"] = open_episode
    return capsule


def build_emergency_capsule(event: dict, guided: list[dict], states: dict, send_status: dict,
                            evidence: str = DEFAULT_EVIDENCE) -> dict:
    """Event capsule: a ticked symptom opens PROC-EMERGENCY-01 at once (CRITICAL). No threshold is applied to values."""
    t = event["timestamp_utc"]
    day, hhmm = event["day"], t[11:16]
    sym = event["trigger"].split(";")[0].replace("_", " ")
    zone = next((p.split("=")[1] for p in event["trigger"].split(";") if p.startswith("zone=")), "not given")
    signals = []
    for g in guided:
        name = "Heart rate" if g["indicator_id"] == "PH01" else NAMES.get(g["indicator_id"], g["indicator_id"])
        s = {"indicator_id": g["indicator_id"], "name": name,
             "value": g["value"], "unit": UNITS.get(g["indicator_id"], g.get("unit", "")),
             "timestamp_utc": g["timestamp_utc"], "source": "GUIDED"}
        if g.get("value_text") in ("SYS", "DIA"):
            s["component"] = g["value_text"]
        if g["indicator_id"] == "PH12":
            s["label"] = "no NASA in-flight reference"
        signals.append(s)
    explanation = ("A symptom was ticked by the crew member. Any ticked symptom opens the guided emergency procedure at once, "
                   "whatever the drift state. Guided measurements are shown as recorded; no threshold is applied. "
                   "Blood glucose has no NASA in-flight reference.")
    return {
        "capsule_type": "emergency",
        "day": day,
        "time_utc": hhmm,
        "states": states,
        "situation": _check(f"Day {day}, {hhmm} UTC: symptom reported ({sym}, zone: {zone}). Guided emergency procedure opened."),
        "signals": signals,
        "evidence": evidence,
        "explanation": _check(explanation),
        "reliability": {"symptom_source": "SELF_REPORTED", "measurements_source": "GUIDED",
                        "thresholds_applied": False, "data_origin": "SYNTHETIC"},
        "action": {"type": event["action"], "procedure_id": event["procedure_id"], "criticality": event["criticality"],
                   "text": _check(f"Open procedure {event['procedure_id']} (CRITICAL). {FIXED_SENTENCE}")},
        "human_decision": "pending",
        "reevaluation": "Re-evaluated when the guided measurements are complete and when the ground answers.",
        "ui_hint": ui_hint(event["action"], event["criticality"]),
        "send_queue": send_status,
    }


def build_resume_capsule(day: int, request_time_utc: str, decision: str, reasons: list[str], gate_inputs: dict,
                         states: dict, override_reasons: list[str] | None = None, criticality: str = "CRITICAL",
                         evidence: str = DEFAULT_EVIDENCE) -> dict:
    """Resume-request capsule, from csync.gate.resume_gate(). The override never changes the decision on its own."""
    hhmm = request_time_utc[11:16]
    ok = decision == "RESUME_AUTHORIZED"
    action = "CONTINUE" if ok else "REFUSE_RESUME"
    text = "Resume authorised by the gate; the human decision is still pending." if ok else \
        "Resume refused. Take new guided measurements for the items listed, then request again."
    explanation = " ".join(human_reason(r) for r in reasons)
    explanation += " " + _strings()["gate_reasons"]["G6"]
    return {
        "capsule_type": "resume",
        "day": day,
        "time_utc": hhmm,
        "states": states,
        "situation": _check(f"Day {day}, {hhmm} UTC: resume request after procedure {gate_inputs['procedure_id']}."),
        "signals": gate_inputs["measurements"],
        "evidence": evidence,
        "explanation": _check(explanation),
        "reliability": {"gate_reasons": reasons, "gate_reasons_text": [human_reason(r) for r in reasons], "gate_reasons_with_override": override_reasons or [],
                        "max_age_min": gate_inputs.get("max_age_min", 10), "data_origin": "SYNTHETIC"},
        "action": {"type": action, "procedure_id": gate_inputs["procedure_id"], "criticality": criticality,
                   "text": _check(text), "gate_decision": decision},
        "human_decision": "pending",
        "reevaluation": "Re-evaluated at the next resume request.",
        "ui_hint": ui_hint(action, criticality),
        "gate_inputs": gate_inputs,
    }
