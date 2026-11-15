"""FICHIER: pitch/deck/capture_app.py · 15/11/2026 ~08:15 UTC · FAIT PAR L'IA (session design) — PAS ENCORE VÉRIFIÉ
Takes the deck captures C1-C6 from the RUNNING app (design fusion, main), element by element, at 2x for the projector.
Run: streamlit run csync/ui/app.py --server.port 8611  (other terminal), then  python pitch/deck/capture_app.py
Writes pitch/deck/captures/crops/C1..C5_crop.png and pitch/deck/captures/C6_habitat_eda_rr1_en.png (in-app NASA panel)."""
import asyncio, io, os
from PIL import Image
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); CROPS = os.path.join(HERE, "captures", "crops"); URL = "http://localhost:8611"


async def day(pg, n):
    s = pg.get_by_role("slider"); await s.focus()
    for _ in range(9): await pg.keyboard.press("ArrowLeft")
    for _ in range(n - 1): await pg.keyboard.press("ArrowRight")
    await pg.wait_for_timeout(2500)


async def shot(pg, selector, path, keep=None):
    el = pg.locator(selector).first
    await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(500)
    im = Image.open(io.BytesIO(await el.screenshot()))
    if keep: im = im.crop((0, int(im.height * keep[0]), im.width, int(im.height * keep[1])))
    im.save(path); print(os.path.relpath(path, HERE), im.size)


async def main():
    os.makedirs(CROPS, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME") or None)
        pg = await b.new_page(viewport={"width": 1280, "height": 3000}, device_scale_factor=2)
        await pg.goto(URL); await pg.wait_for_timeout(7000)
        await day(pg, 7)
        await shot(pg, "[data-testid='stHorizontalBlock']:has(.cs-card)", os.path.join(CROPS, "C1_crop.png"))
        await pg.evaluate("""()=>{let e=document.querySelector('.cs-action');while(e&&getComputedStyle(e).borderTopStyle==='none'||e&&e.classList.contains('cs-action'))e=e.parentElement;if(e)e.id='cs-c2'}""")
        await shot(pg, "#cs-c2", os.path.join(CROPS, "C2_crop.png"))
        await shot(pg, ".st-key-cs-habitat", os.path.join(HERE, "captures", "C6_habitat_eda_rr1_en.png"), keep=(0, 0.52))
        await day(pg, 9)
        for _ in range(2):
            await pg.get_by_role("button", name="Next").click(); await pg.wait_for_timeout(1200)
        await shot(pg, ".st-key-cs-stone", os.path.join(CROPS, "C3_crop.png"), keep=(0, 0.62))
        await pg.get_by_text("Link restored").click(); await pg.wait_for_timeout(1200)
        await shot(pg, ".st-key-cs-stone", os.path.join(CROPS, "C4_crop.png"), keep=(0.845, 1))
        await day(pg, 10)
        await pg.get_by_role("button", name="Request resume").click(); await pg.wait_for_timeout(1500)
        await pg.get_by_role("button", name="Commander override").click(); await pg.wait_for_timeout(1500)
        await shot(pg, ".st-key-cs-stone", os.path.join(CROPS, "C5_crop.png"))
        await b.close()
asyncio.run(main())
