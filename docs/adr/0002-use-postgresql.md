# ADR 0002: Use PostgreSQL

## Status

Accepted

## Context

INSight OS needs a real relational database for content, competitors, trends, ideas, reports, Brand Brain, memory, and performance data. Future semantic search may require vector support.

## Decision

Use PostgreSQL as the primary database.

## Consequences

- UUID primary keys are supported.
- Relational integrity can be enforced with foreign keys.
- JSONB can store AI traces and explainability output.
- pgvector can be added later for semantic search.

