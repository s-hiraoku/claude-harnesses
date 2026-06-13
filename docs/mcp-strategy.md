# MCP Strategy

MCP servers extend Claude Code's tool surface. They are extremely useful and also a foot-gun if installed without thought.

## Recommended servers

- **GitHub** — issues, PRs, code search.
- **Playwright** — browser automation for E2E and UI work.
- **Context7** — version-pinned third-party docs.
- **Serena** — semantic code retrieval.
- **Sequential-Thinking** — step-by-step reasoning scaffolding.
- **Sentry** — production error triage.
- **Excalidraw** — hand-drawn diagrams with live local browser preview.

See per-server pages under `plugins/mcp-pack/docs/` for auth, scopes, and last-verified dates.

## Not recommended

- **Filesystem MCP** — Claude Code already has Read/Edit/Write/Glob/Grep with permissions integration. A filesystem MCP server is redundant and adds attack surface.
- **Anything that ships write tools without scoping** — only enable write tools you actively need this session.

## How many is too many

3–6 servers is the sweet spot. More servers dilute Claude's attention; the available tool list grows and tool selection gets noisy.

## Pair with safety-pack

`mcp-tool-allowlist` (in safety-pack) enforces an allowlist via `CLAUDE_HARNESSES_MCP_ALLOW`. Start with read-only tool patterns and add write tools deliberately:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__github__list_*,mcp__github__get_*,mcp__github__search_*"
```

## Per-server allowlist starters

- GitHub read: `mcp__github__list_*,mcp__github__get_*,mcp__github__search_*`
- Playwright: `mcp__playwright__*`
- Serena read: `mcp__serena__find_*,mcp__serena__get_*`
- Excalidraw: `mcp__excalidraw__*`

## Auth

Never commit auth tokens. Use shell env vars (`export GITHUB_PERSONAL_ACCESS_TOKEN=...`) and reference them in `.mcp.json`. Ship `.env.example` if you need to onboard contributors.
