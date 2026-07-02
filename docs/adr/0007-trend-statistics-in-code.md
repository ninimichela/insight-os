# ADR 0007: Keep Trend Statistics in Code

## Status

Accepted

## Context

Beta Sprint 1 introduces the Trend Engine. The product needs stable, repeatable, and explainable trend rankings before Idea Engine consumes them.

## Decision

Trend Engine will not use GPT for clustering, ranking, scoring, growth calculation, or lifecycle calculation during Beta.

Code and database logic own:

- Topic clustering
- Trend sorting
- Trend Score
- Lifecycle
- Related content selection

GPT is allowed only in Trend Detail to explain an already calculated trend.

## Consequences

- The same dataset produces the same trend ranking.
- AI cost is lower.
- Trend Score and Lifecycle can be explained through `analysis_trace`.
- Future RC layers may add AI judgment, but only after Beta Demo proves the deterministic baseline.
