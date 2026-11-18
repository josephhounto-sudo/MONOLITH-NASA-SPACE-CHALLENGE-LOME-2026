"""Dead code the product can still trip over.

Acceptance: `python -m vulture csync --min-confidence 80` prints no finding,
and csync.memory, csync.glyphs, and csync.sendqueue are still on disk
(they are not deleted without an explicit ask).

Five ways this pass fails:
1. vulture is not installed (the check cannot run).
2. a new unused name appears at confidence >= 80 (stale allow-list).
3. a name that an entry point still calls is deleted (glyphs, sendqueue).
4. the app or the story script no longer imports after the edit (cold start).
5. csync.memory is removed even though the task says to ask first.
"""
import ast
import importlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSYNC = os.path.join(ROOT, "csync")


def _source(rel):
    with open(os.path.join(ROOT, rel), encoding="utf8") as f:
        return f.read()


def test_vulture_is_installed():
    """Failure 1: the checker is missing, so a green pytest would hide dead code."""
    try:
        import vulture  # noqa: F401
    except ImportError as err:
        raise AssertionError("Install vulture, then re-run: python -m pip install vulture") from err


def test_vulture_min_confidence_80_reports_nothing():
    """Failure 2: an unused name at >= 80 confidence is still in csync/."""
    proc = subprocess.run(
        [sys.executable, "-m", "vulture", "csync", "--min-confidence", "80"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    report = (proc.stdout or "") + (proc.stderr or "")
    assert proc.returncode == 0, report.strip() or "vulture failed with no report"
    assert report.strip() == ""


def test_glyphs_and_sendqueue_still_have_a_caller():
    """Failure 3: deleting a symbol an entry point still calls."""
    app = _source("csync/ui/app.py")
    story = _source("scripts/run_story.py")
    assert "glyphs.orbit_inner" in app
    assert "from csync.sendqueue import" in story
    glyphs = ast.parse(_source("csync/glyphs.py"))
    queue = ast.parse(_source("csync/sendqueue.py"))
    glyph_names = {n.name for n in glyphs.body if isinstance(n, ast.FunctionDef)}
    queue_names = {n.name for n in queue.body if isinstance(n, ast.FunctionDef)}
    assert "orbit_inner" in glyph_names
    assert {"deliver", "message_id"} <= queue_names


def test_app_and_story_still_parse():
    """Failure 4: a cold start cannot import the entry points after a deletion."""
    ast.parse(_source("csync/ui/app.py"))
    ast.parse(_source("csync/ui/style.py"))
    ast.parse(_source("scripts/run_story.py"))
    for name in ("csync.glyphs", "csync.sendqueue", "csync.memory"):
        importlib.import_module(name)


def test_memory_module_is_kept():
    """Failure 5: memory is removed without an explicit ask."""
    assert os.path.isfile(os.path.join(CSYNC, "memory.py"))
    mem = ast.parse(_source("csync/memory.py"))
    classes = {n.name for n in mem.body if isinstance(n, ast.ClassDef)}
    assert "LocalMemory" in classes
