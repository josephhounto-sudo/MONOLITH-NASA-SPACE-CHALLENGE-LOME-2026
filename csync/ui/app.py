"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

C-Sync interface (Streamlit). Reads capsules only. Owner: M3 (task cards M3-1..M3-3).
Run: streamlit run csync/ui/app.py

Every colour comes from csync/config/theme.json and every text from csync/config/strings_en.json.
Only exception allowed by card M3-3: the resume button calls csync.gate.resume_gate with the inputs stored in the capsule.
"""
import importlib.util
import json
import os
import re
import sys
import tempfile
from datetime import datetime

import jsonschema
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from csync.capsule import human_reason  # noqa: E402
from csync.gate import resume_gate  # noqa: E402
from csync import habitat, silhouette  # noqa: E402

CFG = os.path.join(ROOT, "csync", "config")
theme = json.load(open(os.path.join(CFG, "theme.json"), encoding="utf8"))
strings = json.load(open(os.path.join(CFG, "strings_en.json"), encoding="utf8"))
UI = strings["ui"]
SCHEMA = json.load(open(os.path.join(ROOT, "contracts", "decision_capsule.schema.json"), encoding="utf8"))
DIMENSIONS = ["Body", "Attention", "Morale", "Mission", "Habitat"]
CONTEXT_DIMENSIONS = ("Mission", "Habitat")


# ------------------------------------------------------------------ data
def fallback_capsules():
    """Capsule file missing: build the same capsules in memory with scripts/run_story.py (written to a temp dir)."""
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with tempfile.TemporaryDirectory() as d:
        return mod.main(d)["histoire"]


@st.cache_data
def load_capsules():
    path = os.path.join(ROOT, "data", "out", "capsules_histoire.json")
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.load(f), False
    return fallback_capsules(), True


def is_valid(cap):
    try:
        jsonschema.validate(cap, SCHEMA)
        return True
    except jsonschema.ValidationError:
        return False


def load_procedure(pid):
    path = os.path.join(ROOT, "data", "procedures", f"{pid}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf8") as f:
        return json.load(f)


# ------------------------------------------------------------------ pieces
def card(dim, state, day):
    s = theme["state"].get(state, theme["state"]["UNKNOWN"])
    if dim in CONTEXT_DIMENSIONS:
        label = UI["context_only"]
    elif state == "UNKNOWN" and day <= 5:
        label = strings["baseline_building"].format(n=day)
    else:
        label = strings["states"][state]
    return (f"<div style='background:{theme['panel']};border-left:6px solid {s['color']};padding:10px;border-radius:4px'>"
            f"<div style='color:{theme['text']};font-weight:600'>{dim}</div>"
            f"<div style='color:{s['color']};font-size:1.1em'>{s['icon']} {label}</div></div>")


def fixed_sentence():
    st.info(strings["fixed_medical_sentence"])


def nominal(cap, day):
    st.subheader(cap["situation"])
    cols = st.columns(len(DIMENSIONS))
    for col, dim in zip(cols, DIMENSIONS):
        col.markdown(card(dim, cap["states"].get(dim, "UNKNOWN"), day), unsafe_allow_html=True)
    st.markdown(f"**{UI['why_label']}** — {cap['explanation']}")
    st.markdown(f"**{UI['action_label']}** — {cap['action'].get('text', '')}")
    with st.expander(UI["signals_label"]):
        st.dataframe([{k: s.get(k) for k in ("indicator_id", "name", "value", "unit", "baseline_mean", "d", "flagged")}
                      for s in cap["signals"]], hide_index=True)
        st.caption(f"{UI['evidence_label']}: {cap['evidence']}")
    st.caption(strings["human_decision_pending"])


def action_screen(cap):
    st.markdown(f"### {UI['emergency_title']}")
    st.subheader(cap["situation"])
    fixed_sentence()
    proc = load_procedure(cap["action"]["procedure_id"])
    if proc is None:
        st.error(UI["invalid_capsule"])
        return
    steps = proc["steps"]
    key = f"step_{cap['action']['procedure_id']}"
    st.session_state.setdefault(key, 0)
    i = st.session_state[key]
    c1, c2, c3 = st.columns([1, 3, 1])
    if c1.button(UI["previous"], disabled=i == 0, key="prev"):
        st.session_state[key] = i = max(0, i - 1)
    if c3.button(UI["next"], disabled=i == len(steps) - 1, key="next"):
        st.session_state[key] = i = min(len(steps) - 1, i + 1)
    step = steps[i]
    c2.markdown(f"**{UI['step_counter'].format(n=step['n'], total=len(steps))}** — {step['text']}")
    recorded = {}
    for s in cap["signals"]:
        recorded.setdefault(s["indicator_id"], []).append(f"{s['value']:g}")
    for m in step.get("measures", [step] if step.get("how_to") else []):
        with st.container(border=True):
            title = m.get("measure", "")
            st.markdown(f"**{title}**")
            st.markdown(f"*{UI['how_to']}:* {m.get('how_to', '')}")
            why, url = m.get("why", ""), m.get("hrp_source_url", "")
            if m.get("nasa_reference") is False or not why or not url.startswith("https://www.nasa.gov/"):
                st.markdown(f"*{UI['source']}:* {UI['no_nasa_reference']}")
            else:
                st.markdown(f"*{UI['why']}:* {why}")
                st.markdown(f"*{UI['source']}:* {url}")
            if m.get("indicator_id") in recorded:
                st.markdown(f"*{UI['recorded']}:* {' / '.join(recorded[m['indicator_id']])} {m.get('unit', '')}")
    q = cap.get("send_queue", {})
    if q:
        t_down, t_up = q["report_created_utc"][11:16], q["report_received_utc"][11:16]
        clock = st.radio(UI["link_clock"], [f"{t_down} — {UI['link_down']}", f"{t_up} — {UI['link_up']}"], horizontal=True)
        if clock.startswith(t_down):
            st.warning(strings["waiting_link"])
        else:
            st.success(strings["delivered_once"])
    st.caption(strings["human_decision_pending"])


def resume_screen(cap):
    st.markdown(f"### {UI['resume_title']}")
    st.subheader(cap["situation"])
    gi = cap["gate_inputs"]
    proc = load_procedure(gi["procedure_id"]) or {}
    gate_proc = {k: proc.get(k) for k in ("prerequisites", "no_physical_prereq", "override_policy")}
    req = datetime.fromisoformat(gi["request_time_utc"])
    meas = [{**m, "timestamp": datetime.fromisoformat(m["timestamp"])} for m in gi["measurements"]]
    st.session_state.setdefault("resume_log", [])
    c1, c2 = st.columns(2)
    if c1.button(UI["request_resume"], key="request_resume"):
        st.session_state["resume_result"] = resume_gate(req, meas, gate_proc)
    if c2.button(UI["commander_override"], key="override"):
        d, reasons = resume_gate(req, meas, gate_proc, override={"by": "Commander"})
        st.session_state["resume_result"] = (d, reasons)
        st.session_state["resume_log"].append(UI["override_logged"].format(t=gi["request_time_utc"][11:16], d=d))
    if "resume_result" in st.session_state:
        d, reasons = st.session_state["resume_result"]
        colour = theme["state"]["DEGRADED" if d == "REFUSE_RESUME" else "NORMAL"]["color"]
        st.markdown(f"<div style='color:{colour};font-size:1.4em;font-weight:700'>{UI['decision']}: {d}</div>",
                    unsafe_allow_html=True)
        st.markdown(f"**{UI['reasons']}**")
        for r in reasons:
            st.markdown(f"- {human_reason(r)}")
        with st.expander(UI["technical_log"]):
            for r in reasons:
                st.text(r)
    if st.session_state["resume_log"]:
        st.markdown(f"**{UI['log_title']}**")
        for line in st.session_state["resume_log"]:
            st.text(line)
    fixed_sentence()
    st.caption(strings["human_decision_pending"])


def trend_svg(rows, base, thr, label, direction):
    """Line chart as an SVG Markdown image with alt text (Vega marks carry no alt, axe svg-img-alt)."""
    import base64
    W, H, L, R, T, B = 640, 220, 52, 16, 16, 34
    vals = [r["value"] for r in rows if r["value"] is not None]
    lo, hi = min(vals + [base, thr]), max(vals + [base, thr])
    pad = (hi - lo) * 0.1 or 1
    lo, hi = lo - pad, hi + pad
    n = max(len(rows) - 1, 1)
    X = lambda i: L + (W - L - R) * i / n
    Y = lambda v: T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    c_val, c_base, c_thr = theme["interactive"], theme["text_secondary"], theme["state"]["WATCH"]["color"]
    txt = theme["text_secondary"]
    g = [f'<rect width="{W}" height="{H}" fill="{theme["surface"]}"/>']
    for v in (lo + pad, (lo + hi) / 2, hi - pad):
        g.append(f'<text x="{L-6}" y="{Y(v)+4:.0f}" font-size="11" text-anchor="end" fill="{txt}" font-family="sans-serif">{v:.3g}</text>')
    for i, r in enumerate(rows):
        g.append(f'<text x="{X(i):.0f}" y="{H-14}" font-size="11" text-anchor="middle" fill="{txt}" font-family="sans-serif">{r["day"]}</text>')
    g.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-1}" font-size="11" text-anchor="middle" fill="{txt}" font-family="sans-serif">Mission day</text>')
    g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(base):.1f}" y2="{Y(base):.1f}" stroke="{c_base}" stroke-width="1.5" stroke-dasharray="2 4"/>')
    g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(thr):.1f}" y2="{Y(thr):.1f}" stroke="{c_thr}" stroke-width="1.5" stroke-dasharray="6 4"/>')
    pts = " ".join(f"{X(i):.1f},{Y(r['value']):.1f}" for i, r in enumerate(rows) if r["value"] is not None)
    g.append(f'<polyline points="{pts}" fill="none" stroke="{c_val}" stroke-width="2"/>')
    for i, r in enumerate(rows):
        if r["value"] is None:
            continue
        fill = c_thr if r["flagged"] else c_val
        g.append(f'<circle cx="{X(i):.1f}" cy="{Y(r["value"]):.1f}" r="{5 if r["flagged"] else 3}" fill="{fill}" stroke="{theme["surface"]}" stroke-width="2"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + "".join(g) + "</svg>"
    flagged = [str(r["day"]) for r in rows if r["flagged"]]
    alt = (f"{label}, days {rows[0]['day']} to {rows[-1]['day']}: values {min(vals):.3g} to {max(vals):.3g}; personal baseline {base:.3g}, "
           f"threshold {thr:.3g}" + (f"; flagged days {', '.join(flagged)}." if flagged else "; no flagged day."))
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    return f"![{alt}]({uri})"


def trends_panel(day):
    """Dynamic chart per indicator up to the chosen day, against the personal baseline (reads data/out/trends_histoire.json)."""
    path = os.path.join(ROOT, "data", "out", "trends_histoire.json")
    if not os.path.exists(path):
        return
    data = json.load(open(path, encoding="utf8"))["indicators"]
    st.divider()
    st.subheader(UI["trend_title"])
    st.markdown(UI["trend_intro"])
    names = UI["trend_names"]
    ind = st.pills(UI["trend_select"], list(names), format_func=names.get, selection_mode="single",
                   default="PH09", key="trend_indicator")
    if not ind:
        return
    t = data[ind]
    rows = [r for r in t["days"] if r["day"] <= day]
    frame = {UI["trend_value"]: [r["value"] for r in rows], UI["trend_base"]: [t["baseline_mean"]] * len(rows),
             UI["trend_thr"]: [t["threshold"]] * len(rows)}
    vals = [r["value"] for r in rows]
    st.markdown(trend_svg(rows, t["baseline_mean"], t["threshold"], f"{names[ind]} ({t['unit']})", t["direction"]),
                unsafe_allow_html=False)
    flagged = [str(r["day"]) for r in rows if r["flagged"]]
    st.markdown(UI["trend_flagged"].format(day=day, days=", ".join(flagged)) if flagged else UI["trend_none"].format(day=day))
    if day <= 5:
        st.caption(UI["trend_building"])


def hazards_panel():
    st.divider()
    st.subheader(UI["hazard_title"])
    st.markdown(UI["hazard_intro"])
    cols = UI["hazard_cols"]
    st.dataframe([{cols[k]: r[k] for k in cols} for r in UI["hazard_rows"]], hide_index=True)
    st.caption(UI["hazard_source"])


def body_map(symptom_zone=None, day=None):
    """Body map section: 8 selectable zones (pills) next to a neutral figure; text comes from pitch/silhouette/fiches.json."""
    st.divider()
    st.subheader(UI["body_map_title"])
    st.markdown(UI["body_map_intro"])
    sheets = silhouette.fiches()
    labels = {rid: silhouette.label(rid) for rid in sheets}
    preset = silhouette.region_for_zone(symptom_zone)
    if preset:
        st.markdown(UI["body_map_symptom"].format(day=day, zone=symptom_zone))
    choice = st.pills(UI["body_map_select"], list(labels), format_func=labels.get, selection_mode="single",
                      default=preset, key=f"body_zone_{day}")
    left, right = st.columns([2, 3])
    left.markdown(silhouette.markdown_image(choice, UI["body_map_alt"].format(zone=labels[choice] if choice else "none")))
    if not choice:
        return
    r = sheets[choice]
    state = silhouette.STATUS_STATE[r["status"]]
    with right:
        st.markdown(f"#### {r['title']}")
        st.markdown(f"**{theme['state'][state]['icon']} {silhouette.STATUS_WORD[r['status']]}**")
        st.markdown(f"**{UI['body_map_indicators']}:** " + "; ".join(r["indicators"]))
        for key, lab in (("how", "body_map_how"), ("why", "body_map_why"), ("when", "body_map_when"), ("not", "body_map_not")):
            text = r.get(key)
            if key == "why" and not text:
                text = UI["body_map_no_ref"] if r["status"] == "measured" else None
            if text:
                st.markdown(f"**{UI[lab]}:** {text}")
        srcs = [s for s in (r.get("how_src"), r.get("when_src")) if s]
        if srcs:
            st.caption(f"{UI['body_map_source']}: " + " · ".join(srcs))


def habitat_panel():
    """Real NASA ISS cabin data, context only. Reads data/real/habitat_*.csv (built by scripts/build_habitat.py)."""
    st.divider()
    st.subheader(UI["habitat_title"])
    st.markdown(UI["habitat_intro"])
    df = habitat.rr1_hourly()
    flat = df[df["artifact"]]
    chart = df.set_index("hour_utc")[["co2_mmhg"]].rename(columns={"co2_mmhg": UI["habitat_series_co2"]})
    chart[UI["habitat_series_limit"]] = habitat.LIMIT_MMHG
    chart[UI["habitat_series_flat"]] = df.set_index("hour_utc")["co2_mmhg"].where(df.set_index("hour_utc")["artifact"])
    st.line_chart(chart, color=[theme["interactive"], theme["text_secondary"], theme["state"]["UNKNOWN"]["color"]])
    if len(flat):
        run = habitat.missions().set_index("mission").loc["RR-1"]
        ppm = float(run["longest_run_ppm"])
        st.markdown(UI["habitat_flag"].format(ppm=ppm, mm=habitat.ppm_to_mmhg(ppm), hours=float(run["longest_run_h"])))
    m = habitat.missions()
    ms = habitat.rr1_measurements()
    count = lambda q: sum(1 for x in ms if x["quality"] == q)  # noqa: E731
    st.caption(UI["habitat_measurements"].format(n=len(ms), ok=count("OK"), art=count("ARTIFACT"), miss=count("MISSING")))
    with st.expander(UI["habitat_more_title"]):
        hourly = df.set_index("hour_utc")
        st.line_chart(hourly[["temp_c"]].rename(columns={"temp_c": UI["habitat_temp"]}), color=[theme["interactive"]])
        st.line_chart(hourly[["rh_pct"]].rename(columns={"rh_pct": UI["habitat_rh"]}), color=[theme["interactive"]])
        rad = habitat.rr1_radiation()
        st.bar_chart(rad.set_index("date")[["total_mgy_day"]].rename(columns={"total_mgy_day": UI["habitat_rad"]}),
                     color=[theme["interactive"]])
        st.caption(UI["habitat_rad_note"].format(acc=float(rad["accumulated_mgy"].iloc[-1])))
    st.markdown(f"**{UI['habitat_table_title']}**")
    st.dataframe(m[list(UI["habitat_columns"])].rename(columns=UI["habitat_columns"]), hide_index=True)
    st.caption(UI["habitat_table_note"].format(n=len(m), k=int((m["artifact_runs_ge_1h"] > 0).sum())))
    st.caption(UI["habitat_credit"])


def provenance_table():
    st.divider()
    st.subheader(UI["prov_title"])
    cols = UI["prov_cols"]
    st.dataframe([{cols[k]: row[k] for k in cols} for row in UI["prov_rows"]], hide_index=True)


# ------------------------------------------------------------------ page
st.set_page_config(page_title=strings["app_title"], layout="wide")
st.warning(strings["synthetic_banner"])
caps, fallback = load_capsules()
if fallback:
    st.caption(UI["fallback_notice"])
day = st.slider(UI["day_slider"], 1, 10, 7)
today = [c for c in caps if c.get("day") == day]
daily = next((c for c in today if c.get("capsule_type", "daily") == "daily"), None)
priority = [c for c in today if c.get("capsule_type") in ("emergency", "resume") and is_valid(c)
            and (c.get("ui_hint") == "ACTION" or c.get("capsule_type") == "resume")]


def action_blocks():
    for c in priority:
        if c.get("capsule_type") == "emergency":
            action_screen(c)
        else:
            resume_screen(c)
        st.divider()


if priority:
    st.info(UI["priority_notice"])
    action_blocks()   # adaptive order: an open procedure comes before the daily cards
if daily is None:
    st.error(UI["no_capsule"])
elif not is_valid(daily):
    st.error(UI["invalid_capsule"])
else:
    nominal(daily, day)
_zone = None
for _c in today:
    if _c.get("capsule_type") == "emergency":
        _m = re.search(r"zone: ([a-z]+)", _c.get("situation", ""))
        _zone = _m.group(1) if _m else None
trends_panel(day)
body_map(_zone, day)
hazards_panel()
habitat_panel()
provenance_table()
