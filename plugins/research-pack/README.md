# research-pack

Research helpers for reading public web pages that ordinary browsing, scraping, snippets, or direct fetch tools cannot read cleanly.

## Components

| Skill | Purpose |
|---|---|
| `jina-reader` | Fetch public URLs through Jina Reader and return LLM-friendly Markdown. |

| Command | Effect |
|---|---|
| `/jina-reader` | Read a URL through Jina Reader and summarize or extract requested facts. |

## Install

```sh
claude /plugin install research-pack@claude-harnesses
```

`jina-reader` is a fallback for public content only. It is not an authorization bypass and should be corroborated for current or high-stakes claims.
