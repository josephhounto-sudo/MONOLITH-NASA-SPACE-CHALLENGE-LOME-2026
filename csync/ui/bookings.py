"""V3 look: the "Bookings Per Day" reference (decision of Joseph, 20/11/2026), measured on its pixels (docs/PLAN_V3.md §2).

Cream page with a soft grain, a dark blurred planet limb and orange halos; the content sits in one smoky glass panel that stays
dark under every line of text (luminance <= 0.07, rule measured on the reference itself: its white text on orange is 2.9:1).
Pills carry the category glow on their right edge, away from the text. Doto (dot font, OFL) is used for every number.

Icons: Lucide (lucide-static 0.460.0, ISC licence, notice in THIRD_PARTY_NOTICES.md), files in csync/ui/assets/lucide/.
"""
from __future__ import annotations

import base64
import os
import re

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "lucide")

# measured on the reference (PIL quantisation, 20/11/2026)
CREAM, SMOKE_DARK, SMOKE, INK = "#F5F0ED", "#2E2621", "#4B4039", "#FFFDFD"
CATEGORY_GLOW = {"Body": "#E98F6D", "Attention": "#CF783C", "Morale": "#E3B08F", "Mission": "#B7A79B", "Habitat": "#D79A76"}
CURVE = "#D79A76"

_GRAIN = ("<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' "
          "baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .18 0 0 0 0 .13 0 0 0 0 .1 0 0 0 .55 0'/>"
          "</filter><rect width='100%' height='100%' filter='url(#n)'/></svg>")


def _uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


def lucide(name: str) -> str:
    """Raw SVG markup of one vendored Lucide icon. Raises FileNotFoundError for an icon that was not vendored."""
    path = os.path.join(ASSETS, name + ".svg")
    with open(path, encoding="utf-8") as fh:
        svg = fh.read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    assert svg.startswith("<svg") and svg.endswith("</svg>"), name
    return svg


def css() -> str:
    grain = _uri(_GRAIN)
    glow = "".join(f".cs-card[data-dim={k}]{{--g:{v}}}" for k, v in CATEGORY_GLOW.items())
    return f"""
html,body,[data-testid="stApp"]{{background:
 url("{grain}"),
 radial-gradient(70% 38% at 50% 112%,rgba(30,22,18,.92),rgba(30,22,18,.55) 55%,transparent 80%),
 radial-gradient(60% 18% at 50% 76%,rgba(207,120,60,.45),transparent 70%),
 radial-gradient(38% 30% at 12% 18%,rgba(233,143,109,.38),transparent 72%),
 radial-gradient(34% 34% at 92% 40%,rgba(197,97,47,.30),transparent 72%),
 {CREAM}!important;background-attachment:fixed!important}}
[data-testid="stMainBlockContainer"]{{max-width:1040px;margin:28px auto 40px;padding:28px 34px 34px!important;border-radius:44px;
 background:linear-gradient(180deg,rgba(75,64,57,.90),rgba(46,38,33,.93) 45%,rgba(34,27,23,.95))!important;
 border:1px solid rgba(255,253,253,.22);box-shadow:inset 1px 1px 0 rgba(255,253,253,.18),0 40px 90px rgba(46,38,33,.45);
 -webkit-backdrop-filter:blur(28px) saturate(130%);backdrop-filter:blur(28px) saturate(130%)}}
@media (max-width:640px){{[data-testid="stMainBlockContainer"]{{margin:10px 6px 24px;padding:18px 14px 22px!important;border-radius:30px}}}}
.cs-top,[data-testid="stSlider"],.cs-strip,.st-key-cs-habitat,[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"],.cs-ind{{
 background-color:rgba(46,38,33,.72)!important;border-color:rgba(255,253,253,.18)!important;border-radius:36px!important}}
.cs-card:not(.ctx){{border-radius:40px!important;background-color:rgba(43,35,30,.86)!important;
 background-image:radial-gradient(60% 90% at 104% 50%,color-mix(in srgb,var(--g,{CURVE}) 70%,transparent),transparent 70%),
 linear-gradient(135deg,rgba(255,253,253,.10),rgba(255,253,253,0) 40%)!important}}
{glow}
.cs-card .dim{{color:{INK}!important}}
.cs-card .dim::before{{background:var(--g,{CURVE})!important;width:10px!important;height:10px!important;box-shadow:0 0 12px var(--g,{CURVE})}}
.stButton>button[kind="primary"],.cs-action{{background:radial-gradient(circle at 50% 40%,#FFFBF5,#FFF2DA 60%,#F3D9B8)!important;color:{SMOKE_DARK}!important;
 border-radius:999px!important;box-shadow:0 0 0 6px rgba(255,242,218,.18),0 0 40px rgba(255,214,170,.55)!important}}
.stButton>button{{border-radius:999px!important}}
[data-testid="stMetricValue"],.cs-num,.cs-live .v,.cs-clock .t{{font-family:Doto,monospace!important;font-weight:700!important;letter-spacing:.02em}}
/* sidebar: light glass, dark ink, one Lucide icon per section, the chosen one is the white pill of the reference */
[data-testid="stSidebar"]{{background:rgba(245,240,237,.78)!important;border-right:1px solid rgba(46,38,33,.14)!important;
 -webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px)}}
[data-testid="stSidebar"] *{{color:{SMOKE_DARK}!important}}
[data-testid="stSidebar"] [role="radiogroup"]{{gap:4px}}
[data-testid="stSidebar"] [data-testid="stRadioOption"]{{padding:8px 12px 8px 42px!important;border-radius:999px;position:relative;margin:0!important;min-height:40px;align-items:center;width:100%}}
[data-testid="stSidebar"] [data-testid="stRadioOption"]>div>div:first-child:not([data-testid]){{display:none!important}}
[data-testid="stSidebar"] [data-testid="stRadioOption"]::before{{content:"";position:absolute;left:14px;top:50%;width:18px;height:18px;margin-top:-9px;
 background:{SMOKE_DARK};-webkit-mask:var(--ico) center/contain no-repeat;mask:var(--ico) center/contain no-repeat}}
[data-testid="stSidebar"] [role="radiogroup"]>[data-selected="true"] [data-testid="stRadioOption"]{{background:{INK};box-shadow:0 6px 18px rgba(46,38,33,.18),inset 0 0 0 1px rgba(46,38,33,.10)}}
[data-testid="stSidebar"] [data-testid="stRadioOption"]:hover{{background:rgba(255,253,253,.6)}}
[data-testid="stAlert"] [data-baseweb="notification"],[data-testid="stAlertContainer"]{{background:rgba(34,27,23,.92)!important;border:1px solid rgba(255,253,253,.22)!important;border-radius:28px!important}}
.cs-hooktl .bar{{background:rgba(255,253,253,.14)!important}}.cs-hooktl .out{{background:{CURVE}!important}}
.cs-card.ctx{{background:rgba(34,27,23,.86)!important;border:1.5px dashed rgba(255,253,253,.38)!important}}
"""


NAV_ICONS = {"tab_home": "house", "tab_cmd": "users", "tab_body": "person-standing", "tab_env": "wind", "tab_trends": "activity",
             "tab_tech": "cpu", "tab_scale": "grid-3x3", "tab_why": "circle-help", "tab_nasa": "rocket", "tab_try": "hand",
             "tab_sources": "book-open", "tab_live": "radio", "role_crew": "person-standing", "role_cmd": "users"}


def nav_css(ui: dict, nav_keys: list[str], role_keys: list[str]) -> str:
    """One icon per sidebar entry, in the order actually shown (the order changes with the role)."""
    assert nav_keys and role_keys
    rules = []
    for group, keys in (("cs-nav", nav_keys), ("cs-role", role_keys)):
        for i, k in enumerate(keys[:20], start=1):
            ico = _uri(lucide(NAV_ICONS[k]))
            rules.append(f'.st-key-{group} [role="radiogroup"]>div:nth-of-type({i}) [data-testid="stRadioOption"]{{--ico:url("{ico}")}}')
    return "\n".join(rules)
