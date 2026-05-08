# Installation

`claude-harnesses` supports four installation methods. Pick the one that matches how you usually adopt tooling.

## 1. Plugin marketplace (recommended)

Add the repository as a Claude Code plugin marketplace, then install the packs you want.

```sh
claude /plugin marketplace add s-hiraoku/claude-harnesses
claude /plugin install full@claude-harnesses
```

To install just one pack:

```sh
claude /plugin install pr-guardian-pack@claude-harnesses
```

Available packs: `safety-pack`, `verification-pack`, `review-pack`, `tdd-pack`, `pr-guardian-pack`, `long-running-pack`, `mcp-pack`, `full`.

## 2. `gh skill install`

For installing individual skills without the full plugin machinery.

```sh
gh skill install s-hiraoku/claude-harnesses tdd --scope project
gh skill install s-hiraoku/claude-harnesses review --scope user
```

Skills land in `.claude/skills/<name>/SKILL.md` (project scope) or `~/.claude/skills/<name>/` (user scope).

## 3. `npx skills add`

Same effect, different CLI.

```sh
npx skills add s-hiraoku/claude-harnesses --skill review
npx skills add s-hiraoku/claude-harnesses --all
```

Use `--global` for user-wide install.

## 4. `scripts/install.sh`

For projects that prefer to vendor harness files into the repository directly.

```sh
git clone https://github.com/s-hiraoku/claude-harnesses /tmp/claude-harnesses
bash /tmp/claude-harnesses/scripts/install.sh \
  --target /path/to/project \
  --pack safety --pack verification --pack pr-guardian \
  --claude-md strict --settings default \
  --ledger
```

Options:

| Flag | Purpose |
|---|---|
| `--target DIR` | Project directory (default: cwd). |
| `--pack NAME` | Install pack(s). Repeatable. |
| `--claude-md NAME` | Install `templates/claude-md/<NAME>/CLAUDE.md` as `./CLAUDE.md`. |
| `--settings NAME` | Install `settings/<NAME>.json` as `.claude/settings.json`. |
| `--skills LIST` | Install comma-separated skills, or `all`. |
| `--hooks LIST` | Install comma-separated hooks, or `all`. |
| `--ledger` | Install ledger templates. |
| `--mcp` | Install `plugins/mcp-pack/.mcp.json` template. |
| `--force` | Overwrite existing files. |
| `--dry-run` | Print actions only. |

## Comparing the methods

| Method | Best for | Granularity | Updates |
|---|---|---|---|
| Plugin marketplace | Most users | Pack-level | Auto via `/plugin update` |
| `gh skill install` | Single-skill adoption | Skill-level | Manual re-install |
| `npx skills add` | Cross-agent shared toolkit | Skill or all | Manual re-install |
| `scripts/install.sh` | Vendoring into repo | File-level | Manual re-run |
