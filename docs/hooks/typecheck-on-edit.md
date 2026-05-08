# typecheck-on-edit

PostToolUse hook that runs a quick typecheck for the file Claude just edited.

## Trigger

- Event: `PostToolUse`
- Matcher: `Edit|Write`

## What it does

- `.ts/.tsx` → `tsc --noEmit -p . --pretty false` (only when `tsconfig.json` exists)
- `.py` → `mypy --no-color-output --hide-error-context <file>`

Errors stream to stderr so Claude sees them as PostToolUse output.

## Exit codes

Always `0`. Type errors are surfaced as text, not as a block.

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Notes

`tsc` runs in project mode (`-p .`) to honor the project's `tsconfig.json` and avoid spurious single-file errors. Without `tsconfig.json`, the hook skips TypeScript altogether.

Pack: [verification-pack](../packs/verification-pack.md)
