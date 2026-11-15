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


# PMData (OSF vx4bk): subjective wellness and Fitbit resting heart rate.
# Scales are the file's own 1-5 scores, not the prototype's KSS or 0-10 scales.
PMDATA_FIELDS = {
    "sleep_duration_h": ("PH09", "h", "SELF_REPORTED"),
    "stress": ("PS02", "1-5", "SELF_REPORTED"),
    "mood": ("PS03", "1-5", "SELF_REPORTED"),
    "resting_heart_rate": ("PH01", "bpm", "DIRECT_MEASUREMENT"),
}


def pmdata_measurements(participant: str, rows: list[dict]) -> list[dict]:
    """One PMData participant -> Measurement records.

    rows: {"timestamp_utc", "field", "value"}. field is a key of PMDATA_FIELDS.
    A null value, or a resting heart rate of 0 (the file's empty day: date null and value 0),
    is MISSING. No plateau rule: a repeated self-report can be real.
    """
    out = []
    for row in rows:
        indicator, unit, kind = PMDATA_FIELDS[row["field"]]
        v = row["value"]
        missing = v is None or (isinstance(v, float) and math.isnan(v)) or (row["field"] == "resting_heart_rate" and v <= 0)
        m = {"timestamp_utc": row["timestamp_utc"], "indicator_id": indicator,
             "value": None if missing else float(v), "unit": unit,
             "quality": "MISSING" if missing else "OK", "origin": "REAL_OPEN",
             "source_id": f"PMDATA-{participant}", "evidence_kind": kind}
        jsonschema.validate(m, SCHEMA)
        out.append(m)
    return out


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
