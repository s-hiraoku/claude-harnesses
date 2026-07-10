# adviser

Use `adviser` as a fallback for Claude Code's native Advisor tool. It sends a bounded consultation brief to a fresh, read-only Opus Task subagent while the main agent remains responsible for execution.

The default consultation gates are:

- after orientation and before choosing a consequential multi-step approach
- when failures recur or the approach changes materially
- after durable changes and verification, before completion

Short mechanical tasks do not require ritual consultation. Conflicting advice must be reconciled against repository evidence rather than followed silently.

Bundled into `adviser-pack`.
