# pr-guardian

Watch a PR after creation. Loop over CI runs and review feedback, fix in batches, comment with the outcome.

## Workflow

1. Identify the PR, branch, remote, base.
2. Check initial state with `gh pr view`, `gh pr checks`, recent comments.
3. Watch CI with `gh run watch`.
4. When CI fails, delegate cluster-level diagnosis to the `ci-fixer` subagent.
5. Address actionable feedback with focused commits. Don't broaden scope.
6. Push fixes; repeat until checks pass or a real blocker remains.
7. Comment on the PR with what changed and which feedback was addressed.

## Loop control

- Cap retries at 5 unless the user explicitly asks for more.
- Record a dated note in `ledger/current.md` after each iteration.
- Stop and surface to the human on environmental/infrastructure failures.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses pr-guardian --scope project
```

Part of `pr-guardian-pack`. Slash command: `/pr-guardian`.
