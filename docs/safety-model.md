# Safety Model

`claude-harnesses` layers four safety mechanisms. Each is independent.

## 1. Permissions (settings.json)

The first line of defense is `settings.json` permissions. Tools listed in `permissions.deny` are blocked before any hook runs. The `settings/{strict,default,experimental}.json` presets pre-populate sensible deny rules:

- `Bash(rm -rf /*)` and `~`/`$HOME` variants
- `Bash(git push --force*)`, `Bash(git reset --hard*)`
- `Bash(chmod -R 777*)`
- `Bash(curl * | sh*)`, `Bash(wget * | sh*)`
- `Read(.env)`, `Read(.env.*)`, `Read(**/id_rsa)`, `Read(**/*.pem)`

## 2. PreToolUse guard hooks (safety-pack)

What permissions cannot pattern-match (high-entropy strings, contextual checks), the safety-pack hooks catch:

- `secret-guard` blocks tool calls containing OpenAI/GitHub/AWS keys, private-key blocks, `.env` secret assignments.
- `dangerous-command-guard` blocks `dd of=/dev/sd*`, piped curl, etc.
- `branch-protection-guard` blocks pushes/commits to `main`/`master`/`production`/`release`.
- `prompt-injection-detector` flags naive jailbreak prefixes in `WebFetch`/`WebSearch`/`Read`.
- `mcp-tool-allowlist` enforces an allowlist for MCP tool calls.

## 3. Stop hook verification (verification-pack)

`stop-verify` blocks the Stop event until `scripts/verify.sh` passes. It honors `stop_hook_active` so it does not loop forever; if Claude Code is already inside a previously-blocked Stop, the hook lets it finish.

## 4. Cost ceiling (long-running-pack)

`cost-ceiling-guard` tracks tool call count per 24h window in `~/.claude-harnesses/cost-ledger.json` and forces a stop past the threshold (default 5000). This is the guardrail against runaway loops.

## Kill switch

Every guard honors `CLAUDE_HARNESSES_DISABLE=1`. If a hook misfires and you cannot make progress, set the variable, recover, then unset.

## What this does NOT replace

- Sandboxing the runtime (containers, restricted filesystems)
- Human review of generated PRs
- Real CI checks
- Real secrets management
