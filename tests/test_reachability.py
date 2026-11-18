"""No dead module: every csync module must be reachable from an entry point the product runs.

Entry points: the Streamlit app, scripts/run_story.py (the app executes it to build the story files) and the new assistant.
A module that nothing reaches is either wired in or deleted. KNOWN_ORPHANS is a ratchet: it may only shrink, each entry has
a reason and an exit, and the test fails if an entry becomes reachable (remove it) or if a NEW orphan appears.
"""
import ast
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRY_POINTS = ["csync/ui/app.py", "scripts/run_story.py"]
# module -> why it is still here and when it must be wired in or deleted
KNOWN_ORPHANS = {
    "csync.memory": "append-only local memory; consumer to be the mission simulator (on-board record that survives restart); delete if the simulator does not use it by the V2 release",
    "csync.assistant": "scripted assistant, tested but not yet shown; to wire into the story screens before the V2 release",
}


def module_path(mod):
    p = os.path.join(ROOT, *mod.split("."))
    for cand in (p + ".py", os.path.join(p, "__init__.py")):
        if os.path.exists(cand):
            return cand
    return None


def imports_of(path):
    tree = ast.parse(open(path, encoding="utf8").read())
    found = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            found |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            found.add(n.module)
            found |= {f"{n.module}.{a.name}" for a in n.names}
    return found


def reachable():
    seen, todo = {"csync.ui.app"}, []      # entry points count as reached
    for rel in ENTRY_POINTS:
        todo.append(os.path.join(ROOT, rel))
    while todo:
        path = todo.pop()
        for mod in imports_of(path):
            if mod.split(".")[0] not in ("csync", "synthetic"):
                continue
            p = module_path(mod)
            if p and mod not in seen:
                seen.add(mod)
                todo.append(p)
    return seen


def all_csync_modules():
    mods = set()
    for dirpath, _, files in os.walk(os.path.join(ROOT, "csync")):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                rel = os.path.relpath(os.path.join(dirpath, f), ROOT)[:-3]
                mods.add(rel.replace(os.sep, "."))
    return mods


def test_no_new_orphan_module():
    orphans = all_csync_modules() - reachable()
    assert orphans == set(KNOWN_ORPHANS), f"unreachable csync modules: {sorted(orphans)}; allowed: {sorted(KNOWN_ORPHANS)}"


def test_every_known_orphan_has_a_reason_and_an_exit():
    for mod, why in KNOWN_ORPHANS.items():
        assert module_path(mod), f"{mod} no longer exists: remove it from KNOWN_ORPHANS"
        assert len(why.split()) >= 8 and ("wire" in why or "delete" in why), mod


# ---- dead public functions and classes: same ratchet (used by no product code; tests alone do not count) ----
KNOWN_UNUSED = {
    "pmdata_measurements": "PhysioNet adapter; consumer = research/analog_pmdata.py (research script, not the app); keep only while that script exists",
    "LocalMemory": "same module as csync.memory; follows its decision: wire into beat 4 with a restart test, or delete",
}


def unused_public_names():
    import glob
    import re
    code_files = glob.glob(os.path.join(ROOT, "csync", "**", "*.py"), recursive=True) + \
        glob.glob(os.path.join(ROOT, "scripts", "*.py")) + glob.glob(os.path.join(ROOT, "synthetic", "*.py"))
    text = {f: open(f, encoding="utf8").read() for f in code_files}
    alltext = "".join(text.values())
    out = set()
    for f in glob.glob(os.path.join(ROOT, "csync", "**", "*.py"), recursive=True):
        for n in ast.parse(text[f]).body:
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith("_"):
                if len(re.findall(r"\b" + n.name + r"\b", alltext)) - 1 <= 0:
                    out.add(n.name)
    return out


def test_no_new_dead_function():
    assert unused_public_names() == set(KNOWN_UNUSED), \
        f"public names no product code uses: {sorted(unused_public_names())}; allowed: {sorted(KNOWN_UNUSED)}"
