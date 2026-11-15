"""FICHIER: pitch/deck/embed_captures.py
Date/heure : sam. 14/11/2026 08:10 Lomé (UTC) · Commit de référence : dc61786 · Version v1
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

Inserts the real captures into the deck while keeping a single self-contained file.
1. Put the PNG files in pitch/deck/captures/ with the exact names of captures_map.md.
2. Run from the repo root:  python pitch/deck/embed_captures.py
3. Output: pitch/deck/deck_final.html (deck.html is never modified). Missing captures stay as frames.
Expected output: one line per capture ("C2: inserted" or "C2: MISSING, frame kept"), then "OK: pitch/deck/deck_final.html".
Python 3 standard library only.
"""
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERN = re.compile(r'(<div class="capture"(?: style="[^"]*")? data-capture="(C\d)" data-file="([^"]+)">)(.*?)(</div>)', re.S)


def main():
    src = open(os.path.join(HERE, "deck.html"), encoding="utf8").read()

    def repl(m):
        start, cid, fname, inner, end = m.groups()
        path = os.path.join(HERE, "captures", fname)
        if not os.path.exists(path):
            print(f"{cid}: MISSING ({fname}), frame kept")
            return m.group(0)
        b64 = base64.b64encode(open(path, "rb").read()).decode("ascii")
        banner = re.search(r'<span class="sb">.*?</span>', inner)
        print(f"{cid}: inserted ({fname})")
        return f'{start}{banner.group(0) if banner else ""}<img alt="Capture {cid}" src="data:image/png;base64,{b64}">{end}'

    out = PATTERN.sub(repl, src)
    # Logo: embed pitch/deck/captures/LOGO_ACTUEL_horizontal.png if present, otherwise drop the placeholder frame.
    logo = os.path.join(HERE, "captures", "LOGO_ACTUEL_horizontal.png")
    placeholder = '<div class="logo">LOGO_À_FOURNIR</div>'
    if os.path.exists(logo):
        b64 = base64.b64encode(open(logo, "rb").read()).decode("ascii")
        out = out.replace(placeholder, f'<img class="logo-img" alt="Team logo" src="data:image/png;base64,{b64}">')
        print("LOGO: inserted")
    else:
        out = out.replace(placeholder, "<div></div>")
        print("LOGO: MISSING (captures/LOGO_ACTUEL_horizontal.png), placeholder removed")
    # Slide 1 motion (Care Sync -> C-Sync, light) + its last frame as poster (PDF/print). 15/11 · FAIT PAR L'IA (session design)
    for attr, mime in (("data-video", "video/mp4"), ("data-poster", "image/png")):
        for rel in re.findall(attr + r'="([^"]+)"', out):
            f = os.path.normpath(os.path.join(HERE, rel))
            if os.path.exists(f):
                b64 = base64.b64encode(open(f, "rb").read()).decode("ascii")
                out = out.replace(f'{attr}="{rel}"', f'src="data:{mime};base64,{b64}"')
                print(f"{attr}: inserted ({os.path.basename(f)})")
            else:
                print(f"{attr}: MISSING ({rel})")
    open(os.path.join(HERE, "deck_final.html"), "w", encoding="utf8").write(out)
    print("OK: pitch/deck/deck_final.html")


if __name__ == "__main__":
    main()
