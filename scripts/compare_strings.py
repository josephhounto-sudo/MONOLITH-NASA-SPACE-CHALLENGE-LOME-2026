"""Compare csync/config/strings_en.json and strings_fr.json.

Prints one gap per line. Exit 0 when there is none.
English is the reference: this script never rewrites it.
Identical strings are a gap unless the whole value is in SAME_IN_BOTH
(a word that is French as well, a name, a citation, or a data sample).
"""
import json
import re
import sys

PH = re.compile(r"\{[^{}]+\}")

# Whole values that are the same string in French. A new identical sentence is a gap.
SAME_IN_BOTH = {
    "C-Sync",
    "Pip",
    "Mission",
    "Source",
    "Commander",  # speaker id in the demo dialogue (shown as speaker_cmd)  # name of the guide bot (20/11/2026)
    "Normal",
    "Mission",
    "Commander",  # speaker id in the demo dialogue (shown as speaker_cmd)
    "Source",
    "Sources",
    "Stress",
    "Stress (0–10)",
    "Situation",
    "Attention",
    "Kora",
    "PhysioNet wearable dataset v1.0.1 (Empatica E4, ODC-By)",
    "Varanoske et al., NASA, NTRS 20240016101 (2025)",
    "NASA Human Research Roadmap, risk 100; gap Sleep-102; task 1453",
    '{"device": "wrist-01", "mission_day": 7, "metric": "sleep_hours", "value": 5.4}',
}


def load_pair(en_path, fr_path):
    """Read both files. On failure, say which file and what to do."""
    missing = []
    for label, path in (("English", en_path), ("French", fr_path)):
        try:
            with open(path, encoding="utf8") as f:
                raw = f.read()
        except OSError as err:
            missing.append(f"{label} file missing ({path}): restore it from git, then re-run. {err}")
            continue
        if not raw.strip():
            missing.append(f"{label} file is empty ({path}): restore it from git, then re-run.")
    if missing:
        raise ValueError("\n".join(missing))
    with open(en_path, encoding="utf8") as f:
        en = json.load(f)
    with open(fr_path, encoding="utf8") as f:
        fr = json.load(f)
    return en, fr


def _meaning(path, en, fr):
    """Mismatches found by reading every pair. Each check names the French error."""
    if path.endswith(".decision") and re.search(r"\bporte\b", fr, re.I):
        return f"{path}: Gate is the resume check, not a door ('porte')"
    if path.endswith(".body_map_why") and "utile" in fr and "compte" not in fr:
        return f"{path}: 'utile' does not say 'why it matters'"
    if path.endswith(".scale_healthy") and re.search(r"une fausse\)?\s*$", fr):
        return f"{path}: 'une fausse' has no noun; the English says a false procedure"
    if path.endswith(".PS04") and "Workload" in en and "travail" not in fr:
        return f"{path}: Workload is 'charge de travail', not 'charge' alone"
    if path.endswith(".limits_1") and "passé" not in fr:
        return f"{path}: the French does not say the comparison is with the person's own past"
    if path.endswith(".resume_stale") and "old" in en and "date de" not in fr and "ancien" not in fr:
        return f"{path}: the French does not say the reading is old"
    return None


def gaps(en, fr, path=""):
    """Return a list of gap lines. Empty list means the two trees match."""
    found = []
    if type(en) is not type(fr):
        return [f"{path or '<root>'}: type {type(en).__name__} vs {type(fr).__name__}"]
    if isinstance(en, dict):
        for key in en:
            child = f"{path}.{key}" if path else key
            if key not in fr:
                found.append(f"{child}: missing in French")
            else:
                found.extend(gaps(en[key], fr[key], child))
        for key in fr:
            if key not in en:
                child = f"{path}.{key}" if path else key
                found.append(f"{child}: missing in English (do not add a French-only key)")
        return found
    if isinstance(en, list):
        if len(en) != len(fr):
            found.append(f"{path}: length {len(en)} vs {len(fr)}")
        for i, (a, b) in enumerate(zip(en, fr, strict=False)):   # unequal lengths are reported just above
            found.extend(gaps(a, b, f"{path}[{i}]"))
        return found
    if isinstance(en, str):
        if PH.findall(en) != PH.findall(fr):
            found.append(f"{path}: placeholders {PH.findall(en)} vs {PH.findall(fr)}")
        if en == fr and any(c.isalpha() for c in en) and en not in SAME_IN_BOTH:
            found.append(f"{path}: identical to English, not in the shared-word list")
        meaning = _meaning(path, en, fr)
        if meaning:
            found.append(meaning)
        return found
    if en != fr:
        found.append(f"{path}: value {en!r} vs {fr!r}")
    return found


def main(argv):
    root_en = argv[1] if len(argv) > 1 else "csync/config/strings_en.json"
    root_fr = argv[2] if len(argv) > 2 else "csync/config/strings_fr.json"
    try:
        en, fr = load_pair(root_en, root_fr)
    except ValueError as err:
        print(err)
        return 2
    except json.JSONDecodeError as err:
        print(f"JSON is not readable: fix the file, then re-run. {err}")
        return 2
    found = gaps(en, fr)
    for line in found:
        print(line)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
