"""Prototype: delay-tolerant messaging (registry id dtn, V3 20/11/2026). SIMULATED link.

Store-and-forward in the spirit of the Bundle Protocol: the spacecraft keeps every report until the ground acknowledges it,
resends what was not acknowledged, and the ground keeps reports in order and drops duplicates. One step = one minute."""
from __future__ import annotations

import random

MAX_STEPS = 60 * 24 * 7   # one week of minutes: every simulation loop is bounded


def simulate(n_reports: int, every_min: int, outage: tuple[int, int], delay_min: int, loss: float, seed: int,
             resend_after_min: int | None = None) -> dict:
    """Send n_reports, one every `every_min` minutes, over a link that is down during `outage` (start, end minutes),
    takes `delay_min` one way and loses a share `loss` of transmissions. Returns delivery facts."""
    assert n_reports >= 1 and every_min >= 1 and delay_min >= 0 and 0 <= loss < 1 and outage[0] <= outage[1]
    resend = resend_after_min or (2 * delay_min + 5)
    rng = random.Random(seed)
    unacked: dict[int, int] = {}            # report id -> minute of last sending
    in_flight: list[tuple[int, int]] = []   # (arrival minute, report id), towards the ground
    acks: list[tuple[int, int]] = []        # (arrival minute, report id), towards the spacecraft
    received, delivered, duplicates, sends, arrival_min = set(), [], 0, 0, {}
    next_expected, buffer = 0, set()
    for t in range(MAX_STEPS):
        up = not (outage[0] <= t < outage[1])
        if t % every_min == 0 and t // every_min < n_reports:
            unacked[t // every_min] = -10**9
        if up:
            for rid, last in list(unacked.items()):
                if t - last >= resend:
                    unacked[rid] = t
                    sends += 1
                    if rng.random() >= loss:
                        in_flight.append((t + delay_min, rid))
        landed = [r for a, r in in_flight if a <= t]
        in_flight = [(a, r) for a, r in in_flight if a > t]
        for rid in landed:
            if rid in received:
                duplicates += 1
            else:
                received.add(rid)
                buffer.add(rid)
                arrival_min[rid] = t
            if up and rng.random() >= loss:
                acks.append((t + delay_min, rid))
        while next_expected in buffer:           # hand over to the ground team strictly in order
            delivered.append(next_expected)
            buffer.discard(next_expected)
            next_expected += 1
        for rid in [r for a, r in acks if a <= t]:
            unacked.pop(rid, None)
        acks = [(a, r) for a, r in acks if a > t]
        if len(delivered) == n_reports and not unacked:
            break
    return {"delivered": delivered, "all_once_in_order": delivered == list(range(n_reports)),
            "duplicates_dropped": duplicates, "transmissions": sends, "minutes": t + 1,
            "last_arrival_min": max(arrival_min.values()) if arrival_min else None}
