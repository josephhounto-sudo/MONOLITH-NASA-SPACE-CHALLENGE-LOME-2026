"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

Reference implementations of EWMA and CUSUM, for tests only — référence, non utilisée par le moteur.
The engine (csync/rules.py) uses the v3 rule only. These two functions mirror research/pilot/pilot.py
(ewma_flags, cusum_flags) on one series of daily deviations d, so the test vectors in
docs/blocks/test_vectors_detectors.json can be checked. Monitoring starts after the baseline days;
a missing day is skipped (the statistic is held, not reset).
"""
import math


def ewma_flags(z, baseline_days=5, lam=0.3, L=2.5):
    """EWMA of d with time-varying control limit L * sigma_n, sigma_n^2 = lam/(2-lam) * (1 - (1-lam)^(2n))."""
    e, n, out = 0.0, 0, []
    for day, v in enumerate(z, start=1):
        if day <= baseline_days or v is None:
            out.append(False)
            continue
        n += 1
        e = lam * v + (1 - lam) * e
        out.append(e > L * math.sqrt(lam / (2 - lam) * (1 - (1 - lam) ** (2 * n))))
    return out


def cusum_flags(z, baseline_days=5, k=0.5, h=3.0):
    """One-sided CUSUM S = max(0, S + d - k); flagged when S > h."""
    s, out = 0.0, []
    for day, v in enumerate(z, start=1):
        if day <= baseline_days or v is None:
            out.append(False)
            continue
        s = max(0.0, s + v - k)
        out.append(s > h)
    return out
