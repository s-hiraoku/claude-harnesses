# docs-updater

Update documentation after code or behavior changes while keeping docs concise and relevant.

## Workflow

1. Identify the changed behavior or workflow.
2. Find only the relevant docs.
3. Update docs concisely.
4. Avoid duplicating source code or restating implementation details.
5. Add examples where they reduce ambiguity.
6. Check links, commands, and names for consistency.

## Final report

List changed docs, what behavior they now describe, and any docs intentionally left untouched.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses docs-updater --scope project
```

Bundled into `long-running-pack`.
