# tdd-pack

Red-Green-Refactor TDD with strict context isolation between phases.

## Components

- **Skill**: `tdd`
- **Subagents**: `tdd-test-writer`, `tdd-implementer`, `tdd-refactorer`
- **Command**: `/tdd`

## Install

```sh
claude /plugin install tdd-pack@claude-harnesses
```

## Usage

```
/tdd add export support to the report module
```

## Why isolation matters

LLMs that see both the spec and the implementation tend to write tests that match the implementation, not the intent. Isolating phases through separate subagents lets each phase focus on a single concern:

- The **test writer** sees the spec, never the implementation.
- The **implementer** sees the failing test, never the spec.
- The **refactorer** sees post-Green code, never the spec or test design notes.

This is honor-system enforcement (each subagent's prompt forbids reading certain inputs) — combine with permissions allowlists for stronger guarantees.
