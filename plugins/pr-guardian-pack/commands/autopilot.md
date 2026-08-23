---
description: Explicitly keep a PR moving until it is merge-ready without merging it.
argument-hint: "[PR URL or number]"
disable-model-invocation: true
---

Run the `autopilot` skill for $ARGUMENTS. If no argument is supplied, target the current branch's pull request.

Use the bundled PR Guardian references as the sole monitoring and merge-readiness workflow. Do not merge, enable auto-merge, force-push, close the PR, or create a separate polling loop.
