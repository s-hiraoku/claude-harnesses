# mcp-pack

Curated `.mcp.json` recipe for the MCP servers most worth running with Claude Code.

## Bundled servers (all opt-in)

| Server | What it adds | Last verified |
|---|---|---|
| `github` | Issues, PRs, code search across your token's repos | 2026-05-08 |
| `playwright` | Browser automation for E2E and UI work | 2026-05-08 |
| `context7` | Version-pinned third-party docs | 2026-05-08 |
| `serena` | Semantic code retrieval over the local repo | 2026-05-08 |
| `sequential-thinking` | Step-by-step reasoning scaffolding | 2026-05-08 |
| `sentry` | Production error triage | 2026-05-08 |

See `docs/<server>.md` in this directory for per-server auth, scopes, and known limits.

## Why `_disabled` by default

MCP servers come from third parties. Their stability, scope, and security posture can change between releases. Shipping them disabled means installing the pack does not surprise you with extra processes, network calls, or write access. Move the entries you actually want from `_disabled` into `mcpServers` in your project's `.mcp.json`.

## Filesystem MCP

We do **not** recommend a filesystem MCP server. Claude Code already ships first-class file tools (Read, Edit, Write, Glob, Grep) with permissions integration; a filesystem MCP server is redundant and adds attack surface.

## Pair with safety-pack

When `safety-pack` is installed, the `mcp-tool-allowlist` hook will block any MCP tool that is not in `CLAUDE_HARNESSES_MCP_ALLOW`. Each server doc lists a starter allowlist string.
