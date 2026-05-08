# long-running-pack

Survive context loss across sessions and protect against runaway loops.

## Components

| Hook | Event | Purpose |
|---|---|---|
| `session-context-injector` | SessionStart | Inject git status and ledger head into the new session's context. |
| `cost-ceiling-guard` | PreToolUse | Cap cumulative tool calls per 24h window (default 5000). |
| `plan-required-on-large-change` | PreToolUse Edit/Write/MultiEdit | Block edits exceeding 4000 bytes; ask the user to break them up or set `CLAUDE_HARNESSES_LARGE_EDIT_OK=1`. |
| `session-end-summary` | SessionEnd | Append a session-end marker to the ledger. |

| Skill | Purpose |
|---|---|
| `goal-manager` | Track durable objectives in `ledger/current.md`. |
| `long-running-orchestrator` | Coordinate ledger + checkpoints + cost guard for multi-session work. |
| `feature-implementation`, `bug-fix`, `refactor-safely`, `release-check`, `docs-updater`, `deslop` | Reusable workflows already useful in long-running sessions. |

| Command | Effect |
|---|---|
| `/checkpoint` | Append a timestamped checkpoint to `ledger/current.md`. |

## Install

```sh
claude /plugin install long-running-pack@claude-harnesses
```

## Tunables

| Env var | Default | Effect |
|---|---|---|
| `CLAUDE_HARNESSES_COST_CEILING` | 5000 | Tool calls per 24h before forced stop. |
| `CLAUDE_HARNESSES_COST_PATH` | `~/.claude-harnesses/cost-ledger.json` | Override ledger location. |
| `CLAUDE_HARNESSES_LARGE_EDIT_BYTES` | 4000 | Per-edit byte threshold. |
| `CLAUDE_HARNESSES_LARGE_EDIT_OK` | unset | Set to `1` to bypass the large-edit gate for one session. |
| `CLAUDE_HARNESSES_DISABLE` | unset | Global kill switch for every hook in the pack. |
