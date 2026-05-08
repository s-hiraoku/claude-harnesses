# prompt-injection-detector

PreToolUse guard that flags suspected prompt-injection patterns in WebFetch/WebSearch/Read input.

## Trigger

- Event: `PreToolUse`
- Matcher: `WebFetch|WebSearch|Read`

## What it blocks

Naive jailbreak prefixes commonly found in scraped hostile content:

- "Ignore (all/previous/prior/above) instructions"
- "Disregard (the) system prompt"
- "You are now (DAN/jailbroken/unrestricted)"
- "Enable developer mode"
- "Print/reveal/show (the) system prompt"

## Exit codes

- `0` — allow
- `2` — block

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Limits

Heuristic. It will not catch sophisticated payloads (encoded, multilingual, hidden in markdown), but it will catch the common naive cases. Combine with conservative permissions on `WebFetch` and `Read` of untrusted paths.

Pack: [safety-pack](../packs/safety-pack.md)
