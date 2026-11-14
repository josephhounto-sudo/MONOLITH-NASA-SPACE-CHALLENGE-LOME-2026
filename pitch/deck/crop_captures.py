"""FICHIER: pitch/deck/crop_captures.py · 14/11/2026 ~14:55 UTC · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Crops (no editing, no scaling) of the real screenshots so that the useful part is larger on the slide:
removes the white side margins and, for C1/C2, the rows that are already said by the slide (app banner, slider, cut-off text).
Originals stay untouched in pitch/deck/captures/. Run from the repo root: python pitch/deck/crop_captures.py
Needs Pillow (outside the engine; only used to prepare the deck)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "captures"); DST = os.path.join(SRC, "crops")
# (file, box = left, top, right, bottom in original pixels)
BOXES = {
    "C1_dimensions_j7_seed42_amp25.png": (105, 290, 1995, 525),
    "C2_capsule_j7_seed42_amp25.png": (105, 30, 1995, 378),
    "C3_procedure_j9_seed42_amp25.png": (105, 0, 1995, 1065),
    "C4_file_envoi_j9_seed42_amp25.png": (105, 0, 1995, 445),
    "C5_reprise_j10_seed42_amp25.png": (105, 1000, 1995, 1700),
}
os.makedirs(DST, exist_ok=True)
for f, box in BOXES.items():
    im = Image.open(os.path.join(SRC, f)).crop(box)
    out = os.path.join(DST, f.split("_")[0] + "_crop.png"); im.save(out); print(out, im.size)
