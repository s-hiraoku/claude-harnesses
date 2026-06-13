# implement-to-merge-ready

Run an end-to-end Claude Code delivery workflow from request to merge-ready pull request.

## Use When

- The user expects implementation, verification, commit, push, PR creation, and CI/review follow-up.
- The task should end with a regular ready-for-review PR, not only local changes.
- Multiple narrower skills need to be composed into one delivery flow.

By default, open regular ready-for-review PRs. Do not create draft PRs unless explicitly requested.

Bundled into `product-pack`.
