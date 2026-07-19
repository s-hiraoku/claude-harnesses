# review-pack

Severity-ranked code review and multi-pass security review with parallel specialist subagents.

## Components

- **Skills**: `review`, `review-briefing`, `security-review`, `simplify`
- **Subagents**: `code-reviewer`, `security-auditor`
- **Commands**: `/review`, `/security-review`

## Install

```sh
claude /plugin install review-pack@claude-harnesses
```

## Usage

```
/review                       # review current branch vs origin/main
/review 123                   # review PR #123
/review-briefing 123          # prepare a read-only human-review briefing
/security-review              # security review of current diff
```
