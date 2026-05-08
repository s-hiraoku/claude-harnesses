# Adoption Checklist

A 30-minute pass to adopt `claude-harnesses` for a new repo.

## 0. Pick a posture

| Posture | Use when |
|---|---|
| `strict` | Production / sensitive / library |
| `default` | Most app development |
| `experimental` | Solo prototype |

## 1. Install the basics

```sh
git clone https://github.com/s-hiraoku/claude-harnesses /tmp/claude-harnesses
bash /tmp/claude-harnesses/scripts/install.sh \
  --target . \
  --pack safety --pack verification --pack pr-guardian \
  --claude-md <strict|frontend|library|nextjs> \
  --settings <strict|default|experimental> \
  --ledger
```

## 2. Confirm the wiring

- `cat .claude/settings.json` — should show merged hooks.
- `ls .claude/hooks/` — should show pack subdirs with scripts.
- `ls .claude/skills/` — should show review/pr-guardian/fix-ci/etc.
- `cat CLAUDE.md` — should be your chosen template.

## 3. Verify

```sh
bash scripts/verify.sh
```

## 4. Try the harness once

Pick a small real task. Use `/review` or `/checkpoint`. Watch:

- `format-on-edit` should run on saves.
- `secret-guard` should block if you intentionally write `sk-AAAA...` somewhere.
- `stop-verify` should re-prompt when verify.sh fails.

## 5. Tighten

- Add project-specific deny rules to `.claude/settings.json`.
- Update `CLAUDE.md` with project-specific guidance (it should be small).
- If using MCP, edit `.mcp.json` to opt in to the servers you actually want.

## 6. Document

Add to your repo's CONTRIBUTING:

> This repo uses `claude-harnesses`. Run `bash scripts/verify.sh` before opening a PR.

You're done.
