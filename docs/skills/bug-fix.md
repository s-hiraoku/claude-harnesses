# bug-fix

Fix bugs with reproduction, minimal changes, regression coverage, and targeted verification.

## Workflow

1. Reproduce the bug, or clearly reason about it when reproduction is not practical.
2. Identify the likely cause in the current implementation.
3. Make the smallest fix that addresses the cause.
4. Add a regression test when possible.
5. Run targeted verification for the affected area.
6. Run broader checks if the fix touches shared behavior.

## Final report includes

- what failed before
- why the fix addresses it
- regression test coverage, if added
- verification run
- remaining risks

## Install

```sh
gh skill install s-hiraoku/claude-harnesses bug-fix --scope project
# or
npx skills add s-hiraoku/claude-harnesses --skill bug-fix
```

The skill is also bundled into `long-running-pack` since it's a durable workflow.
