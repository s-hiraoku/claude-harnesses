# Repository Guidance

This is a Next.js application. Server/client boundaries and routing are load-bearing.

## Principles

- Respect the App Router boundary: server components by default; only mark `"use client"` when needed for interactivity.
- Server actions and route handlers must validate input and authorize the caller.
- Avoid data fetching inside client components when a server component can do it.

## Editing Expectations

- New routes go under `app/`; respect the existing layout structure.
- Server actions live in `app/_actions/` (or matching project convention); never expose secrets through them.
- Use `next/image` and `next/font` for images and fonts.
- Update `middleware.ts` only when there is a clear need.

## Verification

- `npm run lint`, `npm run typecheck`.
- `npm run build` to catch RSC/server-only issues.
- For UI: open the dev server, exercise the route, watch for hydration errors.
- For E2E: Playwright via `mcp-pack` if available.

## Final Report

Include routes/server actions touched, server vs client classification, and verification done.
