---
name: meta-promote
description: Inspect recent Claude Code activity (history, sessions, shell, existing assets), surface repeated patterns, and promote only the high-confidence ones into Skills, subagents, or hooks. Read-only investigation; creation is gated by user approval.
---

# Meta-Promote

Use this workflow when you want recent, repeated engineering work to be packaged as the smallest useful reusable asset — a Skill, a subagent, or a hook. Avoid producing new assets that duplicate or only marginally extend existing ones.

This skill encodes a three-stage protocol: **evidence → shortlist → gated creation**.

## When to run

- The user asks to "review my recent activity and turn repeated patterns into skills / subagents / automations".
- The user explicitly invokes `/meta-promote`.

Do not run unprompted. The evidence sweep reads private history files; treat that as a deliberate user action.

## Stage 1 — Evidence (read-only)

Read the following sources, in this order. Skip a source silently if it does not exist.

1. **Prompt history**: `~/.claude/history.jsonl`
   - One JSON record per prompt. Useful fields: `display`, `project`, `timestamp`, `sessionId`.
   - Tally slash-command usage (`grep '^/'`) and natural-language phrasing.
   - Count distinct projects to judge whether a pattern is repo-specific or cross-repo.
2. **Recent sessions**: `~/.claude/projects/<encoded-path>/*.jsonl`
   - Each project directory contains `sessions-index.json` with summaries — read that first; only open full session bodies when a candidate needs corroboration.
3. **Durable guidance**: `~/.claude/CLAUDE.md` and the current project's `./CLAUDE.md`. Note any rules the user has already written down — those rules are not candidates.
4. **Shell history**: `~/.zsh_history` (fall back to `~/.bash_history`). Look for repeated CLI invocations the user runs outside Claude.
5. **Existing assets**:
   - User skills: `~/.claude/skills/` and `~/.agents/skills/`.
   - Project skills: `.claude/skills/`.
   - Repo plugins (this repo): `plugins/*` and `skills/*`.
   - Installed marketplaces: `~/.claude/plugins/marketplaces/*` and `~/.claude/plugins/cache/*` — slash commands the user already invokes often (e.g. `/release`, `/pr-guardian`) usually live here.
   - Subagents: `.claude/agents/` and inside plugins.
   - Hooks: `~/.claude/settings.json` and the project `settings.json`.

Evidence stays in scratch — do not write summaries of it to disk unless the user asks.

## Stage 2 — Candidate shortlist (with gates)

A candidate is admitted only if **all** the following gates pass:

- **Frequency**: appears at least twice in the evidence.
- **Stable I/O**: the inputs, outputs, and tools/commands used are predictable enough to script or document.
- **Material benefit**: packaging saves real time or avoids real mistakes — not just "it would be cute to automate".
- **No duplicate**: does not overlap ≥80% with an existing skill, subagent, command, or hook. If overlap exists, the right action is to **extend** the existing asset, not create a new one.

Type selection:

- Procedure / knowledge / etiquette the user wants Claude to remember → **Skill**.
- A role-bearing task the user wants to delegate to a fresh context (review, audit, focused investigation) → **subagent**.
- Repeated near-identical user invocations of the same phrasing → **Skill** with manual-invocation frontmatter. Do not create a stand-alone `/slash-command` — slash commands are surfaced from skills now.
- Something that must run on a specific event (pre-commit, post-edit, pre-tool-use) → **hook**.

Scope selection:

- Pattern specific to one project → place under that project's `.claude/`.
- Pattern recurring across multiple projects → place under user-scope `~/.claude/`.
- When this repository is the source of truth for harness distribution, prefer adding to `plugins/<pack>/` and re-exporting via `.claude-plugin/marketplace.json`.

Output the shortlist as a table with these columns:

| Pattern | Occurrences | Proposed type | Scope | Overlap with existing | Confidence |

For each row, write one sentence on **why it is worth packaging** and one on **why no existing asset already covers it**.

Then **stop and wait for approval**. Do not proceed to creation in the same turn.

## Stage 3 — Gated creation

Only after the user approves specific rows:

1. Re-check existing assets one more time for the rows being created — never write on top of an existing file without confirmation.
2. Follow the conventions of this repository when adding to it:
   - Skills go under `skills/<name>/SKILL.md` with `name:` and `description:` frontmatter.
   - Subagents go under `plugins/<pack>/agents/<name>.md` with `name:`, `description:`, optional `tools:`.
   - Slash commands that wrap a skill go under `plugins/<pack>/commands/<name>.md` and read `$ARGUMENTS`.
   - Hooks go under `plugins/<pack>/hooks.json` with deterministic shell commands.
3. Keep new files short. A SKILL.md longer than ~60 lines is usually a sign the workflow is not yet stable.
4. Update `.claude-plugin/marketplace.json` and any umbrella pack only when the new asset belongs in a pack.

For rows the user declined, record nothing on disk. Do not lobby for them again.

## Constraints

- **Never invent occurrence counts.** Cite the evidence file you derived them from.
- **Never describe a pattern as repeated when it appears only once.** Single occurrences are not candidates, even if interesting.
- **Never create more than two new assets in a single run** unless the user explicitly overrides. Skill / subagent description text loads into every future context — proliferation has a real cost.
- **Prefer extending an existing asset** to creating a new one. Say so in the shortlist when applicable.
- **Do not propose memory entries from this skill.** Memory is a separate persistence mechanism; this skill targets reusable, file-based assets.

## Final report

After Stage 2, output the shortlist plus a recommendation (which rows to create, which to skip, why). After Stage 3, list the files created or extended, the rows declined, and any follow-up the user should know about.
