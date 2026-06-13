# jina-reader

Fetch public URLs through Jina AI Reader and convert pages that normal tools cannot read cleanly into LLM-friendly Markdown.

## Workflow

1. Try ordinary browsing, search, or direct fetch first when those tools are suitable.
2. Use Jina Reader when the page is public but normal tools return a blank page, script shell, poor snippets, blocked parsing, or incomplete text.
3. Summarize or extract only the content requested by the user.
4. Mention uncertainty when Jina Reader returns sparse output, a login wall, deleted content, rate-limit text, or an obviously incomplete page.

## Use When

- Public pages are JavaScript-heavy, reader-hostile, or snippet-only.
- X/Twitter posts, threads, GitHub pages, PDFs, or long URLs are hard to inspect through normal fetch tools.
- The user asks to use Jina, `r.jina.ai`, or recover readable Markdown from a URL.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses jina-reader --scope project
```

Use `--scope user` when the skill should be available across projects.

Bundled into `research-pack`.
