# GitHub MCP

The most-installed MCP server. Exposes Claude Code to issues, pull requests, code search, and repository metadata across any repo your token can see.

- **Source**: https://github.com/modelcontextprotocol/servers/tree/main/src/github
- **Auth**: `GITHUB_PERSONAL_ACCESS_TOKEN` with `repo`, `read:org`, `workflow` scopes for full coverage. Use a fine-grained token scoped to specific repositories where possible.
- **Recommended use**: querying issues/PRs, searching repos, reading workflow status. Combine with `pr-guardian-pack` for end-to-end PR automation.
- **Last verified**: 2026-05-08

## Opt in

Move the `github` entry from `_disabled` into `mcpServers` in `.mcp.json` and export the token:

```sh
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_yourtokenhere
```

If you use `safety-pack`, allowlist the read tools:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__github__list_*,mcp__github__get_*,mcp__github__search_*"
```

Add write tools (`mcp__github__create_*`, `mcp__github__update_*`) only when you intentionally need write access in this session.
