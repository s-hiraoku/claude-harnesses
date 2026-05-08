# Decisions

Use this file for durable decisions that future Claude Code sessions should respect.

## Template

### YYYY-MM-DD: Decision Title

- Decision:
- Context:
- Alternatives considered:
- Rationale:
- Consequences:

## Decisions

### 2026-05-08: Plugin marketplace as primary distribution surface

- Decision: Ship `.claude-plugin/marketplace.json` listing 7 functional packs + 1 umbrella `full` pack as the primary distribution path. Support `gh skill install`, `npx skills add`, and `scripts/install.sh` as alternates.
- Context: Users want one-command install. Plugin marketplace is Claude Code's native discovery mechanism.
- Alternatives considered: a single monolithic plugin; copy-only via scripts/install.sh; per-skill repos.
- Rationale: Plugin marketplace gives users selective install of cohesive packs; the four distribution paths cover every preference.
- Consequences: Skills must live at repo root `skills/` for `gh skill`/`npx skills` compatibility, and packs reference them via relative symlinks. CI must validate that symlinks resolve.

### 2026-05-08: Hook scripts are Python by default

- Decision: Guard hooks (secret-guard, dangerous-command-guard, branch-protection-guard, prompt-injection-detector, mcp-tool-allowlist, cost-ceiling-guard, plan-required-on-large-change) are Python 3.10+. Orchestration hooks (stop-verify, format/typecheck/test-on-edit, session-context-injector, session-end-summary) are bash.
- Context: Claude Code passes a JSON envelope on stdin (`{tool_name, tool_input, ...}`). Reliable parsing in bash is fragile.
- Alternatives considered: bash for everything (uses jq); Node.js (extra dependency).
- Rationale: stdlib `json` is universally available; deterministic exit codes are easier to reason about.
- Consequences: Documented `python3 >= 3.10` runtime requirement in SECURITY.md.
