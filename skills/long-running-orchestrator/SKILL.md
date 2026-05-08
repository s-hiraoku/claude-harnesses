---
name: long-running-orchestrator
description: Run multi-hour or multi-session work safely by combining the ledger, checkpoints, cost-ceiling guard, and resumable progress notes so context loss does not erase progress.
---

# Long-Running Orchestrator

Use this workflow when a task is expected to span context compactions, multiple Claude Code sessions, or simply too long to hold in a single context window.

## Workflow

1. Initialize the ledger.
   - Ensure `ledger/current.md` exists.
   - Write a single-paragraph objective, the success criteria, and a checklist plan.
2. Run the work in small, durable steps.
   - Make one focused change at a time.
   - After each meaningful step, append a dated note to `ledger/current.md` (or run `bash scripts/checkpoint.sh`).
   - Update verification status in `ledger/verification.md` whenever a test or build run produces a meaningful result.
3. Guard against runaway.
   - The `cost-ceiling-guard` hook (long-running-pack) tracks cumulative tool calls in `~/.claude-harnesses/cost-ledger.json` and forces a stop when the threshold is hit.
   - When a stop is forced, summarize state in `ledger/current.md` before doing anything else.
4. Resume cleanly across sessions.
   - The first action of any resume session is to read `ledger/current.md` and `ledger/decisions.md`.
   - State briefly what was last done and what comes next.
5. Complete only when:
   - The objective in the ledger is met.
   - Verification has run, with results recorded.
   - A summary of changed files, residual risks, and follow-ups is written.

## Constraints

- Never claim progress that is not reflected in the ledger.
- Never silently widen scope; if the user asks for a related-but-different change, write a new objective rather than extending the current one.

## Final Report

- objective
- final ledger pointer
- verification results
- residual risks and follow-ups
