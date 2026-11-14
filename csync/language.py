"""Banned wording check (PARAMETRES P-20). Applies to every generated explanation, in FR and EN.
Note: negations are also caught ("no diagnosis"), so fixed texts must avoid these words entirely."""
import re

BANNED_EN = ["cause", "caused by", "because of", "diagnosis", "diagnose", "disease", "disorder", "suffers from", "proves", "guaranteed"]
BANNED_FR = ["cause", "causé par", "à cause de", "diagnostic", "diagnostique", "maladie", "pathologie", "souffre de", "prouve", "garanti"]

def banned_hits(text: str) -> list[str]:
    t = text.lower()
    return [w for w in BANNED_EN + BANNED_FR if re.search(r"\b" + re.escape(w), t)]
