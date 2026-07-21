# Verification Log

Use this file to record meaningful verification runs.

## Template

### YYYY-MM-DD HH:MM

- Command:
- Scope:
- Result:
- Notes:

## Runs

### 2026-07-20 (PR #25 Codex feedback fix)

- Command: `python3 scripts/sync-marketplace.py --check`; `ruff check .`; isolated `uv run --no-project --with pytest,jsonschema python -m pytest tests/`; isolated `uvx --with mkdocs-material mkdocs build --strict`
- Scope: Fixed two Codex P2 findings on PR #25. (1) `referenced_agents` only scanned `SKILL.md`, missing subagent references that live in the skill's slash command body (e.g. `fix-ci.md` delegates to `ci-fixer`, but `skills/fix-ci/SKILL.md` never mentions it) — now scans SKILL.md + the bundled command file. (2) Compatibility-alias skills (e.g. `finish-pr-feedback`, which immediately delegates to `pr-guardian`) published as standalone `skill-*` plugins shipped only the alias pointer with nothing to run — `alias_target()` now parses "alias for <skill>" from the frontmatter description and bundles the target skill/command/agents alongside the alias.
- Result: Passed. Sync check in sync, Ruff passed, 77 tests passed, MkDocs strict build completed. `plugins/skill-fix-ci` now includes `agents/ci-fixer.md`; `plugins/skill-finish-pr-feedback` now includes `skills/pr-guardian`, `commands/pr-guardian.md`, and `agents/ci-fixer.md`.
- Notes: Plain pytest inside `scripts/verify.sh` still fails collection on this machine due to the known x86_64 `rpds` wheel under arm64; the isolated arm64 run passed.

### 2026-07-20 (marketplace 3-tier restructure)

- Command: `python3 scripts/sync-marketplace.py --check`; `ruff check .` (via `bash scripts/verify.sh`); isolated `uv run --no-project --with pytest,jsonschema python -m pytest tests/`; isolated `uvx --with mkdocs-material mkdocs build --strict`
- Scope: New `scripts/sync-marketplace.py` generator producing a real `plugins/full` umbrella (all skills/commands/agents plus merged hooks), 25 `plugins/skill-*` micro-plugins, and a regenerated `.claude-plugin/marketplace.json` (38 entries); drift check wired into `scripts/verify.sh`; docs updated for the full/pack/skill install tiers.
- Result: Passed. Sync check in sync, Ruff passed, 77 tests passed (including install-safety invariants over the generated plugins), MkDocs strict build completed.
- Notes: Plain pytest inside `scripts/verify.sh` still fails collection on this machine due to the known x86_64 `rpds` wheel under arm64; the isolated arm64 run passed.

### 2026-07-19 11:49 JST

- Command: `bash scripts/verify.sh`; isolated `uvx` full pytest; isolated `uvx` MkDocs strict build; `python3 scripts/check-eval-coverage.py --base FETCH_HEAD`; isolated `uv run --no-project` plugin validation; `git diff --check`
- Scope: PR #24 follow-up for eval coverage, review-pack distribution, and review-briefing contract fixes.
- Result: Passed with isolated verification. Ruff passed, 39 tests passed, MkDocs strict build completed, eval coverage passed, plugin manifests and component paths validated, and the diff whitespace check passed.
- Notes: Plain pytest in `scripts/verify.sh` failed during collection because the system Python loaded the known incompatible x86_64 `rpds` wheel under arm64. Isolated architecture-compatible dependencies passed; Material for MkDocs emitted its upstream MkDocs 2.0 warning.
### 2026-07-19 12:35 JST

- Command: isolated full pytest; isolated MkDocs strict build; `ruff check .`; `python3 scripts/check-eval-coverage.py --base origin/main`; `git diff --check`
- Scope: PR #22 review follow-up updating the adviser eval harness for deterministic Fable routing and converging the clarified prompt contract.
- Result: Passed. 77 tests passed, MkDocs strict build completed, Ruff passed, eval coverage passed, and the diff whitespace check passed.
- Notes: Empirical prompt tuning converged at 3/3 scenarios and 100% accuracy after two fresh post-fix hold-outs. Material for MkDocs emitted its upstream MkDocs 2.0 warning.

### 2026-07-16 08:12 JST

- Command: `ruff check skills/adviser/scripts tests/test_adviser_routing.py tests/test_install_sh.py`; `pytest -q tests/test_adviser_routing.py tests/test_install_sh.py`; live `run_adviser.py` smoke test with a simulated nested Claude environment; `uvx --with pytest --with pytest-mock --with pytest-asyncio --with anyio --with jsonschema --with pyyaml pytest -q`; `uvx --with mkdocs --with mkdocs-material mkdocs build --strict`; isolated `scripts/validate-plugins.sh`; `quick_validate.py skills/adviser`; `git diff --check`
- Scope: Deterministic Claude Adviser model and effort routing, fail-closed runner isolation, packaging, and documentation.
- Result: Passed. Targeted tests passed with 44 tests, the isolated full suite passed with 77 tests, and live runner checks resolved Sonnet/medium to `claude-fable-5`/medium and Fable/high to `claude-fable-5`/xhigh with zero tools. Plugin manifests and paths validated, the skill validator passed, MkDocs strict build completed, and the diff whitespace check passed.
- Notes: Plain `bash scripts/verify.sh` reached pytest after Ruff passed but collection hit the known system `rpds` architecture mismatch (`x86_64` wheel on arm64). The equivalent isolated arm64 run passed. Claude Code 2.1.210 exposes the effective model but not effective effort in stream JSON, so the runner records effort as requested but not independently verified.

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

### 2026-07-20 12:49 JST

- Command: `uv run --no-project --with-requirements requirements-dev.txt bash scripts/verify.sh`
- Scope: review-briefing skill — switched step-5 output to a self-contained HTML briefing opened in the browser (new `references/briefing-template.html`, terminal fallback kept), plus docs wording update.
- Result: Passed. `sync-marketplace --check` in sync, `ruff check .`, 78 pytest tests, and `mkdocs build --strict` completed.
- Notes: Plain `bash scripts/verify.sh` still hits the host-only x86_64 `rpds` wheel ImportError under arm64; the isolated requirements environment avoids it. Template HTML tag balance verified with a small html.parser script.

### 2026-07-21 08:11 JST

- Command: `uv run --no-project --with-requirements requirements-dev.txt bash scripts/verify.sh`
- Scope: review-briefing PR #31 — addressed CodeRabbit finding (HTML-escape PR-derived data before templating to prevent local XSS); added escape instructions to SKILL.md step 5 and a reminder comment to briefing-template.html.
- Result: Passed. sync-marketplace --check in sync, ruff, 78 pytest tests, mkdocs build --strict; template tag balance re-verified.

### 2026-07-21 (low-cognitive-load briefing format)

- Command: `uv run --no-project --with-requirements requirements-dev.txt bash scripts/verify.sh`
- Scope: review-briefing — replaced the briefing HTML template and canonical format with a low-cognitive-load layout (verdict → basis → importance-ordered points with badges → collapsed trade-offs/verification), and made "lead with the conclusion, defer the detail" a must-fire principle in SKILL.md so the format is reproducible across environments instead of model-improvised. Reason: an earlier all-sections-equal briefing pushed triage back onto the human, and the good pr275 layout only existed as an ad-hoc render, so it varied by environment.
- Result: Passed. sync-marketplace --check in sync, ruff, 78 pytest tests, mkdocs build --strict. Template tag balance verified with html.parser (no unclosed tags, no mismatches).
- Notes: Plain `bash scripts/verify.sh` still hits the host-only x86_64 `rpds` ImportError under arm64; the isolated uv env avoids it. Only HTML/Markdown skill files changed — no Python.
