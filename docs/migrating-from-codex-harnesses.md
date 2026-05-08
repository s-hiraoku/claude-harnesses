# Migrating from codex-harnesses

If you already use [`codex-harnesses`](https://github.com/s-hiraoku/codex-harnesses) and want the same workflow under Claude Code, here is the mapping.

## File mapping

| codex-harnesses | claude-harnesses |
|---|---|
| `AGENTS.md` | `CLAUDE.md` |
| `skills/<name>/SKILL.md` | same path; format identical |
| `hooks/<name>/hook.py` | `plugins/safety-pack/scripts/<name>.py` (rewritten for Claude's JSON envelope) |
| `policies/<name>.yaml` | `settings/<name>.json` (rewritten for Claude's permissions schema) |
| `templates/agents/<flavor>/AGENTS.md` | `templates/claude-md/<flavor>/CLAUDE.md` |
| `examples/<flavor>-project/` | `examples/<flavor>-project/` |
| `scripts/install.sh` | `scripts/install.sh` (added `--pack`) |
| `scripts/verify.sh` | `scripts/verify.sh` (env var rename only) |

## Conceptual differences

- **Hooks are not stand-alone scripts in Claude Code; they are entries in `settings.json`.** claude-harnesses ships them inside plugins so installation wires them automatically.
- **Permissions live in `settings.json`, not in YAML policies.** The translation is mechanical: `mode.approval` → `defaultMode`, `guards.block_*` → `permissions.deny` entries, `git.allow_force_push: false` → `Bash(git push --force*)` in deny.
- **Skills are first-class in Claude Code** and installable via `/plugin`, `gh skill install`, or `npx skills add`. codex-harnesses copies skill files; claude-harnesses also offers plugin-based install.

## Side-by-side adoption

You can run both at once. The skills directory (`skills/<name>/SKILL.md`) is shared in spirit between the two repos; behaviors and verification scripts overlap. Hooks differ because the lifecycle primitives differ.
