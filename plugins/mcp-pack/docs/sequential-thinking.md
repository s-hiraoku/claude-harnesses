# Sequential Thinking MCP

Forces step-by-step reasoning by structuring tool output around explicit thought steps. Useful for design decisions and gnarly debugging.

- **Source**: https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking
- **Auth**: none.
- **Recommended use**: architecture decisions, multi-step root-cause analysis, ambiguous requirements.
- **Last verified**: 2026-05-08

## Opt in

Move the `sequential-thinking` entry from `_disabled` into `mcpServers`. No env vars required.

## Notes

Treat the per-step output as scaffolding, not as the final answer. The point is to slow down decisions, not to replace judgment.
