# Repository Guidance

This is a frontend application. UI changes need a browser, not just type checks.

## Principles

- Follow the existing component patterns. Match the structure of nearby files.
- Preserve accessibility (ARIA, focus, keyboard navigation).
- Never break responsive layout — test mobile and desktop breakpoints.

## Editing Expectations

- Verify UI changes by running the dev server and clicking through the affected flow.
- Match existing styling conventions (Tailwind / CSS modules / Styled Components).
- Add or update component tests for non-trivial behavior.
- Avoid introducing new dependencies without checking bundle impact.

## Verification

- `npm run lint`, `npm run typecheck`, `npm test`.
- For UI changes: open the dev server, exercise the feature, watch for console errors.
- Use Playwright MCP for E2E if available (`mcp-pack`).

## Final Report

Include the routes/components touched, manual verification done, and any uncovered edge cases.
