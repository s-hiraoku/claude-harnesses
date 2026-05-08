# Sentry MCP

Wires Claude Code into your Sentry organization so it can read recent errors, group by frequency, and pull stack traces while triaging.

- **Source**: https://github.com/getsentry/sentry-mcp
- **Auth**: `SENTRY_AUTH_TOKEN` with `event:read`, `project:read`, `org:read` scopes.
- **Recommended use**: production triage, "what's currently on fire" queries, stack-trace-driven bug fixing.
- **Last verified**: 2026-05-08

## Opt in

```sh
export SENTRY_AUTH_TOKEN=...
```

Move the `sentry` entry from `_disabled` into `mcpServers`.

If you use `safety-pack`:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__sentry__list_*,mcp__sentry__get_*"
```
