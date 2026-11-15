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
import sys
import tempfile
from datetime import datetime

import jsonschema
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from csync.capsule import human_reason  # noqa: E402
from csync.gate import resume_gate  # noqa: E402
from csync import habitat  # noqa: E402
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
            for line in st.session_state["resume_log"]:
                st.text(line)
    if st.session_state["resume_log"]:
        st.markdown(f"**{UI['log_title']}**")
        for line in st.session_state["resume_log"]:
            st.text(line)
    fixed_sentence()
    st.caption(strings["human_decision_pending"])


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
    st.markdown(f"**{UI['habitat_table_title']}**")
    st.dataframe(m[list(UI["habitat_columns"])].rename(columns=UI["habitat_columns"]), hide_index=True)
    st.caption(UI["habitat_table_note"].format(n=len(m), k=int((m["artifact_runs_ge_1h"] > 0).sum())))
    st.caption(UI["habitat_credit"])


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
habitat_panel()
