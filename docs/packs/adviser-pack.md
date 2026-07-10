# adviser-pack

Fallback strategic review for Claude Code environments where the native server-side Advisor tool is unavailable.

```text
claude /plugin install adviser-pack@claude-harnesses
```

The pack provides `/adviser` and the `adviser` skill. It consults a fresh, read-only Opus Task subagent after orientation, when work stops converging, and before substantial work is declared complete. The main Claude session retains responsibility for tools, edits, evidence checks, and final decisions.

If Opus or Task subagents are unavailable, the workflow reports the downgrade instead of implying that native Advisor ran.
