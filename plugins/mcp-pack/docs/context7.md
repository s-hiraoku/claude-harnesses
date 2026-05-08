# Context7 MCP

Injects current third-party docs into context. Solves the "knowledge cutoff vs. monthly framework releases" gap by fetching version-specific docs on demand.

- **Source**: https://github.com/upstash/context7
- **Auth**: optional API key for higher rate limits.
- **Recommended use**: working across unfamiliar stacks, calling current SDK methods, citing accurate version-pinned API.
- **Last verified**: 2026-05-08

## Opt in

Move the `context7` entry from `_disabled` into `mcpServers`. No env vars required for default tier.

If you use `safety-pack`:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__context7__*"
```
