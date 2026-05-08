---
name: goal-manager
description: Manage durable task goals for long-running Claude Code work using the project ledger, including objective writing, success criteria, resumption, and completion decisions.
---

# Goal Manager

Use this workflow when a task should be tracked across sessions, compactions, or PR-bound work. Goal state lives in `ledger/current.md` so that future Claude Code sessions can resume from durable context rather than chat history.

## Workflow

1. Decide whether goal tracking is useful.
   - Track when the user asks for multi-step implementation, review, release, or PR work; when work will likely span more than one session; or when a future session may need to resume.
   - Skip for quick questions, casual brainstorming, or work that will clearly finish in one short response.
2. Shape the objective before recording it.
   - Make it outcome-focused, verifiable, and scoped to the current task.
   - Include expected verification and final reporting when they are part of the work.
   - Note any token, time, or scope budgets the user provided.
3. Persist the goal in `ledger/current.md` under "Current Goal" with `Goal`, `Owner`, `Started`, `Status` fields and a `Plan` checklist.
4. Append progress notes during the task with `scripts/checkpoint.sh` or by editing `ledger/current.md` directly. Record dated notes for major decisions, blockers, and verification runs.
5. Use the active goal during the task.
   - Re-read it after resuming, before broad edits, when the user changes direction, and before the final response.
   - If the newest user request conflicts with the active goal, follow the newest request and state the shift briefly in the ledger.
6. Complete the goal only when the real outcome is done.
   - Required implementation or investigation is complete.
   - Relevant checks have run, or blocked checks are clearly reported.
   - The final response can summarize changed files, verification, and remaining risks.

For objective examples, read `references/examples.md` only when wording is unclear.

## Final Report

Include:

- the final goal status
- what changed or was learned
- checks or verification run
- known risks, blockers, or follow-up work
- pointer to the ledger entry for future sessions
