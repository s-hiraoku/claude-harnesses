# meta-pack

Inspect recent Claude Code activity and promote repeated patterns into the smallest useful reusable asset, with creation gated by explicit user approval.

## Components

| Skill | Purpose |
|---|---|
| `meta-promote` | Claude-specific evidence -> shortlist -> gated creation protocol. |
| `meta-packager` | General packaging workflow for repeated Claude Code work. |

| Command | Effect |
|---|---|
| `/meta-promote` | Inspect recent activity and stop after the candidate shortlist. |
| `/meta-packager` | Package approved repeated patterns as skills, subagents, commands, hooks, or automations. |

## Install

```sh
claude /plugin install meta-pack@claude-harnesses
```

Do not run this pack unprompted. The evidence sweep reads private local history and should be treated as a deliberate user action.
