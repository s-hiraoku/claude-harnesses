# product-pack

Product-quality workflows for frontend design, image-guided UI direction, kaizen evaluation loops, and implementation delivery through merge-ready PRs.

## Components

| Skill | Purpose |
|---|---|
| `frontend-design` | Design and implement purpose-fit frontend UI with browser verification. |
| `ui-imagegen-director` | Use image-generated mockups when they improve visual direction, then implement and verify the real UI. |
| `kaizen-loop` | Evaluate a product/codebase, propose prioritized improvements, and implement only approved items. |
| `implement-to-merge-ready` | Drive implementation from intake through tests, self-review, ready-for-review PR, and CI/review follow-up. |

| Command | Effect |
|---|---|
| `/frontend-design` | Run the frontend design workflow for the requested UI surface. |
| `/ui-imagegen-director` | Generate or use visual direction, then implement and browser-check the UI. |
| `/kaizen-loop` | Evaluate and recommend improvements, then wait for approval before editing. |
| `/implement-to-merge-ready` | Deliver the requested change through local verification and PR follow-up. |

## Install

```sh
claude /plugin install product-pack@claude-harnesses
```

Use this pack for product-facing work where the outcome depends on workflow quality, visual quality, or PR readiness rather than a single local edit.
