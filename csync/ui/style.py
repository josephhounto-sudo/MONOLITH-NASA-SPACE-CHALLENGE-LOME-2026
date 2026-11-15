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
import json
import os
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


def inject(name, tag):
    """Call once, right after set_page_config. st.html keeps the CSS out of the markdown stream."""
    tk = _tokens()
    style = os.environ.get("CSYNC_STYLE", "hybrid")
    extra = {"quiet": _QUIET, "hybrid": _HYBRID, "calm": _CALM, "signal": _SIGNAL}.get(style, "")
    st.html("<style>" + _CSS % tk + _art(tk) + extra + "</style>" + _SHAPES)
    st.html(_TOP % {**tk, "name": name, "tag": tag})


def card_vars(colour):
    """Inline custom properties for a state card (the colour is one of the theme state colours)."""
    return f"--rail:{colour};--rail-a:{_rgba(colour, 0.14)}"
