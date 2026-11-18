"""Dark-theme tokens proposed from the pixel run. Not used by the app.

The light page, measured by scripts/measure_contrast.py on 18/11/2026:
body text on day 7 passed 4.5:1. Captions at 14 px failed 4.5
(human decision 4.40 at 1400 px, version line 4.11 at 1400 px).
State words under 4.5 at 1400 px: Attention 3.64, Mission 3.87, Habitat 3.87.
The numbers below are contrast_ratio on a flat fill, not a screenshot.
Do not wire them in while the feature freeze stands (AGENTS.md: bugs only).
csync/ui/style.py is intentionally untouched.
"""
from scripts.measure_contrast import contrast_ratio

# flat fills. Background is the page. Text and state words sit on it.
BACKGROUND = (0x14, 0x18, 0x1F)
TOKENS = {
    "body": (0xF4, 0xF1, 0xEA),
    "caption": (0xC8, 0xD0, 0xD4),
    "normal": (0x7D, 0xD3, 0xA8),
    "watch": (0xE2, 0xA4, 0x3A),
    "degraded": (0xFF, 0x8A, 0x7A),
    "unknown": (0xB7, 0xC2, 0xC8),
}
# captions in the pixel run were 14 px, so 4.5 would pass the written rule,
# but the same caption under 14 px needs 7. The proposal clears 7.
NEED = {"body": 4.5, "caption": 7.0, "normal": 4.5, "watch": 4.5, "degraded": 4.5, "unknown": 4.5}


def ratios():
    return {name: round(contrast_ratio(rgb, BACKGROUND), 2) for name, rgb in TOKENS.items()}


def below():
    found = ratios()
    return [name for name, ratio in found.items() if ratio < NEED[name]]


def main():
    found = ratios()
    print(f"background #{BACKGROUND[0]:02X}{BACKGROUND[1]:02X}{BACKGROUND[2]:02X}")
    for name, ratio in found.items():
        print(f"{name:10} {ratio:5.2f}  need {NEED[name]:.1f}")
    low = below()
    if low:
        print("below:", ", ".join(low))
        return 1
    print("below: none (formula on a flat fill, not a rendered page)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
