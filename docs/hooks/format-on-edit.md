# format-on-edit

PostToolUse hook that formats the file Claude just edited or wrote.

## Trigger

- Event: `PostToolUse`
- Matcher: `Edit|Write|MultiEdit`

## What it does

Detects the file extension and runs the matching formatter when available:

- `.ts/.tsx/.js/.jsx/.mjs/.cjs/.json/.md/.css/.scss/.html/.yml/.yaml` → `prettier --write`
- `.py` → `ruff format` (preferred) or `black --quiet`
- `.go` → `gofmt -w`
- `.rs` → `rustfmt --quiet`

Other extensions are left alone.

## Exit codes

Always `0`. Failures are logged to stderr but never block the session.

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Notes

Requires `jq` to extract the file path from the tool input envelope. If `jq` is missing, the hook silently no-ops.

Pack: [verification-pack](../packs/verification-pack.md)
