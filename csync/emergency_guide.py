"""Emergency guide (V3): several kinds of emergency, each a fixed list of steps with a NASA source per step.

C-Sync's role is to spot, order, time and report; the station's alarms and the onboard checklists come first. No treatment,
no drug. Data: data/procedures/emergency_guide.json."""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "procedures", "emergency_guide.json")
RESERVE_MMHG = 490.0   # Tobias & McMillan 2023 (NTRS 20220019247): time left is counted to 490 mmHg (9.5 psia)
STOP_ISOLATING_MIN = 10.0   # same source: at ten minutes or less, stop isolating and retreat


def load(path: str = PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        g = json.load(fh)
    for c in g["cases"]:
        assert c["steps"], c["id"]
        for s in c["steps"]:
            assert s["src"] in g["sources"], (c["id"], s["text"])   # a step without a known source is refused
    return g


def time_to_reserve(p_before: float, p_now: float, minutes_between: float) -> float | None:
    """Minutes left before the cabin reaches 490 mmHg, from two pressure readings (linear, as the crew does with a gauge
    and a timer). None when the pressure is not falling. Raises ValueError on impossible inputs."""
    if minutes_between <= 0 or p_before <= 0 or p_now <= 0:
        raise ValueError("readings must be positive and separated in time")
    rate = (p_before - p_now) / minutes_between   # mmHg per minute
    if rate <= 0:
        return None
    return max(0.0, (p_now - RESERVE_MMHG) / rate)
