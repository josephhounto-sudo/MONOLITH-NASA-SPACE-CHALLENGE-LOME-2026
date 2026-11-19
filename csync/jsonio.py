"""Read a JSON file with the file closed afterwards (one place, so no handle is left open by a module-level load)."""
import json


def read_json(path):
    """Parsed content of `path` (UTF-8). Raises FileNotFoundError or json.JSONDecodeError: callers decide the fallback."""
    with open(path, encoding="utf8") as f:
        return json.load(f)
