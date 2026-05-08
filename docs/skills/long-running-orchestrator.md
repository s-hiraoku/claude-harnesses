# long-running-orchestrator

Run multi-hour or multi-session work safely by combining the ledger, checkpoints, cost-ceiling guard, and resumable progress notes.

## Workflow

1. Initialize the ledger: ensure `ledger/current.md` exists; write objective + success criteria + plan checklist.
2. Run small, durable steps. After each meaningful step, append a dated note to `ledger/current.md` (or run `bash scripts/checkpoint.sh`).
3. Update `ledger/verification.md` whenever a test/build run produces a meaningful result.
4. Cost-ceiling guard (long-running-pack hook) protects against runaway loops.
5. On forced stop or session end, summarize state in `ledger/current.md` before doing anything else.
6. First action of any resume session is to read `ledger/current.md` and `ledger/decisions.md`.
7. Complete only when the objective is met, verification has run, and a summary is written.

## Constraints

- Never claim progress that is not in the ledger.
- Never silently widen scope; for related-but-different work, write a new objective.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses long-running-orchestrator --scope project
```

Part of `long-running-pack`. Pair with `/checkpoint` and the SessionStart context injector.
