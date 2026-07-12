---
name: pr-guardian
description: Monitor a pull request after opening it or resume a stalled PR, fix CI failures and reviewer feedback, push updates, reply to and resolve review conversations, and comment with the outcome.
---

# PR Guardian

Use this workflow by default after opening a pull request or when resuming a stalled PR with pending CI, CodeRabbit, Codex, bot, or human review feedback. The goal is to leave the PR in a mergeable state by monitoring CI, building a complete feedback inventory, addressing actionable items, pushing focused fixes, resolving review conversations, and reporting the outcome.

## Workflow

1. Resolve the GitHub CLI before doing any PR work.
   - Resolve a usable GitHub CLI as `GH_BIN`: try `command -v gh`, the active Nix user profiles (`$HOME/.nix-profile/bin/gh` and `$HOME/.local/state/nix/profiles/profile/bin/gh`), `/run/current-system/sw/bin/gh`, then platform fallbacks such as `/opt/homebrew/bin/gh` and `/usr/local/bin/gh`. Use the resolved absolute path for every command in this workflow; desktop and sandboxed agent shells may intentionally sanitize the user's interactive `PATH`.
2. Identify the pull request, branch, remote, and expected base branch.
   - If the user says a PR is still blocked, still remains, or points at a repository PR list, enumerate the open PRs in the relevant repositories and process every PR that is `BLOCKED`, has unresolved review threads, or has actionable bot/human feedback. Do not stop after fixing only the current checkout's branch.
   - Derive the target host and repository from the resolved PR URL or remote. Run `"$GH_BIN" auth status --active --hostname <host>` and a read-only `"$GH_BIN" api --hostname <host> repos/<owner>/<repo> --jq .full_name`. An authentication failure on an unrelated host or inactive account is not a blocker. A missing executable, failed target-host authentication, or insufficient target-repository access is a concrete blocker; report the exact failed command and stderr.
3. Check the initial PR state with `gh pr view`, `gh pr checks`, recent PR comments, reviews, and inline review comments. Include `isDraft`, `mergeStateStatus`, `mergeable`, `reviewDecision`, `statusCheckRollup`, `reviews`, `latestReviews`, review requests, PR comments, pull-request review comments, and thread-aware review data in the first read.
   - Do not treat an earlier PR Guardian summary comment as current evidence. A bot review can arrive after that comment, so every resume must re-fetch PR state, comments, reviews, latest reviews, and review threads from GitHub.
   - Read `references/pr-feedback-audit.md` and execute its thread-aware GraphQL query on every target PR before deciding that no feedback remains. Paginate `reviewThreads`, REST review comments, issue comments, check runs, and check-run annotations until every `hasNextPage`/`Link: rel="next"` is exhausted. Summaries and the first 100 nodes are not a complete audit.
4. Start CI monitoring with `gh run watch` for the relevant workflow run. Use exit status when available so failures stop the loop clearly.
5. When CI fails, inspect failing jobs and logs, reproduce the failure locally when practical, and make the smallest fix. Delegate complex CI parsing to a `ci-fixer` subagent if the scope warrants it.
6. Build a complete feedback inventory across human reviews, PR comments, inline review comments, CodeRabbit, Codex, other agent comments, and CI failures. Treat top-level bot summaries such as "Actionable comments posted" as pointers, not proof that all inline comments were fetched. Read `references/pr-feedback-audit.md` for concrete `gh` and GraphQL commands when thread state, bot comments, or cross-repo scanning matters.
7. Classify every feedback item before editing:
   - `fix`: code, docs, tests, CI, or config change is needed.
   - `respond`: clarification is needed and no code change is appropriate.
   - `ignore`: duplicate, outdated, already resolved, or demonstrably wrong.
   - `blocked`: needs credentials, product decision, external service, or maintainer action.
8. Address all `fix` items with focused commits. Do not rewrite unrelated user changes or broaden the PR scope. Add or update tests when the feedback identifies behavior risk.
9. Handle every current review thread explicitly.
   - For every unresolved GitHub review thread, including outdated threads, post a per-thread reply before resolving it. Required conversation resolution is per GitHub review thread, not per PR. The merge gate "all comments must be resolved" is satisfied only when every unresolved `reviewThreads` node has been replied to or intentionally handled and then resolved.
   - For `fix` items, reply in the same review thread or directly to the thread's top-level review comment with the fix made, commit if available, and validation run.
   - For `respond` and `ignore` items, reply in the same review thread or directly to the thread's top-level review comment with the clarification or reason the suggestion is not applicable.
   - Reply before resolving. Use the thread's first review comment `fullDatabaseId` for the REST reply endpoint, then resolve the thread with the GraphQL `reviewThreads.nodes[].id`.
   - Resolve each addressed GitHub review thread after replying when permissions allow. If GitHub does not allow replying or resolving, report the thread URL as `blocked: unresolved required conversation`.
   - For top-level PR comments that cannot be resolved as review threads, add a direct reply or follow-up PR comment with a clear disposition when the comment asks a question, requests a change, or reports a blocker.
   - Do not rely on an aggregate PR comment as a substitute for per-thread disposition; repositories with required conversation resolution stay blocked until each current thread is resolved.
10. Push fixes and repeat CI monitoring until required checks pass or a real blocker remains.
11. Re-read PR state and thread-aware review data after every push and after review automation has had time to update. If CodeRabbit, Codex, or another expected review bot is `pending`, `in_progress`, or says it is still processing changes, keep waiting within the review wait window. Any unresolved-thread count gathered while a review bot is still processing is provisional and must not be reported as the final conversation state.
12. After every expected review bot reaches a terminal state, re-fetch thread-aware review data before replying, resolving, posting a final PR update, or reporting success. New bot comments can appear after CI is already green.
13. The PR is not done while `mergeStateStatus` is `BLOCKED`, `DIRTY`, `UNKNOWN`, or `BEHIND`, while `reviewDecision` is `CHANGES_REQUESTED`, while required checks are pending or failing, while any expected review bot is still processing, or while any review thread remains unresolved, even if `mergeable` says `MERGEABLE`.
14. Comment on the PR with what changed, which checks were verified, which feedback items were addressed, and which suggestions were intentionally not applied. Link to per-thread replies when suggestions are not applied. If no fixes were needed, claim merge-readiness only after the same final gate below passes; otherwise name the remaining blocker.

## Mergeability gate

Before finalizing, run a final state check such as:

```sh
"$GH_BIN" pr view <pr> --json isDraft,mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,reviews,comments,latestReviews,reviewRequests
"$GH_BIN" api repos/{owner}/{repo}/pulls/<pr>/comments --paginate
"$GH_BIN" pr checks <pr> --watch
```

Also re-run the thread-aware GraphQL query and count unresolved review threads:

```sh
"$GH_BIN" api graphql \
  -f owner='<owner>' \
  -f name='<repo>' \
  -F number=<number> \
  -f query='
query($owner:String!, $name:String!, $number:Int!) {
  repository(owner:$owner, name:$name) {
    pullRequest(number:$number) {
      reviewThreads(first:100) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          comments(first:20) {
            nodes {
              fullDatabaseId
              url
              author { login }
              body
              outdated
            }
          }
        }
      }
    }
  }
}'
```

If `pageInfo.hasNextPage` is true, paginate before counting unresolved threads. For each unresolved thread that has been handled, reply and resolve:

```sh
"$GH_BIN" api \
  --method POST \
  repos/<owner>/<repo>/pulls/<pr-number>/comments/<top-level-comment-full-database-id>/replies \
  -f body='Fixed in <commit>: <short disposition>. Verified with <command>.'

"$GH_BIN" api graphql \
  -f threadId='<review-thread-id>' \
  -f query='
mutation($threadId:ID!) {
  resolveReviewThread(input:{threadId:$threadId}) {
    thread { id isResolved }
  }
}'
```

`gh pr view --json comments,reviews` and REST pull-request review comments are useful inputs, but neither proves that every review thread is resolved.

Success requires all of these:

- `isDraft` is false. When the user owns the PR and requested merge-readiness, convert a draft with `"$GH_BIN" pr ready <pr-number-or-url> --repo <host/owner/repo>`; otherwise report the permission or author decision as a blocker. Never rely on the current branch to select the target PR.
- `mergeable` is exactly `MERGEABLE`, after retrying transient `UNKNOWN` while GitHub recomputes it.
- `mergeStateStatus` is clean enough for the repository to merge, usually `CLEAN`, `HAS_HOOKS`, or `UNSTABLE` with only non-required failures explicitly documented.
- `reviewDecision` is not `CHANGES_REQUESTED`.
- All required checks in `statusCheckRollup` pass.
- All actionable human, bot, CodeRabbit, Codex, or agent review comments are fixed, answered, or explicitly explained as not applicable in the relevant review thread or top-level PR conversation.
- Thread-aware review data shows zero unresolved review threads, including outdated threads. If any thread remains unresolved, do not report merge-ready even when `mergeable` is `MERGEABLE`; report `blocked: unresolved required conversations` with the thread URLs unless the only remaining step is a pending external reviewer action.
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
- unresolved review-thread count, including outdated threads
- PR comment posted or drafted
- remaining blockers, risks, or checks still pending
