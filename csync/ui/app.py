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
import altair as alt
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from csync.capsule import human_reason  # noqa: E402
from csync.gate import resume_gate  # noqa: E402
from csync import crew, devicefeed as adapters, emergency_guide, habitat, silhouette  # noqa: E402
from csync.physio import hrv  # noqa: E402
from csync.ui import body3d, bookings, bot, icons, live, style, tech_page, widgets  # noqa: E402
from csync.ui.why import short_verdict, why_parts  # noqa: E402
from csync.jsonio import read_json  # noqa: E402

CFG = os.path.join(ROOT, "csync", "config")
theme = read_json(os.path.join(CFG, "theme.json"))
strings = read_json(os.path.join(CFG, "strings_en.json"))
UI = strings["ui"]
SCHEMA = read_json(os.path.join(ROOT, "contracts", "decision_capsule.schema.json"))
OUT_DIR = os.environ.get("CSYNC_OUT_DIR", os.path.join(ROOT, "data", "out"))   # tests point it at an empty folder (cold clone)
DIMENSIONS = ["Body", "Attention", "Morale", "Mission", "Habitat"]
CONTEXT_DIMENSIONS = ("Mission",)   # Habitat is computed from real NASA data since V2 (decision P6, 18/11)


# ------------------------------------------------------------------ data
@st.cache_resource
def resolve_out_dir(preferred):
    """Folder holding the generated story files. data/out/ is generated, not committed, so a clean clone (the hosted app)
    builds them once, silently, into a temporary folder. A visitor never sees a developer message or a missing panel."""
    needed = ("capsules_histoire.json", "trends_histoire.json")
    if all(os.path.exists(os.path.join(preferred, n)) for n in needed):
        return preferred
    spec = importlib.util.spec_from_file_location("run_story", os.path.join(ROOT, "scripts", "run_story.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    built = tempfile.mkdtemp(prefix="csync_out_")
    mod.main(built)
    return built


@st.cache_data
def load_capsules(out_dir):
    with open(os.path.join(out_dir, "capsules_histoire.json"), encoding="utf8") as f:
        return json.load(f)


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
    shown = state if state in theme["state"] else "UNKNOWN"
    s = theme["state"][shown]
    if dim in CONTEXT_DIMENSIONS:
        label = UI["context_only"]
    elif dim == "Habitat":
        label = UI["habitat_card_unknown"] if state not in ("NORMAL", "WATCH", "DEGRADED") else strings["states"][state]   # says why, never a bare "unknown"
    elif day <= 5:
        shown = "UNKNOWN"
        s = theme["state"]["UNKNOWN"]
        label = strings["baseline_building"].format(n=day)
    else:
        label = strings["states"][state]
    ctx = " ctx" if dim in CONTEXT_DIMENSIONS else ""
    return (f"<div class='cs-card{ctx}' data-state='{shown}' data-dim='{dim}' style='{style.card_vars(s['color'])}'>"
            f"<div class='dim'>{dim}</div>"
            f"<div style='color:{s['color']};font-size:1.1em'>{icons.state_icon(shown)} {label}</div>{hist}</div>")


def fixed_sentence():
    st.info(strings["fixed_medical_sentence"])


# story beats (frozen story): (mission day shown, string key). None keeps the current day.
BEATS = [(3, "beat1"), (7, "beat2"), (9, "beat3"), (9, "beat4"), (10, "beat5"), (None, "beat6")]


def _go_beat(i):
    i = max(0, min(len(BEATS) - 1, i))
    st.session_state["cs-beat"] = i
    if BEATS[i][0] is not None:
        st.session_state["cs-day"] = BEATS[i][0]


def _leave_hook():
    st.session_state["cs-hook-done"] = True
    _go_beat(0)


def story_bar():
    """One idea per step: the six beats of the frozen story, advanced by a button. Presentation only."""
    if not st.session_state.get("cs-hook-done"):
        return
    i = st.session_state.get("cs-beat", 0)
    key = BEATS[i][1]
    with st.container(border=True, key="cs-beats"):
        st.caption(UI["story_step"].format(n=i + 1, total=len(BEATS)))   # plain text: the triangle glyph is reserved for the Degraded state
        st.markdown(f"**{UI[key + '_title']}** — {UI[key + '_line']}")
        st.html(bot.dialogue(UI, UI[key + "_dialogue"]))   # the demo-video dialogue: astronaut, Pip, and briefly the commander
        b, _, n = st.columns([1, 3, 1])
        b.button(UI["story_back"], key="beat-prev", disabled=i == 0, on_click=_go_beat, args=(i - 1,))
        n.button(UI["story_next"], key="beat-next", type="primary", disabled=i == len(BEATS) - 1, on_click=_go_beat, args=(i + 1,))


def _hook_timeline():
    """The clock of the frozen day-9 story, drawn from the emergency capsule (link down/up, report time, arrival on the ground).
    Nothing is typed in: if the capsule is missing the drawing is simply not shown."""
    cap = next((c for c in load_capsules(resolve_out_dir(OUT_DIR)) if c.get("capsule_type") == "emergency" and is_valid(c)), None)
    q = (cap or {}).get("send_queue") or {}
    try:
        t = {k: datetime.fromisoformat(q[k]) for k in ("link_down_utc", "link_up_utc", "report_received_utc")}
        t["report"] = datetime.strptime(q["link_down_utc"][:10] + " " + cap["time_utc"], "%Y-%m-%d %H:%M")
        t0, t1 = t["link_down_utc"], t["report_received_utc"]
        span = (t1 - t0).total_seconds()
        pos = {k: 100 * (v - t0).total_seconds() / span for k, v in t.items()}
        gap = int((t["report_received_utc"] - t["report"]).total_seconds() // 60)
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return
    hm = lambda d: d.strftime("%H:%M")
    st.markdown(
        "<div class='cs-hooktl' role='img' aria-label='" + html.escape(UI["hook_tl_gap"].format(h=gap // 60, m=gap % 60)) + "'>"
        f"<div class='bar'><div class='out' style='width:{pos['link_up_utc']:.1f}%'></div>"
        f"<i style='left:{pos['report']:.1f}%'></i><i style='left:100%'></i></div>"
        f"<div class='lab' style='left:0'>{hm(t['link_down_utc'])}<br>{UI['hook_tl_outage']}</div>"
        f"<div class='lab mid' style='left:{pos['report']:.1f}%'>{hm(t['report'])}<br>{UI['hook_tl_report']}</div>"
        f"<div class='lab end'>{hm(t['report_received_utc'])}<br>{UI['hook_tl_ground']}</div>"
        "</div>"
        f"<p class='cs-hooktl-gap'><b>{UI['hook_tl_gap'].format(h=gap // 60, m=gap % 60)}</b></p>",
        unsafe_allow_html=True)


def hook_screen():
    """Opening problem from the frozen story (day 9, 14:10 UTC), shown once above the overall state. Presentation only."""
    if st.session_state.get("cs-hook-done"):
        return
    with st.container(border=True, key="cs-hook"):
        st.markdown(f"<div class='cs-kicker'>{UI['hook_kicker']}</div>", unsafe_allow_html=True)
        st.subheader(UI["hook_title"])
        st.markdown(UI["hook_text"])
        _hook_timeline()
        st.button(UI["hook_button"], key="hook-go", type="primary", on_click=_leave_hook)


def decision_buttons(cap, day):
    """A human accepts or declines a proposed procedure. Recorded for this browser session only; nothing else changes."""
    act = cap.get("action", {})
    if act.get("type") != "OPEN_PROCEDURE":
        st.caption(strings["human_decision_pending"])
        return
    key = f"decision_{act['procedure_id']}_{day}"
    choice = st.session_state.get(key)
    if choice is None:
        st.caption(strings["human_decision_pending"])
        a, d, _ = st.columns([1, 1, 3])
        if a.button(UI["btn_accept"], key=f"acc_{key}", type="primary"):
            st.session_state[key] = "accepted"
            st.rerun()
        if d.button(UI["btn_decline"], key=f"dec_{key}"):
            st.session_state[key] = "declined"
            st.rerun()
    if choice:
        st.success(UI["decision_" + choice].format(pid=act["procedure_id"], day=day))
        st.caption(UI["decision_session_note"])


def action_block(cap, day):
    """Why this view, the proposed action and the human decision buttons."""
    with st.container(border=True):
        parts = why_parts(cap, UI)
        st.markdown(f"**{UI['why_label']}**")
        for line in parts["lines"]:
            st.markdown(line)
        with st.expander(UI["why_rule_label"]):
            if parts["rule"]:
                st.markdown(parts["rule"])
            if cap.get("situation") and cap["situation"] != short_verdict(cap, strings["states"]):
                st.markdown(cap["situation"])
        st.markdown(f"<div class='cs-action'><b>{UI['action_label']}</b> — {html.escape(str(cap['action'].get('text', '')))}</div>",
                    unsafe_allow_html=True)
        decision_buttons(cap, day)


def rhythm_panel(day):
    """Simulated heart-rhythm variability tied to the story through the capsule's distances. Context only: no state, no procedure."""
    def dist(d):
        c = DAILY_BY_DAY.get(d)
        ds = [s["d"] for s in (c or {}).get("signals", []) if s.get("d") is not None]
        return max([0.0] + ds)
    rows = [hrv.story_rhythm(d, dist(d)) for d in range(1, day + 1)]
    base_days = [hrv.story_rhythm(d, dist(d))["rmssd"] for d in range(1, min(day, 5) + 1)]
    base = sum(base_days) / len(base_days)
    with st.container(border=True):
        st.markdown(f"**{UI['rhythm_title']}**")
        st.write(UI["rhythm_now"].format(v=f"{rows[-1]['rmssd']:.0f}", b=f"{base:.0f}"))
        st.caption(UI["rhythm_legend"])
        st.markdown(widgets.curve_image([{"day": r["day"], "value": r["rmssd"], "flagged": False} for r in rows], base, None,
                                        UI["rhythm_curve"], theme["navy"]["chart"], "Mission day"))
        st.caption(UI["rhythm_note"])


def nominal(cap, day):
    cmd = st.session_state.get("cs-role") == UI["role_cmd"]   # two entries, one capsule: only the order differs
    st.subheader(short_verdict(cap, strings["states"]))
    if cmd:
        cmd_summary_line(day)
        action_block(cap, day)
    else:
        st.caption(UI["crew_own"])
    cols = st.columns(len(DIMENSIONS))
    for col, dim in zip(cols, DIMENSIONS, strict=True):
        col.markdown(card(dim, cap["states"].get(dim, "UNKNOWN"), day, style.history(STATES_BY_DAY, dim, day)), unsafe_allow_html=True)
    sig = widgets.pick_signal(cap, day)
    trend = read_json(os.path.join(OUT, "trends_histoire.json"))["indicators"].get(sig["indicator_id"]) if sig else None
    rows = [r for r in trend["days"] if r["day"] <= day] if trend else []
    if rows and rows[-1]["day"] == day and rows[-1]["value"] is not None:   # no card when the history does not reach the shown day
        left, right = st.columns([1, 1.3])
        left.markdown(widgets.indicator_card(sig, cap["states"][sig["dimension"]], rows, trend["threshold"], day, UI, strings["states"],
                                             theme["navy"]["chart"]), unsafe_allow_html=True)
        with right.container(border=True):
            st.markdown(f"**{sig['name']}** ({sig['unit']})")
            st.caption(UI["ind_curve_legend"])
            st.markdown(widgets.curve_image(rows, sig["baseline_mean"], trend["threshold"], sig["name"], theme["navy"]["chart"], "Mission day"))
    rhythm_panel(day)
    if not cmd:
        action_block(cap, day)
    with st.expander(UI["signals_label"]):
        st.dataframe([{k: s.get(k) for k in ("indicator_id", "name", "value", "unit", "baseline_mean", "d", "flagged")}
                      for s in cap["signals"]], hide_index=True)
        st.caption(f"{UI['evidence_label']}: {cap['evidence']}")


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
    if "resume_result" not in st.session_state and st.session_state.get("cs-beat") == 4:
        # guided story, step 5: the visitor sees the gate answer without having to press the button (same gate, same inputs)
        st.session_state["resume_result"] = resume_gate(req, meas, gate_proc)
    c1, c2 = st.columns(2)
    if c1.button(UI["request_resume"], key="request_resume"):
        st.session_state["resume_result"] = resume_gate(req, meas, gate_proc)
    if c2.button(UI["commander_override"], key="override"):
        d, reasons = resume_gate(req, meas, gate_proc, override={"by": "Commander"})
        st.session_state["resume_result"] = (d, reasons)
        st.session_state["resume_log"].append(UI["override_logged"].format(t=gi["request_time_utc"][11:16], d=plain(d)))
    if "resume_result" in st.session_state:
        d, reasons = st.session_state["resume_result"]
        colour = theme["state"]["DEGRADED" if d == "REFUSE_RESUME" else "NORMAL"]["color"]
        st.markdown(f"<div class='cs-decision' style='color:{colour};{style.card_vars(colour)}'>{UI['decision']}: {plain(d)}</div>",
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


def trend_svg(rows, base, thr, label):
    """Trend curve as an SVG Markdown image with alt text (Vega marks carry no alt, axe svg-img-alt). Drawing code: csync/ui/widgets.py."""
    return widgets.curve_image(rows, base, thr, label, theme["navy"]["chart"], "Mission day")


def trends_panel(day):
    """Dynamic chart per indicator up to the chosen day, against the personal baseline (reads data/out/trends_histoire.json)."""
    path = os.path.join(OUT, "trends_histoire.json")
    data = read_json(path)["indicators"]
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
    if rows:   # what the chart shows, in one computed sentence (V3: a chart is read, not only drawn)
        last = rows[-1]
        st.markdown(UI["trend_read"].format(day=last["day"], name=names[ind], v=last["value"], unit=t["unit"],
                                            d=last["value"] - t["baseline_mean"], base=t["baseline_mean"], thr=t["threshold"]))
    st.markdown(trend_svg(rows, t["baseline_mean"], t["threshold"], f"{names[ind]} ({t['unit']})"),
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


def why_panel():
    """Why a personal baseline, and what happens when that baseline is wrong. Numbers are read from the committed research results."""
    base = os.path.join(ROOT, "research")
    fp = read_json(os.path.join(base, "fixed_vs_personal_results.json"))
    hy = read_json(os.path.join(base, "hybrid_baseline_results.json"))
    cell = lambda r, kind, key: f"{r['drift'][key]['pct']:.1f} % / {r['healthy'][key]['pct']:.1f} %"
    rows = [{"f": UI["why_spread"][int(f[2])], "p": cell(fp[f], 0, "B_personal_2ind"), "c": cell(fp[f], 0, "C_fixed"), "d": cell(fp[f], 0, "D_fixed_sleep_only")}
            for f in ("f=0", "f=1", "f=2", "f=3")]
    st.subheader(UI["why_title"])
    st.markdown(UI["why_intro"])
    st.markdown(md_table(UI["why_cols"], rows))
    st.caption(UI["why_limits"])
    st.subheader(UI["ref_title"])
    st.markdown(UI["ref_intro"])
    cell2 = lambda r, k: f"{r[k]['detect']['pct']:.1f} % / {r[k]['false_alarm']['pct']:.1f} %"
    rows2 = [{"b": UI["ref_bias"][b], "s": cell2(hy[f"adapt=0.0,bias={b}"], "shipped"), "h": cell2(hy[f"adapt=0.0,bias={b}"], "H(g=1.0)")} for b in ("0.0", "0.5", "1.0", "1.5")]
    st.markdown(md_table(UI["ref_cols"], rows2))
    a5, a1 = hy["adapt=0.5,bias=0.0"]["H(g=1.0)"]["false_alarm"]["pct"], hy["adapt=1.0,bias=0.0"]["H(g=1.0)"]["false_alarm"]["pct"]
    st.caption(UI["ref_cost"].format(a5=f"{a5:.1f}", a1=f"{a1:.1f}"))
    st.caption(UI["why_synth"])


@st.cache_data
def _crew_board(day: int):
    return crew.board(day)


def state_glyphs(b, labels):
    """One orbit glyph per crew member, ordered by urgency; same shape code as the state cards and the deck (csync/glyphs.py):
    circle normal, diamond watch, triangle degraded or procedure open, dashed square unknown. Colour only reinforces the shape."""
    import base64
    from csync import glyphs
    nv = theme["navy"]
    sc = {"NORMAL": nv["normal"], "WATCH": nv["watch"], "DEGRADED": nv["degraded"], "UNKNOWN": nv["unknown"]}   # dark panel: light state colours
    ink = nv["cream"]
    step, g, alt = 92, [], []
    for i, r in enumerate(b.itertuples()):
        x = 6 + i * step
        key = "DEGRADED" if r.action == "OPEN_PROCEDURE" else r.action
        g.append(f"<svg x='{x}' y='0' width='60' height='57' viewBox='-1 0 35 33'>{glyphs.orbit_inner(r.action, sc[key])}</svg>")
        g.append(f"<text x='{x + 30}' y='74' text-anchor='middle' font-size='15' font-weight='700' font-family='sans-serif' fill='{ink}'>{str(r.member)[-1]}</text>")
        alt.append(f"{r.member}: {labels[r.action]}")
    W = 12 + len(b) * step
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} 82' width='{W}' height='82'>" + "".join(g) + "</svg>"
    return f"![{'; '.join(alt)}](data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()})"


def cmd_summary_line(day):
    b = _crew_board(day)
    n = lambda k: int((b.action == k).sum())
    st.markdown(f"**{UI['cmd_summary'].format(day=day, n_open=n('OPEN_PROCEDURE'), n_deg=n('DEGRADED'), n_watch=n('WATCH'), n_unk=n('UNKNOWN'))}**")


def commander_panel(day):
    """Crew-level view for the commander: the same rule on six synthetic members, sorted by urgency. Decides nothing."""
    st.subheader(UI["cmd_title"])
    st.markdown(UI["cmd_intro"])
    b = _crew_board(day)
    cmd_summary_line(day)
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
        return {i: (None if pd.isna(v) else float(v)) for i, v in zip(live.INDICATORS, edited[c], strict=True)}
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
    for c, dim in zip(cols, ("Body", "Attention", "Morale"), strict=True):
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
        pub = read_json(os.path.join(ROOT, "research", "pilot", "holdout_results.json"))
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
                      default=preset or "region-chest", key=f"body_zone_{day}")   # never an empty panel on arrival
    left, right = st.columns([3, 2])
    with left:   # V3: 3D mannequin built in code (three.js in the browser); the flat map is its fallback inside the frame
        cap = UI["body3d_cap"].format(zone=labels[choice] if choice else "none")
        page = body3d.viewer_html(choice, cap, UI["body3d_hint"])
        if hasattr(st, "iframe"):
            st.iframe(page, height=body3d.HEIGHT)
        else:
            st.markdown(silhouette.markdown_image(choice, UI["body_map_alt"].format(zone=labels[choice] if choice else "none")))
    if not choice:
        right.markdown(UI["body3d_pick"])
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
    """Real NASA ISS cabin data (the Habitat state is computed from it, see csync/habitat.py). Reads data/real/habitat_*.csv (built by scripts/build_habitat.py)."""
    with st.container(key="cs-habitat"):
        _habitat_body()


def habitat_week():
    """Hero card in the reference style: real ISS cabin CO2 per day, one week at a time, day pills and week arrows."""
    days = habitat.daily_means()
    weeks = [days.iloc[i:i + 7] for i in range(0, len(days) - 6, 7)]
    weeks = [w for w in weeks if w.notna().sum() >= 2]
    assert weeks, "no week with two valid days"
    wi = max(0, min(int(st.session_state.get("cs-week", len(weeks) // 2)), len(weeks) - 1))
    w = weeks[wi]
    vals = [None if v != v else round(float(v), 2) for v in w.tolist()]   # NaN -> None: a missing day is never drawn as 0
    with st.container(key="cs-weekcard"):
        st.html(f"<div class='cs-wk-h'><div><b>{UI['week_title']}</b><span>{UI['week_sub']}</span></div></div>")
        letters = [d.strftime("%a")[0] for d in w.index]
        curve = st.empty()   # the curve is drawn above the day pills, as on the reference, but needs the pill choice first
        sel = st.pills(UI["week_pick"], list(range(7)), format_func=lambda i: letters[i], selection_mode="single",
                       default=max(i for i, v in enumerate(vals) if v is not None), key=f"cs-wday-{wi}", label_visibility="collapsed")
        sel = sel if sel is not None else 0
        alt = UI["week_alt"].format(a=w.index[0].strftime("%d %b"), b=w.index[-1].strftime("%d %b"))
        curve.html(widgets.week_curve_image(vals, sel, habitat.LIMIT_MMHG, alt))
        v = vals[sel]
        st.html(f"<div class='cs-wk-v'><span class='cs-num'>{'--' if v is None else f'{v:.2f}'}</span><small>mmHg · "
                f"{w.index[sel].strftime('%a %d %b %Y')}</small></div><p class='cs-wk-n'>{UI['week_note']}</p>")
        b1, mid, b2 = st.columns([1, 3, 1])
        if b1.button("‹", key="cs-week-prev", disabled=wi == 0, help=UI["week_prev"]):
            st.session_state["cs-week"] = wi - 1
            st.rerun()
        mid.html(f"<p class='cs-wk-r'>{w.index[0].strftime('%b %d')} – {w.index[-1].strftime('%b %d, %Y')}</p>")
        if b2.button("›", key="cs-week-next", disabled=wi == len(weeks) - 1, help=UI["week_next"]):
            st.session_state["cs-week"] = wi + 1
            st.rerun()


def _habitat_body():
    st.subheader(UI["habitat_title"])
    habitat_week()
    st.markdown(UI["habitat_intro"])
    df = habitat.rr1_hourly()
    flat = df[df["artifact"]]
    sm = habitat.summary(df)
    st.markdown(UI["habitat_read"].format(**sm))   # what the chart shows, in one sentence, computed from the data
    chart = df.set_index("hour_utc")[["co2_mmhg"]].rename(columns={"co2_mmhg": UI["habitat_series_co2"]})
    chart[UI["habitat_series_limit"]] = habitat.LIMIT_MMHG
    chart[UI["habitat_series_flat"]] = df.set_index("hour_utc")["co2_mmhg"].where(df.set_index("hour_utc")["artifact"])
    cols = list(chart.columns)
    long = chart.reset_index().melt("hour_utc", var_name="series", value_name="mmHg").dropna()
    st.altair_chart(alt.Chart(long).mark_line().encode(
        x=alt.X("hour_utc:T", title=None), y=alt.Y("mmHg:Q", title=None),
        color=alt.Color("series:N", sort=cols, scale=alt.Scale(domain=cols, range=style.chart_colors(theme)),
                        legend=alt.Legend(orient="bottom", direction="vertical", columns=1, title=None, labelLimit=0))), width="stretch")   # one legend row per series: nothing is cut on a phone
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
    replay_panel()
    with st.expander(UI["habitat_table_title"]):
        st.dataframe(m[list(UI["habitat_columns"])].rename(columns=UI["habitat_columns"]), hide_index=True)
        st.caption(UI["habitat_table_note"].format(n=len(m), k=int((m["artifact_runs_ge_1h"] > 0).sum())))
    st.caption(UI["habitat_credit"])


def replay_panel():
    """Mission replay: pick one real ISS mission, see what the frozen rule would have flagged (pre-registered, research/retro)."""
    r = habitat.replay()
    st.subheader(UI["replay_title"])
    st.caption(UI["replay_intro"])
    pick = st.selectbox(UI["replay_pick"], list(r["mission"]), index=int((r["mission"] == "RR-28").idxmax()), key="cs-replay")
    row = r.set_index("mission").loc[pick]
    c1, c2, c3 = st.columns(3)
    c1.metric(UI["replay_hidden"], int(row["hours_hidden_by_daily_mean"]))
    c2.metric(UI["replay_episodes"], int(row["episodes"]))
    c3.metric(UI["replay_7d"], f"{row['pct_days_7d_above_2.5']:.0f} %")
    st.caption(UI["replay_note"])


def emergency_panel():
    """Several kinds of emergency, steps in order with a NASA source each (csync/emergency_guide.py). Presentation only."""
    g = emergency_guide.load()
    st.subheader(UI["em_title"])
    st.markdown(UI["em_intro"])
    cases = {c["id"]: c for c in g["cases"]}
    cid = st.pills(UI["em_pick"], list(cases), format_func=lambda k: cases[k]["title"], selection_mode="single", default="medical", key="cs-em-case")
    c = cases[cid or "medical"]
    a, b, d = st.columns(3)
    a.markdown(f"**{UI['em_trigger']}**  \n{c['trigger']}")
    b.markdown(f"**{UI['em_role']}**  \n{c['csync_role']}")
    d.markdown(f"**{UI['em_never']}**  \n{c['never']}")
    key = f"cs-em-step-{c['id']}"
    i = max(0, min(int(st.session_state.get(key, 0)), len(c["steps"]) - 1))
    s = c["steps"][i]
    with st.container(key="cs-em-step"):
        st.caption(UI["em_step"].format(i=i + 1, n=len(c["steps"])))
        st.html("<div class='cs-dots'>" + "".join(f"<span class='cs-dot{' on' if k == i else ''}'>{k + 1}</span>"
                                                   for k in range(len(c["steps"]))) + "</div>")
        st.markdown(f"### {s['text']}")
        st.caption(f"{UI['em_src']}: {g['sources'][s['src']]}")
        p1, _, p2 = st.columns([1, 2, 1])
        if p1.button(UI["em_back"], key=f"{key}-b", disabled=i == 0):
            st.session_state[key] = i - 1
            st.rerun()
        if p2.button(UI["em_next"], key=f"{key}-n", type="primary", disabled=i == len(c["steps"]) - 1):
            st.session_state[key] = i + 1
            st.rerun()
        if i == len(c["steps"]) - 1:
            st.success(UI["em_done"])
    if c["id"] in ("depress", "fire", "toxic"):
        st.markdown(f"**{UI['em_headcount']}**")
        cols = st.columns(len(UI["em_crew"]))
        k = sum(1 for n, col in zip(UI["em_crew"], cols, strict=True) if col.checkbox(n, key=f"cs-em-hc-{c['id']}-{n}"))
        st.caption(UI["em_counted"].format(k=k, n=len(UI["em_crew"])))
    if c["id"] == "depress":
        st.markdown(f"**{UI['em_tres_title']}**")
        x1, x2 = st.columns(2)
        pb = x1.number_input(UI["em_p_before"], 400.0, 800.0, 752.0, 0.5, key="cs-em-pb")
        pn = x2.number_input(UI["em_p_now"], 400.0, 800.0, 748.0, 0.5, key="cs-em-pn")
        t = emergency_guide.time_to_reserve(pb, pn, 1.0)
        if t is None:
            st.info(UI["em_tres_none"])
        else:
            st.html(f"<div class='cs-wk-v'><span class='cs-num'>{t:.0f}</span><small>min</small></div>")
            st.markdown(UI["em_tres_out"].format(m=t))
            if t <= emergency_guide.STOP_ISOLATING_MIN:
                st.warning(UI["em_tres_stop"])
        st.caption(UI["em_tres_note"])
    st.info(strings["fixed_medical_sentence"])


def sources_panel():
    provenance_table()
    st.divider()
    st.subheader(UI["next_title"])
    st.caption(UI["next_intro"])
    st.markdown("\n".join(f"- {t}" for t in UI["next_items"]))


def version_stamp():
    """Which code and data this page shows (a stale browser tab or an old clone is visible at a glance)."""
    import subprocess, datetime
    try:
        v = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=3,
                           check=False).stdout.strip() or "unknown"
    except (OSError, subprocess.SubprocessError):   # no git on the host: the stamp says unknown, the page still renders
        v = "unknown"
    try:
        t = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(OUT, "capsules_histoire.json")), datetime.timezone.utc).strftime("%d/%m %H:%M")
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
# Novice audit (20/11): engine codes reached the visitor ("REFUSE_RESUME", "WATCH", "Rule v3", "d >= 1.5"). The words below are
# the same facts in plain language; HTML blocks (cards) keep their own wording. The capsules and the rule are unchanged.
_PLAIN = [(re.compile(r"\bREFUSE_RESUME\b"), "resume refused"), (re.compile(r"\bOPEN_PROCEDURE\b"), "procedure open"),
          (re.compile(r"\bRule v3\b"), "The C-Sync rule"), (re.compile(r"\b[Rr]ule v3\b"), "the C-Sync rule"),
          (re.compile(r"\bWATCH\b"), "Watch"), (re.compile(r"\bDEGRADED\b"), "Degraded"), (re.compile(r"\bUNKNOWN\b"), "No reading yet"),
          (re.compile(r"\bNORMAL\b"), "Normal"), (re.compile(r"\bd ≥ 1\.5\b"), "at least 1.5 times the usual spread")]


def intro_screen():
    """Transition on arrival: three lines appear one after the other, then one button. Still under reduced motion."""
    lines = "".join(f"<p class='cs-intro-l' style='animation-delay:{0.2 + 1.6 * i:.1f}s'>{html.escape(UI[f'intro_{i + 1}'])}</p>" for i in range(3))
    st.html("<style>.cs-intro{max-width:760px;margin:12vh auto 28px;text-align:left}"
            ".cs-intro-l{font-size:clamp(1.3rem,3.2vw,2.1rem);line-height:1.3;font-weight:600;margin:0 0 .9em;opacity:0;"
            "animation:cs-in .9s ease forwards}.cs-intro-l:last-child{color:var(--cs-accent,currentColor)}"
            "@keyframes cs-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
            "@media (prefers-reduced-motion:reduce){.cs-intro-l{animation:none;opacity:1}}</style>"
            f"<div class='cs-intro'>{lines}</div>")
    if st.button(UI["intro_go"], key="cs-intro-go", type="primary"):
        st.session_state["cs-intro-done"] = True
        st.rerun()
    st.caption(UI["intro_src"])


def tech_standalone():
    """Technologies without the demo day bar: the cards that need a capsule read the demo story's day 9 (the drift day)."""
    out = resolve_out_dir(OUT_DIR)   # the hosted app has no data/out: the story files are built on first use (20/11 crash)
    caps = load_capsules(out)
    daily = next((c for c in caps if c.get("capsule_type", "daily") == "daily" and c.get("day") == 9 and is_valid(c)), None)
    tech_page.tech_panel(UI, daily, read_json(os.path.join(out, "trends_histoire.json")), 10, caps)


def nav_groups(commander: bool) -> list[tuple[str, list[str]]]:
    """Navigation by the visitor's path. Pure function (tested): the commander board exists only in the commander's list."""
    if commander:
        return [("nav_g_now", ["tab_live", "tab_cmd"]), ("nav_g_tour", ["tab_home", "tab_emergency", "tab_body", "tab_tech"]),
                ("nav_g_proof", ["tab_env", "tab_trends", "tab_why", "tab_scale", "tab_nasa", "tab_try", "tab_sources"])]
    return [("nav_g_now", ["tab_live"]), ("nav_g_tour", ["tab_home", "tab_trends", "tab_emergency", "tab_body", "tab_tech"]),
            ("nav_g_proof", ["tab_env", "tab_why", "tab_scale", "tab_nasa", "tab_try", "tab_sources"])]


def plain(text):
    """Same fact, visitor's words. Raw HTML is left alone."""
    if not isinstance(text, str) or text.lstrip().startswith("<"):
        return text
    for rx, word in _PLAIN:
        text = rx.sub(word, text)
    return text


for _name in ("markdown", "caption", "info", "warning", "success", "write", "text"):
    _orig = getattr(st, _name)
    setattr(st, _name, (lambda f: (lambda body, *a, **k: f(plain(body), *a, **k)))(_orig))
style.inject(UI["brand_name"], UI["brand_tag"])
# vertical navigation: one section = one visitor question; the global state of the crew is first
# V3 (Joseph, 20/11, final pass): the role is chosen first ("who are you?") and decides what the navigation offers.
# The commander board is the commander's: a crew member never sees it in the navigation (one capsule, one rule, two entries).
# Sections are grouped by the visitor's path: Now (live), Tour (what C-Sync does), Proof (where it comes from).
role = st.sidebar.radio(UI["role_label"], [UI["role_crew"], UI["role_cmd"]], key="cs-role", horizontal=True)
st.sidebar.caption(UI["role_cmd_note"] if role == UI["role_cmd"] else UI["role_crew_note"])
NAV_GROUPS = nav_groups(role == UI["role_cmd"])
_KEYS = [k for _g, keys in NAV_GROUPS for k in keys]
_SECTIONS = [UI[k] for k in _KEYS]
if st.session_state.get("cs-nav") is not None and st.session_state["cs-nav"] not in _SECTIONS:
    st.session_state["cs-nav"] = _SECTIONS[0]   # a crew member who was on the commander board goes back to the live station
_starts = {}
_i = 1
for _g, _keys in NAV_GROUPS:
    _starts[_i] = UI[_g]
    _i += len(_keys)
st.html("<style>" + bookings.nav_css(UI, _KEYS, ["role_crew", "role_cmd"], _starts) + "</style>")
section = st.sidebar.radio(UI["nav_label"], _SECTIONS, key="cs-nav")
_SECTION_KEY = dict(zip(_SECTIONS, _KEYS, strict=True))[section]
if section != UI["tab_live"] or st.session_state.get("cs-bot-done"):   # on a first visit the tutorial speaks; Pip's corner comes after
    bot.dock(UI, _SECTION_KEY, _KEYS)
OUT = resolve_out_dir(OUT_DIR)
if section == UI["tab_live"] and not st.session_state.get("cs-intro-done"):
    intro_screen()   # first visit: one true story, then the station (Joseph 20/11; the popular NASA "quote" is a myth, see intro_src)
    st.stop()
if section == UI["tab_live"]:
    live.panel(UI)   # real NASA station data, live, context only; the guide bot opens here on a first visit
    st.caption(version_stamp())
    st.stop()
# V3 retrospective (20/11): the demo day slider and the Mars transit strip belong to the drift story only. On the body map, the
# real NASA habitat data, the evidence, the hazards and the sources they mixed a simulated day with unrelated facts
# (design rule "one screen, one moment"), so those sections open without them.
_USE_KEYS = {UI[k]: "use_" + {"tab_cmd": "cmd", "tab_body": "body", "tab_env": "env", "tab_trends": "trends", "tab_tech": "tech",
             "tab_scale": "scale", "tab_why": "why", "tab_nasa": "nasa", "tab_try": "try", "tab_sources": "sources", "tab_emergency": "emergency"}[k]
             for k in ("tab_cmd", "tab_body", "tab_env", "tab_trends", "tab_tech", "tab_scale", "tab_why", "tab_nasa", "tab_try", "tab_sources",
                       "tab_emergency")}
_STORY_SECTIONS = (UI["tab_home"], UI["tab_cmd"], UI["tab_trends"])   # 20/11: Technologies no longer carries the demo day bar
if section not in _STORY_SECTIONS:
    _STANDALONE = {UI["tab_body"]: lambda: body_map(None, None), UI["tab_env"]: habitat_panel, UI["tab_scale"]: scale_panel,
                   UI["tab_why"]: why_panel, UI["tab_nasa"]: lambda: (hazards_panel(), countermeasures_panel()),
                   UI["tab_try"]: try_panel, UI["tab_sources"]: sources_panel, UI["tab_emergency"]: emergency_panel,
                   UI["tab_tech"]: tech_standalone}
    st.caption(UI[_USE_KEYS[section]])
    _STANDALONE[section]()
    st.caption(version_stamp())
    st.stop()
if section == UI["tab_home"]:
    hook_screen()   # the opening problem comes first, above the controls
st.warning(strings["synthetic_banner"])
if not st.session_state.get("cs-hook-done") and section == UI["tab_home"]:
    st.stop()   # first screen = the problem, one button, the synthetic notice; the day-7 panel would contradict the day-9 hook
caps = load_capsules(OUT)
day = st.slider(UI["day_slider"], 1, 10, 7, key="cs-day")
today = [c for c in caps if c.get("day") == day]
DAILY_BY_DAY = {c["day"]: c for c in caps if c.get("capsule_type", "daily") == "daily" and is_valid(c)}
STATES_BY_DAY = {d: c["states"] for d, c in DAILY_BY_DAY.items()}
_events, _link, _delay = {}, None, read_json(os.path.join(ROOT, "contracts", "decision.schema.json"))["properties"]["ground_delay_min"]["const"]
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
_USE = {UI["tab_cmd"]: "use_cmd", UI["tab_body"]: "use_body", UI["tab_env"]: "use_env", UI["tab_trends"]: "use_trends", UI["tab_tech"]: "use_tech", UI["tab_scale"]: "use_scale",
        UI["tab_why"]: "use_why", UI["tab_nasa"]: "use_nasa", UI["tab_try"]: "use_try", UI["tab_sources"]: "use_sources"}
if section in _USE:
    st.caption(UI[_USE[section]])
if section == UI["tab_home"]:
    story_bar()
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
elif section == UI["tab_cmd"]:
    commander_panel(day)
else:   # only the three story sections reach this point (the others are standalone above)
    assert section == UI["tab_trends"], section
    trends_panel(day)
st.caption(version_stamp())
