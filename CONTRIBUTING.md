# Contributing

This repository is a harness collection for Claude Code-driven software development. Contributions should keep the repository practical, copyable, and easy to verify.

## What Fits

Good contributions include:

- concise `CLAUDE.md` templates
- focused skills with valid `SKILL.md` frontmatter
- hook examples with clear limits and tests
- plugin manifests that validate against `schemas/plugin.schema.json`
- settings presets that validate against `schemas/settings.schema.json`
- ledger templates and operating patterns
- verification scripts and tests that prevent template drift
- docs that clarify how to adopt or safely adapt the harnesses

Avoid adding a multi-agent router, production hook runtime, or broad framework unless the repository scope changes explicitly.

## Change Guidelines

- Keep examples small enough to copy.
- Keep docs concise and developer-facing.
- Prefer deterministic checks over prose-only expectations.
- Make limits explicit, especially for safety and security examples.
- Update README or docs when adding a new harness type or adoption path.
- Add or update tests when changing hooks, plugins, examples, skills, scripts, or docs links.

## Verification

Before proposing a change, run:

```sh
CLAUDE_HARNESSES_STRICT=1 bash scripts/verify.sh
```

For local development, install dev dependencies first:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Then run:

```sh
.venv/bin/ruff check .
.venv/bin/pytest
```

Do not claim verification passed unless the command completed successfully.

## Skill Changes

Each skill must live in `skills/<name>/SKILL.md` and include frontmatter with:

```yaml
---
name: <name>
description: <when to use this skill>
---
```

Keep skill bodies focused on workflow, verification, and final reporting.

`name` must equal the directory name. `description` must fit on a single line. The repo root `skills/` directory is the canonical home so that `gh skill install` and `npx skills add` work; plugins reference these skills via relative symlinks.

## Hook Changes

Hooks in this repository are examples. When adding or changing a hook:

- document what it blocks and what it does not block
- avoid printing secret values
- return deterministic exit codes (0 = pass, 2 = block, anything else = non-blocking error)
- honor `CLAUDE_HARNESSES_DISABLE=1` as a kill switch
- add tests for allowed and blocked cases
- update `docs/hook-hardening.md` if the hardening guidance changes

## Plugin Changes

Each plugin under `plugins/<name>/` must include `.claude-plugin/plugin.json` validated against `schemas/plugin.schema.json`. The repo-level marketplace index is `.claude-plugin/marketplace.json`. Update both when adding a pack.
