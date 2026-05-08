# safety-pack

Deterministic PreToolUse guards. See [safety model](../safety-model.md) for the layered defense.

| Hook | Event | Blocks |
|---|---|---|
| `secret-guard` | PreToolUse Bash/Edit/Write/MultiEdit | Likely API keys, private keys, `.env` secret assignments |
| `dangerous-command-guard` | PreToolUse Bash | `rm -rf /`, force push, `chmod -R 777`, `dd of=/dev/sd*`, `curl \| sh` |
| `branch-protection-guard` | PreToolUse Bash | direct push/commit to `main`/`master`/`production`/`release` |
| `prompt-injection-detector` | PreToolUse WebFetch/WebSearch/Read | Naive jailbreak prefixes |
| `mcp-tool-allowlist` | PreToolUse mcp__*__* | MCP tool calls outside `CLAUDE_HARNESSES_MCP_ALLOW` |

Install: `claude /plugin install safety-pack@claude-harnesses`

Kill switch: `CLAUDE_HARNESSES_DISABLE=1`. Per-hook overrides documented in the pack README.
