"""FICHIER: pitch/deck/export_pdf_pptx.py · 14/11/2026 ~15:20 UTC · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Exports deck_final.html to a PDF (16:9, 1 slide per page) and to a backup .pptx made of one full-slide image per slide
(visually identical, NOT editable text). Needs playwright + python-pptx (outside the engine). Run from the repo root."""
import asyncio, os, tempfile
from playwright.async_api import async_playwright
from pptx import Presentation
from pptx.util import Emu
HERE = os.path.join(os.getcwd(), "pitch", "deck")
NAME = os.environ.get("DECK", "deck")
SUF = "_FR" if NAME == "deck_fr" else ""
URL = "file://" + os.path.join(HERE, NAME + "_final.html")
async def main():
    tmp = tempfile.mkdtemp(); imgs = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        for i in range(1, 8):
            await pg.goto(f"{URL}#{i}"); await pg.reload(); await pg.wait_for_timeout(250)
            # slide 1 motion: freeze on its last frame (= the poster) so the backup image shows the final title
            await pg.evaluate("()=>{const v=document.querySelector('video');if(v){v.pause();v.currentTime=Math.max(0,(v.duration||5.5)-0.05)}}"); await pg.wait_for_timeout(400)
            f = os.path.join(tmp, f"s{i}.png"); await pg.screenshot(path=f); imgs.append(f)
        await pg.goto(URL); await pg.emulate_media(media="print")
        await pg.pdf(path=os.path.join(HERE, "C-Sync_pitch_7_slides" + SUF + ".pdf"), width="16in", height="9in", print_background=True, prefer_css_page_size=True)
        await b.close()
    pr = Presentation(); pr.slide_width = Emu(12192000); pr.slide_height = Emu(6858000)
    for f in imgs:
        s = pr.slides.add_slide(pr.slide_layouts[6]); s.shapes.add_picture(f, 0, 0, pr.slide_width, pr.slide_height)
    pr.save(os.path.join(HERE, "C-Sync_pitch_SECOURS_images" + SUF + ".pptx")); print("OK")
asyncio.run(main())
