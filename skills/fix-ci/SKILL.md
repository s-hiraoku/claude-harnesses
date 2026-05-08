---
name: fix-ci
description: Diagnose and repair failing CI checks on the current PR by parsing logs, reproducing locally when possible, and pushing focused fixes in batches.
---

# Fix CI

Use this workflow when CI is red on a PR. The goal is to reach green or document a real blocker.

## Workflow

1. List failing checks: `gh pr checks` and `gh run list --branch $(git branch --show-current) --limit 5`.
2. For each failing run, fetch the failing job's log: `gh run view <run-id> --log-failed`.
3. Cluster failures by type:
   - **Build / type errors**: parse compiler output for file:line and fix the immediate cause.
   - **Lint / format**: run the matching local command and apply formatter.
   - **Tests**: re-run failing tests locally if practical; classify as flake vs. real failure.
   - **Infra / dependencies**: lockfile drift, missing env vars, runner image issues.
4. Apply the smallest fix per cluster. Do not bundle unrelated cleanups.
5. Commit with messages like `fix(ci): <cluster description>` and push.
6. Loop with a hard cap (default: 5 attempts). After each attempt, record a dated note in `ledger/current.md`.
7. If a failure looks environmental (runner outage, transient network), retry once and otherwise surface to the human.

## Loop control

- Stop and report when a fix attempt does not change the failure mode.
- Stop and report when the failure indicates a real issue with the user's intended changes (not a CI-only problem).
- Never disable or skip tests as a fix unless explicitly authorized and noted.

## Final Report

Include:

- failing checks at start
- fixes applied per cluster
- commits pushed
- final CI status
- any remaining failures with classification (flake / real / environmental)
