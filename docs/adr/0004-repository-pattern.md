# ADR 0004: Use Repository Pattern

## Status

Accepted

## Context

Routers will otherwise become tightly coupled to SQL and hard to maintain as Content, Brand Brain, Memory, Trend, Idea, and Report logic grows.

## Decision

Use this structure:

```text
Router -> Service -> Repository -> Database
```

## Consequences

- Routers stay thin.
- Business logic lives in services.
- Database logic lives in repositories.
- Tests can target each layer more cleanly.

