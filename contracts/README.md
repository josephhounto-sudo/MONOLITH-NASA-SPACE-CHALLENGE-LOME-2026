# Contracts (draft v0 — 14/11/2026, to be validated by M1 on Saturday 09:00-11:00)
Four base contracts: `measurement`, `dimension_state`, `decision`, `decision_capsule`.
Three merged formats: `scenario_file`, `send_envelope`, `procedure_file`.
Two settings files (no logic): `csync/config/theme.json`, `csync/config/strings_en.json`.
Golden rule: **the UI only reads the capsule.** For an emergency the capsule designates the procedure; the procedure text is a fixed file.
Changing a contract = ask M1, update the schema, update tests, announce it in the group.
