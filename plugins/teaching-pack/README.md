# teaching-pack

Teach the human everything that happened in a session until they can
demonstrably explain it, via an incremental checklist and `AskUserQuestion`
quizzes.

## Components

- **Skills**: `teach-session`
- **Commands**: `/teach-session`

## Install

```sh
claude /plugin install teaching-pack@claude-harnesses
```

## Usage

```
/teach-session                # teach the human what changed this session
```

Use after a non-trivial change, a debugging session, or a hand-off when the goal
is the human's understanding rather than just a working result. The session is
treated as incomplete until the human has demonstrated understanding of every
checklist item, so pair it with the long-running ledger (`goal-manager`) for work
that spans compactions.

## Credit

Adapted from a skill by [@ThariqS](https://gist.github.com/ThariqS/1389dcdff9eba4789887a2211370f06b).
