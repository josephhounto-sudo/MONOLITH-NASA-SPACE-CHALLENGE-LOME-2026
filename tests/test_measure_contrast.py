"""Pixel contrast of the rendered page. The script measures; it does not recolour.

Acceptance: for widths 1400, 1000 and 390, the script prints one table and
lists every sample under 4.5:1 (body and state words) or under 7:1
(captions whose font is below 14 px).

Five ways it fails:
1. the capture has no pixels (app did not paint).
2. the same colour is used for text and background (ratio 1, below 4.5).
3. a width is listed twice, so the table is not one row-set per width.
4. a caption under 14 px is judged with the body threshold.
5. Playwright is missing, and the message does not say how to install it.
"""
import os

import pytest
from PIL import Image

from scripts.measure_contrast import (
    BODY_MIN,
    CAPTION_MIN,
    WIDTHS,
    contrast_ratio,
    load_playwright,
    required_ratio,
    rows_below,
    sample_pair,
    unique_widths,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _solid(size, rgb):
    im = Image.new("RGB", size, rgb)
    return im


def test_empty_capture_says_what_to_do():
    """Failure 1: nothing was painted."""
    im = Image.new("RGB", (0, 0))
    with pytest.raises(ValueError) as err:
        sample_pair(im)
    assert "re-run" in str(err.value).lower()


def test_black_on_white_is_21_and_white_on_white_fails_body():
    """Failure 2: text and background are the same colour."""
    black = (0, 0, 0)
    white = (255, 255, 255)
    assert contrast_ratio(black, white) == pytest.approx(21, abs=0.05)
    flat = _solid((40, 20), white)
    text, bg = sample_pair(flat)
    assert contrast_ratio(text, bg) == pytest.approx(1, abs=0.05)
    assert contrast_ratio(text, bg) < BODY_MIN


def test_duplicate_width_is_rejected():
    """Failure 3: the same width twice."""
    with pytest.raises(ValueError) as err:
        unique_widths([1400, 1000, 1400])
    assert "twice" in str(err.value)
    assert unique_widths(list(WIDTHS)) == [1400, 1000, 390]


def test_small_caption_needs_seven(tmp_path=None):
    """Failure 4: a caption under 14 px must not be judged at 4.5:1."""
    assert required_ratio("caption", 13) == CAPTION_MIN == 7
    assert required_ratio("caption", 14) == BODY_MIN == 4.5
    assert required_ratio("body", 16) == 4.5
    assert required_ratio("state", 18) == 4.5
    row = {"width": 390, "role": "caption", "font_px": 12, "contrast": 5.2, "text": "SIMULATED"}
    assert rows_below([row]) == [row]


def test_missing_playwright_says_how_to_install():
    """Failure 5: the browser library is absent."""
    def boom(name):
        raise ImportError(name)
    with pytest.raises(RuntimeError) as err:
        load_playwright(boom)
    text = str(err.value)
    assert "pip install playwright" in text
    assert "playwright install chromium" in text


def test_script_does_not_write_theme_or_style():
    src = open(os.path.join(ROOT, "scripts", "measure_contrast.py"), encoding="utf8").read()
    assert "theme.json" not in src
    assert "style.py" not in src
    assert 'open("' not in src and "open('" not in src


def test_sample_finds_black_text_on_a_white_field():
    im = _solid((80, 30), (255, 255, 255))
    for x in range(10, 50):
        for y in range(8, 22):
            im.putpixel((x, y), (0, 0, 0))
    text, bg = sample_pair(im)
    assert contrast_ratio(text, bg) > 15
