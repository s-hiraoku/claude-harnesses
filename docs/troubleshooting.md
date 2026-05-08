# Troubleshooting

Common issues and how to recover.

## A hook is misfiring and I cannot make progress

Set the global kill switch and recover:

```sh
export CLAUDE_HARNESSES_DISABLE=1
```

Unset when the underlying issue is resolved. This is the safety net for *every* guard hook in the repository.

## `secret-guard` blocks legitimate content

The hook matches OpenAI/GitHub/AWS-shaped strings. False positives can happen on:

- Test fixtures with realistic-looking keys
- Documentation containing `sk-...` examples

Workarounds:

- Use placeholder strings like `sk-EXAMPLE` (not 20+ chars).
- Or short-circuit the session with `CLAUDE_HARNESSES_DISABLE=1`.

## `branch-protection-guard` denies a legitimate `git commit` / `git push`

You're on `main` / `master` / `production` / `release`. Two paths:

- Acknowledge the action explicitly:
  ```sh
  CLAUDE_HARNESSES_ALLOW_MAIN=1 git commit -m "..."
  ```
- Or check out a feature branch first.

## `cost-ceiling-guard` blocked further tool calls

You hit the 24h ceiling (default 5000 tool calls). Either:

- Reset:
  ```sh
  rm ~/.claude-harnesses/cost-ledger.json
  ```
- Or raise the cap intentionally for this session:
  ```sh
  export CLAUDE_HARNESSES_COST_CEILING=10000
  ```

Before doing either, summarize state in `ledger/current.md` so you don't lose context.

## `plan-required-on-large-change` blocks every Edit

Your edits exceed 4000 bytes. Either:

- Break the edit into smaller chunks (recommended — large edits are usually a sign that planning was skipped).
- Or set a one-session bypass:
  ```sh
  export CLAUDE_HARNESSES_LARGE_EDIT_OK=1
  ```

## `stop-verify` blocks Stop on a passing repo

You probably don't have `scripts/verify.sh` at the repo root, or it's not executable. Either:

- Install it: `bash /tmp/claude-harnesses/scripts/install.sh --target . --no-verify=0` (verify is on by default).
- Or remove the verification-pack Stop hook from `.claude/settings.json`.

If the issue is real verification failure, fix the failing test/lint and the hook will pass on the next Stop.

## MCP tool calls all fail when safety-pack is installed

The `mcp-tool-allowlist` hook denies any MCP tool not in `CLAUDE_HARNESSES_MCP_ALLOW`. Set an allowlist:

```sh
export CLAUDE_HARNESSES_MCP_ALLOW="mcp__github__list_*,mcp__github__get_*,mcp__playwright__*"
```

Add patterns as you confirm each MCP tool is safe in your context.

## `scripts/install.sh` exits with `jq is required to merge hook JSON`

Install jq:

```sh
brew install jq           # macOS
apt-get install -y jq     # Debian/Ubuntu
```

If jq is unavailable, install only `--claude-md`/`--settings`/`--skills` (these don't need merging) and merge hooks manually.

## `pytest` / `mkdocs build --strict` fails locally with arch errors

You are likely running the system Python against architecture-incompatible wheels. Use a repo-local venv:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
PATH=.venv/bin:$PATH bash scripts/verify.sh
```

## Plugin install does nothing

Confirm the marketplace is added and the plugin name matches `marketplace.json`:

```sh
claude /plugin marketplace list
claude /plugin install pr-guardian-pack@claude-harnesses   # not "pr-guardian"
```

Pack names in the marketplace end in `-pack` (except `full` and `mcp-pack`).

## A hook script is not executable

```sh
chmod +x .claude/hooks/<pack>-pack/*.{sh,py}
```

`scripts/install.sh` preserves the source executable bits, so this only happens after manual editing.
