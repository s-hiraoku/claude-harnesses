# Serena MCP

Semantic code retrieval and editing at the symbol level. Replaces grep-shaped searches with intent-based code navigation across 30+ languages.

- **Source**: https://github.com/oraios/serena
- **Auth**: none. Indexes the local repo on first use.
- **Recommended use**: large codebases, cross-file refactors, "find where this idea lives" queries.
- **Last verified**: 2026-05-08

## Opt in

Requires `uv` / `uvx`. Move the `serena` entry from `_disabled` into `mcpServers`.

```sh
brew install uv  # macOS, if you don't have it yet
```

If you use `safety-pack`:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__serena__find_*,mcp__serena__get_*"
```

Add write tools (`mcp__serena__edit_*`) only when intentional.
