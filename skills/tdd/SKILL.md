---
name: tdd
description: Drive development with red-green-refactor using isolated test-writer, implementer, and refactorer subagents so tests reflect intent rather than anticipated implementation.
---

# Test-Driven Development

Use this workflow when implementing new behavior under TDD discipline. Context isolation between phases is enforced by delegating each step to a separate subagent so test design is not contaminated by implementation choices.

## Workflow

1. **Specify**: Restate the desired behavior in one or two sentences and identify the testing framework (jest, pytest, go test, RSpec, etc.).
2. **Red — delegate to `tdd-test-writer`**: Pass the specification only (not the source under test). The subagent writes a failing test and reports the test path and the actual failure output. If the test passes immediately, return to Specify and tighten the spec.
3. **Green — delegate to `tdd-implementer`**: Pass only the failing test path (not the original spec or any prior implementation hints). The subagent writes the smallest implementation that makes the test pass and reports the diff and the passing test output.
4. **Refactor — delegate to `tdd-refactorer`**: Pass only the post-Green code. The subagent improves clarity without changing behavior and reruns the tests to confirm they still pass.
5. **Loop**: Repeat for each behavior. Keep test scope narrow.

## Constraints

- Never let the test-writer read existing implementation code for the function under test.
- Never let the implementer read the original spec or earlier draft implementations beyond the test that is currently failing.
- Refactor only when all tests are green.
- If a test fails for an unexpected reason, treat that as a real signal: do not edit the test to make it pass without restating the spec.

## Final Report

Include:

- behavior implemented
- test files added or updated
- final test status
- refactor changes applied
- residual risks or follow-up tests to write
