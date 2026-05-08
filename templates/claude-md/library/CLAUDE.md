# Repository Guidance

This is a library or SDK. Public API stability is the contract.

## Principles

- Treat the public API as load-bearing. Do not change signatures, return types, or thrown errors without an explicit decision.
- Add tests for every new public surface.
- Keep docs (README, examples, API docs) in sync with code.

## Editing Expectations

- Internal refactors are fine; public API changes need a CHANGELOG entry and migration note.
- Add deprecation warnings before removing a public surface.
- Avoid widening dependencies; keep the library installable in restricted environments.

## Verification

- Run unit tests against every supported runtime/language version listed in CI.
- Run example projects (`examples/`) to confirm they still build.
- For public API changes: regenerate type declarations and check the package contents.

## Final Report

Include changed surfaces, deprecations, CHANGELOG entry, and verification across supported versions.
