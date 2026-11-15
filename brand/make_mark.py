"""C-Sync mark: a crescent "C" (the crew, the stone) with a small body in its mouth (the ground), both on one orbit.
The orbit crosses the crescent as a knockout (negative space). Pure geometry, 100 x 100 grid. FAIT PAR L'IA."""
import math
import sys
CX, CY, R = 46, 54, 34            # disc
KX, KY, KR = 60, 48, 27           # cut that opens the C to the upper right
ORB = dict(cx=46, cy=54, rx=47, ry=15, rot=-24)
DOT = (82.8, 48.2, 6.2)           # on the orbit (t = 40 deg), inside the mouth of the C


def arc(a0, a1, scale=1.0, n=90):
    """Polyline of the orbit between local angles a0..a1 (deg). Local y > 0 = front half (towards the viewer)."""
    o, pts = ORB, []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n); x = o["rx"] * math.cos(a); y = o["ry"] * math.sin(a); r = math.radians(o["rot"])
        pts.append(((o["cx"] + x * math.cos(r) - y * math.sin(r)) * scale, (o["cy"] + x * math.sin(r) + y * math.cos(r)) * scale))
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)


def svg(fill="#141618", orbit=None, size=512, gradient=False, bg=None):
    orbit = orbit or fill
    o = ORB
    ell = f"<ellipse cx='{o['cx']}' cy='{o['cy']}' rx='{o['rx']}' ry='{o['ry']}' transform='rotate({o['rot']} {o['cx']} {o['cy']})'"
    paint = "url(#g)" if gradient else fill
    grad = ("<linearGradient id='g' x1='0' y1='1' x2='1' y2='0'><stop offset='0' stop-color='#0B6E85'/><stop offset='.45' stop-color='#1F2A3D'/>"
            "<stop offset='.78' stop-color='#F77256'/><stop offset='1' stop-color='#FEAA60'/></linearGradient>") if gradient else ""
    back_bg = f"<rect width='100' height='100' fill='{bg}'/>" if bg else ""
    front, back = arc(0, 180), arc(180, 360)
    back_rect = back_bg
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' width='{size}' height='{size}'><title>C-Sync</title><defs>{grad}"
            f"<mask id='c' maskUnits='userSpaceOnUse'><rect width='100' height='100' fill='white'/>"
            f"<circle cx='{KX}' cy='{KY}' r='{KR}' fill='black'/><path d='{front}' fill='none' stroke='black' stroke-width='5'/></mask></defs>{back}"
            f"<path d='{back}' fill='none' stroke='{orbit}' stroke-width='1.6' stroke-linecap='round'/>"
            f"<circle cx='{CX}' cy='{CY}' r='{R}' fill='{paint}' mask='url(#c)'/>"
            f"<path d='{front}' fill='none' stroke='{orbit}' stroke-width='1.6' stroke-linecap='round'/>"
            f"<circle cx='{DOT[0]}' cy='{DOT[1]}' r='{DOT[2]}' fill='{paint}'/></svg>")

if __name__ == "__main__":
    out = sys.argv[1]
    open(f"{out}/csync_mark_ink.svg", "w").write(svg("#141618"))
    open(f"{out}/csync_mark_cream.svg", "w").write(svg("#F4F0E4"))
    open(f"{out}/csync_mark_gradient.svg", "w").write(svg(gradient=True, orbit="#1F2A3D"))
    print("ok")
