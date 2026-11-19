"""Rapport de recette M4 : scénario, attendu, obtenu, écart, gravité. Owner: M4 (fiche de rôle M4).

Run:  python scripts/recette_m4.py                 (écrit docs/RECETTE_M4.md)
      python scripts/recette_m4.py --seeds 50      (plus rapide)
À relancer sur la version taguée de 22:30 (git checkout checkpoint-sat) : la recette de nuit.
Lecture seule : ne modifie ni les fichiers attendus (data/scenarios/), ni le code. Données SYNTHÉTIQUES.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from csync.rules import DRIFT_INDICATORS, daily_values, evaluate  # noqa: E402
from synthetic.generator import generate  # noqa: E402

DIMS = ("Body", "Attention", "Morale")
# BLOQUANT : un acte de l'histoire ou un garde-fou tombe ; MAJEUR : décision ou écran annoncé faux ;
# MINEUR : écart sans effet sur l'écran ; INFO : à savoir pour le pitch, pas un écart à l'attendu.
SEVERITY_DECISION = "MAJEUR"


def load_run_story():
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scenario(sid):
    with open(os.path.join(ROOT, "data", "scenarios", f"{sid}.json"), encoding="utf8") as f:
        return json.load(f)


def git_ref():
    try:
        out = subprocess.run(["git", "describe", "--tags", "--always", "--dirty"], capture_output=True, text=True, cwd=ROOT, check=False)
        return out.stdout.strip() or "inconnu"
    except OSError:
        return "inconnu"


def daily_rows(rs):
    """Attendu jour par jour (data/scenarios) contre obtenu, avec les paramètres de run_story.py (ce que montre l'écran)."""
    rows = []
    for sid, kw in rs.VARIANTS:
        exp = scenario(sid)["expected"]
        df = generate(sid, seed=42, **kw)
        dv = daily_values(df)
        _, _, states, dec, _ = evaluate(dv)
        dec = dec.set_index("day")
        for d, e in exp["days"].items():
            d = int(d)
            for k in (*DIMS, "decision"):
                want = e.get(k)
                got = dec.at[d, "action"] if k == "decision" else states.at[d, k]
                if want is None:
                    continue
                sev = "" if got == want else (SEVERITY_DECISION if k == "decision" else "MINEUR")
                if want != got and sid == "histoire" and d == 7 and k == "Attention":
                    sev = "MAJEUR"           # écran annoncé par la fiche M3-1 (jour 7 : Attention DEGRADED)
                if want == "UNKNOWN" and got == "NORMAL":
                    sev = "BLOQUANT"         # T1 : jamais NORMAL pendant la référence
                rows.append((sid, d, k, want, got, sev))
        n_proc = int((dec.action == "OPEN_PROCEDURE").sum())
        rows.append((sid, "1-10", "jours de procédure", exp["procedure_days"], n_proc,
                     "" if n_proc == exp["procedure_days"] else SEVERITY_DECISION))
        t1 = [(d, dim) for d in states.index for dim, inds in DRIFT_INDICATORS.items()
              if states.at[d, dim] == "NORMAL" and dv.loc[d, [i for i in inds if i in dv.columns]].isna().any()]
        rows.append((sid, "1-10", "T1 donnée manquante jamais NORMAL", "0 cas", f"{len(t1)} cas", "BLOQUANT" if t1 else ""))
        q = df.quality.value_counts().to_dict()
        rows.append((sid, "1-10", "jeu crédible : MISSING et ARTIFACT présents", "oui",
                     f"MISSING {q.get('MISSING', 0)}, ARTIFACT {q.get('ARTIFACT', 0)}",
                     "" if q.get("MISSING") and q.get("ARTIFACT") else "MINEUR"))
    return rows


def event_rows(rs):
    """Actes 2 et 3 : attendus écrits dans histoire.json, obtenus par les fonctions de run_story.py."""
    events = {e["type"]: e for e in scenario("histoire")["events"]}
    with tempfile.TemporaryDirectory(prefix="recette_m4_") as out:
        caps = rs.main(out)["histoire"]
    em = [c for c in caps if c["capsule_type"] == "emergency"]
    rz = [c for c in caps if c["capsule_type"] == "resume"]
    rows = []
    e = events["SY01"]
    got = f"jour {em[0]['day']} {em[0]['time_utc']} {em[0]['action']['procedure_id']} {em[0]['action']['criticality']}" if em else "aucune"
    want = f"jour {e['day']} {e['time_utc']} {e['procedure_id']} {e['criticality']}"
    rows.append(("histoire", 9, "urgence guidée (T4)", want, got, "" if got == want else "BLOQUANT"))
    r = events["REPORT"]
    q = em[0]["send_queue"] if em else {}
    rows.append(("histoire", 9, "compte rendu : remises au sol (T5)", r["deliveries"], q.get("report_deliveries_to_ground"),
                 "" if q.get("report_deliveries_to_ground") == r["deliveries"] else "BLOQUANT"))
    rows.append(("histoire", 9, "compte rendu : réception affichée", r["received_utc"], q.get("report_received_utc", "")[-5:],
                 "" if q.get("report_received_utc", "").endswith(r["received_utc"]) else "MAJEUR"))
    rows.append(("histoire", 9, "compte rendu : réception gardée par le sol", r["received_utc"],
                 q.get("ground_view_received_utc", "")[-5:],
                 "" if q.get("ground_view_received_utc", "").endswith(r["received_utc"]) else "MINEUR (DEV-03)"))
    e = events["RESUME_REQUEST"]
    got = (rz[0]["action"]["type"], rz[0]["reliability"]["gate_reasons"]) if rz else ("aucune", [])
    ok = got[0] == e["expected"] and any(e["expected_reason"] in x for x in got[1])
    rows.append(("histoire", 10, "reprise refusée (G3)", f"{e['expected']} · {e['expected_reason']}",
                 f"{got[0]} · {'; '.join(got[1])}", "" if ok else "BLOQUANT"))
    ovr = rz[0]["reliability"].get("gate_reasons_with_override", []) if rz else []
    rows.append(("histoire", 10, "même avec forçage (G6)", e["with_override"], "; ".join(ovr) or "aucune",
                 "" if any(x.startswith("G6") for x in ovr) else "BLOQUANT"))
    habitat = sorted({c["states"].get("Habitat") for c in caps if c["capsule_type"] == "daily"})
    rows.append(("histoire", "1-10", "Habitat : vraies données NASA EDA RR-1 (STORY.md)", "état calculé",
                 f"états affichés : {', '.join(map(str, habitat))}", "MAJEUR" if habitat == ["UNKNOWN"] else ""))
    morale = sorted({c["states"].get("Morale") for c in caps if c["capsule_type"] == "daily" and c["day"] >= 6})
    rows.append(("histoire", "6-9", "somnolence en hausse visible (STORY.md)", "Morale hors NORMAL un jour au moins",
                 f"Morale : {', '.join(map(str, morale))}", "INFO" if morale == ["NORMAL"] else ""))
    return rows


def stability(n_seeds):
    """Robustesse : l'histoire tient-elle hors de la graine 42 ? (mêmes paramètres que la démo)"""
    res = {}
    for fast in (True, False):
        n = n_seeds if fast else max(1, n_seeds // 2)
        ok7 = att7 = d6 = 0
        for s in range(1000, 1000 + n):
            _, _, st, dc, _ = evaluate(daily_values(generate("histoire", seed=s, drift_amp=2.5, fast=fast)))
            a = dc.set_index("day").action
            ok7 += a[7] == "OPEN_PROCEDURE"
            att7 += st.at[7, "Attention"] == "DEGRADED"
            d6 += a[6] == "OPEN_PROCEDURE"
        res["rapide (démo)" if fast else "complet"] = (n, 100 * ok7 / n, 100 * att7 / n, 100 * d6 / n)
    return res


def full_mode_check(rs):
    """Proposition à M1 (non appliquée) : histoire et témoin en mode complet du poignet, attendus inchangés."""
    res = {}
    for sid, kw in rs.VARIANTS:
        if not kw.get("fast"):
            continue
        df = generate(sid, seed=42, **{**kw, "fast": False})
        _, _, states, dec, _ = evaluate(daily_values(df))
        dec = dec.set_index("day")
        exp = scenario(sid)["expected"]["days"]
        gaps = [(int(d), k) for d, e in exp.items() for k, want in e.items() if want is not None and
                (dec.at[int(d), "action"] if k == "decision" else states.at[int(d), k]) != want]
        q = df.quality.value_counts().to_dict()
        res[sid] = (gaps, q.get("MISSING", 0), q.get("ARTIFACT", 0))
    return res


def fmt(rows):
    lines = ["| Scénario | Jour | Contrôle | Attendu | Obtenu | Écart | Gravité |", "|---|---|---|---|---|---|---|"]
    for sid, d, k, want, got, sev in rows:
        gap = "non" if not sev else "**oui**"
        lines.append(f"| {sid} | {d} | {k} | {want} | {got} | {gap} | {sev or '—'} |")
    return "\n".join(lines)


def main(n_seeds, out_md):
    rs = load_run_story()
    daily, events = daily_rows(rs), event_rows(rs)
    stab = stability(n_seeds)
    full = full_mode_check(rs)
    gaps = [r for r in daily + events if r[5]]
    by_sev = {s: sum(1 for r in gaps if r[5].startswith(s)) for s in ("BLOQUANT", "MAJEUR", "MINEUR", "INFO")}
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M")
    md = [
        "# Rapport de recette M4 (données et tests)",
        f"Généré le {now} UTC (= heure de Lomé) par `python scripts/recette_m4.py`, version `{git_ref()}`. "
        "Données de démonstration **SYNTHÉTIQUES** (générateur csync-synth-0.1, graine 42). Aucun seuil clinique.",
        "Attendus : `data/scenarios/*.json`, écrits **avant** toute exécution et jamais modifiés après coup "
        "(écarts : `docs/TEST_DEVIATIONS.md`). Obtenus : paramètres de `scripts/run_story.py`, donc ce que montre l'écran.",
        "Gravité : **BLOQUANT** = un acte de l'histoire ou un garde-fou tombe · **MAJEUR** = décision ou écran annoncé "
        "faux · **MINEUR** = écart sans effet sur l'écran · **INFO** = à savoir pour le pitch.",
        "",
        "## Bilan",
        f"- Contrôles : {len(daily) + len(events)} · écarts : {len(gaps)} "
        f"(BLOQUANT {by_sev['BLOQUANT']}, MAJEUR {by_sev['MAJEUR']}, MINEUR {by_sev['MINEUR']}, INFO {by_sev['INFO']}).",
        *[f"- **{r[5]}** · {r[0]} jour {r[1]} · {r[2]} : attendu {r[3]}, obtenu {r[4]}." for r in gaps],
        "",
        "## Actes 2 et 3, habitat",
        fmt(events),
        "",
        "## États et décisions jour par jour",
        fmt(daily),
        "",
        "## Robustesse : l'histoire hors de la graine 42 (INFO)",
        "Mêmes paramètres que la démo (amplitude 2,5, règle `Params()`), graines 1000 et suivantes.",
        "",
        "| Mode du poignet | Graines | Procédure ouverte au jour 7 | Attention DEGRADED au jour 7 | Procédure dès le jour 6 |",
        "|---|---|---|---|---|",
        *[f"| {m} | {n} | {a:.0f} % | {b:.0f} % | {c:.0f} % |" for m, (n, a, b, c) in stab.items()],
        "",
        "Lecture : l'écran du jour 7 (« Attention DEGRADED ») dépend de la graine 42. Ne pas dire au jury que cela "
        "arrive à chaque fois : c'est un scénario de démonstration, pas une mesure.",
        "",
        "## Proposition à M1 (non appliquée) : histoire et témoin en mode complet du poignet",
        "En mode rapide, l'histoire montrée au jury ne contient aucune valeur manquante ni aucun artefact "
        "(piège « jeu trop propre » de la fiche M4). Même graine 42, mêmes attendus, `fast=False` :",
        "",
        "| Scénario | Écarts à l'attendu | MISSING | ARTIFACT |",
        "|---|---|---|---|",
        *[f"| {sid} | {len(g)}{' : ' + ', '.join(f'jour {d} {k}' for d, k in g) if g else ''} | {m} | {a} |"
          for sid, (g, m, a) in full.items()],
        "",
        "À changer ensemble si M1 accepte : `VARIANTS` de `scripts/run_story.py` (M2) et `generate_kwargs.fast` des "
        "scénarios (M4, à noter comme DEV-02 : entrée modifiée, attendus intacts). Les valeurs affichées "
        "(FC de repos, explications) changent : à faire avant les captures de 22:30.",
        "",
        "## Non couvert par cette recette",
        "- Écrans Streamlit (M3) et deck : hors périmètre M4.",
        "- G4 « hors plage » : aucune plage de plausibilité n'est définie, la porte ne lit jamais la valeur.",
        "- T3 « confiance réduite 1 h après le retour du capteur » : le moteur ne produit pas de confiance par heure.",
        "- G10 : la simultanéité est simulée par un indicateur (`pending_lock`), pas par un vrai verrou.",
    ]
    with open(out_md, "w", encoding="utf8") as f:
        f.write("\n".join(md) + "\n")
    print(f"{out_md}: {len(gaps)} écart(s) {by_sev}")
    return gaps


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "RECETTE_M4.md"))
    a = ap.parse_args()
    main(a.seeds, a.out)
