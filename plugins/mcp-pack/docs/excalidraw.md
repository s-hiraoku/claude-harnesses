# Excalidraw MCP

Creates and edits Excalidraw diagrams through an MCP server with a real-time local browser preview.

- **Package**: https://www.npmjs.com/package/@scofieldfree/excalidraw-mcp
- **Command**: `npx -y @scofieldfree/excalidraw-mcp`
- **Auth**: none.
- **Recommended use**: Architecture sketches, flow diagrams, and visual explanations with live Excalidraw preview.
- **Last verified**: 2026-06-06

## Opt in

Move the `excalidraw` entry from `_disabled` into `mcpServers`.

If you use `safety-pack`, allowlist the relevant tools:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__excalidraw__*"
```

## Notes

- The first run downloads `@scofieldfree/excalidraw-mcp` via `npx`.
- The server starts a local HTTP/WebSocket preview server on port 3100 by default.
- Stop leaked sessions by terminating the `excalidraw-mcp` or matching `npx` process.
