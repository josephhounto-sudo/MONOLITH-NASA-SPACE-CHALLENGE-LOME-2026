"""Prototype: offline explainer (registry id onboard_explainer, V3 20/11/2026).

The promise is a small on-device language model that retells a capsule in plain words. The part that makes it safe is not
the model but the CHECK every sentence must pass: each number must be found in the capsule, no banned medical wording.
This prototype builds that check first, with a template retelling as the baseline any future model has to beat.
No model, no network: a model is only worth adding if it passes the same check."""
from __future__ import annotations

import json
import re

from csync.language import banned_hits

WORD = {"NORMAL": "normal", "WATCH": "watch", "DEGRADED": "degraded", "UNKNOWN": "no reading yet"}
NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?")
MAX_SIGNALS = 3


def _n(x: float) -> str:
    return f"{x:g}"


def capsule_numbers(cap: dict) -> set[str]:
    """Every number written anywhere in the capsule (fields and texts), in one canonical form (270.0 and 270 are the same)."""
    return {_n(float(x)) for x in NUM.findall(json.dumps(cap, ensure_ascii=False))}


def explain(cap: dict) -> list[str]:
    """Plain retelling of a daily capsule: the day, the states in words, the strongest flagged signals with the usual value."""
    assert "day" in cap and "states" in cap, "not a daily capsule"
    lines = [f"Day {cap['day']}."]
    off = [k for k, v in cap["states"].items() if v in ("WATCH", "DEGRADED")]
    lines.append(("Away from this person's usual: " + ", ".join(f"{k} ({WORD[cap['states'][k]]})" for k in off) + ".") if off
                 else "Nothing away from this person's usual today.")
    personal = [s for s in cap.get("signals", []) if s.get("flagged") and isinstance(s.get("d"), (int, float))
                and isinstance(s.get("value"), (int, float)) and isinstance(s.get("baseline_mean"), (int, float))]
    flagged = sorted(personal, key=lambda s: -abs(s["d"]))[:MAX_SIGNALS]
    for s in flagged:
        lines.append(f"{s['name']}: {_n(s['value'])} today, usually about {_n(s['baseline_mean'])}.")
    lines.append("This is a reading of the data, not a medical opinion; the crew medical officer decides.")
    return lines


def check(lines: list[str], cap: dict) -> list[str]:
    """Problems found: numbers not in the capsule, banned wording. Empty list = the text may be shown."""
    known = capsule_numbers(cap)
    out = []
    for line in lines:
        out += [f"untraced number {n!r}: {line}" for n in NUM.findall(line) if _n(float(n)) not in known]
        out += [f"banned word {w!r}: {line}" for w in banned_hits(line)]
    return out
