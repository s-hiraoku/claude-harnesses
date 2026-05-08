# long-running-pack

Survive context loss across sessions, and protect against runaway loops. See [Long-Running Claude Code](../long-running-claude.md) for the full operating pattern.

## Hooks

- `session-context-injector` — SessionStart context (git status + ledger head).
- `cost-ceiling-guard` — PreToolUse counter; default 5000 calls / 24h.
- `plan-required-on-large-change` — PreToolUse Edit/Write/MultiEdit; default 4000-byte threshold.
- `session-end-summary` — SessionEnd marker in the ledger.

## Skills

- `goal-manager`, `long-running-orchestrator`
- Plus the durable workflow set: `feature-implementation`, `bug-fix`, `refactor-safely`, `release-check`, `docs-updater`, `deslop`.

## Command

- `/checkpoint`

## Tunables

| Env var | Default | Effect |
|---|---|---|
| `CLAUDE_HARNESSES_COST_CEILING` | 5000 | Tool calls per 24h before forced stop. |
| `CLAUDE_HARNESSES_LARGE_EDIT_BYTES` | 4000 | Per-edit byte threshold. |
| `CLAUDE_HARNESSES_LARGE_EDIT_OK` | unset | Set to `1` to bypass the large-edit gate for one session. |

Install: `claude /plugin install long-running-pack@claude-harnesses`
