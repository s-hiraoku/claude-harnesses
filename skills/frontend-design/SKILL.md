---
name: frontend-design
description: Design and implement purpose-fit frontend UI with layout, typography, color, accessibility, image-generated mockups when useful, and browser verification.
---

# Frontend Design

Use this workflow for UI-heavy frontend changes where layout, hierarchy, usability, typography, spacing, color, accessibility, or responsive behavior materially affects the result.

## Workflow

1. Define the product context before changing pixels.
   - Identify the target user, primary job, key workflow, required content, and success criteria.
   - State whether the UI should feel operational, editorial, playful, data-dense, commerce-focused, or another concrete product mode.
2. Inspect the existing frontend.
   - Follow current component, routing, state, styling, token, icon, and accessibility patterns.
   - Reuse the local design system before inventing new primitives.
3. Create a short design brief.
   - State information hierarchy, main actions, navigation, empty/loading/error states, breakpoints, and content density.
   - Pick type scale, spacing, and color roles from the product purpose, not visual novelty.
4. Use image generation only when it improves direction.
   - Generate one to three UI mockups when the product purpose, composition, or visual tone is underspecified.
   - Treat generated images as references for hierarchy, density, and mood, not implementation specs.
   - Do not rely on generated text, inaccessible contrast, decorative clutter, or impossible component states.
5. Convert the direction into code-native decisions.
   - Define layout regions, component responsibilities, responsive behavior, focus order, semantic HTML, color tokens, type scale, and interaction states.
   - Prefer real content and realistic data over placeholder filler.
6. Implement in small, reviewable steps.
   - Keep visual changes scoped to the requested surface.
   - Avoid layout shifts, overlapping text, clipped controls, and viewport-specific breakage.
7. Verify in a real browser.
   - Check representative desktop and mobile viewports.
   - Exercise hover, focus, keyboard, empty, loading, error, long-text, and dense-data states when relevant.
   - Check text fit, contrast, target size, scroll behavior, and whether the primary workflow is obvious without explanatory page copy.
8. Run project verification.
   - Run lint, typecheck, tests, build, or the project-level verification script when available.
   - Capture visual risks that still need human review.

## Imagegen Prompt Template

```text
Use case: ui-mockup
Asset type: frontend design reference, not production artwork
Product context: <what this app/page/tool is for>
Audience: <target user and their level of expertise>
Primary workflow: <the main thing the user must accomplish>
Screen: <dashboard, editor, settings page, checkout, onboarding, etc.>
Information hierarchy: <top priority content, secondary content, supporting controls>
Layout direction: <density, navigation model, panels, tables, forms, canvas, etc.>
Typography: <quiet utility, editorial, technical, playful, etc.>
Color: <brand constraints or desired color roles; avoid one-note palettes>
Responsive target: <desktop, mobile, or both>
Accessibility constraints: readable contrast, visible focus states, no overlapping text, usable controls
Avoid: decorative clutter, fake unreadable microtext, impossible widgets, stock landing-page composition
```

## Final Report

Include the design goal, selected direction, whether image generation was used, changed files, browser viewport coverage, verification run, and remaining visual or accessibility risks.
