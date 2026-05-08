# Quickstart

Five-minute setup for a typical project. Pick **one** of the four installation methods below; they all reach the same end state.

## Option A — Anthropic plugin marketplace (recommended)

From inside a Claude Code session:

```text
/plugin marketplace add s-hiraoku/claude-harnesses
/plugin install full@claude-harnesses
```

Or from the shell:

```sh
claude plugin marketplace add s-hiraoku/claude-harnesses
claude plugin install full@claude-harnesses
```

After installation, run a session and try:

```text
/checkpoint           # write a ledger entry
/verify               # run scripts/verify.sh
/review               # review the current branch
```

## Option B — APM (Agent Package Manager)

```sh
apm install s-hiraoku/claude-harnesses/full
```

Or declare it once in `apm.yml` and check it into the repo:

```yaml
plugins:
  - s-hiraoku/claude-harnesses/safety-pack
  - s-hiraoku/claude-harnesses/verification-pack
  - s-hiraoku/claude-harnesses/pr-guardian-pack
  - s-hiraoku/claude-harnesses/long-running-pack
```

```sh
apm install
```

## Option C — `gh skill install` (single skill)

```sh
gh skill install s-hiraoku/claude-harnesses tdd --scope project
gh skill install s-hiraoku/claude-harnesses review --scope project
```

## Option D — `npx skills add` (single skill or all)

```sh
npx skills add s-hiraoku/claude-harnesses --skill review
npx skills add s-hiraoku/claude-harnesses --all
```

## Optional: vendor with `scripts/install.sh`

When you want to commit the harness files into your repo without a plugin runtime:

```sh
git clone https://github.com/s-hiraoku/claude-harnesses /tmp/claude-harnesses
bash /tmp/claude-harnesses/scripts/install.sh \
  --target . \
  --pack safety --pack verification --pack pr-guardian \
  --claude-md strict \
  --settings default \
  --ledger
```

## Verify the install

```sh
ls .claude/                       # commands/, agents/, skills/, hooks/, settings.json
cat .claude/settings.json | jq '.hooks | keys'
```

You should see `PreToolUse`, `PostToolUse`, and `Stop` (depending on which packs you installed).

## First real task

1. Run `/checkpoint` once. The ledger now has a starting checkpoint.
2. Make a small code change. `format-on-edit` should reformat the file. `typecheck-on-edit` and `test-on-edit` should run silently.
3. Try a deliberate `git push --force origin main`. It should be denied by `branch-protection-guard` (or by `permissions.deny` if you used the strict preset).
4. Set `CLAUDE_HARNESSES_DISABLE=1` and confirm hooks short-circuit. Unset to re-enable.

You're done. Continue to the [Adoption Checklist](adoption-checklist.md) for tightening.
