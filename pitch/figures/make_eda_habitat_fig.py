"""FICHIER: pitch/figures/make_eda_habitat_fig.py · 14/11/2026 ~14:40 UTC · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Figure C6 from the RAW 5-min series of NASA EDA mission RR-1 (data/real/raw/eda_all_missions.json.gz).
Plateau detected with csync.quality.flag_plateaus(min_len=144) = constant for >= 12 h (144 points of 5 min).
Run from the repo root: python pitch/figures/make_eda_habitat_fig.py   (writes the EN and FR PNG files)."""
import gzip, json, os, sys
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
sys.path.insert(0, os.getcwd())
from csync.quality import flag_plateaus

d = json.load(gzip.open("data/real/raw/eda_all_missions.json.gz"))["missions"]["RR-1"]["telemetry"]
ts = [datetime.fromisoformat(x) for x in d["time"]]
runs = flag_plateaus(d["co2_iss"], min_len=144)
assert len(runs) == 1, runs
r = runs[0]
hours = (ts[r["end"]] - ts[r["start"]]).total_seconds() / 3600 + 5 / 60
assert r["length"] == 1837 and r["value"] == 2646, r
lo, hi = datetime(2014, 9, 20), datetime(2014, 10, 6)
idx = [i for i, t in enumerate(ts) if lo <= t <= hi]
x = [ts[i] for i in idx]

L = {
 "en": dict(title="Real ISS cabin telemetry, mission RR-1 (Sep 20 – Oct 6, 2014) · 5-min data",
            co2="CO$_2$ (ppm)", tmp="Cabin temperature (°C)", rh="Relative humidity (%)",
            note=f"constant {r['value']:,} ppm for {hours:.0f} h (6.4 days)\n→ flagged ARTIFACT, never read as “normal”",
            foot="Data and visualizations are courtesy of the NASA OSDR Environmental Data App (EDA). Real data; the crew in the demo is synthetic.",
            out="pitch/figures/nasa_eda_habitat_en.png"),
 "fr": dict(title="Télémétrie réelle de la cabine ISS, mission RR-1 (20 sept. – 6 oct. 2014) · données à 5 min",
            co2="CO$_2$ (ppm)", tmp="Température cabine (°C)", rh="Humidité relative (%)",
            note=f"constant à {r['value']:,} ppm pendant {hours:.0f} h (6,4 jours)\n→ signalé ARTIFACT, jamais lu comme « normal »".replace(",", " ", 1),
            foot="Données et visualisations : NASA OSDR Environmental Data App (EDA). Données réelles ; l'équipage de la démo est simulé.",
            out="pitch/figures/nasa_eda_habitat_fr.png"),
}
for lang, t in L.items():
    fig, ax = plt.subplots(3, 1, figsize=(16, 8.3), sharex=True, dpi=120)
    for a, key, lab in zip(ax, ["co2_iss", "temperature_iss", "rh_iss"], [t["co2"], t["tmp"], t["rh"]]):
        a.plot(x, [d[key][i] for i in idx], color="#1f4e79", lw=1.2)
        a.set_ylabel(lab, fontsize=13); a.grid(alpha=.25); a.tick_params(labelsize=12)
    ax[0].axvspan(ts[r["start"]], ts[r["end"]], color="#e8a96a", alpha=.35)
    ax[0].annotate(t["note"], xy=(datetime(2014, 9, 24, 12), 2646), xytext=(datetime(2014, 9, 21, 14), 3650),
                   fontsize=15, color="#7a4300", arrowprops=dict(arrowstyle="->", color="#7a4300"))
    ax[0].set_title(t["title"], loc="left", fontsize=15)
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%m-%d")); ax[2].set_xlabel("UTC", fontsize=12)
    fig.text(.01, .008, t["foot"], fontsize=11, color="#444")
    fig.tight_layout(rect=(0, .03, 1, 1))
    fig.savefig(t["out"]); plt.close(fig); print("wrote", t["out"])
