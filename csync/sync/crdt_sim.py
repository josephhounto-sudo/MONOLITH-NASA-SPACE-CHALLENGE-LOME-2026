"""SIMULATED last-writer-wins registers. This module is a simulation of an offline link."""
from __future__ import annotations

import random


class Replica:
    def __init__(self, replica_id: str):
        self.replica_id = replica_id
        self._reg: dict[str, tuple] = {}

    def set(self, key: str, value, ts: int) -> None:
        """Last-writer-wins register. Equal timestamps keep the greater replica id."""
        candidate = (int(ts), self.replica_id, value)
        current = self._reg.get(key)
        if current is None or (candidate[0], candidate[1]) >= (current[0], current[1]):
            self._reg[key] = candidate

    def state(self) -> dict:
        return {key: entry[2] for key, entry in self._reg.items()}

    def merge(self, other: "Replica") -> None:
        """Commutative, associative, idempotent union of registers."""
        _absorb(self, other._reg)

    def _snapshot(self) -> dict:
        return dict(self._reg)


def _absorb(dest: Replica, entries: dict) -> None:
    for key, entry in entries.items():
        current = dest._reg.get(key)
        if current is None or (entry[0], entry[1]) >= (current[0], current[1]):
            dest._reg[key] = entry


def simulate_link(a: Replica, b: Replica, delay_steps: int, outage: tuple[int, int] | None, steps: int, seed: int) -> list[dict]:
    """Returns one record per step: {"step", "a", "b", "converged": bool}. Messages arrive after delay_steps; none during outage."""
    rng = random.Random(seed)
    pending: list[tuple[int, str, dict]] = []
    records = []
    for step in range(steps):
        blocked = outage is not None and outage[0] <= step < outage[1]
        if not blocked:
            waiting = []
            for arrive, target, entries in pending:
                if arrive <= step:
                    _absorb(a if target == a.replica_id else b, entries)
                else:
                    waiting.append((arrive, target, entries))
            pending = waiting
        if delay_steps <= 0 or step < steps - delay_steps:
            a.set(f"k{rng.randrange(4)}", (a.replica_id, rng.randrange(50)), step)
            b.set(f"k{rng.randrange(4)}", (b.replica_id, rng.randrange(50)), step)
        if not blocked:
            if delay_steps <= 0:
                snap_a, snap_b = a._snapshot(), b._snapshot()
                _absorb(a, snap_b)
                _absorb(b, snap_a)
            else:
                pending.append((step + delay_steps, b.replica_id, a._snapshot()))
                pending.append((step + delay_steps, a.replica_id, b._snapshot()))
        records.append({"step": step, "a": a.state(), "b": b.state(), "converged": a.state() == b.state()})
    return records
