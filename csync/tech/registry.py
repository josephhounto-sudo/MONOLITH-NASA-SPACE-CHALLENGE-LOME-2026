"""Technology registry: the only source for what the interface may say a technology does. Status is read from JSON, never typed in a page."""
from __future__ import annotations

import importlib.util
import json
import os

_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "technologies.json")
STATUSES = ("BUILT", "PROTOTYPE", "ANNOUNCED")


def load(path: str = _PATH) -> dict:
    """Return {"statuses": {...}, "items": [...]}. Raises ValueError on an unknown status or a duplicate id."""
    with open(path, encoding="utf8") as f:
        reg = json.load(f)
    seen = set()
    for it in reg["items"]:
        if it["status"] not in STATUSES:
            raise ValueError(f"unknown status for {it['id']}: {it['status']}")
        if it["id"] in seen:
            raise ValueError(f"duplicate id {it['id']}")
        seen.add(it["id"])
    return reg


def module_exists(name: str | None) -> bool:
    """True when the dotted module can be found without importing it."""
    if not name:
        return False
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def audit(reg: dict) -> list[str]:
    """Problems that would make the interface overclaim: a BUILT or PROTOTYPE item whose module is missing, or an
    ANNOUNCED item that has no label of its status."""
    problems = []
    for it in reg["items"]:
        if it["status"] in ("BUILT", "PROTOTYPE") and not module_exists(it.get("module")):
            problems.append(f"{it['id']}: status {it['status']} but module {it.get('module')} not found")
        if it["status"] == "BUILT" and it.get("data") not in ("SIMULATED", "REAL"):
            problems.append(f"{it['id']}: BUILT needs data labelled SIMULATED or REAL")
    return problems


def label(reg: dict, item: dict) -> str:
    """Words shown next to the technology, taken from the registry."""
    return reg["statuses"][item["status"]]
