import json

import pytest

from csync.tech import registry


def test_registry_loads_and_has_no_overclaim():
    reg = registry.load()
    assert reg["items"]
    assert registry.audit(reg) == []


def test_every_item_has_a_status_label_and_purpose():
    reg = registry.load()
    for it in reg["items"]:
        assert registry.label(reg, it)
        assert it["purpose"].endswith(".")


def test_overclaim_is_caught(tmp_path):
    p = tmp_path / "t.json"
    p.write_text(json.dumps({"statuses": {"BUILT": "b", "PROTOTYPE": "p", "ANNOUNCED": "a"},
                             "items": [{"id": "x", "name": "X", "status": "BUILT", "module": "csync.nope.nothing", "purpose": "x.", "data": "SIMULATED"}]}))
    assert registry.audit(registry.load(str(p)))


def test_unknown_status_and_duplicate_rejected(tmp_path):
    base = {"statuses": {}, "items": [{"id": "a", "name": "A", "status": "MAGIC", "module": None, "purpose": "x.", "data": "NONE"}]}
    p = tmp_path / "t.json"
    p.write_text(json.dumps(base))
    with pytest.raises(ValueError):
        registry.load(str(p))
    base["items"] = [{"id": "a", "name": "A", "status": "ANNOUNCED", "module": None, "purpose": "x.", "data": "NONE"}] * 2
    p.write_text(json.dumps(base))
    with pytest.raises(ValueError):
        registry.load(str(p))


def test_forbidden_words_not_in_registry_text():
    with open(registry._PATH, encoding="utf8") as f:
        text = f.read().lower()
    for w in ("cause", "diagnos", "prove", "guarantee", "disease"):
        assert w not in text
