"""One shape code for the app AND the deck: the orbit glyph. Core silhouette = state (circle normal, diamond watch,
triangle degraded, dashed square unknown); the orbit and its dot say how far from the personal baseline. Same geometry as csync/ui/style.py. 15/11 · FAIT PAR L'IA."""

_CORE = {
    "NORMAL": ("<circle cx='16' cy='16' r='6' fill='{c}'/>", (27.2, 9.9), ""),
    "WATCH": ("<path d='M16 9.6 22.4 16 16 22.4 9.6 16Z' fill='{c}'/>", (28.4, 9.2), " pathLength='100' stroke-dasharray='86 6 8 0'"),
    "DEGRADED": ("<path d='M16 9.2 22.2 20.2H9.8Z' fill='{c}'/>", (29.5, 8.5), " pathLength='100' stroke-dasharray='58 16 26 0'"),
    "UNKNOWN": ("<rect x='10.5' y='10.5' width='11' height='11' rx='1.5' fill='none' stroke='{c}' stroke-width='1.8' stroke-dasharray='3 2.4'/>", None, " stroke-dasharray='3 3' opacity='.7'"),
}


def orbit_inner(state, color):
    """SVG elements of one glyph in a 35x33 box (viewBox -1 0 35 33)."""
    state = "DEGRADED" if state == "OPEN_PROCEDURE" else state
    core, dot, ring_extra = _CORE[state]
    ring = f"<ellipse cx='16' cy='17' rx='14' ry='5.5' transform='rotate(-24 16 17)' fill='none' stroke='{color}' stroke-width='1.9'{ring_extra}/>"
    d = f"<circle cx='{dot[0]}' cy='{dot[1]}' r='2.6' fill='{color}'/>" if dot else ""
    return ring + core.format(c=color) + d


def orbit_svg(state, color, size=48, label=""):
    aria = f" role='img' aria-label='{label}'" if label else " aria-hidden='true'"
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='-1 0 35 33' width='{size}' height='{round(size * 33 / 35)}'{aria}>{orbit_inner(state, color)}</svg>"
