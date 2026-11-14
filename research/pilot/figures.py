"""Pitch-ready figure from the pilot (English labels). Run after pilot.py."""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
s = pd.read_csv(os.path.join(HERE, "pilot_summary.csv"))
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.facecolor": SURF,
                     "figure.facecolor": SURF, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": GRID, "xtick.color": INK2, "ytick.color": INK2, "axes.labelcolor": INK2})

def wilson(p, n, z=1.96):
    p = p / 100
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return 100 * (c - h), 100 * (c + h)

fig, ax = plt.subplots(figsize=(7.6, 4.6))
labels = {"A rule v3 (d>=1)": "A · current rule (d ≥ 1)", "B rule proposed (d>=1.5 + floor)": "B · proposed rule (d ≥ 1.5 + floor)",
          "C EWMA": "C · EWMA trend", "D CUSUM": "D · CUSUM", "E combined score (diagonal)": "E · combined score"}
offs = {"A rule v3 (d>=1)": (-8, -14), "B rule proposed (d>=1.5 + floor)": (8, -16), "C EWMA": (8, 4), "D CUSUM": (8, -10), "E combined score (diagonal)": (8, -4)}
for m in labels:
    ctl = s[(s.method == m) & (s.missing == 0) & (s.drift == 0)].iloc[0]
    det = s[(s.method == m) & (s.missing == 0) & (s.drift == 1.5)].iloc[0]
    detm = s[(s.method == m) & (s.missing == 0.1) & (s.drift == 1.5)].iloc[0]
    lo, hi = wilson(ctl.pct_procedure, ctl.runs)
    best = m.startswith("C") or m.startswith("B")
    col = "#2a78d6" if best else INK2
    ax.plot([lo, hi], [det.pct_procedure] * 2, color=col, lw=1, alpha=0.6)
    ax.annotate("", xy=(ctl.pct_procedure, detm.pct_procedure), xytext=(ctl.pct_procedure, det.pct_procedure),
                arrowprops=dict(arrowstyle="->", color=col, lw=1, alpha=0.7))
    ax.scatter([ctl.pct_procedure], [det.pct_procedure], s=90, color=col, zorder=3, edgecolor=SURF, linewidth=2)
    ax.annotate(labels[m], (ctl.pct_procedure, det.pct_procedure), xytext=offs[m], textcoords="offset points", fontsize=8.5, color=INK)
ax.set_xlim(-1, 20); ax.set_ylim(60, 103)
ax.set_xlabel("False procedures on a crew member with NO drift (% of 300 runs) — lower is better")
ax.set_ylabel("Drift of 1.5 SD detected (% of 150 runs)")
ax.set_title("Which detector for 5 days of personal baseline?", loc="left", fontsize=12, fontweight="bold", color=INK)
ax.text(0, 61, "Arrow: same method with 10 % of daily data missing.  Bar: 95 % interval of the false-procedure rate.\nSynthetic astronauts (generator csync-synth-0.1); not real crew, not a clinical performance.", fontsize=7.5, color=INK2)
fig.tight_layout()
os.makedirs(os.path.join(ROOT, "pitch", "figures"), exist_ok=True)
for p in (os.path.join(HERE, "pilot_tradeoff.png"), os.path.join(ROOT, "pitch", "figures", "pilot_tradeoff.png")):
    fig.savefig(p, dpi=200, bbox_inches="tight")
print("saved")
