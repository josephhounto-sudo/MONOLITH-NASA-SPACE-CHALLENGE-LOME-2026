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
 -webkit-backdrop-filter:none!important;backdrop-filter:none!important}}
:root{{--cs-accent:#FF8A4C}}
/* no blur on the main panel: it is 90-95 % opaque (blur invisible) and a backdrop-filter traps fixed children such as Pip's corner */
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
[data-testid="stMetricValue"],[data-testid="stMetricValue"] *,.cs-num,.cs-live .v,.cs-clock .t{{font-family:Doto,monospace!important;font-weight:700!important;letter-spacing:.02em}}
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
[data-testid="stPills"] button,[data-testid="stButtonGroup"] button{{background:rgba(255,253,253,.08)!important;border:1px solid rgba(255,253,253,.22)!important;color:{INK}!important;border-radius:999px!important}}
[data-testid="stButtonGroup"] button[aria-checked="true"],[data-testid="stButtonGroup"] button[kind$="Active"]{{background:{INK}!important;color:{SMOKE_DARK}!important}}
[data-testid="stButtonGroup"] button[aria-checked="true"] *,[data-testid="stButtonGroup"] button[kind$="Active"] *{{color:{SMOKE_DARK}!important}}
.st-key-cs-weekcard{{border-radius:44px;padding:22px 24px 14px;margin:6px 0 18px;
 background:radial-gradient(70% 60% at 60% 35%,rgba(215,154,118,.30),transparent 70%),linear-gradient(180deg,rgba(124,115,110,.55),rgba(46,38,33,.92) 55%)!important;
 border:1px solid rgba(255,253,253,.22);box-shadow:inset 1px 1px 0 rgba(255,253,253,.20),0 30px 70px rgba(0,0,0,.35)}}
.cs-wk-h b{{display:block;font-size:1.5rem;font-weight:500}} .cs-wk-h span{{font-size:.95rem}}
.st-key-cs-weekcard [data-testid="stButtonGroup"],.st-key-cs-weekcard [data-testid="stElementContainer"]:has([data-testid="stButtonGroup"]){{width:100%!important;max-width:none!important}}
.st-key-cs-weekcard [data-testid="stButtonGroup"] [role="radiogroup"]{{display:flex!important;flex-wrap:nowrap!important;justify-content:space-between!important;
 width:100%!important;max-width:none!important;padding:0 7.5% 0 0;box-sizing:border-box;gap:4px}}
.st-key-cs-weekcard [data-testid="stPills"] button,.st-key-cs-weekcard [data-testid="stButtonGroup"] button{{width:46px;height:46px;min-width:46px;padding:0!important;justify-content:center;
 background:rgba(255,253,253,.04)!important;border:1px solid rgba(255,253,253,.35)!important}}
.st-key-cs-weekcard [data-testid="stButtonGroup"] button[aria-checked="true"]{{background:{INK}!important;color:{SMOKE_DARK}!important;box-shadow:0 0 22px rgba(255,253,253,.35)}}
.st-key-cs-weekcard [data-testid="stButtonGroup"] button[aria-checked="true"] *{{color:{SMOKE_DARK}!important}}
.st-key-cs-weekcard [data-testid^="stBaseButton"]{{width:44px;height:44px;min-height:44px;padding:0!important;border-radius:999px!important}}
.cs-wk-v{{display:flex;align-items:baseline;gap:10px;margin:4px 0 0}} .cs-wk-v .cs-num{{font-size:44px;line-height:1}}
.cs-wk-n{{font-size:.92rem;margin:.3em 0 0}} .cs-wk-r{{text-align:center;font-size:1.05rem;margin:.55em 0 0}}
/* on a computer the navigation stays open: on the hosted app a collapsed sidebar (remembered by the browser) came back
   with no button to reopen it (seen 20/11/2026 06:50 UTC); phones keep their close button */
@media (min-width:900px){{[data-testid="stSidebarCollapseButton"]{{display:none!important}}}}
/* operations bar: three telemetry fields + flat timeline (replaces the decorative orbit) */
.cs-ops{{padding:14px 18px 16px!important}}
.cs-ops .ops{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:12px}}
.cs-ops .ops>div{{border-radius:999px;padding:8px 16px;background:rgba(255,253,253,.06);border:1px solid rgba(255,253,253,.16);display:flex;flex-direction:column;min-width:0}}
.cs-ops .ops small{{font-size:12.5px;opacity:.9}} .cs-ops .ops b{{font-family:Doto,monospace;font-weight:700;font-size:18px;letter-spacing:.02em}}
.cs-ops .ops b.down{{color:#F2C14E;font-family:inherit;font-size:14px}} .cs-ops .ops i{{font-style:normal;font-size:12.5px}}
.cs-ops .tl{{position:relative;height:74px;margin:0 2px}}
.cs-ops .tl::before{{content:"";position:absolute;left:0;right:0;top:34px;height:2px;background:rgba(255,253,253,.18);border-radius:2px}}
.cs-ops .tl .base{{position:absolute;top:0;height:20px;border-top:2px solid rgba(255,253,253,.35);font-size:12.5px;padding-top:2px;text-align:center}}
.cs-ops .tl .nowline{{position:absolute;top:18px;bottom:6px;width:2px;margin-left:-1px;background:{INK};box-shadow:0 0 12px {CURVE}}}
.cs-ops .tl .nd{{position:absolute;top:27px;width:16px;height:16px;margin-left:-8px;border-radius:999px;border:1px solid rgba(255,253,253,.5);background:rgba(255,253,253,.12)}}
.cs-ops .tl .nd.fut{{background:transparent;border-style:dashed;opacity:.6}}
.cs-ops .tl .nd.sh-NORMAL{{background:#4CD6A0;border-color:#4CD6A0}} .cs-ops .tl .nd.sh-WATCH{{background:#F2C14E;border-color:#F2C14E}}
.cs-ops .tl .nd.sh-DEGRADED{{background:#FF6B5B;border-color:#FF6B5B}}
.cs-ops .tl .nd.now{{box-shadow:0 0 0 5px rgba(255,253,253,.18),0 0 18px {CURVE}}}
.cs-ops .tl .dn{{position:absolute;top:48px;transform:translateX(-50%);font-family:Doto,monospace;font-weight:700;font-size:14px}}
.cs-ops .tl .dn.now{{color:{INK}}} .cs-ops .tl .dn.fut{{opacity:.55}}
.cs-ops .tl .tag{{position:absolute;top:2px;transform:translateX(-50%);font-size:12px;font-weight:700;padding:1px 8px;border-radius:999px;background:#FF6B5B;color:#2E2621}}
@media (max-width:640px){{.cs-ops .ops{{grid-template-columns:1fr}} .cs-ops .ops>div{{border-radius:22px}}}}
.cs-dot.on{{background:{INK}!important;color:{SMOKE_DARK}!important}}
.cs-dots{{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 6px}}
.cs-dot{{min-width:30px;height:30px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font-family:Doto,monospace;font-weight:700;font-size:14px;border:1px solid rgba(255,253,253,.28)}}
.cs-card.ctx{{background:rgba(34,27,23,.86)!important;border:1.5px dashed rgba(255,253,253,.38)!important}}
"""


NAV_ICONS = {"tab_home": "house", "tab_cmd": "users", "tab_body": "person-standing", "tab_env": "wind", "tab_trends": "activity",
             "tab_tech": "cpu", "tab_scale": "grid-3x3", "tab_why": "circle-help", "tab_nasa": "rocket", "tab_try": "hand",
             "tab_sources": "book-open", "tab_live": "radio", "tab_emergency": "siren", "role_crew": "person-standing", "role_cmd": "users"}


def nav_css(ui: dict, nav_keys: list[str], role_keys: list[str], group_starts: dict[int, str] | None = None) -> str:
    """One icon per sidebar entry, in the order actually shown (the order changes with the role); a small group title
    above the first entry of each group (group_starts: {1-based position: title})."""
    assert nav_keys and role_keys
    rules = []
    for i, title in (group_starts or {}).items():
        assert 1 <= i <= len(nav_keys) and '"' not in title
        rules.append(f'.st-key-cs-nav [role="radiogroup"]>div:nth-of-type({i})::before{{content:"{title}";display:block;margin:{18 if i > 1 else 4}px 0 6px 12px;'
                     'font-size:.74rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;opacity:.8}')
    for group, keys in (("cs-nav", nav_keys), ("cs-role", role_keys)):
        for i, k in enumerate(keys[:20], start=1):
            ico = _uri(lucide(NAV_ICONS[k]))
            rules.append(f'.st-key-{group} [role="radiogroup"]>div:nth-of-type({i}) [data-testid="stRadioOption"]{{--ico:url("{ico}")}}')
    return "\n".join(rules)
