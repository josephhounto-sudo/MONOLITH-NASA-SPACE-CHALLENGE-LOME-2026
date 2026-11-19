"""Measure WCAG contrast from pixels of the running C-Sync page.

Widths: 1400, 1000, 390. This script does not change any colour.
Body and state words need 4.5:1. A caption whose font is under 14 px needs 7:1.

Run: python scripts/measure_contrast.py
     python scripts/measure_contrast.py --url http://127.0.0.1:8501
"""
import sys

BODY_MIN = 4.5
CAPTION_MIN = 7.0
WIDTHS = (1400, 1000, 390)
ROLES = ("body", "caption", "state")


def _lin(channel):
    s = channel / 255
    if s <= 0.04045:
        return s / 12.92
    return ((s + 0.055) / 1.055) ** 2.4


def rel_luminance(rgb):
    r, g, b = rgb[:3]
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(a, b):
    hi, lo = rel_luminance(a), rel_luminance(b)
    if hi < lo:
        hi, lo = lo, hi
    return (hi + 0.05) / (lo + 0.05)


def unique_widths(widths):
    seen = set()
    out = []
    for w in widths:
        if w in seen:
            raise ValueError(f"Width {w} is listed twice. Pass each width once: 1400, 1000, 390.")
        if not isinstance(w, int) or w < 320 or w > 2000:
            raise ValueError(f"Width {w} is not usable. Use 1400, 1000 and 390.")
        seen.add(w)
        out.append(w)
    if not out:
        raise ValueError("No width was given. Use 1400, 1000 and 390.")
    return out


def required_ratio(role, font_px):
    if role not in ROLES:
        raise ValueError(f"Unknown role {role}. Use body, caption or state.")
    if role == "caption" and font_px < 14:
        return CAPTION_MIN
    return BODY_MIN


def sample_pair(image):
    """Text colour and background colour from a crop.

    Background is the median pixel. Text is the mean of the pixels whose
    luminance is at least 0.15 away from that median (the glyphs, not a
    soft gradient). If no pixel is that far, the crop has no separable text.
    """
    image = image.convert("RGB")
    raw = image.tobytes()
    pixels = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
    if not pixels or image.size[0] == 0 or image.size[1] == 0:
        raise ValueError("Capture is empty. Start the app, wait until the page is painted, then re-run.")
    lums = [rel_luminance(p) for p in pixels]
    order = sorted(range(len(pixels)), key=lambda i: lums[i])
    bg = pixels[order[len(order) // 2]]
    med = lums[order[len(order) // 2]]
    far = [i for i in order if abs(lums[i] - med) >= 0.15]
    if len(far) < 5:
        return bg, bg
    far.sort(key=lambda i: abs(lums[i] - med), reverse=True)
    take = far[:max(5, len(far) // 2)]
    n = len(take)
    text = (
        sum(pixels[i][0] for i in take) // n,
        sum(pixels[i][1] for i in take) // n,
        sum(pixels[i][2] for i in take) // n,
    )
    return text, bg


def rows_below(rows):
    out = []
    for row in rows:
        if row["contrast"] is None:
            continue
        need = required_ratio(row["role"], row["font_px"])
        if row["contrast"] < need:
            out.append(row)
    return out


def load_playwright(importer=None):
    if importer is None:
        import importlib
        importer = importlib.import_module
    try:
        return importer("playwright.sync_api")
    except ImportError as err:
        raise RuntimeError(
            "Playwright is not installed. Run: python -m pip install playwright "
            "&& python -m playwright install chromium"
        ) from err


def format_table(rows):
    head = f"{'width':>6}  {'role':<8}  {'px':>5}  {'contrast':>8}  {'need':>5}  {'ok':<4}  text"
    lines = [head]
    for row in rows:
        if row["contrast"] is None:
            lines.append(
                f"{row['width']:>6}  {row['role']:<8}  {row['font_px']:>5.1f}  {'n/a':>8}  {'':>5}  {'n/a':<4}  {row['text']}"
            )
            continue
        need = required_ratio(row["role"], row["font_px"])
        ok = "yes" if row["contrast"] >= need else "NO"
        lines.append(
            f"{row['width']:>6}  {row['role']:<8}  {row['font_px']:>5.1f}  {row['contrast']:>8.2f}  "
            f"{need:>5.1f}  {ok:<4}  {row['text']}"
        )
    return "\n".join(lines)


def _crop(shot, box):
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(shot)).convert("RGB")
    x, y = int(box["x"]) + 1, int(box["y"]) + 1
    w, h = max(1, int(box["w"]) - 2), max(1, int(box["h"]) - 2)
    x = max(0, min(x, im.width - 1))
    y = max(0, min(y, im.height - 1))
    return im.crop((x, y, min(im.width, x + w), min(im.height, y + h)))


def measure_url(url, widths, opener):
    """opener(width) returns (screenshot_bytes, list of element dicts). Tests can pass a fake."""
    rows = []
    for width in unique_widths(list(widths)):
        shot, elements = opener(width)
        if not elements:
            raise ValueError(
                f"No text at width {width}. The page did not render. Open the app and re-run."
            )
        for el in elements:
            if el.get("role") not in ROLES:
                continue
            if el.get("png") is not None:
                import io
                from PIL import Image
                crop = Image.open(io.BytesIO(el["png"])).convert("RGB")
            else:
                crop = _crop(shot, el)
            text_rgb, bg_rgb = sample_pair(crop)
            ratio = None if text_rgb == bg_rgb else round(contrast_ratio(text_rgb, bg_rgb), 2)
            rows.append({
                "width": width,
                "role": el["role"],
                "font_px": float(el["font_px"]),
                "contrast": ratio,
                "text": el["text"],
            })
    return rows


def _browser_opener(url):
    sync = load_playwright()

    def grab(locator, role, limit, width):
        found = []
        count = min(locator.count(), 40)
        for i in range(count):
            if len(found) >= limit:
                break
            el = locator.nth(i)
            if el.evaluate("e => !!e.closest(\"[data-testid='stSlider']\")"):
                continue
            if role == "body" and el.evaluate("e => !!e.closest(\"[data-testid='stSidebar']\")"):
                continue
            text = " ".join(el.inner_text().split())[:72]
            if not text:
                continue
            box = el.bounding_box()
            if box is None or box["x"] + box["width"] < 0 or box["x"] > width:
                continue
            font = el.evaluate("e => parseFloat(getComputedStyle(e).fontSize) || 16")
            try:
                if box["y"] > 1000 or box["y"] + box["height"] < 0:
                    el.scroll_into_view_if_needed(timeout=2000)
                png = el.screenshot(timeout=3000)
            except sync.Error as exc:   # an element that cannot be captured is reported, never silently counted as passing
                print(f"NOT MEASURED ({width}px {role}): {text} ({type(exc).__name__})")
                continue
            found.append({"role": role, "text": text, "font_px": round(float(font), 1), "png": png})
        return found

    def open_at(width):
        with sync.sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": 1000})
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            try:
                page.wait_for_selector(".cs-card", timeout=20000)
            except sync.Error:
                page.wait_for_timeout(3000)
            elements = []
            elements += grab(page.locator(".cs-card"), "state", 6, width)
            elements += grab(page.locator("[data-testid='stCaptionContainer']"), "caption", 6, width)
            body = page.locator("[data-testid='stMarkdownContainer'] p, h1, h2, h3")
            elements += grab(body, "body", 8, width)
            browser.close()
            return None, elements

    return open_at


def _start_app():
    import socket
    import subprocess
    import time
    import urllib.request
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "csync/ui/app.py",
         "--server.port", str(port), "--server.headless", "true",
         "--server.address", "127.0.0.1", "--browser.gatherUsageStats", "false"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 90
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("The app stopped before it was ready. Re-run after `python -m streamlit run csync/ui/app.py`.")
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return proc, url
        except OSError:
            time.sleep(1)
    proc.kill()
    raise RuntimeError("The app did not answer within 90 s. Start it yourself and re-run with --url.")


def main(argv):
    url = ""
    if "--url" in argv:
        i = argv.index("--url")
        if i + 1 >= len(argv):
            print("Pass a URL after --url, for example http://127.0.0.1:8501")
            return 2
        url = argv[i + 1]
    proc = None
    try:
        if not url:
            proc, url = _start_app()
        rows = measure_url(url, WIDTHS, _browser_opener(url))
    except (RuntimeError, ValueError) as err:
        print(err)
        return 2
    finally:
        if proc is not None and proc.poll() is None:
            proc.kill()
    print(format_table(rows))
    low = rows_below(rows)
    print("")
    if not low:
        print("Below threshold: none")
    else:
        print(f"Below threshold: {len(low)}")
        for row in low:
            need = required_ratio(row["role"], row["font_px"])
            print(f"  {row['width']}px {row['role']} {row['contrast']:.2f} < {need:.1f}  {row['text']}")
    return 1 if low else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
