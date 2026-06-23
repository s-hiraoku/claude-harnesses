# Current Task Ledger

Use this file to keep long-running work resumable.

## Current Goal

- Goal: Bootstrap claude-harnesses with curated hooks, skills, MCP recipes, slash commands, and a plugin marketplace.
- Owner: Claude Code
- Started: 2026-05-08
- Status: Phase 0 in progress

## Context

- Repository: claude-harnesses
- Branch: main
- Sibling reference: ../codex-harnesses
- Important files: README.md, CLAUDE.md, .claude-plugin/marketplace.json, plugins/, skills/, scripts/install.sh, docs/

## Plan

- [ ] Phase 0: bootstrap (README, CLAUDE.md, CI, verify.sh, ledger)
- [ ] Phase 1: port 8 skills from codex-harnesses
- [ ] Phase 2: plugin marketplace MVP (review/pr-guardian/tdd packs)
- [ ] Phase 3: safety + verification packs + settings presets
- [ ] Phase 4: long-running pack + remaining skills
- [ ] Phase 5: MCP pack + full umbrella
- [ ] Phase 6: docs site + examples + install.sh + CI hardening

## Progress

Record dated progress notes here.

- 2026-06-23 22:28 JST: PR #9 guard pass found failing `Eval quality gate / check` because `evals/pr-guardian/ledger.md` was missing. Also found Codex inline review comments requesting eval coverage and explicit pull-request review-comment fetching. Added `evals/pr-guardian/`, updated pr-guardian gate instructions, and verified locally with the eval gate plus repository checks.

## Blockers

- None recorded.

## Next Step

- Finish Phase 0 bootstrap and confirm CI is green.

## Checkpoints

`scripts/checkpoint.sh` appends entries here.
