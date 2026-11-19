"""SIMULATED replicas. Fixed seeds stand in for a property search. This is a simulation."""
import random

from csync.sync.crdt_sim import Replica, simulate_link


def _fill(replica, seed):
    rng = random.Random(seed)
    for step in range(6):
        replica.set(f"k{rng.randrange(4)}", rng.randrange(20), rng.randrange(6))


def _copy(replica):
    twin = Replica(replica.replica_id)
    twin.merge(replica)
    return twin


def test_merge_is_idempotent():
    left, right = Replica("a"), Replica("b")
    _fill(left, 1)
    _fill(right, 2)
    left.merge(right)
    once = left.state()
    left.merge(right)
    assert left.state() == once


def test_merge_is_commutative_over_fixed_seeds():
    for seed in range(25):
        left, right = Replica("a"), Replica("b")
        _fill(left, seed)
        _fill(right, seed + 100)
        one, other = _copy(left), _copy(right)
        one.merge(other)
        other.merge(_copy(left))
        assert one.state() == other.state()


def test_merge_is_associative_over_fixed_seeds():
    for seed in range(25):
        first, second, third = Replica("a"), Replica("b"), Replica("c")
        _fill(first, seed)
        _fill(second, seed + 10)
        _fill(third, seed + 20)
        left = _copy(first)
        left.merge(_copy(second))
        left.merge(_copy(third))
        right = _copy(first)
        mid = _copy(second)
        mid.merge(_copy(third))
        right.merge(mid)
        assert left.state() == right.state()


def test_equal_timestamp_keeps_the_greater_replica_id():
    left, right = Replica("a"), Replica("b")
    left.set("k", "from-a", 5)
    right.set("k", "from-b", 5)
    left.merge(right)
    right.merge(left)
    assert left.state()["k"] == "from-b"
    assert right.state()["k"] == "from-b"


def test_simulation_converges_after_the_outage():
    earth, ship = Replica("earth"), Replica("ship")
    log = simulate_link(earth, ship, delay_steps=2, outage=(4, 8), steps=16, seed=3)
    assert len(log) == 16
    assert [row["step"] for row in log] == list(range(16))
    assert any(not row["converged"] for row in log if 4 <= row["step"] < 8)
    assert log[-1]["converged"] is True
    assert log[-1]["a"] == earth.state()
    assert log[-1]["b"] == ship.state()
