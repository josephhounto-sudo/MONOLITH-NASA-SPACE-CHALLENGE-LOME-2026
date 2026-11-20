"""Technologies page: one card per registry item. A card shows a live demo only when the registry says the module exists."""
from __future__ import annotations

import copy

import streamlit as st

from csync.analytics.changepoint import bocpd, cusum
from csync.crypto.capsule_sign import generate_keypair, sign_capsule, verify_capsule
from csync.physio.hrv import clean_rr, rmssd, sdnn, simulated_rr
from csync.sync.crdt_sim import Replica, simulate_link
from csync.proto import common_signal, dtn, explainer, exposure_ledger
from csync.ui import camera_lab
from csync.tech import registry

_ANIM = """<style>
.cs-dtn{position:relative;height:34px;margin:6px 0 10px;border-radius:17px;background:rgba(0,0,0,.35);border:1px solid rgba(244,237,224,.25);overflow:hidden}
.cs-dtn i{position:absolute;top:12px;width:10px;height:10px;border-radius:50%;background:#FF6B5B;left:6px;animation:cs-hop 6s linear infinite}
.cs-dtn i:nth-child(2){animation-delay:2s;background:#F4EDE0}.cs-dtn i:nth-child(3){animation-delay:4s}
.cs-dtn b{position:absolute;top:4px;font-size:.78rem;color:#F4EDE0;font-weight:500}
@keyframes cs-hop{0%{left:6px;opacity:1}40%{left:46%;opacity:1}60%{left:46%;opacity:.4}100%{left:calc(100% - 18px);opacity:1}}
@media (prefers-reduced-motion:reduce){.cs-dtn i{animation:none}}
</style>"""


def _strip(n, marks, off=None):
    """A row of numbered dots (days or steps): the technology shows its effect as a picture, not as prose.
    marks: {index: (css colour, word)}; off: (start, end) range drawn as a cut link."""
    assert 1 <= n <= 40
    cells = []
    for i in range(1, n + 1):
        colour, word = marks.get(i, (None, ""))
        cut = off and off[0] <= i < off[1]
        style = (f"background:{colour};color:#2E2621" if colour else "background:rgba(255,253,253,.06)") + (";opacity:.45;border-style:dashed" if cut else "")
        cells.append(f"<span class='cs-dot' style='{style}' title='{word}'>{i}</span>")
    return "<div class='cs-dots'>" + "".join(cells) + "</div>"


_DOTS = """<style>.cs-dots{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 6px}
.cs-dot{min-width:30px;height:30px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font-family:Doto,monospace;font-weight:700;
 font-size:14px;border:1px solid rgba(255,253,253,.28);color:#FFFDFD}</style>"""


def _banner(UI, item, reg):
    st.markdown(f"**{item['name']}** · {registry.label(reg, item)}")
    st.caption(item["purpose"])
    word = {"NONE": UI["tech_data_none"], "ON_DEVICE": UI["tech_data_device"]}.get(item["data"], item["data"])
    st.caption(UI["tech_data"].format(d=word))


def _changepoint(UI, trends, sig, day):
    t = trends["indicators"].get("CO01")
    rows = [r for r in t["days"] if r["day"] <= day and r["value"] is not None] if t else []
    sd = (sig or {}).get("baseline_sd_used")
    if not rows or not sd:
        st.caption(UI["tech_cp_missing"])
        return
    vals = [r["value"] for r in rows]
    fixed = next((r["day"] for r in rows if r["value"] > t["threshold"]), None)
    res = cusum(vals, t["baseline_mean"], sd)
    marks = {}
    if fixed:
        marks[fixed] = ("#F2C14E", UI["tech_cp_mark_fixed"])
    if res["alarm_index"] is not None:
        marks[rows[res["alarm_index"]]["day"]] = ("#E9A27A", UI["tech_cp_mark_cusum"])
    st.html(_DOTS + _strip(len(rows), marks))
    st.write(UI["tech_cp_fixed"].format(d=fixed) if fixed else UI["tech_cp_none"].format(d=day))
    st.write(UI["tech_cp_cusum"].format(d=rows[res["alarm_index"]]["day"]) if res["alarm_index"] is not None else UI["tech_cp_cusum_none"])
    if len(vals) >= 3:
        z = [(v - t["baseline_mean"]) / sd for v in vals]
        idx = bocpd(z)["most_likely_index"]
        if idx is not None:
            st.write(UI["tech_cp_bocpd"].format(d=rows[idx]["day"]))
    st.caption(UI["tech_cp_note"])
    _changepoint_try(UI)


def _changepoint_try(UI):
    import numpy as np
    from csync.rules import Params
    k = Params().d_threshold
    slope = st.slider(UI["tech_cp_try"], 0.0, 12.0, 4.0, 1.0, key="tech_cp_slope")
    rng = np.random.default_rng(11)
    mean, sd = 265.0, 13.0
    vals = [mean + rng.normal(0, sd) + (slope * (d - 5) if d > 5 else 0) for d in range(1, 21)]
    fixed = next((i + 1 for i in range(1, 20) if (vals[i] - mean) / sd >= k and (vals[i - 1] - mean) / sd >= k), None)
    res = cusum(vals, mean, sd)
    alarm = res["alarm_index"] + 1 if res["alarm_index"] is not None else None
    marks = {}
    if fixed:
        marks[fixed] = ("#F2C14E", UI["tech_cp_mark_fixed"])
    if alarm:
        marks[alarm] = ("#E9A27A", UI["tech_cp_mark_cusum"])
    st.html(_DOTS + _strip(20, marks))
    st.caption(UI["tech_cp_try_res"].format(f=fixed or "–", c=alarm or "–"))


def _signature(UI, cap):
    if "tech_key" not in st.session_state:
        st.session_state["tech_key"] = generate_keypair()
    private = st.session_state["tech_key"][0]
    env = sign_capsule(cap, private, None)
    st.caption(UI["tech_sig_hash"].format(h=env["payload_sha256"][:16]))
    tampered = st.button(UI["tech_sig_btn"], key="tech_tamper")
    what = st.radio(UI["tech_sig_pick"], UI["tech_sig_opts"], key="tech_sig_what", horizontal=True)
    target = copy.deepcopy(cap)
    if tampered or what == UI["tech_sig_opts"][1]:
        target["day"] = cap["day"] + 1
    elif what == UI["tech_sig_opts"][2]:
        target["states"] = {**target["states"], next(iter(target["states"])): "NORMAL"}
    elif what == UI["tech_sig_opts"][3] and target.get("signals"):
        target["signals"][0] = {**target["signals"][0], "value": (target["signals"][0].get("value") or 0) + 1}
    ok, why = verify_capsule(target, env, None)
    st.metric(UI["tech_sig_metric"], env["payload_sha256"][:8], UI["tech_sig_valid"] if ok else UI["tech_sig_broken"],
              delta_color="normal" if ok else "inverse")
    st.write(UI["tech_sig_ok"] if ok else UI["tech_sig_bad"].format(r=why))


def _sync(UI):
    a, b = Replica("earth"), Replica("ship")
    out = st.slider(UI["tech_sync_cut"], 0, 20, (6, 14), key="tech_sync_out")
    delay = st.slider(UI["tech_sync_delay"], 0, 4, 2, key="tech_sync_delay")
    rec = simulate_link(a, b, delay, out, 24, 7)
    first = next((r["step"] for r in rec if r["step"] >= out[1] and r["converged"]), None)
    st.html(_DOTS + _strip(24, {first: ("#4CD6A0", UI["tech_sync_mark"])} if first else {}, off=out))
    st.write(UI["tech_sync_text"].format(a=out[0], b=out[1], d=delay))
    st.write(UI["tech_sync_ok"].format(s=first) if first is not None else UI["tech_sync_ko"])


def _hrv(UI):
    stress = st.slider(UI["tech_hrv_stress"], 0.0, 1.0, 0.0, 0.1, key="tech_stress")
    rr, dropped = clean_rr(simulated_rr(120, 62.0, 5, stress))
    c1, c2 = st.columns(2)
    c1.metric(UI["tech_hrv_rmssd_lab"], f"{rmssd(rr):.0f} ms")
    c2.metric(UI["tech_hrv_sdnn_lab"], f"{sdnn(rr):.0f} ms")
    import altair as alt
    import pandas as pd
    beats = pd.DataFrame({"beat": range(1, 61), "ms": rr[:60]})
    st.altair_chart(alt.Chart(beats).mark_line(color="#E9A27A", strokeWidth=2.5).encode(   # zero is off the axis: the variation is the signal
        x=alt.X("beat:Q", title=None), y=alt.Y("ms:Q", title=None, scale=alt.Scale(zero=False))).properties(height=150), width="stretch")
    st.caption(UI["tech_hrv_dropped"].format(n=dropped))
    st.caption(UI["tech_hrv_note"])


@st.cache_data(show_spinner=False)
def _cs_scores():
    return (common_signal.accuracy(range(0, 200)), common_signal.accuracy(range(5000, 6000)),
            common_signal.accuracy_all_days(range(5000, 6000)))


def _common(UI):
    import numpy as np
    a, b, c = _cs_scores()
    st.write(UI["tech_cs_result"].format(a=100 * a, b=100 * b))
    st.caption(UI["tech_cs_all"].format(c=100 * c))
    k = st.slider(UI["tech_cs_k"], 1, 4, 3, key="tech_cs_k")
    size = st.slider(UI["tech_cs_size"], 0.5, 3.0, 2.2, 0.1, key="tech_cs_size")
    rng = np.random.default_rng(5)
    z = {f"Crew {chr(65 + i)}": list(rng.normal(0, 1, 10) * 0.6) for i in range(4)}
    for m in list(z)[:k]:
        z[m][4] += size
    st.caption(UI["tech_cs_try"].format(k=k))
    marks = {}
    for r in common_signal.attribute(z):
        if r["kind"] != "none":
            marks[r["day"]] = ("#F2C14E" if r["kind"] == "shared" else "#E9A27A", r["kind"])
            word = UI["tech_cs_shared"] if r["kind"] == "shared" else UI["tech_cs_individual"].format(m=", ".join(r["members"]))
            st.caption(UI["tech_cs_day"].format(d=r["day"], k=word))
    st.html(_DOTS + _strip(10, marks))


def _ledger(UI):
    import altair as alt
    led = exposure_ledger.ledger()
    days = [d.strftime("%d %b %Y") for d in led["date"]]
    pick = st.select_slider(UI["tech_led_pick"], days, value=days[-1], key="tech_led_day")
    row = led.iloc[days.index(pick)]
    m1, m2 = st.columns(2)
    m1.metric(UI["tech_led_rad"], f"{row['radiation_mgy_cum']:.2f} mGy")
    co2 = row["co2_7d_mmhg"]
    m2.metric(UI["tech_led_co2"], "–" if co2 != co2 else f"{co2:.2f} mmHg",
              None if co2 != co2 else (UI["tech_led_above"] if row["co2_7d_above_2_5"] else UI["tech_led_below"]),
              delta_color="inverse" if co2 == co2 and row["co2_7d_above_2_5"] else "off")
    c1, c2 = st.columns(2)
    for col, field, title, colour in ((c1, "radiation_mgy_cum", UI["tech_led_rad"], "#E9A27A"), (c2, "co2_7d_mmhg", UI["tech_led_co2"], "#F2C14E")):
        col.caption(title)
        col.altair_chart(alt.Chart(led.dropna(subset=[field])).mark_line(color=colour, strokeWidth=2.5).encode(
            x=alt.X("date:T", title=None), y=alt.Y(f"{field}:Q", title=None, scale=alt.Scale(zero=False))).properties(height=150), width="stretch")
    st.caption(UI["tech_led_note"])


def _explainer(UI):
    import json
    import os
    st.write(UI["tech_ex_what"])
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "out", "capsules_histoire.json")
    with open(path, encoding="utf-8") as fh:
        caps = {c["day"]: c for c in json.load(fh) if c.get("capsule_type", "daily") == "daily"}
    day = st.select_slider(UI["tech_ex_pick"], sorted(caps), value=9 if 9 in caps else max(caps), key="tech_ex_day")
    cap = caps[day]
    lines = explainer.explain(cap)
    st.caption(UI["tech_ex_day"].format(d=day))
    st.markdown("\n".join(f"> {x}" for x in lines))
    assert explainer.check(lines, cap) == []
    st.caption(UI["tech_ex_ok"])
    mine = st.text_input(UI["tech_ex_try"], UI["tech_ex_try_default"], key="tech_ex_mine", max_chars=200)
    probs = explainer.check([mine], cap) if mine.strip() else []
    st.caption(UI["tech_ex_pass"] if not probs else UI["tech_ex_block"].format(r="; ".join(p.split(":")[0] for p in probs)))


def _dtn(UI):
    c1, c2, c3 = st.columns(3)
    hours = c1.slider(UI["tech_dtn_out"], 0, 12, 6, key="tech_dtn_out")
    delay = c2.slider(UI["tech_dtn_delay"], 0, 24, 20, key="tech_dtn_delay")
    loss = c3.slider(UI["tech_dtn_loss"], 0, 30, 10, 5, key="tech_dtn_loss")
    r = dtn.simulate(200, 3, (60, 60 + 60 * hours), delay, loss / 100, seed=4)
    m1, m2, m3 = st.columns(3)
    m1.metric(UI["tech_dtn_m_ok"], UI["tech_dtn_yes"] if r["all_once_in_order"] else UI["tech_dtn_no"])
    m2.metric(UI["tech_dtn_m_tx"], r["transmissions"])
    m3.metric(UI["tech_dtn_m_dup"], r["duplicates_dropped"])
    st.caption(UI["tech_dtn_res"].format(h=r["last_arrival_min"] // 60, m=r["last_arrival_min"] % 60))


def _camera(UI, mode):
    w = {k[len("tech_camw_"):]: v for k, v in UI.items() if k.startswith("tech_camw_")}
    w["note"] = UI["tech_cam_note_" + mode]
    st.iframe(camera_lab.page(mode, w, UI["tech_cam_unit_" + mode]), height=camera_lab.HEIGHT)


def _promise_lines(UI, item):
    if item.get("test"):
        st.markdown(f"**{UI['tech_test']}:** {item['test']}  \n**{UI['tech_drop']}:** {item['drop_if']}")


def _building(UI, item):
    """A concept is a promise with its test: what it would bring, how we will know, and what would make us drop it."""
    assert item.get("test") and item.get("drop_if"), f"concept {item['id']} has no test: a promise without a test is not shown"
    if item["id"] == "dtn":
        st.markdown(_ANIM + "<div class='cs-dtn'><i></i><i></i><i></i></div>", unsafe_allow_html=True)
    st.markdown(f"**{UI['tech_test']}:** {item['test']}  \n**{UI['tech_drop']}:** {item['drop_if']}")
    st.caption(UI["tech_building"] if item["id"] == "dtn" else UI["tech_building_static"])


def tech_panel(UI, daily, trends, day):
    """Render all technology cards. `daily` is the shown day's capsule (or None)."""
    reg = registry.load()
    problems = registry.audit(reg)
    assert not problems, problems   # an overclaiming registry must never reach a visitor
    st.subheader(UI["tech_title"])
    st.caption(UI["tech_intro"])
    sig = next((s for s in (daily or {}).get("signals", []) if s.get("indicator_id") == "CO01"), None)
    groups = {UI["tech_g_measure"]: "measure", UI["tech_g_decide"]: "decide", UI["tech_g_deliver"]: "deliver"}
    g = st.segmented_control(UI["tech_g_label"], list(groups), default=list(groups)[1], key="tech_group") or list(groups)[1]
    st.caption(UI["tech_g_why_" + groups[g]])
    for item in [i for i in reg["items"] if i.get("group") == groups[g]]:
        with st.container(border=True):
            _banner(UI, item, reg)
            live = item["status"] in ("BUILT", "PROTOTYPE") and registry.module_exists(item.get("module"))
            if not live:
                _building(UI, item)
            elif item["id"] == "changepoint":
                _changepoint(UI, trends, sig, day)
            elif item["id"] == "signed_capsule" and daily:
                _signature(UI, daily)
            elif item["id"] == "offline_sync":
                _sync(UI)
            elif item["id"] == "hrv":
                _hrv(UI)
            elif item["id"] == "common_signal":
                _common(UI)
                _promise_lines(UI, item)
            elif item["id"] == "dtn":
                _dtn(UI)
                _promise_lines(UI, item)
            elif item["id"] in ("camera_pulse", "eye_blink"):
                _camera(UI, "pulse" if item["id"] == "camera_pulse" else "blink")
                _promise_lines(UI, item)
            elif item["id"] == "onboard_explainer":
                _explainer(UI)
                _promise_lines(UI, item)
            elif item["id"] == "exposure_ledger":
                _ledger(UI)
                _promise_lines(UI, item)
