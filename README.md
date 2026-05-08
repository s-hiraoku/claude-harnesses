# claude-harnesses

[![Verify](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/verify.yml/badge.svg)](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/verify.yml)
[![GitHub Pages](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/pages.yml/badge.svg)](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/pages.yml)

`claude-harnesses` is a curated collection of hooks, skills, MCP recipes, slash commands, and subagents for **long-running, safe, high-quality Claude Code-driven software development**.

Claude Code should not be expected to succeed by intelligence alone. This repository provides the durable scaffolding around it: deterministic guardrails, resumable task memory, and reusable workflows for the work that comes up over and over (review, TDD, CI fix, security review, refactor, release check).

The user guide is published at **[s-hiraoku.github.io/claude-harnesses](https://s-hiraoku.github.io/claude-harnesses/)**.

## Four ways to install

Pick whichever fits how you usually adopt tooling.

### 1) Plugin marketplace (recommended)

```sh
claude /plugin marketplace add s-hiraoku/claude-harnesses
claude /plugin install full@claude-harnesses
```

Or install just the pack you need:

```sh
claude /plugin install pr-guardian-pack@claude-harnesses
claude /plugin install safety-pack@claude-harnesses
claude /plugin install tdd-pack@claude-harnesses
```

Available packs: `safety-pack`, `verification-pack`, `review-pack`, `tdd-pack`, `pr-guardian-pack`, `long-running-pack`, `mcp-pack`, `full`.

### 2) `gh skill install`

```sh
gh skill install s-hiraoku/claude-harnesses tdd --scope project
gh skill install s-hiraoku/claude-harnesses review --scope user
```

### 3) `npx skills add`

```sh
npx skills add s-hiraoku/claude-harnesses --skill review
npx skills add s-hiraoku/claude-harnesses --all
```

### 4) `scripts/install.sh`

```sh
git clone https://github.com/s-hiraoku/claude-harnesses /tmp/claude-harnesses
bash /tmp/claude-harnesses/scripts/install.sh \
  --target /path/to/project \
  --pack pr-guardian --pack safety --pack verification \
  --claude-md strict --settings default --ledger
```

See [docs/installation.md](docs/installation.md) for the full comparison.

## What it ships

| Category | Items |
|---|---|
| **Plugin packs** | safety, verification, review, tdd, pr-guardian, long-running, mcp, full |
| **Skills** (14) | bug-fix, feature-implementation, refactor-safely, review, release-check, docs-updater, goal-manager, pr-guardian, tdd, security-review, simplify, fix-ci, deslop, long-running-orchestrator |
| **Hooks** (13) | secret-guard, dangerous-command-guard, branch-protection-guard, prompt-injection-detector, mcp-tool-allowlist, stop-verify, format-on-edit, typecheck-on-edit, test-on-edit, session-context-injector, cost-ceiling-guard, plan-required-on-large-change, session-end-summary |
| **MCP recipes** | GitHub, Playwright, Context7, Serena, Sequential-Thinking, Sentry |
| **Slash commands** | `/verify`, `/review`, `/security-review`, `/tdd`, `/fix-ci`, `/pr-guardian`, `/checkpoint` |
| **Subagents** | code-reviewer, security-auditor, tdd-test-writer, tdd-implementer, tdd-refactorer, ci-fixer |
| **Settings presets** | strict, default, experimental |
| **CLAUDE.md templates** | strict, frontend, library, nextjs |

## Why harnesses

Long-running agent work fails when context drifts, verification is skipped, safety rules are vague, or project conventions live only in chat history. Harnesses move the important parts into durable files and deterministic checks.

Use this repository to help Claude Code:

- keep durable guidance close to the code
- reuse task workflows instead of re-explaining them
- record long-running task state in a ledger
- run checks before stopping
- block obviously unsafe commands and leaked secrets
- separate guidance, tools, memory, enforcement, and verification

## Harness model

- `CLAUDE.md`: durable project guidance.
- `skills/`: reusable task workflows, each in a directory with `SKILL.md`.
- `plugins/`: bundled packs (skills + hooks + agents + commands) with `.claude-plugin/plugin.json` manifests.
- `.mcp.json`: external tool and knowledge access.
- Hooks (under each pack's `hooks.json` + `scripts/`): deterministic scripts wired to Claude Code's lifecycle events.
- `settings/`: example `settings.json` profiles (strict / default / experimental).
- `ledger/`: resumable task memory for long-running work.
- `scripts/`: verification and checkpoint utilities.

## Kill switch

All guard hooks honor `CLAUDE_HARNESSES_DISABLE=1`. Set it to recover from a misfiring hook without editing config.

## Sister project

[`codex-harnesses`](https://github.com/s-hiraoku/codex-harnesses) provides the same idea for Codex. Skills are largely shared in spirit; hooks differ because Codex and Claude Code expose different lifecycle primitives.

## Non-goals

This repository does not:

- implement a multi-agent router
- provide a production hook runtime
- implement an MCP server
- replace project-specific tests or review
- guarantee safety without sandboxing, settings.json permissions, and human review

## License

[MIT](LICENSE).
