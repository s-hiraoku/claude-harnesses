# claude-harnesses

[![Verify](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/verify.yml/badge.svg)](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/verify.yml)
[![GitHub Pages](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/pages.yml/badge.svg)](https://github.com/s-hiraoku/claude-harnesses/actions/workflows/pages.yml)

`claude-harnesses` is a curated collection of hooks, skills, MCP recipes, slash commands, and subagents for **long-running, safe, high-quality Claude Code-driven software development**.

Claude Code should not be expected to succeed by intelligence alone. This repository provides the durable scaffolding around it: deterministic guardrails, resumable task memory, and reusable workflows for the work that comes up over and over (review, TDD, CI fix, security review, refactor, release check).

The user guide is published at **[s-hiraoku.github.io/claude-harnesses](https://s-hiraoku.github.io/claude-harnesses/)**.

## Four ways to install

Pick whichever fits how you usually adopt tooling.

### 1) Anthropic plugin marketplace (recommended)

From inside a Claude Code session:

```text
/plugin marketplace add s-hiraoku/claude-harnesses
/plugin install full@claude-harnesses
```

Or install just the pack you need:

```text
/plugin install pr-guardian-pack@claude-harnesses
/plugin install safety-pack@claude-harnesses
/plugin install tdd-pack@claude-harnesses
```

The same flow works non-interactively from the shell:

```sh
claude plugin marketplace add s-hiraoku/claude-harnesses
claude plugin install full@claude-harnesses
```

Available packs: `safety-pack`, `verification-pack`, `review-pack`, `tdd-pack`, `pr-guardian-pack`, `long-running-pack`, `mcp-pack`, `full`.

### 2) APM (Agent Package Manager)

[APM](https://github.com/microsoft/apm) is a cross-agent dependency manager that works with Claude Code, Cursor, Copilot, and others.

```sh
apm install s-hiraoku/claude-harnesses/full
# or pin to a tag
apm install s-hiraoku/claude-harnesses/tdd-pack#v0.1.0
```

Or declare the dependencies in `apm.yml` and run `apm install` to reproduce the same setup across machines.

### 3) `gh skill install`

```sh
gh skill install s-hiraoku/claude-harnesses tdd --scope project
gh skill install s-hiraoku/claude-harnesses review --scope user
```

### 4) `npx skills add`

```sh
npx skills add s-hiraoku/claude-harnesses --skill review
npx skills add s-hiraoku/claude-harnesses --all
```

For vendoring harness files directly into your repo without a plugin runtime, see [`scripts/install.sh`](docs/installation.md#optional-vendor-with-scriptsinstallsh).

See [docs/installation.md](docs/installation.md) for the full comparison.

## What it ships

| Category | Items |
|---|---|
| **Plugin packs** | safety, verification, review, tdd, pr-guardian, long-running, mcp, full |
| **Skills** (15) | bug-fix, feature-implementation, refactor-safely, review, release-check, docs-updater, goal-manager, pr-guardian, tdd, security-review, simplify, fix-ci, deslop, long-running-orchestrator, empirical-prompt-tuning |
| **Hooks** (13) | secret-guard, dangerous-command-guard, branch-protection-guard, prompt-injection-detector, mcp-tool-allowlist, stop-verify, format-on-edit, typecheck-on-edit, test-on-edit, session-context-injector, cost-ceiling-guard, plan-required-on-large-change, session-end-summary |
| **MCP recipes** | GitHub, Playwright, Context7, Serena, Sequential-Thinking, Sentry |
| **Slash commands** | `/verify`, `/review`, `/security-review`, `/tdd`, `/fix-ci`, `/pr-guardian`, `/checkpoint` |
| **Subagents** | code-reviewer, security-auditor, tdd-test-writer, tdd-implementer, tdd-refactorer, ci-fixer |
| **Settings presets** | strict, default, experimental |
| **CLAUDE.md templates** | strict, frontend, library, nextjs |

## Skill evaluation (quality gate)

Skills are prompts, and the author of a prompt can't judge its quality. Every skill in this repo goes through an empirical evaluation loop:

1. Freeze 2–3 realistic scenarios with `[critical]`-tagged requirements in `evals/<skill>/scenarios.yaml`.
2. Dispatch fresh subagents (one per scenario, in parallel) via the Task tool.
3. Score two-sided: executor self-report + frozen requirements checklist (pass/fail, accuracy, tool steps, duration).
4. Apply the minimum fix; loop with a NEW subagent until improvements plateau.
5. Append a passing entry to `evals/<skill>/ledger.md`.

CI (`eval-quality-gate.yml`) blocks any PR that modifies `skills/<name>/SKILL.md` without a recent passing ledger entry. Trivial fixes can opt out with `[skip-eval]` in the PR description.

The method is published as the [`empirical-prompt-tuning` skill](skills/empirical-prompt-tuning/SKILL.md). Full how-to and copy-paste prompt template: [docs/skill-evaluation.md](docs/skill-evaluation.md).

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
