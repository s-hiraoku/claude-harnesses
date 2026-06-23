# Verification Log

Use this file to record meaningful verification runs.

## Template

### YYYY-MM-DD HH:MM

- Command:
- Scope:
- Result:
- Notes:

## Runs

### 2026-06-23 22:25 JST

- Command: `PATH=/tmp/claude-harnesses-pr9-venv/bin:$PATH bash scripts/verify.sh`
- Scope: PR #9 pr-guardian mergeability gate hardening, inline review comment coverage, and `evals/pr-guardian` ledger coverage.
- Result: Passed. `ruff check .`, `pytest` (36 passed), and `mkdocs build --strict` completed.
- Notes: A first plain `bash scripts/verify.sh` attempt failed because the system Python loaded an incompatible `rpds` wheel (`x86_64` instead of `arm64e` or `arm64`); reran through a temporary venv with CI dependencies.

### 2026-06-23 22:25 JST

- Command: `PATH=/tmp/claude-harnesses-pr9-venv/bin:$PATH bash scripts/validate-plugins.sh`
- Scope: Plugin validation after updating the pr-guardian pack command.
- Result: Passed. All plugin manifests validated and component paths stayed inside plugin roots.
- Notes: `jsonschema` emitted its upstream CLI deprecation warning.

### 2026-06-23 22:25 JST

- Command: `PATH=/tmp/claude-harnesses-pr9-venv/bin:$PATH python3 scripts/check-eval-coverage.py --base origin/main`
- Scope: Eval quality gate after adding `evals/pr-guardian/ledger.md`.
- Result: Passed. `ok: pr-guardian (ledger 2026-06-23)`.
- Notes: Also reported existing passing ledgers for `frontend-design`, `implement-to-merge-ready`, and `meta-packager`.

### 2026-06-23 21:15 JST

- Command: `python3 scripts/check-eval-coverage.py --base origin/main`
- Scope: Eval quality gate after teaching it to ignore deleted skills and updating the `meta-packager` ledger entry.
- Result: Passed. `ok: meta-packager (ledger 2026-06-23)`.
- Notes: Covers the CI failure where deleted `meta-promote` was incorrectly treated as needing an evaluation ledger.

### 2026-06-23 21:15 JST

- Command: `uvx --with pytest --with pytest-mock --with pytest-asyncio --with anyio --with jsonschema --with pyyaml pytest`
- Scope: Test suite after fixing the eval quality gate.
- Result: Passed. 36 tests passed.
- Notes: Added a regression test for ignoring deleted skills in the eval quality gate.

### 2026-06-23 21:15 JST

- Command: `uvx --with mkdocs --with mkdocs-material mkdocs build --strict`
- Scope: Documentation build after fixing the eval quality gate.
- Result: Passed.
- Notes: MkDocs strict build completed; Material for MkDocs emitted its upstream MkDocs 2.0 warning.

### 2026-06-23 21:03 JST

- Command: `bash scripts/verify.sh`
- Scope: Consolidated `meta-promote` into `meta-packager` and removed the duplicate skill/command/docs entry.
- Result: Failed after `ruff check .` passed.
- Notes: `pytest` failed during collection because the system Python loaded an incompatible `rpds` wheel (`x86_64` instead of `arm64e` or `arm64`).

### 2026-06-23 21:03 JST

- Command: `uvx --with pytest --with pytest-mock --with pytest-asyncio --with anyio --with jsonschema --with pyyaml pytest`
- Scope: Test suite after consolidating `meta-promote` into `meta-packager`.
- Result: Passed. 35 tests passed.
- Notes: Used an isolated `uvx` environment with architecture-compatible dependencies.

### 2026-06-23 21:03 JST

- Command: `uvx --with mkdocs --with mkdocs-material mkdocs build --strict`
- Scope: Documentation build after removing `meta-promote` docs and nav entries.
- Result: Passed.
- Notes: MkDocs strict build completed; Material for MkDocs emitted its upstream MkDocs 2.0 warning.

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
