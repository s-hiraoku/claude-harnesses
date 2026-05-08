# full

Umbrella plugin that pulls in every functional pack:

- `safety-pack` — PreToolUse guards
- `verification-pack` — format/typecheck/test on edit + Stop verification
- `review-pack` — code review + security review with parallel subagents
- `tdd-pack` — Red-Green-Refactor with isolated subagents
- `pr-guardian-pack` — watch PRs to green
- `long-running-pack` — SessionStart context, cost guard, ledger
- `mcp-pack` — curated `.mcp.json` recipes

## Install

```sh
claude /plugin install full@claude-harnesses
```

If `dependsOn` is not yet supported by your Claude Code version, install each pack individually:

```sh
for pack in safety-pack verification-pack review-pack tdd-pack pr-guardian-pack long-running-pack mcp-pack; do
  claude /plugin install "${pack}@claude-harnesses"
done
```
