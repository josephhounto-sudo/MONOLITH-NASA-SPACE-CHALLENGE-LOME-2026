"""Load the raw EDA series (24 missions) saved on 14/11/2026.
Usage:  python scripts/eda_load.py            -> prints one line per mission
In code: from scripts.eda_load import load; d = load(); d["RR-1"]["telemetry"]["time"]
Source: https://visualization.osdr.nasa.gov/eda/ (NASA OSDR Environmental Data App).
Data and visualizations are courtesy of the Environmental Data App (EDA)."""
import gzip, json, hashlib, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / "data" / "real" / "raw" / "eda_all_missions.json.gz"
def load(check=True):
    raw = P.read_bytes()
    if check:
        want = (P.parent / "SHA256SUMS.txt").read_text().split()[0]
        assert hashlib.sha256(raw).hexdigest() == want, "checksum mismatch"
    return json.loads(gzip.decompress(raw))["missions"]
if __name__ == "__main__":
    for name, m in load().items():
        t, r = m.get("telemetry"), m.get("radiation")
        print(f"{name:10} telemetry={len(t['time']) if t else 0:7} radiation_days={len(r['time']) if r else 0}")
