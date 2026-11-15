"""Device-feed adapter: JSON lines from any device that follows this format -> the daily values rule v3 reads.

One line = {"device": "wrist-01", "mission_day": 6, "metric": "sleep_hours", "value": 5.5}.
Several lines for the same day and metric are averaged. A line that is malformed, has an unknown metric, a non-numeric value or a
value outside the format-check range is REJECTED and listed with its reason: its indicator stays missing (UNKNOWN), never normal.
The ranges only catch format errors (a heart rate of 900); they are not clinical thresholds. No real device is connected yet.
15/11/2026 · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
"""
from __future__ import annotations

import json
import math

METRICS = {"sleep_hours": "PH09", "resting_hr_bpm": "PH01", "pvt_mean_rt_ms": "CO01", "pvt_lapses": "CO02",
           "kss": "PS01", "stress": "PS02", "mood": "PS03", "load": "PS04"}
FORMAT_RANGE = {"PH09": (0, 24), "PH01": (20, 250), "CO01": (100, 1500), "CO02": (0, 200),
                "PS01": (1, 9), "PS02": (0, 10), "PS03": (1, 5), "PS04": (0, 10)}
DAYS = (6, 7)


def parse(text: str) -> dict:
    """Returns {"days": {6: {indicator: mean or None}, 7: {...}}, "accepted": n, "rejected": [(line_no, reason)]}."""
    sums: dict = {}
    accepted, rejected = 0, []
    for n, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rec = json.loads(raw)
            day, metric, value = rec["mission_day"], rec["metric"], rec["value"]
        except (ValueError, KeyError, TypeError):
            rejected.append((n, "not a JSON object with mission_day, metric, value"))
            continue
        ind = METRICS.get(metric)
        if ind is None:
            rejected.append((n, f"unknown metric '{metric}'"))
        elif day not in DAYS or isinstance(day, bool):
            rejected.append((n, f"mission_day must be one of {DAYS}"))
        elif isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            rejected.append((n, "value is not a finite number"))
        elif not FORMAT_RANGE[ind][0] <= value <= FORMAT_RANGE[ind][1]:
            rejected.append((n, f"value {value} outside the format-check range {FORMAT_RANGE[ind]}"))
        else:
            sums.setdefault((day, ind), []).append(float(value))
            accepted += 1
    days = {d: {i: (sum(sums[(d, i)]) / len(sums[(d, i)]) if (d, i) in sums else None) for i in METRICS.values()} for d in DAYS}
    return {"days": days, "accepted": accepted, "rejected": rejected}
