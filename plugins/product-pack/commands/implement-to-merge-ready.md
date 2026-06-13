---
description: Implement the requested change through local verification, self-review, ready-for-review PR creation, and CI/review follow-up.
argument-hint: "<implementation request>"
---

Run the `implement-to-merge-ready` skill.

Use `$ARGUMENTS` as the implementation request. Preserve unrelated changes, create a regular ready-for-review PR by default, do not create a draft PR unless explicitly requested, and report branch, PR URL, checks, and remaining blockers.
