# review

Bug-first, risk-focused review workflow before merge or release.

## Workflow

1. Identify the review scope: diff, files, commit range, pull request, or task goal.
2. Inspect changed behavior before style or cleanup concerns.
3. Prioritize bugs, regressions, security risks, data-loss risks, and missing verification.
4. Check whether tests, docs, migrations, and release notes match the behavioral impact.
5. Look for edge cases around empty input, permissions, concurrency, rollback, and failure paths.
6. Keep findings specific, reproducible, and tied to exact files or lines when possible.
7. Avoid broad refactor suggestions unless they block correctness, safety, or maintainability.
8. If no issues are found, say so clearly and note remaining test gaps or residual risk.

For large diffs, the skill delegates per-area passes to parallel `code-reviewer` subagents (one per concern: correctness, security, performance, tests) and combines findings.

## Final report

Lead with severity-ranked findings. For each: severity, file:line, what can fail, why it matters, fix direction. End with verification reviewed and a one-line verdict.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses review --scope project
```

Part of `review-pack`. Slash command: `/review`.
