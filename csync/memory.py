"""Local memory: an append-only JSON-lines file on the device, no network. One line per record.

A record is stored once: the key is (indicator_id, timestamp_utc, source_id), so replaying the same source (for example
after a restart) adds nothing. Nothing is ever edited or deleted; a quality flag stays with the value it describes.
"""
from __future__ import annotations

import json
import os


class LocalMemory:
    def __init__(self, path: str):
        self.path = path
        self._keys = set()
        if os.path.exists(path):
            for rec in self.records():
                self._keys.add(self._key(rec))

    @staticmethod
    def _key(rec: dict):
        return (rec["indicator_id"], rec["timestamp_utc"], rec["source_id"])

    def records(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, encoding="utf8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def add(self, records: list[dict]) -> int:
        """Append records not seen before; return how many were new."""
        new = [r for r in records if self._key(r) not in self._keys]
        if new:
            with open(self.path, "a", encoding="utf8") as f:
                for r in new:
                    f.write(json.dumps(r, sort_keys=True) + "\n")
                    self._keys.add(self._key(r))
        return len(new)
