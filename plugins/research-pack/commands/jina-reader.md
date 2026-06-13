---
description: Fetch a public URL through Jina Reader and summarize or extract the requested content.
argument-hint: "<url> [what to extract]"
---

Run the `jina-reader` skill.

Use `$ARGUMENTS` as the target URL and optional extraction request. Prefer the bundled `skills/jina-reader/scripts/read_url.py` script when the URL is long, contains a fragment, points at X/Twitter, or normal fetch tools returned incomplete content.
