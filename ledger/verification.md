# Verification Log

Use this file to record meaningful verification runs.

## Template

### YYYY-MM-DD HH:MM

- Command:
- Scope:
- Result:
- Notes:

## Runs

### 2026-06-06 09:07 JST

- Command: `PATH="/Volumes/SSD/ghq/github.com/s-hiraoku/claude-harnesses/.venv/bin:$PATH" bash scripts/verify.sh`
- Scope: Added the `@scofieldfree/excalidraw-mcp` recipe to `mcp-pack`, plus marketplace and docs references.
- Result: Passed. `ruff check .`, `pytest` (34 passed), and `mkdocs build --strict` completed.
- Notes: A first plain `bash scripts/verify.sh` attempt failed because the global Python imported an x86_64 `rpds` extension under arm64 Python; rerunning through the repository `.venv` used the correct architecture.

### 2026-06-04

- Command: `.venv/bin/python -m pytest -q` and `bash scripts/validate-plugins.sh`
- Scope: Plugin marketplace install-safety after wiring shared skills + `_shared` hook helpers via in-plugin symlinks and rewriting manifests to the documented spec (no `components` wrapper, `dependencies` not `dependsOn`).
- Result: 34 passed; all plugin manifests validate; all component paths stay inside their plugin root. Negative test confirmed both gates fail on a dangling skill symlink. Hook smoke test: `secret-guard.py` allows a clean command and blocks an AWS key via the relocated `_shared/envelope.py` import.
- Notes: System `python3` lacks `jsonschema`; CI installs it (`plugin-validate.yml`). `scripts/verify.sh` runs the plugin tests transitively via pytest (pyproject.toml detected).
