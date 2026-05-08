# Philosophy

Long-running agent work fails in predictable ways:

1. Context drifts. The agent forgets the goal halfway through.
2. Verification is skipped. "It compiles" becomes "it works."
3. Safety rules live in chat history. Nothing enforces them.
4. Skills are re-explained every session. The same prompt boilerplate is rewritten.
5. Reviews happen too late. Mistakes propagate.

`claude-harnesses` is a deliberate response to each:

1. **Ledger** captures goal, plan, progress, decisions, risks, verification — durable across sessions and compactions.
2. **Stop-verify** hook blocks completion until `scripts/verify.sh` passes. PostToolUse hooks run format/typecheck/test on every edit.
3. **Permissions presets** + **safety-pack** PreToolUse hooks enforce safety mechanically.
4. **Skills** with frontmatter give Claude Code reusable workflow definitions; install once.
5. **Review-pack** + **pr-guardian-pack** + **tdd-pack** put review and test discipline in front of merge, not after.

Harnesses do not replace judgment. They keep the cheap mistakes from happening so judgment can focus on the expensive ones.
