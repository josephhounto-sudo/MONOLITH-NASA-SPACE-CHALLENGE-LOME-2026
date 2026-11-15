"""Deck shapes carry real numbers: the dots and rings in pitch/deck/deck.html match research/pilot/holdout_results.json; every slide is on the dark surface."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = open(os.path.join(ROOT, "pitch", "deck", "deck.html"), encoding="utf8").read()
PUB = json.load(open(os.path.join(ROOT, "research", "pilot", "holdout_results.json"), encoding="utf8"))


def test_dot_grid_matches_published_control():
    c = PUB["control (false procedure)"]
    m = re.search(r"data-n='(\d+)' data-hits='(\d+)'", DECK)
    assert (int(m.group(1)), int(m.group(2))) == (c["n"], c["hits"])
    svg = DECK[m.start():DECK.index("</svg>", m.start())]
    assert svg.count("<circle") == c["n"]


def test_rings_match_published_detection():
    m = re.search(r"data-gradual='(\d+)/(\d+)' data-abrupt='(\d+)/(\d+)'", DECK)
    g, a = PUB["gradual 1.5 SD"], PUB["abrupt 2 SD"]
    assert tuple(map(int, m.groups())) == (g["hits"], g["n"], a["hits"], a["n"])
    assert f"{round(100 * g['hits'] / g['n'])}%" in DECK and f"{round(100 * a['hits'] / a['n'])}%" in DECK


def test_all_slides_dark_no_pink_surface():
    sections = re.findall(r'<section class="slide[^"]*"', DECK)
    assert len(sections) == 7 and all("stone" in s for s in sections)
