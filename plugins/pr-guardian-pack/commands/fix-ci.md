---
description: Diagnose and repair failing CI checks on the current PR.
argument-hint: "[run-id]"
---

Run the `fix-ci` skill. If $ARGUMENTS is given, treat it as the GitHub Actions run id to start from; otherwise use the latest failing run on the current branch.

Delegate cluster-level diagnosis and fix attempts to the `ci-fixer` subagent. Cap at 5 attempts and surface remaining failures with classification (flake / real / environmental).
