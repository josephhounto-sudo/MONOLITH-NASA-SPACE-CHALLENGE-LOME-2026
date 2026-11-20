"""Camera lab page (prototypes camera_pulse and eye_blink): self-contained HTML shown in an iframe with camera permission.
Nothing is recorded or sent; the camera starts only on the visitor's click and stops on the second click."""
from __future__ import annotations

import html
import json
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
TASKS = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.2.3/vision_bundle.mjs"   # Apache-2.0
WASM = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.2.3/wasm"
MODEL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
HEIGHT = 330


def page(mode: str, words: dict, unit: str) -> str:
    assert mode in ("pulse", "blink")
    need = {"start", "stop", "hold", "denied", "nomodel", "clear", "noisy", "wait", "closed", "noface", "stopped", "note"}
    assert need <= set(words), need - set(words)
    with open(os.path.join(ASSETS, "camera_lab.js"), encoding="utf-8") as fh:
        js = fh.read()
    cfg = {"mode": mode, "words": words, "tasks": TASKS, "wasm": WASM, "model": MODEL}
    box = ("<div style='position:absolute;left:40%;top:22%;width:20%;height:12%;border:2px dashed #FF8A4C;border-radius:10px'></div>"
           if mode == "pulse" else "")
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>
body{{margin:0;font:14px/1.4 system-ui,sans-serif;color:#FFFDFD;background:transparent}}
.w{{display:flex;gap:16px;align-items:stretch;padding:14px;border-radius:28px;background:rgba(34,27,23,.92);border:1px solid rgba(255,253,253,.2)}}
.cam{{position:relative;width:260px;height:195px;border-radius:20px;overflow:hidden;background:#1C1512;flex:none}}
video{{width:100%;height:100%;object-fit:cover;transform:scaleX(-1)}}
.r{{display:flex;flex-direction:column;gap:8px;min-width:0}}
#val{{font:700 54px/1 Doto,monospace;color:#FF8A4C}} button{{border:0;border-radius:999px;padding:10px 18px;font-weight:600;background:#FFFDFD;color:#2E2621;cursor:pointer;width:max-content}}
small{{opacity:.9}}</style></head><body><div class='w'><div class='cam'><video id='vid' playsinline muted></video>{box}</div>
<div class='r'><button id='go'>{html.escape(words['start'])}</button><div><span id='val'>–</span> <b>{html.escape(unit)}</b></div>
<span id='q'></span><span id='msg'></span><small>{html.escape(words['note'])}</small></div></div>
<script>window.CS_CAM={json.dumps(cfg)};</script><script type='module'>{js}</script></body></html>"""
