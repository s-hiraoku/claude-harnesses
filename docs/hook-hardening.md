# Hook Hardening

The hooks shipped here are examples that follow consistent rules. When you adapt them, keep these properties.

## Contract

- Exit `0` → allow.
- Exit `2` → block (PreToolUse denies the tool call; Stop blocks the stop).
- Anything else → non-blocking error (Claude Code logs it; the action proceeds).

## Required behaviors

1. Honor `CLAUDE_HARNESSES_DISABLE=1` and short-circuit to exit 0.
2. Read the JSON envelope from stdin without crashing on malformed input.
3. Run in under 1 second wall clock for PreToolUse (Claude Code is waiting).
4. Never print secret values. Redact to `<prefix>... (<length> chars)`.
5. Write block reasons to stderr — Claude Code surfaces them to the user.

## Optional but recommended

- Include the matched tool name in the block reason for debuggability.
- Provide a per-hook env var to bypass (e.g. `CLAUDE_HARNESSES_ALLOW_MAIN`).
- Avoid network calls; PreToolUse hooks should be pure functions of the input.
- Avoid touching the filesystem outside the cost ledger.

## Stop hook reentrancy

A Stop hook that returns exit 2 forces Claude Code to continue. If your hook always returns 2, you have an infinite loop. Always check `stop_hook_active` in the JSON envelope and let Claude finish when that flag is `true`.
