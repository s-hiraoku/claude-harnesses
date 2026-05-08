# fix-ci

Diagnose and repair failing CI checks on the current PR. Reach green or document a real blocker.

## Workflow

1. List failing checks: `gh pr checks` and `gh run list --branch $(git branch --show-current) --limit 5`.
2. Fetch failing-job logs: `gh run view <run-id> --log-failed`.
3. Cluster failures by type: build/type errors, lint/format, tests, infra/deps.
4. Apply the smallest fix per cluster. One cluster per commit.
5. Loop with a hard cap (default 5 attempts). Record dated notes in `ledger/current.md` between attempts.
6. Surface to the human when failure mode does not change between attempts, or when the failure is environmental.

## Constraints

- Never disable or skip tests as a fix unless explicitly authorized.
- Treat suspected flakes by re-running once; otherwise treat as real.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses fix-ci --scope project
```

Part of `pr-guardian-pack`. Slash command: `/fix-ci`. Delegates to the `ci-fixer` subagent.
