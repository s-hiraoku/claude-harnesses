# Playwright MCP

Browser automation via Playwright. Exposes navigate, fill, click, screenshot, and accessibility-snapshot tools so Claude Code can drive a real browser for E2E tests, regressions, and UI work.

- **Source**: https://github.com/microsoft/playwright-mcp
- **Auth**: none.
- **Recommended use**: E2E test scaffolding, manual exploratory regression, UI bug reproduction.
- **Last verified**: 2026-05-08

## Opt in

Move the `playwright` entry from `_disabled` into `mcpServers`. The first invocation downloads the Playwright browser bundle.

If you use `safety-pack`, allowlist the relevant tools:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__playwright__*"
```

## Notes

- Playwright runs as a separate process; cancel it via `pkill -f playwright` if a session leaks the browser.
- Per-test isolation matters for CI; see Playwright docs for `--workers` and trace settings.
