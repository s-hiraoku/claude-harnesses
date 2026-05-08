# pr-guardian-pack

Watch PRs after creation. Loop over CI runs and review feedback, fix in batches, comment with the outcome.

## Skills

- `pr-guardian` — orchestrates the watch loop, with a hard cap of 5 retries and ledger updates per iteration.
- `fix-ci` — diagnose and repair failing CI checks by cluster.

## Subagent

- `ci-fixer` — parses `gh run view --log-failed`, classifies failures, applies one-cluster-per-commit fixes.

## Commands

- `/pr-guardian [PR#]`
- `/fix-ci [run-id]`

## Loop control

- Caps at 5 attempts.
- Each iteration writes a dated note to `ledger/current.md`.
- Stops when mergeable, when a fix attempt does not change the failure mode, or when a real blocker is identified.

Install: `claude /plugin install pr-guardian-pack@claude-harnesses`
