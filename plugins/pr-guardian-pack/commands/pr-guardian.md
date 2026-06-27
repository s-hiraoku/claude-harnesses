---
description: Watch or resume a PR until it is mergeable. Loops over CI runs and review feedback, dispatching fixes via subagents.
argument-hint: "[PR number]"
---

Run the `pr-guardian` skill against PR $ARGUMENTS (or the current branch's PR if empty).

Loop:

1. `gh pr checks` and `gh pr view --json mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,reviews,comments`.
2. If CI is failing, delegate to the `ci-fixer` subagent with the failing-job log.
3. Inventory human, bot, CodeRabbit, Codex, and agent feedback; classify each item as `fix`, `respond`, `ignore`, or `blocked`.
4. Address actionable feedback with focused commits and explain items not applied.
5. Push fixes; re-check.
6. Stop only when required checks pass, `reviewDecision` is not `CHANGES_REQUESTED`, actionable review threads are handled, and `mergeStateStatus` is no longer blocking. `mergeable: MERGEABLE` alone is not sufficient. Otherwise stop after 5 attempts or when a real blocker is identified.

Record dated progress in `ledger/current.md` after each iteration.
