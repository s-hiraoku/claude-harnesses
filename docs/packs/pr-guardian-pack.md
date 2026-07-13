# pr-guardian-pack

Watch PRs after creation or resume stalled PRs. Loop over CI runs and human, bot, CodeRabbit, Codex, or agent review feedback, fix in batches, comment with the outcome.

## Skills

- `pr-guardian` — orchestrates CI monitoring and complete feedback recovery, re-observes successful open PRs for late reviews, and verifies current-head bot evidence through REST review `commit_id` values.
- `fix-ci` — diagnose and repair failing CI checks by cluster.

## Subagent

- `ci-fixer` — parses `gh run view --log-failed`, classifies failures, applies one-cluster-per-commit fixes.

## Commands

- `/pr-guardian [PR#]`
- `/fix-ci [run-id]`

## Loop control

- Caps at 5 attempts.
- Each iteration writes a dated note to `ledger/current.md`.
- Stops only after required checks pass, requested changes are cleared, actionable review threads are handled, and `mergeStateStatus` is no longer blocking. `mergeable: MERGEABLE` alone is not sufficient.
- Also stops when a fix attempt does not change the failure mode or when a real blocker is identified.

Install: `claude /plugin install pr-guardian-pack@claude-harnesses`
