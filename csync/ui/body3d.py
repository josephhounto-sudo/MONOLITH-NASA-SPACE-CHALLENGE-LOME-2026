"""3D body viewer (V3): a mannequin built in code, rendered in the visitor's browser with three.js 0.187.0 (MIT, unpkg).
Zone looks come from the zone sheets (pitch/silhouette/fiches.json); the flat 2D map is the fallback without WebGL."""
from __future__ import annotations

import html
import json
import os

from csync import silhouette

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
THREE = "https://unpkg.com/three@0.187.0/build/three.module.js"
ADDONS = "https://unpkg.com/three@0.187.0/examples/jsm/"
# "Cesium Man" (Khronos glTF Sample Assets, commit f0920f5), CC BY 4.0 (c) Cesium 2017; texture and logo are not used
MODEL = ("https://cdn.jsdelivr.net/gh/KhronosGroup/glTF-Sample-Assets@f0920f5b32d172a30efe3f9257e965918831e6ea"
         "/Models/CesiumMan/glTF-Binary/CesiumMan.glb")
MODEL_CREDIT = "3D figure: Cesium Man by Cesium, CC BY 4.0 (Khronos glTF Sample Assets)"
HEIGHT = 640


def viewer_html(selected: str | None, caption: str, hint: str) -> str:
    """Self-contained page for the 3D viewer (pure function, tested)."""
    status = {rid: r["status"] for rid, r in silhouette.fiches().items()}
    assert status and all(v in ("measured", "unknown", "context") for v in status.values())
    if selected is not None:
        assert selected in status, selected
    with open(os.path.join(ASSETS, "body3d.js"), encoding="utf-8") as fh:
        js = fh.read()
    labels = {rid: silhouette.label(rid) for rid in status}
    cfg = {"model": MODEL, "status": status, "selected": selected, "fallback": silhouette.svg(selected),
           "labels": labels, "words": silhouette.STATUS_WORD, "measuredWord": "Measured", "offWord": "Not monitored yet"}
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>
html,body{{margin:0;height:100%;background:transparent;font:14px/1.4 system-ui,-apple-system,Segoe UI,sans-serif;color:#FFFDFD}}
#wrap{{position:relative;height:{HEIGHT - 8}px;border-radius:36px;overflow:hidden;
 background:radial-gradient(70% 55% at 50% 38%,rgba(215,154,118,.28),transparent 70%),linear-gradient(180deg,rgba(75,64,57,.85),rgba(34,27,23,.95));
 border:1px solid rgba(255,253,253,.18)}}
#stage{{position:absolute;inset:0 0 58px 0}} #stage svg{{height:100%;width:auto;display:block;margin:auto}}
#cap{{position:absolute;left:18px;right:18px;bottom:12px;display:flex;flex-direction:column;gap:2px;font-size:13.5px}}
#cap b{{font-weight:600}}
.co{{position:absolute;display:flex;flex-direction:column;padding:5px 12px;border-radius:999px;background:rgba(34,27,23,.82);border:1px solid rgba(255,253,253,.28);font-size:12.5px;line-height:1.25;white-space:nowrap}}
.co b{{font-weight:600}} .co span{{font-size:11.5px;opacity:.95}} .co.off{{border-style:dashed}}
.co.sel{{background:#FFFDFD;color:#2E2621;box-shadow:0 0 22px rgba(255,138,76,.55)}}
.ld{{fill:none;stroke:rgba(255,253,253,.55);stroke-width:1.2}} .ld.sel{{stroke:#FF8A4C;stroke-width:2}}
</style></head><body><div id='wrap' role='img' aria-label='{html.escape(caption)}'><div id='stage'></div>
<div id='tip' style='position:absolute;pointer-events:none;opacity:0;transition:opacity .15s;padding:6px 12px;border-radius:999px;
 background:#FFFDFD;color:#2E2621;font-size:13px;font-weight:600;white-space:nowrap;box-shadow:0 8px 20px rgba(0,0,0,.3)'></div><svg id='leaders' style='position:absolute;inset:0 0 58px 0;width:100%;height:calc(100% - 58px);pointer-events:none'></svg>
<div id='callouts' style='position:absolute;inset:0 0 58px 0;pointer-events:none'></div><div id='cap'><b>{html.escape(caption)}</b><span>{html.escape(hint)}</span><small style='opacity:.85'>{html.escape(MODEL_CREDIT)}</small></div></div>
<script type='importmap'>{json.dumps({"imports": {"three": THREE, "three/addons/": ADDONS}})}</script>
<script>window.CS_BODY={json.dumps(cfg)};</script><script>{js}</script></body></html>"""
