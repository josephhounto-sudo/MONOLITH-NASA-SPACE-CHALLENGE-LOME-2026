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


def _banner(UI, item, reg):
    st.markdown(f"**{item['name']}** · {registry.label(reg, item)}")
    st.caption(item["purpose"])
    st.caption(UI["tech_data"].format(d=item["data"]))


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
    st.write(UI["tech_sig_ok"] if ok else UI["tech_sig_bad"].format(r=why))


def _sync(UI):
    a, b = Replica("earth"), Replica("ship")
    out = (6, 14)
    rec = simulate_link(a, b, 2, out, 24, 7)
    first = next((r["step"] for r in rec if r["step"] >= out[1] and r["converged"]), None)
    st.write(UI["tech_sync_text"].format(a=out[0], b=out[1]))
    st.write(UI["tech_sync_ok"].format(s=first) if first is not None else UI["tech_sync_ko"])


def _hrv(UI):
    stress = st.slider(UI["tech_hrv_stress"], 0.0, 1.0, 0.0, 0.1, key="tech_stress")
    rr, dropped = clean_rr(simulated_rr(120, 62.0, 5, stress))
    st.write(UI["tech_hrv_rmssd"].format(v=f"{rmssd(rr):.0f}"))
    st.write(UI["tech_hrv_sdnn"].format(v=f"{sdnn(rr):.0f}"))
    st.caption(UI["tech_hrv_dropped"].format(n=dropped))
    st.caption(UI["tech_hrv_note"])


def _building(UI, item):
    if item["id"] == "dtn":
        st.markdown(_ANIM + "<div class='cs-dtn'><i></i><i></i><i></i></div>", unsafe_allow_html=True)
    st.caption(UI["tech_building"])


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
