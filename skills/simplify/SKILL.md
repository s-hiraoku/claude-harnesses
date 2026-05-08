---
name: simplify
description: Review changed code on the current branch for reuse, clarity, and dead complexity, then propose or apply minimal cleanup without changing behavior.
---

# Simplify

Use this workflow after a feature is functionally complete but before review or merge, to remove avoidable complexity introduced during implementation.

## Workflow

1. List changed files: `git diff origin/main...HEAD --stat` and `git diff origin/main...HEAD --name-only`.
2. For each meaningful file, ask:
   - Is there an existing helper, type, or constant in the codebase that does this already? Search before adding.
   - Are there abstractions or layers that the change does not actually need yet?
   - Is there error handling for cases that cannot occur?
   - Are there comments restating what the code already says?
   - Are there unused variables, imports, or branches?
3. Apply minimal, behavior-preserving cleanups. Do not rewrite working code for stylistic reasons.
4. Re-run targeted tests for each touched module to confirm behavior is unchanged.

## Constraints

- Never introduce new abstractions during simplify — that is a separate refactor task.
- Preserve public APIs and observable behavior exactly.
- If a cleanup is risky, propose it in the final report instead of applying it.

## Final Report

Include:

- files cleaned up
- specific reductions (lines removed, helpers reused)
- tests run and result
- proposals not applied (with reasoning)
