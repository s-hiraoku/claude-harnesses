# pr-guardian-pack

Watch PRs after creation. Monitor CI, dispatch fixes via the `ci-fixer` subagent, address review feedback, and post outcome comments.

## Components

- **Skills**: `pr-guardian`, `fix-ci`
- **Subagents**: `ci-fixer`
- **Commands**: `/pr-guardian`, `/fix-ci`

## Install

```sh
claude /plugin install pr-guardian-pack@claude-harnesses
```

## Usage

```
/pr-guardian            # watch the current branch's PR
/pr-guardian 123        # watch PR #123
/fix-ci                 # repair the latest failing CI run
```

## Loop control

PR Guardian caps retries at 5 by default. After each iteration the skill writes a dated note to `ledger/current.md` so the next session can resume.
