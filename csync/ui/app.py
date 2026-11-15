"""2026-11-14 ~07:00 Lome (UTC) | reference commit dc61786 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
2026-11-15 ~07:10 (UTC) design-v2: event first on the "stone" container, warm field per criticality — FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

C-Sync interface (Streamlit). Reads capsules only. Owner: M3 (task cards M3-1..M3-3).
Run: streamlit run csync/ui/app.py

Every colour comes from csync/config/theme.json and every text from csync/config/strings_en.json.
Only exception allowed by card M3-3: the resume button calls csync.gate.resume_gate with the inputs stored in the capsule.
"""
import importlib.util
import html
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
from csync import crew, devicefeed as adapters, habitat, silhouette  # noqa: E402
from csync.ui import style  # noqa: E402

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
def card(dim, state, day, hist=""):
    s = theme["state"].get(state, theme["state"]["UNKNOWN"])
    if dim in CONTEXT_DIMENSIONS:
        label = UI["context_only"]
    elif state == "UNKNOWN" and day <= 5:
        label = strings["baseline_building"].format(n=day)
    else:
        label = strings["states"][state]
    ctx = " ctx" if dim in CONTEXT_DIMENSIONS else ""
    return (f"<div class='cs-card{ctx}' data-state='{state if state in theme['state'] else 'UNKNOWN'}' style='{style.card_vars(s['color'])}'>"
            f"<div class='dim'>{dim}</div>"
            f"<div style='color:{s['color']};font-size:1.1em'>{s['icon']} {label}</div>{hist}</div>")


def fixed_sentence():
    st.info(strings["fixed_medical_sentence"])


def nominal(cap, day):
    st.subheader(cap["situation"])
    cols = st.columns(len(DIMENSIONS))
    for col, dim in zip(cols, DIMENSIONS):
        col.markdown(card(dim, cap["states"].get(dim, "UNKNOWN"), day, style.history(STATES_BY_DAY, dim, day)), unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"**{UI['why_label']}** — {cap['explanation']}")
        st.markdown(f"<div class='cs-action'><b>{UI['action_label']}</b> — {html.escape(str(cap['action'].get('text', '')))}</div>",
                    unsafe_allow_html=True)
    with st.expander(UI["signals_label"]):
        st.dataframe([{k: s.get(k) for k in ("indicator_id", "name", "value", "unit", "baseline_mean", "d", "flagged")}
                      for s in cap["signals"]], hide_index=True)
        st.caption(f"{UI['evidence_label']}: {cap['evidence']}")
    st.caption(strings["human_decision_pending"])


def action_screen(cap):
    st.markdown(f"<div class='cs-kicker'>{UI['emergency_title']}</div>", unsafe_allow_html=True)
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
    st.markdown(f"<div class='cs-kicker'>{UI['resume_title']}</div>", unsafe_allow_html=True)
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
        st.markdown(f"<div class='cs-decision' style='color:{colour};{style.card_vars(colour)}'>{UI['decision']}: {d}</div>",
                    unsafe_allow_html=True)
        with st.container(border=True):
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
    ch = theme["chart"]
    c_val, c_base, c_thr, txt = ch["value"], ch["baseline"], ch["threshold"], ch["ink"]
    g = []
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
        g.append(f'<circle cx="{X(i):.1f}" cy="{Y(r["value"]):.1f}" r="{5 if r["flagged"] else 3}" fill="{fill}" stroke="{ch["ring"]}" stroke-width="2"/>')
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


def md_table(cols, rows):
    """Markdown table: long cells wrap (st.dataframe truncates them) and screen readers get a real table."""
    esc = lambda t: str(t).replace("|", "/").replace("\n", " ")
    head = "| " + " | ".join(esc(c) for c in cols.values()) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "\n".join("| " + " | ".join(esc(r[k]) for k in cols) + " |" for r in rows)


@st.cache_data
def _crew_board(day: int):
    return crew.board(day)


def state_glyphs(b, labels):
    """One ring per crew member, ordered by urgency; the state is the ring's shape (solid, double, dotted, dashed), colour only reinforces it."""
    import base64
    f = theme["fusion"]
    sc = f["state_on_light"]
    style = {"OPEN_PROCEDURE": (sc["DEGRADED"], "", 3, True), "DEGRADED": (sc["DEGRADED"], "", 3, False),
             "WATCH": (sc["WATCH"], "6 4", 3, False), "UNKNOWN": (sc["UNKNOWN"], "2 5", 3, False), "NORMAL": (sc["NORMAL"], "", 3, False)}
    g, alt = [], []
    for i, r in enumerate(b.itertuples()):
        col, dash, sw, double = style[r.action]
        cx = 34 + i * 76
        d = f' stroke-dasharray="{dash}"' if dash else ""
        g.append(f'<circle cx="{cx}" cy="34" r="22" fill="none" stroke="{col}" stroke-width="{sw}"{d}/>')
        if double:
            g.append(f'<circle cx="{cx}" cy="34" r="14" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        g.append(f'<text x="{cx}" y="39" text-anchor="middle" font-size="14" font-family="sans-serif" fill="{f["ink"]}">{str(r.member)[-1]}</text>')
        alt.append(f"{r.member}: {labels[r.action]}")
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {34 + len(b) * 76} 70" width="{34 + len(b) * 76}" height="70">' + "".join(g) + "</svg>"
    return f"![{'; '.join(alt)}](data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()})"


def commander_panel(day):
    """Crew-level view for the commander: the same rule on six synthetic members, sorted by urgency. Decides nothing."""
    st.subheader(UI["cmd_title"])
    st.markdown(UI["cmd_intro"])
    b = _crew_board(day)
    n = lambda k: int((b.action == k).sum())
    st.markdown(f"**{UI['cmd_summary'].format(day=day, n_open=n('OPEN_PROCEDURE'), n_deg=n('DEGRADED'), n_watch=n('WATCH'), n_unk=n('UNKNOWN'))}**")
    w, names = UI["cmd_status"], UI["try_names"]
    rows = [{"m": r.member, "b": w[r.Body.upper()] if r.Body.upper() in w else r.Body, "a": w[r.Attention.upper()], "o": w[r.Morale.upper()],
             "s": w[r.action], "t": UI["cmd_since"].format(d=int(r.since)) if r.since == r.since and r.since else "—",
             "f": ", ".join(names[i] for i in r.flagged) or "—", "h": UI["cmd_pending"] if r.human else "—"} for r in b.itertuples()]
    st.markdown(state_glyphs(b, w))
    st.markdown(md_table(UI["cmd_cols"], rows))
    st.caption(UI["cmd_note"])
    st.caption(UI["cmd_synth"])


def hazards_panel():
    st.divider()
    st.subheader(UI["hazard_title"])
    st.markdown(UI["hazard_intro"])
    cols = UI["hazard_cols"]
    st.markdown(md_table(cols, UI["hazard_rows"]))
    st.caption(UI["hazard_source"])


def countermeasures_panel():
    st.divider()
    st.subheader(UI["cm_title"])
    st.markdown(UI["cm_intro"])
    cols = UI["cm_cols"]
    st.markdown(md_table(cols, UI["cm_rows"]))
    st.caption(UI["cm_source"])


def try_panel():
    """Typed check-in -> the same rule v3 engine (csync.live). Synthetic baseline, nothing clinical."""
    import pandas as pd
    from csync import live
    st.subheader(UI["try_title"])
    st.markdown(UI["try_intro"])
    base = live.baseline()
    mean = {i: round(float(base[i].mean()), 1) for i in live.INDICATORS}
    choice = st.radio(UI["try_preset"], [UI["try_preset_base"], UI["try_preset_story"]], horizontal=True, key="try_preset")
    a_, b_ = (mean, mean) if choice == UI["try_preset_base"] else (live.story_day(6), live.story_day(7))
    names = UI["try_names"]
    frame = pd.DataFrame({UI["try_col_ind"]: [names[i] for i in live.INDICATORS],
                          UI["try_col_a"]: [a_.get(i) for i in live.INDICATORS], UI["try_col_b"]: [b_.get(i) for i in live.INDICATORS]})
    edited = st.data_editor(frame, hide_index=True, disabled=[UI["try_col_ind"]], width="stretch",
                            key="try_editor_" + ("b" if choice == UI["try_preset_base"] else "s"))
    def col(c):
        return {i: (None if pd.isna(v) else float(v)) for i, v in zip(live.INDICATORS, edited[c])}
    day6, day7 = col(UI["try_col_a"]), col(UI["try_col_b"])
    with st.expander(UI["ad_title"]):
        st.caption(UI["ad_help"])
        feed = st.text_area(UI["ad_title"], placeholder=UI["ad_ph"], height=120, key="device_feed", label_visibility="collapsed")
    if feed.strip():
        parsed = adapters.parse(feed)
        day6, day7 = parsed["days"][6], parsed["days"][7]
        if parsed["accepted"]:
            st.success(UI["ad_ok"].format(n=parsed["accepted"]))
        for n_, r_ in parsed["rejected"]:
            st.warning(UI["ad_bad"].format(n=n_, r=r_))
    out = live.try_it(day6, day7)
    st.markdown(f"**{UI['try_result']}**")
    cols = st.columns(3)
    for c, dim in zip(cols, ("Body", "Attention", "Morale")):
        c.markdown(card(dim, out["states"][dim], 7).replace("✓ ", ""), unsafe_allow_html=True)   # word + shape; the tick is kept for the slider day only
    rows = [{"n": names[i], "d": "–" if out["z"][i] is None else f"{out['z'][i]:+.1f}",
             "f": "✓ " + UI["try_flagged"] if out["flagged"][i] else ""} for i in live.INDICATORS]
    st.markdown(f"**{UI['try_d_title']}**")
    st.markdown(md_table({"n": UI["try_col_ind"], "d": "d", "f": UI["try_flagged"]}, rows))
    st.info(UI["try_open"].format(p=out["procedure_id"]) if out["action"] == "OPEN_PROCEDURE" else UI["try_continue"])
    flagged = ", ".join(names[i] for i in live.INDICATORS if out["flagged"][i]) or UI["sbar_a_none"]
    st.markdown(f"**{UI['sbar_title']}**")
    st.markdown(f"**{UI['sbar_s']}** — {UI['sbar_s_t']}  \n**{UI['sbar_b']}** — {UI['sbar_b_t']}  \n"
                f"**{UI['sbar_a']}** — " + UI["sbar_a_t"].format(b=out["states"]["Body"], a=out["states"]["Attention"], m=out["states"]["Morale"], f=flagged)
                + f"  \n**{UI['sbar_r']}** — " + (UI["sbar_r_open"].format(p=out["procedure_id"]) if out["action"] == "OPEN_PROCEDURE" else UI["sbar_r_cont"]))


@st.cache_data(show_spinner=False)
def _nasa_scale():
    from csync import scale
    return scale.reprocess_nasa()


def dot_grid(n, hits, alt, cols=25, hit_color=None, miss_color=None):
    """One dot per simulated crew: filled = counted in the result above, ring = not. Shape plus fill, so colour is never the only cue."""
    import base64
    sc = theme["fusion"]["state_on_light"]
    hit_color, miss_color = hit_color or sc["NORMAL"], miss_color or sc["UNKNOWN"]
    r, gap = 5, 15
    rows_n = -(-n // cols)
    W, H = cols * gap + 4, rows_n * gap + 4
    g = []
    for i in range(n):
        cx, cy = 2 + (i % cols) * gap + gap // 2, 2 + (i // cols) * gap + gap // 2
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{hit_color}"/>' if i < hits else
                 f'<circle cx="{cx}" cy="{cy}" r="{r - 1}" fill="none" stroke="{miss_color}" stroke-width="1.6"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + "".join(g) + "</svg>"
    return f"![{alt}](data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()})"


def scale_panel():
    """Evidence at scale: real NASA telemetry re-processed now; synthetic crews run through the shipped rule on fresh seeds."""
    from csync import scale
    st.subheader(UI["scale_title"])
    st.markdown(f"**{UI['scale_real_h']}**")
    st.markdown(UI["scale_real_intro"])
    r = _nasa_scale()
    c1, c2, c3 = st.columns(3)
    c1.metric(UI["scale_m_missions"], f"{r['missions']}")
    c2.metric(UI["scale_m_points"], f"{r['points']:,}")
    c3.metric(UI["scale_m_hours"], f"{r['hours']:,}")
    cols = {"mission": UI["scale_c_mission"], "hours": UI["scale_c_hours"], "runs": UI["scale_c_runs"], "longest": UI["scale_c_longest"],
            "above": UI["scale_c_above"], "cap": UI["scale_c_cap"]}
    rows = [{"mission": x["mission"], "hours": x["hours"], "runs": x["artifact_runs_ge_1h"], "longest": x["longest_run_h"],
             "above": x["pct_hours_above_3mmhg"], "cap": "yes" if x["sensor_zero_or_cap"] else "no"} for x in r["rows"]]
    st.markdown(md_table(cols, rows))
    st.caption(UI["scale_usable"].format(n=len(rows), s=r["seconds"]))
    st.markdown(f"**{UI['scale_chart']}**")
    st.bar_chart({x["mission"]: x["longest_run_h"] for x in r["rows"]}, color=style.chart_colors(theme)[0] if hasattr(style, "chart_colors") else None)
    st.divider()
    st.markdown(f"**{UI['scale_crews_h']}**")
    st.markdown(UI["scale_crews_intro"].format(s0=50000))
    size = st.radio(" ", [UI["scale_run_q"], UI["scale_run_l"]], horizontal=True, key="scale_size", label_visibility="collapsed")
    if st.button(UI["scale_run_btn"], key="scale_go"):
        n0, n1 = (100, 50) if size == UI["scale_run_q"] else (300, 150)
        with st.spinner("…"):
            out = scale.crews(n0, n1)
        pub = json.load(open(os.path.join(ROOT, "research", "pilot", "holdout_results.json"), encoding="utf8"))
        def line(label, k, key):
            d = out[k]
            return {"set": label, "hits": f"{d['hits']}/{d['n']}", "pct": f"{100 * d['hits'] / d['n']:.1f}",
                    "ci": f"{d['ci'][0]:.1f}–{d['ci'][1]:.1f}", "pub": f"{pub[key]['pct']}"}
        st.markdown(md_table({"set": UI["scale_c_set"], "hits": UI["scale_c_hits"], "pct": UI["scale_c_pct"], "ci": UI["scale_c_ci"], "pub": UI["scale_c_pub"]},
                             [line(UI["scale_healthy"], "control", "control (false procedure)"), line(UI["scale_drift"], "gradual", "gradual 1.5 SD")]))
        c, gr = out["control"], out["gradual"]
        st.markdown(dot_grid(c["n"], c["hits"], f"{c['hits']} of {c['n']} healthy crews triggered a procedure.", hit_color=theme["fusion"]["state_on_light"]["DEGRADED"]))
        st.markdown(dot_grid(gr["n"], gr["hits"], f"{gr['hits']} of {gr['n']} drifting crews flagged.", cols=25))
        st.caption(UI["scale_took"].format(n=n0 + n1, s=out["seconds"]))


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
        for ref in r.get("pubmed", []):
            st.caption(f"{UI['body_map_pubmed']}: {ref['cite']}. {ref['title']}. [PMID {ref['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{ref['pmid']}/)")


def habitat_panel():
    """Real NASA ISS cabin data, context only. Reads data/real/habitat_*.csv (built by scripts/build_habitat.py)."""
    with st.container(key="cs-habitat"):
        _habitat_body()


def _habitat_body():
    st.subheader(UI["habitat_title"])
    st.markdown(UI["habitat_intro"])
    df = habitat.rr1_hourly()
    flat = df[df["artifact"]]
    chart = df.set_index("hour_utc")[["co2_mmhg"]].rename(columns={"co2_mmhg": UI["habitat_series_co2"]})
    chart[UI["habitat_series_limit"]] = habitat.LIMIT_MMHG
    chart[UI["habitat_series_flat"]] = df.set_index("hour_utc")["co2_mmhg"].where(df.set_index("hour_utc")["artifact"])
    st.line_chart(chart, color=style.chart_colors(theme))
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


def version_stamp():
    """Which code and data this page shows (a stale browser tab or an old clone is visible at a glance)."""
    import subprocess, datetime
    try:
        v = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=3).stdout.strip() or "unknown"
    except Exception:
        v = "unknown"
    try:
        t = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(ROOT, "data", "out", "capsules_histoire.json")), datetime.timezone.utc).strftime("%d/%m %H:%M")
    except OSError:
        t = "unknown"
    return UI["version_label"].format(v=v, t=t)


def provenance_table():
    st.divider()
    st.subheader(UI["prov_title"])
    cols = UI["prov_cols"]
    st.dataframe([{cols[k]: row[k] for k in cols} for row in UI["prov_rows"]], hide_index=True)


# ------------------------------------------------------------------ page
st.set_page_config(page_title=strings["app_title"], layout="wide")
style.inject(UI["brand_name"], UI["brand_tag"])
st.warning(strings["synthetic_banner"])
caps, fallback = load_capsules()
if fallback:
    st.caption(UI["fallback_notice"])
day = st.slider(UI["day_slider"], 1, 10, 7)
today = [c for c in caps if c.get("day") == day]
STATES_BY_DAY = {c["day"]: c["states"] for c in caps if c.get("capsule_type", "daily") == "daily" and is_valid(c)}
_events, _link, _delay = {}, None, json.load(open(os.path.join(ROOT, "contracts", "decision.schema.json")))["properties"]["ground_delay_min"]["const"]
for c in caps:
    if c.get("capsule_type") == "emergency" and is_valid(c):
        _events[c["day"]] = UI["event_emergency"]
        q = c.get("send_queue", {})
        _delay = q.get("ground_delay_min", _delay)
        if c["day"] == day and q:
            _link = (q["link_down_utc"][11:16], q["link_up_utc"][11:16])
    elif c.get("capsule_type") == "resume" and is_valid(c) and c["action"].get("type") == "REFUSE_RESUME":
        _events[c["day"]] = UI["event_resume"]
style.mission_strip(UI, STATES_BY_DAY, _events, day, _link, _delay)
daily = next((c for c in today if c.get("capsule_type", "daily") == "daily"), None)
# warm light field = highest criticality of the day (appearance only, fusion profile)
crits = {c.get("action", {}).get("criticality") for c in today if is_valid(c)}
acting = any(c.get("action", {}).get("type") not in (None, "CONTINUE") for c in today if is_valid(c))
style.field("critical" if "CRITICAL" in crits else "watch" if acting else "calm")
# what demands action now comes first: the CRITICAL event on the dark stone surface, then the crew state
for c in today:
    if c.get("capsule_type") == "emergency" and is_valid(c) and c["ui_hint"] == "ACTION":
        with st.container(key="cs-stone"):
            action_screen(c)
    elif c.get("capsule_type") == "resume" and is_valid(c):
        with st.container(key="cs-stone"):
            resume_screen(c)
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
st.divider()
st.subheader(UI["more_title"])
_tabs = st.tabs([UI["tab_try"], UI["tab_cmd"], UI["tab_scale"], UI["tab_trends"], UI["tab_body"], UI["tab_nasa"], UI["tab_env"], UI["tab_sources"]])
with _tabs[0]:
    try_panel()
with _tabs[1]:
    commander_panel(day)
with _tabs[2]:
    scale_panel()
with _tabs[3]:
    trends_panel(day)
with _tabs[4]:
    body_map(_zone, day)
with _tabs[5]:
    hazards_panel()
    countermeasures_panel()
with _tabs[6]:
    habitat_panel()
with _tabs[7]:
    provenance_table()
    st.divider()
    st.subheader(UI["next_title"])
    st.caption(UI["next_intro"])
    st.markdown("\n".join(f"- {t}" for t in UI["next_items"]))
st.caption(version_stamp())
