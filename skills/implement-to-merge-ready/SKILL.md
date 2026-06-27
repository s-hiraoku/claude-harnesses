---
name: implement-to-merge-ready
description: Run an end-to-end Claude Code delivery workflow from user request to merge-ready pull request, including planning, implementation, tests, self-review, ready-for-review PR creation, CI/review follow-up, and final status.
---

# Implement To Merge Ready

Use this orchestration workflow when an implementation task should not stop at local code changes. Drive the work from intake through PR stabilization, composing narrower skills and tools when their trigger conditions apply.

## Workflow

1. Confirm scope and repository state.
   - Read local instructions such as `AGENTS.md` and `CLAUDE.md` before editing.
   - Inspect `git status`, branch, remotes, package scripts, tests, and relevant source structure.
   - Ask only when ambiguity would cause risky or irreversible work.
   - Preserve unrelated user changes.
2. Set a goal for substantial work.
   - Use goal tracking when the task includes implementation plus verification or PR work.
   - Write the objective in outcome terms: behavior to deliver, verification to run, PR to open, and merge-readiness follow-up.
3. Plan the implementation.
   - State a concise plan once enough context is known.
   - Choose the narrowest applicable mode: feature, bug fix, refactor, docs, frontend, backend, or CI repair.
   - Keep the plan reviewable and update it when discoveries change the work.
4. Design UI work before coding when relevant.
   - Use `ui-imagegen-director` for visual direction when UI quality or visual target matters.
   - For HTML/CSS/client-side UI work, use current frontend guidance before implementation.
   - Build the actual usable screen or flow, not a marketing placeholder, unless requested.
   - Verify responsive layouts and important states in a real browser after significant UI edits.
5. Implement in focused steps.
   - Prefer existing project patterns, APIs, and tests.
   - Keep commits and code changes scoped to the request.
   - Update docs when commands, configuration, APIs, workflows, or user-visible behavior changes.
6. Verify locally.
   - Run targeted tests first, then broader lint/type/build/test commands when practical.
   - For UI changes, run the app if needed and inspect the changed flow with browser screenshots or interaction checks.
   - If a check cannot run, capture the exact blocker and any partial verification completed.
7. Review before PR.
   - Inspect `git diff` for bugs, regressions, missing tests, data loss, security issues, and edge cases.
   - Fix actionable issues found during self-review before committing.
   - Confirm the final diff does not include unrelated files or generated noise.
8. Commit, push, and open a PR.
   - Create a clear commit history appropriate to the repo.
   - Push the branch to the expected remote.
   - Open a regular ready-for-review pull request by default.
   - Do not create a draft PR and do not pass `--draft` unless the user explicitly asks for a draft.
   - Include summary, tests, screenshots when useful, and known risks.
9. Bring the PR toward merge-ready.
   - Check required checks, CI runs, review requests, bot comments, and unresolved review threads.
   - On CI failure, inspect logs, reproduce locally when possible, make the smallest fix, push, and re-check.
   - Address actionable human, bot, CodeRabbit, Codex, and agent feedback. Use `pr-guardian` when review automation posts "Actionable comments posted", requested changes, or inline comments after the PR is opened.
   - Do not treat a PR as merge-ready while any required check, bot review, or review status is still pending. Wait and re-check at least once after the PR checks/reviews appear; if a bot such as CodeRabbit is still pending after a reasonable watch window, report the PR as "CI passed, bot review pending" rather than complete/merge-ready.
   - Before finalizing, perform a thread-aware review check when available, and report the count of unresolved current review threads. If the count is nonzero, continue addressing comments or clearly mark the PR as blocked, not merge-ready.
   - Do not merge unless the user explicitly asks and repo policy permits it.

## Skill Composition

Use narrower skills when relevant: `goal-manager`, `feature-implementation`, `bug-fix`, `refactor-safely`, `docs-updater`, `frontend-design`, `ui-imagegen-director`, `review`, `fix-ci`, and `pr-guardian`.

## Progress Updates

Keep the user informed after repository/context inspection, before edits, after local verification, after PR creation, and after CI or review follow-up.

## Final Report

Include goal status when used, changed behavior and key files, local checks, PR URL/branch, CI/review status, fixes after PR creation, unresolved current review-thread count, and remaining blockers or risks. If any check or bot review is pending, say so explicitly and do not call the PR merge-ready.
