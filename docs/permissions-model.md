# Permissions Model

Claude Code uses `.claude/settings.json` to express permissions. The `permissions` object has three knobs:

- `defaultMode`: starting permission mode for the session. Common values:
  - `default` — ask the user for risky actions.
  - `plan` — start in plan mode; nothing executes until a plan is approved.
  - `acceptEdits` — auto-approve edits.
- `allow`: list of patterns that auto-approve matching tool calls.
- `deny`: list of patterns that block matching tool calls before any hook runs.

## Pattern syntax

- `Bash(<glob>)` matches a Bash command. Globs use `*` as the wildcard.
- `Read(<glob>)` matches Read tool with a path matching the glob.
- Bare tool names (`Read`, `Glob`, `Grep`) match the entire tool.
- MCP tools are matched as `mcp__<server>__<tool>`.

## Three presets

- `settings/strict.json` — `defaultMode: plan`, narrow allow list, broad deny list. Use for production-impacting or sensitive repos.
- `settings/default.json` — `defaultMode: default`, sensible allow list for common dev commands.
- `settings/experimental.json` — `defaultMode: acceptEdits`, only deny for clearly destructive ops. Use for greenfield prototyping where speed matters.

## Combining with hooks

`permissions.deny` is the cheaper, more reliable layer; use it first. Hooks add what permissions cannot express (high-entropy detection, branch lookups, environment-aware checks).
