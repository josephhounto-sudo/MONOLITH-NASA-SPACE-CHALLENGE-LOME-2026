"""Commander board: six SYNTHETIC crew members, each evaluated by the SAME rule v3 (csync.rules.evaluate).

The board only sorts and shows what the rule already says: who changed, since when, what is pending a human decision.
Nothing here is a clinical threshold and no member is a real person. Members are generated with csync.synthetic seeds 61001+
(never used for tuning 1000-7149 or held-out 30000-37149).
15/11/2026 · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
"""
from __future__ import annotations

import dataclasses
import math

import pandas as pd

from csync.rules import DRIFT_INDICATORS, Params, daily_values, evaluate
from synthetic.generator import Person, generate

INDICATORS = [i for lst in DRIFT_INDICATORS.values() for i in lst]
RANK = {"OPEN_PROCEDURE": 0, "DEGRADED": 1, "WATCH": 2, "UNKNOWN": 3, "NORMAL": 4}
# label, seed, scenario, drift amplitude (SD), indicators removed from day 6 (sensor gap)
MEMBERS = [("Crew A", 61001, "stable", 0.0, ()), ("Crew B", 61002, "stable", 0.0, ()),
           ("Crew C", 61003, "drift", 1.5, ()), ("Crew D", 61004, "stable", 0.0, ()),
           ("Crew E", 61005, "drift", 2.0, ()), ("Crew F", 61006, "stable", 0.0, ("PH01",))]


def _person(seed: int) -> Person:
    """Small, deterministic personal differences so the six baselines are not identical."""
    k = (seed % 7) - 3
    return dataclasses.replace(Person(), sleep_h=7.2 + 0.15 * k, hr_rest=62.0 + 1.5 * k, rt_ms=265.0 + 4 * k)


def member_series(label: str) -> pd.DataFrame:
    _, seed, scen, amp, gap = next(m for m in MEMBERS if m[0] == label)
    df = generate("histoire" if scen == "drift" else "temoin", seed=seed, person=_person(seed), drift=scen == "drift",
                  event=False, drift_amp=amp, fast=True)
    dv = daily_values(df)[INDICATORS].copy()
    for ind in gap:
        dv.loc[6:, ind] = math.nan
    return dv


def board(day: int, prm: Params = Params()) -> pd.DataFrame:
    """One row per member for mission `day` (1-10), most urgent first. Columns: member, Body, Attention, Morale, action, procedure, since, flagged, human."""
    rows = []
    for label, *_ in MEMBERS:
        z, flags, states, dec, _ref = evaluate(member_series(label), prm)
        st = states.loc[day].to_dict()
        d = dec[dec.day == day].iloc[0]
        action = d.action if d.action == "OPEN_PROCEDURE" else (
            "DEGRADED" if "DEGRADED" in st.values() else "WATCH" if "WATCH" in st.values() else "UNKNOWN" if "UNKNOWN" in st.values() else "NORMAL")
        since = None
        for back in range(day, 0, -1):          # first day of the current unbroken run of non-normal, non-unknown states
            if all(v in ("NORMAL", "UNKNOWN") for v in states.loc[back].values):
                break
            since = back
        flagged = [i for i in INDICATORS if bool(flags.at[day, i])]
        rows.append({"member": label, **st, "action": action, "procedure": d.procedure_id or "", "since": since,
                     "flagged": flagged, "human": "pending" if d.action == "OPEN_PROCEDURE" else ""})
    out = pd.DataFrame(rows)
    out["rank"] = out.action.map(RANK)
    return out.sort_values(["rank", "member"], kind="stable").drop(columns="rank").reset_index(drop=True)
