# autopilot

Autopilot is the explicit, user-triggered entry point for keeping a pull request moving until it is merge-ready without merging it.

It delegates all monitoring, feedback auditing, current-head review checks, and readiness decisions to generated references copied byte-for-byte from the canonical `pr-guardian` workflow. This keeps one source of truth for pagination, durable-runner behavior, review-thread resolution, and stabilization without exposing PR Guardian as a second model-invocable Skill in the standalone plugin.

## Usage

```text
/autopilot
/autopilot 123
/autopilot https://github.com/owner/repo/pull/123
```

Bare `/autopilot` is available when the root Skill is installed directly. Claude Code namespaces plugin Skills and commands, so use the matching form after a marketplace install:

```text
/skill-autopilot:autopilot 123
/pr-guardian-pack:autopilot 123
/full:autopilot 123
```

The skill sets `disable-model-invocation: true`, so ordinary PR work does not start Autopilot implicitly. Only a user invocation grants the bounded follow-up loop.

Autopilot may reconcile conflicts, fix actionable feedback or CI, push focused changes, and resolve addressed review threads. It never merges, enables auto-merge, force-pushes, closes the PR, or broadens scope without separate authorization.

For fork pull requests, Autopilot reads the head repository, head ref, and head SHA from GitHub, verifies the push remote targets that repository, and pushes the explicit head ref. It never substitutes the base repository's same-named branch.

Install it individually:

```text
/plugin install skill-autopilot@claude-harnesses
```

It is also included in `pr-guardian-pack` and `full`. Install `skill-autopilot` when you want only the explicit entry point; the larger packs also expose their normal model-invocable PR Guardian workflow.
