"""Upward CUSUM and a Gaussian online change-point. SIMULATED series stay labelled by the caller."""
from __future__ import annotations

import math


def cusum(values: list[float], baseline_mean: float, baseline_sd: float, k: float = 0.5, h: float = 4.0) -> dict:
    """One-sided upward CUSUM on z=(x-mean)/sd. Returns {"alarm_index": int | None, "scores": list[float]}.
    Raises ValueError if baseline_sd <= 0 or values is empty. None values are not accepted (caller filters)."""
    if not values:
        raise ValueError("CUSUM needs at least one value; pass a non-empty series.")
    if baseline_sd <= 0:
        raise ValueError("baseline_sd must be > 0; check the baseline before calling CUSUM.")
    scores: list[float] = []
    total = 0.0
    alarm: int | None = None
    for index, value in enumerate(values):
        if value is None:
            raise ValueError("CUSUM does not accept missing values; filter them before the call.")
        score = (value - baseline_mean) / baseline_sd
        total = max(0.0, total + score - k)
        scores.append(total)
        if alarm is None and total >= h:
            alarm = index
    return {"alarm_index": alarm, "scores": scores}


def _logsumexp(terms: list[float]) -> float:
    top = max(terms)
    if top == -math.inf:
        return -math.inf
    return top + math.log(sum(math.exp(term - top) for term in terms))


def _predict(value: float, count: int, total: float) -> float:
    """Log density of a unit-variance observation. Unknown mean, prior N(0, 1)."""
    precision = 1.0 + count
    mean = total / precision
    variance = 1.0 + 1.0 / precision
    return -0.5 * math.log(2.0 * math.pi * variance) - (value - mean) ** 2 / (2.0 * variance)


def bocpd(values: list[float], hazard: float = 1 / 20) -> dict:
    """Bayesian online change-point (Gaussian, unknown mean, known unit variance on z-scores). Returns
    {"change_prob": list[float], "most_likely_index": int | None}. Pure python or numpy. Deterministic."""
    if not values:
        return {"change_prob": [], "most_likely_index": None}
    log_hazard = math.log(hazard)
    log_stay = math.log(1.0 - hazard)
    log_run = [0.0]
    sums = [0.0]
    counts = [0]
    change_prob: list[float] = []
    for value in values:
        log_pred = [_predict(value, counts[run], sums[run]) for run in range(len(log_run))]
        log_change = _logsumexp([log_run[run] + log_pred[run] + log_hazard for run in range(len(log_run))])
        log_grow = [log_run[run] + log_pred[run] + log_stay for run in range(len(log_run))]
        joint = [log_change, *log_grow]
        normaliser = _logsumexp(joint)
        log_run = [term - normaliser for term in joint]
        sums = [0.0, *[sums[run] + value for run in range(len(sums))]]
        counts = [0, *[counts[run] + 1 for run in range(len(counts))]]
    # A constant hazard makes P(run length 0) equal to the hazard at every step.
    # The informative mass is the final posterior over where the current run started.
    length = len(values)
    change_prob = [0.0] * length
    for run, log_prob in enumerate(log_run):
        start = (length - 1) - run
        if 0 <= start < length:
            change_prob[start] = math.exp(log_prob)
    best_run = max(range(len(log_run)), key=log_run.__getitem__)
    started = (length - 1) - best_run
    most = started if 0 < started < length else None
    return {"change_prob": change_prob, "most_likely_index": most}
