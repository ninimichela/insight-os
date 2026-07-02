# ADR 0009: Weekly Report Does Not Recalculate

## Status

Accepted

## Context

Beta Sprint 3 introduces Weekly Report. Trends and Ideas already have deterministic scores from earlier Beta sprints.

## Decision

Weekly Report reads existing data and does not recalculate:

- Trend Score
- Trend ranking
- Idea Priority
- Idea ranking

GPT may only format structured data into readable Markdown.

## Consequences

- Reports are traceable to existing Trend, Idea, and Content IDs.
- Report output remains aligned with Dashboard rankings.
- PDF and PPT remain out of scope until RC or later.
