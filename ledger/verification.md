# Verification Log

Use this file to record meaningful verification runs.

## Template

### YYYY-MM-DD HH:MM

- Command:
- Scope:
- Result:
- Notes:

## Runs

### 2026-07-12 23:30 JST

- Command: `python -m pytest tests/test_skills.py -q`; `PATH=/tmp/pr20-verify-venv/bin:$PATH bash scripts/verify.sh`; `git diff --check`
- Scope: PR #20 follow-up to resolve the target PR and project before starting the durable PR Guardian runner.
- Result: Passed. Targeted skill tests passed with 4 tests, the repository verification suite passed with 39 tests, and the diff whitespace check passed.
- Notes: The plain repository verification initially hit the known system `rpds` architecture mismatch. The passing run used an isolated arm64-compatible environment; MkDocs was unavailable and was skipped by the non-strict verification script.

### 2026-06-28 08:14 JST

- Command: `ruff check .`; `pytest tests/test_plugins.py tests/test_skills.py`; `uvx --with pytest --with pytest-mock --with pytest-asyncio --with anyio --with jsonschema --with pyyaml pytest tests/test_plugins.py tests/test_skills.py`; `uvx --with pytest --with pytest-mock --with pytest-asyncio --with anyio --with jsonschema --with pyyaml pytest`; `uvx --with mkdocs --with mkdocs-material mkdocs build --strict`; `git diff --check`
- Scope: PR #11 `pr-guardian` follow-up after Codex review requested bundling `pr-guardian` with `product-pack`.
- Result: Passed with isolated verification. Ruff passed, targeted plugin/skill tests passed with 10 tests, full pytest passed with 36 tests, MkDocs strict build completed, and diff whitespace check passed.
- Notes: Plain `pytest tests/test_plugins.py tests/test_skills.py` failed during collection because the system Python loaded an incompatible `rpds` wheel (`x86_64` instead of `arm64e` or `arm64`). The equivalent isolated `uvx` run passed. Material for MkDocs emitted its upstream MkDocs 2.0 warning.

### 2026-06-27 16:12 JST

- Command: `bash scripts/verify.sh`
- Scope: Consolidated PR feedback recovery into `pr-guardian`.
- Result: Failed after `ruff check .` passed.
- Notes: `pytest` failed during collection because the system Python loaded an incompatible `rpds` wheel (`x86_64` instead of `arm64e` or `arm64`).

### 2026-06-27 16:12 JST

- Command: `ruff check .`; `git diff --cached --check`; `uvx --with pytest --with pytest-mock --with pytest-asyncio --with anyio --with jsonschema --with pyyaml pytest`; `uvx --with mkdocs --with mkdocs-material mkdocs build --strict`
- Scope: Consolidated PR feedback recovery into `pr-guardian`, retained `finish-pr-feedback` as a compatibility alias, and updated related docs/commands.
- Result: Passed. Ruff passed, staged diff whitespace check passed, pytest passed with 36 tests, and MkDocs strict build completed.
- Notes: Used isolated `uvx` environments for pytest and MkDocs to avoid the system `rpds` architecture mismatch. Material for MkDocs emitted its upstream MkDocs 2.0 warning.

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

### 2026-07-18 10:05 JST

- Command: `uv run --no-project --with-requirements requirements-dev.txt bash scripts/verify.sh`
- Scope: executable PR Guardian GraphQL/REST pagination audit, adjacent-reference contract checks, plugin command, skill/pack docs, and tests.
- Result: passed
- Notes: `ruff check .`, 39 pytest tests, and `mkdocs build --strict` passed. A preceding plain `bash scripts/verify.sh` run stopped during collection because the system Python loaded an incompatible x86_64 `rpds` wheel under arm64e; the isolated requirements environment removed that host-only failure.

### 2026-06-04

- Command: `.venv/bin/python -m pytest -q` and `bash scripts/validate-plugins.sh`
- Scope: Plugin marketplace install-safety after wiring shared skills + `_shared` hook helpers via in-plugin symlinks and rewriting manifests to the documented spec (no `components` wrapper, `dependencies` not `dependsOn`).
- Result: 34 passed; all plugin manifests validate; all component paths stay inside their plugin root. Negative test confirmed both gates fail on a dangling skill symlink. Hook smoke test: `secret-guard.py` allows a clean command and blocks an AWS key via the relocated `_shared/envelope.py` import.
- Notes: System `python3` lacks `jsonschema`; CI installs it (`plugin-validate.yml`). `scripts/verify.sh` runs the plugin tests transitively via pytest (pyproject.toml detected).
