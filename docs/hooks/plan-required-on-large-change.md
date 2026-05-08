# plan-required-on-large-change

PreToolUse hook that blocks single Edit/Write/MultiEdit operations exceeding a byte threshold.

## Trigger

- Event: `PreToolUse`
- Matcher: `Edit|Write|MultiEdit`

## What it does

Computes the size of the new content for the call:

- `Write` → length of `tool_input.content`
- `Edit` → length of `tool_input.new_string`
- `MultiEdit` → sum of `new_string` across all edits

If the size exceeds the threshold (default 4000 bytes), the hook exits 2 with a recoverable message.

## Why

Big edits are usually a sign that the model has skipped planning. Breaking them up is almost always a better experience; when not, the explicit override exists.

## Exit codes

- `0` — allow
- `2` — block

## Tunables

| Env var | Default | Effect |
|---|---|---|
| `CLAUDE_HARNESSES_DISABLE` | unset | `=1` disables the hook |
| `CLAUDE_HARNESSES_LARGE_EDIT_BYTES` | `4000` | Per-edit byte threshold |
| `CLAUDE_HARNESSES_LARGE_EDIT_OK` | unset | `=1` bypasses for the current session |

Pack: [long-running-pack](../packs/long-running-pack.md)
