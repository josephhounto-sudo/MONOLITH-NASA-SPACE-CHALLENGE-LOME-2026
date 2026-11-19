"""Indicator card (watch style) and curve chart (bookings style). Presentation only: every number comes from the capsule and the trends file.

The card answers one question, "which of my numbers left my own normal, and by how much", with the value, its unit, the state word and icon,
the personal normal and threshold as two dotted lines, and one dot per mission day. Colour is the third cue: word and icon always stay.
"""
import base64
import html

from csync.ui import icons

_RANK = {"UNKNOWN": 0, "NORMAL": 1, "WATCH": 2, "DEGRADED": 3}


def _num(v):
    return f"{v:.0f}" if abs(v) >= 100 else f"{v:.1f}"


def _uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def smooth_path(pts):
    """Catmull-Rom curve through the points, as an SVG path (the curve of the bookings reference). At least two points."""
    assert len(pts) >= 2, "a curve needs two points"
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def pick_signal(cap, day):
    """The flagged signal in the most severe dimension (ties: largest distance d). None while the baseline is building or nothing is flagged."""
    if day <= 5:
        return None
    best, key = None, (-1, -1.0)
    for s in cap.get("signals", []):
        if not s.get("flagged") or s.get("d") is None:
            continue
        k = (_RANK.get(cap["states"].get(s.get("dimension"), "UNKNOWN"), 0), abs(s["d"]))
        if k > key:
            best, key = s, k
    return best


def dots_image(rows, base, thr, ch, alt):
    """Watch-style history: one dot per day between two dotted lines (personal normal and threshold), the current day ringed. Image tag with a text alternative."""
    W, H = 300, 96
    vals = [r["value"] for r in rows if r["value"] is not None]
    lo, hi = min(vals + [base, thr]), max(vals + [base, thr])
    pad = (hi - lo) * 0.18 or 1
    lo, hi = lo - pad, hi + pad
    X = lambda i: 12 + (W - 52) * i / 9
    Y = lambda v: 12 + (H - 24) * (hi - v) / (hi - lo)
    g = [f'<line x1="6" x2="{W-34}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{ch["baseline"]}" stroke-opacity=".7" stroke-width="1.6" '
         f'stroke-dasharray="1 5" stroke-linecap="round"/>' for v in (thr, base)]
    for v in (thr, base):
        g.append(f'<text x="{W-30}" y="{Y(v)+4:.1f}" font-size="14" fill="{ch["ink"]}" font-family="sans-serif">{v:.0f}</text>')
    for i, r in enumerate(rows):
        if r["value"] is None:
            continue
        col = ch["flagged"] if r["flagged"] else ch["value"]
        g.append(f'<circle cx="{X(i):.1f}" cy="{Y(r["value"]):.1f}" r="{3.4 if i < len(rows) - 1 else 4.2}" fill="{col}" opacity="{1 if i >= len(rows) - 3 else .75}"/>')
    last = rows[-1]
    g.append(f'<circle cx="{X(len(rows) - 1):.1f}" cy="{Y(last["value"]):.1f}" r="9" fill="none" stroke="{ch["value"]}" stroke-width="2"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + "".join(g) + "</svg>"
    return f"<img src='{_uri(svg)}' alt='{html.escape(alt, quote=True)}'>"   # a real tag: markdown image syntax is not parsed inside an HTML block


def indicator_card(sig, state, rows, thr, day, ui, states_words, ch):
    """HTML of the watch-style card for one signal. `rows` = that indicator's days up to `day` (from trends_histoire.json)."""
    assert rows and rows[-1]["day"] == day, "rows must end on the shown day"
    assert state in _RANK, "unknown state"
    unit, base = sig["unit"], sig["baseline_mean"]
    above = [str(r["day"]) for r in rows if r["value"] is not None and r["value"] > thr] if sig.get("d", 0) > 0 else \
            [str(r["day"]) for r in rows if r["value"] is not None and r["value"] < thr]
    alt = ui["ind_dots_alt"].format(name=sig["name"], a=rows[0]["day"], b=day, v=_num(sig["value"]), unit=unit, base=_num(base), thr=_num(thr),
                                    days=", ".join(above) if above else "-")
    arrow = "↑" if sig.get("d", 0) > 0 else "↓"
    chip = f"{icons.state_icon(state)} {html.escape(states_words[state])}"
    name = html.escape(sig["name"])
    dist = f"{abs(sig['d']):.1f}"
    why = ui["ind_why"].format(base=_num(base), thr=_num(thr), unit=html.escape(unit), d=dist)
    t0, t1 = ui["ind_tick"].format(d=rows[0]["day"]), ui["ind_tick"].format(d=day)
    return (f"<section class='cs-ind' data-state='{state}' aria-label='{name}'>"
            f"<div class='row'><span class='lab'>{name}</span><span class='chip'>{chip}</span></div>"
            f"<div class='big'><span>{_num(sig['value'])}</span><small>{html.escape(unit)}</small>"
            f"<span class='arr' aria-label='{html.escape(ui['ind_beyond'])}'>{arrow}</span></div>"
            f"<p class='why'>{why}</p>"
            f"{dots_image(rows, base, thr, ch, alt)}"
            f"<div class='ticks'><span>{t0}</span><span>{t1}</span></div></section>")


def curve_image(rows, base, thr, label, ch, day_word):
    """Trend curve: smooth line, soft area, two dotted lines, a glowing point on the last day. Markdown image with a text alternative (used on its own, outside an HTML block)."""
    W, H, L, R, T, B = 480, 230, 48, 14, 22, 44
    vals = [r["value"] for r in rows if r["value"] is not None]
    lo, hi = min(vals + [base, thr]), max(vals + [base, thr])
    pad = (hi - lo) * 0.14 or 1
    lo, hi = lo - pad, hi + pad
    n = max(len(rows) - 1, 1)
    X = lambda i: L + (W - L - R) * i / n
    Y = lambda v: T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    pts = [(X(i), Y(r["value"])) for i, r in enumerate(rows) if r["value"] is not None]
    g = [f'<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ch["threshold"]}" stop-opacity=".38"/>'
         f'<stop offset="1" stop-color="{ch["threshold"]}" stop-opacity="0"/></linearGradient>'
         f'<radialGradient id="g"><stop offset="0" stop-color="{ch["value"]}"/><stop offset="1" stop-color="{ch["flagged"]}" stop-opacity="0"/></radialGradient></defs>']
    for v in (lo + pad, (lo + hi) / 2, hi - pad):
        g.append(f'<text x="{L-8}" y="{Y(v)+4:.0f}" font-size="15" text-anchor="end" fill="{ch["ink"]}" font-family="sans-serif">{v:.3g}</text>')
    for i, r in enumerate(rows):
        g.append(f'<text x="{X(i):.0f}" y="{H-22}" font-size="15" text-anchor="middle" fill="{ch["ink"]}" font-family="sans-serif">{r["day"]}</text>')
    g.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-4}" font-size="15" text-anchor="middle" fill="{ch["ink"]}" font-family="sans-serif">{html.escape(day_word)}</text>')
    for v, col in ((base, ch["baseline"]), (thr, ch["flag_line"])):
        g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{col}" stroke-opacity=".8" stroke-width="1.6" stroke-dasharray="1 5" stroke-linecap="round"/>')
    if len(pts) >= 2:
        line = smooth_path(pts)
        g.append(f'<path d="{line} L{pts[-1][0]:.1f},{H-B} L{pts[0][0]:.1f},{H-B} Z" fill="url(#a)"/>')
        g.append(f'<path d="{line}" fill="none" stroke="{ch["threshold"]}" stroke-width="3" stroke-linecap="round"/>')
    for i, r in enumerate(rows):
        if r["value"] is None:
            continue
        if r["flagged"]:
            g.append(f'<circle cx="{X(i):.1f}" cy="{Y(r["value"]):.1f}" r="5.5" fill="{ch["flagged"]}" stroke="{ch["ring"]}" stroke-width="2"/>')
    lx, ly = pts[-1]
    g.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="15" fill="url(#g)" opacity=".7"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="5.5" fill="{ch["value"]}" '
             f'stroke="{ch["flagged"] if rows[-1]["flagged"] else ch["threshold"]}" stroke-width="3"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + "".join(g) + "</svg>"
    flagged = [str(r["day"]) for r in rows if r["flagged"]]
    alt = (f"{label}, days {rows[0]['day']} to {rows[-1]['day']}: values {min(vals):.3g} to {max(vals):.3g}; personal baseline {base:.3g}, "
           f"threshold {thr:.3g}" + (f"; flagged days {', '.join(flagged)}." if flagged else "; no flagged day."))
    return f"![{alt}]({_uri(svg)})"
