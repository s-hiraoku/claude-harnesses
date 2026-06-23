# meta-pack

Inspect recent Claude Code activity and package repeated patterns into the smallest useful reusable asset, with creation gated by explicit user approval.

## Components

| Skill | Purpose |
|---|---|
| `meta-packager` | Evidence -> shortlist -> gated creation workflow for repeated Claude Code work. |

| Command | Effect |
|---|---|
| `/meta-packager` | Inspect recent activity, shortlist candidates, and package approved repeated patterns as skills, subagents, commands, hooks, or automations. |

## Install

```sh
claude /plugin install meta-pack@claude-harnesses
```

Do not run this pack unprompted. The evidence sweep reads private local history and should be treated as a deliberate user action.
