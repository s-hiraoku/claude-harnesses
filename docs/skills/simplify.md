# simplify

Review changed code on the current branch for reuse, clarity, and dead complexity. Apply minimal cleanup.

## Workflow

1. List changed files: `git diff origin/main...HEAD --stat`.
2. For each meaningful file, ask:
   - Is there an existing helper that does this already?
   - Are there abstractions or layers the change does not need yet?
   - Error handling for cases that cannot occur?
   - Comments restating what code already says?
   - Unused variables, imports, or branches?
3. Apply minimal, behavior-preserving cleanups.
4. Re-run targeted tests for each touched module.

## Constraints

- No new abstractions during simplify (that's a separate refactor).
- Preserve public APIs and observable behavior exactly.
- Risky cleanups go in the report, not the diff.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses simplify --scope project
```

Part of `review-pack`.
