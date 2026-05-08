# Task Ledger Patterns

A ledger is durable task memory. It survives context compactions, session restarts, and the inevitable handoff between two operators (or two Claude Code sessions).

## Files

- `ledger/current.md` — active task state, plan checklist, dated progress notes.
- `ledger/decisions.md` — durable decisions with rationale.
- `ledger/risks.md` — known risks during the work.
- `ledger/verification.md` — log of meaningful verification runs.

## When to update

- **Always**: at the start of a long-running task (set `Goal`/`Status`/`Plan`).
- **After meaningful steps**: append a dated note in `current.md` (or run `bash scripts/checkpoint.sh`).
- **When you make a decision that future sessions would re-litigate**: write it to `decisions.md`.
- **When you spot a risk you cannot resolve immediately**: write it to `risks.md`.
- **When verification produces a meaningful result**: write it to `verification.md`.

## When NOT to update

- Trivial tasks. A typo fix does not need a ledger entry.
- One-shot reviews. Quick PR reviews can finalize without touching the ledger.

## Resumption checklist

When a new session starts on a long-running task, the first action is to read `ledger/current.md` and `ledger/decisions.md`, then state in one paragraph what was last done and what comes next.
