# secret-guard

PreToolUse guard that blocks tool calls likely to expose hard-coded secrets.

## Trigger

- Event: `PreToolUse`
- Matcher: `Bash|Edit|Write|MultiEdit`

## What it blocks

- OpenAI-style API keys (`sk-...`)
- GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`)
- AWS access key IDs (`AKIA...`)
- Private key blocks (`-----BEGIN ... PRIVATE KEY-----`)
- `.env`-style secret assignments (`*SECRET=`, `*TOKEN=`, `*API_KEY=`, `PASSWORD=`)

## Exit codes

- `0` — allow
- `2` — block (Claude Code denies the tool call; reason is shown to the user)

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1` — global

## Limits

Heuristic. Will miss obfuscated secrets and high-entropy strings that don't match a known prefix. Combine with `permissions.deny` for `.env` reads.

Pack: [safety-pack](../packs/safety-pack.md)
