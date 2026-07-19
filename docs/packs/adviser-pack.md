# adviser-pack

Fallback strategic review for Claude Code environments where the native server-side Advisor tool is unavailable.

```text
claude /plugin install adviser-pack@claude-harnesses
```

The pack provides `/adviser` and the `adviser` skill. It consults a fresh, tool-free Fable process after orientation, when work stops converging, and before substantial work is declared complete. Sonnet and Opus callers preserve their effort; Fable callers move to the next effort. The main Claude session retains responsibility for tools, edits, evidence checks, and final decisions.

Unknown parent context, Fable/max, and failed or unverifiable child execution stop without a weaker fallback.
