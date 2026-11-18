"""Split a daily explanation into a verdict, one line per flagged indicator, and the rule.

The capsule text is not rewritten. Numbers come from the capsule signals.
"""


def _num(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def short_verdict(cap, state_words):
    """One short sentence for the screen. The stored situation text is left unchanged."""
    if not isinstance(cap, dict):
        raise ValueError("Pass a decision capsule (a dict). Rebuild the story files, then reload this page.")
    day = cap.get("day")
    states = cap.get("states") if isinstance(cap.get("states"), dict) else {}
    words = state_words if isinstance(state_words, dict) else {}
    away = []
    for dim in ("Body", "Attention", "Morale", "Habitat"):
        state = states.get(dim)
        if state in ("WATCH", "DEGRADED"):
            away.append(f"{dim} {words.get(state, state)}")
    if not isinstance(day, int):
        text = cap.get("situation")
        return text.strip() if isinstance(text, str) and text.strip() else "No comparison is shown for this day."
    if not away:
        if any(states.get(dim) == "UNKNOWN" for dim in ("Body", "Attention", "Morale")):
            return f"Day {day}: personal baseline is still being built."
        return f"Day {day}: nothing is away from this person's own normal."
    return f"Day {day}: " + ", ".join(away) + "."


def why_parts(cap, templates):
    """Return verdict, lines, and the rule sentence (empty if the record has none)."""
    if not isinstance(cap, dict):
        raise ValueError("Pass a decision capsule (a dict). Rebuild the story files, then reload this page.")
    if not isinstance(templates, dict):
        raise ValueError("Pass the interface text dict. Check the string files, then reload.")
    situation = cap.get("situation")
    verdict = situation.strip() if isinstance(situation, str) and situation.strip() else "No comparison is shown for this day."
    signals = cap.get("signals") if isinstance(cap.get("signals"), list) else []
    lines = []
    for sig in signals:
        if not isinstance(sig, dict) or not sig.get("flagged"):
            continue
        name = sig.get("name") if isinstance(sig.get("name"), str) and sig.get("name").strip() else "Reading"
        value, normal, times = sig.get("value"), sig.get("baseline_mean"), sig.get("d")
        unit = sig.get("unit") if isinstance(sig.get("unit"), str) else ""
        if _num(value) and _num(normal) and _num(times):
            lines.append(templates["why_line"].format(
                name=name, value=f"{value:g}", unit=unit, normal=f"{normal:g}", times=f"{times:.1f}"))
        elif _num(value):
            lines.append(templates["why_context"].format(name=name, value=f"{value:g}", unit=unit))
        else:
            lines.append(templates["why_missing"].format(name=name))
    rule = ""
    explanation = cap.get("explanation") if isinstance(cap.get("explanation"), str) else ""
    for chunk in explanation.split(". "):
        piece = chunk.strip()
        if piece.startswith("Rule "):
            rule = piece if piece.endswith(".") else piece + "."
            break
    return {"verdict": verdict, "lines": lines, "rule": rule}
