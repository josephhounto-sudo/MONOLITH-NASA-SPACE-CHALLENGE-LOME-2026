"""C-Sync look: "Monolith Glass". Appearance only, no logic, no clinical text.

Rules (docs/DESIGN_DIRECTION.md):
- Layer 0, a deep space background with slow decorative shapes (aria-hidden, no pointer events).
- Layer 1, content panels: a thick, mostly opaque material, so text stays legible.
- Layer 2, the functional layer (top bar, banner, buttons, slider): lighter frosted glass.
- Red, amber and green belong to states, cyan belongs to interaction, blue only tints chrome and background.
- Nothing carries meaning by colour alone: every state keeps its icon and its word.
- Motion is slow (60 to 220 s loops), uses transform and opacity only, and stops under prefers-reduced-motion.
- Frosted glass falls back to opaque panels under prefers-reduced-transparency or without backdrop-filter.
All colours come from csync/config/theme.json.
"""
import base64
import json
import os
from string import Template
from urllib.parse import quote

import streamlit as st

CFG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
THEME = json.load(open(os.path.join(CFG, "theme.json"), encoding="utf8"))


def _rgba(hex_colour, alpha):
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


_CSS = """
:root{
  --cs-surface:%(surface)s; --cs-panel:%(panel)s; --cs-text:%(text)s; --cs-text2:%(text2)s;
  --cs-cyan:%(cyan)s; --cs-trust:%(trust)s; --cs-trust-soft:%(trust_soft)s; --cs-deep:%(deep)s; --cs-warm:%(warm)s;
  --cs-glass:%(glass)s; --cs-thick:%(thick)s; --cs-line:%(line)s; --cs-hi:%(hi)s;
  --cs-font:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI Variable Display","Segoe UI",Inter,system-ui,sans-serif;
}
html,body,[data-testid="stApp"]{background:
  radial-gradient(1200px 700px at 78%% -10%%,%(trust_a)s,transparent 60%%),
  radial-gradient(900px 600px at -5%% 105%%,%(cyan_a)s,transparent 60%%),
  linear-gradient(180deg,var(--cs-deep),var(--cs-surface) 70%%);
  background-attachment:fixed;color:var(--cs-text);font-family:var(--cs-font);}
[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stMain"]{background:transparent!important}
[data-testid="stMain"],[data-testid="stMainBlockContainer"]{position:relative;z-index:1}
[data-testid="stMainBlockContainer"]{max-width:1180px;padding-top:1.2rem}
h1,h2,h3,h4{font-family:var(--cs-font);letter-spacing:-.015em}
h3{font-size:clamp(1.45rem,2.6vw,2.05rem)!important;font-weight:650!important;line-height:1.2;margin:.9rem 0 .8rem!important}
p,li,label,[data-testid="stMarkdownContainer"]{font-feature-settings:"tnum" 1,"cv11" 1}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] *{color:var(--cs-text2)!important;opacity:1!important}

[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
[data-testid="stHorizontalBlock"]{margin-bottom:.9rem}
/* layer 0: background shapes */
.cs-bg{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.cs-bg .blob{position:absolute;border-radius:50%%;filter:blur(70px);opacity:.5;will-change:transform}
.cs-bg .b1{width:46vw;height:46vw;left:-12vw;top:-14vw;background:%(trust_a2)s;animation:csdrift1 70s ease-in-out infinite alternate}
.cs-bg .b2{width:34vw;height:34vw;right:-8vw;bottom:-10vw;background:%(cyan_a2)s;animation:csdrift2 90s ease-in-out infinite alternate}
.cs-bg .b3{width:22vw;height:22vw;right:18vw;top:8vh;background:%(warm_a)s;opacity:.35;animation:csdrift1 110s ease-in-out infinite alternate-reverse}
.cs-bg .poly,.cs-bg .rings,.cs-bg .lines{position:absolute}
.cs-bg .poly{right:-5vw;top:4vh;width:min(38vw,540px);aspect-ratio:1;opacity:.42;animation:csspin 160s linear infinite}
.cs-bg .rings{left:-9vw;bottom:-9vw;width:min(40vw,560px);aspect-ratio:1;opacity:.4;animation:csspin 240s linear infinite reverse}
.cs-bg .lines{left:0;top:0;width:100%%;height:100%%;opacity:.5;animation:csdrift2 120s ease-in-out infinite alternate}
.cs-bg .dots{position:absolute;left:3vw;top:20vh;width:260px;height:200px;opacity:.35;
  background-image:radial-gradient(circle,%(text2_a)s 1.2px,transparent 1.6px);background-size:18px 18px;
  -webkit-mask-image:linear-gradient(135deg,#000,transparent 80%%);mask-image:linear-gradient(135deg,#000,transparent 80%%);
  animation:csdrift1 100s ease-in-out infinite alternate}
@keyframes csspin{to{transform:rotate(360deg)}}
@keyframes csdrift1{from{transform:translate3d(0,0,0)}to{transform:translate3d(4vw,3vh,0)}}
@keyframes csdrift2{from{transform:translate3d(0,0,0)}to{transform:translate3d(-3vw,-2vh,0)}}

/* layer 2: top bar */
.cs-top{display:flex;align-items:center;gap:14px;padding:12px 18px;margin:0 0 14px;border-radius:18px;
  background:var(--cs-glass);border:1px solid var(--cs-line);box-shadow:inset 0 1px 0 var(--cs-hi),0 12px 40px rgba(0,0,0,.35);
  -webkit-backdrop-filter:blur(16px) saturate(140%%);backdrop-filter:blur(16px) saturate(140%%)}
.cs-top .nm{font-weight:700;font-size:1.15rem;letter-spacing:-.01em}
.cs-top .tg{color:var(--cs-text2);font-size:.86rem;letter-spacing:.02em}

/* banner and alerts: glass pills */
[data-testid="stAlert"]{border-radius:14px;border:1px solid var(--cs-line);background:var(--cs-glass)!important;
  box-shadow:inset 0 1px 0 var(--cs-hi);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
[data-testid="stAlert"] p{color:var(--cs-text)!important}

/* layer 1: content panels */
.cs-card{display:flex;flex-direction:column;justify-content:center;gap:4px;min-height:98px;padding:14px 16px 14px 18px;border-radius:16px;position:relative;overflow:hidden;
  background:linear-gradient(135deg,var(--rail-a),transparent 55%%),var(--cs-thick);border:1px solid var(--cs-line);
  box-shadow:inset 0 1px 0 var(--cs-hi),0 10px 30px rgba(0,0,0,.3);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.cs-card::before{content:"";position:absolute;left:0;top:12px;bottom:12px;width:4px;border-radius:0 4px 4px 0;background:var(--rail)}
.cs-card .dim{color:var(--cs-text2);font-size:.78rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase}
.cs-card .st{font-size:1.1em;font-weight:600}
.cs-card.ctx{background:transparent;border-style:dashed}
.cs-card.ctx::before{background:var(--cs-text2);opacity:.5}
[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"]{background:var(--cs-thick)!important;border:1px solid var(--cs-line)!important;
  border-radius:16px!important;box-shadow:inset 0 1px 0 var(--cs-hi),0 10px 30px rgba(0,0,0,.28);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
[data-testid="stExpander"] summary{font-weight:600}
.cs-decision{display:inline-block;margin:6px 0 2px;padding:10px 18px;border-radius:14px;border:1px solid var(--cs-line);font-size:1.4em;font-weight:700;
  background:linear-gradient(135deg,var(--rail-a),transparent 70%%),var(--cs-thick);box-shadow:inset 0 1px 0 var(--cs-hi)}
.cs-kicker{display:inline-block;margin:.2rem 0 -.2rem;padding:4px 12px;border-radius:999px;border:1px solid var(--cs-line);background:var(--cs-glass);color:var(--cs-cyan);font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
hr{border-color:var(--cs-line)!important;margin:1.4rem 0!important}

/* layer 2: controls */
.stButton>button{border-radius:999px;border:1px solid var(--cs-line);background:var(--cs-glass);color:var(--cs-text);font-weight:600;padding:.5rem 1.2rem;
  box-shadow:inset 0 1px 0 var(--cs-hi);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);transition:border-color .25s,transform .25s,box-shadow .25s}
.stButton>button:hover:not(:disabled){border-color:var(--cs-cyan);box-shadow:inset 0 1px 0 var(--cs-hi),0 0 0 3px %(cyan_a)s;transform:translateY(-1px)}
.stButton>button:focus-visible{outline:2px solid var(--cs-cyan);outline-offset:3px}
.stButton>button:disabled{opacity:.45}
[data-testid="stSlider"]{padding:.4rem .9rem .2rem;border-radius:16px;background:var(--cs-glass);border:1px solid var(--cs-line);
  -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
[data-testid="stRadio"] label{color:var(--cs-text)}

/* accessibility fallbacks */
@media (prefers-reduced-motion:reduce){.cs-bg *,.cs-bg{animation:none!important}.stButton>button{transition:none}}
@media (prefers-reduced-transparency:reduce){
  .cs-top,[data-testid="stAlert"],.cs-card,[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"],.stButton>button,[data-testid="stSlider"]{
    -webkit-backdrop-filter:none!important;backdrop-filter:none!important;background:var(--cs-panel)!important}
  .cs-bg{opacity:.35}}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
  .cs-top,[data-testid="stAlert"],.stButton>button,[data-testid="stSlider"]{background:var(--cs-panel)!important}}
@media (max-width:760px){.cs-bg .poly{opacity:.3}.cs-top{padding:10px 14px}}
"""

_SHAPES = """
<div class="cs-bg" aria-hidden="true">
  <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  <div class="dots"></div><div class="lines"></div><div class="rings"></div><div class="poly"></div>
</div>
"""

_TOP = """
<header class="cs-top">
  <div class="mark" aria-hidden="true"></div>
  <div><div class="nm">%(name)s</div><div class="tg">%(tag)s</div></div>
</header>
"""


# Profile "quiet": the unslop-style pass (docs/DESIGN_SKILL_SOURCES.md). Same markup, CSS only. Select with CSYNC_STYLE=quiet.
_QUIET = """
html,body,[data-testid="stApp"]{background:var(--cs-surface)!important}
.cs-bg .blob,.cs-bg .rings,.cs-bg .dots,.cs-bg .lines{display:none}
.cs-bg .poly{animation:none;opacity:.22}
.cs-top,[data-testid="stAlert"],[data-testid="stSlider"],.stButton>button,.cs-kicker{-webkit-backdrop-filter:none!important;backdrop-filter:none!important;box-shadow:none!important}
.cs-top,[data-testid="stAlert"],[data-testid="stSlider"]{background:var(--cs-panel)!important;border-radius:12px}
.cs-card,.cs-decision,[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"]{background:var(--cs-panel)!important;
  box-shadow:none!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important;border-radius:12px!important}
.cs-card .dim{font-size:.8rem;font-weight:500;letter-spacing:0;text-transform:none}
.cs-kicker{padding:0;border:0;background:none!important;color:var(--cs-text2);font-size:.9rem;font-weight:500;letter-spacing:0;text-transform:none}
.stButton>button{border-radius:10px;background:var(--cs-panel);font-weight:500}
.stButton>button:hover:not(:disabled){transform:none;box-shadow:none!important}
"""

# Profile "hybrid": glass kept on the three state cards and the decision panel only; no looping motion, no uppercase labels,
# no blur on controls or alerts. Select with CSYNC_STYLE=hybrid. M1 decision 14/11 21:30: "glass with a little quiet" (not yet human-tested).
_HYBRID = """
.cs-bg,.cs-bg *{animation:none!important}
.cs-top,[data-testid="stAlert"],[data-testid="stSlider"],.stButton>button,.cs-kicker{-webkit-backdrop-filter:none!important;backdrop-filter:none!important;box-shadow:none!important}
.cs-top,[data-testid="stAlert"],[data-testid="stSlider"]{background:var(--cs-panel)!important}
.cs-card .dim{font-size:.82rem;font-weight:600;letter-spacing:0;text-transform:none}
.cs-kicker{letter-spacing:0;text-transform:none}
.stButton>button:hover:not(:disabled){transform:none;box-shadow:none!important}
"""

# Profile "calm": design pass with the csync-design skill (P2 one rich zone, P3 neutral banner, P4 equal cards, P5 sentence case, P7 no motion).
# Same markup as the others, CSS only. Select with CSYNC_STYLE=calm. Proposed 15/11 05:15, awaiting M1 preview.
_CALM = """
.cs-bg{display:none!important}
html,body,[data-testid="stApp"]{background:var(--cs-surface)!important}
.cs-top,[data-testid="stAlert"],[data-testid="stSlider"],.stButton>button,.cs-kicker,.cs-card,.cs-decision,[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"]{
  -webkit-backdrop-filter:none!important;backdrop-filter:none!important;box-shadow:none!important}
.cs-top,[data-testid="stSlider"],[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"]{background:var(--cs-panel)!important;border-radius:12px!important}
[data-testid="stAlert"],[data-testid="stAlert"] [data-baseweb="notification"],[data-testid="stAlertContainer"]{background:var(--cs-panel)!important;border-radius:12px;border-color:var(--cs-line)!important}
.cs-card{min-height:112px;border-radius:12px;background:linear-gradient(90deg,var(--rail-a),transparent 60%),var(--cs-panel)}
.cs-card.ctx{background:transparent}
.cs-card .dim{font-size:.82rem;font-weight:600;letter-spacing:0;text-transform:none}
.cs-card .st{font-size:1.15rem;font-weight:600}
.cs-kicker{letter-spacing:0;text-transform:none;background:none!important;border:0;padding:0}
.cs-action{margin:.5rem 0 .2rem;padding:.75rem 1rem;border-left:4px solid var(--cs-cyan);background:var(--cs-panel);border-radius:0 12px 12px 0;font-size:1.12rem;font-weight:600}
.stButton>button{border-radius:10px;background:var(--cs-panel);font-weight:600}
.stButton>button:hover:not(:disabled){transform:none}
"""

# Profile "signal": built from M1's brief (futuristic, light glass, shapes) + the two Pinterest ideas kept in DESIGN_DIRECTION s6
# (one distinct shape per state, Swiss grid with a large state word) + emil-design-eng (named transitions, strong ease-out, press feedback).
# Glass only on the state cards and the decision; one static background; no loops. Select with CSYNC_STYLE=signal.
_SIGNAL = """
:root{--cs-ease:cubic-bezier(.23,1,.32,1)}
.cs-bg,.cs-bg *{animation:none!important}
.cs-bg .dots,.cs-bg .lines,.cs-bg .rings,.cs-bg .b3{display:none}
.cs-bg .poly{top:47vh;right:3vw;width:min(32vw,440px);opacity:.2}
.cs-top,[data-testid="stAlert"],[data-testid="stSlider"],.stButton>button,.cs-kicker{-webkit-backdrop-filter:none!important;backdrop-filter:none!important;box-shadow:none!important}
.cs-top,[data-testid="stSlider"]{background:var(--cs-panel)!important;border-radius:12px}
[data-testid="stAlert"],[data-testid="stAlert"] [data-baseweb="notification"],[data-testid="stAlertContainer"]{background:var(--cs-panel)!important;border-radius:12px;border-color:var(--cs-line)!important}
.cs-card{min-height:136px;padding:16px 18px;border-radius:18px;justify-content:space-between;gap:12px;
  background:linear-gradient(160deg,rgba(255,255,255,.09),rgba(255,255,255,.02) 55%),linear-gradient(135deg,var(--rail-a),transparent 70%),var(--cs-glass);
  -webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%)}
.cs-card::before{display:none}
.cs-card .dim{font-size:.82rem;font-weight:600;letter-spacing:0;text-transform:none;color:var(--cs-text2)}
.cs-card>div:last-child{font-size:1.65rem!important;font-weight:700;line-height:1.15;font-variant-numeric:tabular-nums}
.cs-card.ctx>div:last-child{font-size:1rem!important;font-weight:500;line-height:1.35}
.cs-card::after{content:"";position:absolute;top:14px;right:14px;width:26px;height:26px;background:var(--rail);
  -webkit-mask:var(--shape) center/contain no-repeat;mask:var(--shape) center/contain no-repeat}
.cs-card[data-state="NORMAL"]{--shape:url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='white' stroke-width='2'/%3E%3C/svg%3E")}
.cs-card[data-state="WATCH"]{--shape:url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2.5 21.5 12 12 21.5 2.5 12Z' fill='none' stroke='white' stroke-width='2' stroke-linejoin='round'/%3E%3C/svg%3E")}
.cs-card[data-state="DEGRADED"]{--shape:url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 3 22 20.5H2Z' fill='none' stroke='white' stroke-width='2' stroke-linejoin='round'/%3E%3C/svg%3E")}
.cs-card[data-state="UNKNOWN"]{--shape:url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='3.5' y='3.5' width='17' height='17' rx='2' fill='none' stroke='white' stroke-width='2' stroke-dasharray='4 3'/%3E%3C/svg%3E")}
.cs-card.ctx{background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none}
.cs-card.ctx::after{opacity:.55}
.cs-action{margin:.5rem 0 .2rem;padding:.8rem 1.1rem;border-radius:14px;border:1px solid color-mix(in srgb,var(--cs-cyan) 45%,transparent);background:var(--cs-panel);font-size:1.12rem;font-weight:600}
.cs-kicker{letter-spacing:0;text-transform:none;background:none!important;border:0;padding:0}
.stButton>button{border-radius:10px;background:var(--cs-panel);font-weight:600;transition:transform 160ms var(--cs-ease),border-color 160ms var(--cs-ease)}
.stButton>button:hover:not(:disabled){transform:none;box-shadow:none!important}
.stButton>button:active:not(:disabled){transform:scale(.97)}
@media (prefers-reduced-motion:reduce){.stButton>button{transition:none}}
"""

def _uri(svg):
    return "url(\"data:image/svg+xml;utf8," + quote(svg) + "\")"


def _art(tk):
    """Decorative SVG art as CSS background images (st.html strips inline <svg>)."""
    ln, ln2, cy, ts, dp = tk["line_s"], tk["line_s2"], tk["cyan"], tk["trust_soft"], tk["deep"]
    lines = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="none" fill="none" stroke="%s" stroke-width="1">'
             '<path d="M-100 700 C 300 520, 700 820, 1200 420 S 1700 260, 1800 300"/>'
             '<path d="M-100 740 C 300 560, 700 860, 1200 460 S 1700 300, 1800 340"/>'
             '<path d="M-100 780 C 300 600, 700 900, 1200 500 S 1700 340, 1800 380"/></svg>') % ln
    rings = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-200 -200 400 400" fill="none" stroke="%s" stroke-width="1">'
             '<circle r="190" stroke-dasharray="2 9"/><circle r="140"/><circle r="92" stroke-dasharray="14 10"/><circle r="44"/>'
             '</svg>') % ln
    poly = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-250 -250 500 500" fill="none">'
            '<defs><radialGradient id="p" cx="38%%" cy="32%%" r="75%%"><stop offset="0" stop-color="%s" stop-opacity=".6"/>'
            '<stop offset="1" stop-color="%s" stop-opacity=".95"/></radialGradient></defs>'
            '<path d="M-60 -70 C 20 -120, 110 -60, 100 20 C 92 100, 10 120, -50 80 C -110 40, -110 -30, -60 -70 Z" fill="url(#p)"/>'
            '<g stroke="%s" stroke-width="1.3" stroke-linejoin="round"><polygon points="0,-210 170,-90 130,130 -40,200 -190,60 -150,-120"/>'
            '<polyline points="0,-210 20,10 130,130"/><polyline points="-150,-120 20,10 170,-90"/><polyline points="-190,60 20,10 -40,200"/>'
            '<polyline points="0,-210 -190,60"/><polyline points="170,-90 -40,200"/><polyline points="-150,-120 130,130"/></g></svg>') % (ts, dp, ln2)
    mark = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -24 40 48" fill="none" stroke="%s" stroke-width="1.7" stroke-linejoin="round">'
            '<polygon points="0,-22 11,-9 11,14 0,22 -11,14 -11,-9"/><polyline points="0,-22 0,22"/><polyline points="-11,-9 0,-1 11,-9"/></svg>') % cy
    return (".cs-bg .lines{background:%s center/100%% 100%% no-repeat}.cs-bg .rings{background:%s center/contain no-repeat}"
            ".cs-bg .poly{background:%s center/contain no-repeat}.cs-top .mark{width:34px;height:34px;flex:none;background:%s center/contain no-repeat}"
            % (_uri(lines), _uri(rings), _uri(poly), _uri(mark)))


def _tokens():
    d, t = THEME["design"], THEME
    return {
        "surface": t["surface"], "panel": t["panel"], "text": t["text"], "text2": t["text_secondary"], "cyan": t["interactive"],
        "trust": d["trust"], "trust_soft": d["trust_soft"], "deep": d["deep"], "warm": d["aurora_warm"],
        "glass": _rgba(t["panel"], 0.55), "thick": _rgba(t["panel"], 0.82), "line": _rgba(d["trust_soft"], 0.20),
        "hi": "rgba(255,255,255,0.09)",
        "trust_a": _rgba(d["trust"], 0.28), "cyan_a": _rgba(t["interactive"], 0.12),
        "trust_a2": _rgba(d["trust"], 0.55), "cyan_a2": _rgba(t["interactive"], 0.28), "warm_a": _rgba(d["aurora_warm"], 0.28),
        "text2_a": _rgba(t["text_secondary"], 0.55),
        "line_s": _rgba(d["trust_soft"], 0.35), "line_s2": _rgba(t["text"], 0.55),
    }


# ---------------------------------------------------------------- profile "fusion" (default from 15/11)
# Fusion of mock-up directions 1 (Pleats: light glass, white pleats, warm and cool light fields) and 3 (Monolith: wireframe
# cage around a dark stone). Built from M1's six reference images (docs/DESIGN_FUSION.md). One rule gives each parent a role:
#   light glass = context and calm; the dark stone surface = only what demands action now (CRITICAL: emergency, refused resume).
#   warm field strength = the day's highest criticality (calm / watch / critical); cool field = the link to the ground.
# Standalone CSS (does not reuse _CSS). Colours from theme.json -> fusion; fonts are local files (Fontshare licence, offline).
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def _asset(name):
    """C-Sync mark (brand/make_mark.py -> csync/ui/assets) as a data URI: st.html strips inline <svg>, not <img>."""
    with open(os.path.join(ASSETS, name), "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()


def _font(name):
    with open(os.path.join(FONTS, name), "rb") as f:
        return base64.b64encode(f.read()).decode()


def _shape(body, filled=True):
    paint = "" if filled else " fill='none' stroke='black' stroke-width='1.8' stroke-dasharray='3.4 2.6'"
    return _uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><g{paint}>{body}</g></svg>")


def _orbit(core, dot=None, ring_extra="", dashed=False):
    """C-Sync state glyph: the core keeps a distinct silhouette per state (circle / diamond / triangle / dashed square),
    the orbit says how far the crew member is from their own baseline ("in sync" -> drifting -> off the orbit). 15/11 · FAIT PAR L'IA."""
    ring = "<ellipse cx='16' cy='17' rx='14' ry='5.5' transform='rotate(-24 16 17)' fill='none' stroke='black' stroke-width='1.9'%s/>" % ring_extra
    body = ring + core + (f"<circle cx='{dot[0]}' cy='{dot[1]}' r='2.6'/>" if dot else "")
    return _uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='-1 0 35 33'>{body}</svg>")


_FUSION = Template(r"""
@font-face{font-family:"Clash Display";src:url(data:font/woff2;base64,$clash) format("woff2");font-weight:200 700;font-display:swap}
@font-face{font-family:Satoshi;src:url(data:font/woff2;base64,$satoshi) format("woff2");font-weight:300 900;font-display:swap}
:root{--f-paper:$paper;--f-ink:$ink;--f-ink2:$ink2;--f-stone:$stone;--f-stone2:$stone2;--f-cream:$cream;--f-cream2:$cream2;
 --f-warm:$warm;--f-warm2:$warm2;--f-cool:$cool;--f-lilac:$lilac;--f-cyan:$cyan;
 --f-normal:$l_normal;--f-watch:$l_watch;--f-degraded:$l_degraded;--f-unknown:$l_unknown;
 --f-d-watch:$d_watch;--f-d-degraded:$d_degraded;
 --f-glass:rgba(255,255,255,.58);--f-line:rgba(255,255,255,.95);--f-hair:rgba(20,22,24,.12);
 --f-ease:cubic-bezier(.23,1,.32,1);--f-warm-o:.18;
 --f-display:"Clash Display","Satoshi",system-ui,sans-serif;--f-text:Satoshi,-apple-system,"Segoe UI",system-ui,sans-serif}
html,body,[data-testid="stApp"]{color:var(--f-ink);font-family:var(--f-text);
 background:radial-gradient(560px 460px at 18% 22%,color-mix(in srgb,var(--f-warm) calc(var(--f-warm-o)*100%),transparent),transparent 72%),
  radial-gradient(420px 360px at 30% 10%,color-mix(in srgb,var(--f-warm2) calc(var(--f-warm-o)*90%),transparent),transparent 72%),
  radial-gradient(620px 560px at 88% 96%,color-mix(in srgb,var(--f-cool) 42%,transparent),transparent 72%),
  radial-gradient(460px 420px at 100% 70%,color-mix(in srgb,var(--f-lilac) 32%,transparent),transparent 72%),var(--f-paper);
 background-attachment:fixed}
[data-testid="stApp"]::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.85;
 background:repeating-linear-gradient(103deg,transparent 0 46px,rgba(255,255,255,.95) 46px 47.5px,transparent 47.5px 64px),
  repeating-linear-gradient(97deg,transparent 0 88px,rgba(255,255,255,.7) 88px 89px)}
[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stMain"],[data-testid="stBottomBlockContainer"]{background:transparent!important}
[data-testid="stMain"],[data-testid="stMainBlockContainer"]{position:relative;z-index:1}
[data-testid="stMainBlockContainer"]{max-width:1200px;padding-top:1.1rem}
[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
p,li,label,[data-testid="stMarkdownContainer"]{font-family:var(--f-text);font-feature-settings:"tnum" 1}
h1,h2,h3,h4{font-family:var(--f-display)!important;font-weight:600!important;letter-spacing:-.015em;color:var(--f-ink)}
h3{font-size:clamp(1.4rem,2.4vw,1.95rem)!important;line-height:1.15!important;margin:.6rem 0 .8rem!important}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] *{color:var(--f-ink2)!important;opacity:1!important}
hr{border-color:var(--f-hair)!important;margin:1.4rem 0!important}
a{color:var(--f-stone);text-underline-offset:3px}

/* signature: the cage around the stone (direction 3), static, decorative */
.cs-top{position:relative;overflow:hidden}
.cs-cage{position:absolute;right:-6px;top:50%;width:150px;height:150px;transform:translateY(-50%);pointer-events:none;opacity:.9;
 background:$cage center/contain no-repeat}

/* top bar: light glass */
.cs-top{display:flex;align-items:center;gap:14px;padding:12px 18px;margin:0 0 12px;border-radius:22px;background:var(--f-glass);
 border:1px solid var(--f-line);box-shadow:inset 0 1px 0 #fff,0 18px 50px rgba(120,60,80,.10);-webkit-backdrop-filter:blur(26px) saturate(170%);backdrop-filter:blur(26px) saturate(170%)}
.cs-top .mark{width:30px;height:34px;flex:none;background:var(--f-ink);-webkit-mask:$mark center/contain no-repeat;mask:$mark center/contain no-repeat}
.cs-top .mk{width:44px;height:44px;flex:none;margin:-4px 0}.cs-top .mk-static{display:none}
.cs-top .nm{font-family:var(--f-display);font-weight:600;font-size:1.3rem}
.cs-top .tg{color:var(--f-ink2);font-size:.88rem}

/* alerts: synthetic banner = amber outline chip; info = fixed sentence */
[data-testid="stAlert"]{border-radius:16px}
[data-testid="stAlert"] [data-baseweb="notification"],[data-testid="stAlertContainer"]{background:rgba(255,255,255,.72)!important;border:1px solid var(--f-hair)!important;border-radius:16px!important}
[data-testid="stAlert"] p{color:var(--f-ink)!important;font-weight:600}

/* slider and native controls */
[data-testid="stSlider"]{padding:.45rem 1rem .25rem;border-radius:18px;background:var(--f-glass);border:1px solid var(--f-line);
 -webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px)}
.stButton>button{border-radius:999px;font-weight:600;padding:.5rem 1.25rem;border:1px solid var(--f-hair);background:rgba(255,255,255,.85);color:var(--f-ink);
 transition:transform 160ms var(--f-ease),background-color 160ms var(--f-ease)}
.stButton>button:active:not(:disabled){transform:scale(.97)}
.stButton>button:focus-visible{outline:2px solid var(--f-stone);outline-offset:3px}

/* state cards: light glass, big state word, one filled shape per state (circle, diamond, triangle, dashed square) */
[data-testid="stHorizontalBlock"]{margin-bottom:.8rem}
.cs-card{position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;gap:10px;min-height:178px;
 padding:16px 18px;border-radius:26px;background:var(--f-glass);border:1px solid var(--f-line);
 box-shadow:inset 0 1px 0 #fff,0 1px 2px rgba(20,22,24,.04),0 22px 56px rgba(120,60,80,.10);-webkit-backdrop-filter:blur(26px) saturate(170%);backdrop-filter:blur(26px) saturate(170%)}
.cs-card[data-state="NORMAL"]{--c:var(--f-normal);--s:$o_normal}
.cs-card[data-state="WATCH"]{--c:var(--f-watch);--s:$o_watch}
.cs-card[data-state="DEGRADED"]{--c:var(--f-degraded);--s:$o_degraded;background:linear-gradient(160deg,rgba(255,255,255,.7),rgba(255,232,226,.72))}
.cs-card[data-state="UNKNOWN"]{--c:var(--f-unknown);--s:$o_unknown}
.cs-card::after{content:"";position:absolute;right:12px;top:10px;width:52px;height:52px;background:var(--c);
 -webkit-mask:var(--s) center/contain no-repeat;mask:var(--s) center/contain no-repeat}
.cs-card .dim{color:var(--f-ink2);font-size:.9rem;font-weight:600}
.cs-card>div:nth-child(2){color:var(--c)!important;font-family:var(--f-display);font-weight:600;font-size:clamp(1.5rem,2.3vw,2.15rem)!important;line-height:1.05;letter-spacing:-.015em}
.cs-card.ctx{background:rgba(255,255,255,.22);box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none;border:1.5px dashed rgba(86,99,106,.62)}
.cs-card.ctx>div:nth-child(2),.cs-card[data-state="UNKNOWN"]>div:nth-child(2){color:var(--f-ink2)!important;font-family:var(--f-text);font-size:.98rem!important;font-weight:500;line-height:1.3;letter-spacing:0}
.cs-card[data-state="UNKNOWN"]:not(.ctx){border:1.5px dashed rgba(86,99,106,.62);background:rgba(255,255,255,.4)}

/* panels */
[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"]{background:var(--f-glass)!important;border:1px solid var(--f-line)!important;border-radius:22px!important;
 box-shadow:inset 0 1px 0 #fff,0 18px 46px rgba(120,60,80,.08);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px)}
.cs-action{margin:.5rem 0 .2rem;padding:.85rem 1.15rem;border-radius:16px;background:rgba(255,255,255,.85);border:1.5px solid var(--f-ink);font-size:1.08rem;font-weight:600;color:var(--f-ink)}
.cs-kicker{display:inline-flex;align-items:center;gap:8px;padding:4px 12px 4px 10px;border-radius:999px;font-size:.88rem;font-weight:700}
.cs-kicker::before{content:"";width:13px;height:12px;background:currentColor;-webkit-mask:$s_degraded center/contain no-repeat;mask:$s_degraded center/contain no-repeat}

/* the stone: CRITICAL only (emergency, resume request). Dark surface, cream text, state colours of the dark theme. */
.st-key-cs-stone{background:
  radial-gradient(1px 1px at 12% 18%,rgba(244,240,228,.55),transparent 60%),radial-gradient(1px 1px at 37% 9%,rgba(244,240,228,.4),transparent 60%),
  radial-gradient(1.5px 1.5px at 63% 22%,rgba(244,240,228,.5),transparent 60%),radial-gradient(1px 1px at 88% 14%,rgba(244,240,228,.45),transparent 60%),
  radial-gradient(1px 1px at 79% 41%,rgba(244,240,228,.3),transparent 60%),radial-gradient(1.5px 1.5px at 94% 63%,rgba(244,240,228,.4),transparent 60%),
  radial-gradient(1px 1px at 6% 72%,rgba(244,240,228,.35),transparent 60%),radial-gradient(1px 1px at 52% 88%,rgba(244,240,228,.3),transparent 60%),
  radial-gradient(260px 160px at 100% 0%,rgba(11,110,133,.28),transparent 70%),
  radial-gradient(1px 1px,rgba(244,240,228,.16) 50%,transparent 51%) 0 0/37px 41px,
  radial-gradient(1px 1px,rgba(244,240,228,.10) 50%,transparent 51%) 17px 23px/53px 47px,var(--f-stone)!important;border-radius:30px;padding:26px 28px 22px!important;color:var(--f-cream);
 box-shadow:0 0 0 1px color-mix(in srgb,var(--f-d-degraded) 45%,transparent),0 30px 80px rgba(20,24,40,.28)}
.st-key-cs-stone *{color:var(--f-cream)}
.st-key-cs-stone h3{color:var(--f-cream)!important}
.st-key-cs-stone [data-testid="stCaptionContainer"],.st-key-cs-stone [data-testid="stCaptionContainer"] *{color:var(--f-cream2)!important}
.st-key-cs-stone .cs-kicker{background:var(--f-d-degraded);color:var(--f-stone)!important}
.st-key-cs-stone .cs-kicker *{color:var(--f-stone)!important}
.st-key-cs-stone a{color:var(--f-cyan)!important}
.st-key-cs-stone [data-testid="stVerticalBlockBorderWrapper"],.st-key-cs-stone [data-testid="stExpander"]{background:var(--f-stone2)!important;border:1px solid rgba(244,240,228,.16)!important;box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none}
.st-key-cs-stone [data-testid="stAlert"] [data-baseweb="notification"],.st-key-cs-stone [data-testid="stAlertContainer"]{background:rgba(244,240,228,.08)!important;border:1px solid rgba(244,240,228,.22)!important}
.st-key-cs-stone [data-testid="stAlert"] p{color:var(--f-cream)!important}
.st-key-cs-stone .stButton>button{background:transparent;color:var(--f-cream);border:1px solid rgba(244,240,228,.4)}
.st-key-cs-stone .stButton>button p{color:inherit!important}
.st-key-cs-stone .stButton>button:disabled{opacity:.5}
.st-key-cs-stone [data-testid="stRadio"] label,.st-key-cs-stone [data-testid="stRadio"] p{color:var(--f-cream)!important}
.st-key-cs-stone .cs-decision{display:inline-block;margin:6px 0 2px;padding:10px 18px;border-radius:14px;font-family:var(--f-display);font-size:1.5em;font-weight:600;
 background:rgba(244,240,228,.06);border:1px solid rgba(244,240,228,.2)}
.st-key-cs-stone .cs-decision,.st-key-cs-stone .cs-decision *{color:inherit}
.st-key-cs-stone hr{border-color:rgba(244,240,228,.18)!important}
[data-testid="stCode"],.st-key-cs-stone pre{background:rgba(0,0,0,.25)!important}

/* shapes as classes (trajectory nodes, card history) */
.sh-NORMAL{--c:var(--f-normal);--s:$s_normal}.sh-WATCH{--c:var(--f-watch);--s:$s_watch}
.sh-DEGRADED{--c:var(--f-degraded);--s:$s_degraded}.sh-UNKNOWN{--c:var(--f-unknown);--s:$s_unknown}
/* mission strip: corner metadata + orbital trajectory (refs Lunar, 21 Grams) */
.cs-strip{position:relative;margin:2px 0 14px;padding:14px 22px 10px;border-radius:22px;background:var(--f-glass);border:1px solid var(--f-line);
 box-shadow:inset 0 1px 0 #fff,0 18px 46px rgba(120,60,80,.08);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px)}
.cs-strip .meta{display:flex;justify-content:space-between;gap:16px;font-size:.78rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--f-ink2)}
.cs-strip .meta b{color:var(--f-ink);font-weight:700}.cs-strip .meta .down{color:var(--f-watch)}
.cs-orbit{position:relative;height:104px;margin:6px 0 2px}
.cs-orbit .arc{position:absolute;left:0;right:0;top:12px;height:148px;border:1px solid rgba(20,22,24,.22);border-radius:50%;
 -webkit-mask:linear-gradient(#000 0,#000 50%,transparent 50%);mask:linear-gradient(#000 0,#000 50%,transparent 50%)}
.cs-orbit .nd{position:absolute;width:16px;height:16px;transform:translate(-50%,-50%);background:var(--c);-webkit-mask:var(--s) center/contain no-repeat;mask:var(--s) center/contain no-repeat}
.cs-orbit .nd.now{width:26px;height:26px}
.cs-orbit .halo{position:absolute;width:44px;height:44px;transform:translate(-50%,-50%);border-radius:50%;border:1px solid rgba(20,22,24,.35)}
.cs-orbit .evt{position:absolute;width:30px;height:30px;transform:translate(-50%,-50%);border-radius:50%;border:1.5px solid var(--f-degraded)}
.cs-orbit .dn{position:absolute;transform:translate(-50%,0);font-size:.78rem;font-variant-numeric:tabular-nums;color:var(--f-ink2)}
.cs-orbit .dn.now{color:var(--f-ink);font-weight:700}
.cs-orbit .nd.fut{width:7px;height:7px;border-radius:50%;background:rgba(20,22,24,.28);-webkit-mask:none;mask:none}
.cs-orbit .tag{position:absolute;transform:translate(-50%,0);font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
.cs-orbit .tag.crit{color:var(--f-degraded)}.cs-orbit .tag.base{color:var(--f-ink2)}
.cs-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
/* card history: one small shape per day (ref Flutter: stacked layers = time) */
.cs-card .hist{display:flex;gap:4px;align-items:center;position:relative;z-index:1}
.cs-card .hist i{width:9px;height:9px;background:var(--c);-webkit-mask:var(--s) center/contain no-repeat;mask:var(--s) center/contain no-repeat;opacity:.9}
.cs-card .hist i.fut{background:rgba(20,22,24,.14);-webkit-mask:none;mask:none;border-radius:50%;width:5px;height:5px}
.cs-card .hist i.now{width:13px;height:13px;opacity:1}
/* habitat section (real NASA data): glass panel, chart legible on light */
.st-key-cs-habitat{background:var(--f-glass)!important;border:1px solid var(--f-line);border-radius:26px;padding:20px 22px 12px!important;
 box-shadow:inset 0 1px 0 #fff,0 18px 46px rgba(40,80,110,.08);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px)}
.st-key-cs-habitat h3::before{content:"NASA DATA";display:inline-block;vertical-align:middle;margin-right:10px;padding:3px 8px;border-radius:6px;
 font-family:var(--f-text);font-size:.7rem;font-weight:800;letter-spacing:.1em;background:var(--f-stone);color:var(--f-cream)}
/* 1 % pass: nested radii (outer - padding), one type ramp, tabular figures */
.st-key-cs-stone [data-testid="stVerticalBlockBorderWrapper"]{border-radius:18px!important}
[data-testid="stMarkdownContainer"] p{line-height:1.55}
[data-testid="stDataFrame"]{border-radius:14px;overflow:hidden}
@media (max-width:900px){.cs-orbit .tag{display:none}}
/* motion and transparency fallbacks */
@media (prefers-reduced-motion:reduce){.stButton>button{transition:none}.cs-top .mk-anim{display:none}.cs-top .mk-static{display:block}}
@media (prefers-reduced-transparency:reduce){
 .cs-top,.cs-card,.cs-strip,.st-key-cs-habitat,[data-testid="stSlider"],[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"]{-webkit-backdrop-filter:none!important;backdrop-filter:none!important;background:#fff!important}
 [data-testid="stApp"]::before{display:none}}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.cs-top,.cs-card,[data-testid="stSlider"]{background:#fff!important}}
@media (max-width:760px){.cs-cage{opacity:.35}}

/* glass v2 (15/11, done by the AI design session): light that behaves like glass, not a white box.
   edge light (warm top-left, cool bottom-right) + soft specular sheen + fine grain. Meaning stays in the shapes; this is surface only. */
.cs-card,.cs-top,[data-testid="stSlider"]{--g-noise:url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxNjAnIGhlaWdodD0nMTYwJz48ZmlsdGVyIGlkPSduJz48ZmVUdXJidWxlbmNlIHR5cGU9J2ZyYWN0YWxOb2lzZScgYmFzZUZyZXF1ZW5jeT0nLjknIG51bU9jdGF2ZXM9JzInIHN0aXRjaFRpbGVzPSdzdGl0Y2gnLz48ZmVDb2xvck1hdHJpeCB2YWx1ZXM9JzAgMCAwIDAgLjIgIDAgMCAwIDAgLjIgIDAgMCAwIDAgLjI1ICAwIDAgMCAuNTUgMCcvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEwMCUnIGZpbHRlcj0ndXJsKCNuKScvPjwvc3ZnPg==")}
.cs-card:not(.ctx),.cs-top{background-image:linear-gradient(135deg,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 38%),var(--g-noise);background-blend-mode:normal,soft-light;
 box-shadow:inset 1.5px 1.5px 0 rgba(255,255,255,.95),inset -1px -1px 0 rgba(100,218,244,.35),inset 0 0 24px rgba(255,255,255,.35),0 1px 2px rgba(20,22,24,.04),0 26px 60px rgba(120,60,80,.12);
 -webkit-backdrop-filter:blur(28px) saturate(180%) brightness(1.04);backdrop-filter:blur(28px) saturate(180%) brightness(1.04)}
.cs-card[data-state="DEGRADED"]{background-image:linear-gradient(135deg,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 38%),linear-gradient(160deg,rgba(255,255,255,.7),rgba(255,232,226,.72)),var(--g-noise)}
.cs-card:not(.ctx)::before{content:"";position:absolute;left:-30%;top:-60%;width:90%;height:120%;pointer-events:none;transform:rotate(18deg);
 background:radial-gradient(closest-side,rgba(255,255,255,.55),rgba(255,255,255,0));opacity:.55}
.cs-card:not(.ctx):hover{box-shadow:inset 1.5px 1.5px 0 #fff,inset -1px -1px 0 rgba(247,114,86,.4),inset 0 0 28px rgba(255,255,255,.45),0 30px 70px rgba(120,60,80,.16);transition:box-shadow .3s}
@media (prefers-reduced-transparency:reduce){.cs-card:not(.ctx),.cs-top{background-image:none;background-color:#FFFFFF}.cs-card:not(.ctx)::before{display:none}}
""")

_FIELD = {"calm": ".06", "watch": ".22", "critical": ".62"}


def _fusion_css():
    f, t = THEME["fusion"], THEME
    lo = f["state_on_light"]
    cage = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='-250 -250 500 500' fill='none'>"
            "<defs><radialGradient id='p' cx='38%' cy='32%' r='75%'><stop offset='0' stop-color='" + f["stone2"] + "'/>"
            "<stop offset='1' stop-color='" + f["stone"] + "'/></radialGradient></defs>"
            "<path d='M-60 -70 C 20 -120, 110 -60, 100 20 C 92 100, 10 120, -50 80 C -110 40, -110 -30, -60 -70 Z' fill='url(#p)'/>"
            "<g stroke='" + f["stone"] + "' stroke-width='1.3' stroke-linejoin='round'><polygon points='0,-210 170,-90 130,130 -40,200 -190,60 -150,-120'/>"
            "<polyline points='0,-210 20,10 130,130'/><polyline points='-150,-120 20,10 170,-90'/><polyline points='-190,60 20,10 -40,200'/>"
            "<polyline points='0,-210 -190,60'/><polyline points='170,-90 -40,200'/><polyline points='-150,-120 130,130'/></g></svg>")
    mark = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='-20 -24 40 48' fill='none' stroke='black' stroke-width='1.7' stroke-linejoin='round'>"
            "<polygon points='0,-22 11,-9 11,14 0,22 -11,14 -11,-9'/><polyline points='0,-22 0,22'/><polyline points='-11,-9 0,-1 11,-9'/></svg>")
    return _FUSION.substitute(
        clash=_font("ClashDisplay-Variable.woff2"), satoshi=_font("Satoshi-Variable.woff2"),
        paper=f["paper"], ink=f["ink"], ink2=f["ink2"], stone=f["stone"], stone2=f["stone2"], cream=f["cream"], cream2=f["cream2"],
        warm=f["warm"], warm2=f["warm2"], cool=f["cool"], lilac=f["lilac"], cyan=t["interactive"],
        l_normal=lo["NORMAL"], l_watch=lo["WATCH"], l_degraded=lo["DEGRADED"], l_unknown=lo["UNKNOWN"],
        d_watch=t["state"]["WATCH"]["color"], d_degraded=t["state"]["DEGRADED"]["color"],
        cage=_uri(cage), mark=_uri(mark),
        s_normal=_shape("<circle cx='12' cy='12' r='10'/>"), s_watch=_shape("<path d='M12 1.5 22.5 12 12 22.5 1.5 12Z'/>"),
        s_degraded=_shape("<path d='M12 2 22.6 21H1.4Z'/>"),
        s_unknown=_shape("<rect x='2' y='2' width='20' height='20' rx='2'/>", filled=False),
        o_normal=_orbit("<circle cx='16' cy='16' r='6'/>", dot=(27.2, 9.9)),
        o_watch=_orbit("<path d='M16 9.6 22.4 16 16 22.4 9.6 16Z'/>", dot=(28.4, 9.2), ring_extra=" pathLength='100' stroke-dasharray='86 6 8 0'"),
        o_degraded=_orbit("<path d='M16 9.2 22.2 20.2H9.8Z'/>", dot=(29.5, 8.5), ring_extra=" pathLength='100' stroke-dasharray='58 16 26 0'"),
        o_unknown=_orbit("<rect x='10.5' y='10.5' width='11' height='11' rx='1.5' fill='none' stroke='black' stroke-width='1.8' stroke-dasharray='3 2.4'/>", ring_extra=" stroke-dasharray='3 3' opacity='.7'"))


def field(level):
    """Fusion profile only: the warm light field follows the day's highest criticality (calm, watch, critical)."""
    if _profile() == "fusion":
        st.html("<style>:root{--f-warm-o:%s}</style>" % _FIELD.get(level, _FIELD["calm"]))


def _profile():
    return os.environ.get("CSYNC_STYLE", "fusion")


def inject(name, tag):
    """Call once, right after set_page_config. st.html keeps the CSS out of the markdown stream."""
    tk = _tokens()
    style = _profile()
    if style == "fusion":
        st.html("<style>" + _fusion_css() + "</style>")
        st.html("<header class='cs-top'>"
                f"<img class='mk mk-anim' alt='' aria-hidden='true' src='{_asset('csync_mark_animated.svg')}'>"
                f"<img class='mk mk-static' alt='' aria-hidden='true' src='{_asset('csync_mark_static.svg')}'>"
                f"<div><div class='nm'>{name}</div><div class='tg'>{tag}</div></div></header>")
        return
    extra = {"quiet": _QUIET, "hybrid": _HYBRID, "calm": _CALM, "signal": _SIGNAL}.get(style, "")
    st.html("<style>" + _CSS % tk + _art(tk) + extra + "</style>" + _SHAPES)
    st.html(_TOP % {**tk, "name": name, "tag": tag})


def card_vars(colour):
    """Inline custom properties for a state card (the colour is one of the theme state colours)."""
    return f"--rail:{colour};--rail-a:{_rgba(colour, 0.14)}"



# ---------------------------------------------------------------- fusion helpers used by app.py (appearance only)
_RANK = {"UNKNOWN": 0, "NORMAL": 1, "WATCH": 2, "DEGRADED": 3}


def worst(states):
    """Highest state among the evaluated dimensions of one day (for the trajectory node)."""
    vals = [v for k, v in states.items() if k in ("Body", "Attention", "Morale")]
    return max(vals, key=lambda v: _RANK.get(v, 0)) if vals else "UNKNOWN"


def chart_colors(theme):
    """Habitat chart colours: legible on the light glass for the fusion profile (graphics >= 3:1)."""
    if _profile() == "fusion":
        c = theme["fusion"]["chart"]
        return [c["series"], c["limit"], c["flagged"]]
    return [theme["interactive"], theme["text_secondary"], theme["state"]["UNKNOWN"]["color"]]


def history(states_by_day, dim, day, n_days=10):
    """Fusion only: a row of small shapes, one per day up to `day` (the drift becomes visible), dots for days to come."""
    if _profile() != "fusion":
        return ""
    cells = []
    for d in range(1, n_days + 1):
        if d > day:
            cells.append("<i class='fut'></i>")
        else:
            s = states_by_day.get(d, {}).get(dim, "UNKNOWN")
            cells.append(f"<i class='sh-{s}{' now' if d == day else ''}'></i>")
    return f"<div class='hist' aria-hidden='true'>{''.join(cells)}</div>"


def mission_strip(ui, states_by_day, events, day, link, delay_min, n_days=10):
    """Fusion only: corner metadata and an orbital trajectory of the mission (one node per day, shaped by its highest state)."""
    if _profile() != "fusion":
        return
    import math
    nodes, labels = [], []
    for d in range(1, n_days + 1):
        x = 4 + (d - 1) * 92 / (n_days - 1)
        y = 12 + 74 - 74 * math.sqrt(max(0.0, 1 - ((x - 50) / 50) ** 2))   # on the ellipse drawn by .arc
        now = " now" if d == day else ""
        if d > day:   # days to come: planned trajectory only, no state, no event (the screen never shows the future)
            nodes.append(f"<span class='nd fut' style='left:{x:.2f}%;top:{y:.1f}px'></span>")
            labels.append(f"<span class='dn fut' style='left:{x:.2f}%;top:{y + 14:.1f}px'>{d}</span>")
            continue
        s = worst(states_by_day.get(d, {}))
        lab = ui["node_label"].format(d=d, state=s.title())
        if d == day:
            nodes.append(f"<span class='halo' style='left:{x:.2f}%;top:{y:.1f}px'></span>")
        if d in events:
            nodes.append(f"<span class='evt' style='left:{x:.2f}%;top:{y:.1f}px'></span>")
            labels.append(f"<span class='tag crit' style='left:{x:.2f}%;top:{y - 40:.1f}px'>{events[d]}</span>")
        nodes.append(f"<span class='nd sh-{s}{now}' role='img' aria-label='{lab}' style='left:{x:.2f}%;top:{y:.1f}px'></span>")
        labels.append(f"<span class='dn{now}' style='left:{x:.2f}%;top:{y + 14:.1f}px'>{d}</span>")
    xb = 4 + 2 * 92 / (n_days - 1)
    labels.append(f"<span class='tag base' style='left:{xb:.2f}%;top:{12 + 74 - 74 * math.sqrt(1 - ((xb - 50) / 50) ** 2) + 32:.1f}px'>{ui['baseline_short']} 1–5</span>")
    link_txt = (f"<span class='down'>{ui['link_status_down'].format(a=link[0], b=link[1])}</span>" if link else ui["link_status_ok"])
    st.html(
        f"<section class='cs-strip' aria-label='{ui['trajectory_label']}'>"
        f"<div class='meta'><span><b>{ui['mission_name']}</b> · {ui['day_of'].format(d=day, n=n_days)}</span>"
        f"<span>{link_txt} · {ui['ground_delay'].format(m=delay_min)}</span></div>"
        f"<div class='cs-orbit'><div class='arc'></div>{''.join(nodes)}{''.join(labels)}</div></section>")
