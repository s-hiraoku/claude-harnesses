# deslop

Remove AI-generated boilerplate (vague comments, unused try/except, defensive validation, restated docstrings) from changed code without changing behavior.

## Common slop signatures

- Comments that restate the next line verbatim.
- `try`/`except Exception` that re-raises with a wrapper message and no other handling.
- Input validation for cases the type system already rules out.
- "Helper" functions used exactly once.
- Multi-paragraph docstrings on private functions.
- "Added for issue #N" / "Used by foo" comments that bind code to the conversation.
- Unreachable defensive branches.

## Workflow

1. List changed files: `git diff origin/main...HEAD --name-only`.
2. For each non-trivial file, read the diff and look for the signatures above.
3. Apply minimal removals; preserve every observable behavior.
4. Re-run targeted tests.

## Constraints

- Don't delete genuine error handling at system boundaries (HTTP, subprocess, file IO).
- Don't delete comments that explain a non-obvious WHY.
- Unsure → leave it and propose the removal in the report.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses deslop --scope project
```

Bundled into `long-running-pack`.
