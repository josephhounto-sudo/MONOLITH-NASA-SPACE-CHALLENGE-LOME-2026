"""Live console (V3 home): real ISS cabin air from NASA's public ISSLive feed, four mission clocks, and the honest status of
the physiology channels. Context only: nothing here opens a procedure or changes a state (AGENTS.md, decisions of 20/11).

The feed is read in the visitor's browser (push.lightstreamer.com, adapter ISSLIVE, client lightstreamer-client-web 9.2.3,
Apache-2.0). Item identifiers come from the ISSLive symbol dictionary (Lightstreamer ISSLive example, src/assets/PUIList.xml).
"""
from __future__ import annotations

import html
import os

import streamlit as st

from csync.ui import bookings, bot, style

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LS_CLIENT = "https://unpkg.com/lightstreamer-client-web@9.2.3/lightstreamer.min.js"
CARDS = (("co2lab", "card_co2lab", "mmHg", True), ("co2n3", "card_co2n3", "mmHg", True),
         ("o2", "card_o2", "% of cabin air", False), ("cabin", "card_cabin", "mmHg", False))
ICONS = {"co2lab": "cloud", "co2n3": "cloud", "o2": "wind", "cabin": "gauge"}
HEIGHT = 470   # desktop; on a phone the page scrolls inside (cards stack)


def _js() -> str:
    with open(os.path.join(ASSETS, "live.js"), encoding="utf-8") as fh:
        js = fh.read()
    assert "readingState" in js and "LIMIT_PPCO2_MMHG = 3.0" in js
    return js


def console_html(ui: dict) -> str:
    """Self-contained page for the live component (pure function, tested)."""
    e = lambda k: html.escape(ui[k])   # noqa: E731
    clocks = "".join(f"<div class='clk'><span class='z'>{html.escape(n)}</span><span class='t' id='clk{i}'>--:--:--</span></div>"
                     for i, n in enumerate(("Station (UTC)", "Houston", "Moscow", "Lomé")))
    cards = []
    for key, label, unit, ctx in CARDS:
        ico = bookings.lucide(ICONS[key]).replace("<svg", "<svg class='ico' aria-hidden='true'", 1)
        delta = f"<span class='dl' id='d-{key}'></span>" if ctx else ""
        cards.append(f"<div class='pill' id='c-{key}' data-state='Connecting'><div class='top'><span class='lab'>{e(label)}</span>{ico}</div>"
                     f"<div class='num'><span class='v' id='v-{key}'>--</span><small>{html.escape(unit)}</small>{delta}</div>"
                     f"<div class='meta'><span class='st' id='s-{key}'>Connecting</span> <span class='why' id='w-{key}'>waiting for the first reading from the station</span></div>"
                     + (f"<div class='ctx' id='ctx-{key}'></div>" if ctx else "") + "</div>")
    ops = (f"<div class='ops'><div class='clk'><span class='z'>{e('ops_link')}</span><span class='t2' id='link'>Connecting</span></div>"
           f"<div class='clk'><span class='z'>{e('ops_delay')}</span><span class='t2'>{e('live_delay')}</span></div></div>")
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>
@font-face{{font-family:Doto;font-weight:700;src:url(data:font/woff2;base64,{style._font('Doto-700.woff2')}) format("woff2")}}
body{{margin:0;font:15px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;color:{bookings.INK};background:transparent}}
.clocks{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 14px}}
.clk{{border-radius:999px;padding:8px 14px;background:rgba(34,27,23,.82);border:1px solid rgba(255,253,253,.18);display:flex;flex-direction:column}}
.clk .z{{font-size:13px;opacity:.95}} .clk .t,.v{{font-family:Doto,monospace;font-weight:700}} .clk .t{{font-size:22px;letter-spacing:.04em}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:-6px 0 14px}} .t2{{font-weight:700;font-size:15px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.pill{{position:relative;border-radius:40px;padding:16px 20px 14px;background-color:rgba(34,27,23,.90);
 background-image:radial-gradient(55% 90% at 106% 50%,rgba(215,154,118,.62),transparent 72%);border:1px solid rgba(255,253,253,.18);
 box-shadow:inset 1px 1px 0 rgba(255,253,253,.16)}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:8px}} .lab{{font-weight:600}}
.ico{{width:22px;height:22px;flex:none}}
.dl{{margin-left:auto;font-size:13px;font-weight:600;padding:3px 10px;border-radius:999px;border:1px solid rgba(255,253,253,.4);background:rgba(255,253,253,.06)}}
.dl:empty{{display:none}} .meta{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.st{{font-size:13px;font-weight:700;padding:2px 10px;border-radius:999px;border:1px solid rgba(255,253,253,.5)}}
.pill[data-state=Live] .st{{border-color:#4CD6A0;color:#4CD6A0}} .pill[data-state=Check] .st,.pill[data-state='Last known'] .st{{border-color:#F2C14E;color:#F2C14E}}
.num{{display:flex;align-items:baseline;gap:8px;margin:6px 0 2px}} .v{{font-size:46px;line-height:1}} .num small{{font-size:14px}}
.why,.ctx,.note{{font-size:13.5px}} .ctx{{margin-top:2px}}
.src{{margin:12px 2px 0;font-size:13.5px}} #feed,#unit{{font-size:13.5px}}
@media (max-width:560px){{.clocks{{grid-template-columns:1fr 1fr}}.grid{{grid-template-columns:1fr}}.v{{font-size:40px}}}}
</style></head><body>
<div class='clocks' role='group' aria-label='Mission clocks'>{clocks}</div>{ops}
<div class='grid'>{''.join(cards)}</div>
<p class='src'>{e('live_source')} <span id='feed'></span> <span id='unit'></span></p>
<script src='{LS_CLIENT}'></script><script>{_js()}</script></body></html>"""


def physiology_html(ui: dict) -> str:
    rows = [("live_phys_hr", "live_simulated"), ("live_phys_blink", "live_in_dev")]
    out = []
    for k, status in rows:
        out.append(f"<div class='cs-card ctx'><div class='dim'>{html.escape(ui[k])}</div>"
                   f"<div style='font-size:1.05em'>{html.escape(ui[status])}</div>"
                   f"<p style='margin:.4em 0 0'>{html.escape(ui[k + '_note'])}</p></div>")
    return "<div class='cs-phys'>" + "".join(out) + "</div>"


def panel(ui: dict) -> None:
    bot.tutorial(ui)
    st.subheader(ui["live_title"])
    st.caption(ui["live_intro"])
    page = console_html(ui)
    if hasattr(st, "iframe"):
        st.iframe(page, height="content")
    else:   # older Streamlit on a host
        import streamlit.components.v1 as components
        components.html(page, height=HEIGHT, scrolling=False)
    st.subheader(ui["live_phys_title"])
    st.html(physiology_html(ui))
