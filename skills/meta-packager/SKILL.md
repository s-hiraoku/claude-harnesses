---
name: meta-packager
description: Analyze recent Claude Code work and package repeated patterns as the smallest useful skill, custom subagent, slash command, hook, or automation.
---

# Meta Packager

Use this workflow when the user asks Claude Code to turn repeated recent work into reusable assets such as skills, custom subagents, slash commands, hooks, or automations.

## Workflow

1. Collect evidence in this order: recent Claude prompts and sessions, project `CLAUDE.md`, user `~/.claude/CLAUDE.md`, shell history, then existing skills, subagents, hooks, commands, plugins, and automations.
2. Inventory existing reusable assets before proposing anything new. Check repository-local assets first, then user-level assets such as `~/.claude/skills`, `~/.agents/skills`, `~/.claude/agents`, `~/.claude/commands`, `~/.claude/plugins`, and project `.claude/` directories.
3. Group candidate patterns by repeated user intent, not exact prompt wording. Count only eligible occurrences from the collected evidence.
4. For each candidate, record occurrence count, stable inputs, expected outputs, tools or commands used, failure modes, and overlapping existing assets.
5. Apply creation gates before packaging: at least two occurrences, stable inputs and outputs, material time or error-reduction benefit, no existing asset already covers most of the workflow, and no repository policy conflict.
6. Choose the smallest package type that fits.
   - Skill: repeatable procedural work.
   - Custom subagent: read-heavy parallel triage with a summary returned to the parent.
   - Slash command: a thin manual trigger for an existing workflow.
   - Hook: deterministic lifecycle enforcement.
   - Automation: scheduled or event-driven behavior with clear triggers.
7. Output a shortlist table before editing files. Mark low-confidence, one-off, or duplicate candidates as deferred.
8. Create only user-approved high-confidence items. Prefer extending an existing asset over creating a parallel asset.
9. For custom subagents, remind the user they require deliberate invocation and do not run automatically.
10. Update README or `docs/` when adding or changing reusable harness concepts, then run relevant verification.

## Evidence Hints

Useful local checks include:

```sh
tail -80 ~/.claude/history.jsonl
find ~/.claude/projects -name 'sessions-index.json' -o -name '*.jsonl' | tail -80
find ~/.claude/skills ~/.agents/skills ~/.claude/agents ~/.claude/commands -maxdepth 3 -type f 2>/dev/null
find ~/.claude/plugins -maxdepth 4 -type f 2>/dev/null
```

If a state source is unavailable, empty, or blocked by permissions, say so and continue with the remaining evidence. Do not inspect credential files or unrelated private application data.

## Package Rules

- Skill: procedures an agent should follow on demand, especially review loops, release checks, scaffolding, debugging playbooks, or repeated command sequences.
- Custom subagent: parallel read-heavy work such as independent security, test-gap, or maintainability scans. Avoid when work is primarily file editing or conflict-prone.
- Hook: deterministic enforcement such as command guards, verification gates, or context injection.
- Automation: scheduled audits, follow-ups, notifications, or monitoring loops.
- Existing asset extension: use when an existing asset already covers most of the candidate and needs only a narrow addition.

## Final Report

Include evidence sources inspected, unavailable sources, shortlist table, items created or extended with paths, deferred duplicates, verification commands and results, and the subagent invocation reminder when any subagent candidate is created or recommended.
