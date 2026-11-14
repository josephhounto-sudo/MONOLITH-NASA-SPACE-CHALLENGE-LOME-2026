"""Validate JSON files against the contracts. Usage: python scripts/validate_contracts.py"""
import json, os, glob, sys
from jsonschema import Draft202012Validator
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schemas = {os.path.basename(p).split(".")[0]: json.load(open(p)) for p in glob.glob(os.path.join(ROOT, "contracts", "*.schema.json"))}
targets = [("procedure_file", glob.glob(os.path.join(ROOT, "data", "procedures", "*.json"))),
           ("scenario_file", glob.glob(os.path.join(ROOT, "data", "scenarios", "*.json")))]
bad = 0
for name, files in targets:
    v = Draft202012Validator(schemas[name])
    for f in files:
        errs = list(v.iter_errors(json.load(open(f, encoding="utf8"))))
        print(("OK   " if not errs else "FAIL ") + os.path.relpath(f, ROOT), *[e.message for e in errs[:3]])
        bad += bool(errs)
for n, s in schemas.items():
    Draft202012Validator.check_schema(s)
print(f"{len(schemas)} schemas valid; {bad} file(s) failing")
sys.exit(1 if bad else 0)
