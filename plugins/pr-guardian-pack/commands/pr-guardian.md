---
description: Watch a PR until it is mergeable. Loops over CI runs and review feedback, dispatching fixes via subagents.
argument-hint: "[PR number]"
---

Run the `pr-guardian` skill against PR $ARGUMENTS (or the current branch's PR if empty).

Loop:

1. `gh pr checks` and `gh pr view`.
2. If CI is failing, delegate to the `ci-fixer` subagent with the failing-job log.
3. Address actionable review feedback.
4. Push fixes; re-check.
5. Stop when mergeable, when 5 attempts have been made, or when a real blocker is identified.

Record dated progress in `ledger/current.md` after each iteration.
