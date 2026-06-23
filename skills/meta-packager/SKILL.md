---
name: meta-packager
description: Analyze recent Claude Code work and package repeated patterns as the smallest useful skill, custom subagent, slash command, hook, or automation. Use when asked to mine prompts, sessions, shell history, or recent repeated work for reusable Claude Code assets.
---

# Meta Packager

Use this workflow when the user asks Claude Code to turn repeated recent work into reusable assets such as skills, custom subagents, slash commands, hooks, or automations.

## Workflow

1. Confirm the packaging scope: target repository assets by default, user-global assets only when the user asks for them, and no live service changes unless explicitly requested.
2. Collect evidence in this order: recent Claude prompts and sessions, project `CLAUDE.md`, user `~/.claude/CLAUDE.md`, shell history, then existing skills, subagents, hooks, commands, plugins, and automations. Keep collection read-only.
3. Inventory existing reusable assets before proposing anything new. Check repository-local assets first, then user-level assets such as `~/.claude/skills`, `~/.agents/skills`, `~/.claude/agents`, `~/.claude/commands`, `~/.claude/plugins`, and project `.claude/` directories.
4. Group candidate patterns by repeated user intent, not exact prompt wording. Count only eligible occurrences from the collected evidence.
5. For each candidate, record occurrence count, stable inputs, expected outputs, tools or commands used, failure modes, and overlapping existing assets.
6. Apply all creation gates before packaging: at least two occurrences, stable inputs and outputs, material time or error-reduction benefit, no existing asset already covers most of the workflow, and no repository policy conflict.
7. Choose the smallest package type that fits: skill for repeatable procedural work, custom subagent for read-heavy parallel triage with a summary returned to the parent, slash command for a thin manual trigger around an existing workflow, hook for deterministic lifecycle enforcement, automation for scheduled or event-driven behavior with clear triggers.
8. Output a shortlist table and stop for explicit user approval before editing files. If the user has already approved a specific candidate in the current request, proceed only with that candidate.
9. Create or extend only approved high-confidence items. Prefer extending an existing asset over creating a parallel skill, subagent, slash command, hook, or automation.
10. For custom subagents, include an explicit reminder that they require deliberate invocation and do not run automatically.
11. Update README or `docs/` when adding or changing reusable harness concepts, then run relevant verification.

## Evidence Hints

Useful local checks include:

```sh
tail -80 ~/.claude/history.jsonl
find ~/.claude/projects -name 'sessions-index.json' -o -name '*.jsonl' | tail -80
find ~/.claude/skills ~/.agents/skills ~/.claude/agents ~/.claude/commands -maxdepth 3 -type f 2>/dev/null
find ~/.claude/plugins -maxdepth 4 -type f 2>/dev/null
```

If a state source is unavailable, empty, or blocked by permissions, say so and continue with the remaining evidence. Do not inspect credential files or unrelated private application data. Do not quote secrets, personal content, or long session excerpts in reports; summarize only the pattern, source category, and evidence count.

## Package Rules

- Skill: procedures an agent should follow on demand, especially review loops, release checks, scaffolding, debugging playbooks, or repeated command sequences.
- Custom subagent: parallel read-heavy work such as independent security, test-gap, or maintainability scans. Avoid when work is primarily file editing or conflict-prone.
- Slash command: a thin manual trigger for an existing skill or workflow. Do not create one when skill frontmatter is enough.
- Hook: deterministic enforcement such as command guards, verification gates, or context injection.
- Automation: scheduled audits, follow-ups, notifications, or monitoring loops.
- Existing asset extension: use when an existing asset already covers most of the candidate and needs only a narrow addition.

## Creation Rules

- Write new assets into the target repository by default. Use user-global locations only when the user explicitly asks for global installation.
- For new skills, create the smallest valid skill folder with `SKILL.md`; add resources only when they materially improve reuse.
- For custom subagents, use the target repository's established `.claude/agents/` or plugin `agents/` format when one exists. If no format is discoverable, recommend the subagent contract instead of inventing a storage convention.
- For slash commands, create only thin wrappers that invoke an existing skill or stable workflow and read `$ARGUMENTS` when needed.
- For hooks, create deterministic payload scripts and tests or usage examples when practical. Document that registration is a separate integration step.
- For automations, use the available automation tooling when present. If no automation tool or project convention is available, write a proposed trigger/action spec and stop before pretending it is installed.

## Final Report

Include evidence sources inspected, unavailable sources, shortlist table, items created or extended with paths, deferred duplicates, verification commands and results, the subagent invocation reminder when any subagent candidate is created or recommended, and a note that slash commands, hooks, and automations are not active unless they were explicitly wired into the target environment.
