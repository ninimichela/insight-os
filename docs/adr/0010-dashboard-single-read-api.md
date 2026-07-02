# ADR 0010: Dashboard Uses One Read API

## Status

Accepted

## Context

Beta Sprint 4 introduces the Dashboard. The product needs a simple first screen that answers what the content team should focus on today.

## Decision

The Dashboard will use one read-only API:

- `GET /dashboard`

It returns stats, top trends, top ideas, latest report, and recent activity in one response.

Dashboard does not recalculate data and does not trigger generation workflows.

## Consequences

- First load stays fast and predictable.
- The frontend avoids one request per section.
- Dashboard remains a decision surface instead of becoming an admin system.
