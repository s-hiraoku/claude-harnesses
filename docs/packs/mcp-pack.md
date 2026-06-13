# mcp-pack

Curated `.mcp.json` recipe. Seven servers ship disabled by default; opt in per project. See [MCP Strategy](../mcp-strategy.md).

## Servers

- GitHub
- Playwright
- Context7
- Serena
- Sequential-Thinking
- Sentry
- Excalidraw

Each server has a per-server doc with auth, scopes, and last-verified date in `plugins/mcp-pack/docs/`.

## Filesystem MCP

Not recommended. Claude Code already ships first-class file tools.

Install: `claude /plugin install mcp-pack@claude-harnesses`
