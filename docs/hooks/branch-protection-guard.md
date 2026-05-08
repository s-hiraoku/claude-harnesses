# branch-protection-guard

PreToolUse guard that blocks direct push or commit to protected branches.

## Trigger

- Event: `PreToolUse`
- Matcher: `Bash`

## What it blocks

- `git push [origin] {main,master,production,release}` (any combination)
- `git commit` while on a protected branch (verified at runtime via `git branch --show-current`)

When the current branch cannot be determined (no git, detached HEAD, timeout), commit is **fail-closed**: blocked with a recoverable message.

## Exit codes

- `0` — allow (early return when text doesn't contain `"git"`)
- `2` — block

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1` — global
- `CLAUDE_HARNESSES_ALLOW_MAIN=1` — per-session bypass to acknowledge an intentional protected-branch action

## Notes

The `"git" not in text` early return keeps the hot-path fast on the common Bash command (no fork unless the command actually mentions git).

Pack: [safety-pack](../packs/safety-pack.md)
