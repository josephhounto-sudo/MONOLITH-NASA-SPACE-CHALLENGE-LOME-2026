"""Layout check on the running page: every section at 1400, 1000 and 390 px.

Flags: horizontal page scroll, text clipped by its own box (scrollWidth > clientWidth with overflow hidden),
elements that stick out of the viewport, and Streamlit error boxes. Changes nothing.
Run: python scripts/check_layout.py [--url http://127.0.0.1:8501]
"""
import sys

WIDTHS = (1400, 1000, 390)
NAMES = ("Overall state", "Commander board", "Body map", "Habitat (real NASA data)", "Trends", "Evidence at scale",
         "Why a personal baseline?", "NASA hazards and countermeasures", "Try it yourself", "Sources")
JS = """() => {
  const out = [], vw = document.documentElement.clientWidth;
  if (document.documentElement.scrollWidth > vw + 1) out.push('page scrolls sideways: ' + document.documentElement.scrollWidth + ' > ' + vw);
  document.querySelectorAll('[data-testid="stException"], [data-testid="stAlert"] .stException').forEach(e => out.push('error box: ' + e.innerText.slice(0, 80)));
  const main = document.querySelector('section.main, [data-testid="stMain"]') || document.body;
  main.querySelectorAll('p,span,div,h1,h2,h3,li,button,label').forEach(e => {
    if (e.children.length > 0 && e.tagName !== 'BUTTON') return;
    const t = (e.innerText || '').trim(); if (t.length < 2) return;
    const r = e.getBoundingClientRect(); if (r.width === 0 || r.height === 0) return;
    const cs = getComputedStyle(e);
    if (e.scrollWidth > e.clientWidth + 2 && cs.overflow !== 'visible' && cs.overflowX !== 'auto' && cs.overflowX !== 'scroll') out.push('clipped: ' + t.slice(0, 40));
    if (r.right > vw + 2 && cs.position !== 'fixed') out.push('outside viewport: ' + t.slice(0, 40));
  });
  return Array.from(new Set(out));
}"""


def main(url):
    from playwright.sync_api import sync_playwright
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in WIDTHS:
            pg = b.new_page(viewport={"width": w, "height": 1000})
            pg.goto(url)
            pg.wait_for_timeout(5000)
            for i, name in enumerate(NAMES):
                if i:
                    for _ in range(2):
                        try:
                            pg.locator('section[data-testid="stSidebar"]').get_by_text(name, exact=True).first.click(timeout=3000)
                            break
                        except Exception:
                            pg.locator('[data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"]').first.click(timeout=3000)
                            pg.wait_for_timeout(600)
                    pg.wait_for_timeout(2500)
                for issue in pg.evaluate(JS):
                    bad += 1
                    print(f"{w:5d}px  {name[:28]:28}  {issue}")
            pg.close()
        b.close()
    print(f"issues: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    u = sys.argv[sys.argv.index("--url") + 1] if "--url" in sys.argv else "http://127.0.0.1:8501"
    sys.exit(main(u))
