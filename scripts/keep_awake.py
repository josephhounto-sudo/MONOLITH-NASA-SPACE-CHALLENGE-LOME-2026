"""Keep the hosted app awake. Streamlit Community Cloud puts a free app to sleep after a period without visits, and a plain
HTTP request does not wake it (the response is a static shell). This script opens the app in a real browser, clicks the
wake button if the sleep page is shown, and fails loudly if the app does not come back (the workflow run turns red)."""
import asyncio
import sys

from playwright.async_api import async_playwright

URL = "https://monolith-nasa-space-challenge-lome-kwtv79qy52ihwgezt8byuy.streamlit.app/"
WAIT_MS = 120_000


async def main() -> int:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(URL, wait_until="domcontentloaded", timeout=WAIT_MS)
        await page.wait_for_timeout(8_000)
        wake = page.get_by_role("button", name="Yes, get this app back up!")
        if await wake.count():
            print("asleep: waking")
            await wake.click()
        try:
            await page.wait_for_timeout(30_000)
            await page.goto(URL + "~/+/", wait_until="domcontentloaded", timeout=WAIT_MS)   # the app itself, outside the frame
            await page.get_by_text("C-Sync").first.wait_for(timeout=WAIT_MS)
        except Exception:   # noqa: BLE001 - any failure here means the app is not up; the run must turn red
            print("app did not come up", file=sys.stderr)
            await browser.close()
            return 1
        print("awake")
        await browser.close()
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
