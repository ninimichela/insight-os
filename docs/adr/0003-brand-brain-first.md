# ADR 0003: Brand Brain First

## Status

Accepted

## Context

The product should not be a generic AI writing tool. It should help commercial real estate teams make better brand-specific content decisions.

## Decision

Brand Brain is a first-class concept. AI generation must eventually read brand positioning, tone, keywords, avoid words, historical performance, and content memory before producing recommendations.

## Consequences

- Brand knowledge belongs in data/config, not hard-coded prompts.
- Prompt output should differ by project even when the same prompt is used.
- MVP may start with seed JSON, then move to database-backed Brand Brain.

