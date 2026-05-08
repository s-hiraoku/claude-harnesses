# goal-manager

Track durable task goals across sessions, compactions, and PR-bound work using the project ledger.

## Workflow

1. Decide whether goal tracking is useful.
   - Track when work spans multiple sessions, compactions, or PR rounds.
   - Skip for one-off questions or trivial tasks.
2. Shape the objective: outcome-focused, verifiable, scoped.
3. Persist the goal in `ledger/current.md` under "Current Goal" with `Goal`, `Owner`, `Started`, `Status`, and a `Plan` checklist.
4. Append progress notes during work — `bash scripts/checkpoint.sh` or direct edits.
5. Re-read the ledger when resuming. State briefly what was last done and what comes next.
6. Complete only when the real outcome is done, verification has run, and a summary is recorded.

## Examples

See `skills/goal-manager/references/examples.md` for translations from informal requests to concrete objectives.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses goal-manager --scope project
```

Bundled into `long-running-pack`. Pair with the `/checkpoint` slash command.
