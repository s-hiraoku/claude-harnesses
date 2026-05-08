# tdd-pack

Red-Green-Refactor TDD with strict subagent context isolation.

## Skill

- `tdd` — orchestrates the cycle, delegating each phase to an isolated subagent.

## Subagents

- `tdd-test-writer` — Red. Sees only the spec; never the implementation.
- `tdd-implementer` — Green. Sees only the failing test; never the spec or earlier drafts.
- `tdd-refactorer` — Refactor. Improves clarity post-Green without changing behavior.

## Command

- `/tdd <short behavior spec>`

## Why isolation matters

LLMs that see both the spec and the implementation tend to write tests that match the implementation, not the intent. Separate subagents enforce information boundaries.

Install: `claude /plugin install tdd-pack@claude-harnesses`
