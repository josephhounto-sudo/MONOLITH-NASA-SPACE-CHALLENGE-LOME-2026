"""Source adapters: each turns one source into Measurement records (contracts/measurement.schema.json) and nothing else.

Quality control sits here, before any rule sees the data: a missing value is MISSING, a run of identical values is
ARTIFACT (csync.quality.flag_plateaus), everything else is OK. Real NASA data keeps origin REAL_OPEN.
"""
from __future__ import annotations

import json
import math
import os

import jsonschema

from csync.quality import flag_plateaus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, "contracts", "measurement.schema.json"), encoding="utf8"))
EDA_INDICATORS = {"co2_ppm": ("HA01", "ppm"), "temp_c": ("HA02", "degC"), "rh_pct": ("HA03", "%")}


def eda_measurements(times, values, column: str, mission: str, min_len: int = 6) -> list[dict]:
    """NASA OSDR EDA series (one habitat variable) -> Measurements. Habitat is mission context, never scored."""
    indicator, unit = EDA_INDICATORS[column]
    values = list(values)
    flat = set()
    for run in flag_plateaus(values, min_len):
        flat.update(range(run["start"], run["end"] + 1))
    out = []
    for i, (t, v) in enumerate(zip(times, values)):
        missing = v is None or (isinstance(v, float) and math.isnan(v))
        m = {"timestamp_utc": str(t), "indicator_id": indicator, "value": None if missing else float(v), "unit": unit,
             "quality": "MISSING" if missing else ("ARTIFACT" if i in flat else "OK"), "origin": "REAL_OPEN",
             "source_id": f"NASA-OSDR-EDA-{mission}", "evidence_kind": "MISSION_CONTEXT"}
        jsonschema.validate(m, SCHEMA)
        out.append(m)
    return out
