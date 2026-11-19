"""Static checks that need no running app: lint rules of ruff.toml, and the shared rule parameters stay untouched."""
import dataclasses
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_ruff_reports_nothing_on_csync():
    ruff = shutil.which("ruff")
    assert ruff, "ruff missing: pip install -r requirements-dev.txt"
    r = subprocess.run([ruff, "check", "csync"], cwd=ROOT, capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout + r.stderr


def test_shared_default_parameters_are_not_mutated_by_a_full_story_run():
    """rules.py keeps a Params() default argument (frozen rule v3). Running every crew must leave the defaults as written."""
    from csync import crew, rules
    before = dataclasses.asdict(rules.Params())
    for day in range(1, 11):
        crew.board(day)
    rules.evaluate(crew.member_series(crew.MEMBERS[0][0]))
    assert dataclasses.asdict(rules.evaluate.__defaults__[0]) == before
    assert dataclasses.asdict(rules.Params()) == before
    assert sys.modules["csync.rules"].PROPOSED == rules.Params()
