"""Independent reference implementation of C-Sync drift detectors (stdlib only).

Implemented strictly from the G3 specification (commit dc61786):
- Baseline period: days 1..5 (t <= 5) are never flagged.
- Rule (d >= 1.5, 2 consecutive days, t > 5): missing values (None/NaN) reset the consecutive counter to 0.
- EWMA (lambda=0.3, L=2.5, t > 5): evaluated over non-missing observations n = 1, 2, ...
  e_n = lambda * z + (1 - lambda) * e_{n-1}, e_0 = 0
  sigma_n = sqrt((lambda / (2 - lambda)) * (1 - (1 - lambda)**(2 * n)))
  flagged iff e_n > L * sigma_n.
- CUSUM (k=0.5, h=3.0, t > 5): evaluated over non-missing observations:
  s_n = max(0.0, s_{n-1} + z - k), s_0 = 0
  flagged iff s_n > h.
"""

import json
import math
from typing import Dict, List, Optional, Sequence


def _is_missing(val: Optional[float]) -> bool:
    return val is None or (isinstance(val, float) and math.isnan(val))


def detect_rule(
    z_series: Sequence[Optional[float]],
    threshold: float = 1.5,
    consecutive_days: int = 2,
    baseline_days: int = 5,
) -> List[bool]:
    """Two-consecutive-days threshold detector (only active for day t > baseline_days)."""
    flags: List[bool] = []
    run = 0
    for idx, val in enumerate(z_series):
        day = idx + 1
        if _is_missing(val):
            run = 0
            flags.append(False)
            continue
        if float(val) >= threshold:
            run += 1
        else:
            run = 0
        flags.append(day > baseline_days and run >= consecutive_days)
    return flags


def detect_ewma(
    z_series: Sequence[Optional[float]],
    lam: float = 0.3,
    limit_l: float = 2.5,
    baseline_days: int = 5,
) -> List[bool]:
    """One-sided upper EWMA detector with exact finite-sample variance (t > baseline_days)."""
    flags: List[bool] = []
    e_prev = 0.0
    n = 0
    asymp_factor = lam / (2.0 - lam)
    for idx, val in enumerate(z_series):
        day = idx + 1
        if day <= baseline_days or _is_missing(val):
            flags.append(False)
            continue
        n += 1
        z_val = float(val)
        e_curr = lam * z_val + (1.0 - lam) * e_prev
        sigma_n = math.sqrt(asymp_factor * (1.0 - (1.0 - lam) ** (2 * n)))
        flags.append(e_curr > limit_l * sigma_n)
        e_prev = e_curr
    return flags


def detect_cusum(
    z_series: Sequence[Optional[float]],
    k: float = 0.5,
    h: float = 3.0,
    baseline_days: int = 5,
) -> List[bool]:
    """One-sided upper CUSUM detector (t > baseline_days)."""
    flags: List[bool] = []
    s_prev = 0.0
    for idx, val in enumerate(z_series):
        day = idx + 1
        if day <= baseline_days or _is_missing(val):
            flags.append(False)
            continue
        z_val = float(val)
        s_curr = max(0.0, s_prev + z_val - k)
        flags.append(s_curr > h)
        s_prev = s_curr
    return flags


def evaluate_vectors(vectors: Dict[str, dict]) -> Dict[str, dict]:
    """Run all three detectors on a dictionary of test cases and compare against expected arrays."""
    results: Dict[str, dict] = {}
    for case_name, payload in vectors.items():
        z_vals = payload["z_days_1_to_10"]
        got_ewma = detect_ewma(z_vals, lam=0.3, limit_l=2.5, baseline_days=5)
        got_cusum = detect_cusum(z_vals, k=0.5, h=3.0, baseline_days=5)
        got_rule = detect_rule(z_vals, threshold=1.5, consecutive_days=2, baseline_days=5)

        exp_ewma = payload["ewma_lambda0.3_L2.5_flags_days_1_to_10"]
        exp_cusum = payload["cusum_k0.5_h3_flags"]
        exp_rule = payload["rule_d1.5_two_consecutive_flags"]

        results[case_name] = {
            "ewma": {"got": got_ewma, "expected": exp_ewma, "match": got_ewma == exp_ewma},
            "cusum": {"got": got_cusum, "expected": exp_cusum, "match": got_cusum == exp_cusum},
            "rule": {"got": got_rule, "expected": exp_rule, "match": got_rule == exp_rule},
        }
    return results


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "docs/blocks/test_vectors_detectors.json"
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    report = evaluate_vectors(data)
    for case, dets in report.items():
        print(f"=== {case} ===")
        for det_name, info in dets.items():
            status = "OK" if info["match"] else "MISMATCH"
            print(f"  {det_name:6s}: {status} | got={info['got']}")
