# adviser

Use `adviser` as a fallback for Claude Code's native Advisor tool. It sends a bounded consultation packet to a fresh, tool-free Claude process on a deterministic stronger route while the main agent remains responsible for execution.

The default consultation gates are:

- after orientation and before choosing a consequential multi-step approach
- when failures recur or the approach changes materially
- after durable changes and verification, before completion

Short mechanical tasks do not require ritual consultation. Conflicting advice must be reconciled against repository evidence rather than followed silently.

This is workflow compatibility, not server compatibility. The fallback cannot reproduce native Advisor's complete-transcript delivery, same-turn sub-inference, billing and cache accounting, or `Advising` UI.

## Model and effort mapping

The policy translates Luna to Sonnet, Terra to Opus, and Sol to Fable. Sonnet and Opus callers route to Fable at the same effort. Fable callers route to the next effort in `low → medium → high → xhigh → max`; Fable/max is unavailable and fails closed.

The runner discovers effort from `CLAUDE_EFFORT` and the current model from the unique `CLAUDE_CODE_SESSION_ID` transcript. It invokes `claude -p` with explicit model and effort, no tools, safe mode, and no session persistence. Unknown or ambiguous context, recursion, route ceiling, initialization mismatch, malformed output, child failure, and timeout never trigger a weaker fallback.

Claude Code 2.1.210 exposes the effective model and empty tool list in stream JSON, but not the effective effort. Reports therefore distinguish an explicitly requested effort escalation from an independently verified effective model.

Bundled into `adviser-pack`.

## Enable automatic timing

Installing the skill makes `/adviser` available, but a user-global standing instruction is needed when you want it applied to consequential tasks that never mention Adviser. Add this to `~/.claude/CLAUDE.md`:

```md
## Adviser

For consequential work that takes more than a few steps, consider an adviser at important decision points. Typical high-value checkpoints are after orientation but before committing to an approach, and after the deliverable is durable and verified but before declaring completion. These are defaults, not a fixed call quota.

Use Claude Code's native `advisor` tool when it is available. When native Advisor is unavailable, run the globally installed `adviser` skill, which routes Sonnet or Opus to Fable at the same effort and Fable to its next effort. Do not run both for ceremony and do not substitute a weaker route.

Also consult when material ambiguity blocks a decision, failures recur, the approach stops converging, or a materially different direction is under consideration. Skip ritual consultations for short reactive work whose next action is already dictated by fresh tool output.

Keep the main Claude session responsible for execution and weigh advice against repository evidence, primary sources, and empirical verification. Do not assume the fallback received a complete transcript; report the selected route and the runner's verification limits.
```

This keeps native Advisor first and activates the fallback only in environments where it is unavailable.
