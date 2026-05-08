# Claude Code Configuration

Claude Code reads configuration from a layered set of files. claude-harnesses ships content for each layer.

## Layers (high precedence first)

1. **Project local**: `.claude/settings.local.json` (gitignored).
2. **Project shared**: `.claude/settings.json` (committed).
3. **User**: `~/.claude/settings.json`.
4. **Plugin** components installed via `/plugin install`.
5. **Built-in defaults**.

## What goes where

| Content | Where | Why |
|---|---|---|
| Permissions presets | `.claude/settings.json` (project-shared) | Same posture for everyone on the repo |
| Personal hook overrides | `.claude/settings.local.json` | Don't make your teammates inherit your kill-switches |
| Hooks from a plugin | Auto-merged when plugin installs | Stays in sync with plugin updates |
| MCP server config | `.mcp.json` | Shared so the team's tool surface matches |
| Skills | `.claude/skills/<name>/` (committed) or via plugin | Skills are workflow content; share them |
| Subagents | `.claude/agents/<name>.md` (committed) or via plugin | Same |
| Slash commands | `.claude/commands/<name>.md` (committed) or via plugin | Same |
| CLAUDE.md | repo root | Auto-loaded by Claude Code |

## Auto-loaded files

- `CLAUDE.md` at repo root — always loaded.
- `~/.claude/CLAUDE.md` — your personal global preamble.
- `.claude/rules/*.md` — additional rule files (loaded via the `Read`/instruction loader).

## Practical setup

Most projects want this:

1. Run `bash /path/to/claude-harnesses/scripts/install.sh --target . --pack safety --pack verification --pack pr-guardian --claude-md strict --settings default --ledger`.
2. Commit the result.
3. Add `.claude/settings.local.json` to `.gitignore` (it usually already is).
4. Each contributor picks personal kill-switches in `settings.local.json`.
