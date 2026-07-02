# ADR 0001: Use FastAPI for Backend

## Status

Accepted

## Context

INSight OS needs a backend that can expose clean APIs, integrate with Python AI tooling, support background jobs, and remain simple for early MVP development.

## Decision

Use FastAPI for the backend.

## Consequences

- Python AI integrations are straightforward.
- OpenAPI/Swagger documentation is available by default.
- The backend can evolve from MVP APIs into production services.
- The team must keep business logic out of routers and use Service/Repository layers.

