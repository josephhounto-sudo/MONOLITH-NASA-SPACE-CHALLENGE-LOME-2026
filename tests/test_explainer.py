"""Prototype offline explainer: the promise's own test (200 explanations, every number traced, no banned word),
and the check must catch an invented number (a check that cannot fail is not a check)."""
import copy
import json
import os

import numpy as np

from csync.proto import explainer as ex

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "out")


def _daily():
    caps = []
    for f in ("capsules_histoire.json", "capsules_temoin.json", "capsules_capteur.json"):
        with open(os.path.join(OUT, f), encoding="utf-8") as fh:
            caps += [c for c in json.load(fh) if c.get("capsule_type", "daily") == "daily"]
    assert caps
    return caps


def _two_hundred():
    """SIMULATED variants of the demo capsules that have something to say: values jittered so the 200 texts differ."""
    base = [c for c in _daily() if any(s.get("flagged") and s.get("d") is not None for s in c.get("signals", []))]
    assert len(base) >= 3
    rng, out = np.random.default_rng(7), []
    for i in range(200):
        c = copy.deepcopy(base[i % len(base)])
        for s in c.get("signals", []):
            if isinstance(s.get("value"), (int, float)):
                s["value"] = round(float(s["value"]) * float(rng.uniform(0.8, 1.2)), int(rng.integers(0, 3)))
        out.append(c)
    return out


def test_two_hundred_explanations_every_number_traced_no_banned_word():
    caps = _two_hundred()
    texts = [ex.explain(c) for c in caps]
    assert len({" ".join(t) for t in texts}) > 100            # really different texts, not one text 200 times
    for c, t in zip(caps, texts, strict=True):
        assert ex.check(t, c) == [], ex.check(t, c)


def test_the_check_catches_an_invented_number_and_a_banned_word():
    cap = _daily()[0]
    assert ex.check(["Reaction time: 987654 today."], cap)
    assert ex.check(["This is a diagnosis."], cap)
