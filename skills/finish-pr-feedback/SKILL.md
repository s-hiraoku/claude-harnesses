---
name: finish-pr-feedback
description: Compatibility alias for pr-guardian. Use pr-guardian for stalled pull requests, CodeRabbit/Codex review feedback, CI failures, and merge-ready PR follow-up.
---

# Finish PR Feedback

This skill name is retained for compatibility with existing prompts. Use `pr-guardian` for the actual workflow.

When invoked, immediately switch to the `pr-guardian` workflow and treat the request as a PR follow-up run. `pr-guardian` now owns CI monitoring, complete review feedback inventory, `fix`/`respond`/`ignore`/`blocked` classification, CodeRabbit/Codex inline comment handling, re-check loops, and the final mergeability gate.
