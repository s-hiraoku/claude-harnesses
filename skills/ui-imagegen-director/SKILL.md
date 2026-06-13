---
name: ui-imagegen-director
description: Direct high-quality frontend UI work by using image-generated mockups when useful, translating the chosen direction into code, and verifying the rendered UI in a browser.
---

# UI Imagegen Director

Use this workflow when visual direction is the weak link: the user wants a polished frontend, a UI mockup, an app screen, a dashboard, a landing page, a visual redesign, or image generation to guide frontend implementation.

This skill composes three activities:

1. Create or refine a UI direction with image generation.
2. Translate the selected direction into real frontend code.
3. Verify the rendered result in a browser and iterate visually.

## Workflow

1. Inspect product context before designing.
   - audience and job-to-be-done
   - screen type: dashboard, settings, editor, commerce, landing page, game, etc.
   - existing framework, design system, component library, and constraints
   - whether the surface is an operational tool, expressive site, or immersive/game UI
2. Pick one clear visual direction before image generation.
   - Prefer a concrete direction such as refined B2B operations, editorial analytics, industrial console, playful maker tool, scientific workspace, or focused commerce catalog.
   - Decide the memorable design move: typography, information density, layout rhythm, product imagery, surface treatment, motion, or interaction model.
3. Write an implementation-oriented prompt.
   - Ask for a UI screenshot or screen mockup, not a marketing poster, unless explicitly requested.
   - Include layout regions, expected content density, states, and constraints.
   - Prohibit generic AI UI patterns: SaaS card walls, purple-blue gradient dominance, decorative blobs, fake glass, ungrounded icons, oversized hero sections for tools, and placeholder text that hides hierarchy.
4. Use image generation when a new visual target or raster asset is needed.
   - Use the available image generation tool or plugin for mockups and project-bound assets.
   - Keep generated images in the project when they are production assets.
   - Do not use a generated screenshot as the final UI. It is a reference unless the user asked for a bitmap asset.
5. Critique the generated direction before coding.
   - Check fit with product, audience, workflow, feasibility, responsive behavior, accessibility, and implementation cost.
   - If it misses the intent, do one targeted revision instead of drifting through unrelated variants.
6. Implement the chosen direction in code.
   - Reuse existing components, tokens, routing, state, and data patterns.
   - Encode the visual direction with real layout, typography, CSS variables/design tokens, states, and responsive constraints.
   - Keep operational tools efficient and scannable.
7. Verify visually in a browser after frontend changes.
   - Start or reuse the dev server.
   - Open the relevant route with Browser or Playwright when available.
   - Check desktop and mobile widths.
   - Look for text overflow, overlaps, unstable dimensions, broken assets, inaccessible contrast, blank canvases, and mismatch with the selected direction.
   - Iterate in code until the rendered UI is coherent, not merely until tests pass.

## Prompt Template

```text
Create an implementation-oriented UI mockup for <product/screen>.

Audience and job: <who uses it and what they need to accomplish>
Screen type: <dashboard/settings/editor/landing page/etc.>
Visual direction: <one concrete aesthetic direction>
Memorable design move: <typography/layout/density/media/motion/etc.>
Required regions: <navigation/header/main content/actions/states>
Content density: <sparse/balanced/dense> with realistic labels and data hierarchy
Implementation constraints: design must translate into web components and responsive CSS
Avoid: generic SaaS card walls, purple-blue gradient dominance, decorative blobs, fake glass, unreadable tiny text, marketing hero layout unless requested
Output: high-quality UI screenshot-style mockup, clear hierarchy, realistic spacing, no watermark
```

## When To Skip Image Generation

Skip generation and implement directly when the user requests a small deterministic CSS fix, the project has a strict design system, the work is primarily data correctness or accessibility remediation, or the asset is an existing SVG/vector/icon-system edit.

## Final Report

Include chosen visual direction, generated asset or mockup paths if any, implementation files changed, browser/device checks performed, and remaining visual risks.
