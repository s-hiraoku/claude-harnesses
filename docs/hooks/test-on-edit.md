# test-on-edit

PostToolUse hook that runs only the tests related to the file Claude just edited.

## Trigger

- Event: `PostToolUse`
- Matcher: `Edit|Write`

## What it does

For each edited file, locate the matching test:

- `.py` → `test_<stem>.py` or `<stem>_test.py`
- `.ts/.tsx/.js/.jsx` → `<stem>.test.*` or `<stem>.spec.*`
- Files already in `*test*`, `*spec*`, `*__tests__*` paths are themselves the target.

Then run:

- `.py` → `pytest <test_file>`
- JS/TS → `npx --no-install vitest run <file>` then fall back to `npx --no-install jest <file>`

The `find` is pruned against `node_modules`, `.venv`, `.git`, `dist`, `build`, `target`, `site` so it stays fast on large repos.

## Exit codes

Always `0`. Test failures are surfaced as stderr text, not as a block.

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

Pack: [verification-pack](../packs/verification-pack.md)
