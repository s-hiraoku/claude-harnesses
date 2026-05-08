# review-pack

Severity-ranked code review and multi-pass security review with parallel specialist subagents.

## Skills

- `review` — bug-first review workflow, optionally parallelized via `code-reviewer` subagents.
- `security-review` — multi-pass security review, parallel `security-auditor` subagents per concern.
- `simplify` — review changed code for reuse and dead complexity.

## Subagents

- `code-reviewer` — severity-ranked review, returns structured findings.
- `security-auditor` — single-concern specialist (injection, authn/authz, secrets, supply chain, IaC, business logic).

## Commands

- `/review [PR# or scope]`
- `/security-review [scope]`

Install: `claude /plugin install review-pack@claude-harnesses`
