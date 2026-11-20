"""Technologies page: one card per registry item. A card shows a live demo only when the registry says the module exists."""
from __future__ import annotations

import copy

import streamlit as st

from csync.analytics.changepoint import bocpd, cusum
from csync.crypto.capsule_sign import generate_keypair, sign_capsule, verify_capsule
from csync.physio.hrv import clean_rr, rmssd, sdnn, simulated_rr
from csync.sync.crdt_sim import Replica, simulate_link
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
    st.caption(UI["tech_data"].format(d=UI["tech_data_none"] if item["data"] == "NONE" else item["data"]))


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


def _signature(UI, cap):
    if "tech_key" not in st.session_state:
        st.session_state["tech_key"] = generate_keypair()
    private = st.session_state["tech_key"][0]
    env = sign_capsule(cap, private, None)
    st.caption(UI["tech_sig_hash"].format(h=env["payload_sha256"][:16]))
    tampered = st.button(UI["tech_sig_btn"], key="tech_tamper")
    target = {**copy.deepcopy(cap), "day": cap["day"] + 1} if tampered else cap
    ok, why = verify_capsule(target, env, None)
    st.metric(UI["tech_sig_metric"], env["payload_sha256"][:8], UI["tech_sig_valid"] if ok else UI["tech_sig_broken"],
              delta_color="normal" if ok else "inverse")
    st.write(UI["tech_sig_ok"] if ok else UI["tech_sig_bad"].format(r=why))


def _sync(UI):
    a, b = Replica("earth"), Replica("ship")
    out = (6, 14)
    rec = simulate_link(a, b, 2, out, 24, 7)
    first = next((r["step"] for r in rec if r["step"] >= out[1] and r["converged"]), None)
    st.html(_DOTS + _strip(24, {first: ("#4CD6A0", UI["tech_sync_mark"])} if first else {}, off=out))
    st.write(UI["tech_sync_text"].format(a=out[0], b=out[1]))
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
        x=alt.X("beat:Q", title=None), y=alt.Y("ms:Q", title=None, scale=alt.Scale(zero=False))).properties(height=150), use_container_width=True)
    st.caption(UI["tech_hrv_dropped"].format(n=dropped))
    st.caption(UI["tech_hrv_note"])


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
    for item in reg["items"]:
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
