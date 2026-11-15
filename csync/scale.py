"""Evidence at scale: everything here is computed when called, from the raw files and the shipped rule. Nothing is typed in.
1) real NASA OSDR/EDA habitat telemetry (24 missions, 5-minute series) -> quality control per mission (habitat context only);
2) synthetic crews run through the SAME rule v3 on seeds never used for tuning.
15/11/2026 · FAIT PAR L'IA (session design) — PAS ENCORE VÉRIFIÉ
"""
from __future__ import annotations

import os
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "real", "raw", "eda_all_missions.json.gz")
THR = 1.5   # shipped threshold, no retuning


def raw_inventory() -> dict:
    """Counts straight from the raw NASA file: missions, 5-minute points, hours of telemetry."""
    sys.path.insert(0, ROOT)
    from scripts.eda_load import load   # noqa: PLC0415   (verifies the SHA-256 of the raw file)
    pts = {m: len(v["telemetry"]["time"]) for m, v in load().items() if v.get("telemetry")}
    return {"missions": len(pts), "points": sum(pts.values()), "hours": round(sum(pts.values()) * 5 / 60), "per_mission": pts}


def reprocess_nasa() -> dict:
    """Re-run the quality control (plateau detection, mmHg conversion) on the raw file; returns rows + timing."""
    sys.path.insert(0, ROOT)
    from scripts import build_habitat   # noqa: PLC0415
    t = time.time()
    rows = build_habitat.main(tempfile.mkdtemp())
    return {"rows": rows, "seconds": round(time.time() - t, 1), **raw_inventory()}


def crews(n_control: int = 100, n_gradual: int = 50, seed0: int = 50000) -> dict:
    """Run the shipped rule on fresh synthetic crews. Seeds seed0.. are never used for tuning (tuning used 1000-7149, held-out 30000-37149)."""
    sys.path.insert(0, os.path.join(ROOT, "research", "pilot"))
    sys.path.insert(0, ROOT)
    from pilot import ABS_FLOOR, procedure_days, run_flags, states_from_flags, zscores   # noqa: PLC0415
    from pilot2 import control, gradual   # noqa: PLC0415
    from pilot3 import wilson   # noqa: PLC0415

    def hit(dv):
        return bool(procedure_days(states_from_flags(run_flags(zscores(dv, ABS_FLOOR), THR), dv)))

    t = time.time()
    k0 = sum(hit(control(seed0 + i)) for i in range(n_control))
    k1 = sum(hit(gradual(seed0 + 10000 + i)) for i in range(n_gradual))
    return {"control": {"n": n_control, "hits": k0, "ci": wilson(k0, n_control)},
            "gradual": {"n": n_gradual, "hits": k1, "ci": wilson(k1, n_gradual)}, "seconds": round(time.time() - t, 1), "seed0": seed0}
