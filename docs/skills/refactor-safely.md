# refactor-safely

Refactor code without behavior changes using small mechanical steps and verification.

## Workflow

1. Identify the current behavior and public interfaces.
2. Avoid broad rewrites unless they are explicitly justified.
3. Make small mechanical changes.
4. Preserve public APIs, data formats, and user-visible behavior.
5. Run tests after meaningful steps.
6. Update docs only if structure, commands, or contributor guidance changes.

## Final report

State explicitly that behavior should be unchanged. List changed files, verification run, and any areas that need extra review.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses refactor-safely --scope project
```

Bundled into `long-running-pack`.
