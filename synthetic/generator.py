"""Synthetic scenario generator for the demo story "Mars transit, days 1 to 10" (generator csync-synth-0.1).

Every value produced here is SYNTHETIC and labelled as such (origin, generator_version, seed).
Person parameters are design choices, not clinical references. Real data used:
- NASA OSDR EDA RR-1 (ISS cabin CO2 / temperature / humidity / radiation) -> origin REAL_OPEN
- PhysioNet S10 (wrist sensor noise 5.1 bpm, ~55 % beat coverage) -> noise model only
Variants: "histoire" (story with drift + emergency), "temoin" (control, no drift), "capteur" (sensor outage).
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from csync.rules import DIMENSION_OF

GENERATOR_VERSION = "csync-synth-0.1"
DAY0 = datetime(2031, 3, 1)   # fictional day 1 (UTC)
UNITS = {"PH01": "bpm", "PH09": "h", "PH10": "mmHg", "PH11": "degC", "PH12": "mg/dL", "SY01": "category",
         "CO01": "ms", "CO02": "count (>=355 ms)", "PS01": "KSS 1-9", "PS02": "0-10", "PS03": "1-5", "PS04": "0-10",
         "MI03": "0-10", "MI05": "min", "HA01": "ppm", "HA02": "degC", "HA03": "%", "HA05": "mGy/day"}
EVIDENCE = {"PH01": "DIRECT_MEASUREMENT", "PH09": "SELF_REPORTED", "PH10": "DIRECT_MEASUREMENT", "PH11": "DIRECT_MEASUREMENT",
            "PH12": "DIRECT_MEASUREMENT", "SY01": "SELF_REPORTED", "CO01": "BIOLOGICAL_TEST", "CO02": "BIOLOGICAL_TEST",
            "PS01": "SELF_REPORTED", "PS02": "SELF_REPORTED", "PS03": "SELF_REPORTED", "PS04": "SELF_REPORTED",
            "MI03": "OPERATIONAL_PROXY", "MI05": "MISSION_CONTEXT", "HA01": "DIRECT_MEASUREMENT", "HA02": "DIRECT_MEASUREMENT",
            "HA03": "DIRECT_MEASUREMENT", "HA05": "DIRECT_MEASUREMENT"}

def ts(day: int, hh: int, mm: int = 0) -> datetime:
    return DAY0 + timedelta(days=day - 1, hours=hh, minutes=mm)

def meas(t, ind, value, quality="OK", origin="SYNTHETIC", source="SYN", value_text="", seed=None):
    return {"timestamp_utc": t.isoformat(timespec="minutes"), "day": (t - DAY0).days + 1, "indicator_id": ind,
            "dimension": DIMENSION_OF.get(ind, ""), "value": value, "value_text": value_text, "unit": UNITS.get(ind, ""),
            "quality": quality, "origin": origin, "source_id": source, "evidence_kind": EVIDENCE.get(ind, ""),
            "generator_version": GENERATOR_VERSION if origin == "SYNTHETIC" else "", "seed": seed if origin == "SYNTHETIC" else ""}

# ---------------------------------------------------------------- générateur
@dataclass
class Person:  # valeurs de référence de l'astronaute fictif (conception)
    sleep_h: float = 7.2;  sleep_sd: float = 0.45
    hr_rest: float = 62.0; hr_sd: float = 2.5
    rt_ms: float = 265.0;  rt_trial_sd: float = 0.18   # log-normal par essai (sigma)
    rt_day_sd: float = 10.0
    kss: float = 3.0;  kss_sd: float = 0.8
    stress: float = 3.0; stress_sd: float = 1.0    # 3 = médiane réelle des niveaux « Baseline » de S10 (n=36)
    mood: float = 3.8;  mood_sd: float = 0.4
    load: float = 4.0;  load_sd: float = 1.0
    sbp: float = 118; dbp: float = 76; bp_sd: float = 5
    temp_c: float = 36.6; temp_sd: float = 0.15

def pvt_session(rng, mean_rt, day_shift, sigma=0.18, duration_s=180):
    """Simule un PVT-B de 3 min : intervalles 1-4 s, temps de réaction log-normaux. Renvoie (moyenne, lapses>=355, n)."""
    t, rts = 0.0, []
    mu = math.log(mean_rt + day_shift) - sigma**2 / 2
    while t < duration_s:
        isi = rng.uniform(1, 4)
        rt = float(np.exp(rng.normal(mu, sigma)))
        rts.append(rt)
        t += isi + rt / 1000
    rts = np.array(rts)
    return float(rts.mean()), int((rts >= 355).sum()), len(rts)

def clip_int(x, lo, hi):
    return int(min(hi, max(lo, round(x))))

def generate(variant="histoire", seed=42, person: Person | None = None, n_days=10, drift_amp=1.5,
             wrist_coverage=0.55, habitat=None, radiation=None, outage=None, drift=True, event=True, fast=False):
    """Génère les Mesures du scénario. variant ∈ {histoire, temoin, capteur}.
    drift_amp = amplitude de la dérive en écarts-types personnels (P-05 : 1 à 2)."""
    rng = np.random.default_rng(seed)
    p = person or Person()
    rows = []
    drift_days = {6: 0.6, 7: 0.85, 8: 1.0, 9: 1.1} if (drift and variant == "histoire") else {}
    for day in range(1, n_days + 1):
        k = drift_days.get(day, 0.0)  # fraction de l'amplitude
        a = drift_amp * k
        # --- nuit et sommeil déclaré (P-04 : < 6 h les jours 6 à 9)
        sleep = p.sleep_h + rng.normal(0, p.sleep_sd) - a * p.sleep_sd
        if variant == "histoire" and day in drift_days:
            sleep = min(sleep, 5.9 - 0.25 * (day - 6))
        rows.append(meas(ts(day, 7, 30), "PH09", round(sleep * 4) / 4, seed=seed))
        # --- FC de repos (moyenne 06:00-07:00 du poignet) : dérive légère, pas exigée par P-05
        hr_rest = p.hr_rest + rng.normal(0, p.hr_sd) + 0.5 * a * p.hr_sd
        # --- check-in 07:30
        rows.append(meas(ts(day, 7, 31), "PS01", clip_int(p.kss + rng.normal(0, p.kss_sd) + a * p.kss_sd, 1, 9), seed=seed))
        rows.append(meas(ts(day, 7, 32), "PS02", clip_int(p.stress + rng.normal(0, p.stress_sd) + 0.4 * a * p.stress_sd, 0, 10), seed=seed))
        m1 = clip_int(p.mood + rng.normal(0, p.mood_sd) - 0.3 * a * p.mood_sd, 1, 5)
        m2 = clip_int(p.mood + rng.normal(0, p.mood_sd) - 0.3 * a * p.mood_sd, 1, 5)
        rows.append(meas(ts(day, 7, 33), "PS03", (m1 + m2) / 2, value_text=f"{m1};{m2}", seed=seed))
        rows.append(meas(ts(day, 7, 34), "PS04", clip_int(p.load + rng.normal(0, p.load_sd) + 0.3 * a * p.load_sd, 0, 10), seed=seed))
        # --- PVT-B 3 min à 08:00
        mean_rt, lapses, n = pvt_session(rng, p.rt_ms, rng.normal(0, p.rt_day_sd) + a * 2.2 * p.rt_day_sd)
        rows.append(meas(ts(day, 8, 0), "CO01", round(mean_rt, 1), value_text=f"n={n}", seed=seed))
        rows.append(meas(ts(day, 8, 0), "CO02", lapses, value_text=f"n={n}", seed=seed))
        # --- tension et température quotidiennes (07:40)
        sbp = round(p.sbp + rng.normal(0, p.bp_sd)); dbp = round(p.dbp + rng.normal(0, p.bp_sd * 0.7))
        rows.append(meas(ts(day, 7, 40), "PH10", sbp, value_text="SYS", seed=seed))
        rows.append(meas(ts(day, 7, 40), "PH10", dbp, value_text="DIA", seed=seed))
        rows.append(meas(ts(day, 7, 41), "PH11", round(p.temp_c + rng.normal(0, p.temp_sd), 1), seed=seed))
        # --- mission
        rows.append(meas(ts(day, 7, 0), "MI03", clip_int(5 + (1 if day in (6, 7, 8) else 0) + rng.normal(0, 0.7), 0, 10), seed=seed))
        rows.append(meas(ts(day, 0, 0), "MI05", 20, origin="SYNTHETIC", seed=seed, value_text="parameter"))
        # --- poignet : FC toutes les 5 min (24 h) ; mode rapide (Monte-Carlo) = moyenne 06:00-07:00 directement
        if fast:
            n_ok = rng.binomial(12, min(1.0, wrist_coverage + 0.35))
            v = None if n_ok < 3 else round(hr_rest - 4 * math.cos(2 * math.pi * (6.5 - 4) / 24) + rng.normal(0, 5.1 / math.sqrt(n_ok)), 1)
            rows.append(meas(ts(day, 7, 0), "PH01", v, quality="OK" if v is not None else "MISSING", source="WRIST-DAILY", seed=seed))
        for i in (range(0) if fast else range(288)):
            t = ts(day, 0) + timedelta(minutes=5 * i)
            hour = t.hour + t.minute / 60
            if outage and outage[0] <= t < outage[1]:
                rows.append(meas(t, "PH01", None, quality="MISSING", source="WRIST", seed=seed, value_text="sensor outage"))
                continue
            if rng.random() > min(1.0, wrist_coverage + 0.35):  # part de fenêtres de 5 min sans battement fiable
                rows.append(meas(t, "PH01", None, quality="MISSING", source="WRIST", seed=seed, value_text="no beat detected"))
                continue
            circ = -4 * math.cos(2 * math.pi * (hour - 4) / 24)  # creux nocturne (conception)
            awake = 0 if (hour < 6.5 or hour >= 23) else 12
            v = hr_rest + circ + awake + rng.normal(0, 5.1)       # 5,1 bpm = médiane du bruit intra-fenêtre S10
            q = "ARTIFACT" if rng.random() < 0.01 else "OK"
            if q == "ARTIFACT":
                v = v + rng.choice([-35, 45])
            rows.append(meas(t, "PH01", round(v, 1), quality=q, source="WRIST", seed=seed))
        # --- habitat réel (EDA RR-1) : 1 point par heure
        if habitat is not None:
            for _, r in habitat[habitat.story_day == day].iterrows():
                t = ts(day, int(r.hour))
                for ind, col in (("HA01", "co2_ppm"), ("HA02", "temp_c"), ("HA03", "rh_pct")):
                    rows.append(meas(t, ind, r[col], origin="REAL_OPEN", source="S03-EDA-RR1"))
        if radiation is not None:
            rr = radiation[radiation.story_day == day]
            for _, r in rr.iterrows():
                rows.append(meas(ts(day, 12), "HA05", r.total_mgy_day, origin="REAL_OPEN", source="S03-EDA-RR1"))
    # --- jour 9 : urgence (acte 2)
    if variant == "histoire" and event:
        rows.append(meas(ts(9, 14, 10), "SY01", None, value_text="chest_pain;zone=thorax", seed=seed))
        rows.append(meas(ts(9, 14, 13), "PH01", 104, source="GUIDED", seed=seed, value_text="guided measurement"))
        rows.append(meas(ts(9, 14, 15), "PH10", 142, source="GUIDED", value_text="SYS", seed=seed))
        rows.append(meas(ts(9, 14, 15), "PH10", 91, source="GUIDED", value_text="DIA", seed=seed))
        rows.append(meas(ts(9, 14, 17), "PH11", 36.9, source="GUIDED", seed=seed))
        rows.append(meas(ts(9, 14, 19), "PH12", 112, source="GUIDED", seed=seed, value_text="no NASA in-flight reference"))
        # --- jour 10 : mesures guidées avant la demande de reprise (acte 3)
        rows.append(meas(ts(10, 8, 46), "PH01", 71, source="GUIDED", seed=seed, value_text="guided measurement"))
        rows.append(meas(ts(10, 8, 55), "CO01", 268.0, source="GUIDED", seed=seed, value_text="control PVT"))
    df = pd.DataFrame(rows)
    df.insert(0, "variant", variant)
    return df

