# Hooks

| Hook | Pack | Event |
|---|---|---|
| [secret-guard](secret-guard.md) | safety-pack | PreToolUse Bash/Edit/Write/MultiEdit |
| [dangerous-command-guard](dangerous-command-guard.md) | safety-pack | PreToolUse Bash |
| [branch-protection-guard](branch-protection-guard.md) | safety-pack | PreToolUse Bash |
| [prompt-injection-detector](prompt-injection-detector.md) | safety-pack | PreToolUse WebFetch/WebSearch/Read |
| [mcp-tool-allowlist](mcp-tool-allowlist.md) | safety-pack | PreToolUse mcp__*__* |
| [format-on-edit](format-on-edit.md) | verification-pack | PostToolUse Edit/Write/MultiEdit |
| [typecheck-on-edit](typecheck-on-edit.md) | verification-pack | PostToolUse Edit/Write |
| [test-on-edit](test-on-edit.md) | verification-pack | PostToolUse Edit/Write |
| [stop-verify](stop-verify.md) | verification-pack | Stop |
| [session-context-injector](session-context-injector.md) | long-running-pack | SessionStart |
| [cost-ceiling-guard](cost-ceiling-guard.md) | long-running-pack | PreToolUse |
| [plan-required-on-large-change](plan-required-on-large-change.md) | long-running-pack | PreToolUse Edit/Write/MultiEdit |
| [session-end-summary](session-end-summary.md) | long-running-pack | SessionEnd |

All hooks honor `CLAUDE_HARNESSES_DISABLE=1`. See [hook hardening](../hook-hardening.md) for the contract every hook follows.
