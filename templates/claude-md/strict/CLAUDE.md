# Repository Guidance

This repository expects conservative, verified changes. Treat behavior as load-bearing.

## Principles

- Make the smallest change that solves the problem.
- Never modify shared infrastructure, migrations, or release artifacts without explicit confirmation.
- Run `bash scripts/verify.sh` before claiming completion.

## Editing Expectations

- Inspect the existing patterns before adding new ones.
- Preserve public APIs, data formats, and observable behavior.
- Add or update tests for behavior changes.
- Update docs when commands, configuration, or APIs change.

## Local Harness

- Settings preset: `.claude/settings.json` matches `claude-harnesses/settings/strict.json` (default mode: `plan`).
- Long-running work uses `ledger/` for resumable state.

## Verification

- Repository-level: `bash scripts/verify.sh`.
- Targeted: re-run only the tests that touch changed modules during work.
- Summarize changed files, verification, and remaining risks in the final response.
