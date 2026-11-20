"""3D body viewer (V3): a mannequin built in code, rendered in the visitor's browser with three.js 0.187.0 (MIT, unpkg).
Zone looks come from the zone sheets (pitch/silhouette/fiches.json); the flat 2D map is the fallback without WebGL."""
from __future__ import annotations

import html
import json
import os

from csync import silhouette

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
THREE = "https://unpkg.com/three@0.187.0/build/three.module.js"
HEIGHT = 520


def viewer_html(selected: str | None, caption: str, hint: str) -> str:
    """Self-contained page for the 3D viewer (pure function, tested)."""
    status = {rid: r["status"] for rid, r in silhouette.fiches().items()}
    assert status and all(v in ("measured", "unknown", "context") for v in status.values())
    if selected is not None:
        assert selected in status, selected
    with open(os.path.join(ASSETS, "body3d.js"), encoding="utf-8") as fh:
        js = fh.read()
    cfg = {"three": THREE, "status": status, "selected": selected, "fallback": silhouette.svg(selected)}
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>
html,body{{margin:0;height:100%;background:transparent;font:14px/1.4 system-ui,-apple-system,Segoe UI,sans-serif;color:#FFFDFD}}
#wrap{{position:relative;height:{HEIGHT - 8}px;border-radius:36px;overflow:hidden;
 background:radial-gradient(70% 55% at 50% 38%,rgba(215,154,118,.28),transparent 70%),linear-gradient(180deg,rgba(75,64,57,.85),rgba(34,27,23,.95));
 border:1px solid rgba(255,253,253,.18)}}
#stage{{position:absolute;inset:0 0 58px 0}} #stage svg{{height:100%;width:auto;display:block;margin:auto}}
#cap{{position:absolute;left:18px;right:18px;bottom:12px;display:flex;flex-direction:column;gap:2px;font-size:13.5px}}
#cap b{{font-weight:600}}
</style></head><body><div id='wrap' role='img' aria-label='{html.escape(caption)}'><div id='stage'></div>
<div id='cap'><b>{html.escape(caption)}</b><span>{html.escape(hint)}</span></div></div>
<script>window.CS_BODY={json.dumps(cfg)};</script><script>{js}</script></body></html>"""
