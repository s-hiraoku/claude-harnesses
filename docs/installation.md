# Installation

`claude-harnesses` supports four installation methods. Pick the one that matches how you usually adopt tooling.

## 1. Anthropic plugin marketplace (recommended)

Use Claude Code's built-in plugin system. Add this repository as a marketplace, then install the pack you want from inside a Claude Code session.

```text
/plugin marketplace add s-hiraoku/claude-harnesses
/plugin install full@claude-harnesses
```

Use `/plugin` (no arguments) to browse the marketplace interactively, or install a specific pack:

```text
/plugin install safety-pack@claude-harnesses
/plugin install verification-pack@claude-harnesses
/plugin install review-pack@claude-harnesses
/plugin install tdd-pack@claude-harnesses
/plugin install pr-guardian-pack@claude-harnesses
/plugin install long-running-pack@claude-harnesses
/plugin install mcp-pack@claude-harnesses
/plugin install product-pack@claude-harnesses
/plugin install research-pack@claude-harnesses
/plugin install meta-pack@claude-harnesses
/plugin install teaching-pack@claude-harnesses
```

You can run the same flow non-interactively from the shell:

```sh
claude plugin marketplace add s-hiraoku/claude-harnesses
claude plugin install pr-guardian-pack@claude-harnesses
```

Add `--scope project` to commit the install to `.claude/`, or `--scope local` to keep it private to your machine.

Available packs: `safety-pack`, `verification-pack`, `review-pack`, `tdd-pack`, `pr-guardian-pack`, `long-running-pack`, `mcp-pack`, `product-pack`, `research-pack`, `meta-pack`, `teaching-pack`, `full`.

Useful follow-ups:

- `/plugin marketplace list` — see registered marketplaces
- `/plugin marketplace remove claude-harnesses` (or `rm`) — remove the marketplace
- `/plugin update claude-harnesses` — pull the latest

## 2. APM — Agent Package Manager

[APM](https://github.com/microsoft/apm) is a cross-agent dependency manager (like `package.json` for AI agents). It works with Claude Code, Cursor, Copilot, and others, and reproduces the same setup across machines.

Install one pack directly:

```sh
apm install s-hiraoku/claude-harnesses/safety-pack
apm install s-hiraoku/claude-harnesses/pr-guardian-pack
```

Pin to a tag or branch:

```sh
apm install s-hiraoku/claude-harnesses/tdd-pack#v0.1.0
```

Or declare the dependencies in `apm.yml` and run `apm install` to reproduce the setup:

```yaml
# apm.yml
plugins:
  - s-hiraoku/claude-harnesses/safety-pack
  - s-hiraoku/claude-harnesses/verification-pack
  - s-hiraoku/claude-harnesses/pr-guardian-pack
  - s-hiraoku/claude-harnesses/long-running-pack
  - s-hiraoku/claude-harnesses/product-pack
```

```sh
apm install
```

APM resolves the plugin manifests under `plugins/<name>/.claude-plugin/plugin.json` and wires the components into your client's expected layout.

## 3. `gh skill install` — single skill at a time

For installing individual skills without the full plugin machinery. Skills are picked up by Claude Code (and other agents that follow the universal `SKILL.md` format).

```sh
gh skill install s-hiraoku/claude-harnesses tdd --scope project
gh skill install s-hiraoku/claude-harnesses review --scope user
```

Pin to a tag or branch:

```sh
gh skill install s-hiraoku/claude-harnesses tdd@v0.1.0 --scope project
```

| Scope | Lands in | Shared with team |
|---|---|---|
| `--scope project` | `.claude/skills/<name>/` | Yes (commit it) |
| `--scope user` | `~/.claude/skills/<name>/` | No |

Available skills: `bug-fix`, `feature-implementation`, `refactor-safely`, `review`, `release-check`, `docs-updater`, `goal-manager`, `pr-guardian`, `tdd`, `security-review`, `simplify`, `fix-ci`, `deslop`, `long-running-orchestrator`, `empirical-prompt-tuning`, `teach-session`, `meta-packager`, `frontend-design`, `ui-imagegen-director`, `implement-to-merge-ready`, `kaizen-loop`, `jina-reader`.

## 4. `npx skills add` — single skill or all of them

Same idea as `gh skill install`, different CLI. Works without GitHub CLI installed.

```sh
npx skills add s-hiraoku/claude-harnesses --skill review
npx skills add s-hiraoku/claude-harnesses --skill tdd --skill security-review
npx skills add s-hiraoku/claude-harnesses --all
```

Use `--global` to install user-wide instead of project-local.

### Companion Skills for Vercel Frontends

For React, Next.js, and Vercel-hosted frontend work, install Vercel's official skills alongside the local harness skills:

```sh
npx skills add vercel-labs/agent-skills --global --skill vercel-react-best-practices vercel-composition-patterns vercel-react-view-transitions web-design-guidelines
npx skills add vercel-labs/next-skills --global --skill next-best-practices
```

Use `vercel-react-best-practices` for React and Next.js performance patterns, `vercel-composition-patterns` for component APIs, `vercel-react-view-transitions` for React view transition work, and `web-design-guidelines` for UI, accessibility, and UX review. Add `next-cache-components` or `next-upgrade` from `vercel-labs/next-skills` only for projects that need those specific Next.js workflows.

## Optional: vendor with `scripts/install.sh`

When you want to commit the harness files directly into your repo (no plugin runtime, no per-skill CLI), clone this repo and run:

```sh
git clone https://github.com/s-hiraoku/claude-harnesses /tmp/claude-harnesses
bash /tmp/claude-harnesses/scripts/install.sh \
  --target /path/to/project \
  --pack safety --pack verification --pack pr-guardian \
  --claude-md strict --settings default \
  --ledger
```

| Flag | Purpose |
|---|---|
| `--target DIR` | Project directory (default: cwd). |
| `--pack NAME` | Install pack(s). Repeatable. |
| `--claude-md NAME` | Install `templates/claude-md/<NAME>/CLAUDE.md` as `./CLAUDE.md`. |
| `--settings NAME` | Install `settings/<NAME>.json` as `.claude/settings.json`. |
| `--skills LIST` | Install comma-separated skills, or `all`. |
| `--ledger` | Install ledger templates. |
| `--mcp` | Install `plugins/mcp-pack/.mcp.json` template. |
| `--no-verify` | Skip installing `scripts/verify.sh` (installed by default). |
| `--force` | Overwrite existing files. |
| `--dry-run` | Print actions only. |

## Comparing the four methods

| Method | Best for | Granularity | Updates | Cross-agent |
|---|---|---|---|---|
| Plugin marketplace | Most Claude Code users | Pack-level | `/plugin update` | Claude Code only |
| APM | Reproducible cross-agent setups (CI, dotfiles) | Pack-level via `apm.yml` | `apm install` re-run | Yes (Claude Code, Cursor, Copilot, etc.) |
| `gh skill install` | One specific skill | Skill-level | Manual re-install | Multi-agent (universal SKILL.md) |
| `npx skills add` | Same as gh skill, no GitHub CLI required | Skill-level or all | Manual re-install | Multi-agent (universal SKILL.md) |
