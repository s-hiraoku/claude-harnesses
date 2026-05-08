# Long-Running Claude Code

Claude Code sessions can run for hours. They can also fail in ways short sessions cannot — context compaction loses data, runaway loops burn budget, and what was "the goal" two hours ago has drifted.

`long-running-pack` is the answer to each.

## SessionStart context injection

`session-context-injector` runs at every session start. It emits a short markdown block with the current branch, working-tree status, and the head of `ledger/current.md`. Claude Code receives this as additional context, so the new session knows what the previous one was working on.

## Cost ceiling

`cost-ceiling-guard` increments a per-machine counter in `~/.claude-harnesses/cost-ledger.json` on every PreToolUse. Past the threshold (default 5000 calls per 24h), it returns exit 2 to block further tool calls.

When the ceiling fires:

1. Summarize what the session accomplished in `ledger/current.md`.
2. Either delete the ledger to reset, or `export CLAUDE_HARNESSES_COST_CEILING=10000` to raise the cap intentionally.

## Plan-required-on-large-change

`plan-required-on-large-change` blocks single edits over 4000 bytes. Big edits are usually a sign that the model has skipped planning. Break the change into smaller pieces or set `CLAUDE_HARNESSES_LARGE_EDIT_OK=1` for one session.

## SessionEnd summary

`session-end-summary` appends a session-end marker so the ledger always shows where work paused.

## Goal-manager skill

`goal-manager` writes the current objective and plan into `ledger/current.md` at the start of work. Future sessions read it on resume. Combine with `/checkpoint` (also in this pack) to append timestamped progress notes.

## Long-running-orchestrator skill

`long-running-orchestrator` wires the above together: ledger init, small steps, checkpoint after each step, resume cleanly.

## Operating pattern

1. First action: `/checkpoint` to capture starting state.
2. Define an objective in `ledger/current.md` using the `goal-manager` skill.
3. Work in small steps; after each, append a dated note.
4. When verification runs, record results in `ledger/verification.md`.
5. End the session intentionally with a final summary in `ledger/current.md`.
