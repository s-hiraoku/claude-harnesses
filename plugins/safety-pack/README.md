# safety-pack

Deterministic PreToolUse guards for safe autonomous operation.

## Components

| Hook | Event | What it blocks |
|---|---|---|
| `secret-guard` | PreToolUse Bash/Edit/Write/MultiEdit | OpenAI/GitHub/AWS keys, private-key blocks, `.env` secret assignments |
| `dangerous-command-guard` | PreToolUse Bash | `rm -rf /`, `git reset --hard`, force push, `chmod -R 777`, `dd of=/dev/sd*`, `curl \| sh` |
| `branch-protection-guard` | PreToolUse Bash | direct push/commit to `main`/`master`/`production`/`release` |
| `prompt-injection-detector` | PreToolUse WebFetch/WebSearch/Read | naive jailbreak prefixes in fetched content |
| `mcp-tool-allowlist` | PreToolUse mcp__*__* | MCP tool calls outside `CLAUDE_HARNESSES_MCP_ALLOW` |

All hooks honor `CLAUDE_HARNESSES_DISABLE=1` as a global kill switch and exit with code 2 to deny matching tool calls.

## Install

```sh
claude /plugin install safety-pack@claude-harnesses
```

## Per-hook overrides

| Env var | Effect |
|---|---|
| `CLAUDE_HARNESSES_DISABLE=1` | Disable all guard hooks. |
| `CLAUDE_HARNESSES_ALLOW_MAIN=1` | Allow direct push/commit to a protected branch for one session. |
| `CLAUDE_HARNESSES_MCP_ALLOW="mcp__github__*,mcp__playwright__*"` | Comma-separated allowlist of MCP tool patterns. |

## Limits

These hooks are heuristics. They reduce common foot-guns; they do not replace permissions, sandboxing, code review, and CI.
