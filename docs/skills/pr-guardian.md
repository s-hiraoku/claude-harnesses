# pr-guardian

Watch a PR after creation or resume a stalled PR. Loop over CI runs and human, bot, CodeRabbit, Codex, or agent review feedback, fix in batches, comment with the outcome.

## Workflow

1. Identify the PR, branch, remote, base.
2. Check initial state with `gh pr view`, `gh pr checks`, recent comments, reviews, and inline review comments.
3. Watch CI with `gh run watch`.
4. When CI fails, delegate cluster-level diagnosis to the `ci-fixer` subagent.
5. Build a complete feedback inventory and classify each item as `fix`, `respond`, `ignore`, or `blocked`.
6. Address all `fix` items with focused commits. Don't broaden scope.
7. Explain `respond` and `ignore` items in review replies or the outcome comment.
8. Run the adjacent audit reference's executable GraphQL cursor loops for review threads and nested comments, and exhaust its REST pagination commands for reviews, comments, checks, and annotations.
9. Use paginated REST review `commit_id` values to prove expected bot reviews target the current head; `gh pr view` review objects are not sufficient evidence.
10. Push fixes from an isolated worktree only while the remote head still matches the pinned SHA; repeat until checks pass, requested changes are cleared, actionable threads are handled, or a real blocker remains.
11. Keep successful open PRs under durable observation so a same-head late review reactivates the guardian, then comment with the final outcome.

## Loop control

- Cap retries at 5 unless the user explicitly asks for more.
- If the same CI failure or review comment returns after two fixes, inspect the underlying assumption before trying again.
- Record a dated note in `ledger/current.md` after each iteration.
- Stop and surface to the human on environmental/infrastructure failures.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses pr-guardian --scope project
```

Part of `pr-guardian-pack`. Slash command: `/pr-guardian`.
