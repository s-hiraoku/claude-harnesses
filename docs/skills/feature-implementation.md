# feature-implementation

Implement a feature safely with planning, focused edits, tests, docs, and verification.

## Workflow

1. Understand the goal and user-visible behavior.
2. Inspect the existing structure, patterns, tests, and docs.
3. Make a short implementation plan.
4. Implement in small, reviewable steps.
5. Add or update tests when behavior can be tested.
6. Update docs when commands, configuration, APIs, or user behavior changes.
7. Run targeted verification during the work.
8. Run repository-level verification before finalizing when practical.

## Final report includes

- what changed
- tests or checks run
- docs updated
- known risks or follow-up work

## Install

```sh
gh skill install s-hiraoku/claude-harnesses feature-implementation --scope project
# or
npx skills add s-hiraoku/claude-harnesses --skill feature-implementation
```

Bundled into `long-running-pack`.
