"""Prototype: crew-wide or individual? (registry id common_signal, V3 20/11/2026). SIMULATED data only.

When several crew members leave their own normal on the same day, the change is more likely shared (cabin air, schedule)
than personal; C-Sync then says "shared signal, check the cabin" instead of pointing at one person.
Rule (design parameter, not NASA): on a day, a member is "off" if their deviation z >= Z_OFF; if at least SHARED_MIN of the
crew are off, the day is "shared"; otherwise each off member is "individual"."""
from __future__ import annotations

import numpy as np

Z_OFF = 1.5
SHARED_MIN = 3


def attribute(z_by_member: dict[str, list[float]]) -> list[dict]:
    """Per day: {"day", "kind": "shared" | "individual" | "none", "members": [...]}. Days are aligned across members."""
    assert z_by_member, "no crew"
    n = {len(v) for v in z_by_member.values()}
    assert len(n) == 1, "members must have the same number of days"
    out = []
    for d in range(n.pop()):
        off = sorted(m for m, z in z_by_member.items() if z[d] >= Z_OFF)
        kind = "shared" if len(off) >= SHARED_MIN else ("individual" if off else "none")
        out.append({"day": d + 1, "kind": kind, "members": off})
    return out


def simulate(seed: int, n_members: int = 4, days: int = 10, shift: float = 2.2) -> tuple[dict, list[str]]:
    """SIMULATED crew: noise N(0,1); one shared shift on a random day for everyone, one individual shift on another day.
    Returns (z_by_member, truth per day: shared / individual / none)."""
    rng = np.random.default_rng(seed)
    z = {f"Crew {chr(65 + i)}": rng.normal(0, 1, days) * 0.6 for i in range(n_members)}
    d_shared, d_ind = rng.choice(days, size=2, replace=False)
    who = rng.choice(list(z))
    for m in z:
        z[m][d_shared] += shift
    z[who][d_ind] += shift
    truth = ["none"] * days
    truth[d_shared], truth[d_ind] = "shared", "individual"
    return {m: list(v) for m, v in z.items()}, truth


def accuracy(seeds: range) -> float:
    """Share of the planted shared/individual days attributed correctly (the promise's own test: >= 90 %)."""
    hit = total = 0
    for s in seeds:
        z, truth = simulate(s)
        got = attribute(z)
        for g, t in zip(got, truth, strict=True):
            if t != "none":
                total += 1
                hit += g["kind"] == t
    assert total > 0
    return hit / total
