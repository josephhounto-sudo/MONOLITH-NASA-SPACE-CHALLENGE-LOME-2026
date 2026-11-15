"""2026-11-15 ~07:30 (UTC) design-v2 | FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

Guard-rails for the "fusion" look (CSYNC_STYLE default): measured contrasts of the theme tokens, the stone-only-for-CRITICAL
rule, fonts shipped locally with their licence. Pixel-level contrast on the rendered app is measured separately
(docs/DESIGN_FUSION.md); this file only locks the tokens so a later edit cannot silently break them.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = json.load(open(os.path.join(ROOT, "csync", "config", "theme.json"), encoding="utf8"))
F = THEME["fusion"]


def lum(h):
    c = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def test_state_colours_on_light_glass_reach_4_5():
    for state, colour in F["state_on_light"].items():
        for bg in (F["paper"], F["glass"]):
            assert ratio(colour, bg) >= 4.5, (state, bg, round(ratio(colour, bg), 2))


def test_text_roles_on_light_and_on_stone():
    assert ratio(F["ink"], F["paper"]) >= 7 and ratio(F["ink2"], F["paper"]) >= 4.5
    assert ratio(F["cream"], F["stone"]) >= 7 and ratio(F["cream2"], F["stone"]) >= 4.5
    for state in ("WATCH", "DEGRADED"):   # dark-theme state colours are used on the stone surface
        assert ratio(THEME["state"][state]["color"], F["stone"]) >= 4.5, state
    assert ratio(THEME["interactive"], F["stone"]) >= 4.5   # links on the stone


def test_unknown_is_never_drawn_like_normal():
    css = open(os.path.join(ROOT, "csync", "ui", "style.py"), encoding="utf8").read()
    assert re.search(r'data-state="UNKNOWN"\]:not\(\.ctx\)\{border:1\.5px dashed', css)
    assert ".cs-card.ctx{" in css and "dashed" in css.split(".cs-card.ctx{", 1)[1].split("}", 1)[0]


def test_stone_surface_only_wraps_critical_screens():
    app = open(os.path.join(ROOT, "csync", "ui", "app.py"), encoding="utf8").read()
    blocks = re.findall(r'with st\.container\(key="cs-stone"\):\n\s+(\w+)\(', app)
    assert sorted(blocks) == ["action_screen", "resume_screen"]


def test_fonts_are_local_with_licence():
    d = os.path.join(ROOT, "csync", "ui", "fonts")
    for f in ("ClashDisplay-Variable.woff2", "Satoshi-Variable.woff2", "FFL_Fontshare_License.txt"):
        assert os.path.getsize(os.path.join(d, f)) > 1000, f
