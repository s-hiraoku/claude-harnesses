# Repository Guidance

This repository contains harness examples for Claude Code-driven software development. Keep changes concise, practical, and developer-facing.

## Principles

- Prefer deterministic checks over vague instructions.
- Separate durable guidance, reusable workflows, external tools, task memory, enforcement, and verification.
- Keep `CLAUDE.md` templates small enough to remain useful over time.
- Treat hooks as examples unless they are explicitly hardened and integrated.
- Skills, hooks, agents, and slash commands are first-class. The `.claude-plugin/marketplace.json` index is the canonical distribution surface.
- Do not describe this repository as a multi-agent router.

## Editing Expectations

- Update `README.md` or `docs/` when adding or changing harness concepts.
- Keep skill files focused on reusable task workflows.
- Keep settings presets readable and conservative by default.
- Avoid over-engineering. This repository should remain easy to copy from.

## Local Harness

This repository dogfoods its strict harness:

- Treat `settings/strict.json` as the repository safety posture for plugins running against it.
- Use `scripts/verify.sh` as the final repository-level verification command.
- Use `ledger/` for long-running, security-sensitive, risky, or interrupted work.
- Record meaningful verification runs in `ledger/verification.md` when a task relies on them.

## Verification

- Run relevant checks before finalizing changes.
- Prefer `bash scripts/verify.sh` as the repository-level check.
- Summarize changed files, verification results, and known risks in the final response.
