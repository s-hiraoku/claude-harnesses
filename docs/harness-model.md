# Harness Model

A "harness" is the durable scaffolding around an autonomous agent. The agent supplies intelligence; the harness supplies guardrails, memory, and reusable workflows.

`claude-harnesses` separates concerns into the same five layers as `codex-harnesses`, mapped to Claude Code's primitives:

| Concern | claude-harnesses | Claude Code primitive |
|---|---|---|
| Durable guidance | `CLAUDE.md`, `templates/claude-md/` | The CLAUDE.md file Claude Code auto-loads |
| Reusable workflows | `skills/<name>/SKILL.md` | `.claude/skills/` |
| External tools | `plugins/mcp-pack/.mcp.json` | `.mcp.json` |
| Enforcement | `plugins/<pack>/hooks.json` + `scripts/` | `settings.json` hooks (PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd) |
| Verification | `scripts/verify.sh`, `verification-pack` | Stop hook + slash command |
| Task memory | `ledger/` | A directory the agent treats as durable state |

## Why packs

A pack bundles components that belong together (e.g. `pr-guardian-pack` bundles a skill, a subagent, and two slash commands). Users install the packs they want; they do not have to memorize a flat list of components.

## Why settings presets

`settings/{strict,default,experimental}.json` capture the three common postures for a project. They translate the codex-harnesses YAML policies into Claude Code's permissions schema so users can drop in a starting point and edit from there.
