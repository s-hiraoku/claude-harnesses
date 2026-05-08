# FAQ

## Why not just one big plugin?

Different teams want different surfaces. A library team wants `review-pack` + `tdd-pack`. A frontend team wants `verification-pack` + `safety-pack` + the Playwright MCP. Splitting into 7 functional packs (plus 1 umbrella) means selective install without "all or nothing."

## Why hooks at all? Settings permissions cover most of the same ground.

`permissions.deny` is the cheaper, more reliable layer; we use it first (see the [permissions model](permissions-model.md)). Hooks add what permissions cannot pattern-match: high-entropy secret detection, branch lookup at runtime, MCP allowlisting, Stop-time verification. The two layers compose.

## Why Python for guard hooks and bash for orchestration hooks?

Python has stdlib JSON parsing, deterministic exit codes, and a richer regex implementation. Bash is shorter for scripts that mostly orchestrate other tools (formatters, test runners). The shared `plugins/_shared/hook-prelude.sh` removes the boilerplate from bash hooks.

## How is this different from `codex-harnesses`?

Same idea, different agent. Skills are largely shared in spirit; hooks differ because Codex and Claude Code expose different lifecycle primitives. See [migrating from codex-harnesses](migrating-from-codex-harnesses.md).

## Can I use this in a repository that already has hooks/skills/agents?

Yes. `scripts/install.sh` deep-merges into existing `.claude/settings.json`, concatenating per-event hook arrays rather than replacing them. Existing skills/agents/commands are left in place; the install adds new ones alongside.

## Will the cost ceiling stop a productive long session?

The default ceiling is 5000 tool calls per 24 hours. A typical "long session" is 200–800 tool calls; multi-day work runs around 2000. The ceiling is a guardrail against *runaway* loops, not against productive work. Raise it with `CLAUDE_HARNESSES_COST_CEILING=10000` if you're sure.

## Are subagent context isolations actually enforced?

Honor system, not sandbox. The TDD subagents (`tdd-test-writer`, `tdd-implementer`, `tdd-refactorer`) are constrained by their prompts and their `tools` field; they do not see each other's output unless the parent agent passes it. We rely on the parent agent to honor the boundary. See the [tdd pack page](packs/tdd-pack.md) for the threat model.

## Why aren't the MCP servers enabled by default?

MCP servers come from third parties and may change scope, auth, or stability between releases. Shipping them disabled (under `_disabled` in `.mcp.json`) means installing the pack does not surprise you with extra processes, network calls, or write access. Each server has a per-server doc with `last verified` date.

## What does "harness" mean in this project?

A harness is the durable scaffolding around an autonomous agent: the durable guidance file (`CLAUDE.md`), reusable workflows (`skills/`), enforcement (`settings.json` + hooks), task memory (`ledger/`), and verification (`scripts/verify.sh`). The agent supplies intelligence; the harness supplies guardrails, memory, and reusable workflows. See [harness model](harness-model.md).

## Can I contribute a new pack?

Yes — see [CONTRIBUTING.md](https://github.com/s-hiraoku/claude-harnesses/blob/main/CONTRIBUTING.md). New packs need: a `plugin.json` validated against `schemas/plugin.schema.json`, a marketplace entry, a docs page under `docs/packs/`, and tests where applicable.

## How do I disable just one hook without uninstalling the pack?

Edit `.claude/settings.json` and remove the matching entry from the relevant event's array. Or for a single session, the global kill switch:

```sh
export CLAUDE_HARNESSES_DISABLE=1
```

## What's the relationship between skills at the repo root and skills inside packs?

The repo-root `skills/<name>/SKILL.md` is the canonical home so `gh skill install` and `npx skills add` work directly against the repo. Packs reference the same skills via relative symlinks under `plugins/<pack>/skills/`, so plugin install picks them up too. CI verifies the symlinks resolve.
