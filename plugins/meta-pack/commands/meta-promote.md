---
description: Inspect recent Claude Code activity and surface repeated patterns that should become Skills, subagents, or hooks. Read-only investigation; creation is gated by your approval.
argument-hint: "[optional focus: e.g. 'last 7 days', 'this project only', a topic keyword]"
---

Run the `meta-promote` skill.

If `$ARGUMENTS` is non-empty, treat it as a scope or focus hint (time window, project filter, or a topic keyword). Otherwise, sweep the default sources at user scope.

Stop after presenting the candidate shortlist and wait for explicit approval before creating any asset.
