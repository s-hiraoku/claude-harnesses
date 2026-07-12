# adviser

Use `adviser` as a fallback for Claude Code's native Advisor tool. It sends a bounded consultation packet to a fresh, review-only Opus Task subagent while the main agent remains responsible for execution. The review-only role is prompt-enforced unless the runtime supplies separate tool restrictions.

The default consultation gates are:

- after orientation and before choosing a consequential multi-step approach
- when failures recur or the approach changes materially
- after durable changes and verification, before completion

Short mechanical tasks do not require ritual consultation. Conflicting advice must be reconciled against repository evidence rather than followed silently.

This is workflow compatibility, not server compatibility. The fallback cannot reproduce native Advisor's automatic complete-transcript delivery, same-turn sub-inference, model-pair validation, billing and cache accounting, or `Advising` UI. It also must not describe Opus as a stronger reviewer unless the main model and runtime make that true.

Bundled into `adviser-pack`.

## Enable automatic timing

Installing the skill makes `/adviser` available, but a user-global standing instruction is needed when you want it applied to consequential tasks that never mention Adviser. Add this to `~/.claude/CLAUDE.md`:

```md
## Adviser

For consequential work that takes more than a few steps, consider an adviser at important decision points. Typical high-value checkpoints are after orientation but before committing to an approach, and after the deliverable is durable and verified but before declaring completion. These are defaults, not a fixed call quota.

Use Claude Code's native `advisor` tool when it is available. When native Advisor is unavailable, run the globally installed `adviser` skill as the fallback, preferring an Opus Task reviewer. Do not run both for ceremony.

Also consult when material ambiguity blocks a decision, failures recur, the approach stops converging, or a materially different direction is under consideration. Skip ritual consultations for short reactive work whose next action is already dictated by fresh tool output.

Keep the main Claude session responsible for execution and weigh advice against repository evidence, primary sources, and empirical verification. Do not assume the fallback received a complete transcript or uses a stronger model; report those capabilities only when verified.
```

This keeps native Advisor first and activates the fallback only in environments where it is unavailable.
