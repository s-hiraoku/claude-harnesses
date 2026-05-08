---
description: Run a structured code review of the current branch or a named PR using the review skill.
argument-hint: "[PR number or 'branch']"
---

Run the `review` skill against $ARGUMENTS (or the current branch if empty).

If the diff is large (>30 changed files), spawn multiple `code-reviewer` subagents in parallel — one per concern (correctness, security, performance, tests) — and combine their findings.

Lead the response with the severity-ordered findings list, then a one-line verdict.
