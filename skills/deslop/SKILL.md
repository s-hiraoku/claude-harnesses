---
name: deslop
description: Remove AI-generated boilerplate (vague comments, unused try/except, defensive validation, restated docstrings) from changed code without changing behavior.
---

# Deslop

Use this workflow when changes on the current branch contain visibly LLM-generated patterns that hurt readability or maintainability.

## Common slop signatures

- Comments that restate the next line verbatim.
- `try`/`except Exception` that re-raises with a wrapper message and no other handling.
- Input validation for cases the type system already rules out.
- "Helper" functions used exactly once.
- Multi-paragraph docstrings on private functions.
- "Added for issue #N" / "Used by foo" comments that bind code to the conversation.
- Unreachable defensive branches (`if config is not None` after a non-Optional construction).

## Workflow

1. List changed files: `git diff origin/main...HEAD --name-only`.
2. For each non-trivial file, read the diff and look for the signatures above.
3. Apply minimal removals. Preserve every observable behavior.
4. Re-run targeted tests for each touched module.

## Constraints

- Do not delete genuine error handling at system boundaries (HTTP, subprocess, file IO).
- Do not delete comments that explain a non-obvious WHY.
- If unsure, leave it and propose the removal in the report.

## Final Report

- files changed
- slop categories removed (one line each)
- tests run and result
- proposals not applied
