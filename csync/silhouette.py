"""Body map: a neutral front-view figure with 8 selectable zones. Data: pitch/silhouette/fiches.json (zone sheets, NASA HRP
sources, honest 'not measured' status). Colours come from csync/config/theme.json. No face, no person: a generic shape.
The map is an image (Streamlit removes inline SVG); selection is a keyboard-accessible control next to it, never the
image alone, and every zone is also named in words."""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHES = os.path.join(ROOT, "pitch", "silhouette", "fiches.json")
THEME = json.load(open(os.path.join(ROOT, "csync", "config", "theme.json"), encoding="utf8"))

# region id -> (short label, shapes as (tag, attributes)); geometry of pitch/silhouette/silhouette.svg
SHAPES = {
    "region-head": ("Head", [("circle", 'cx="200" cy="68" r="38"')]),
    "region-chest": ("Chest", [("rect", 'x="140" y="122" width="120" height="108" rx="24"')]),
    "region-abdomen": ("Abdomen", [("rect", 'x="148" y="234" width="104" height="88" rx="16"')]),
    "region-arm": ("Arm", [("rect", 'x="98" y="128" width="36" height="168" rx="18"'),
                           ("rect", 'x="266" y="128" width="36" height="168" rx="18"')]),
    "region-hand": ("Hand", [("circle", 'cx="116" cy="314" r="17"'), ("circle", 'cx="284" cy="314" r="17"')]),
    "region-legs": ("Legs", [("rect", 'x="152" y="326" width="42" height="208" rx="20"'),
                             ("rect", 'x="206" y="326" width="42" height="208" rx="20"')]),
    "region-body": ("Whole body", [("rect", 'x="12" y="20" width="118" height="40" rx="10"')]),
    "region-habitat": ("Habitat", [("rect", 'x="20" y="568" width="360" height="56" rx="12"')]),
}
STATUS_STATE = {"measured": "NORMAL", "unknown": "UNKNOWN", "context": "UNKNOWN"}
STATUS_WORD = {"measured": "Measured by C-Sync", "unknown": "Not measured — shown as Unknown",
               "context": "Context only — not evaluated"}
# symptom zone words reported in capsules -> region id
ZONE_TO_REGION = {"thorax": "region-chest", "chest": "region-chest", "head": "region-head", "abdomen": "region-abdomen",
                  "arm": "region-arm", "hand": "region-hand", "leg": "region-legs", "legs": "region-legs"}


def fiches() -> dict:
    with open(FICHES, encoding="utf8") as f:
        data = json.load(f)
    return {r["id"]: r for r in data["regions"]}


def label(region_id: str) -> str:
    return SHAPES[region_id][0]


def region_for_zone(zone: str | None) -> str | None:
    return ZONE_TO_REGION.get((zone or "").strip().lower())


def svg(selected: str | None = None) -> str:
    """SVG string of the figure; the selected zone is outlined and the others keep their status colour."""
    t, st_ = THEME, fiches()
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 640" role="img" '
           f'aria-label="Neutral front-view body map, 8 zones, selected: {label(selected) if selected else "none"}">',
           f'<rect width="400" height="640" fill="{t["surface"]}"/>',
           f'<rect x="186" y="104" width="28" height="20" rx="6" fill="{t["panel"]}" stroke="{t["text_secondary"]}" stroke-width="2"/>']
    for rid, (_, shapes) in SHAPES.items():
        state = STATUS_STATE[st_[rid]["status"]]
        colour = t["state"][state]["color"]
        dash = ' stroke-dasharray="6 5"' if st_[rid]["status"] != "measured" else ""
        sel = rid == selected
        width, stroke = (5, t["interactive"]) if sel else (3, colour)
        for tag, attrs in shapes:
            out.append(f'<{tag} {attrs} fill="{t["panel"]}" stroke="{stroke}" stroke-width="{width}"{dash}/>')
    out.append("</svg>")
    return "".join(out)


def markdown_image(selected: str | None, alt: str) -> str:
    """The figure as a Markdown image with alt text (Streamlit's own image element sets no alt attribute)."""
    import base64
    data = base64.b64encode(svg(selected).encode("utf8")).decode("ascii")
    alt = alt.replace("[", "(").replace("]", ")")
    return f"![{alt}](data:image/svg+xml;base64,{data})"
