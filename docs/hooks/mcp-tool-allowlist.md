# mcp-tool-allowlist

PreToolUse guard that enforces an allowlist for MCP tool calls.

## Trigger

- Event: `PreToolUse`
- Matcher: `mcp__.*__.*`

## What it blocks

Any MCP tool call (`mcp__<server>__<tool>`) that doesn't match a pattern in `CLAUDE_HARNESSES_MCP_ALLOW`. Patterns use shell glob syntax (`fnmatch`), so server-wide grants are easy:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__github__list_*,mcp__github__get_*,mcp__playwright__*"
```

If the env var is empty or unset, **every** MCP tool call is blocked. This is intentional fail-closed: unknown MCP tools should be opt-in.

## Exit codes

- `0` — allow
- `2` — block

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Recommended starters

See per-server docs under `plugins/mcp-pack/docs/` for read-only allowlist strings per server.

Pack: [safety-pack](../packs/safety-pack.md)
