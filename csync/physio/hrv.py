"""Beat-to-beat summaries. simulated_rr builds a SIMULATED series, never a recorded one."""
from __future__ import annotations

import math
import random
import statistics


def _require(rr_ms: list[float], minimum: int) -> None:
    if len(rr_ms) < minimum:
        raise ValueError(f"Need at least {minimum} intervals; got {len(rr_ms)}.")
    if any(value <= 0 for value in rr_ms):
        raise ValueError("Every interval must be > 0; drop non-positive values first.")


def rmssd(rr_ms: list[float]) -> float:
    """Root mean square of successive differences. Raises ValueError if fewer than 3 intervals or any <= 0."""
    _require(rr_ms, 3)
    gaps = [(rr_ms[index + 1] - rr_ms[index]) ** 2 for index in range(len(rr_ms) - 1)]
    return math.sqrt(sum(gaps) / len(gaps))


def sdnn(rr_ms: list[float]) -> float:
    """Sample standard deviation of the intervals (divisor n-1)."""
    _require(rr_ms, 3)
    return statistics.stdev(rr_ms)


def simulated_rr(seconds: int, mean_hr: float, seed: int, stress: float = 0.0) -> list[float]:
    """SIMULATED RR series in ms; stress in [0,1] lowers variability. Deterministic."""
    if seconds < 1 or mean_hr <= 0 or not 0.0 <= stress <= 1.0:
        raise ValueError("simulated_rr needs seconds >= 1, mean_hr > 0, and stress from 0 to 1.")
    rng = random.Random(seed)
    mean_rr = 60000.0 / mean_hr
    count = max(3, int(seconds * mean_hr / 60))
    phase = rng.random()
    scale = 1.0 - stress
    return [mean_rr + scale * (30.0 * math.sin(index + phase) + 10.0) for index in range(count)]


def clean_rr(rr_ms: list[float], low: float = 300.0, high: float = 2000.0) -> tuple[list[float], int]:
    """Drops out-of-range intervals; returns (kept, dropped_count)."""
    kept = [value for value in rr_ms if low <= value <= high]
    return kept, len(rr_ms) - len(kept)
