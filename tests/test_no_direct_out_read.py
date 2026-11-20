"""20/11 crash on the hosted app: a page opened data/out directly, which only exists on a developer's machine (generated,
not committed). Local tests passed because the folder was there. Rule: only app.resolve_out_dir decides where story files are."""
import os
import re

UI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csync", "ui")


def test_no_page_reads_the_generated_folder_directly():
    bad = []
    for name in os.listdir(UI):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(UI, name), encoding="utf8") as fh:
            for i, line in enumerate(fh, 1):
                code = line.split("#")[0]
                if re.search(r"""["']data["']\s*,\s*["']out["']""", code) and "OUT_DIR = os.environ.get" not in code:
                    bad.append(f"{name}:{i}")
    assert bad == [], bad
