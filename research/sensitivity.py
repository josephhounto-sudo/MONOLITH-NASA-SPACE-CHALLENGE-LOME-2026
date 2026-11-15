"""Sensitivity of the shipped drift rule on fresh synthetic seeds.

Grid: d threshold 1.0 to 2.5 by 0.25, consecutive days in {1, 2, 3},
baseline length in {3, 5, 7}. Seeds are 60000 and above (never the tuning
range 1000-7149, never the held-out range 30000-37149, never 61001-61006,
never 50000+).

Scenarios, all SYNTHETIC (generator csync-synth-0.1, fast=True):
- false triggers: variant temoin, seeds 60000-60199 (200 crews)
- drift 1.5 SD: variant histoire, drift_amp=1.5, no event, seeds 62000-62149
  (150). This is the story ramp (days 6-9), including the sleep cap in the
  generator. It is not a pure step of 1.5 SD.
- jump 2 SD: temoin seeds 63000-63149, then from day 8 an added shift of
  2 personal baseline SD (days 1-5, ddof=1) on Attention and Morale, in the
  unfavourable direction.

The rule itself is csync.rules.evaluate. Only Params change. SD floors stay
at the shipped values. A hit is at least one OPEN_PROCEDURE.

The cell (1.5, 2, 5) is the shipped rule. Nothing in this grid is an optimum.
Run: python research/sensitivity.py
"""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "research", "pilot"))

from csync.rules import DIRECTION, DRIFT_INDICATORS, Params, daily_values, evaluate
from pilot3 import wilson
from synthetic.generator import generate

D_VALUES = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
CONSEC = [1, 2, 3]
BASELINE = [3, 5, 7]
CONTROL = range(60000, 60200)
GRADUAL = range(62000, 62150)
ABRUPT = range(63000, 63150)
INDS = [i for ids in DRIFT_INDICATORS.values() for i in ids]
JUMP_INDS = DRIFT_INDICATORS["Attention"] + DRIFT_INDICATORS["Morale"]


def frame(seed: int, kind: str) -> pd.DataFrame:
    if kind == "drift15":
        df = generate("histoire", seed=seed, drift=True, event=False, drift_amp=1.5, fast=True)
    else:
        df = generate("temoin", seed=seed, drift=False, event=False, fast=True)
    dv = daily_values(df)
    if kind == "jump2":
        sd = dv.loc[1:5, INDS].std(ddof=1)
        for ind in JUMP_INDS:
            step = sd[ind]
            if pd.notna(step) and step > 0:
                dv.loc[dv.index >= 8, ind] = dv.loc[dv.index >= 8, ind] + DIRECTION[ind] * 2.0 * step
    return dv


def opens(dv: pd.DataFrame, prm: Params) -> bool:
    _, _, _, decisions, _ = evaluate(dv, prm)
    return bool((decisions.action == "OPEN_PROCEDURE").any())


def shipped_cell_matches(seed: int, kind: str) -> bool:
    """Cell (d=1.5, 2 consecutive days, 5-day baseline) equals Params()."""
    dv = frame(seed, kind)
    explicit = Params(baseline_days=5, d_threshold=1.5, consecutive_days=2)
    a = evaluate(dv, Params())
    b = evaluate(dv, explicit)
    same_z = a[0].equals(b[0])
    same_flags = a[1].equals(b[1])
    same_states = a[2].equals(b[2])
    same_dec = a[3].reset_index(drop=True).equals(b[3].reset_index(drop=True))
    return bool(same_z and same_flags and same_states and same_dec)


def run_grid() -> pd.DataFrame:
    crews = {
        "false": [frame(s, "false") for s in CONTROL],
        "drift15": [frame(s, "drift15") for s in GRADUAL],
        "jump2": [frame(s, "jump2") for s in ABRUPT],
    }
    rows = []
    for base in BASELINE:
        for consec in CONSEC:
            for d in D_VALUES:
                prm = Params(baseline_days=base, d_threshold=d, consecutive_days=consec)
                for name, series in crews.items():
                    k = sum(opens(dv, prm) for dv in series)
                    n = len(series)
                    lo, hi = wilson(k, n)
                    rows.append({
                        "d": d, "consecutive": consec, "baseline": base, "scenario": name,
                        "k": k, "n": n, "pct": round(100.0 * k / n, 1),
                        "ci_lo": round(float(lo), 1), "ci_hi": round(float(hi), 1),
                    })
    return pd.DataFrame(rows)


def _cell(grid: pd.DataFrame, d, consec, base, scenario) -> pd.Series:
    m = grid[(grid.d == d) & (grid.consecutive == consec) & (grid.baseline == base) & (grid.scenario == scenario)]
    return m.iloc[0]


def compromise_text(grid: pd.DataFrame) -> str:
    """Describe the tradeoff from this grid. Does not name an optimum."""
    def fmt(row):
        return f"{row.pct:.1f}% ({int(row.k)}/{int(row.n)}, Wilson {row.ci_lo:.1f}–{row.ci_hi:.1f})"

    shipped = {s: _cell(grid, 1.5, 2, 5, s) for s in ("false", "drift15", "jump2")}
    low = {s: _cell(grid, 1.0, 2, 5, s) for s in ("false", "drift15", "jump2")}
    high = {s: _cell(grid, 2.5, 2, 5, s) for s in ("false", "drift15", "jump2")}
    one = {s: _cell(grid, 1.5, 1, 5, s) for s in ("false", "drift15", "jump2")}
    three = {s: _cell(grid, 1.5, 3, 5, s) for s in ("false", "drift15", "jump2")}
    b3 = {s: _cell(grid, 1.5, 2, 3, s) for s in ("false", "drift15", "jump2")}
    b7 = {s: _cell(grid, 1.5, 2, 7, s) for s in ("false", "drift15", "jump2")}
    lines = [
        "Compromis lu sur cette grille (graines neuves, équipages synthétiques). Aucune case n'est un optimum.",
        f"Réglage livré (1,5 ; 2 jours ; référence 5) : faux déclenchements {fmt(shipped['false'])} ; "
        f"dérive 1,5 ET de l'histoire {fmt(shipped['drift15'])} ; saut 2 ET {fmt(shipped['jump2'])}.",
        f"Même référence et 2 jours, seuil 1,0 : faux {fmt(low['false'])}, dérive {fmt(low['drift15'])}, saut {fmt(low['jump2'])}.",
        f"Même référence et 2 jours, seuil 2,5 : faux {fmt(high['false'])}, dérive {fmt(high['drift15'])}, saut {fmt(high['jump2'])}.",
        f"Seuil 1,5 et référence 5, sur 1 jour : faux {fmt(one['false'])}, dérive {fmt(one['drift15'])}, saut {fmt(one['jump2'])}.",
        f"Seuil 1,5 et référence 5, sur 3 jours : faux {fmt(three['false'])}, dérive {fmt(three['drift15'])}, saut {fmt(three['jump2'])}.",
        f"Seuil 1,5 et 2 jours, référence de 3 jours : faux {fmt(b3['false'])}, dérive {fmt(b3['drift15'])}, saut {fmt(b3['jump2'])}.",
        f"Seuil 1,5 et 2 jours, référence de 7 jours : faux {fmt(b7['false'])}, dérive {fmt(b7['drift15'])}, saut {fmt(b7['jump2'])}.",
        "Lire ainsi : abaisser le seuil ou exiger un seul jour augmente à la fois les procédures sur équipage témoin et les procédures sur dérive ou saut. "
        "Monter le seuil ou exiger 3 jours fait l'inverse. Une référence de 7 jours inclut, dans le scénario de dérive, des jours déjà décalés (la rampe de l'histoire commence au jour 6) : la comparaison n'est plus celle d'une référence propre.",
        "Limite : un seul générateur, 10 jours, graines 60000-60199 / 62000-62149 / 63000-63149. Ces taux ne se comparent pas aux 0,7 % / 95,3 % / 59,3 % du pilote 3, qui utilisent d'autres graines et, pour le saut, un écart-type de population.",
    ]
    return "\n".join(lines)


def save_figure(grid: pd.DataFrame, path: str) -> None:
    styles = {1: ("-", "o"), 2: ("--", "s"), 3: (":", "^")}
    titles = {"false": "Faux déclenchements", "drift15": "Dérive 1,5 ET (histoire)", "jump2": "Saut 2 ET"}
    fig, axes = plt.subplots(3, 3, figsize=(11.2, 8.4), sharex=True, sharey=True)
    for r, scenario in enumerate(("false", "drift15", "jump2")):
        for c, base in enumerate(BASELINE):
            ax = axes[r][c]
            sub = grid[(grid.scenario == scenario) & (grid.baseline == base)]
            for consec in CONSEC:
                part = sub[sub.consecutive == consec].sort_values("d")
                ls, mk = styles[consec]
                y = part.pct.to_numpy()
                lo = part.ci_lo.to_numpy()
                hi = part.ci_hi.to_numpy()
                ax.errorbar(
                    part.d, y, yerr=[(y - lo).clip(min=0), (hi - y).clip(min=0)],
                    linestyle=ls, marker=mk, color="black", ecolor="0.45",
                    capsize=2, linewidth=1.2, markersize=5, label=f"{consec} j d'affilée",
                )
            if base == 5:
                hit = sub[(sub.consecutive == 2) & (sub.d == 1.5)].iloc[0]
                ax.scatter([1.5], [hit.pct], s=160, facecolors="none", edgecolors="black", linewidths=1.6, zorder=5)
            ax.set_ylim(-3, 103)
            ax.set_xticks(D_VALUES)
            ax.grid(True, axis="y", color="0.85")
            if r == 0:
                ax.set_title(f"Référence {base} j")
            if c == 0:
                ax.set_ylabel(titles[scenario] + " (%)")
            if r == 2:
                ax.set_xlabel("Seuil d")
            if r == 0 and c == 2:
                ax.legend(frameon=False, fontsize=8)
    fig.suptitle(
        "Sensibilité de la règle v3 — équipages synthétiques, graines 60000+\n"
        "Rond trait plein = 1 jour, carré tireté = 2 jours, triangle pointillé = 3 jours. Barres = Wilson 95 %.\n"
        "Cercle vide = réglage livré (1,5 ; 2 ; 5). Aucune case n'est un optimum.",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)


def main() -> None:
    grid = run_grid()
    out_csv = os.path.join(ROOT, "research", "sensitivity_grid.csv")
    fig = os.path.join(ROOT, "docs", "figures", "sensitivity.png")
    note = os.path.join(ROOT, "research", "sensitivity_note.txt")
    grid.to_csv(out_csv, index=False)
    save_figure(grid, fig)
    text = compromise_text(grid)
    with open(note, "w", encoding="utf8") as f:
        f.write(text + "\n")
    print(text)
    print(f"wrote {out_csv}")
    print(f"wrote {fig}")


if __name__ == "__main__":
    main()
