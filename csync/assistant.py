"""Scripted assistant for the V2 story screens. Deterministic, offline, no language model.

It reads ONE decision capsule and fixed text templates from csync/config/strings_*.json.
Every number it says is copied from the capsule or from the rule parameters (csync.rules.Params);
it never computes a new fact. A free-text model is out of scope for V2 (it can invent, needs a network).
"""
from __future__ import annotations

import re

from csync.rules import Params

QUESTIONS = ("why", "data", "limits")
MAX_SHOWN_DRIFT = 2                       # at most two indicators are named per answer (the largest d)
CREW_DIMENSIONS = ("Body", "Attention", "Morale")
UNITS = {"bpm": " bpm", "ms": " ms", "h": " h"}   # any other unit is left out rather than shown half-readable


def _num(v: float) -> str:
    return f"{round(float(v), 1):g}"


def _unit(u: str) -> str:
    return UNITS.get(u, "")


def _why(cap: dict, A: dict, strings: dict) -> list[str]:
    crew = A["crew_name"]
    kind = cap.get("capsule_type", "daily")
    if kind == "emergency":
        m = re.search(r"\((.+?), zone", cap["situation"])
        symptom = m.group(1) if m else "a symptom"
        return [A["emergency"].format(crew=crew, symptom=symptom, time=cap["time_utc"]), strings["fixed_medical_sentence"]]
    if kind == "resume":
        gi = cap["gate_inputs"]
        limit = gi["max_age_min"]
        names = strings["indicator_names"]
        out = [A["resume_stale"].format(name=names.get(m["indicator_id"], m["indicator_id"]), age=m["age_min"], limit=limit)
               for m in gi["measurements"] if m["age_min"] > limit]
        if cap["action"]["type"] == "REFUSE_RESUME":
            out.append(A["resume_refused"])
        return out
    states = [cap["states"][d] for d in ("Body", "Attention", "Morale")]
    if all(s == "UNKNOWN" for s in states) and cap["reliability"].get("baseline_status") != "ready":
        return [A["learning"].format(crew=crew, n=cap["day"]), *_habitat_line(cap, A)]
    out = []
    if cap["reliability"].get("missing_indicators"):
        out.append(A["missing"])
    flagged = sorted((s for s in cap["signals"] if s["flagged"] and s["dimension"] in CREW_DIMENSIONS),
                     key=lambda s: -s["d"])[:MAX_SHOWN_DRIFT]
    if not flagged:
        out.append(A["calm"].format(crew=crew))
    else:
        for s in flagged:
            out.append(A["drift"].format(name=s["name"], value=_num(s["value"]), mean=_num(s["baseline_mean"]), unit=_unit(s["unit"])))
        prm = Params()
        out.append(A["rule"].format(crew=crew, thr=_num(prm.d_threshold), days=prm.consecutive_days))
    out.extend(_habitat_line(cap, A))
    return out


def _habitat_line(cap: dict, A: dict) -> list[str]:
    """Cabin air line, only when the capsule says the habitat state was computed from real NASA data."""
    if not cap["reliability"].get("habitat_in_calculation"):
        return []
    sig = next((s for s in cap["signals"] if s["dimension"] == "Habitat"), None)
    if sig is None:
        return []
    state = cap["states"]["Habitat"]
    limit = _num(sig["limit"])
    if state == "WATCH":
        return [A["habitat_watch"].format(hours=sig["hours_above"], limit=limit)]
    if state == "NORMAL":
        return [A["habitat_ok"].format(limit=limit)]
    return [A["habitat_unknown"]]


def _data(cap: dict, A: dict) -> list[str]:
    out = [A["data_origin"] if cap["reliability"].get("data_origin") == "SYNTHETIC" else A["data_origin_unstated"]]
    rel = cap["reliability"]
    if rel.get("habitat_in_calculation"):
        sig = next((s for s in cap["signals"] if s["dimension"] == "Habitat"), None)
        if sig is not None:
            out.append(A["data_context_mission"])
            out.append(A["data_habitat_real"].format(limit=_num(sig["limit"])))
            out.append(A["data_habitat_scope"])
    elif rel.get("context_only"):
        out.append(A["data_context"])
        out.append(A["data_nasa"])
    return out


def _limits(A: dict) -> list[str]:
    crew = A["crew_name"]
    return [A["limits_1"].format(crew=crew), A["limits_2"], A["limits_3"], A["limits_4"]]


def answer(cap: dict, qid: str, strings: dict) -> list[str]:
    """Lines the assistant says for one capsule and one preset question. Unknown question -> ValueError."""
    if qid not in QUESTIONS:
        raise ValueError(f"unknown question: {qid!r}")
    A = strings["assistant"]
    if qid == "why":
        return _why(cap, A, strings)
    if qid == "data":
        return _data(cap, A)
    return _limits(A)
