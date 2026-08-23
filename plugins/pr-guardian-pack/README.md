# pr-guardian-pack

Watch PRs after creation or resume stalled PRs. Monitor CI, dispatch fixes via the `ci-fixer` subagent, inventory human/bot/agent review feedback, and post outcome comments.

## Components

- **Skills**: `autopilot`, `pr-guardian`, `fix-ci`
- **Subagents**: `ci-fixer`
- **Commands**: `/autopilot`, `/pr-guardian`, `/fix-ci`

## Install

```sh
claude /plugin install pr-guardian-pack@claude-harnesses
```

## Usage

```
/autopilot              # explicitly keep the current PR moving; never merge
/autopilot 123          # explicitly keep PR #123 moving; never merge
/pr-guardian            # watch the current branch's PR
/pr-guardian 123        # watch PR #123
/fix-ci                 # repair the latest failing CI run
```

## Loop control

PR Guardian caps retries at 5 by default. After each iteration the skill writes a dated note to `ledger/current.md` so the next session can resume.
