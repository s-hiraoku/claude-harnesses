---
name: pr-guardian
description: Monitor a pull request after opening it or resume a stalled PR, fix CI failures and reviewer feedback, push updates, reply to and resolve review conversations, and comment with the outcome.
---

# PR Guardian

Use this workflow by default after opening a pull request or when resuming a stalled PR with pending CI, CodeRabbit, Codex, bot, or human review feedback. The goal is to leave the PR in a mergeable state by monitoring CI, building a complete feedback inventory, addressing actionable items, pushing focused fixes, resolving review conversations, and reporting the outcome.

## Workflow

1. Identify the pull request, branch, remote, and expected base branch.
2. Check the initial PR state with `gh pr view`, `gh pr checks`, recent PR comments, reviews, and inline review comments. Include `mergeStateStatus`, `mergeable`, `reviewDecision`, `statusCheckRollup`, `reviews`, `latestReviews`, PR comments, pull-request review comments, and thread-aware review data in the first read.
3. Start CI monitoring with `gh run watch` for the relevant workflow run. Use exit status when available so failures stop the loop clearly.
4. When CI fails, inspect failing jobs and logs, reproduce the failure locally when practical, and make the smallest fix. Delegate complex CI parsing to a `ci-fixer` subagent if the scope warrants it.
5. Build a complete feedback inventory across human reviews, PR comments, inline review comments, CodeRabbit, Codex, other agent comments, and CI failures. Treat top-level bot summaries such as "Actionable comments posted" as pointers, not proof that all inline comments were fetched. Read `references/pr-feedback-audit.md` for concrete `gh` and GraphQL commands when thread state, bot comments, or cross-repo scanning matters.
6. Classify every feedback item before editing:
   - `fix`: code, docs, tests, CI, or config change is needed.
   - `respond`: clarification is needed and no code change is appropriate.
   - `ignore`: duplicate, outdated, already resolved, or demonstrably wrong.
   - `blocked`: needs credentials, product decision, external service, or maintainer action.
7. Address all `fix` items with focused commits. Do not rewrite unrelated user changes or broaden the PR scope. Add or update tests when the feedback identifies behavior risk.
8. Handle every current review thread explicitly.
   - For `fix` items, reply in the same review thread or directly to the review comment with the fix made and validation run.
   - For `respond` and `ignore` items, reply in the same review thread or directly to the review comment with the clarification or reason the suggestion is not applicable.
   - Resolve each addressed GitHub review thread when permissions allow. If GitHub does not allow replying or resolving, report the thread URL as `blocked: unresolved required conversation`.
   - Do not rely on an aggregate PR comment as a substitute for per-thread disposition; repositories with required conversation resolution stay blocked until each current thread is resolved.
9. Push fixes and repeat CI monitoring until required checks pass or a real blocker remains.
10. Re-read PR state and thread-aware review data after every push and after review automation has had time to update. The PR is not done while `mergeStateStatus` is `BLOCKED`, `DIRTY`, `UNKNOWN`, or `BEHIND`, while `reviewDecision` is `CHANGES_REQUESTED`, while required checks are pending or failing, or while any current non-outdated review thread remains unresolved, even if `mergeable` says `MERGEABLE`.
11. Comment on the PR with what changed, which checks were verified, which feedback items were addressed, and which suggestions were intentionally not applied. Link to per-thread replies when suggestions are not applied.

## Mergeability gate

Before finalizing, run a final state check such as:

```sh
gh pr view <pr> --json mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,reviews,comments
gh api repos/{owner}/{repo}/pulls/<pr>/comments --paginate
gh pr checks <pr> --watch
```

Use GraphQL or another thread-aware API when unresolved review thread state matters. `gh pr view --json comments,reviews` and REST pull-request review comments are useful inputs, but neither proves that every review thread is resolved.

Success requires all of these:

- `mergeStateStatus` is clean enough for the repository to merge, usually `CLEAN`, `HAS_HOOKS`, or `UNSTABLE` with only non-required failures explicitly documented.
- `reviewDecision` is not `CHANGES_REQUESTED`.
- All required checks in `statusCheckRollup` pass.
- All actionable human, bot, CodeRabbit, Codex, or agent review comments are fixed, answered, or explicitly explained as not applicable in the relevant review thread.
- Thread-aware review data shows zero unresolved current, non-outdated review threads. If unresolved threads remain because GitHub permissions prevent replying or resolving, report `blocked: unresolved required conversations` with the thread URLs.
- Bot reviews have had enough time to update after the last push. If checks passed but a bot review is still pending, report "checks passed, bot review pending" instead of merge-ready.

If `mergeable` is `MERGEABLE` but `mergeStateStatus` remains `BLOCKED`, keep investigating branch protection, unresolved requested changes, required review state, required conversations, or pending checks. Do not report the PR as mergeable until the blocking reason is gone or documented as an external blocker.

## Loop control

- Do not loop indefinitely. Cap retries at 5 unless the user explicitly asks for more.
- If the same failure or review comment returns after two fixes, stop broad changes and inspect the underlying assumption before trying again.
- After each CI failure, record a dated note in `ledger/current.md` so the next session can resume.
- Stop and surface to the human when a failure looks like an environmental or infrastructure issue that automated fixes cannot address.

## Final Report

Include:

- PR identifier and branch
- feedback sources inspected, including thread-aware inline review status when relevant
- CI runs watched and final status
- fixes pushed
- comments or review feedback addressed, including per-thread replies and resolved thread count
- unresolved current review-thread count
- PR comment posted or drafted
- remaining blockers, risks, or checks still pending
