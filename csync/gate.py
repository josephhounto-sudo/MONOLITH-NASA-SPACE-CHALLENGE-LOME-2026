"""Resume gate: data-driven, fails closed. Acceptance cases G1-G10 are in tests/test_gate.py."""
from __future__ import annotations

def resume_gate(request_time, measurements, procedure, session_state="SUSPENDED", override=None,
                now=None, pending_lock=False, max_age_min=10):
    """Return (decision, reasons). decision is RESUME_AUTHORIZED or REFUSE_RESUME.

    procedure = {"prerequisites": [{"indicator_id", "max_age_min", "sources"}], "no_physical_prereq": bool,
                 "override_policy": dict | None}
    measurements = [{"indicator_id", "timestamp", "quality", "source"}]
    A Commander override is logged but never authorises a resume on its own.
    """
    now = now or request_time
    if pending_lock:
        return "REFUSE_RESUME", ["G10: another resume request is already being processed"]
    if session_state != "SUSPENDED":
        return "REFUSE_RESUME", [f"G9: session is {session_state}, not SUSPENDED"]
    if procedure.get("override_policy") is None:
        return "REFUSE_RESUME", ["G5: override policy missing or invalid"]
    prereq = procedure.get("prerequisites", [])
    if not prereq and not procedure.get("no_physical_prereq"):
        return "REFUSE_RESUME", ["G7: the procedure declares no prerequisite"]
    reasons, ok = [], True
    for pr in prereq:
        ind, limit = pr["indicator_id"], pr.get("max_age_min", max_age_min)
        cands = [m for m in measurements if m["indicator_id"] == ind and m.get("source") in pr.get("sources", ["GUIDED"])]
        if not cands:
            ok = False; reasons.append(f"G2: {ind} missing"); continue
        m = max(cands, key=lambda x: x["timestamp"])
        if m["timestamp"] >= now:
            ok = False; reasons.append(f"G8: {ind} timestamped in the future"); continue
        if m["quality"] != "OK":
            ok = False; reasons.append(f"G4: {ind} quality is {m['quality']}"); continue
        age = (request_time - m["timestamp"]).total_seconds() / 60
        if age > limit:
            ok = False; reasons.append(f"G3: {ind} is stale ({age:.0f} min > {limit} min)")
    if not ok:
        if override:
            reasons.append("G6: Commander override logged; it never authorises a resume on its own")
        return "REFUSE_RESUME", reasons
    return "RESUME_AUTHORIZED", ["G1: all prerequisites present, valid and recent"]
