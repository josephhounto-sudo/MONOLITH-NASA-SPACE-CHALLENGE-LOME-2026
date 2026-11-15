import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# Clean clone: data/out/ is generated, not committed. Build it once so `pytest` alone works (15/11, found by a fresh-clone run).
import pytest


@pytest.fixture(scope="session", autouse=True)
def _story_outputs():
    here = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(here, "data", "out", "trends_histoire.json")):
        import subprocess
        subprocess.run([sys.executable, os.path.join(here, "scripts", "run_story.py")], cwd=here, check=True, capture_output=True)
