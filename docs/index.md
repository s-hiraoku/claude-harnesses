# Claude Harnesses

A curated collection of hooks, skills, MCP recipes, slash commands, and subagents for **long-running, safe, high-quality Claude Code-driven development**.

Claude Code should not be expected to succeed by intelligence alone. This repository provides the durable scaffolding around it: deterministic guardrails, resumable task memory, and reusable workflows for the work that comes up over and over (review, TDD, CI fix, security review, refactor, release check).

## What it ships

- **12 plugin packs** (safety, verification, review, tdd, pr-guardian, long-running, mcp, product, research, meta, teaching, full) — installable in one command via Claude Code's plugin marketplace.
- **23 skills** with universal `SKILL.md` frontmatter — installable individually via `gh skill install` or `npx skills add`.
- **13 hooks** wired into `PreToolUse` / `PostToolUse` / `Stop` / `SessionStart` / `SessionEnd` events.
- **Curated `.mcp.json` recipes** for GitHub, Playwright, Context7, Serena, Sequential-Thinking, Sentry, and Excalidraw.
- **Settings presets** (strict / default / experimental) and **CLAUDE.md templates** (strict / frontend / library / nextjs).
- A **task ledger** pattern for sessions that span multiple compactions or runs.
- A **skill evaluation harness** (`empirical-prompt-tuning` + `evals/` + CI quality gate) that keeps every skill held to a frozen requirements checklist before merge.

## Four ways to install

See [Installation](installation.md) for the full guide. The short version:

```sh
# 1) Plugin marketplace (one command, full pack)
claude /plugin marketplace add s-hiraoku/claude-harnesses
claude /plugin install full@claude-harnesses

# 2) gh skill install (single skill)
gh skill install s-hiraoku/claude-harnesses tdd --scope project

# 3) npx skills add (single skill or all)
npx skills add s-hiraoku/claude-harnesses --skill review

# 4) scripts/install.sh (selective copy)
bash scripts/install.sh --target /path --pack pr-guardian --pack safety
```

## Why harnesses?

Long-running agent work fails when context drifts, verification is skipped, safety rules are vague, or project conventions live only in chat history. Harnesses move the important parts into durable files and deterministic checks.

## Keeping skill quality high

Skills are prompts, and the author of a prompt cannot judge its quality. Every skill in this repository goes through an empirical evaluation loop — fresh subagents execute the skill against frozen scenarios, results are scored two-sidedly, and the skill is iterated until improvements plateau. A CI gate enforces a recent passing run before any skill change merges.

See [Skill Evaluation](skill-evaluation.md) for the practical how-to, and the [empirical-prompt-tuning skill](skills/empirical-prompt-tuning.md) for the method itself.

## Sister project

This repository is a sister project to [`codex-harnesses`](https://github.com/s-hiraoku/codex-harnesses), translated and re-engineered for Claude Code's native primitives (plugins, hooks, skills, agents, slash commands, MCP).
