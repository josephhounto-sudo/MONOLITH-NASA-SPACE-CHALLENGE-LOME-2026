"""20/11 crash on the hosted app: a page read data/out directly. data/out is generated and not committed, so on a clean clone
the file is missing. Only resolve_out_dir (app.py) and the documented in-memory fallback (csync/live.py) may name it.
The cold-start tests missed it because data/out exists on the developer machine: this test reads the code instead."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = {os.path.join("csync", "ui", "app.py"), os.path.join("csync", "live.py")}


def test_no_page_reads_the_generated_folder_directly():
    bad = []
    for d, _, files in os.walk(os.path.join(ROOT, "csync")):
        for f in files:
            if not f.endswith(".py"):
                continue
            rel = os.path.relpath(os.path.join(d, f), ROOT)
            with open(os.path.join(d, f), encoding="utf8") as fh:
                code = fh.read()
            if rel not in ALLOWED and re.search(r"""["']data["']\s*,\s*["']out["']|data/out/""", code.split('"""', 2)[-1]):
                bad.append(rel)
    assert not bad, bad


def test_technologies_page_opens_on_a_clean_clone(tmp_path, monkeypatch):
    import json
    import shutil
    from streamlit.testing.v1 import AppTest
    src = os.path.join(ROOT, "data", "out")
    hidden = tmp_path / "out_hidden"
    if os.path.isdir(src):
        shutil.move(src, hidden)   # simulate the hosted app: no generated folder at all
    try:
        monkeypatch.setenv("CSYNC_OUT_DIR", str(tmp_path / "empty"))
        with open(os.path.join(ROOT, "csync/config/strings_en.json"), encoding="utf8") as fh:
            ui = json.load(fh)["ui"]
        at = AppTest.from_file(os.path.join(ROOT, "csync/ui/app.py"), default_timeout=180)
        at.session_state["cs-hook-done"] = True
        at.session_state["cs-bot-done"] = True
        at.session_state["cs-nav"] = ui["tab_tech"]
        at.run()
        assert not at.exception, at.exception
    finally:
        if hidden.exists():
            shutil.move(str(hidden), src)
